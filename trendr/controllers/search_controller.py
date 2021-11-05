from trendr.extensions import db
from trendr.models.search_model import Search
from datetime import datetime


def new_search(search_string) -> Search:
    search = Search(search_string=search_string, ran_at=datetime.now())
    db.session.add(search)
    db.session.commit()
    return search
