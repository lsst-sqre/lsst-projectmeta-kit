"""LSST the Docs client.
"""

__all__ = ('get_ltd_product_urls',)


async def get_ltd_product_urls(session):
    """Get URLs for LSST the Docs (LTD) products from the LTD Keeper API.

    Parameters
    ----------
    session : `aiohttp.ClientSession`
        Your application's aiohttp client session.
        See http://aiohttp.readthedocs.io/en/stable/client.html.

    Returns
    -------
    product_urls : `list`
        List of product URLs.
    """
    product_url = 'https://keeper.lsst.codes/products/'
    async with session.get(product_url) as response:
        data = await response.json()

    return data['products']
