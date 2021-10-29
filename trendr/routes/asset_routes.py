import re
import os
import json
import yfinance as yf
import yahooquery as yq

from flask import Blueprint, request, jsonify
from textblob import TextBlob

from trendr.connectors import twitter_connector
from trendr.connectors import fear_and_greed_connector
from trendr.connectors import coin_gecko_connector
from trendr.tasks.social.twitter.gather import store_tweet_by_id
from trendr.tasks.social.reddit.gather import (
    store_comments,
    store_submissions
)
from .helpers.json_response import json_response

assets = Blueprint("assets", __name__, url_prefix="/assets")


@assets.route('/fear-greed', methods=['GET'])
def fear_and_greed():
    crypto_values = fear_and_greed_connector.get_current_crypto_fear_and_greed()
    stock_values = fear_and_greed_connector.get_current_stock_fear_and_greed()
    data = {'crypto_values': crypto_values, 'stock_values': stock_values}
    return jsonify(data)


@assets.route('/stocks/official-channels', methods=['GET'])
def stock_official_channels():
    content = request.get_json()
    req = yf.Ticker(content['name']).info
    result = {'website': req['website']}
    return jsonify(result)


@assets.route('/crypto/official-channels', methods=['GET'])
def crypto_official_channels():
    content = request.get_json()
    coin_id = content['name']
    return jsonify(coin_gecko_connector.get_coin_links(coin_id))


@assets.route('/historic-fear-greed', methods=['GET'])
def historic_fear_and_greed_crypto():
    content = request.get_json()
    if content and 'days' in content:
        days = int(content['days'])
    else:
        days = 365
    values = fear_and_greed_connector.get_crypto_historic_values(days)
    return jsonify(values)


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


@assets.route('/sp500', methods=['GET'])
def sp_500():
    content = request.get_json()
    print("\nfetching history market data for S&P500" + "\n")

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


@assets.route('/gdow', methods=['GET'])
def gdow():
    content = request.get_json()
    print("\nfetching history market data for The Global Dow" + "\n")

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


@assets.route("/stats", methods=["POST"])
def stats():
    content = request.get_json()

    print("\nfetching general stats for: " + content['name'] + "\n")

    stock = yf.Ticker(content['name'])
    return jsonify(stock.info)


@assets.route("/history", methods=["POST"])
def history():
    content = request.get_json()

    print("\nfetching history market data for: " + content["name"] + "\n")

    stock = yf.Ticker(content["name"])
    p = content["period"]

    period_to_interval = {
        "1d": "5m",
        "5d": "30m",
        "1mo": "1h",
        "3mo": "1h",
        "1y": "1d",
        "5y": "5d",
    }

    return stock.history(
        period=p,
        interval=period_to_interval.get(p),
        prepost="True",
        actions="False",
    ).to_json()


@assets.route("/twitter_sentiment", methods=["POST"])
def twitter_sentiment():
    content = request.get_json()

    results = twitter_connector.get_tweets_mentioning_asset(content["name"])
    text = []

    for result in results:
        print(result.text)

        text_clean = re.sub(r'@[A-Za-z0-9]+', '', result.text)
        text_clean = re.sub(r'#', '', text_clean)
        text_clean = re.sub('\n', ' ', text_clean)

        # using this will take a lot longer that TextBlobs default analyzer
        # blob = TextBlob(result.text, analyzer=NaiveBayesAnalyzer())

        blob = TextBlob(text_clean)

        # first number: polarity (-1.0 = very negative, 0 = neutral, 1.0 = very positive)
        # second number: subjectivity (0.0 = objective, 1.0 = subjective)
        text.append([text_clean, blob.sentiment])

    return jsonify(text)


@assets.route("/reddit_sentiment", methods=["GET"])
def reddit_sentiment_route():

    res = store_tweet_by_id.delay(tweet_id=1450846775221399566)

    res_2 = store_submissions.delay(keywords=["apple"], limit=50)
    res_3 = store_comments.delay(keywords=["apple"], limit=50)

    return json_response(
        [res.get(timeout=100), res_2.get(timeout=100), res_3.get(timeout=100)]
    )
