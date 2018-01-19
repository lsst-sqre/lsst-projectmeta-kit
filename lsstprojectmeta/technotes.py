"""Reduce technote projects into JSON-LD metadata.
"""

__all__ = ('get_ltd_product_urls', 'process_technote_products',
           'process_technote', 'reduce_technote_metadata')

import asyncio
import datetime
import re

import yaml

from .github.urls import parse_repo_slug_from_url, make_raw_content_url
from .github.graphql import github_request, GitHubQuery


TECHNOTE_HANDLE_PATTERN = re.compile(r'^(sqr|dmtn|smtn)-\d+')


async def get_ltd_product_urls(session):
    """Get URLs for LSST the Docs (LTD) products from the LTD Keeper API.

    Parameters
    ----------
    session : `aiohttp.ClientSession`
        Your application's aiohttp client session.
        See http://aiohttp.readthedocs.io/en/stable/client.html.

    Returns
    -------
    product_urls : `list`
        List of product URLs.
    """
    product_url = 'https://keeper.lsst.codes/products/'
    async with session.get(product_url) as response:
        data = await response.json()

    return data['products']


async def process_technote_products(session, product_urls, github_api_token,
                                    mongo_collection=None):
    """Run a pipeline to process extract, transform, and load metadata for
    multiple technote projects

    Parameters
    ----------
    github_url : `str`
        URL of the technote's GitHub repository.
    session : `aiohttp.ClientSession`
        Your application's aiohttp client session.
        See http://aiohttp.readthedocs.io/en/stable/client.html.
    github_api_token : `str`
        A GitHub personal API token. See the `GitHub personal access token
        guide`_.
    mongo_collection : `motor.motor_asyncio.AsyncIOMotorCollection`, optional
        MongoDB collection. This should be the common MongoDB collection for
        LSST projectmeta JSON-LD records.
    """
    tasks = [asyncio.ensure_future(
             process_technote(session, github_api_token,
                              ltd_product_url=product_url,
                              mongo_collection=mongo_collection))
             for product_url in product_urls]
    await asyncio.gather(*tasks)


async def process_technote(session, github_api_token,
                           ltd_product_url=None,
                           github_url=None,
                           mongo_collection=None):
    """ETL pipeline for a technote resource.

    Parameters
    ----------
    session : `aiohttp.ClientSession`
        Your application's aiohttp client session.
        See http://aiohttp.readthedocs.io/en/stable/client.html.
    github_api_token : `str`
        A GitHub personal API token. See the `GitHub personal access token
        guide`_.
    ltd_product_url : `str`, optional
        URL of the technote's product resource in the LTD Keeper API. This
        URL can be used instead of providing a ``github_url``.
    github_url : `str`, optional
        URL of a technote's GitHub repository. If provided, this URL is
        used instead of ``ltd_product_url`` as the root of the data pipeline.
    mongo_collection : `motor.motor_asyncio.AsyncIOMotorCollection`, optional
        MongoDB collection. This should be the common MongoDB collection for
        LSST projectmeta JSON-LD records. If provided, ths JSON-LD is upserted
        into the MongoDB collection.

    Returns
    -------
    metadata : `dict`
        JSON-LD-formatted dictionary.

    .. `GitHub personal access token guide`: https://ls.st/41d
    """
    print('starting {} | {}'.format(ltd_product_url, github_url))
    if github_url is None:
        async with session.get(ltd_product_url) as response:
            ltd_product_data = await response.json()
        print(ltd_product_data)
        product_name = ltd_product_data['slug']

        # Ensure the product is a technote
        technote_series_match = TECHNOTE_HANDLE_PATTERN.match(product_name)
        if technote_series_match is None:
            # TODO could log or raise an exception here?
            print('{} is not a technote'.format(product_name))
            return

        github_url = ltd_product_data['doc_repo']
        print(github_url)
    else:
        # The LSST the Docs product resource wasn't downloaded
        ltd_product_data = {}

    # Strip the .git extension, if present
    if github_url.endswith('.git'):
        github_url = github_url[:-4]

    repo_slug = parse_repo_slug_from_url(github_url)

    # Extract the metadata.yaml file
    metadata_yaml = await _download_metadata_yaml(session, github_url)
    metadata = yaml.safe_load(metadata_yaml)

    # Extract data from the GitHub API
    github_query = GitHubQuery.load('technote_repo')
    github_variables = {
        "orgName": repo_slug.owner,
        "repoName": repo_slug.repo
    }
    github_data = await github_request(session, github_api_token,
                                       query=github_query,
                                       variables=github_variables)

    try:
        jsonld = reduce_technote_metadata(
            github_url, metadata, github_data, ltd_product_data)
    except Exception as exception:
        message = "Issue building JSON-LD for technote {url}:\n\t{err}"
        print(message.format(url=github_url, err=exception))
        return

    if mongo_collection is not None:
        await _upload_to_mongodb(mongo_collection, jsonld)
    print(jsonld)

    print('finished {} | {}'.format(ltd_product_url, github_url))

    return jsonld


def reduce_technote_metadata(github_url, metadata, github_data,
                             ltd_product_data):
    """Reduce a technote project's metadata from multiple sources into a
    single JSON-LD resource.

    Parameters
    ----------
    github_url : `str`
        URL of the technote's GitHub repository.
    metadata : `dict`
        The parsed contents of ``metadata.yaml`` found in a technote's
        repository.
    github_data : `dict`
        The contents of the ``technote_repo`` GitHub GraphQL API query.
    ltd_product_data : `dict`
        JSON dataset for the technote corresponding to the
        ``/products/<product>`` of LTD Keeper.

    Returns
    -------
    metadata : `dict`
        JSON-LD-formatted dictionary.

    .. `GitHub personal access token guide`: https://ls.st/41d
    """
    repo_slug = parse_repo_slug_from_url(github_url)

    # Initialize a schema.org/Report and schema.org/SoftwareSourceCode
    # linked data resource
    jsonld = {
        '@context': [
            "https://raw.githubusercontent.com/codemeta/codemeta/2.0-rc/"
            "codemeta.jsonld",
            "http://schema.org"],
        '@type': ['Report', 'SoftwareSourceCode'],
        'codeRepository': github_url
    }

    if 'url' in metadata:
        url = metadata['url']
    elif 'published_url' in ltd_product_data:
        url = ltd_product_data['published_url']
    else:
        raise RuntimeError('No identifying url could be found: '
                           '{}'.format(github_url))
    jsonld['@id'] = url
    jsonld['url'] = url

    if 'series' in metadata and 'serial_number' in metadata:
        jsonld['reportNumber'] = '{series}-{serial_number}'.format(**metadata)
    else:
        raise RuntimeError('No reportNumber: {}'.format(github_url))

    if 'doc_title' in metadata:
        jsonld['name'] = metadata['doc_title']

    if 'description' in metadata:
        jsonld['description'] = metadata['description']

    if 'authors' in metadata:
        jsonld['author'] = [{'@type': 'Person', 'name': author_name}
                            for author_name in metadata['authors']]

    if 'last_revised' in metadata:
        # Prefer getting the 'last_revised' date from metadata.yaml
        # since it's considered an override.
        jsonld['dateModified'] = datetime.datetime.strptime(
            metadata['last_revised'],
            '%Y-%m-%d')
    else:
        # Fallback to parsing the date of the last commit to the
        # default branch on GitHub (usually `master`).
        try:
            _repo_data = github_data['data']['repository']
            _master_data = _repo_data['defaultBranchRef']
            jsonld['dateModified'] = datetime.datetime.strptime(
                _master_data['target']['committedDate'],
                '%Y-%m-%dT%H:%M:%SZ')
        except KeyError:
            pass

    try:
        _license_data = github_data['data']['repository']['licenseInfo']
        _spdxId = _license_data['spdxId']
        if _spdxId is not None:
            _spdx_url = 'https://spdx.org/licenses/{}.html'.format(_spdxId)
            jsonld['license'] = _spdx_url
    except KeyError:
        pass

    try:
        # Find the README(|.md|.rst|*) file in the repo root
        _master_data = github_data['data']['repository']['defaultBranchRef']
        _files = _master_data['target']['tree']['entries']
        for _node in _files:
            filename = _node['name']
            normalized_filename = filename.lower()
            if normalized_filename.startswith('readme'):
                readme_url = make_raw_content_url(repo_slug, 'master',
                                                  filename)
                jsonld['readme'] = readme_url
                break
    except KeyError:
        pass

    # Assume Travis is the CI service (always true at the moment)
    travis_url = 'https://travis-ci.org/{}'.format(repo_slug.full)
    jsonld['contIntegration'] = travis_url

    return jsonld


async def _download_metadata_yaml(session, github_url):
    """Download the metadata.yaml file from a technote's GitHub repository.
    """
    metadata_yaml_url = _build_metadata_yaml_url(github_url)
    async with session.get(metadata_yaml_url) as response:
        return await response.text()


def _build_metadata_yaml_url(github_url):
    """Compute the URL to the raw metadata.yaml resource given the technote's
    GitHub repository URL.

    Parameters
    ----------
    github_url : `str`
        URL of the technote's GitHub repository.

    Returns
    -------
    metadata_yaml_url : `str`
        metadata.yaml URL (using the ``raw.githubusercontent.com`` domain).
    """
    repo_slug = parse_repo_slug_from_url(github_url)
    return make_raw_content_url(repo_slug, 'master', 'metadata.yaml')


async def _upload_to_mongodb(collection, jsonld):
    """Upsert the technote resource into the projectmeta MongoDB collection.

    Parameters
    ----------
    collection : `motor.motor_asyncio.AsyncIOMotorCollection`
        The MongoDB collection.
    jsonld : `dict`
        The JSON-LD document that reprsents the technote resource.
    """
    document = {
        'data': jsonld
    }
    query = {
        'data.reportNumber': jsonld['reportNumber']
    }
    await collection.update(query, document, upsert=True, multi=False)
