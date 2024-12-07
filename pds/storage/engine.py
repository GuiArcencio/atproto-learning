from os import makedirs

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pds.storage.models import RepoBase


def repo_session() -> sessionmaker:
    folder = "data"
    makedirs(folder, exist_ok=True)

    engine = create_engine(f"sqlite+pysqlite:///{folder}/blocks.db")
    RepoBase.metadata.create_all(engine)

    return sessionmaker(engine)
