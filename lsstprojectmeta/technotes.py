"""Reduce technote projects into JSON-LD metadata.
"""

__all__ = ('reduce_technote',)

import yaml
import datetime

from .github.urls import parse_repo_slug_from_url, make_raw_content_url
from .github.graphql import github_request, GitHubQuery


async def reduce_technote(github_url, session, github_api_token,
                          mongo_collection=None):
    """Reduce a technote project's metadata into JSON-LD.

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

    Returns
    -------
    metadata : `dict`
        JSON-LD-formatted dictionary.

    .. `GitHub personal access token guide`: https://ls.st/41d
    """
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
        jsonld['@id'] = metadata['url']
        jsonld['url'] = metadata['url']

    if 'series' in metadata and 'serial_number' in metadata:
        jsonld['reportNumber'] = '{series}-{serial_number}'.format(**metadata)

    if 'doc_title' in metadata:
        jsonld['name'] = metadata['doc_title']

    if 'description' in metadata:
        jsonld['description'] = metadata['description']

    if 'authors' in metadata:
        jsonld['author'] = [{'@type': 'Person', 'name': author_name}
                            for author_name in metadata['authors']]

    try:
        _master_data = github_data['data']['repository']['defaultBranchRef']
        _modified_datetime = datetime.datetime.strptime(
            _master_data['target']['committedDate'],
            '%Y-%m-%dT%H:%M:%SZ')
        jsonld['dateModified'] = _modified_datetime
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

    if mongo_collection is not None:
        await _upload_to_mongodb(mongo_collection, jsonld)

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
