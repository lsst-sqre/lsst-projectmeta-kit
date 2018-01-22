"""Test LsstLatexDoc using sample data from DMTN-044.tex.
"""

import os
import pytest
from lsstprojectmeta.tex.lsstdoc import LsstLatexDoc

TITLE = "LSST DM Software Release Considerations"

SHORT_TITLE = "DM Software Releases"

HTML_TITLE = "LSST DM Software Release Considerations\n"

HTML_SHORT_TITLE = "DM Software Releases\n"

PLAIN_TITLE = "LSST DM Software Release Considerations\n"

PLAIN_SHORT_TITLE = "DM Software Releases\n"

AUTHORS = ["John D. Swinbank"]

HTML_AUTHORS = ["John D. Swinbank"]

PLAIN_AUTHORS = ["John D. Swinbank"]

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
    "than as a complete solution.</p>"
    "<p>This material is based on discussions with several team members over "
    "a considerable period. Errors are to be expected; apologies are "
    "extended; corrections are welcome.</p>\n"
)

PLAIN_ABSTRACT = (
    "This attempts to summarise the debate around, and suggest a path "
    "forward, for LSST software releases. Although some recommendations are "
    "made, they are intended to serve as the basis of discussion, rather "
    "than as a complete solution.\n\n"
    "This material is based on discussions with several team members over "
    "a considerable period. Errors are to be expected; apologies are "
    "extended; corrections are welcome.\n"
)

IS_DRAFT = False

HANDLE = 'DMTN-044'

SERIES = 'DMTN'

SERIAL = '044'

ATTRIBUTES = [
    ('title', TITLE),
    ('short_title', SHORT_TITLE),
    ('html_title', HTML_TITLE),
    ('plain_title', PLAIN_TITLE),
    ('html_short_title', HTML_SHORT_TITLE),
    ('plain_short_title', PLAIN_SHORT_TITLE),
    ('authors', AUTHORS),
    ('html_authors', HTML_AUTHORS),
    ('plain_authors', PLAIN_AUTHORS),
    ('abstract', ABSTRACT),
    ('html_abstract', HTML_ABSTRACT),
    ('plain_abstract', PLAIN_ABSTRACT),
    ('is_draft', IS_DRAFT),
    ('handle', HANDLE),
    ('series', SERIES),
    ('serial', SERIAL),
]

JSONLD = {
    '@context': [
        "https://raw.githubusercontent.com/codemeta/codemeta/2.0-rc/"
        "codemeta.jsonld",
        "http://schema.org"],
    '@type': ['Report', 'SoftwareSourceCode'],
    'language': 'TeX',
    'reportNumber': HANDLE,
    'name': PLAIN_TITLE,
    'description': PLAIN_ABSTRACT,
    'author': [{'@type': 'Person', 'name': author_name}
               for author_name in PLAIN_AUTHORS],
}


@pytest.fixture
def lsstdoc():
    tex_path = os.path.join(os.path.dirname(__file__),
                            'data',
                            'DMTN-044',
                            'DMTN-044.tex')
    return LsstLatexDoc.read(tex_path)


@pytest.mark.parametrize('attribute,expected', ATTRIBUTES)
def test_attribute(lsstdoc, attribute, expected):
    assert getattr(lsstdoc, attribute) == expected


def test_revision_date(lsstdoc):
    r"""DMTN-044 sets a 2017-06-26 value for \setDocDate, which is deprecated
    and ignored (so it falls back to Git).
    """
    assert lsstdoc.revision_datetime_source == 'git'


def test_jsonld(lsstdoc):
    jsonld = lsstdoc.build_jsonld()
    for key, value in JSONLD.items():
        assert jsonld[key] == value
    assert jsonld['dateModified'] == lsstdoc.revision_datetime
