"""
Documentation of CoingeckoAPI python wrapper can be found in: https://pypi.org/project/pycoingecko/
The actual documentation of CoinGecko API can be found in: https://www.coingecko.com/en/api/documentation
"""
import json
import os
from datetime import datetime
from pycoingecko import CoinGeckoAPI

# print(finnhub_client.company_profile(symbol='AAPL'))


def convert_time(date_list):
    """
    Returns a list of RFC 1123 time strings from a list of unix timestamp
    :param date_list: a list of unix times
    :return: a python dataframe from this unix time
    """
    for row in date_list:
        row[0] = datetime.utcfromtimestamp(row[0] / 1000).strftime(
            "%a, %d %b %Y %H:%M:%S GMT"
        )
    return date_list


supported_currencies = [
    "aed",
    "ars",
    "aud",
    "bch",
    "bdt",
    "bhd",
    "bits",
    "bmd",
    "bnb",
    "brl",
    "btc",
    "cad",
    "chf",
    "clp",
    "cny",
    "czk",
    "dkk",
    "dot",
    "eos",
    "eth",
    "eur",
    "gbp",
    "hkd",
    "huf",
    "idr",
    "ils",
    "inr",
    "jpy",
    "krw",
    "kwd",
    "link",
    "lkr",
    "ltc",
    "mmk",
    "mxn",
    "myr",
    "ngn",
    "nok",
    "nzd",
    "php",
    "pkr",
    "pln",
    "rub",
    "sar",
    "sats",
    "sek",
    "sgd",
    "thb",
    "try",
    "twd",
    "uah",
    "usd",
    "vef",
    "vnd",
    "xag",
    "xau",
    "xdr",
    "xlm",
    "xrp",
    "yfi",
    "zar",
]


def get_historic_prices(coin, days, currency="usd"):
    """
    :param coin: The id of the coin as defined in the coingecko json file and API
    :param days: How many days of data to return
    :return: a list of prices
    """
    currency = currency.lower()
    if currency not in supported_currencies:
        return None
    cg_api = CoinGeckoAPI()
    coin = coin.lower()
    prices = cg_api.get_coin_market_chart_by_id(
        id=coin, vs_currency=currency, days=days
    )["prices"]
    return convert_time(prices)


def get_historic_volumes(coin, days):
    """
    :param coin: The id of the coin as defined in the coingecko json file and API
    :param days: How many days of data to return
    :returns a list of volumes
    """
    cg_api = CoinGeckoAPI()
    coin = coin.lower()
    volumes = cg_api.get_coin_market_chart_by_id(id=coin, vs_currency="usd", days=days)[
        "total_volumes"
    ]
    return convert_time(volumes)


def print_historic_price(dict_of_prices):
    """
    prints the provided dictionary
    :param dict_of_prices: A dictionary of the time and price
    """
    for prices in dict_of_prices:
        print(prices)


def get_market_cap_history(coin: str, days: int = 3):
    """
    :param coin: The id of the coin as defined in the coingecko json file and API
    :param days: How many days of data to return
    :return: a dictionary of the coins market cap and time of capture
    """
    cg_api = CoinGeckoAPI()
    coin = coin.lower()
    market_cap = cg_api.get_coin_market_chart_by_id(
        id=coin, vs_currency="usd", days=days
    )["market_caps"]
    return convert_time(market_cap)


def get_coin_live_stats(coin):
    """
    :param coin: The id of the coin as defined in the coingecko json file and API
    :return: current live stats of a coin as a dictionary
    """
    cg_api = CoinGeckoAPI()
    coin = coin.lower()

    info = cg_api.get_coin_by_id(coin, localization=False)

    if len(info) == 0:
        return -1

    exchanges = []
    if info["tickers"] != None:
        for market in info["tickers"]:
            if market["market"]["name"] not in exchanges:
                exchanges.append(market["market"]["name"])

    coin_stats = {
        "Name": info["name"],
        "Symbol": info["symbol"],
        "Image": info["image"]["large"],
        "Address": info["platforms"],
        "MarketCapRank": info["market_data"]["market_cap_rank"],
        "DayHigh": info["market_data"]["high_24h"]["USD"]
        if "USD" in info["market_data"]["high_24h"]
        else info["market_data"]["high_24h"]["usd"],
        "DayLow": info["market_data"]["low_24h"]["USD"]
        if "USD" in info["market_data"]["low_24h"]
        else info["market_data"]["low_24h"]["usd"],
        "Price": info["market_data"]["current_price"]["usd"]
        if "usd" in info["market_data"]["current_price"]
        else None,
        "MarketCap": info["market_data"]["market_cap"]["usd"]
        if "usd" in info["market_data"]["market_cap"]
        else None,
        "24HrMarketCapChange": info["market_data"]["market_cap_change_percentage_24h"]
        if info["market_data"]["market_cap_change_percentage_24h"] != None
        else None,
        "24HrPriceChange": info["market_data"]["price_change_percentage_24h"]
        if info["market_data"]["price_change_percentage_24h"] != None
        else None,
        "exchanges": exchanges,
        "homepage": info["links"]["homepage"][0]
        if len(info["links"]["homepage"][0]) > 0
        else None,
    }
    return coin_stats


def convert_symbol_to_id(symbol):
    """
    :param symbol: The ticker of a coin/token
    :return: if this symbl exists, we return the corresponding ID used by coingecko API
    """
    # token_file = open('CoinGeckoCoins.json', encoding="utf8")
    token_file = open("connectors/CoinGeckoCoins.json", encoding="utf8")
    tokens = json.load(token_file)
    for token in tokens:
        if token["symbol"] == symbol:
            return token["id"]


def get_symbol_eth_address(symbol):
    """
    :param symbol: The ticker of a coin/token
    :return: the eth token contract address if it exists, or None of it's not an ETH token
    """
    token_file = open("connectors/CoinGeckoCoins.json", encoding="utf8")
    tokens = json.load(token_file)
    for token in tokens:
        if token["symbol"] == symbol:
            if len(token["platforms"]["ethereum"]) > 0:
                return token["platforms"]["ethereum"]
    return None


def get_id_eth_address(id):
    """
    :param id: The id of a coin/token
    :returns the eth token contract address if it exists, or None of it's not an ETH token
    """
    # token_file = open('CoinGeckoCoins.json', encoding="utf8")
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_path = os.path.join(SITE_ROOT, "CoinGeckoCoins.json")
    tokens = json.loads(open(json_path, encoding="utf8").read())
    for token in tokens:
        if token["id"] == id:
            if (
                "ethereum" in token["platforms"]
                and len(token["platforms"]["ethereum"]) > 0
            ):
                return token["platforms"]["ethereum"]
    return None


def get_coin_links(coin_id):
    """
    :param coin_id: The ID of the coin, as stored in coin gecko coins json file
    :return: a dictionary with the available links for the passed coin
    """
    cg_api = CoinGeckoAPI()
    data = cg_api.get_coin_by_id(
        coin_id, localization=False, market_data=False, community_data=False
    )["links"]

    links = {}
    if len(data["homepage"][0]) > 0:
        links["homepage"] = data["homepage"][0]
    if len(data["twitter_screen_name"]) > 0:
        links["twitter"] = "https://twitter.com/" + data["twitter_screen_name"]

    links["blockchain_links"] = []
    for blockchain_url in data["blockchain_site"]:
        if len(blockchain_url) > 0:
            links["blockchain_links"].append(blockchain_url)
    if len(data["repos_url"]["github"]) > 0:
        links["repos_link"] = data["repos_url"]["github"][0]
    if len(data["telegram_channel_identifier"]) > 0:
        links["telegram_url"] = "https://t.me/" + data["telegram_channel_identifier"]

    return links
