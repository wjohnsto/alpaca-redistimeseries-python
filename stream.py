import os
from alpaca_trade_api.stream import Stream, Quote
from alpaca_trade_api.common import URL
from redistimeseries.client import Client as RedisTimeSeries

redis = RedisTimeSeries(host=os.getenv('REDIS_HOST'))


def get_keys(symbol: str):
    bid_key = f'{symbol}:bid'
    ask_key = f'{symbol}:ask'
    return bid_key, ask_key


async def create_ts(symbol: str):
    bid_key, ask_key = get_keys(symbol)

    try:
        await redis.create(bid_key, retention_msecs=1800000, duplicate_policy='last', labels={'symbol': symbol})
    except Exception as e:
        pass

    try:
        await redis.create(ask_key, retention_msecs=1800000, duplicate_policy='last', labels={'symbol': symbol})
    except Exception as e:
        pass


async def quote_callback(q: Quote):
    """
        Sample quote object:
        {
            'ask_exchange': 'V',
            'ask_price': 293.99,
            'ask_size': 1,
            'bid_exchange': 'V',
            'bid_price': 293.95,
            'bid_size': 1,
            'conditions': ['R'],
            'symbol': 'MSFT',
            'tape': 'C',
            'timestamp': 1644868628563261552
        }
    """
    bid_key, ask_key = get_keys(q.symbol)
    await create_ts(q.symbol)
    redis.madd([
        (bid_key, str(int(q.timestamp.timestamp() * 1000)), q.bid_price),
        (ask_key, str(int(q.timestamp.timestamp() * 1000)), q.ask_price)
    ])


# Initiate Class Instance
stream = Stream(base_url=URL('https://paper-api.alpaca.markets'),
                data_feed='iex')  # <- replace to SIP if you have PRO subscription

# subscribing to event
stream.subscribe_quotes(quote_callback, 'MSFT')

stream.run()
