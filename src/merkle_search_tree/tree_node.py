from typing import Optional

from multiformats import CID

from merkle_search_tree.tree_entry import TreeEntry

class TreeNode:
    left_node: Optional[CID]
    entries: list[TreeEntry]