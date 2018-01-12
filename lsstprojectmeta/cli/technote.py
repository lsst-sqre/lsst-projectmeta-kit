"""Command line interface for lsstprojectmeta-ingest-technote.
"""
import argparse
import asyncio
import pprint

import aiohttp

from ..technotes import reduce_technote


def main():
    """Command line entrypoint to reduce technote metadata.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--github-url',
        help='GitHub URL of a technote.')
    parser.add_argument(
        '--github-token',
        help='GitHub person access token.')
    args = parser.parse_args()

    async def _run(github_url, github_api_token):
        pp = pprint.PrettyPrinter(indent=2)
        async with aiohttp.ClientSession() as session:
            jsonld = await reduce_technote(github_url, session,
                                           github_api_token)
        pp.pprint(jsonld)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(_run(args.github_url, args.github_token))
