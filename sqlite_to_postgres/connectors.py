import sqlite3
from contextlib import contextmanager
from datetime import datetime

from logger import logger


# Register the custom sqlite datetime converter
def convert_datetime(val: str):
    return datetime.fromisoformat(val.decode())


sqlite3.register_converter('timestamp', convert_datetime)


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


@contextmanager
def sqlite_conn_context(db_path: str) -> sqlite3.Connection:
    try:
        conn = sqlite3.connect(
            f'file:{db_path}?mode=ro',  # Open in read-only mode
            detect_types=sqlite3.PARSE_DECLTYPES,
            uri=True,
        )
        conn.row_factory = dict_factory
        yield conn
        conn.close()
    except sqlite3.OperationalError as e:
        logger.error(
            'Error when trying to open SQLite database file: {}', str(e)
        )
