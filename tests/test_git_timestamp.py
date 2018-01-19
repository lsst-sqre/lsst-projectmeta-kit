"""Tests for the lsstprojectmeta.git.timestamp.
"""

from datetime import datetime
import os

import pytest

from lsstprojectmeta.git.timestamp import (
    read_git_commit_timestamp_for_file,
    _iter_filepaths_with_extension,
    get_content_commit_date)


def test_git_commit_timestamp_for_file():
    """Smoke-test read_git_commit_timestamp_for_file with README.rst in
    lsstprojectmeta's own Git repo.
    """
    test_dir = os.path.dirname(__file__)
    readme_path = os.path.abspath(os.path.join(test_dir, '..', 'README.rst'))
    timestamp = read_git_commit_timestamp_for_file(readme_path)
    assert isinstance(timestamp, datetime)


def test_git_commit_timestamp_for_file_nonexistent():
    """Smoke-test read_git_commit_timestamp_for_file with README.rst in
    lsstprojectmeta's own Git repo.
    """
    path = 'doesnt_exist.txt'
    with pytest.raises(IOError):
        read_git_commit_timestamp_for_file(path)


def test_iter_filepaths_with_extension():
    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    filepaths = _iter_filepaths_with_extension('py', root_dir=repo_dir)
    assert os.path.join('tests', 'test_git_timestamp.py') in filepaths
    assert 'README.rst' not in filepaths


def test_get_project_content_commit_date():
    """Smoke test using the lsstprojectmeta repo.
    """
    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    commit_date = get_content_commit_date(('rst', 'py'), root_dir=repo_dir)
    assert isinstance(commit_date, datetime)

    # Verify file search is case sensitive
    with pytest.raises(RuntimeError):
        get_content_commit_date(('RST', 'PY'), root_dir=repo_dir)
