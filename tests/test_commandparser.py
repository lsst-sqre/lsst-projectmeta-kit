"""Tests for the tex.commandparser module.
"""

import os
import re

import pytest

from lsstprojectmeta.tex.commandparser import LatexCommand


@pytest.fixture
def ldm_nnn_data():
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'LDM-nnn.tex')
    with open(data_path) as f:
        source = f.read()
    return source


def test_sample_title(ldm_nnn_data):
    """Test parsing the title command from the LDM-nnn name."""
    elements = [
        {'name': 'short_title', 'required': False, 'bracket': '['},
        {'name': 'long_title', 'required': True, 'bracket': '{'}
    ]
    command = LatexCommand('title', *elements)
    parsed_commands = list(command.parse(ldm_nnn_data))

    assert len(parsed_commands) == 1

    parsed = parsed_commands[0]
    assert parsed['long_title'] == 'Title of document'
    assert parsed['short_title'] == 'Short title'

    assert 'short_title' in parsed
    assert 'long_title' in parsed


def test_simple_title():
    """Test parsing the title command for a trivial source sample."""
    sample = (r"Hello world\n\title[Short]{Title}\nFin\n"
              r"\setDocRef{LDM-nnn}\n")
    elements = [
        {'name': 'short_title', 'required': False, 'bracket': '['},
        {'name': 'long_title', 'required': True, 'bracket': '{'}
    ]
    command = LatexCommand('title', *elements)
    parsed = next(command.parse(sample))

    assert parsed['long_title'] == 'Title'
    assert parsed['short_title'] == 'Short'

    assert 'short_title' in parsed
    assert 'long_title' in parsed


def test_no_short_title():
    """Test parsing the title command for a trivial source sample that
    doesn't include a short title.
    """
    sample = ("Hello world\n" + r"\title{Title}" + "\nFin\n"
              r"\setDocRef{LDM-nnn}" + "\n")
    elements = [
        {'name': 'short_title', 'required': False, 'bracket': '['},
        {'name': 'long_title', 'required': True, 'bracket': '{'}
    ]
    command = LatexCommand('title', *elements)
    parsed = next(command.parse(sample))

    assert parsed['long_title'] == 'Title'
    with pytest.raises(KeyError):
        parsed['short_title']

    assert 'short_title' not in parsed
    assert 'long_title' in parsed


def test_no_short_title_v2():
    """Test parsing the title command for a trivial source sample that
    doesn't include a short title, but where the [..]{..} does occur
    elsewhere.
    """
    sample = ("Hello world\n" + r"\title{Title}" + "\nFin\n"
              r"\setDocRef[Trap]{LDM-nnn}" + "\n")
    elements = [
        {'name': 'short_title', 'required': False, 'bracket': '['},
        {'name': 'long_title', 'required': True, 'bracket': '{'}
    ]
    command = LatexCommand('title', *elements)
    parsed = next(command.parse(sample))

    assert parsed['long_title'] == 'Title'
    with pytest.raises(KeyError):
        parsed['short_title']

    assert 'short_title' not in parsed
    assert 'long_title' in parsed


@pytest.mark.parametrize(
    'command,sample',
    [('title', '% hello\n' + r'\title{Hello world}'),
     ('title', '% hello\n' + r'\title{Hello world}' + '\n'
         r'\titlename{Imposter}')])
def test_command_regex(command, sample):
    """Test the regex make my LatexCommand._make_command_regex to ensure that
    it detects the command and not look-alike latex commands. Each sample
    should have only one detection.
    """
    command_regex = LatexCommand._make_command_regex(command)
    matches = re.findall(command_regex, sample)
    assert len(matches) == 1


def test_optional_bracket():
    """Test parsing a command where the sole token has no brackets around it.
    """
    sample = (
        "Hello.\n\n"
        r"\input test.tex"
        "\n\nMore content."
    )

    command = LatexCommand(
        'input',
        {'name': 'filename', 'required': True, 'bracket': '{'}
    )
    parsed = next(command.parse(sample))
    assert parsed['filename'] == 'test.tex'
