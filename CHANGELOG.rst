##########
Change Log
##########

0.2.0 (2017-09-21)
==================

The 0.2.0 release brings Pandoc integration for better conversions from LaTeX to HTML and plain text.

Changes
-------

- Renamed ``metasrc.tex.texnormalizer`` to ``metasrc.tex.normalizer``.
- We now assign a ``NullHandler`` to metasrc's root logger.
  This makes it easier for you to add your own handlers and control metasrc's logging.

New
---

- New dependencies on ``pypandoc>=1.4``, ``panflute==1.10.6``, ``aiohttp>=2.25``, and ``pybtex>=0.21``.

- New ``metasrc.pandoc`` namespace for working with Pandoc:

  - ``metasrc.pandoc.convert.convert_text()`` and ``convert_lsstdoc_tex()`` wraps pypandoc's ``convert_text()`` function and provides extra conveniences, like running with the ``metasrc-deparagraph`` filter and ensuring that pandoc is installed.
  - ``metasrc.pandoc.convert.ensure_pandoc()`` is a decorator that ensures Pandoc is installed before running the wrapped function.
    If necessary, it uses pypandoc to install Pandoc.
  - The ``metasrc-deparagraph`` CL program is a Pandoc filter, made with panflute, that removes the paragraph tags around a single paragraph of text.
    This is useful when extracting single paragraphs or sentences (such as titles or authors).

- New functionality in ``metasrc.tex.lsstdoc.LsstDoc`` that improves the quality of LaTeX to HTML5 conversions:

  - ``LsstDoc`` now lazily parses an lsstdoc LaTeX document.
    Content is extracted or processed when attributes are accessed.
  - ``LsstDoc.read()`` class method for reading LaTeX source, normalizing it, and creating an ``LsstDoc`` instance.
  - New ``html_*`` and ``plain_*`` attributes with content converted to the given format.
    For example, ``html_abstract`` is the abstract converted to HTML5 with Pandoc.
    The regular attributes, ``title``, ``abstract``, and ``authors`` provide the original LaTeX.
  - The ``LsstDoc.bib_db`` attributes provides a ``pybtex.database.BibliographyData`` instance with all BibTeX bibliography referenced by the document.
  - The ``html_abstract`` and ``plain_abstract`` attributes pre-process the LaTeX snippet before converting with Pandoc.
    The only pre-processing step implemented so far is the citation linker, which replaces ``\cite*`` commands with hyperlinks (``\href``).
    This decouples the LaTeX snippet from the BibTeX database.

- New ``metasrc.tex.lsstbib`` module:
  
  - The ``get_bibliography()`` function Lets you get a ``pybtex.database.BibliographyData`` instance that includes BibTeX from both local BibTeX files and the common lsst-texmf BibTeX files.
    ``aiohttp`` (``asyncio``) lets us download lsst-texmf BibTeX files quickly from the ``master`` branch on GitHub.
  - ``get_url_from_entry()`` makes it easier to get a URL to the entity described by a pybtex Entry.
    Works with DocuShare handles, ``adsurl``, DOIs, and plain ``url`` fields.
  - ``get_authoryear_from_entry()`` creates natbib-like in-text citations from a pybtex Entry.
    For example, "Sick et al (2017)."

- New ``metasrc.tex.citelink`` module.
  The ``CitationLinker`` class processes LaTeX source and replaces citation commands with hyperlinks to decouple a LaTeX snippet from a BibTeX database.
  This is useful for Pandoc conversions to HTML.
  These commands are currently converted:

  - ``\citeds``
  - ``\citedsp``
  - ``\citep``

0.1.4 (2017-09-07)
==================

- Add new ``metasrc.tex.commandparser.LatexCommand`` to extract argument content for LaTeX commands using stream parsing and bracket matching.
  This is an improvement on the regular expression matching used by ``LsstDoc`` that was brittle to multi-line commands. (`DM-11821 <https://jira.lsstcorp.org/browse/DM-11821>`_)
- Port ``metasrc.tex.lsstdoc.LsstDoc`` to use ``LatexCommand`` (no external API changes).
- Port ``metasrc.tex.scraper.get_newcommand_macros`` to use ``LatexCommand`` (no external API changes).

0.1.3 (2017-07-12)
==================

- Add new ``metasrc.tex.texnormalizer.read_tex_file`` function that reads a tex file and inserts reference files into the source.
  Works with ``\input`` and ``\include`` commands.
- New support for macro resolution in TeX source.
  The ``metasrc.tex.scraper.get_macros`` to scrape TeX macro definitions from ``\def`` and ``\newcommand`` commands.
  The ``metasrc.tex.texnormalizer.replace_macros`` function takes the output from ``get_macros`` and replaces macros in TeX source with the macro content.
  Only static macros (those without arguments) are supported by these functions.
- Add ``LsstDoc.is_draft`` property.
  This property is ``True`` if the ``lsstdraft`` option is in the ``documentclass`` declaration.

0.1.2 (2017-06-17)
==================

- Add new ``metasrc.tex.texnormalizer`` module with ``remove_comments()` and ``remove_trailing_whitespace()`` functions.
  Projects can use these functions in a pipeline to clean TeX source to make subsequent parsing tasks easier.
  (`DM-10961 <https://jira.lsstcorp.org/browse/DM-10961>`)

0.1.1 (2017-06-13)
==================

- Make regular expressions for parsing lsstdoc TeX documents more flexible with respect to internal whitespace (`DM-10920 <https://jira.lsstcorp.org/browse/DM-10920>`_).

0.1.0 (2017-05-24)
==================

- Initial version.
- ``metasrc.github.auth`` module support GitHub authentication using their integrations API.
- ``metasrc.tex.lsstdoc`` supports data scraping from LSST LaTeX documents based on the ``lsstdoc`` class from `lsst-texmf`_.

.. _lsst-texmf: https://lsst-texmf.lsst.io
