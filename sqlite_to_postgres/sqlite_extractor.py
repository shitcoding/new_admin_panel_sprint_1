import sqlite3


class SQLiteExtractor:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def fetch_all(
        self,
        table_name: str,
    ) -> list[dict]:
        curs = self.conn.cursor()
        curs.execute(f'SELECT * FROM {table_name};')
        data = curs.fetchall()
        return data

    def fetch_chunks(
        self,
        table_name: str,
        chunk_size: int = 100,
    ) -> list[dict]:
        curs = self.conn.cursor()
        curs.execute(f'SELECT * FROM {table_name};')
        while True:
            data_chunk = curs.fetchmany(chunk_size)
            if not data_chunk:
                break
            yield data_chunk
