from os import urandom
from time import time_ns

from pds.utils.encoding import base32_sortable_encode

_CLOCK_ID = urandom(3)


def generate_tid() -> str:
    microseconds = time_ns() // 1000

    # 53 bits
    tid_integer = (microseconds & 0x1FFFFFFFFFFFFF) << 10
    # 10 bits
    tid_integer = tid_integer | (int.from_bytes(_CLOCK_ID) & 0x3FF)

    tid_bytes = tid_integer.to_bytes(length=8, byteorder="big")

    return base32_sortable_encode(tid_bytes)
