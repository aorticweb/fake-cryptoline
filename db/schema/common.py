import logging
import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Any, Dict

from sqlalchemy import TIMESTAMP, Column, inspect
from sqlalchemy.dialects.postgresql import UUID, insert
from sqlalchemy.ext.declarative import as_declarative, declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import now as sqlnow

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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


class Lookup:
    """
    This is an experimental class to populate database rows for lookup tables.
    Warning: Avoid modifying existing rows (id, or other columns), no change
    will be applied.
    """

    model: Any = None
    value_column: str
    id_cache: Dict[int, model]
    value_cache: Dict[Any, model]

    @classmethod
    def get_all(cls):
        return [m for m in vars(cls).values() if isinstance(m, cls.model)]

    # TODO:
    # fetch current database rows and update if exists
    # create if it does not exist
    @classmethod
    def populate_db(cls, db_session: Session):
        rows = cls.get_all()
        if len(rows) == 0:
            return
        stmt = insert(cls.model).on_conflict_do_nothing()
        db_session.execute(stmt, [row.dict() for row in rows])
        logger.info(f"populated {len(rows)} lookup rows for {cls.model.__name__}")

    @classmethod
    def populate_id_cache(cls):
        if cls.id_cache is None:
            cls.id_cache = {m.id: m for m in cls.get_all()}

    @classmethod
    def populate_value_cache(cls):
        if cls.value_cache is None:
            cls.value_cache = {getattr(m, cls.value_column): m for m in cls.get_all()}

    @classmethod
    def get_by_id(cls, id: int) -> model:
        cls.populate_id_cache()
        return cls.id_cache.get(id)

    @classmethod
    def get_by_value(cls, value: Any) -> model:
        cls.populate_value_cache()
        return cls.value_cache.get(value)
