from typing import Optional

from multiformats import CID

class TreeEntry:
    prefix_length: int
    key_suffix: bytes
    value: CID
    right_node: Optional[CID]