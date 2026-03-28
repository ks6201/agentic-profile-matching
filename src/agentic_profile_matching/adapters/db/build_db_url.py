

import os

from sqlalchemy import URL
from dotenv import load_dotenv

def build_db_url() -> URL:
    load_dotenv()

    database_url = URL.create(
        "postgresql+psycopg2",
        username=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PASS"),
        host=os.getenv("DATABASE_HOST"),
        port=int(os.getenv("DATABASE_PORT") or 5432),
        database=os.getenv("DATABASE")

    )
    return database_url