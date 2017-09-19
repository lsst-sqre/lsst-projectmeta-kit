"""Tests for the metasrc.tex.lsstbib module.
"""

from metasrc.tex.lsstbib import get_lsst_bibtex


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
