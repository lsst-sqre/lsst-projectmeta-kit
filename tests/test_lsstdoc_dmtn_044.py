"""Test LsstDoc using sample data from DMTN-044.tex.
"""

import os
import pytest
from metasrc.tex.lsstdoc import LsstDoc

TITLE = "LSST DM Software Release Considerations"

SHORT_TITLE = "DM Software Releases"

HTML_TITLE = "LSST DM Software Release Considerations\n"

HTML_SHORT_TITLE = "DM Software Releases\n"

AUTHORS = ["John D. Swinbank"]

HTML_AUTHORS = ["John D. Swinbank\n"]

ABSTRACT = (
    "This attempts to summarise the debate around, and suggest a path "
    "forward, for\nLSST software releases. Although some recommendations "
    "are made, they are\nintended to serve as the basis of discussion, "
    "rather than as a complete\nsolution.\n\nThis material is based on "
    "discussions with several team members over a\nconsiderable period. "
    "Errors are to be expected; apologies are extended;\ncorrections are "
    "welcome."
)

HTML_ABSTRACT = (
    "<p>This attempts to summarise the debate around, and suggest a path "
    "forward, for LSST software releases. Although some recommendations are "
    "made, they are intended to serve as the basis of discussion, rather "
    "than as a complete solution.</p>\n"
    "<p>This material is based on discussions with several team members over "
    "a considerable period. Errors are to be expected; apologies are "
    "extended; corrections are welcome.</p>\n"
)

IS_DRAFT = False

HANDLE = 'DMTN-044'

SERIES = 'DMTN'

SERIAL = '044'

ATTRIBUTES = [
    ('title', TITLE),
    ('short_title', SHORT_TITLE),
    ('html_title', HTML_TITLE),
    ('html_short_title', HTML_SHORT_TITLE),
    ('authors', AUTHORS),
    ('html_authors', HTML_AUTHORS),
    ('abstract', ABSTRACT),
    ('html_abstract', HTML_ABSTRACT),
    ('is_draft', IS_DRAFT),
    ('handle', HANDLE),
    ('series', SERIES),
    ('serial', SERIAL),
]


@pytest.fixture
def lsstdoc():
    tex_path = os.path.join(os.path.dirname(__file__),
                            'data',
                            'DMTN-044',
                            'DMTN-044.tex')
    return LsstDoc.read(tex_path)


@pytest.mark.parametrize('attribute,expected', ATTRIBUTES)
def test_attribute(lsstdoc, attribute, expected):
    assert getattr(lsstdoc, attribute) == expected
