from abc import ABC, abstractmethod
from typing import Self, Optional

import dag_cbor
from multiformats import CID
from sqlalchemy.orm import Session
from pds.storage import repo_session, DataBlock
from pds.crypto.hash import hash, MULTIHASH

def generate_cid(data: bytes):
    return CID(
        base="base32",
        version=1,
        codec="dag-cbor",
        digest=(MULTIHASH, hash(data))
    )

class ContentAddressable(ABC):
    @abstractmethod
    def to_json(self) -> dict:
        pass

    def to_cbor(self) -> bytes:
        return dag_cbor.encode(self.to_json())
    
    def to_cid(self) -> CID:
        return generate_cid(self.to_cbor())
    
    def to_datablock(self) -> DataBlock:
        content = self.to_cbor()
        cid = generate_cid(content)

        return DataBlock(
            cid=bytes(cid),
            content=content
        )
    
    
    @classmethod
    @abstractmethod
    def from_json(cls, data: dict) -> Self:
        pass

    @classmethod
    def from_cid(cls, session: Session, cid: CID) -> Optional[Self]:
        block = DataBlock.get(session, bytes(cid))
        if block is None: return None

        _, content = block.decode()

        return cls.from_json(content)

