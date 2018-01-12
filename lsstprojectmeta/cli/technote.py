"""Command line interface for lsstprojectmeta-ingest-technote.
"""
import argparse
import asyncio
import pprint

import aiohttp
from motor.motor_asyncio import AsyncIOMotorClient

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

    async def _run(github_url, github_api_token, mongo_collection):
        pp = pprint.PrettyPrinter(indent=2)
        async with aiohttp.ClientSession() as session:
            jsonld = await reduce_technote(github_url, session,
                                           github_api_token,
                                           mongo_collection=mongo_collection)
        pp.pprint(jsonld)

    if args.mongodb_uri is not None:
        mongo_client = AsyncIOMotorClient(args.mongodb_uri)
        collection = mongo_client[args.mongodb_db][args.mongodb_collection]
    else:
        collection = None

    loop = asyncio.get_event_loop()
    loop.run_until_complete(_run(args.github_url, args.github_token,
                                 collection))
