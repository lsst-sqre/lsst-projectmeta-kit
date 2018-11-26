"""Test the lsstprojectmeta.tex.citelink module.
"""

import pytest

from lsstprojectmeta.tex.citelink import (
    CitedsLinker, CitedspLinker, CitepLinker)
from lsstprojectmeta.tex.lsstbib import get_bibliography


@pytest.mark.parametrize(
    'sample,expected',
    # Basic citeds command
    [(r'\citeds{LDM-151}', r'\href{https://ls.st/LDM-151}{LDM-151}'),
     # With an alternative title text
     (r'\citeds[Pipelines Design]{LDM-151}',
      r'\href{https://ls.st/LDM-151}{Pipelines Design}'),
     # Two citeds commands
     (r'\citeds[Pipelines Design]{LDM-151} \citeds{LDM-230}',
      r'\href{https://ls.st/LDM-151}{Pipelines Design} '
      r'\href{https://ls.st/LDM-230}{LDM-230}')])
def test_citeds(sample, expected):
    replace_citeds = CitedsLinker()
    assert replace_citeds(sample) == expected


@pytest.mark.parametrize(
    'sample,expected',
    # Basic citedsp command
    [(r'\citedsp{LDM-151}', r'[\href{https://ls.st/LDM-151}{LDM-151}]'),
     # With an alternative title text
     (r'\citedsp[Pipelines Design]{LDM-151}',
      r'[\href{https://ls.st/LDM-151}{Pipelines Design}]'),
     # Two citedsp commands
     (r'\citedsp[Pipelines Design]{LDM-151} \citedsp{LDM-230}',
      r'[\href{https://ls.st/LDM-151}{Pipelines Design}] '
      r'[\href{https://ls.st/LDM-230}{LDM-230}]')])
def test_citedsp(sample, expected):
    replace_citedsp = CitedspLinker()
    assert replace_citedsp(sample) == expected


@pytest.mark.parametrize(
    'sample,expected',
    # Basic citedp command, single author
    [(r'\citep{1996PASP..108..851S}',
      r'[\href{http://adsabs.harvard.edu/abs/'
      r'1996PASP..108..851S}{Stetson 1996}]'),
     # Basic citep command, multi author
     (r'\citep{2017ApJ...838....5L}',
      r'[\href{http://adsabs.harvard.edu/abs/'
      r'2017ApJ...838....5L}{Leistedt and Hogg 2017}]'),
     # Basic citep command, multi author
     (r'\citep{1996PASP..108..851S, 2017ApJ...838....5L}',
      r'[\href{http://adsabs.harvard.edu/abs/'
      r'1996PASP..108..851S}{Stetson 1996}, '
      r'\href{http://adsabs.harvard.edu/abs/'
      r'2017ApJ...838....5L}{Leistedt and Hogg 2017}]')])
def test_citep(sample, expected):
    db = get_bibliography()
    replace_citep = CitepLinker(bibtex_database=db)
    assert replace_citep(sample) == expected
