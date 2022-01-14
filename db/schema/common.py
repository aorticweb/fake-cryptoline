import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import TIMESTAMP, Column, inspect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative, declarative_base
from sqlalchemy.sql.functions import now as sqlnow

# needed for defined default func

Base = declarative_base()
metadata = Base.metadata


def same_as_created_at(context):
    return context.get_current_parameters()["created_at"]


@as_declarative()
class Base:
    def dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def for_json(self):
        json_valid_dict = {}
        dictionary = self.dict()
        for key, value in dictionary.items():
            if isinstance(value, UUID) or isinstance(value, Decimal):
                json_valid_dict[key] = str(value)
            elif isinstance(value, date) or isinstance(value, datetime):
                json_valid_dict[key] = value.isoformat()
            else:
                json_valid_dict[key] = value

        return json_valid_dict

    def __rich_repr__(self):
        """Rich repr for interactive console.

        See https://rich.readthedocs.io/en/latest/pretty.html#rich-repr-protocol
        """
        return self.dict().items()


def uuid_gen() -> uuid.UUID:
    return uuid.uuid4()


def utc_timestamp_gen():
    """Generate a tz-aware timestamp pinned to UTC"""
    return datetime.utcnow()


class UUIDMixin:
    id = Column(UUID, primary_key=True, default=uuid_gen)


class TimestampMixin:
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=utc_timestamp_gen,
        server_default=sqlnow(),
    )

    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=same_as_created_at,
        onupdate=utc_timestamp_gen,
        server_default=sqlnow(),
    )


class SoftDeleteixin:
    deleted = Column(TIMESTAMP)
