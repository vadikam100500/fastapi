import datetime as dt
import json
import os
from typing import Optional

import aioredis
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv('REDIS_URL')
PAST_KEY = os.getenv('PAST_KEY')


async def open_pool():
    try:
        return await aioredis.from_url(REDIS_URL, encoding='utf-8',
                                       decode_responses=True)
    except ConnectionError:
        # some action for DevOps
        pass


def get_date(date: Optional[str] = None):
    return date if date else str(dt.datetime.now())


async def add_to_send(pool, client_id, message, date=None):
    """
    Write to db messages to send like: {user_id} as hash {date: message}.

    I know you are cool, but don't think that it will be several messages
    for 1 milisecond.
    I can make it like {some_hash} - {user_id: str({date: message})}
    if u want.
    """
    date = get_date(date)
    await pool.hset(client_id, date, message)


def check_for_actual(data: dict, new_date: str):
    """Delete old messages from data, because we can't set TTL."""
    new_date = dt.datetime.strptime(new_date, '%Y-%m-%d %H:%M:%S.%f')
    not_fresh = []
    # i wouldn't make asyncio tasks here, because it's not by tor,
    # if all ok, i remake it
    for date in data.keys():
        if (new_date
            - dt.datetime.strptime(date,
                                   '%Y-%m-%d %H:%M:%S.%f')).days > 30:
            not_fresh.append(date)
        else:
            break
    for date in not_fresh:
        data.pop(date)
    return data


async def add_to_sended(pool, client_id, message, date=None):
    """
    Write to db sended messages like:
    {past_key} as hash {user_id: str({date: message})}.

    Date is a bad key, but i think user couldn't make anything
    for 1 milisecond, even with bot.
    """
    date = get_date(date)
    new_data = {date: message}
    if data := await pool.hget(PAST_KEY, client_id):
        old_data = json.loads(data)
        # we can set ttl only for whole user =(
        data = check_for_actual(old_data, date)
        data.update(new_data)
    else:
        data = new_data
    await pool.hset(PAST_KEY, client_id, json.dumps(data))
