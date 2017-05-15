"""Metadata extraction from lsstdoc LSST LaTeX documents."""

import re


# Title regular expression
# \\title{Title of document}"
TITLE_PATTERN = re.compile(
    r"\\title"  # title command
    r"(?:\[(?P<short_title>.*?)\])?"  # optional short title
    r"{(?P<title>.*?)}")  # primary title


class LsstDoc(object):
    """lsstdoc LaTeX document source.

    Parameters
    ----------
    tex_source : `str`
        LaTeX source for the main file of an lsstdoc LaTeX document.
    """

    def __init__(self, tex_source):
        super().__init__()
        self._tex = tex_source

        self._parse_title()

    def _parse_title(self):
        """Parse the title from TeX source."""
        matches = TITLE_PATTERN.search(self._tex)
        if matches is not None:
            self._title = matches.group('title')
            self._short_title = matches.group('short_title')

    @property
    def title(self):
        """Document title (`str`)."""
        if hasattr(self, '_title'):
            return self._title
        else:
            return None

    @property
    def short_title(self):
        """Document short title (`str`)."""
        if hasattr(self, '_short_title'):
            return self._short_title
        else:
            return None
