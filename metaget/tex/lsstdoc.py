"""Metadata extraction from lsstdoc LSST LaTeX documents."""

import re


# Title regular expression
# \\title{Title of document}"
TITLE_PATTERN = re.compile(
    r"\\title"  # title command
    r"(?:\[(?P<short_title>.*?)\])?"  # optional short title
    r"{(?P<title>.*?)}")  # primary title

# Author regular expression
AUTHOR_PATTERN = re.compile(
    r"\\author"
)


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
        self._parse_author()

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

    @property
    def authors(self):
        """Authors (`list` of `str`)."""
        if hasattr(self, '_authors'):
            return self._authors
        else:
            return []

    def _parse_title(self):
        """Parse the title from TeX source."""
        match = TITLE_PATTERN.search(self._tex)
        if match is not None:
            self._title = match.group('title')
            self._short_title = match.group('short_title')

    def _parse_author(self):
        """Parse the author from TeX source.

        goal is to parse::

           \author{
           A.~Author,
           B.~Author,
           and
           C.~Author}

        Into::

           ['A. Author', 'B. Author', 'C. Author']
        """
        match = AUTHOR_PATTERN.search(self._tex)
        if match:
            # start of content is character after the \author tag pattern match
            start = match.end(0)
            content = self._extract_in_brackets(start)

            # Clean content
            content = content.replace('\n', ' ')
            content = content.replace('~', ' ')
            content = content.strip()

            # Split content into list of individual authors
            authors = []
            for part in content.split(','):
                part = part.strip()
                if 'and' in part:
                    for split_part in part.split('and'):
                        split_part = split_part.strip()
                        if len(split_part) > 0:
                            authors.append(split_part)
                else:
                    authors.append(part)
            self._authors = authors

    def _extract_in_brackets(self, start, opening='{', closing='}'):
        """Extract text found inside delimiters

        Parameters
        ----------
        start : `int`
            Start index into ``self._tex`` where the opening delimiter can be
            found.
        opening : `str`, optional
            Opening delimiter.
        closing : `str`, optional
            Closing delimiter.
        """
        if self._tex[start] != opening:
            message = "Starting character is not an opening delimeter: {0}"
            raise RuntimeError(message.format(self._tex[start]))

        balance = 0
        for i, c in enumerate(self._tex[start:]):
            if c == opening:
                balance += 1
            elif c == closing:
                balance -= 1
            if balance == 0:
                break

        # Text inside delimiters; exclude the delimiters themselves
        return self._tex[start+1:start+i]
