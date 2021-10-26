from flask_security.models import fsqla_v2 as fsqla
from sqlalchemy.orm import relationship
from trendr.extensions import db


class Role(db.Model, fsqla.FsRoleMixin):
    __tablename__ = "role"


class User(db.Model, fsqla.FsUserMixin):
    __tablename__ = "user"

    # There is a one-many relationship between users and searches
    searches = relationship("Search", back_populates="user")

    def __repr__(self):
        return "<User {}>".format(self.email)
