"""Ad hoc tests of the LsstLatexDoc class. Other test modules rigorously verify
LsstLatexDoc against sample documents.
"""

from pybtex.database import BibliographyData
import pytest

from lsstprojectmeta.tex.lsstdoc import LsstLatexDoc


def test_no_short_title():
    """title without a short title."""
    sample = r"\title{Title}"
    lsstdoc = LsstLatexDoc(sample)
    assert lsstdoc.title == "Title"


def test_title_variations():
    """Test variations on the title command's formatting."""
    # Test with whitespace in title command
    input_txt = r"\title    [Test Plan]  { \product ~Test Plan}"
    lsstdoc = LsstLatexDoc(input_txt)
    assert lsstdoc.title == r"\product ~Test Plan"
    assert lsstdoc.short_title == "Test Plan"


def test_author_variations():
    """Test variations on the author command's formatting."""
    input_txt = (r"\author   {William O'Mullane, Mario Juric, "
                 r"Frossie Economou}"
                 r"                  % the author(s)")
    lsstdoc = LsstLatexDoc(input_txt)
    assert lsstdoc.authors == ["William O'Mullane",
                               "Mario Juric",
                               "Frossie Economou"]


def test_handle_variations():
    """Test variations on the handle command's formatting."""
    input_txt = r"\setDocRef      {LDM-503} % the reference code "
    lsstdoc = LsstLatexDoc(input_txt)
    assert lsstdoc.handle == "LDM-503"


def test_abstract_variations():
    """Test variations on the abstract command's formatting."""
    input_txt = (r"\setDocAbstract {" + "\n"
                 r"This is the  Test Plan for \product. In it we define terms "
                 r"associated with testing and further test specifications "
                 r"for specific items.}")
    expected_abstract = (
        r"This is the  Test Plan for \product. In it we define terms "
        r"associated with testing and further test specifications for "
        r"specific items."
    )
    lsstdoc = LsstLatexDoc(input_txt)
    assert lsstdoc.abstract == expected_abstract


@pytest.mark.parametrize(
    'sample, expected',
    [(r'\documentclass[DM,lsstdraft,toc]{lsstdoc}', True),
     (r'\documentclass[DM,toc]{lsstdoc}', False),
     (r'\documentclass[DM, lsstdraft, toc]{lsstdoc}', True)])
def test_is_draft(sample, expected):
    lsstdoc = LsstLatexDoc(sample)
    assert lsstdoc.is_draft == expected


def test_html_title():
    sample = r"\title{``Complex'' title \textit{like} $1+2$}"
    expected = ('“Complex” title <em>like</em> '
                '<span class="math inline">1\u2005+\u20052</span>\n')
    lsstdoc = LsstLatexDoc(sample)
    converted = lsstdoc.html_title
    assert converted == expected


def test_default_load_bib_db():
    """Test that the common lsst-texmf bibliographies are always loaded.
    """
    lsstdoc = LsstLatexDoc('')
    assert isinstance(lsstdoc.bib_db, BibliographyData)
