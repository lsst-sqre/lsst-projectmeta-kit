"""Test the metasrc.tex.citelink module.
"""

import pytest

from metasrc.tex.citelink import CitedsLinker, CitedspLinker


@pytest.mark.parametrize(
    'sample,expected',
    # Basic citeds command
    [('\citeds{LDM-151}', '\href{https://ls.st/LDM-151}{LDM-151}'),
     # With an alternative title text
     ('\citeds[Pipelines Design]{LDM-151}',
      '\href{https://ls.st/LDM-151}{Pipelines Design}'),
     # Two citeds commands
     ('\citeds[Pipelines Design]{LDM-151} \citeds{LDM-230}',
      '\href{https://ls.st/LDM-151}{Pipelines Design} '
      '\href{https://ls.st/LDM-230}{LDM-230}')])
def test_citeds(sample, expected):
    replace_citeds = CitedsLinker()
    assert replace_citeds(sample) == expected


@pytest.mark.parametrize(
    'sample,expected',
    # Basic citedsp command
    [('\citedsp{LDM-151}', '[\href{https://ls.st/LDM-151}{LDM-151}]'),
     # With an alternative title text
     ('\citedsp[Pipelines Design]{LDM-151}',
      '[\href{https://ls.st/LDM-151}{Pipelines Design}]'),
     # Two citedsp commands
     ('\citedsp[Pipelines Design]{LDM-151} \citedsp{LDM-230}',
      '[\href{https://ls.st/LDM-151}{Pipelines Design}] '
      '[\href{https://ls.st/LDM-230}{LDM-230}]')])
def test_citedsp(sample, expected):
    replace_citedsp = CitedspLinker()
    assert replace_citedsp(sample) == expected
