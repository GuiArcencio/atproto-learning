from typing import Self

from multiformats import CID
from sqlalchemy.orm import Session

from pds.repo.mst.tree_node import SignedCommit, TreeNode, UnsignedCommit
from pds.repo.tid import generate_tid
from pds.storage import DataBlock, get_account_info, repo_session, update_account_info


class MerkleSearchTree:
    commit: SignedCommit

    @classmethod
    def new(
        cls,
        session: Session,
        did: str,
        signing_key: bytes,
    ) -> Self:
        tree = MerkleSearchTree()
        root_node = TreeNode.create_empty()

        commit = UnsignedCommit(
            did=did, version=3, data=root_node.to_cid(), revision=generate_tid()
        )
        signed_commit = commit.sign(signing_key)

        session.add(root_node.to_datablock())
        session.add(signed_commit.to_datablock())
        update_account_info(mst_root=signed_commit.to_cid().encode("base32"))

        return tree

    @classmethod
    def load(cls, session: Session) -> Self:
        tree = MerkleSearchTree()

        account_info = get_account_info()
        commit_cid = CID.decode(account_info["mst_root"])

        tree.commit = SignedCommit.from_cid(session, commit_cid)

        return tree
