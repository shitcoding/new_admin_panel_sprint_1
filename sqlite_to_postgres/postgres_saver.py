from dataclasses import fields

import psycopg2

from db_dataclasses import (Filmwork, Genre, GenreFilmwork, Person,
                            PersonFilmwork)
from logger import logger


def dataclass_to_pg_dict_row(obj):
    pg_dict_row = {}
    for field in fields(obj):
        pg_column_name = getattr(obj, 'field_map', {}).get(
            field.name, field.name
        )
        pg_dict_row[pg_column_name] = getattr(obj, field.name)
    return pg_dict_row


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
        logger.info('Saving {} entries to PosgreSQL...', len(obj_list))

        for obj in obj_list:
            try:
                pg_row = dataclass_to_pg_dict_row(obj)
                column_names = ','.join(pg_row.keys())
                column_placeholders = ','.join(['%s'] * len(pg_row))
                values = curs.mogrify(
                    column_placeholders, tuple(pg_row.values())
                ).decode('utf-8')

                query = (
                    f'INSERT INTO {obj.table_schema}.{obj.table_name} '
                    f'({column_names}) VALUES ({values})'
                    f' ON CONFLICT (id) DO NOTHING'
                )
                curs.execute(query)
            except (psycopg2.Error, psycopg2.OperationalError) as e:
                logger.exception('Error saving entry to PosgreSQL: {}', str(e))
        logger.info('Succesfully processed {} entries', len(obj_list))
