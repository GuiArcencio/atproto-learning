from typing import Self

from mst.tree_node import TreeNode

class MerkleSearchTree:
    root: TreeNode

    @classmethod
    def new(cls) -> Self:
        tree = MerkleSearchTree()
        tree.root = TreeNode.create_root()
        return tree