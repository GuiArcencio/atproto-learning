from enum import Enum
from typing import Optional, Self, Sequence

import dag_cbor
from multiformats import CID
from sqlalchemy import PrimaryKeyConstraint, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class RepoBase(DeclarativeBase):
    pass


class DataBlock(RepoBase):
    __tablename__ = "datablock"

    cid: Mapped[bytes] = mapped_column(primary_key=True)
    revision: Mapped[str] = mapped_column(String(13))
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


class KeyPair(RepoBase):
    __tablename__ = "keypair"

    class KeyPairType(Enum):
        ROTATION = "rotation"
        SIGNING = "signing"

    private_key: Mapped[bytes]
    public_key: Mapped[bytes]
    keypair_type: Mapped[KeyPairType]

    __table_args__ = (PrimaryKeyConstraint("private_key", "public_key"),)


class AccountInfo(RepoBase):
    __tablename__ = "account_info"

    key: Mapped[str] = mapped_column(primary_key=True)
    value: Mapped[str]

    @classmethod
    def get(cls, session: Session, key: str) -> Optional[Self]:
        return session.get(cls, key)
