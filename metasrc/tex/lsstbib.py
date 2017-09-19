"""APIs for getting and working with the BibTeX databases in lsst-texmf.
"""

__all__ = ['get_lsst_bibtex']

import asyncio
import logging

from aiohttp import ClientSession

# https://lsst-texmf.lsst.io/lsstdoc.html#bibliographies
KNOWN_LSSTTEXMF_BIB_NAMES = ('lsst', 'lsst-dm', 'refs', 'books', 'refs_ads')


# Cache of bibtex file content, keyed by name (see KNOWN_LSSTTEXMF_BIB_NAMES).
_LSSTTEXMF_BIB_CACHE = {}


async def _download_text(url, session):
    """Asynchronously request a URL and get the encoded text content of the
    body.

    Parameters
    ----------
    url : `str`
        URL to download.
    session : `aiohttp.ClientSession`
        An open aiohttp session.

    Returns
    -------
    content : `str`
        Content downloaded from the URL.
    """
    logger = logging.getLogger(__name__)
    async with session.get(url) as response:
        # aiohttp decodes the content to a Python string
        logger.info('Downloading %r', url)
        return await response.text()


async def _download_lsst_bibtex(bibtex_names):
    """Asynchronously download a set of lsst-texmf BibTeX bibliographies from
    GitHub.

    Parameters
    ----------
    bibtex_names : sequence of `str`
        Names of lsst-texmf BibTeX files to download. For example:

        .. code-block:: python

           ['lsst', 'lsst-dm', 'refs', 'books', 'refs_ads']

    Returns
    -------
    bibtexs : `list` of `str`
        List of BibTeX file content, in the same order as ``bibtex_names``.
    """
    blob_url_template = (
        'https://raw.githubusercontent.com/lsst/lsst-texmf/master/texmf/'
        'bibtex/bib/{name}.bib'
    )
    urls = [blob_url_template.format(name=name) for name in bibtex_names]

    tasks = []
    async with ClientSession() as session:
        for url in urls:
            task = asyncio.ensure_future(_download_text(url, session))
            tasks.append(task)

        return await asyncio.gather(*tasks)


def get_lsst_bibtex(bibtex_filenames=None):
    """Get content of lsst-texmf bibliographies.

    BibTeX content is downloaded from GitHub (``master`` branch of
    https://github.com/lsst/lsst-texmf or retrieved from an in-memory cache.

    Parameters
    ----------
    bibtex_filenames : sequence of `str`, optional
        List of lsst-texmf BibTeX files to retrieve. These can be the filenames
        of lsst-bibtex files (for example, ``['lsst.bib', 'lsst-dm.bib']``)
        or names without an extension (``['lsst', 'lsst-dm']``). The default
        (recommended) is to get *all* lsst-texmf bibliographies:

        .. code-block:: python

           ['lsst', 'lsst-dm', 'refs', 'books', 'refs_ads']

    Returns
    -------
    bibtex : `dict`
        Dictionary with keys that are bibtex file names (such as ``'lsst'``,
        ``'lsst-dm'``). Values are the corresponding bibtex file content
        (`str`).
    """
    logger = logging.getLogger(__name__)

    if bibtex_filenames is None:
        # Default lsst-texmf bibliography files
        bibtex_names = KNOWN_LSSTTEXMF_BIB_NAMES
    else:
        # Sanitize filenames (remove extensions, path)
        bibtex_names = []
        for filename in bibtex_filenames:
            name = os.path.basename(os.path.splitext(filename)[0])
            if name not in KNOWN_LSSTTEXMF_BIB_NAMES:
                logger.warning('%r is not a known lsst-texmf bib file',
                               name)
                continue
            bibtex_names.append(name)

    # names of bibtex files not in cache
    uncached_names = [name for name in bibtex_names
                      if name not in _LSSTTEXMF_BIB_CACHE]
    if len(uncached_names) > 0:
        # Download bibtex and put into the cache
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(_download_lsst_bibtex(uncached_names))
        loop.run_until_complete(future)
        for name, text in zip(bibtex_names, future.result()):
            _LSSTTEXMF_BIB_CACHE[name] = text

    return {name: _LSSTTEXMF_BIB_CACHE[name] for name in bibtex_names}
