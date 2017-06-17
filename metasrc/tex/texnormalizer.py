"""Functions for normalizing TeX source.
"""

import re


def remove_comments(tex_source):
    """Delete latex comments from TeX source.

    Parameters
    ----------
    tex_source : str
        TeX source content.

    Returns
    -------
    tex_source : str
        TeX source without comments.
    """
    # Expression via http://stackoverflow.com/a/13365453
    return re.sub(r'(?<!\\)%.*$', r'', tex_source, flags=re.M)


def remove_trailing_whitespace(tex_source):
    """Delete trailing whitespace from TeX source.

    Parameters
    ----------
    tex_source : str
        TeX source content.

    Returns
    -------
    tex_source : str
        TeX source without trailing whitespace.
    """
    # Expression via https://stackoverflow.com/a/17350806
    return re.sub(r'\s+$', '', tex_source, flags=re.M)
