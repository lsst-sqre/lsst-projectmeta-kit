"""Test LsstLatexDoc using sample data from LDM-151.tex.
"""

import datetime
import os
import pytest
import pytz
from lsstprojectmeta.tex.lsstdoc import LsstLatexDoc

TITLE = "Data Management Science Pipelines Design"

SHORT_TITLE = None

HTML_TITLE = "Data Management Science Pipelines Design\n"

HTML_SHORT_TITLE = None

PLAIN_TITLE = "Data Management Science Pipelines Design\n"

PLAIN_SHORT_TITLE = None

AUTHORS = [
    "J.D. Swinbank",
    "T. Axelrod", "A.C. Becker", "J. Becla", "E. Bellm",
    "J.F. Bosch", "H. Chiang", "D.R. Ciardi", "A.J. Connolly",
    "G.P. Dubois-Felsmann", "F. Economou", "M. Fisher-Levine", "M. Graham",
    r"\v{Z}. Ivezi\'c", r"M. Juri\'c",
    "T. Jenness", "R.L. Jones", "J. Kantor", "S. Krughoff", "K-T. Lim",
    "R.H. Lupton", "F. Mueller", "D. Petravick", "P.A. Price",
    "D.J. Reiss", "D. Shaw", "C. Slater", "M. Wood-Vasey", "X. Wu",
    "P. Yoachim", r"\emph{for the LSST Data Management}"
]

HTML_AUTHORS = [
    "J.D. Swinbank",
    "T. Axelrod", "A.C. Becker", "J. Becla", "E. Bellm",
    "J.F. Bosch", "H. Chiang", "D.R. Ciardi", "A.J. Connolly",
    "G.P. Dubois-Felsmann", "F. Economou", "M. Fisher-Levine",
    "M. Graham", "Ž. Ivezić", "M. Jurić",
    "T. Jenness", "R.L. Jones", "J. Kantor", "S. Krughoff",
    "K-T. Lim", "R.H. Lupton", "F. Mueller", "D. Petravick",
    "P.A. Price", "D.J. Reiss", "D. Shaw", "C. Slater",
    "M. Wood-Vasey", "X. Wu", "P. Yoachim",
    "<em>for the LSST Data Management</em>"
]

PLAIN_AUTHORS = [
    "J.D. Swinbank",
    "T. Axelrod", "A.C. Becker", "J. Becla", "E. Bellm",
    "J.F. Bosch", "H. Chiang", "D.R. Ciardi", "A.J. Connolly",
    "G.P. Dubois-Felsmann", "F. Economou", "M. Fisher-Levine",
    "M. Graham", "Ž. Ivezić", "M. Jurić",
    "T. Jenness", "R.L. Jones", "J. Kantor", "S. Krughoff",
    "K-T. Lim", "R.H. Lupton", "F. Mueller", "D. Petravick",
    "P.A. Price", "D.J. Reiss", "D. Shaw", "C. Slater",
    "M. Wood-Vasey", "X. Wu", "P. Yoachim",
    "_for the LSST Data Management_"
]

ABSTRACT = (
    r"The LSST Science Requirements Document (the LSST \SRD) specifies a set "
    r"of data product guidelines, designed to support science goals "
    r"envisioned to be enabled by the LSST observing program." + "\n"
    r"Following these guidlines, the details of these data products have "
    r"been described in the LSST Data Products Definition Document (\DPDD), "
    r"and captured in a formal flow-down from the \SRD via the LSST System "
    r"Requirements (\LSR), Observatory System Specifications (\OSS), to the "
    r"Data Management System Requirements (\DMSR)." + "\n"
    r"The LSST Data Management subsystem's responsibilities include the "
    r"design, implementation, deployment and execution of software pipelines "
    r"necessary to generate these data products. This document describes the "
    r"design of the scientific aspects of those pipelines."
)

HTML_ABSTRACT = (
    '<p>The LSST Science Requirements Document (the LSST '
    '<span><a href="https://docushare.lsst.org/docushare/dsweb/Get/LPM-17">'
    'SRD</a></span>) specifies a set of data product guidelines, designed to '
    'support science goals envisioned to be enabled by the LSST observing '
    'program. Following these guidlines, the details of these data products '
    'have been described in the LSST Data Products Definition Document '
    '(<span><a href="https://docushare.lsst.org/docushare/dsweb/Get/'
    'LSE-163">DPDD</a></span>), and captured in a formal flow-down from '
    'the <span><a href="https://docushare.lsst.org/docushare/dsweb/Get/'
    'LPM-17">SRD</a></span>via the LSST System Requirements (<span>'
    '<a href="https://docushare.lsst.org/docushare/dsweb/Get/LSE-29">'
    'LSR</a></span>), Observatory System Specifications (<span>'
    '<a href="https://docushare.lsst.org/docushare/dsweb/Get/LSE-30">'
    'OSS</a></span>), to the Data Management System Requirements '
    '(<span><a href="https://docushare.lsst.org/docushare/dsweb/Get/'
    'LSE-61">DMSR</a></span>). The LSST Data Management subsystem’s '
    'responsibilities include the design, implementation, deployment and '
    'execution of software pipelines necessary to generate these data '
    'products. This document describes the design of the scientific aspects '
    'of those pipelines.</p>\n'
)

# NOTE there's an issue with getting spaces to appear after commands.
# xspace doesn't work for us.
PLAIN_ABSTRACT = (
    "The LSST Science Requirements Document (the LSST SRD) specifies a set "
    "of data product guidelines, designed to support science goals "
    "envisioned to be enabled by the LSST observing program. "
    "Following these guidlines, the details of these data products have "
    "been described in the LSST Data Products Definition Document (DPDD), "
    "and captured in a formal flow-down from the SRDvia the LSST System "
    "Requirements (LSR), Observatory System Specifications (OSS), to the "
    "Data Management System Requirements (DMSR). "
    "The LSST Data Management subsystem’s responsibilities include the "
    "design, implementation, deployment and execution of software pipelines "
    "necessary to generate these data products. This document describes the "
    "design of the scientific aspects of those pipelines.\n"
)

IS_DRAFT = False

HANDLE = 'LDM-151'

SERIES = 'LDM'

SERIAL = '151'

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
                            'LDM-151',
                            'LDM-151.tex')
    return LsstLatexDoc.read(tex_path)


@pytest.mark.parametrize('attribute,expected', ATTRIBUTES)
def test_attribute(lsstdoc, attribute, expected):
    assert getattr(lsstdoc, attribute) == expected


def test_revision_date(lsstdoc):
    r"""LDM-151 uses a set value for \date."""
    expected_datetime = datetime.datetime(2017, 7, 19, 7, 0, tzinfo=pytz.utc)
    assert lsstdoc.revision_datetime == expected_datetime
    assert lsstdoc.revision_datetime_source == 'tex'


def test_jsonld(lsstdoc):
    jsonld = lsstdoc.build_jsonld()
    for key, value in JSONLD.items():
        assert jsonld[key] == value
    assert jsonld['dateModified'] == lsstdoc.revision_datetime
