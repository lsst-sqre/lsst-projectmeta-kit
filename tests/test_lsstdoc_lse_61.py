"""Test LsstLatexDoc using sample data from LSE-61.tex.
"""

import datetime
import os
import pytest
import pytz
from lsstprojectmeta.tex.lsstdoc import LsstLatexDoc

TITLE = "Data Management System (DMS) Requirements"

SHORT_TITLE = None

HTML_TITLE = "Data Management System (DMS) Requirements\n"

HTML_SHORT_TITLE = None

PLAIN_TITLE = "Data Management System (DMS) Requirements\n"

PLAIN_SHORT_TITLE = None

AUTHORS = [
    "Gregory Dubois-Felsmann", "Tim Jenness"
]

HTML_AUTHORS = [
    "Gregory Dubois-Felsmann", "Tim Jenness"
]

PLAIN_AUTHORS = [
    "Gregory Dubois-Felsmann", "Tim Jenness"
]

ABSTRACT = None

HTML_ABSTRACT = None

PLAIN_ABSTRACT = None

IS_DRAFT = False

HANDLE = 'LSE-61'

SERIES = 'LSE'

SERIAL = '61'

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
    tex_path = os.path.join(os.path.dirname(__file__),
                            'data',
                            'LSE-61',
                            'LSE-61.tex')
    return LsstLatexDoc.read(tex_path)


@pytest.mark.parametrize('attribute,expected', ATTRIBUTES)
def test_attribute(lsstdoc, attribute, expected):
    assert getattr(lsstdoc, attribute) == expected


def test_revision_date(lsstdoc):
    r"""LSE-61 uses a set value for \date."""
    expected_datetime = datetime.datetime(2017, 9, 12, 7, 0, tzinfo=pytz.utc)
    assert lsstdoc.revision_datetime == expected_datetime
    assert lsstdoc.revision_datetime_source == 'tex'


def test_jsonld(lsstdoc):
    jsonld = lsstdoc.build_jsonld()
    for key, value in JSONLD.items():
        assert jsonld[key] == value
    assert jsonld['dateModified'] == lsstdoc.revision_datetime
