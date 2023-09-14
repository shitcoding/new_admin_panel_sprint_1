import sqlite3

import psycopg2
from connectors import sqlite_conn_context
from db_dataclasses import (Filmwork, Genre, GenreFilmwork, Person,
                            PersonFilmwork)
from db_settings import DSL, SQLITE_DB_PATH
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from sqlite_extractor import SQLiteExtractor

TABLES = (Genre, Filmwork, Person, PersonFilmwork, GenreFilmwork)



def load_from_sqlite(
    sqlite_conn: sqlite3.Connection,
    pg_conn: _connection,
    chunk_size: int = 100,
):
    """Основной метод загрузки данных из SQLite в Postgres"""
    # postgres_saver = PostgresSaver(pg_conn)
    sqlite_extractor = SQLiteExtractor(sqlite_conn)
    for db_dataclass in TABLES:
        for chunk in sqlite_extractor.fetch_chunks(
            db_dataclass.table_name, chunk_size
        ):
            obj_list = [db_dataclass(**item) for item in chunk]
            print(obj_list)
            print('\n\n')


if __name__ == '__main__':
    with sqlite_conn_context(SQLITE_DB_PATH) as sqlite_conn, psycopg2.connect(
        **DSL, cursor_factory=DictCursor
    ) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
