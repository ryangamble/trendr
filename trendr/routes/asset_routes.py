from flask import Blueprint, request, jsonify
import yfinance as yf
import yahooquery as yq
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import re

import pmaw
from trendr.connectors import twitter_connector
from trendr.connectors import reddit_connector
from trendr.tasks.reddit import *
from .helpers.json_response import json_response

assets = Blueprint('assets', __name__, url_prefix="/assets")


@assets.route('/search', methods=['POST'])
def search():
    content = request.get_json()

    data = yq.search(content['query'], news_count=0, quotes_count=10)

    return jsonify(data)


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


@assets.route('/twitter_sentiment', methods=['GET'])
def twitter_sentiment():
    results = twitter_connector.get_tweets_mentioning_asset("AAPL")
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
