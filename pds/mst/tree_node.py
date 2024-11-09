from typing import Optional, Self

from multiformats import CID

from mst.tree_entry import TreeEntry

class TreeNode:
    left_node: Optional[CID]
    entries: list[TreeEntry]

    @staticmethod
    def create_root() -> Self:
        root = TreeNode()
        root.left_node = None
        root.entries = []
        return root