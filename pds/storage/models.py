from typing import Optional, Self, Sequence

import dag_cbor
from multiformats import CID
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class RepoBase(DeclarativeBase):
    pass


class DataBlock(RepoBase):
    __tablename__ = "datablock"

    cid: Mapped[bytes] = mapped_column(primary_key=True)
    content: Mapped[bytes]

    @classmethod
    def get_all(cls, session: Session) -> Sequence[Self]:
        statement = select(cls)
        return session.scalars(statement).all()

    @classmethod
    def get(cls, session: Session, cid: bytes) -> Optional[Self]:
        return session.get(cls, cid)

    def decode(self) -> tuple[CID, dict]:
        return (CID.decode(self.cid), dag_cbor.decode(self.content))
