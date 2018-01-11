"""Tests for lsstprojectmeta.github.urls.
"""

import pytest
from lsstprojectmeta.github.urls import parse_repo_slug_from_url


@pytest.mark.parametrize(
    'url,expected',
    [('https://github.com/lsst-sqre/lsst-projectmeta-kit',
     ('lsst-sqre/lsst-projectmeta-kit', 'lsst-sqre', 'lsst-projectmeta-kit'))])
def test_parse_repo_slug_from_url(url, expected):
    repo_slug = parse_repo_slug_from_url(url)
    assert repo_slug.full == expected[0]
    assert repo_slug.owner == expected[1]
    assert repo_slug.repo == expected[2]
