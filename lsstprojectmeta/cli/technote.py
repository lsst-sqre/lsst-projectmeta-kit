"""Command line interface for lsstprojectmeta-ingest-technote.
"""
import argparse
import asyncio
import pprint

import aiohttp
from motor.motor_asyncio import AsyncIOMotorClient

from ..technotes import (get_ltd_product_urls, process_technote,
                         process_technote_products)


def main():
    """Command line entrypoint to reduce technote metadata.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--github-url',
        help='GitHub URL of a technote (optional). If not provided then all '
             'technotes are processed.')
    parser.add_argument(
        '--github-token',
        help='GitHub person access token.')
    parser.add_argument(
        '--mongodb-uri',
        help='MongoDB connection URI')
    parser.add_argument(
        '--mongodb-db',
        default='lsstprojectmeta',
        help='Name of MongoDB database')
    parser.add_argument(
        '--mongodb-collection',
        default='resources',
        help='Name of the MongoDB collection for projectmeta resources')
    args = parser.parse_args()

    if args.mongodb_uri is not None:
        mongo_client = AsyncIOMotorClient(args.mongodb_uri, ssl=True)
        collection = mongo_client[args.mongodb_db][args.mongodb_collection]
    else:
        collection = None

    loop = asyncio.get_event_loop()

    if args.github_url is not None:
        # Run single technote
        loop.run_until_complete(_run_single_technote(args.github_url,
                                                     args.github_token,
                                                     collection))
    else:
        # Run bulk technote processing
        loop.run_until_complete(_run_bulk_etl(args.github_token,
                                              collection))


async def _run_bulk_etl(github_api_token, mongo_collection):
    async with aiohttp.ClientSession() as session:
        product_urls = await get_ltd_product_urls(session)
        print(product_urls)
        await process_technote_products(session, product_urls,
                                        github_api_token,
                                        mongo_collection=mongo_collection)


async def _run_single_technote(github_url, github_api_token, mongo_collection):
    pp = pprint.PrettyPrinter(indent=2)
    async with aiohttp.ClientSession() as session:
        jsonld = await process_technote(session, github_api_token,
                                        github_url=github_url,
                                        mongo_collection=mongo_collection)
    pp.pprint(jsonld)
