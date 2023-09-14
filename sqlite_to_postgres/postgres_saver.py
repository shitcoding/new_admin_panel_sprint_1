from dataclasses import astuple, fields

import psycopg2
from db_dataclasses import (Filmwork, Genre, GenreFilmwork, Person,
                            PersonFilmwork)


class PostgresSaver:
    def __init__(self, conn: psycopg2.extensions.connection):
        self.conn = conn

    def save_objects(
        self,
        obj_list: list[
            Filmwork | Genre | Person | GenreFilmwork | PersonFilmwork
        ],
    ):
        curs = self.conn.cursor()

        for obj in obj_list:
            columns = [field.name for field in fields(obj)]
            column_names = ','.join(columns)
            column_placeholders = ','.join(['%s'] * len(columns))

            values = curs.mogrify(column_placeholders, astuple(obj)).decode(
                'utf-8'
            )

            query = (
                f'INSERT INTO {obj.table_schema}.{obj.table_name} ({column_names}) VALUES ({values})'
                f' ON CONFLICT (id) DO NOTHING'
            )
            curs.execute(query)
