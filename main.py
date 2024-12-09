import dag_cbor
from multiformats import CID

from pds.crypto.hash import hash
from pds.crypto.keys import generate_key_pair, verify_signature
from pds.repo.cid import generate_cid
from pds.repo.mst.tree import MerkleSearchTree
from pds.storage import DataBlock, repo_session


def main():
    pub, priv = generate_key_pair()
    with repo_session("did:plc:teste").begin() as session:
        MerkleSearchTree.new(session, "did:plc:teste", priv)

    with repo_session("did:plc:teste").begin() as session:
        tree = MerkleSearchTree.load(session)
        print(tree)


if __name__ == "__main__":
    main()
