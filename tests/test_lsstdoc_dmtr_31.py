"""Test LsstLatexDoc using sample data from DMTR-31.tex.
"""

import datetime
import os
import pytest
import pytz
from lsstprojectmeta.tex.lsstdoc import LsstLatexDoc

TITLE = "S17B HSC PDR1 Reprocessing Report"

SHORT_TITLE = None

HTML_TITLE = "S17B HSC PDR1 Reprocessing Report\n"

HTML_SHORT_TITLE = None

PLAIN_TITLE = "S17B HSC PDR1 Reprocessing Report\n"

PLAIN_SHORT_TITLE = None

AUTHORS = [
    "Hsin-Fang Chiang", "Greg Daues", "Samantha Thrush", "the NCSA team"
]

HTML_AUTHORS = [
    "Hsin-Fang Chiang", "Greg Daues", "Samantha Thrush",
    "the NCSA team"
]

PLAIN_AUTHORS = [
    "Hsin-Fang Chiang", "Greg Daues", "Samantha Thrush",
    "the NCSA team"
]

ABSTRACT = (
    "This document captures information about the large scale HSC "
    "reprocessing we performed in Cycle S17B."
)

HTML_ABSTRACT = (
    "<p>This document captures information about the large scale HSC "
    "reprocessing we performed in Cycle S17B.</p>\n"
)

PLAIN_ABSTRACT = (
    "This document captures information about the large scale HSC "
    "reprocessing we performed in Cycle S17B.\n"
)

IS_DRAFT = False

HANDLE = 'DMTR-31'

SERIES = 'DMTR'

SERIAL = '31'

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
                            'DMTR-31',
                            'DMTR-31.tex')
    return LsstLatexDoc.read(tex_path)


@pytest.mark.parametrize('attribute,expected', ATTRIBUTES)
def test_attribute(lsstdoc, attribute, expected):
    assert getattr(lsstdoc, attribute) == expected


def test_revision_date(lsstdoc):
    r"""DMTR-31 uses a set value for \date."""
    expected_datetime = datetime.datetime(2017, 8, 28, 7, 0, tzinfo=pytz.utc)
    assert lsstdoc.revision_datetime == expected_datetime
    assert lsstdoc.revision_datetime_source == 'tex'


def test_jsonld(lsstdoc):
    jsonld = lsstdoc.build_jsonld()
    for key, value in JSONLD.items():
        assert jsonld[key] == value
    assert jsonld['dateModified'] == lsstdoc.revision_datetime
