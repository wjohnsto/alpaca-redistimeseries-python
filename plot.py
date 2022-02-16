import datetime
import os
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from redistimeseries.client import Client as RedisTimeSeries

redis = RedisTimeSeries(host=os.getenv('REDIS_HOST'))


def query(key, begin_time, end_time):
    try:
        results = redis.mrange(begin_time*1000, end_time*1000, filters=[f'symbol={key}'], bucket_size_msec=1000, aggregation_type='max')
        bids = []
        asks = []
        if (f'{key}:bid' in results[0]):
            bids += results[0][f'{key}:bid'][1]
            asks += results[1][f'{key}:ask'][1]
        else:
            bids += results[1][f'{key}:bid'][1]
            asks += results[0][f'{key}:ask'][1]
        return bids, asks
    except Exception as e:
        print("\n Error: %s" % e)
    print('')


now = int(time.time())
bids, asks = query('MSFT', now - 3600, now)
times = [datetime.datetime.fromtimestamp(
    record[0] / 1000).strftime('%Y-%m-%d %H:%M:%S') for record in bids]
bid_values = [round(float(record[1]), 2) for record in bids]
ask_values = [round(float(record[1]), 2) for record in asks]

df = pd.DataFrame({'timestamp': times, 'bid': bid_values, 'ask': ask_values})
print(df)
df.plot.line(x='timestamp', y=['ask'])
plt.show()
df.plot(x="timestamp", y=["ask"])
