from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from configs.db_config import get_connect_string, DB_CONFIG


class SessionManager:
    """如果不懂，可以暂时先看作一个进行了优化的session对象工厂"""
    _engine = None
    _Session = None

    @classmethod
    def _init_engine(cls):
        if cls._engine is None:
            cls._engine = create_engine(
                get_connect_string(),
                pool_size=DB_CONFIG['pool_size'],
                max_overflow=DB_CONFIG['max_overflow'],
                echo=DB_CONFIG['echo_sql']
            )
            cls._Session = sessionmaker(
                bind=cls._engine,
                autocommit=False,
                autoflush=False
            )

    @classmethod
    def get_session(cls) -> Session:
        cls._init_engine()
        return cls._Session()