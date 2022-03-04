import os

import aioredis
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv('REDIS_URL')
PAST_KEY = os.getenv('PAST_KEY')
MAIN_URL = os.getenv('MAIN_URL')


async def open_pool():
    try:
        return await aioredis.from_url(REDIS_URL, encoding='utf-8',
                                       decode_responses=True)
    except ConnectionError:
        # some action for DevOps
        pass
