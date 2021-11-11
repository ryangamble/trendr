from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, String

from trendr.extensions import db
from trendr.models.association_tables import user_asset_association


class Asset(db.Model):
    __tablename__ = "asset"

    id = db.Column(Integer, primary_key=True, autoincrement="auto")
    identifier = db.Column(String, nullable=False, unique=True)

    # There is a many-many relationship between users and assets
    users = relationship(
        "User",
        secondary=user_asset_association,
        back_populates="assets",
    )