##########
Change Log
##########

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
