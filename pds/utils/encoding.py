from base64 import b32encode

_OLD_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
_NEW_CHARS = "234567abcdefghijklmnopqrstuvwxyz"
_TRANSLATION_TABLE = translation_table = str.maketrans(_OLD_CHARS, _NEW_CHARS, "=")

def base32_sortable_encoding(data: bytes) -> str:
    # was this really necessary? ffs
    encoded_str = b32encode(data).decode()
    
    return encoded_str.translate(_TRANSLATION_TABLE)