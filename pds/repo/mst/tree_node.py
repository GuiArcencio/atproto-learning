from __future__ import annotations

from typing import Optional, Self

from dataclasses import dataclass

from repo.cid import ContentAddressable
from multiformats import CID
from repo.mst.tree_entry import TreeEntry
from repo.cid import ContentAddressable
from crypto.keys import sign

@dataclass
class TreeNode(ContentAddressable):
    left_node: Optional[CID]
    entries: list[TreeEntry]

    @classmethod
    def create_empty(cls) -> Self:
        return TreeNode(
            left_node=None,
            entries=list()
        )
    
    def to_json(self) -> dict:
        return {
            "l": self.left_node,
            "e": list(map(lambda e: e.to_json(), self.entries))
        }

@dataclass
class UnsignedCommit(ContentAddressable):
    did: str
    version: int
    data: CID
    revision: str

    def to_json(self) -> dict:
        return {
            "did": self.did,
            "version": self.version,
            "data": self.data,
            "rev": self.revision,
            "prev": None
        }

    def sign(self, signing_key: bytes) -> SignedCommit:
        serialized = self.to_cbor()
        signature = sign(signing_key, serialized)

        return SignedCommit(
            did=self.did,
            version=self.version,
            data=self.data,
            revision=self.revision,
            signature=signature
        )

@dataclass
class SignedCommit(UnsignedCommit):
    signature: bytes

    def to_json(self) -> dict:
        base_json = super().to_json()
        base_json["sig"] = self.signature

        return base_json
    
    def to_unsigned(self) -> UnsignedCommit:
        return UnsignedCommit(
            did=self.did,
            version=self.version,
            data=self.data,
            revision=self.revision
        )

