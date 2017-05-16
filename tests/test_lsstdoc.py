import os

import pytest

from metaget.tex.lsstdoc import LsstDoc, TITLE_PATTERN


@pytest.fixture
def ldm_nnn_data():
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'LDM-nnn.tex')
    with open(data_path) as f:
        source = f.read()
    return source


def test_sample_title(ldm_nnn_data):
    lsstdoc = LsstDoc(ldm_nnn_data)
    assert lsstdoc.title == "Title of document"
    assert lsstdoc.short_title == "Short title"


def test_no_short_title():
    """title without a short title."""
    sample = r"\title{Title}"
    match = TITLE_PATTERN.search(sample)
    assert match.group('title') == 'Title'
    assert match.group('short_title') is None


def test_authors(ldm_nnn_data):
    expected = ['A. Author', 'B. Author', 'C. Author']
    lsstdoc = LsstDoc(ldm_nnn_data)
    assert lsstdoc.authors == expected


def test_sample_abstract(ldm_nnn_data):
    expected = ("%\nThis document demonstrates how to use the LSST \\LaTeX\\ "
                "class files to make Data Management\ndocuments. Build this "
                "document in the normal way, making sure that the class "
                "file is\navailable in the \\LaTeX\\ load path.")
    lsstdoc = LsstDoc(ldm_nnn_data)
    assert lsstdoc.abstract == expected
