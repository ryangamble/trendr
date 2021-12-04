from trendr.extensions import db
from trendr.models.asset_model import Asset
from trendr.models.search_model import Search
from datetime import datetime


def new_search(asset: Asset) -> Search:
    search = Search(asset=asset, ran_at=datetime.now())
    db.session.add(search)
    db.session.commit()
    return search
