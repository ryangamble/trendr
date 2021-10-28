from flask import Blueprint, request, jsonify
import yfinance as yf
import yahooquery as yq
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import re
import os, json
from trendr.connectors.CoinGeckoHandler import *
import pmaw
from trendr.connectors import twitter_connector
from trendr.connectors import reddit_connector
from trendr.connectors.FearGreed import *
from trendr.tasks.reddit import *
from .helpers.json_response import json_response

assets = Blueprint('assets', __name__, url_prefix="/assets")



@assets.route('/FearGreed', methods=['GET'])
def FearandGreed():
    # content = request.get_json()
    cryptoVals = FearGreed.getCryptoCurrentValue()
    stockVals = FearGreed.getStocksCurrentValue()
    data = {'cryptoVals': cryptoVals, 'stockVals': stockVals}
    return jsonify(data)

@assets.route('/HistoricFearGreed', methods=['GET'])
def historicFearandGreedCrypto():
    content = request.get_json()
    if content and 'days' in content:
        days = int(content['days'])
    else:
        days = 365
    vals = FearGreed.getCryptoHistoricValues(days)
    return jsonify(vals)

@assets.route('/search', methods=['POST'])
def search():
    content = request.get_json()
    query = content['query']

    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_path = os.path.join(SITE_ROOT, '../connectors', 'CoinGeckoCoins.json')
    crypto_list = json.loads(open(json_path).read())

    crypto_filtered = [
        v for v in crypto_list
        if query.lower() == v['symbol'].lower() or query.lower() == v['name'].lower()
        or query.lower() in v['symbol'].lower() or query.lower() in v['name'].lower()
    ]

    short_list = sorted(crypto_filtered, key=lambda d: len(d['name']))

    # print(filtered[0:10])

    stock_filtered = yq.search(query, news_count=0, quotes_count=10)

    search_results = []
    # print (data)

    for item in stock_filtered['quotes'][0:5]:
        if item['typeDisp'] == 'Equity' or item['typeDisp'] == 'ETF':
            item['typeDisp'] = item.pop('typeDisp').lower()
            if 'shortname' in item:
                item['name'] = item.pop('shortname')
            if 'longname' in item:
                item['name'] = item.pop('longname')
            item.pop('isYahooFinance')
            item.pop('quoteType')
            item.pop('index')
            item.pop('score')
            search_results.append(item)

    for item in short_list[0:5]:
        item['typeDisp'] = 'crypto'
        item['symbol'] = item.pop('symbol').upper()
        search_results.append(item)

    print('\n\nSearch Results for ' + query + ':\n')
    print(search_results)

    return jsonify(search_results)

@assets.route('/SP500', methods=['GET'])
def SP500():
    content = request.get_json()
    print("\nfetching history market data for S&P500"  + "\n")

    stock = yf.Ticker('GSPC')
    p = content['period']

    period_to_interval = {
        "1d": "5m",
        "5d": "30m",
        "1mo": "1h",
        "3mo": "1h",
        "1y": "1d",
        "5y": "5d"
    }
    return stock.history(period=p, interval=period_to_interval.get(p), prepost="True", actions="False").to_json()


@assets.route('/GDOW', methods=['GET'])
def GDOW():
    content = request.get_json()
    print("\nfetching history market data for The Global Dow"  + "\n")

    stock = yf.Ticker('GDOW')
    p = content['period']

    period_to_interval = {
        "1d": "5m",
        "5d": "30m",
        "1mo": "1h",
        "3mo": "1h",
        "1y": "1d",
        "5y": "5d"
    }
    return stock.history(period=p, interval=period_to_interval.get(p), prepost="True", actions="False").to_json()

@assets.route('/stats', methods=['POST'])
def stats():
    content = request.get_json()

    print("\nfetching general stats for: " + content['name'] + "\n")

    stock = yf.Ticker(content['name'])
    return jsonify(stock.info)

@assets.route('/crypto/stats', methods=['POST'])


@assets.route('/history', methods=['POST'])
def history():
    content = request.get_json()

    print("\nfetching history market data for: " + content['name'] + "\n")

    stock = yf.Ticker(content['name'])
    p = content['period']

    period_to_interval = {
        "1d": "5m",
        "5d": "30m",
        "1mo": "1h",
        "3mo": "1h",
        "1y": "1d",
        "5y": "5d"
    }

    return stock.history(period=p, interval=period_to_interval.get(p), prepost="True", actions="False").to_json()


@assets.route('/twitter_sentiment', methods=['GET'])
def twitter_sentiment():
    content = request.get_json()
    text = []

    for result in results:
        print(result.text)

        textClean = re.sub(r'@[A-Za-z0-9]+', '', result.text)
        textClean = re.sub(r'#', '', textClean)
        textClean = re.sub('\n', ' ', textClean)

        # using this will take a lot longer that TextBlobs default analyzer
        # blob = TextBlob(result.text, analyzer=NaiveBayesAnalyzer())

        blob = TextBlob(textClean)

        # first number: polarity (-1.0 = very negative, 0 = neutral, 1.0 = very positive)
        # second number: subjectivity (0.0 = objective, 1.0 = subjective)
        text.append([textClean, blob.sentiment])

    return jsonify(text)

@assets.route('/reddit_sentiment', methods=['GET'])
def reddit_sentiment_route():
    res = reddit_sentiment.delay()

    return json_response(res.get(timeout=30))

