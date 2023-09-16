import sqlite3

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from connectors import sqlite_conn_context
from db_dataclasses import (Filmwork, Genre, GenreFilmwork, Person,
                            PersonFilmwork)
from db_settings import DSL, SQLITE_DB_PATH
from logger import logger
from postgres_saver import PostgresSaver
from sqlite_extractor import SQLiteExtractor

TABLES = (Genre, Filmwork, Person, PersonFilmwork, GenreFilmwork)


def load_from_sqlite(
    sqlite_conn: sqlite3.Connection,
    pg_conn: _connection,
    chunk_size: int = 100,
):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_extractor = SQLiteExtractor(sqlite_conn)
    for db_dataclass in TABLES:
        for chunk in sqlite_extractor.fetch_chunks(
            db_dataclass.table_name, chunk_size
        ):
            obj_list = [db_dataclass(**item) for item in chunk]
            postgres_saver.save_objects(obj_list)


if __name__ == '__main__':
    with sqlite_conn_context(SQLITE_DB_PATH) as sqlite_conn, psycopg2.connect(
        **DSL, cursor_factory=DictCursor
    ) as pg_conn:

        logger.info(f'Loading data from SQLite to PostgreSQL...')
        load_from_sqlite(sqlite_conn, pg_conn)
        logger.info(f'Data migration completed succesfully')
