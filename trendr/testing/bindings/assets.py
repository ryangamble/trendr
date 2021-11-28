"""
This file is for creating functions to call /assets endpoints
"""


def fear_greed(client):
    return client.get("/assets/fear-greed")


def perform_asset_search(client):
    return client.get("/assets/perform-asset-search")


def search(client, params):
    param_string = "?"
    for key, value in params.items():
        param_string += f"{key}={value}&"
    param_string = param_string[:-1]
    return client.get(f"/assets/search{param_string}")


def historic_fear_greed(client, params):
    param_string = "?"
    for key, value in params.items():
        param_string += f"{key}={value}&"
    param_string = param_string[:-1]
    return client.get(f"/assets/historic-fear-greed{param_string}")


def stocks_listed_exchanges(client, params):
    param_string = "?"
    for key, value in params.items():
        param_string += f"{key}={value}&"
    param_string = param_string[:-1]
    return client.get(f"/assets/stocks/listed-exchanges{param_string}")


def crypto_stats(client, params):
    param_string = "?"
    for key, value in params.items():
        param_string += f"{key}={value}&"
    param_string = param_string[:-1]
    return client.get(f"/assets/crypto/stats{param_string}")


def stock_stats(client, params):
    param_string = "?"
    for key, value in params.items():
        param_string += f"{key}={value}&"
    param_string = param_string[:-1]
    return client.get(f"/assets/stock/stats{param_string}")


def crypto_eth_address(client, params):
    param_string = "?"
    for key, value in params.items():
        param_string += f"{key}={value}&"
    param_string = param_string[:-1]
    return client.get(f"/assets/crypto/eth-address{param_string}")


def token_info(client, params):
    param_string = "?"
    for key, value in params.items():
        param_string += f"{key}={value}&"
    param_string = param_string[:-1]
    return client.get(f"/assets/token/info{param_string}")


def token_top_holders(client, params):
    param_string = "?"
    for key, value in params.items():
        param_string += f"{key}={value}&"
    param_string = param_string[:-1]
    return client.get(f"/assets/token/top-holders{param_string}")


def crypto_price_history(client, params):
    param_string = "?"
    for key, value in params.items():
        param_string += f"{key}={value}&"
    param_string = param_string[:-1]
    return client.get(f"/assets/crypto/price-history{param_string}")


def crypto_volume_history(client, params):
    param_string = "?"
    for key, value in params.items():
        param_string += f"{key}={value}&"
    param_string = param_string[:-1]
    return client.get(f"/assets/crypto/volume-history{param_string}")


def stock_history(client, params):
    param_string = "?"
    for key, value in params.items():
        param_string += f"{key}={value}&"
    param_string = param_string[:-1]
    return client.get(f"/assets/stock/history{param_string}")


def twitter_sentiment(client, params):
    param_string = "?"
    for key, value in params.items():
        param_string += f"{key}={value}&"
    param_string = param_string[:-1]
    return client.get(f"/assets/twitter-sentiment{param_string}")


def reddit_sentiment(client, params):
    param_string = "?"
    for key, value in params.items():
        param_string += f"{key}={value}&"
    param_string = param_string[:-1]
    return client.get(f"/assets/reddit-sentiment{param_string}")


def tweet_summary(client, asset_identifier):
    return client.get(f"/assets/tweet-summary/{asset_identifier}")
