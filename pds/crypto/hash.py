import hashlib

_HASHING_FUNCTION = hashlib.sha256

MULTIHASH = "sha2-256"

def hash(content: bytes) -> bytes:
    return _HASHING_FUNCTION(content, usedforsecurity=False).digest()