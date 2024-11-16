from base64 import b32encode

_CHAR_MAP = dict(enumerate("234567abcdefghijklmnopqrstuvwxyz"))
_INVERTED_CHAR_MAP = {value: key for key, value in _CHAR_MAP.items()}

def base32_sortable_encode(data: bytes) -> str:
    # was this really necessary? ffs
    encoded_string = ""
    
    data_as_int = int.from_bytes(data, "big")
    while data_as_int > 0:
        index = data_as_int & 0b11111
        encoded_string = _CHAR_MAP[index] + encoded_string
        data_as_int = data_as_int >> 5

    return encoded_string

# This function likely won't be used, but it's
# necessary for tests
def base32_sortable_decode(data: str) -> bytes:
    decoded_int = 0
    number_of_bits = 0

    for character in data:
        decoded_int = decoded_int << 5
        value = _INVERTED_CHAR_MAP[character]
        decoded_int = decoded_int | value
        number_of_bits += 5

    # This is a ceil operation
    number_of_bytes = (number_of_bits + 7) // 8

    return decoded_int.to_bytes(number_of_bytes, "big")