"""Tests for the lsstprojectmeta.github.graphql module.
"""

from lsstprojectmeta.github.graphql import GitHubQuery


def test_github_query():
    query = GitHubQuery.load('technote_repo')
    assert str(query) == query.query
    assert query.name == 'technote_repo'
    assert query.query.startswith('query ')
