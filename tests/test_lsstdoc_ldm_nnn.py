"""Test LsstLatexDoc using sample data from LDM-nnn.tex.
"""

import datetime
import os
import pytest
from lsstprojectmeta.tex.lsstdoc import LsstLatexDoc

TITLE = "Title of document"

SHORT_TITLE = "Short title"

HTML_TITLE = "Title of document\n"

HTML_SHORT_TITLE = "Short title\n"

PLAIN_TITLE = "Title of document\n"

PLAIN_SHORT_TITLE = "Short title\n"

AUTHORS = ['A. Author', 'B. Author', 'C. Author']

HTML_AUTHORS = ['A. Author', 'B. Author', 'C. Author']

PLAIN_AUTHORS = ['A. Author', 'B. Author', 'C. Author']

ABSTRACT = (
    "This document demonstrates how to use the LSST \\LaTeX\\ "
    "class files to make Data Management\ndocuments. Build this "
    "document in the normal way, making sure that the class "
    "file is\navailable in the \\LaTeX\\ load path."
)

HTML_ABSTRACT = (
    '<p>This document demonstrates how to use the LSST LaTeX\xa0class files '
    'to make Data Management documents. Build this document in the normal '
    'way, making sure that the class file is available in the LaTeX\xa0load '
    'path.</p>\n'
)

PLAIN_ABSTRACT = (
    'This document demonstrates how to use the LSST LaTeX\xa0class files '
    'to make Data Management documents. Build this document in the normal '
    'way, making sure that the class file is available in the LaTeX\xa0load '
    'path.\n'
)

IS_DRAFT = True

HANDLE = 'LDM-nnn'

SERIES = 'LDM'

SERIAL = 'nnn'

ATTRIBUTES = [
    ('title', TITLE),
    ('short_title', SHORT_TITLE),
    ('html_title', HTML_TITLE),
    ('html_short_title', HTML_SHORT_TITLE),
    ('plain_title', PLAIN_TITLE),
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
    tex_path = os.path.join(os.path.dirname(__file__), 'data', 'LDM-nnn.tex')
    return LsstLatexDoc.read(tex_path)


@pytest.mark.parametrize('attribute,expected', ATTRIBUTES)
def test_attribute(lsstdoc, attribute, expected):
    assert getattr(lsstdoc, attribute) == expected


def test_revision_date(lsstdoc):
    r"""LDM-nnn is a draft so it falls back to git (would anyway since
    ``\date`` is ``\today``).
    """
    assert isinstance(lsstdoc.revision_datetime, datetime.datetime)
    assert lsstdoc.revision_datetime_source == 'git'


def test_jsonld(lsstdoc):
    jsonld = lsstdoc.build_jsonld()
    for key, value in JSONLD.items():
        assert jsonld[key] == value
    assert jsonld['dateModified'] == lsstdoc.revision_datetime
