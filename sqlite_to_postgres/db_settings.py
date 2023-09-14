import os

from dotenv import load_dotenv

load_dotenv()

SQLITE_DB_PATH = os.getenv('SQLITE_DB_PATH', 'db.sqlite')

DSL = {
    'dbname': os.getenv('POSTGRES_DB_NAME'),
    'user': os.getenv('POSTGRES_DB_USER'),
    'password': os.getenv('POSTGRES_DB_PASS'),
    'host': os.getenv('POSTGRES_DB_HOST'),
    'port': os.getenv('POSTGRES_DB_PORT'),
}
