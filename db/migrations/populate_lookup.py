import logging

# Script to manually run population of lookup table
from db.schema import sync_lookup
from db.session import session_from_env

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

with session_from_env() as db_session:
    logger.info("Starting lookup table population")
    sync_lookup(db_session)
    db_session.commit()
