import os
import json
import pandas as pd
from trendr.extensions import celery, db
from trendr.models.asset_model import Asset

@celery.task
def populate_database_with_symbols():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_path = os.path.join(SITE_ROOT, "CoinGeckoCoins.json")
    tokens = json.loads(open(json_path, encoding="utf8").read())
    for token in tokens:
        symbol = token['symbol']
        asset = Asset(
            identifier="cryto:" + symbol,
            reddit_q = symbol,
            twitter_q = symbol,
        )
        db.session.add(asset)
        # print('id', token['id'], 'symbol', token['symbol'], 'name', token['name'], 'crypto')

    df_stocks = pd.read_csv('yahoo_stocks.csv')
    for i in range(len(df_stocks)):
        ticker = df.iloc[i]['Ticker']
        asset = Asset(
            identifier="equity:" + ticker,
            reddit_q= ticker,
            twitter_q= ticker,
        )
        db.session.add(asset)
        # print('id' , '','symbol', df.iloc[i]['Ticker'],'name',  df.iloc[i]['Name'], 'Stock')

    df_etfs = pd.read_csv('yahoo_etfs.csv')
    for i in range(len(df_etfs)):
        ticker = df.iloc[i]['Ticker']
        asset = Asset(
            identifier="etf:" + ticker,
            reddit_q= ticker, #
            twitter_q= ticker,
        )
        db.session.add(asset)
        # print('id' , '','symbol', df.iloc[i]['Ticker'], 'name',  df.iloc[i]['Name'], 'ETF')

    df_indexes = pd.read_csv('yahoo_indexes.csv')
    for i in range(len(df_indexes)):
        ticker = df.iloc[i]['Ticker']
        asset = Asset(
            identifier="etf:" + ticker,
            reddit_q= ticker, #
            twitter_q= ticker,
        )
        db.session.add(asset)
    db.session.commit()
    # print('\n\n\n\nPopulating the databse!\n\n\n\n')
    # print('id' , '','symbol', df.iloc[i]['Ticker'], 'name', df.iloc[i]['Name'], 'Index')

