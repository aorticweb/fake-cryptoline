import os
from contextlib import contextmanager
from logging import getLogger
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

logger = getLogger(__name__)


def engine(db_uri: str):
    return create_engine(db_uri, pool_pre_ping=True)


@contextmanager
def session_from_env() -> Generator[Session, None, None]:
    """
    Generate DB connection from env var
    SQLALCHEMY_DATABASE_URI
    """
    if os.environ.get("SQLALCHEMY_DATABASE_URI", None) is None:
        logger.error("SQLALCHEMY_DATABASE_URI not set!")
        raise RuntimeError("no SQLALCHEMY_DATABASE_URI defined")

    db = _session(os.environ["SQLALCHEMY_DATABASE_URI"])

    try:
        yield db
    finally:
        db.close()


@contextmanager
def session_from_uri(db_uri) -> Generator[Session, None, None]:
    db = _session(db_uri)
    try:
        yield db
    finally:
        db.close()


def _session(db_uri) -> Session:
    db_uri = os.environ["SQLALCHEMY_DATABASE_URI"]
    return sessionmaker(
        autocommit=False, expire_on_commit=False, autoflush=False, bind=engine(db_uri)
    )()
