from os import makedirs

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pds.storage.models import RepoBase


def repo_session(did: str) -> sessionmaker:
    folder = f"data/{did}"
    makedirs(folder, exist_ok=True)

    engine = create_engine(f"sqlite+pysqlite:///{folder}/repo.db")
    RepoBase.metadata.create_all(engine)

    return sessionmaker(engine)
