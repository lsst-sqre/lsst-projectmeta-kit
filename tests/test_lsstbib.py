"""Tests for the lsstprojectmeta.tex.lsstbib module.
"""

from pybtex.database import BibliographyData, parse_string
import pytest

from lsstprojectmeta.tex.lsstbib import (
    get_lsst_bibtex, get_bibliography,
    get_url_from_entry, NoEntryUrlError,
    get_authoryear_from_entry, AuthorYearError)


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


def test_get_docushare_url_from_entry():
    bibtex = (
        '@DocuShare{LDM-151,\n'
        '    author =       {John D. Swinbank and others},\n'
        '    title =        "{Data Management Science Pipelines Design}",\n'
        '    year =         2017,\n'
        '    month =        may,\n'
        '    handle =       {LDM-151},\n'
        '}\n'
    )
    db = parse_string(bibtex, 'bibtex')
    entry = db.entries['LDM-151']
    assert get_url_from_entry(entry) == 'https://ls.st/LDM-151'


def test_get_ads_url_from_entry():
    bibtex = (
        r'@ARTICLE{2009MNRAS.400.1181Z,' + '\n'
        r' author = {{Zibetti}, S. and {Charlot}, S. and {Rix}, H.-W.},' + '\n'
        r' title = "{Resolved stellar mass maps of galaxies - I. Method and '
        r' implications for global mass estimates}",' + '\n'
        r' journal = {\mnras},' + '\n'
        r'archivePrefix = "arXiv",' + '\n'
        r' eprint = {0904.4252},' + '\n'
        r' primaryClass = "astro-ph.CO",' + '\n'
        r' keywords = {techniques: image processing , '
        r'techniques: photometric , galaxies: fundamental parameters , '
        r'galaxies: general , galaxies: photometry , '
        r'galaxies: stellar content},' + '\n'
        r'     year = 2009,' + '\n'
        r'    month = dec,' + '\n'
        r'   volume = 400,' + '\n'
        r'    pages = {1181-1198},' + '\n'
        r'      doi = {10.1111/j.1365-2966.2009.15528.x},' + '\n'
        r'adsurl = {http://adsabs.harvard.edu/abs/2009MNRAS.400.1181Z},' + '\n'
        r'adsnote = {Provided by the SAO/NASA Astrophysics Data System}' + '\n'
        r'}' + '\n'
    )
    db = parse_string(bibtex, 'bibtex')
    entry = db.entries['2009MNRAS.400.1181Z']
    expected = 'http://adsabs.harvard.edu/abs/2009MNRAS.400.1181Z'
    assert get_url_from_entry(entry) == expected


def test_get_doi_url_from_entry():
    bibtex = (
        '@ARTICLE{2009MNRAS.400.1181Z,\n'
        '  author = {{Zibetti}, S. and {Charlot}, S. and {Rix}, H.-W.},\n'
        '  title = "{Resolved stellar mass maps of galaxies - I. Method and '
        '  implications for global mass estimates}",\n'
        r'  journal = {\mnras},' + '\n'
        'archivePrefix = "arXiv",\n'
        '   eprint = {0904.4252},\n'
        ' primaryClass = "astro-ph.CO",\n'
        ' keywords = {techniques: image processing , '
        'techniques: photometric , galaxies: fundamental parameters , '
        'galaxies: general , galaxies: photometry , '
        'galaxies: stellar content},\n'
        '     year = 2009,\n'
        '    month = dec,\n'
        '   volume = 400,\n'
        '    pages = {1181-1198},\n'
        '      doi = {10.1111/j.1365-2966.2009.15528.x},\n'
        '  adsnote = {Provided by the SAO/NASA Astrophysics Data System}\n'
        '}\n'
    )
    db = parse_string(bibtex, 'bibtex')
    entry = db.entries['2009MNRAS.400.1181Z']
    expected = 'https://doi.org/10.1111/j.1365-2966.2009.15528.x'
    assert get_url_from_entry(entry) == expected


def test_get_url_from_entry():
    bibtex = (
        '@ARTICLE{2009MNRAS.400.1181Z,\n'
        '  author = {{Zibetti}, S. and {Charlot}, S. and {Rix}, H.-W.},\n'
        '  title = "{Resolved stellar mass maps of galaxies - I. Method and '
        '  implications for global mass estimates}",\n'
        r'  journal = {\mnras},' + '\n'
        'archivePrefix = "arXiv",\n'
        '   eprint = {0904.4252},\n'
        ' primaryClass = "astro-ph.CO",\n'
        ' keywords = {techniques: image processing , '
        'techniques: photometric , galaxies: fundamental parameters , '
        'galaxies: general , galaxies: photometry , '
        'galaxies: stellar content},\n'
        '     year = 2009,\n'
        '    month = dec,\n'
        '   volume = 400,\n'
        '    pages = {1181-1198},\n'
        '   url = {http://adsabs.harvard.edu/abs/2009MNRAS.400.1181Z},\n'
        '  adsnote = {Provided by the SAO/NASA Astrophysics Data System}\n'
        '}\n'
    )
    db = parse_string(bibtex, 'bibtex')
    entry = db.entries['2009MNRAS.400.1181Z']
    expected = 'http://adsabs.harvard.edu/abs/2009MNRAS.400.1181Z'
    assert get_url_from_entry(entry) == expected


def test_get_no_url_from_entry():
    bibtex = (
        '@ARTICLE{2009MNRAS.400.1181Z,\n'
        '  author = {{Zibetti}, S. and {Charlot}, S. and {Rix}, H.-W.},\n'
        '  title = "{Resolved stellar mass maps of galaxies - I. Method and '
        '  implications for global mass estimates}",\n'
        r'  journal = {\mnras},' + '\n'
        'archivePrefix = "arXiv",\n'
        '   eprint = {0904.4252},\n'
        ' primaryClass = "astro-ph.CO",\n'
        ' keywords = {techniques: image processing , '
        'techniques: photometric , galaxies: fundamental parameters , '
        'galaxies: general , galaxies: photometry , '
        'galaxies: stellar content},\n'
        '     year = 2009,\n'
        '    month = dec,\n'
        '   volume = 400,\n'
        '    pages = {1181-1198},\n'
        '  adsnote = {Provided by the SAO/NASA Astrophysics Data System}\n'
        '}\n'
    )
    db = parse_string(bibtex, 'bibtex')
    entry = db.entries['2009MNRAS.400.1181Z']
    with pytest.raises(NoEntryUrlError):
        get_url_from_entry(entry)


def test_get_authoryear():
    bibtex = (
        '@DocuShare{LDM-151,\n'
        '    author =       {John D. Swinbank and others},\n'
        '    title =        "{Data Management Science Pipelines Design}",\n'
        '    year =         2017,\n'
        '    month =        may,\n'
        '    handle =       {LDM-151},\n'
        '}\n'
    )
    db = parse_string(bibtex, 'bibtex')
    entry = db.entries['LDM-151']
    expected = 'Swinbank and others 2017'
    assert get_authoryear_from_entry(entry) == expected

    expected = 'Swinbank and others (2017)'
    assert get_authoryear_from_entry(entry, paren=True) == expected


def test_get_authoryear_single_author():
    bibtex = (
        '@DocuShare{LDM-151,\n'
        '    author =       {John D. Swinbank},\n'
        '    title =        "{Data Management Science Pipelines Design}",\n'
        '    year =         2017,\n'
        '    month =        may,\n'
        '    handle =       {LDM-151},\n'
        '}\n'
    )
    db = parse_string(bibtex, 'bibtex')
    entry = db.entries['LDM-151']
    expected = 'Swinbank 2017'
    assert get_authoryear_from_entry(entry) == expected

    expected = 'Swinbank (2017)'
    assert get_authoryear_from_entry(entry, paren=True) == expected


def test_get_authoryear_exception():
    # No year in this entry
    bibtex = (
        '@DocuShare{LDM-151,\n'
        '    author =       {John D. Swinbank},\n'
        '    title =        "{Data Management Science Pipelines Design}",\n'
        '    month =        may,\n'
        '    handle =       {LDM-151},\n'
        '}\n'
    )
    db = parse_string(bibtex, 'bibtex')
    entry = db.entries['LDM-151']
    with pytest.raises(AuthorYearError):
        get_authoryear_from_entry(entry)
