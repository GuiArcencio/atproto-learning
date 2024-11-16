from time import sleep, time_ns

from freezegun import freeze_time

from pds.repo.tid import generate_tid
from pds.utils.encoding import base32_sortable_decode

@freeze_time("2024-10-14 13:52")
def test_tid_timestamp_is_valid():
    tid = generate_tid()
    tid_int = int.from_bytes(base32_sortable_decode(tid))
    time_microseconds = tid_int >> 10

    assert time_microseconds == (time_ns() // 1000)

def test_tid_format():
    tid = generate_tid()

    assert len(tid) == 13
    assert tid.isascii()

def test_different_tids_after_1ms():
    tid_1 = generate_tid()
    sleep(0.001) # 1ms
    tid_2 = generate_tid()

    assert tid_1 != tid_2