"""config/database.py"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool
from config.settings import Settings
import time
import os
os.environ['TZ'] = 'Asia/Jakarta'
time.tzset()


from contextlib import contextmanager

settings = Settings()

# Deklarasikan Base di sini
Base = declarative_base()

class DatabaseConfig:
    def __init__(self):
        self.engine = None
        self.session_factory = None
        self._initialize()

    def _initialize(self):
        db_url = f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
        
        self.engine = create_engine(
            db_url,
            poolclass=QueuePool,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
            pool_recycle=3600,
            connect_args={'connect_timeout': 10}
        )
        
        self.session_factory = scoped_session(
            sessionmaker(
                bind=self.engine,
                autocommit=False,
                autoflush=False
            )
        )

    @contextmanager
    def get_session(self):
        session = self.session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def test_connection(self):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                with self.get_session() as session:
                    session.execute("SELECT 1")
                return True
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                time.sleep(2 ** attempt)
        return False

# Export Base untuk digunakan di modul lain
__all__ = ['DatabaseConfig', 'Base']
