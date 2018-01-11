"""Reduce technote projects into JSON-LD metadata.
"""

__all__ = ('reduce_technote',)

import yaml

from .github.urls import parse_repo_slug_from_url, make_raw_content_url


async def reduce_technote(github_url, session):
    """Reduce a technote project's metadata into JSON-LD.

    Parameters
    ----------
    github_url : `str`
        URL of the technote's GitHub repository.
    session : `aiohttp.ClientSession`
        Your application's aiohttp client session.
        See http://aiohttp.readthedocs.io/en/stable/client.html.

    Returns
    -------
    metadata : `dict`
        JSON-LD-formatted dictionary.
    """
    metadata_yaml = await _download_metadata_yaml(session, github_url)
    metadata = yaml.safe_load(metadata_yaml)

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

    # Assume Travis is the CI service (always true at the moment)
    repo_slug = parse_repo_slug_from_url(github_url)
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
