"""Tests for lsstprojectmeta.github.urls.
"""

import pytest
from lsstprojectmeta.github.urls import (
    parse_repo_slug_from_url, RepoSlug, make_raw_content_url,
    normalize_repo_root_url)


@pytest.mark.parametrize(
    'url,expected',
    [('https://github.com/lsst-sqre/lsst-projectmeta-kit',
     ('lsst-sqre/lsst-projectmeta-kit', 'lsst-sqre', 'lsst-projectmeta-kit')),
     ('https://github.com/lsst/LDM-151',
     ('lsst/LDM-151', 'lsst', 'LDM-151')),
     ('https://github.com/lsst-dm/dmtn-030',
     ('lsst-dm/dmtn-030', 'lsst-dm', 'dmtn-030')),
     ])
def test_parse_repo_slug_from_url(url, expected):
    repo_slug = parse_repo_slug_from_url(url)
    assert repo_slug.full == expected[0]
    assert repo_slug.owner == expected[1]
    assert repo_slug.repo == expected[2]


@pytest.mark.parametrize(
    'inputs,expected',
    [(('lsst-sqre/sqr-020', 'master', 'metadata.yaml'),
      'https://raw.githubusercontent.com/lsst-sqre/sqr-020/'
      'master/metadata.yaml'),
     ((RepoSlug('lsst-sqre/sqr-020', 'lsst-sqre', 'sqr-020'),
       'master', 'metadata.yaml'),
      'https://raw.githubusercontent.com/lsst-sqre/sqr-020/'
      'master/metadata.yaml')]
    )
def test_make_raw_content_url(inputs, expected):
    assert make_raw_content_url(*inputs) == expected


@pytest.mark.parametrize(
    'url,expected', [
        ('https://github.com/lsst/LDM-151.git',
         'https://github.com/lsst/LDM-151')
    ])
def test_normalize_repo_root_url(url, expected):
    assert normalize_repo_root_url(url) == expected
