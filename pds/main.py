import dag_cbor

from crypto.keys import generate_key_pair, sign, verify_signature

public_key, private_key = generate_key_pair()

data = {
    "ola": 3
}

signature = sign(private_key, dag_cbor.encode(data))

print(verify_signature(public_key, dag_cbor.encode(data), signature))