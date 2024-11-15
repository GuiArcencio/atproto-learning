from typing import Optional, Self

from multiformats import CID

from mst.tree_entry import TreeEntry

class TreeNode:
    left_node: Optional[CID]
    entries: list[TreeEntry]
    
class SignedCommit:
    did: str
    version: int
    data: CID
    revision: str
    previous: None
    signature: bytes

class UnsignedCommit:
    did: str
    version: int
    data: CID
    revision: str
    previous: None
    signature: bytes