"""Build and parse standard GitHub URLs.
"""

__all__ = ('parse_repo_slug_from_url',)

import collections
import re


RepoSlug = collections.namedtuple('RepoSlug', 'full owner repo')
"""GitHub repository slug (`collections.namedtuple`).

Attributes
----------
full : `str`
    Full repository slug. Example: ``'lsst-sqre/lsst-projectmeta-kit'``.
owner : `str`
    Repository owner component. Example: ``'lsst-sqre'``.
repo : `str`
    Repository name component. Example: ``'lsst-projectmeta-kit'``.
"""

# Detects a GitHub repo slug from a GitHub URL
GITHUB_SLUG_PATTERN = re.compile(
    r"https://github.com"
    r"/(?P<org>[a-z0-9\-_~%!$&'()*+,;=:@]+)"
    r"/(?P<name>[a-z0-9\-_~%!$&'()*+,;=:@]+)")


def parse_repo_slug_from_url(github_url):
    """Get the slug, <owner>/<repo_name>, for a GitHub repository from
    its URL.

    Parameters
    ----------
    github_url : `str`
        URL of a GitHub repository.

    Returns
    -------
    repo_slug : `RepoSlug`
        Repository slug with fields ``full``, ``owner``, and ``repo``.
        See `RepoSlug` for details.

    Raises
    ------
    RuntimeError
        Raised if the URL cannot be parsed.
    """
    match = GITHUB_SLUG_PATTERN.match(github_url)
    if not match:
        message = 'Could not parse GitHub slug from {}'.format(github_url)
        raise RuntimeError(message)

    _full = '/'.join((match.group('org'),
                      match.group('name')))
    return RepoSlug(_full, match.group('org'), match.group('name'))
