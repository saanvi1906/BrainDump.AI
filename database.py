from sqlmodel import SQLModel, create_engine
from sqlalchemy.engine import Engine
from config import settings

def _sqlite_connect_args(url: str):
    return {"check_same_thread": False} if url.startswith("sqlite") else {}

engine: Engine = create_engine(settings.DATABASE_URL, connect_args=_sqlite_connect_args(settings.DATABASE_URL), echo=False)

def init_db():
    SQLModel.metadata.create_all(engine)
