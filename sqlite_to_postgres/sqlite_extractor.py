import sqlite3

from logger import logger


class SQLiteExtractor:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def fetch_all(
        self,
        table_name: str,
    ) -> list[dict]:
        curs = self.conn.cursor()
        try:
            curs.execute(f'SELECT * FROM {table_name};')
            data = curs.fetchall()
            logger.info(f'Fetched all data from SQLite table: {table_name}')
            return data
        except sqlite3.Error as e:
            logger.error(
                f'Error fetching data from SQLite table {table_name}: {e}'
            )
            return []

    def fetch_chunks(
        self,
        table_name: str,
        chunk_size: int = 100,
    ) -> list[dict]:
        curs = self.conn.cursor()
        try:
            curs.execute(f'SELECT * FROM {table_name};')
            while data_chunk := curs.fetchmany(chunk_size):
                logger.info(
                    f'Fetched {chunk_size} entries '
                    f'from SQLite table: {table_name}'
                )
                yield data_chunk
        except sqlite3.Error as e:
            logger.error(
                f'Error fetching data from SQLite table {table_name}: {e}'
            )
            return []
