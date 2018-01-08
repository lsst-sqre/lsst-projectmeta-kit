"""Reduce technote projects into JSON-LD metadata.
"""

__all__ = ('reduce_technote',)

import re

import yaml


# Detects a GitHub repo slug from a GitHub URL
GITHUB_SLUG_PATTERN = re.compile(
    r"https://github.com"
    r"/(?P<org>[a-z0-9\-_~%!$&'()*+,;=:@]+)"
    r"/(?P<name>[a-z0-9\-_~%!$&'()*+,;=:@]+)")


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
    print(metadata)


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
    # Extract repo slug from the repo url
    match = GITHUB_SLUG_PATTERN.match(github_url)
    if match:
        repo_slug = '/'.join((match.group('org'),
                              match.group('name')))
    else:
        message = 'Could not parse GitHub slug from {}'.format(github_url)
        raise RuntimeError(message)

    template = 'https://raw.githubusercontent.com/{slug}/master/metadata.yaml'
    return template.format(slug=repo_slug)
