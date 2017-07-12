##########
Change Log
##########

[0.1.3] - (2017-07-12)
======================

- Add new ``metasrc.tex.texnormalizer.read_tex_file`` function that reads a tex file and inserts reference files into the source.
  Works with ``\input`` and ``\include`` commands.
- New support for macro resolution in TeX source.
  The ``metasrc.tex.scraper.get_macros`` to scrape TeX macro definitions from ``\def`` and ``\newcommand`` commands.
  The ``metasrc.tex.texnormalizer.replace_macros`` function takes the output from ``get_macros`` and replaces macros in TeX source with the macro content.
  Only static macros (those without arguments) are supported by these functions.
- Add ``LsstDoc.is_draft`` property.
  This property is ``True`` if the ``lsstdraft`` option is in the ``documentclass`` declaration.

[0.1.2] - (2017-06-17)
======================

- Add new ``metasrc.tex.texnormalizer`` module with ``remove_comments()` and ``remove_trailing_whitespace()`` functions.
  Projects can use these functions in a pipeline to clean TeX source to make subsequent parsing tasks easier.
  (`DM-10961 <https://jira.lsstcorp.org/browse/DM-10961>`)

[0.1.1] - (2017-06-13)
======================

- Make regular expressions for parsing lsstdoc TeX documents more flexible with respect to internal whitespace (`DM-10920 <https://jira.lsstcorp.org/browse/DM-10920>`_).

[0.1.0] - (2017-05-24)
======================

- Initial version.
- ``metasrc.github.auth`` module support GitHub authentication using their integrations API.
- ``metasrc.tex.lsstdoc`` supports data scraping from LSST LaTeX documents based on the ``lsstdoc`` class from `lsst-texmf`_.

.. _lsst-texmf: https://lsst-texmf.lsst.io
