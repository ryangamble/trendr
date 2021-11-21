"""
This file is for creating functions to call /assets endpoints
"""


def fear_greed(client):
    return client.get("/assets/fear-greed")


def perform_asset_search(client):
    return client.get("/assets/perform_asset_search")


def search(client, params):
    return client.get("/assets/search", params=params)


def historic_fear_greed(client, params):
    return client.get("/assets/historic-fear-greed", params=params)


def stocks_listed_exchanges(client, params):
    return client.get("/assets/stocks/listed-exchanges", params=params)


def crypto_stats(client, params):
    return client.get("/assets/crypto/stats", params=params)


def stock_stats(client, params):
    return client.get("/assets/stock/stats", params=params)


def crypto_eth_address(client, params):
    return client.get("/assets/crypto/eth-address", params=params)


def token_info(client, params):
    return client.get("/assets/token/info", params=params)


def token_top_holders(client, params):
    return client.get("/assets/token/top-holders", params=params)


def crypto_price_history(client, params):
    return client.get("/assets/crypto/price-history", params=params)


def crypto_volume_history(client, params):
    return client.get("/assets/crypto/volume-history", params=params)


def stock_history(client, params):
    return client.get("/assets/stock/history", params=params)


def twitter_sentiment(client, params):
    return client.get("/assets/twitter_sentiment", params=params)


def reddit_sentiment(client, params):
    return client.get("/assets/reddit_sentiment", params=params)


def tweet_summary(client, asset_identifier):
    return client.get(f"/assets/tweet-summary/{asset_identifier}")
