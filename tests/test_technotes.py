"""Tests for lsstprojectmeta.technotes.
"""

import asyncio

import aiohttp
import pytest
import yaml

from lsstprojectmeta.technotes import (
    _build_metadata_yaml_url,
    _download_metadata_yaml)


@pytest.mark.parametrize(
    'repo_url,expected',
    [('https://github.com/lsst-sqre/sqr-020',
      'https://raw.githubusercontent.com/lsst-sqre/sqr-020/'
      'master/metadata.yaml')])
def test_build_metadata_yaml_url(repo_url, expected):
    assert _build_metadata_yaml_url(repo_url) == expected


def test_download_metadata_yaml():
    github_url = 'https://github.com/lsst-sqre/sqr-020'

    async def _test():
        async with aiohttp.ClientSession() as session:
            text_data = await _download_metadata_yaml(session, github_url)
        assert isinstance(text_data, str)
        metadata = yaml.safe_load(text_data)
        assert isinstance(metadata, dict)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(_test())


@pytest.mark.skip(reason="Needs to be refactored to eliminate network "
                         "requests")
def test_sqr_020():
    github_url = 'https://github.com/lsst-sqre/sqr-020'

    # TODO make mock metadata.yaml and GitHub query datasources and test the
    # reduce_technote_metadata function.
    jsonld = {}

    # Cursory content tests (not thorough). This testing strategy
    # will need to change because the document itself will change.
    assert jsonld['@id'] == 'https://sqr-020.lsst.io'
    assert jsonld['url'] == 'https://sqr-020.lsst.io'
    assert jsonld['name'] == ('Expressing LSST Project Metadata with '
                              'JSON-LD')
    assert jsonld['reportNumber'] == 'SQR-020'
    assert jsonld['author'][0]['name'] == 'Jonathan Sick'
    assert jsonld['codeRepository'] == github_url
    assert jsonld['contIntegration'] == ('https://travis-ci.org/'
                                         'lsst-sqre/sqr-020')
    assert 'dateModified' not in jsonld  # but will come from GitHub.
