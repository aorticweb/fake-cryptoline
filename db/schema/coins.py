import enum

from sqlalchemy import VARCHAR, Boolean, Column

from db.schema.common import Base, UUIDMixin


class CoinTypeEnum(enum.Enum):
    crypto = "CRYPTO"
    fiat = "FIAT"


class Coin(UUIDMixin, Base):
    __tablename__ = "coin"

    symbol = Column(VARCHAR(30), nullable=False, index=True, unique=True)
    name = Column(VARCHAR(100), nullable=False, unique=True)
    type = Column(VARCHAR(20), default=CoinTypeEnum.crypto.value)
    stable = Column(Boolean, default=False, server_default="0")
    enabled = Column(Boolean, default=True, server_default="1")
