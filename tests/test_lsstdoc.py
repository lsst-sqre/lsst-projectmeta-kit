"""Ad hoc tests of the LsstDoc class. Other test modules rigorously verify
LsstDoc against sample documents.
"""

from pybtex.database import BibliographyData
import pytest

from metasrc.tex.lsstdoc import LsstDoc


def test_no_short_title():
    """title without a short title."""
    sample = r"\title{Title}"
    lsstdoc = LsstDoc(sample)
    assert lsstdoc.title == "Title"


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


def test_html_title():
    sample = "\\title{``Complex'' title \\textit{like} $1+2$}"
    expected = ('“Complex” title <em>like</em> '
                '<span class="math inline">1\u2005+\u20052</span>\n')
    lsstdoc = LsstDoc(sample)
    converted = lsstdoc.html_title
    assert converted == expected


def test_default_load_bib_db():
    """Test that the common lsst-texmf bibliographies are always loaded.
    """
    lsstdoc = LsstDoc('')
    assert isinstance(lsstdoc.bib_db, BibliographyData)
