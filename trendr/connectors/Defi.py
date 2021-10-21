import requests
from CoinGeckoHandler import *
from trendr.config import ETHPLORERE_KEY
class Defi:

    '''
    Ethplrer API Documentation: https://github.com/EverexIO/Ethplorer/wiki/Ethplorer-API
    '''
    ethplorerURL = 'https://api.ethplorer.io/'
    # APIKEY = 'EK-fvFC8-t2SqhCU-YAqss'
    APIKEY = ETHPLORERE_KEY

    @staticmethod
    def getTopTokenHolders(tokAddr, number):
        '''
        tokAddr: Contract address of the token on the eth chain
        number: How many of the top holders are returned(max is 100)
        return the top holders in a dictionary
        '''
        path = Defi.ethplorerURL + "getTopTokenHolders/" + str(tokAddr) + "?apiKey=" + Defi.APIKEY +"&limit=" + str(number)
        response = requests.get(path)
        return response.json()['holders']

    @staticmethod
    def volumeHistory(tokAddr):
        '''
        tokAddr: Contract address of the token on the eth chain
        returns the volume of the token across avaialble data
        '''
        path = Defi.ethplorerURL + "getTokenPriceHistoryGrouped/" + str(tokAddr)  + "?apiKey=" + Defi.APIKEY
        response = requests.get(path)
        return response.json()


    @staticmethod
    def getTokenInfo(tokAddr):
        '''
        tokAddr: Contract address of the token on the eth chain
        return a json of token data from ethplorer API
        '''
        path = "getTokenInfo/"
        response = requests.get(Defi.ethplorerURL + path + tokAddr + "?apiKey=" + Defi.APIKEY)
        return response.json()

    def getSymbolAddress(symbol):
        '''
        symbol: ticker of the token
        returns the eth address of a token. If not available, returns None
        '''
        addr = CoinGeckoHandler.getSymbolEthAddress(symbol)
        if addr is not None:
            return addr
        else:
            return None


class TokenInfo:
    '''
    This class is a wrapper that combines Defi. Just supplying the symbol of a token
    to the constructor will fill all the data of in an object.
    '''
    def __init__(self, symbol, number=100):
        '''
        symbol: ticker of the cypto currency token0
        number: the number of top holders to return(max is 100)
        creates an object for the token and will fill all its info at creation.
        '''
        if number > 100:
            number = 100
        addr = Defi.getSymbolAddress(symbol)
        info = Defi.getTokenInfo(addr)
        self.attributes = {}
        self.attributes['addr'] = addr
        self.attributes['name'] = info['name']
        self.attributes['availableSupply'] = "{0:.2f}".format(float(info['price']['availableSupply']))
        # self.attributes['totalSupply'] = info['totalSupply']
        self.attributes['holdersCount'] = info["holdersCount"]
        self.attributes['Offical Website'] = info["website"]
        self.attributes['Offical Telegram'] = info["telegram"]
        self.attributes['Offical Twitter'] = info["twitter"]
        self.attributes['volume24h'] = str('$') + "{0:.2f}".format(float(info['price']["volume24h"]))
        # self.attributes['volDiff1'] = info['price']["volDiff1"]
        holderInfo = TokenInfo.getTopTokenHolders(self.attributes['addr'], number)
        self.top100holdersList = holderInfo[0]
        self.top100Ownership = str('%') + "{0:.2f}".format(float(holderInfo[1]))
        self.attributes['Liquidity'] = str('$') + str(Liquidity.getTokenLiquidity(addr))

    @staticmethod
    def getTopTokenHolders(tokAddr, number):
        '''
        tokAddr: The ETH address of the token
        number: How many of the top holders are returned(max is 100)
        returns two values, a list of lists, where each list has the number of tokens of holder,
        and the total ownership of the total supply. The second value is how many of the total supply
        this number of holders own.
        '''
        holders = Defi.getTopTokenHolders(tokAddr, number)
        top100TotalOwnership = 0
        Top100HoldersList = []
        for holder in holders:
            top100TotalOwnership += float(holder["share"])
            Top100HoldersList.append([holder['balance'], str('%') + str(holder['share']) ])
        # print(type(Top100HoldersList[0][0]))
        return Top100HoldersList, top100TotalOwnership

    def printSummary(self):
        '''
        prints a summary of all the information of this token object.
        '''
        for key in self.attributes:
            print(key + ":" + str(self.attributes[key]))
        self.printHolderSummary()

    def printHolderSummary(self):
        '''
        prints a summary of the top holders of this token object
        '''
        print('Top', len(self.top100holdersList), 'holders:')
        for holder in self.top100holdersList:
            print(holder)
        print('Total Ownership of Top', len(self.top100holdersList),':', self.top100Ownership)


    def getAddress(self):
        '''
        returns the token contract address of this token object
        '''
        return self.attributes['addr']

class Liquidity:
    '''
    Uniswap API documenation: https://docs.uniswap.org/protocol/V2/reference/API/overview
    '''

    SingleTokenliquidityQuery = """
    {{
    token(id: "{0}"){{
    name
    symbol
    tradeVolumeUSD
    totalLiquidity
    }}
    }}
    """

    url = 'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2'
    @staticmethod
    def getTokenLiquidity(tokAddr):
        try:
            response = requests.post(Liquidity.url, json = {"query": Liquidity.SingleTokenliquidityQuery.format(tokAddr)})
            response = json.loads(response.text)
            liqTot = response['data']['token']['totalLiquidity']
            return float("{0:.2f}".format(float(liqTot)))
        except:
            return None

token = TokenInfo('rvp', 10)
Defi.volumeHistory(token.getAddress())
