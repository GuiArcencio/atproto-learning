from typing import Self

from multiformats import CID
from sqlalchemy.orm import Session

from pds.repo.mst.tree_node import SignedCommit, TreeNode, UnsignedCommit
from pds.repo.tid import generate_tid
from pds.storage import AccountInfo, DataBlock, repo_session


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
        revision = generate_tid()

        commit = UnsignedCommit(
            did=did, version=3, data=root_node.to_cid(), revision=revision
        )
        signed_commit = commit.sign(signing_key)

        session.add(root_node.to_datablock(revision=revision))
        session.add(signed_commit.to_datablock(revision=revision))
        session.add(
            AccountInfo(key="mst_root", value=signed_commit.to_cid().encode("base32"))
        )

        return tree

    @classmethod
    def load(cls, session: Session) -> Self:
        tree = MerkleSearchTree()

        mst_root = AccountInfo.get(session, "mst_root").value
        commit_cid = CID.decode(mst_root)

        tree.commit = SignedCommit.from_cid(session, commit_cid)

        return tree

    def put_record(self, session: Session, key: bytes, record: bytes):
        pass
