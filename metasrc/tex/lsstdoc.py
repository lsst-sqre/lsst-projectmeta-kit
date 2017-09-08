"""Metadata extraction from lsstdoc LSST LaTeX documents."""

__all__ = ['LsstDoc']

import logging

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
        self._logger = logging.getLogger(__name__)

        self._tex = tex_source

    @property
    def title(self):
        """LaTeX-formatted document title (`str`)."""
        if not hasattr(self, '_title'):
            self._parse_title()

        return self._title

    @property
    def short_title(self):
        """LaTeX-formatted document short title (`str`)."""
        if not hasattr(self, '_short_title'):
            self._parse_title()

        return self._short_title

    @property
    def authors(self):
        """LaTeX-formatted authors (`list` of `str`)."""
        if not hasattr(self, '_authors'):
            self._parse_author()

        return self._authors

    @property
    def abstract(self):
        """LaTeX-formatted abstract (`str`)."""
        if not hasattr(self, '_abstract'):
            self._parse_abstract()

        return self._abstract

    @property
    def handle(self):
        """LaTeX-formatted document handle (`str`)."""
        if not hasattr(self, '_handle'):
            self._parse_doc_ref()

        return self._handle

    @property
    def series(self):
        """Document series identifier (`str`)."""
        if not hasattr(self, '_series'):
            self._parse_doc_ref()

        return self._series

    @property
    def serial(self):
        """Document serial number within series (`str`)."""
        if not hasattr(self, '_serial'):
            self._parse_doc_ref()

        return self._serial

    @property
    def is_draft(self):
        """Document is a draft if ``'lsstdoc'`` is included in the
        documentclass options (`bool`).
        """
        if not hasattr(self, '_document_options'):
            self._parse_documentclass()

        if 'lsstdraft' in self._document_options:
            return True
        else:
            return False

    def _parse_documentclass(self):
        """Parse documentclass options.

        Sets the the ``_document_options`` attribute.
        """
        command = LatexCommand(
            'documentclass',
            {'name': 'options', 'required': False, 'bracket': '['},
            {'name': 'class_name', 'required': True, 'bracket': '{'})
        try:
            parsed = next(command.parse(self._tex))
        except StopIteration:
            self._logger.warning('lsstdoc has no documentclass')
            self._document_options = []

        try:
            content = parsed['options']
            self._document_options = [opt.strip()
                                      for opt in content.split(',')]
        except KeyError:
            self._logger.warning('lsstdoc has no documentclass options')
            self._document_options = []

    def _parse_title(self):
        """Parse the title from TeX source.

        Sets these attributes:

        - ``_title``
        - ``_short_title``
        """
        command = LatexCommand(
            'title',
            {'name': 'short_title', 'required': False, 'bracket': '['},
            {'name': 'long_title', 'required': True, 'bracket': '{'})
        try:
            parsed = next(command.parse(self._tex))
        except StopIteration:
            self._logger.warning('lsstdoc has no title')
            self._title = None
            self._short_title = None

        self._title = parsed['long_title']

        try:
            self._short_title = parsed['short_title']
        except KeyError:
            self._logger.warning('lsstdoc has no short title')
            self._short_title = None

    def _parse_doc_ref(self):
        """Parse the document handle.

        Sets the ``_series``, ``_serial``, and ``_handle`` attributes.
        """
        command = LatexCommand(
            'setDocRef',
            {'name': 'handle', 'required': True, 'bracket': '{'})
        try:
            parsed = next(command.parse(self._tex))
        except StopIteration:
            self._logger.warning('lsstdoc has no setDocRef')
            self._handle = None
            self._series = None
            self._serial = None
            return

        self._handle = parsed['handle']
        try:
            self._series, self._serial = self._handle.split('-', 1)
        except ValueError:
            self._logger.warning('lsstdoc handle cannot be parsed into '
                                 'series and serial: %r', self._handle)
            self._series = None
            self._serial = None

    def _parse_author(self):
        """Parse the author from TeX source.

        Sets the ``_authors`` attribute.

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
            self._logger.warning('lsstdoc has no author')
            self._authors = []
            return

        try:
            content = parsed['authors']
        except KeyError:
            self._logger.warning('lsstdoc has no author')
            self._authors = []
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
        """Parse the abstract from the TeX source.

        Sets the ``_abstract`` attribute.
        """
        command = LatexCommand(
            'setDocAbstract',
            {'name': 'abstract', 'required': True, 'bracket': '{'})
        try:
            parsed = next(command.parse(self._tex))
        except StopIteration:
            self._logger.warning('lsstdoc has no abstract')
            self._abstract = None
            return

        try:
            content = parsed['abstract']
        except KeyError:
            self._logger.warning('lsstdoc has no abstract')
            self._abstract = None
            return

        content = content.strip()
        self._abstract = content
