# Introduction

This project is a very barebones setup for taking the Alpaca streaming API results for stock quotes and piping the data into RedisTimeSeries. As a start the code simply stores the bid and ask values in Redis, as well as plots them for you using matplotlib.

# Installation

```
$ docker-compose up -d # only if you want to run Redis locally
$ poetry install
```

# Usage

Set the following environment variables:

1. `APCA_API_KEY_ID`: Your Alpaca API Key found on the Alpaca dashboard
1. `APCA_API_SECRET_KEY`: Your Alpaca API Secret found on the Alpaca dashboard
1. `REDIS_HOST`: Defaults to `localhost`, set to something else if you're running Redis on a different machine.

Run the following command:

```
$ poetry run python stream.py
```

Check with RedisInsight to see that `MSFT:bids` and `MSFT:asks` exist in your Redis database. Then, wait for some time before running the following command:

```
$ poetry run python plot.py
```
