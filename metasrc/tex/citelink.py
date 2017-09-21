__all__ = ['CitationLinker']

from .commandparser import LatexCommand

from .lsstbib import (
    get_url_from_entry, NoEntryUrlError, get_authoryear_from_entry,
    AuthorYearError)


class CitationLinker(object):
    """LaTeX source processor that converts citation commands to ``\href``
    commands.

    This processing is useful for decoupling BibTeX from extracted TeX source
    snippets, like abstracts, that are intended to be converted into another
    markup language by pandoc.

    Parameters
    ----------
    bibtex_database : `pybtex.database.BibliographyData`
        A pybtex bibliography. Use `metasrc.lsstbib.get_bibliography` to get
        this.
    """

    def __init__(self, bibtex_database):
        super().__init__()
        self._db = bibtex_database

        # Register and build Linker classes. They all share the same API.
        self._linker_classes = [CitedsLinker, CitedspLinker]
        self._linkers = [cls(self._db) for cls in self._linker_classes]

    def __call__(self, tex_source):
        """Convert citations in LaTeX source to Hyperref links.

        Parameters
        ----------
        tex_source : `str`
            LaTeX document source.

        Returns
        -------
        processed_tex : `str`
            LaTeX document source with all citation commands converted to
            ``\hyperref`` commands.
        """
        for linker in self._linkers:
            tex_source = linker(tex_source)
        return tex_source


class BaseCommandLinker(object):
    """Baseclass for citation linkers that process specific types of
    LaTeX commands.
    """

    def __call__(self, tex_source):
        """Convert commands of type ``command`` in LaTeX source to Hyperref
        links.

        Parameters
        ----------
        tex_source : `str`
            LaTeX document source.

        Returns
        -------
        processed_tex : `str`
            LaTeX document source with commands of type ``command`` to
            ``\hyperref`` commands.
        """
        while True:
            try:
                parsed = next(self.command.parse(tex_source))
            except StopIteration:
                break
            tex_source = self._replace_command(tex_source, parsed)
        return tex_source


class CitedsLinker(BaseCommandLinker):
    """Replace a ``\citeds`` citation with ``\href`` command.

    Examples
    --------
    >>> replace_citeds = CitedsLinker()
    >>> print(replace_citeds('\citeds{LDM-151}'))
    \href{https://ls.st/LDM-151}{LDM-151}

    Variant with defined title text:

    >>> print(replace_citeds('\citeds[Pipelines Design]{LDM-151}'))
    \href{https://ls.st/LDM-151}{Pipelines Design}
    """

    def __init__(self, bibtex_database=None):
        super().__init__()
        self._db = bibtex_database
        self.command = LatexCommand(
            'citeds',
            {'bracket': '[', 'required': False, 'name': 'title'},
            {'bracket': '{', 'required': True, 'name': 'citekey'}
        )
        self.template = '\\href{{{url}}}{{{content}}}'

    def _replace_command(self, tex_source, parsed):
        if 'title' in parsed:
            content = parsed['title']
        else:
            # The document handle
            # Could get this from BibTeX
            content = parsed['citekey']

        url = 'https://ls.st/{citekey}'.format(citekey=parsed['citekey'])

        href_command = self.template.format(url=url, content=content)
        tex_source = tex_source.replace(
            parsed.command_source,
            href_command)

        return tex_source


class CitedspLinker(BaseCommandLinker):
    """Replace a ``\citedsp`` citation with ``\href`` command.

    Examples
    --------
    >>> replace_citedsp = CitedspLinker()
    >>> print(replace_citedsp('\citedsp{LDM-151}'))
    [\href{https://ls.st/LDM-151}{LDM-151}]

    Variant with defined title text:

    >>> print(replace_citedsp('\citedsp[Pipelines Design]{LDM-151}'))
    [\href{https://ls.st/LDM-151}{Pipelines Design}]
    """

    def __init__(self, bibtex_database=None):
        super().__init__()
        self._db = bibtex_database
        self.command = LatexCommand(
            'citedsp',
            {'bracket': '[', 'required': False, 'name': 'title'},
            {'bracket': '{', 'required': True, 'name': 'citekey'}
        )
        self.template = '[\\href{{{url}}}{{{content}}}]'

    def _replace_command(self, tex_source, parsed):
        if 'title' in parsed:
            content = parsed['title']
        else:
            # The document handle
            # Could get this from BibTeX
            content = parsed['citekey']

        url = 'https://ls.st/{citekey}'.format(citekey=parsed['citekey'])

        href_command = self.template.format(url=url, content=content)
        tex_source = tex_source.replace(
            parsed.command_source,
            href_command)

        return tex_source


class CitepLinker(BaseCommandLinker):
    """Replace a ``\citep`` citation with an ``\href`` command.
    """

    def __init__(self, bibtex_database=None):
        super().__init__()
        self._db = bibtex_database
        self.command = LatexCommand(
            'citep',
            {'bracket': '[', 'required': False, 'name': 'prefix'},
            {'bracket': '[', 'required': False, 'name': 'suffix'},
            {'bracket': '{', 'required': True, 'name': 'citekeys'}
        )
        self.outer_template = "[{content}]"
        self.link_template = "\\href{{{url}}}{{{content}}}"

    def _replace_command(self, tex_source, parsed):
        cite_keys = [k.strip() for k in parsed['citekeys'].split(',')]

        hrefs = []
        for cite_key in cite_keys:
            if self._db and cite_key in self._db.entries:
                entry = self._db.entries[cite_key]
                try:
                    url = get_url_from_entry(entry)
                except NoEntryUrlError:
                    url = None

                try:
                    authoryear = get_authoryear_from_entry(entry, paren=False)
                except AuthorYearError:
                    authoryear = None

                if url is not None and authoryear is not None:
                    hrefs.append(self.link_template.format(url=url,
                                                           content=authoryear))
                elif url is None and authoryear is not None:
                    # No link in this case
                    hrefs.append(authoryear)
                elif url is not None and authoryear is None:
                    # Link with cite key
                    hrefs.append(self.link_template.format(url=url,
                                                           content=cite_key))
                else:
                    # Just show cite key
                    hrefs.append(cite_key)

        replacement = self.outer_template.format(content=', '.join(hrefs))
        tex_source = tex_source.replace(
            parsed.command_source,
            replacement)

        return tex_source
