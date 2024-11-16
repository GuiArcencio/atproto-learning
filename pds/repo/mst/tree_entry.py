from typing import Optional

from dataclasses import dataclass

from multiformats import CID

from repo.cid import ContentAddressable

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
            "t": self.right_node
        }