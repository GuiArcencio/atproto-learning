from pds.repo.mst.tree import MerkleSearchTree
from pds.repo.cid import generate_cid
from pds.crypto.keys import generate_key_pair, verify_signature
from pds.storage import repo_session, DataBlock
from multiformats import CID
from pds.crypto.hash import hash
import dag_cbor

def main():
    pub, priv = generate_key_pair()
    print(MerkleSearchTree.new("did:plc:teste", priv))

    with repo_session().begin() as session:
        block: DataBlock
        for block in DataBlock.get_all(session):
            cid, content = block.decode()

            print(cid.encode("base32"))
            print(generate_cid(dag_cbor.encode(content)))

if __name__ == "__main__":
    main()