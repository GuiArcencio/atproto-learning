from multiformats import CID

from cryptography.hash import hash, MULTIHASH

def generate_cid(content: bytes) -> CID:
    return CID(
        base="base32",
        version=1,
        codec="dag-cbor",
        digest=(MULTIHASH, hash(content))
    )