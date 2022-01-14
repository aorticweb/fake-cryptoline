from sqlalchemy import CHAR, VARCHAR, Column

from db.schema.common import Base, SoftDeleteixin, TimestampMixin, UUIDMixin
from db.schema.const import ETH_ADDRESS_LENGTH


class User(UUIDMixin, TimestampMixin, SoftDeleteixin, Base):
    __tablename__ = "user"

    public_key = Column(CHAR(ETH_ADDRESS_LENGTH), unique=True, index=True, nullable=False)
    user_name = Column(VARCHAR(100), unique=True, index=True, nullable=False)
    email = Column(VARCHAR(255), nullable=True)
    phone = Column(VARCHAR(12), nullable=True)
