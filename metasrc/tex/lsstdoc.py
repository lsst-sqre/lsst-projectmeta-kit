"""Metadata extraction from lsstdoc LSST LaTeX documents."""

import re


# Title regular expression
# \\title{Title of document}"
TITLE_PATTERN = re.compile(
    r"\\title\s*"  # title command, with optional whitespace
    r"(?:\[(?P<short_title>.*?)\])?"  # optional short title
    r"\s*"  # optional whitespace between items, before braces
    r"{(?P<title>.*?)}")  # primary title

# Author regular expression
AUTHOR_PATTERN = re.compile(
    r"\\author"
    r"\s*"  # optional whitespace between items, before braces
)

# Abstract regular expression
ABSTRACT_PATTERN = re.compile(
    r"\\setDocAbstract"
    r"\s*"  # optional whitespace after command, before braces
)

# Document reference (handle) regular expression
DOCREF_PATTERN = re.compile(
    r"\\setDocRef\s*{(?P<handle>.*?)}"
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
        self._parse_abstract()
        self._parse_doc_ref()

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

    @property
    def abstract(self):
        """Abstract (`str`)."""
        if hasattr(self, '_abstract'):
            return self._abstract
        else:
            return None

    @property
    def handle(self):
        """Document handle (`str`)."""
        if hasattr(self, '_handle'):
            return self._handle
        else:
            return None

    @property
    def series(self):
        """Document series (`str`)."""
        if hasattr(self, '_series'):
            return self._series
        else:
            return None

    @property
    def serial(self):
        """Document serial number within series (`str`)."""
        if hasattr(self, '_serial'):
            return self._serial
        else:
            return None

    def _parse_title(self):
        """Parse the title from TeX source."""
        match = TITLE_PATTERN.search(self._tex)
        if match is not None:
            self._title = match.group('title')
            self._short_title = match.group('short_title')

    def _parse_doc_ref(self):
        """Parse the document handle."""
        match = DOCREF_PATTERN.search(self._tex)
        if match is not None:
            self._handle = match.group('handle')
            self._series, self._serial = self._handle.split('-', 1)

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

    def _parse_abstract(self):
        match = ABSTRACT_PATTERN.search(self._tex)
        if match:
            start = match.end(0)
            content = self._extract_in_brackets(start)
            content = content.strip()
            # TODO probably want to unwrap paragraphs.
            self._abstract = content

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
        return self._tex[start + 1:start + i]
