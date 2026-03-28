
from agentic_profile_matching.adapters.db.build_db_url import build_db_url
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

class Database:
    def __init__(self):

        database_url = build_db_url()

        self.engine = create_engine(
            database_url,
            pool_size=10,
            max_overflow=20,
            echo=False
        )

        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )

    def get_session(self) -> Session:
        return self.SessionLocal()