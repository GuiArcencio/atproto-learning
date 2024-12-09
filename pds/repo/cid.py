from abc import ABC, abstractmethod
from typing import Optional, Self

import dag_cbor
from multiformats import CID
from sqlalchemy.orm import Session

from pds.crypto.hash import MULTIHASH, hash
from pds.storage import DataBlock


def generate_cid(data: bytes):
    return CID(
        base="base32", version=1, codec="dag-cbor", digest=(MULTIHASH, hash(data))
    )


class ContentAddressable(ABC):

    @abstractmethod
    def to_json(self) -> dict: ...

    def to_cbor(self) -> bytes:
        return dag_cbor.encode(self.to_json())

    def to_cid(self) -> CID:
        return generate_cid(self.to_cbor())

    def to_datablock(self, revision: str) -> DataBlock:
        content = self.to_cbor()
        cid = generate_cid(content)

        return DataBlock(cid=bytes(cid), revision=revision, content=content)

    @classmethod
    @abstractmethod
    def from_json(cls, data: dict) -> Self: ...

    @classmethod
    def from_cid(cls, session: Session, cid: CID) -> Optional[Self]:
        block = DataBlock.get(session, bytes(cid))
        if block is None:
            return None

        _, content = block.decode()

        return cls.from_json(content)
