"""Metadata extraction from lsstdoc LSST LaTeX documents."""

__all__ = ['LsstDoc']

from .commandparser import LatexCommand


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

        self._parse_documentclass()
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

    @property
    def is_draft(self):
        """Document is a draft if ``'lsstdoc'`` is included in the
        documentclass options (`bool`).
        """
        if hasattr(self, '_document_options'):
            if 'lsstdraft' in self._document_options:
                return True
        return False

    def _parse_documentclass(self):
        """Parse documentclass options."""
        command = LatexCommand(
            'documentclass',
            {'name': 'options', 'required': False, 'bracket': '['},
            {'name': 'class_name', 'required': True, 'bracket': '{'})
        try:
            parsed = next(command.parse(self._tex))
        except StopIteration:
            return

        try:
            content = parsed['options']
            self._document_options = [opt.strip()
                                      for opt in content.split(',')]
        except KeyError:
            pass

    def _parse_title(self):
        """Parse the title from TeX source."""
        command = LatexCommand(
            'title',
            {'name': 'short_title', 'required': False, 'bracket': '['},
            {'name': 'long_title', 'required': True, 'bracket': '{'})
        try:
            parsed = next(command.parse(self._tex))
        except StopIteration:
            return

        self._title = parsed['long_title']

        try:
            self._short_title = parsed['short_title']
        except KeyError:
            pass

    def _parse_doc_ref(self):
        """Parse the document handle."""
        command = LatexCommand(
            'setDocRef',
            {'name': 'handle', 'required': True, 'bracket': '{'})
        try:
            parsed = next(command.parse(self._tex))
        except StopIteration:
            return

        self._handle = parsed['handle']
        self._series, self._serial = self._handle.split('-', 1)

    def _parse_author(self):
        """Parse the author from TeX source.

        Goal is to parse::

           \author{
           A.~Author,
           B.~Author,
           and
           C.~Author}

        Into::

           ['A. Author', 'B. Author', 'C. Author']
        """
        command = LatexCommand(
            'author',
            {'name': 'authors', 'required': True, 'bracket': '{'})
        try:
            parsed = next(command.parse(self._tex))
        except StopIteration:
            return

        try:
            content = parsed['authors']
        except KeyError:
            return

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
        command = LatexCommand(
            'setDocAbstract',
            {'name': 'abstract', 'required': True, 'bracket': '{'})
        try:
            parsed = next(command.parse(self._tex))
        except StopIteration:
            return

        try:
            content = parsed['abstract']
        except KeyError:
            return

        content = content.strip()
        # TODO probably want to unwrap paragraphs.
        self._abstract = content
