"""Metadata extraction from lsstdoc LSST LaTeX documents."""

__all__ = ['LsstDoc']

import logging

from .commandparser import LatexCommand
from ..pandoc.convert import convert_lsstdoc_tex
from .scraper import get_macros
from .texnormalizer import read_tex_file, replace_macros


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

    @classmethod
    def read(cls, root_tex_path):
        """Construct an `LsstDoc` instance by reading and parsing the LaTeX
        source.

        Parameters
        ----------
        root_tex_path : `str`
            Path to the LaTeX source on the filesystem. For multi-file LaTeX
            projects this should be the path to the root document.

        Notes
        -----
        This method implements the following pipeline:

        1. `metasrc.tex.texnormalizer.read_tex_file`
        2. `metasrc.tex.scraper.get_macros`
        3. `metasrc.tex.texnormalizer.replace_macros`

        Thus ``input`` and ``includes`` are resolved along with simple macros.
        """
        # Read and normalize the TeX source, replacing macros with content
        tex_source = read_tex_file(root_tex_path)
        tex_macros = get_macros(tex_source)
        tex_source = replace_macros(tex_source, tex_macros)
        return cls(tex_source)

    @property
    def html_title(self):
        """HTML5-formatted document title (`str`)."""
        return self.format_title(format='html5', deparagraph=True,
                                 mathjax=False, smart=True)

    @property
    def title(self):
        """LaTeX-formatted document title (`str`)."""
        if not hasattr(self, '_title'):
            self._parse_title()

        return self._title

    @property
    def html_short_title(self):
        """HTML5-formatted document short title (`str`)."""
        return self.format_short_title(format='html5', deparagraph=True,
                                       mathjax=False, smart=True)

    @property
    def short_title(self):
        """LaTeX-formatted document short title (`str`)."""
        if not hasattr(self, '_short_title'):
            self._parse_title()

        return self._short_title

    @property
    def html_authors(self):
        """HTML5-formatted authors (`list` of `str`)."""
        return self.format_authors(format='html5', deparagraph=True,
                                   mathjax=False, smart=True)

    @property
    def authors(self):
        """LaTeX-formatted authors (`list` of `str`)."""
        if not hasattr(self, '_authors'):
            self._parse_author()

        return self._authors

    @property
    def html_abstract(self):
        """HTML5-formatted document abstract (`str`)."""
        return self.format_abstract(format='html5', deparagraph=False,
                                    mathjax=False, smart=True)

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

    def format_title(self, format='html5', deparagraph=True, mathjax=False,
                     smart=True, extra_args=None):
        """Get the document title in the specified markup format.

        Parameters
        ----------
        format : `str`, optional
            Output format (such as ``'html5'`` or ``'plain'``).
        deparagraph : `bool`, optional
            Remove the paragraph tags from single paragraph content.
        mathjax : `bool`, optional
            Allow pandoc to use MathJax math markup.
        smart : `True`, optional
            Allow pandoc to create "smart" unicode punctuation.
        extra_args : `list`, optional
            Additional command line flags to pass to Pandoc. See
            `metasrc.pandoc.convert.convert_text`.

        Returns
        -------
        output_text : `str`
            Converted content or `None` if the title is not available in
            the document.
        """
        if self.title is None:
            return None

        output_text = convert_lsstdoc_tex(
            self.title, 'html5',
            deparagraph=deparagraph,
            mathjax=mathjax,
            smart=smart,
            extra_args=extra_args)
        return output_text

    def format_short_title(self, format='html5', deparagraph=True,
                           mathjax=False, smart=True, extra_args=None):
        """Get the document short title in the specified markup format.

        Parameters
        ----------
        format : `str`, optional
            Output format (such as ``'html5'`` or ``'plain'``).
        deparagraph : `bool`, optional
            Remove the paragraph tags from single paragraph content.
        mathjax : `bool`, optional
            Allow pandoc to use MathJax math markup.
        smart : `True`, optional
            Allow pandoc to create "smart" unicode punctuation.
        extra_args : `list`, optional
            Additional command line flags to pass to Pandoc. See
            `metasrc.pandoc.convert.convert_text`.

        Returns
        -------
        output_text : `str`
            Converted content or `None` if the short title is not available in
            the document.
        """
        if self.short_title is None:
            return None

        output_text = convert_lsstdoc_tex(
            self.short_title, 'html5',
            deparagraph=deparagraph,
            mathjax=mathjax,
            smart=smart,
            extra_args=extra_args)
        return output_text

    def format_abstract(self, format='html5', deparagraph=False, mathjax=False,
                        smart=True, extra_args=None):
        """Get the document abstract in the specified markup format.

        Parameters
        ----------
        format : `str`, optional
            Output format (such as ``'html5'`` or ``'plain'``).
        deparagraph : `bool`, optional
            Remove the paragraph tags from single paragraph content.
        mathjax : `bool`, optional
            Allow pandoc to use MathJax math markup.
        smart : `True`, optional
            Allow pandoc to create "smart" unicode punctuation.
        extra_args : `list`, optional
            Additional command line flags to pass to Pandoc. See
            `metasrc.pandoc.convert.convert_text`.

        Returns
        -------
        output_text : `str`
            Converted content or `None` if the title is not available in
            the document.
        """
        if self.abstract is None:
            return None

        output_text = convert_lsstdoc_tex(
            self.abstract, 'html5',
            deparagraph=deparagraph,
            mathjax=mathjax,
            smart=smart,
            extra_args=extra_args)
        return output_text

    def format_authors(self, format='html5', deparagraph=True, mathjax=False,
                       smart=True, extra_args=None):
        """Get the document authors in the specified markup format.

        Parameters
        ----------
        format : `str`, optional
            Output format (such as ``'html5'`` or ``'plain'``).
        deparagraph : `bool`, optional
            Remove the paragraph tags from single paragraph content.
        mathjax : `bool`, optional
            Allow pandoc to use MathJax math markup.
        smart : `True`, optional
            Allow pandoc to create "smart" unicode punctuation.
        extra_args : `list`, optional
            Additional command line flags to pass to Pandoc. See
            `metasrc.pandoc.convert.convert_text`.

        Returns
        -------
        output_text : `list` of `str`
            Sequence of author names in the specified output markup format.
        """
        formatted_authors = []
        for latex_author in self.authors:
            formatted_author = convert_lsstdoc_tex(
                latex_author, 'html5',
                deparagraph=deparagraph,
                mathjax=mathjax,
                smart=smart,
                extra_args=extra_args)
            formatted_authors.append(formatted_author)
        return formatted_authors

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
