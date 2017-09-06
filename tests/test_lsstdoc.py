import os

import pytest

from metasrc.tex.lsstdoc import LsstDoc


@pytest.fixture
def ldm_nnn_data():
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'LDM-nnn.tex')
    with open(data_path) as f:
        source = f.read()
    return source


@pytest.fixture
def dmtn_036_data():
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'DMTN-036.tex')
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
    lsstdoc = LsstDoc(sample)
    assert lsstdoc.title == "Title"


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


def test_sample_handle(ldm_nnn_data):
    lsstdoc = LsstDoc(ldm_nnn_data)
    assert lsstdoc.handle == 'LDM-nnn'
    assert lsstdoc.series == 'LDM'
    assert lsstdoc.serial == 'nnn'


def test_title_variations():
    """Test variations on the title command's formatting."""
    # Test with whitespace in title command
    input_txt = "\\title    [Test Plan]  { \product ~Test Plan}"
    lsstdoc = LsstDoc(input_txt)
    assert lsstdoc.title == "\product ~Test Plan"
    assert lsstdoc.short_title == "Test Plan"


def test_author_variations():
    """Test variations on the author command's formatting."""
    input_txt = ("\\author   {William O'Mullane, Mario Juric, "
                 "Frossie Economou}"
                 "                  % the author(s)")
    lsstdoc = LsstDoc(input_txt)
    assert lsstdoc.authors == ["William O'Mullane",
                               "Mario Juric",
                               "Frossie Economou"]


def test_handle_variations():
    """Test variations on the handle command's formatting."""
    input_txt = "\setDocRef      {LDM-503} % the reference code "
    lsstdoc = LsstDoc(input_txt)
    assert lsstdoc.handle == "LDM-503"


def test_abstract_variations():
    """Test variations on the abstract command's formatting."""
    input_txt = ("\setDocAbstract {\n"
                 "This is the  Test Plan for \product. In it we define terms "
                 "associated with testing and further test specifications for "
                 "specific items.}")
    expected_abstract = (
        "This is the  Test Plan for \product. In it we define terms "
        "associated with testing and further test specifications for "
        "specific items."
    )
    lsstdoc = LsstDoc(input_txt)
    assert lsstdoc.abstract == expected_abstract


@pytest.mark.parametrize(
    'sample, expected',
    [(r'\documentclass[DM,lsstdraft,toc]{lsstdoc}', True),
     (r'\documentclass[DM,toc]{lsstdoc}', False),
     (r'\documentclass[DM, lsstdraft, toc]{lsstdoc}', True)])
def test_is_draft(sample, expected):
    lsstdoc = LsstDoc(sample)
    assert lsstdoc.is_draft == expected


def test_dmtn_036_title(dmtn_036_data):
    lsstdoc = LsstDoc(dmtn_036_data)
    assert lsstdoc.title == ("jointcal: Simultaneous Astrometry \\& "
                             "Photometry for thousands of\nExposures with "
                             "Large CCD Mosaics")
