from loguru import logger

logger.add(
    'logs/sqlite_to_postgres.log',
    rotation='1 MB',
    level='INFO',
)
