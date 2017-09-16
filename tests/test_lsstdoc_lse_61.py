"""Test LsstDoc using sample data from LSE-61.tex.
"""

import os
import pytest
from metasrc.tex.lsstdoc import LsstDoc

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


@pytest.fixture
def lsstdoc():
    tex_path = os.path.join(os.path.dirname(__file__),
                            'data',
                            'LSE-61',
                            'LSE-61.tex')
    return LsstDoc.read(tex_path)


@pytest.mark.parametrize('attribute,expected', ATTRIBUTES)
def test_attribute(lsstdoc, attribute, expected):
    assert getattr(lsstdoc, attribute) == expected
