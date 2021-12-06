import os
import json
import pandas as pd
from trendr.extensions import celery, db
from trendr.models.asset_model import Asset

called = False


def populate_database_with_symbols():
    """
    Populates the asset table with crypto, stocks, etfs, and indexes.
    If the table was populated previously, it will return.
    """
    global called
    if called:
        return "Function has been called previously"
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

    coin_gecko_path = os.path.join(SITE_ROOT, "CoinGeckoCoins.json")
    tokens = json.loads(open(coin_gecko_path, encoding="utf8").read())

    for token in tokens:
        symbol = token["symbol"]
        asset = Asset(
            identifier="crypto:" + token["id"],
            coinGeckoid=token["id"],
            reddit_q=symbol,
            twitter_q=symbol,
        )
        try:
            db.session.add(asset)
        except Exception as e:
            return "Asset Table have been populated previously"

    try:
        db.session.commit()
    except Exception as e:
        return "Asset Table have been populated previously"

    yahoo_stocks_path = os.path.join(SITE_ROOT, "yahoo_stocks.csv")
    df_stocks = pd.read_csv(yahoo_stocks_path)
    for i in range(len(df_stocks)):
        ticker = df_stocks.iloc[i]["Ticker"]
        asset = Asset(
            identifier="equity:" + ticker,
            reddit_q=ticker,
            twitter_q=ticker,
        )
        db.session.add(asset)
    db.session.commit()

    yahoo_etfs_path = os.path.join(SITE_ROOT, "yahoo_etfs.csv")
    df_etfs = pd.read_csv(yahoo_etfs_path)
    for i in range(len(df_etfs)):
        ticker = df_etfs.iloc[i]["Ticker"]
        asset = Asset(
            identifier="etf:" + ticker,
            reddit_q=ticker,  #
            twitter_q=ticker,
        )
        db.session.add(asset)

    db.session.commit()
    yahoo_indexes_path = os.path.join(SITE_ROOT, "yahoo_indexes.csv")
    df_indexes = pd.read_csv(yahoo_indexes_path)
    for i in range(len(df_indexes)):
        ticker = df_indexes.iloc[i]["Ticker"]
        asset = Asset(
            identifier="etf:" + ticker,
            reddit_q=ticker,
            twitter_q=ticker,
        )
        db.session.add(asset)
    db.session.commit()
    called = True
    return "Completed Populating table"
