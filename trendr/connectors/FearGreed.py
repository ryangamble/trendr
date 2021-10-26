import requests
from datetime import datetime


class FearGreed:

    def __init__():
        pass

    @staticmethod
    def convertTime(unixTime):
        '''
        unixTime: time unixtime format
        returns time as a pytohn date timestamp
        '''
        return datetime.utcfromtimestamp(unixTime)

    @staticmethod
    def getCryptoCurrentValue():
        '''
        returns the current value of the fear and greed index with its represntation
        '''
        response = requests.get("https://api.alternative.me/fng/?limit=1")
        values = {}
        values['value'] = response.json()['data'][0]['value']
        values['valueText'] = response.json()['data'][0]['value_classification']
        # values['timestamp'] = FearGreed.convertTime(float(response.json()['data'][0]['timestamp']))
        return values

    @staticmethod
    def getCryptoHistoricValues(days=365):
        '''
        days: how many days of crypto fear and index values are requested
        returns historic values of crypto fear and greed index up to 2018
        '''
        if days == 0:
            days = 1
        response = requests.get("https://api.alternative.me/fng/?limit=" + str(days))
        valueList = []
        for stamp in response.json()['data']:
            values = {}
            values['value'] = stamp['value']
            values['value_classification'] = stamp['value_classification']
            values['timestamp'] = FearGreed.convertTime(float(stamp['timestamp']))
            valueList.append(values)

        return valueList
    @staticmethod
    def printHistoricValues(listOfVals):
        for value in listOfVals:
            print(value)

    @staticmethod
    def getStocksCurrentValue():
        '''
        returns the stock market current fear and greed index value
        '''
        url = "https://fear-and-greed-index.p.rapidapi.com/v1/fgi"
        headers = {
            'x-rapidapi-host': "fear-and-greed-index.p.rapidapi.com",
            'x-rapidapi-key': "b5ba7967dcmsh69f36a951adbe11p1d2ff4jsnabfb5a0d224e"
            }
        response = requests.request("GET", url, headers=headers)
        return response.json()['fgi']['now']



print(FearGreed.getStocksCurrentValue())
print(FearGreed.getCryptoCurrentValue())
# print(response.text)
# print(FearGreed.getCurrentValue())
# vals = FearGreed.getHistoricValues(5)
# FearGreed.printHistoricValues(vals)