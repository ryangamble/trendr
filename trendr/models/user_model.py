from flask_security.models import fsqla_v2 as fsqla
from sqlalchemy.orm import relationship
from sqlalchemy.types import Boolean
from trendr.extensions import db
from trendr.models.association_tables import user_asset_association


class Role(db.Model, fsqla.FsRoleMixin):
    __tablename__ = "role"


class User(db.Model, fsqla.FsUserMixin):
    __tablename__ = "user"

    # settings
    _settings_attrs = ("dark_mode",)
    dark_mode = db.Column(Boolean, nullable=False)

    # There is a one-many relationship between users and searches
    searches = relationship("Search", back_populates="user")

    # There is a many-many relationship between users and assets
    assets = relationship(
        "Asset",
        secondary=user_asset_association,
        back_populates="users",
    )
    def get_settings(self):
        """
        Returns keyword dict of setting_name: setting_value
        """
        settings = {}
        for attr in self._settings_attrs:
            if hasattr(self, attr):
                settings[attr] = getattr(self, attr)
        
        return settings

    def set_settings(self, **kwargs):
        """
        Set settings contained in keyword args
        """

        for key, val in kwargs.values():
            if key in self._settings_attrs and hasattr(self, key):
                setattr(self, key, val)

        db.session.commit()

    def __repr__(self):
        return "<User {}>".format(self.email)
