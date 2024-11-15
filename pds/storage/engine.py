from os import makedirs

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from storage.models import RepoBase

def repo_session() -> sessionmaker:
    folder = "data/blocks.db"

    engine = create_engine(f"sqlite+pysqlite:///{folder}/blocks.db")
    RepoBase.metadata.create_all(engine)

    return sessionmaker(engine)