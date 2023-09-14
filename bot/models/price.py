from bot.data.models.base import Base


class PairPrice(Base):
    symbol: str
    price: float
    reference_asset: str = "USD"
