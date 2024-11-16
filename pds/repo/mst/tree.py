from typing import Self

from repo.tid import generate_tid
from repo.mst.tree_node import SignedCommit, UnsignedCommit, TreeNode

from storage import repo_session, update_account_info

class MerkleSearchTree:
    commit: SignedCommit

    @classmethod
    def new(
        cls,
        did: str,
        signing_key: bytes
    ) -> Self:
        with repo_session().begin() as session:
            tree = MerkleSearchTree()
            root_node = TreeNode.create_empty()

            commit = UnsignedCommit(
                did=did,
                version=3,
                data=root_node.to_cid(),
                revision=generate_tid()
            )
            signed_commit = commit.sign(signing_key)

            session.add(root_node.to_datablock())
            session.add(signed_commit.to_datablock())
            update_account_info(
                mst_root=signed_commit.to_cid().encode("base32")
            )

            return tree