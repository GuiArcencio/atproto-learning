from dataclasses import dataclass
from typing import Optional, Self

from multiformats import CID

from pds.repo.cid import ContentAddressable


@dataclass
class TreeEntry(ContentAddressable):
    prefix_length: int
    key_suffix: bytes
    value: CID
    right_node: Optional[CID]

    def to_json(self) -> dict:
        return {
            "p": self.prefix_length,
            "k": self.key_suffix,
            "v": self.value,
            "t": self.right_node,
        }

    @classmethod
    def from_json(cls, data: dict) -> Self:
        return TreeEntry(
            prefix_length=data["p"],
            key_suffix=data["k"],
            value=data["v"],
            right_node=data["t"],
        )
