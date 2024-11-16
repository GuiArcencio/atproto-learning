from pds.repo.mst.tree import MerkleSearchTree
from pds.repo.cid import generate_cid
from pds.crypto.keys import generate_key_pair, verify_signature
from pds.storage import repo_session, DataBlock
from multiformats import CID
from pds.crypto.hash import hash
import dag_cbor


def main():
    with repo_session().begin() as session:
        # pub, priv = generate_key_pair()
        # print(MerkleSearchTree.new(session, "did:plc:teste", priv))

        print(MerkleSearchTree.load(session).commit.load_root(session))


if __name__ == "__main__":
    main()
