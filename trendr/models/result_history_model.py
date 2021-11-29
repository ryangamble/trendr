import enum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.types import Integer, DateTime, String, Enum

from trendr.extensions import db


class SymbolTypeEnum(enum.Enum):
    CRYPTO = 0
    STOCK = 1


class ResultHistory(db.Model):
    __tablename__ = "result_history"

    id = db.Column(Integer, primary_key=True, autoincrement="auto")

    ran_at = db.Column(DateTime, nullable=False, default=func.now())
    symbol = db.Column(String, nullable=False)
    type = db.Column(Enum(SymbolTypeEnum), nullable=False)

    # There is a many-one relationship between search and user
    user_id = db.Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="result_histories")
