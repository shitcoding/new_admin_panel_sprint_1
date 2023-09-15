import sqlite3
from dataclasses import astuple, fields

import psycopg2
import pytest
from psycopg2.extras import DictCursor

from sqlite_to_postgres.connectors import sqlite_conn_context
from sqlite_to_postgres.db_dataclasses import (Filmwork, Genre, GenreFilmwork,
                                               Person, PersonFilmwork)
from sqlite_to_postgres.db_settings import DSL, SQLITE_DB_PATH

TABLE_DATACLASSES = (Genre, Filmwork, Person, PersonFilmwork, GenreFilmwork)


def convert_pg_row_to_dataclass(row, dataclass):
    mapped_row = {}
    for field in fields(dataclass):
        pg_column_name = getattr(dataclass, 'field_map', {}).get(
            field.name, field.name
        )
        mapped_row[field.name] = row[pg_column_name]
    return dataclass(**mapped_row)


@pytest.mark.parametrize('table_dataclass', TABLE_DATACLASSES)
def test_data_consistency(table_dataclass):
    with sqlite_conn_context(SQLITE_DB_PATH) as sqlite_conn, psycopg2.connect(
        **DSL, cursor_factory=DictCursor
    ) as pg_conn:
        # Fetch data from SQLite
        sqlite_cursor = sqlite_conn.cursor()
        sqlite_cursor.execute(f'SELECT * FROM {table_dataclass.table_name}')
        sqlite_data = [table_dataclass(**row) for row in sqlite_cursor.fetchall()]

        # Fetch data from PostgreSQL
        pg_cursor = pg_conn.cursor()
        pg_cursor.execute(f'SELECT * FROM content.{table_dataclass.table_name}')
        rows = pg_cursor.fetchall()
        pg_data = [convert_pg_row_to_dataclass(row, table_dataclass) for row in rows]

        # Check record count
        assert len(sqlite_data) == len(
            pg_data
        ), f'Record count mismatch for table {table_dataclass.table_name}'

        # Check record content
        for record in sqlite_data:
            assert (
                record in pg_data
            ), f'Record {record} not found in PostgreSQL data for table {table_dataclass.table_name}'
