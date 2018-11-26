"""Tests for lsstprojectmeta.tex.scraper.
"""

from lsstprojectmeta.tex import scraper


def test_get_def_macros():
    sample = r"\def \name {content}"
    macros = scraper.get_def_macros(sample)

    assert r'\name' in macros
    assert macros[r'\name'] == 'content'


def test_get_def_macros_LDM_503():
    sample = (r'\documentclass[DM,STP,toc]{lsstdoc}' + '\n'
              '%set the WP number or product here for the requirements\n'
              r'\def\product{Data Management}' + '\n'
              r'\def\cycle{S17}' + '\n')
    macros = scraper.get_def_macros(sample)

    assert macros[r'\product'] == 'Data Management'
    assert macros[r'\cycle'] == 'S17'


def test_get_newcommand_macros():
    sample = r"\newcommand {\name} {content}"
    macros = scraper.get_newcommand_macros(sample)
    assert macros[r'\name'] == 'content'

    sample = r"\newcommand { \name } {content}"
    macros = scraper.get_newcommand_macros(sample)
    assert macros[r'\name'] == 'content'

    sample = r"\newcommand{\name}{content}"
    macros = scraper.get_newcommand_macros(sample)
    assert macros[r'\name'] == 'content'
