from abc import ABC, abstractmethod

import dag_cbor
from multiformats import CID
from storage.models import DataBlock
from crypto.hash import hash, MULTIHASH

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