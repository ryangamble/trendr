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
    if len(stats) == 0:
        return -1

    coin_stats = {
        'Name': coin,
        'Price': '$' + str(stats[coin]['usd']),
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
    token_file = open('connectors/CoinGeckoCoins.json', encoding="utf8")
    tokens = json.load(token_file)
    for token in tokens:
        if token['symbol'] == symbol:
            return token['id']


def get_symbol_eth_address(symbol):
    """
    :param symbol: The ticker of a coin/token
    :returns the eth token contract address if it exists, or None of it's not an ETH token
    """
    token_file = open('connectors/CoinGeckoCoins.json', encoding="utf8")
    tokens = json.load(token_file)
    for token in tokens:
        if token['symbol'] == symbol:
            if len(token['platforms']['ethereum']) > 0:
                return token['platforms']['ethereum']
    return None

def get_coin_links(coinid):
    '''
    :param coinid: The ID of the coin, as stored in coin gecko coins json file
    :returns a dictionary with the available links for the passed coin
    '''
    cg_api = CoinGeckoAPI()
    data = cg_api.get_coin_by_id(coinid,
        localization=False, market_data=False, community_data=False)['links']

    links = {}
    if len(data['homepage'][0]) > 0:
        links['homepage'] =  data['homepage'][0]
    if len(data['twitter_screen_name'])> 0:
        links['twitter'] : "https://twitter.com/" + data['twitter_screen_name']

    links['blockchain_links'] = []
    for blockchainurl in data['blockchain_site']:
        if len(blockchainurl) > 0:
            links['blockchain_links'].append(blockchainurl)
    if len(data['repos_url']['github']) > 0:
        links['repos_link'] = (data['repos_url']['github'][0])
    if len(data['telegram_channel_identifier']) > 0:
        links['Telegram_URL'] = 'https://t.me/' + data['telegram_channel_identifier']

    return links