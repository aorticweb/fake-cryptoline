import enum

from sqlalchemy import CheckConstraint, Column, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import VARCHAR, Boolean, Integer

from db.schema.common import Base, SoftDeleteixin, TimestampMixin, UUIDMixin
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
    send_email = Column(Boolean, default=False, server_default="0")
    send_sms = Column(Boolean, default=False, server_default="0")
    priority = Column(Integer, default=1, server_default="1")
    repeat = Column(Boolean, default=False, server_default="0")


class NotificationStatusEnum(enum.Enum):
    pending = "PENDING"
    attempting_delivery = "ATTEMPTING_DELIVERY"
    delivered = "DELIVERED"
    cleared = "CLEARED"


class Notification(UUIDMixin, TimestampMixin, SoftDeleteixin, Base):
    __tablename__ = "alert_notification"

    alert_id = Column(UUID, ForeignKey("alert.id"), nullable=False)
    status = Column(
        VARCHAR(30),
        default=NotificationStatusEnum.pending.value,
        server_default="0",
        nullable=False,
    )
