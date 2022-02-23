from sqlalchemy.orm import Session

from .alerts import *  # noqa:
from .alerts import sync_lookup as alert_sync_lookup
from .coin_list import sync_lookup as coin_list_sync_lookup
from .coins import *  # noqa:
from .coins import sync_lookup as coin_sync_lookup
from .users import *  # noqa:


def sync_lookup(db_session: Session):
    alert_sync_lookup(db_session)
    coin_sync_lookup(db_session)
    coin_list_sync_lookup(db_session)
