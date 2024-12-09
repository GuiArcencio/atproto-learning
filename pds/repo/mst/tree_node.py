from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Self

from multiformats import CID
from sqlalchemy.orm import Session

from pds.crypto.keys import sign, verify_signature
from pds.repo.cid import ContentAddressable
from pds.repo.mst.tree_entry import TreeEntry


@dataclass
class TreeNode(ContentAddressable):
    left_node: Optional[CID]
    entries: list[TreeEntry]

    @classmethod
    def create_empty(cls) -> Self:
        return TreeNode(
            left_node=None,
            entries=list(),
        )

    def to_json(self) -> dict:
        return {
            "l": self.left_node,
            "e": list(map(lambda e: e.to_json(), self.entries)),
        }

    @classmethod
    def from_json(cls, data: dict) -> Self:
        return TreeNode(left_node=data["l"], entries=data["e"])


# Intended to be used only as a temporary object
# to be signed
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
            "prev": None,
        }

    @classmethod
    def from_json(cls, data: dict) -> Self:
        return UnsignedCommit(
            did=data["did"],
            version=data["version"],
            data=data["data"],
            revision=data["rev"],
        )

    def sign(self, signing_key: bytes) -> SignedCommit:
        serialized = self.to_cbor()
        signature = sign(signing_key, serialized)

        return SignedCommit(
            did=self.did,
            version=self.version,
            data=self.data,
            revision=self.revision,
            signature=signature,
        )


@dataclass
class SignedCommit(UnsignedCommit):
    signature: bytes

    def to_json(self) -> dict:
        base_json = super().to_json()
        base_json["sig"] = self.signature

        return base_json

    @classmethod
    def from_json(cls, data: dict) -> Self:
        return SignedCommit(
            did=data["did"],
            version=data["version"],
            data=data["data"],
            revision=data["rev"],
            signature=data["sig"],
        )

    def to_unsigned(self) -> UnsignedCommit:
        return UnsignedCommit(
            did=self.did, version=self.version, data=self.data, revision=self.revision
        )

    def verify_signature(self, public_key: bytes) -> bool:
        data = self.to_unsigned().to_cbor()
        return verify_signature(public_key, data, self.signature)

    def load_root(self, session: Session) -> TreeNode:
        # TODO: assert is not None
        return TreeNode.from_cid(session, self.data)
