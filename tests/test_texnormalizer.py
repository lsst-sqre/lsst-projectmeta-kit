"""Tests for the metasrc.tex.texnormalizer module.
"""

import os
import re

import metasrc.tex.texnormalizer as texnormalizer


def test_remove_comments_abstract():
    sample = ("\setDocAbstract{%\n"
              " The LSST Data Management System (DMS) is a set of services\n"
              " employing a variety of software components running on\n"
              " computational and networking infrastructure that combine to\n"
              " deliver science data products to the observatory's users and\n"
              " support observatory operations.  This document describes the\n"
              " components, their service instances, and their deployment\n"
              " environments as well as the interfaces among them, the rest\n"
              " of the LSST system, and the outside world.\n"
              "}")
    expected = (
        "\setDocAbstract{\n"
        " The LSST Data Management System (DMS) is a set of services\n"
        " employing a variety of software components running on\n"
        " computational and networking infrastructure that combine to\n"
        " deliver science data products to the observatory's users and\n"
        " support observatory operations.  This document describes the\n"
        " components, their service instances, and their deployment\n"
        " environments as well as the interfaces among them, the rest\n"
        " of the LSST system, and the outside world.\n"
        "}")
    assert texnormalizer.remove_comments(sample) == expected


def test_escaped_remove_comments():
    """Test remove_comments where a "%" is escaped."""
    sample = "The uncertainty is 5\%.  % a comment"
    expected = "The uncertainty is 5\%.  "
    assert texnormalizer.remove_comments(sample) == expected


def test_single_line_remove_comments():
    sample = "This is content.  % a comment"
    expected = "This is content.  "
    assert texnormalizer.remove_comments(sample) == expected


def test_remove_single_line_trailing_whitespace():
    sample = "This is content.    "
    expected = "This is content."
    assert texnormalizer.remove_trailing_whitespace(sample) == expected


def test_multi_line_trailing_whitespace():
    sample = ("First line.    \n"
              "Second line. ")
    expected = ("First line.\n"
                "Second line.")
    assert texnormalizer.remove_trailing_whitespace(sample) == expected


def test_read_tex_file():
    project_dir = os.path.join(os.path.dirname(__file__), 'data', 'texinputs')
    root_filepath = os.path.join(project_dir, 'LDM-nnn.tex')
    tex_source = texnormalizer.read_tex_file(root_filepath)

    # verify that input'd and include'd content is present
    assert re.search(r'\\setDocAbstract', tex_source) is not None
    assert re.search(r'\\section{Introduction}', tex_source) is not None
