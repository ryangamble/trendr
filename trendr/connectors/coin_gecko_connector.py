"""
Documentation of CoingeckoAPI python wrapper can be found in: https://pypi.org/project/pycoingecko/
The actual documentation of CoinGecko API can be found in: https://www.coingecko.com/en/api/documentation
"""
import json
from datetime import datetime
from pycoingecko import CoinGeckoAPI


def convert_time(date_list):
    """
    :param date_list: a list of unix times
    :returns a python dataframe from this unix time
    """
    for row in date_list:
        row[0] = datetime.utcfromtimestamp(row[0]/1000)
    return date_list


def get_historic_prices(coin, days):
    """
    :param coin: The id of the coin as defined in the coingecko json file and API
    :param days: How many days of data to return
    :returns a list of prices
    """
    cg_api = CoinGeckoAPI()
    coin = coin.lower()
    prices = cg_api.get_coin_market_chart_by_id(id=coin, vs_currency='usd', days=days)['prices']
    return convert_time(prices)

def get_historic_volumes(coin, days):
    """
    :param coin: The id of the coin as defined in the coingecko json file and API
    :param days: How many days of data to return
    :returns a list of volumes
    """
    cg_api = CoinGeckoAPI()
    coin = coin.lower()
    volumes = cg_api.get_coin_market_chart_by_id(id=coin, vs_currency='usd', days=days)['total_volumes']
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
    :returns a dictionary of the coins market cap and time of capture
    """
    cg_api = CoinGeckoAPI()
    coin = coin.lower()
    market_cap = cg_api.get_coin_market_chart_by_id(id=coin, vs_currency='usd', days=days)['market_caps']
    return convert_time(market_cap)


def get_coin_live_stats(coin):
    """
    :param coin: The id of the coin as defined in the coingecko json file and API
    :returns current live stats of a coin as a dictionary
    """
    cg_api = CoinGeckoAPI()
    coin = coin.lower()
    stats = cg_api.get_price(ids=coin, vs_currencies='usd', include_market_cap='true', include_24hr_vol='true',
                             include_24hr_change='true', include_last_updated_at='true')
    
    info = cg_api.get_coin_by_id(coin)

    if len(stats) == 0 or len(info) == 0:
        return -1

    coin_stats = {
        'Name': info['name'],
        'Symbol': info['symbol'],
        'Image': info['image']['large'],
        'Address': info['platforms'],
        'MarketCapRank': info['market_data']['market_cap_rank'],
        'DayHigh': info['market_data']['high_24h']['usd'],
        'DayLow': info['market_data']['low_24h']['usd'],
        'Price': stats[coin]['usd'],
        'MarketCap': '${0:,.2f}'.format(stats[coin]['usd_market_cap']),
        '24HrVolume': '${0:,.2f}'.format(stats[coin]['usd_24h_vol']),
        '24HrChange': "%{:.2f}".format(stats[coin]['usd_24h_change'])
    }
    return coin_stats


def convert_symbol_to_id(symbol):
    """
    :param symbol: The ticker of a coin/token
    :returns if this symbl exists, we return the corresponding ID used by coingecko API
    """
    token_file = open('CoinGeckoCoins.json', encoding="utf8")
    tokens = json.load(token_file)
    for token in tokens:
        if token['symbol'] == symbol:
            return token['id']


def get_symbol_eth_address(symbol):
    """
    :param symbol: The symbol of a coin/token
    :returns the eth token contract address if it exists, or None of it's not an ETH token
    """
    token_file = open('CoinGeckoCoins.json', encoding="utf8")
    tokens = json.load(token_file)
    for token in tokens:
        if token['symbol'] == symbol:
            if len(token['platforms']['ethereum']) > 0:
                return token['platforms']['ethereum']
    return None


def get_id_eth_address(id):
    """
    :param id: The id of a coin/token
    :returns the eth token contract address if it exists, or None of it's not an ETH token
    """
    token_file = open('CoinGeckoCoins.json', encoding="utf8")
    tokens = json.load(token_file)
    for token in tokens:
        if token['id'] == id:
            if len(token['platforms']['ethereum']) > 0:
                return token['platforms']['ethereum']
    return None
