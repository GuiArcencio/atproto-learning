from cryptography.hazmat.primitives.asymmetric import ec, utils
from cryptography.hazmat.primitives.hashes import SHA256


_CURVE = ec.SECP256R1()
_ORDER = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551
_ALGORITHM = ec.ECDSA(SHA256(), deterministic_signing=True)

def generate_key_pair() -> tuple[bytes, bytes]:
    private_key = ec.generate_private_key(_CURVE)
    public_key = private_key.public_key()
    public_numbers = public_key.public_numbers()

    private_key_bytes = private_key.private_numbers().private_value.to_bytes(length=32)
    public_key_bytes = public_numbers.x.to_bytes(length=32)
    sign_byte = bytes([0x02 if public_numbers.y % 2 == 0 else 0x03])
    public_key_bytes = sign_byte + public_key_bytes

    return public_key_bytes, private_key_bytes

def sign(private_key: bytes, data: bytes) -> bytes:
    key = ec.derive_private_key(int.from_bytes(private_key), _CURVE)
    signature = key.sign(data, _ALGORITHM)

    # Ensure low S
    r, s = utils.decode_dss_signature(signature)
    if s > _ORDER // 2:
        s = _ORDER - s

    return utils.encode_dss_signature(r, s)

def verify_signature(public_key: bytes, data: bytes, signature: bytes) -> bool:
    key = ec.EllipticCurvePublicKey.from_encoded_point(_CURVE, public_key)
    try:
        key.verify(signature, data, _ALGORITHM)
        return True
    except:
        return False