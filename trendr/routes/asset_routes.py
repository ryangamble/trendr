from flask import Blueprint, request, jsonify
import yfinance as yf
import yahooquery as yq
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import re
import os, json

import pmaw
from trendr.connectors import twitter_connector
from trendr.connectors import reddit_connector
from trendr.tasks.reddit import *
from .helpers.json_response import json_response

assets = Blueprint('assets', __name__, url_prefix="/assets")


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
    
    for item in crypto_filtered[0:10]:
        item['typeDisp'] = 'crypto'
        item['symbol'] = item.pop('symbol').upper()
        search_results.append(item)
    
    print('\n\nSearch Results for ' + query + ':\n')
    print(search_results)

    return jsonify(search_results)


@assets.route('/stats', methods=['POST'])
def stats():
    content = request.get_json()

    print("\nfetching general stats for: " + content['name'] + "\n")

    stock = yf.Ticker(content['name'])
    return jsonify(stock.info)


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


@assets.route('/twitter_sentiment', methods=['POST'])
def twitter_sentiment():
    content = request.get_json()

    results = twitter_connector.get_tweets_mentioning_asset(content['name'])
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
