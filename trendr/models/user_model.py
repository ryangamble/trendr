from flask_security.models import fsqla_v2 as fsqla
from sqlalchemy.orm import relationship
from sqlalchemy.types import Boolean, String
from trendr.extensions import db
from trendr.models.association_tables import user_asset_association


class Role(db.Model, fsqla.FsRoleMixin):
    __tablename__ = "role"


class User(db.Model, fsqla.FsUserMixin):
    __tablename__ = "user"

    # settings
    _settings_attrs = ("dark_mode", "currency")
    dark_mode = db.Column(Boolean, nullable=False, default=False)
    currency = db.Column(String, nullable=False, default="USD")

    # There is a one-many relationship between users and searches
    searches = relationship("Search", back_populates="user")

    # There is a one-many relationship between users and result histories
    result_histories = relationship("ResultHistory", back_populates="user")

    # There is a many-many relationship between users and assets
    assets = relationship(
        "Asset",
        secondary=user_asset_association,
        back_populates="users",
    )

    def __repr__(self):
        return "<User {}>".format(self.email)
