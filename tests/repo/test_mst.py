import pds.storage
from pds.crypto.keys import generate_key_pair
from pds.repo.mst.tree import MerkleSearchTree
from pds.repo.mst.tree_node import TreeNode


def test_mst_creation_and_load():
    did = "did:plc:test"
    public_key, private_key = generate_key_pair()

    with pds.storage.repo_session(did).begin() as session:
        MerkleSearchTree.new(session, did, private_key)
    with pds.storage.repo_session(did).begin() as session:
        tree = MerkleSearchTree.load(session)

        assert tree.commit.did == did
        assert tree.commit.version == 3
        assert tree.commit.verify_signature(public_key)
        assert tree.commit.load_root(session) == TreeNode(left_node=None, entries=[])
