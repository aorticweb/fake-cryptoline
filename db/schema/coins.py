from sqlalchemy import VARCHAR, Boolean, Column, ForeignKey, Integer
from sqlalchemy.orm import Session

from db.schema.common import Base, Lookup


class CoinType(Base):
    __tablename__ = "coin_type"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(VARCHAR(20), nullable=False, unique=True)

    def __init__(self, id: int, type: str):
        self.id = id
        self.type = type


class CoinTypeEnum(Lookup):
    model = CoinType
    value_column = "type"

    crypto = CoinType(1, "crypto")
    fiat = CoinType(2, "fiat")
    stable = CoinType(3, "stable")


class Coin(Base):
    __tablename__ = "coin"

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(VARCHAR(30), nullable=False, index=True, unique=True)
    name = Column(VARCHAR(100), nullable=False, unique=True)
    chain_name = Column(VARCHAR(100), nullable=False, unique=True)
    type_id = Column(Integer, ForeignKey("coin_type.id"), default=CoinTypeEnum.crypto.id)
    enabled = Column(Boolean, default=True, server_default="1")

    def __init__(self, id, symbol, name, chain_name, type_id=CoinTypeEnum.crypto.id, enabled=True):
        self.id = id
        self.symbol = symbol
        self.name = name
        self.chain_name = chain_name
        self.type_id = type_id
        self.enabled = enabled


def sync_lookup(db_session: Session):
    CoinTypeEnum.populate_db(db_session)
