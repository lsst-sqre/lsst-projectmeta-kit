"""Tests for the metasrc.tex.lsstbib module.
"""

from pybtex.database import BibliographyData

from metasrc.tex.lsstbib import get_lsst_bibtex, get_bibliography


def test_get_lsst_bibtex():
    bibtex = get_lsst_bibtex()
    assert 'lsst' in bibtex
    assert 'lsst-dm' in bibtex
    assert 'refs' in bibtex
    assert 'books' in bibtex
    assert 'refs_ads' in bibtex

    # Repeat (exercises cache)
    bibtex = get_lsst_bibtex()
    assert 'lsst' in bibtex
    assert 'lsst-dm' in bibtex
    assert 'refs' in bibtex
    assert 'books' in bibtex
    assert 'refs_ads' in bibtex


def test_get_bibliography():
    bib = get_bibliography()
    assert isinstance(bib, BibliographyData)

    # Key from 'lsst' bibtex file
    assert 'LDM-151' in bib.entries
    # Key from 'lsst-dm' bibtex file
    assert '2002SPIE.4844..225C' in bib.entries
    # Key from 'refs' bibtex file
    assert '1991.Spyak.OpticalEngineering' in bib.entries
    # Key from 'books' bibtex file
    assert 'Adass08' in bib.entries
    # Key from 'refs_ads' bibtex file
    assert '1727RSPT...35..637B' in bib.entries
