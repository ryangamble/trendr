import json
from datetime import datetime
from pycoingecko import CoinGeckoAPI

'''
Documentation of CoingeckoAPI python wrapper can be found in: https://pypi.org/project/pycoingecko/
The actual documentation of CoinGecko API can be found in: https://www.coingecko.com/en/api/documentation


'''
class CoinGeckoHandler():

    cg = CoinGeckoAPI()
    def __init__(self):
        pass

    @staticmethod
    def convertTime(dateList):
        '''
        datelist: a list of unix times
        returns a python dataframe from this unix time
        '''
        for row in dateList:
            row[0] = datetime.utcfromtimestamp(row[0]/1000)

    @staticmethod
    def getHistoricPrices(coin, days):
        '''
        coin: The id of the coin as defined in the coingecko json file and API
        days: How many days of data to return
        returns a list of prices
        '''
        coin = coin.lower()
        prices = CoinGeckoHandler.cg.get_coin_market_chart_by_id(id= coin ,vs_currency='usd',days=days)['prices']
        CoinGeckoHandler.convertTime(prices)
        return prices

    @staticmethod
    def printHistoricPrice(dictOfPrices):
        '''
        dictofPrices: A dictionary of the time and price
        prints this dictionary
        '''
        for prices in dictOfPrices:
            print (prices)

    @staticmethod
    def getMarketCapHistory(coin, days):
        '''
        coin: The id of the coin as defined in the coingecko json file and API
        days: How many days of data to return
        returns a dictionary of the coins market cap and time of capture
        '''
        coin = coin.lower()
        mktCap = self.cg.get_coin_market_chart_by_id(id='bitcoin',vs_currency='usd',days='3')['market_caps']
        CoinGeckoHandler.convertTime(mktCap)
        return mktCap

    @staticmethod
    def getCoinLiveStats(coin):
        '''
        coin: The id of the coin as defined in the coingecko json file and API
        returns current live stats of a coin as a dictionary
        '''
        coin = coin.lower()
        stats = CoinGeckoHandler.cg.get_price(ids=coin, vs_currencies='usd', include_market_cap='true',
         include_24hr_vol='true', include_24hr_change='true', include_last_updated_at='true')
        if len(stats) == 0:
            return -1
        print (stats)
        coinStats = {'Name': coin}
        coinStats['Price'] = '$' + str(stats[coin]['usd'])
        coinStats['MarketCap'] = '${0:,.2f}'.format(stats[coin]['usd_market_cap'])
        coinStats['24HrVolume'] = '${0:,.2f}'.format(stats[coin]['usd_24h_vol'])
        coinStats['24HrChange'] = "%{:.2f}".format(stats[coin]['usd_24h_change'])
        return coinStats

    @staticmethod
    def converSymbolToId(symbol):
        '''
        symbol: The ticker of a coin/token
        if this symbl exists, we return the corresponding ID used by coingecko API
        '''
        tokFile = open('CoinGeckoCoins.json', encoding="utf8")
        tokens = json.load(tokFile)
        for token in tokens:
            if token['symbol'] == symbol:
                return token['id']

    def getSymbolEthAddress(symbol):
        '''
        symbol: The ticker of a coin/token
        return the ethd token contract address if it exists, or None of it's not
        an ETH token
        '''
        tokFile = open('CoinGeckoCoins.json', encoding="utf8")
        tokens = json.load(tokFile)
        for token in tokens:
            if token['symbol'] == symbol:
                if len(token['platforms']['ethereum']) > 0:
                    return token['platforms']['ethereum']
        return None


# print(prices)
# CoinGeckoHandler.converSymbolToId('rvp')
# print(handler.getCoinLiveStats('bitcoin'))