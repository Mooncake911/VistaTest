import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()


def get_database_url() -> str:
    if database_url := os.getenv("DATABASE_URL"):
        return database_url

    return "sqlite:///./diary.db"


DATABASE_URL = get_database_url()

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args={
        "check_same_thread": False
    } if DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=engine)


def drop_tables():
    Base.metadata.drop_all(bind=engine)
