"""Service monitors for system health."""

from fastapi.logger import logger
from geneweaver.db.monitor.db_health import health_check as db_health_check
from psycopg import Cursor


def check_db_health(cursor: Cursor) -> dict:
    """Check DB health status.

    @param cursor: DB cursor
    @return: db health response (dict).
    """
    try:
        results = db_health_check(cursor)
        return results

    except Exception as err:
        logger.error(err)
        raise err
