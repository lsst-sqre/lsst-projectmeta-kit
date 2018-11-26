"""Test LsstLatexDoc using sample data from LSE-63.tex.
"""

import datetime
import os
import pytest
import pytz
from lsstprojectmeta.tex.lsstdoc import LsstLatexDoc

TITLE = "LSST Data Quality Assurance Plan"

SHORT_TITLE = None

HTML_TITLE = "LSST Data Quality Assurance Plan\n"

HTML_SHORT_TITLE = None

PLAIN_TITLE = "LSST Data Quality Assurance Plan\n"

PLAIN_SHORT_TITLE = None

AUTHORS = [
    "Tony Tyson", "DQA Team", "Science Collaboration"
]

HTML_AUTHORS = [
    "Tony Tyson", "DQA Team", "Science Collaboration"
]

PLAIN_AUTHORS = [
    "Tony Tyson", "DQA Team", "Science Collaboration"
]

ABSTRACT = (
    r"LSST must supply trusted petascale data products. The mechanisms by "
    r"which the LSST project achieve this unprecedented level of data "
    r"quality will have spinoff to data-enabled science generally. This "
    r"document specifies high-level requirements for a LSST Data Quality "
    r"Assessment" + "\n"
    r"Framework, and defines the four levels of quality "
    r"assessment (QA) tools. Because this process involves system-wide "
    r"hardware and software, data QA must be defined at the System level. The "
    r"scope of this document is limited to the description of the overall "
    r"framework and the general requirements. It derives from the LSST "
    r"Science Requirements Document \citedsp{LPM-17}. A flow-down document "
    r"will describe detailed implementation of the QA, including the "
    r"algorithms.  In most cases the monitoring strategy, the development "
    r"path for these tools or the algorithms are known. Related documents "
    r"are: LSST System Requirements \citedsp{LSE-29}, Optimal Deployment "
    r"Parameters \citeds{Document-11624}, Observatory System Specifications "
    r"\citedsp{LSE-30}, Configuration Management Plan \citedsp{LPM-19}, "
    r"Project Quality Assurance Plan \citedsp{LPM-55}, Software Development "
    r"Plan \citedsp{LSE-16}, Camera Quality implementation Plan "
    r"\citedsp{LCA-227}, System Engineering Management Plan \citedsp{LSE-17}, "
    r"and the Operations Plan \citedsp{LPM-73}."
)

HTML_ABSTRACT = (
    "<p>LSST must supply trusted petascale data products. The mechanisms by "
    "which the LSST project achieve this unprecedented level of data "
    "quality will have spinoff to data-enabled science generally. This "
    "document specifies high-level requirements for a LSST Data Quality "
    "Assessment Framework, and defines the four levels of quality "
    "assessment (QA) tools. Because this process involves system-wide "
    "hardware and software, data QA must be defined at the System level. The "
    "scope of this document is limited to the description of the overall "
    "framework and the general requirements. It derives from the LSST "
    "Science Requirements Document [<a href=\"https://ls.st/LPM-17\">"
    "LPM-17</a>]. A flow-down document will describe detailed implementation "
    "of the QA, including the algorithms. In most cases the monitoring "
    "strategy, the development path for these tools or the algorithms are "
    "known. Related documents are: LSST System Requirements "
    "[<a href=\"https://ls.st/LSE-29\">LSE-29</a>], Optimal Deployment "
    "Parameters <a href=\"https://ls.st/Document-11624\">Document-11624</a>, "
    "Observatory System Specifications "
    "[<a href=\"https://ls.st/LSE-30\">LSE-30</a>], Configuration Management "
    "Plan [<a href=\"https://ls.st/LPM-19\">LPM-19</a>], "
    "Project Quality Assurance Plan "
    "[<a href=\"https://ls.st/LPM-55\">LPM-55</a>], "
    "Software Development Plan [<a href=\"https://ls.st/LSE-16\">LSE-16</a>], "
    "Camera Quality implementation Plan "
    "[<a href=\"https://ls.st/LCA-227\">LCA-227</a>], "
    "System Engineering Management Plan "
    "[<a href=\"https://ls.st/LSE-17\">LSE-17</a>], "
    "and the Operations Plan "
    "[<a href=\"https://ls.st/LPM-73\">LPM-73</a>].</p>\n"
)

PLAIN_ABSTRACT = (
    "LSST must supply trusted petascale data products. The mechanisms by "
    "which the LSST project achieve this unprecedented level of data "
    "quality will have spinoff to data-enabled science generally. This "
    "document specifies high-level requirements for a LSST Data Quality "
    "Assessment Framework, and defines the four levels of quality "
    "assessment (QA) tools. Because this process involves system-wide "
    "hardware and software, data QA must be defined at the System level. The "
    "scope of this document is limited to the description of the overall "
    "framework and the general requirements. It derives from the LSST "
    "Science Requirements Document [LPM-17]. A flow-down document will "
    "describe detailed implementation of the QA, including the algorithms. "
    "In most cases the monitoring strategy, the development path for these "
    "tools or the algorithms are known. Related documents are: "
    "LSST System Requirements [LSE-29], "
    "Optimal Deployment Parameters Document-11624, "
    "Observatory System Specifications [LSE-30], "
    "Configuration Management Plan [LPM-19], "
    "Project Quality Assurance Plan [LPM-55], "
    "Software Development Plan [LSE-16], "
    "Camera Quality implementation Plan [LCA-227], "
    "System Engineering Management Plan [LSE-17], "
    "and the Operations Plan [LPM-73].\n"
)

IS_DRAFT = False

HANDLE = 'LSE-63'

SERIES = 'LSE'

SERIAL = '63'

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
                            'LSE-63.tex')
    return LsstLatexDoc.read(tex_path)


@pytest.mark.parametrize('attribute,expected', ATTRIBUTES)
def test_attribute(lsstdoc, attribute, expected):
    assert getattr(lsstdoc, attribute) == expected


def test_revision_date(lsstdoc):
    r"""LSE-63 uses a set value for \date."""
    expected_datetime = datetime.datetime(2017, 5, 17, 7, 0, tzinfo=pytz.utc)
    assert lsstdoc.revision_datetime == expected_datetime
    assert lsstdoc.revision_datetime_source == 'tex'


def test_jsonld(lsstdoc):
    jsonld = lsstdoc.build_jsonld()
    for key, value in JSONLD.items():
        assert jsonld[key] == value
    assert jsonld['dateModified'] == lsstdoc.revision_datetime
