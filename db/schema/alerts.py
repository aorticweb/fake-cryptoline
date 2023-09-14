import enum

from sqlalchemy import CheckConstraint, Column, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session, relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import VARCHAR, Boolean, Integer

from db.schema.common import Base, Lookup, SoftDeleteixin, TimestampMixin, UUIDMixin
from db.schema.const import PRICE_DECIMAL_LEN, PRICE_INT_LEN
from db.schema.users import User


class AlertPriorityEnum(enum.Enum):
    low = 1  # do not send notification
    medium = 2  # send notification
    high = 3  # send notification


class Alert(UUIDMixin, TimestampMixin, SoftDeleteixin, Base):
    __tablename__ = "alert"
    __table_args__ = (CheckConstraint("priority BETWEEN 1 AND 3"),)

    user_id = Column(UUID, ForeignKey("user.id", ondelete="cascade"), nullable=False)
    user = relationship(User)
    strike_price = Column(
        Numeric(PRICE_DECIMAL_LEN + PRICE_INT_LEN, PRICE_DECIMAL_LEN), nullable=False
    )
    coin_symbol = Column(Integer, ForeignKey("coin.symbol"), nullable=False)
    send_email = Column(Boolean, default=False, server_default="0")
    send_sms = Column(Boolean, default=False, server_default="0")
    priority = Column(Integer, default=1, server_default="1")
    repeat = Column(Boolean, default=False, server_default="0")


class NotificationStatus(Base):
    __tablename__ = "notification_status"

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(VARCHAR(40), nullable=False, unique=True)

    def __init__(self, id: int, status: str):
        self.id = id
        self.status = status


class NotificationStatusEnum(Lookup):
    model = NotificationStatus
    value_column = "status"

    pending = NotificationStatus(1, "pending")
    attempting_delivery = NotificationStatus(2, "attempting delivery")
    delivered = NotificationStatus(3, "delivered")
    cleared = NotificationStatus(4, "cleared")


class Notification(UUIDMixin, TimestampMixin, SoftDeleteixin, Base):
    __tablename__ = "alert_notification"

    alert_id = Column(UUID, ForeignKey("alert.id"), nullable=False)
    status_id = Column(
        Integer,
        ForeignKey("notification_status.id"),
        default=NotificationStatusEnum.pending.id,
        server_default=str(NotificationStatusEnum.pending.id),
        nullable=False,
    )


def sync_lookup(db_session: Session):
    NotificationStatusEnum.populate_db(db_session)
