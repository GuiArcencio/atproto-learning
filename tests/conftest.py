import pytest
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker

from pds.storage.models import RepoBase


def fake_session(_: str, fake_engine: Engine) -> sessionmaker:
    RepoBase.metadata.create_all(fake_engine)

    return sessionmaker(fake_engine)


@pytest.fixture(scope="function", autouse=True)
def mock_db(monkeypatch):
    fake_engine = create_engine(f"sqlite+pysqlite:///:memory:")
    fake_session_function = lambda x: fake_session(x, fake_engine)

    monkeypatch.setattr("pds.storage.engine.repo_session", fake_session_function)
    monkeypatch.setattr("pds.storage.repo_session", fake_session_function)
