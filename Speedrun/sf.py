"""Minimal reimplementation of the parts of the `sf` helper module
(guyinatuxedo/sf) used by the SunshineCTF 2020 speedrun solve scripts.

Only BufferOverflow and WriteFmtStr are provided, with just the methods the
committed exploits rely on. Built on top of pwntools.
"""
from pwn import p32, p64, fmtstr_payload


class BufferOverflow(object):
    def __init__(self, arch=64):
        self.arch = arch
        self.input_start = 0
        self.writes = []  # list of (index, bytes)

    def set_input_start(self, offset):
        # `offset` is the distance (in bytes) from the start of our input to the
        # reference point that add_int*/add_int64 offsets are measured against.
        self.input_start = offset

    def _add(self, offset, packed):
        # Offsets shrink toward the reference point, input grows from the start,
        # so the byte index of a field at `offset` is (input_start - offset).
        idx = self.input_start - offset
        self.writes.append((idx, packed))

    def add_int32(self, offset, value):
        self._add(offset, p32(value & 0xffffffff))

    def add_int64(self, offset, value):
        self._add(offset, p64(value & 0xffffffffffffffff))

    def add_int(self, offset, value):
        if self.arch == 64:
            self.add_int64(offset, value)
        else:
            self.add_int32(offset, value)

    def generate_payload(self):
        end = 0
        for idx, packed in self.writes:
            end = max(end, idx + len(packed))
        buf = bytearray(b"A" * end)
        for idx, packed in self.writes:
            buf[idx:idx + len(packed)] = packed
        return bytes(buf)


class WriteFmtStr(object):
    def __init__(self, arch=32, value=0, address=0, offset=0,
                 printed_bytes=0, alignment_bytes=0,
                 value_base=0, address_base=0):
        self.arch = arch
        self.value = value
        self.address = address
        self.offset = offset
        self.printed_bytes = printed_bytes
        self.alignment_bytes = alignment_bytes
        self.value_base = value_base
        self.address_base = address_base

    def generate_fmt_str(self):
        target_addr = self.address + self.address_base
        target_val = self.value + self.value_base
        payload = fmtstr_payload(
            self.offset,
            {target_addr: target_val},
            numbwritten=self.printed_bytes,
            write_size='short',
        )
        return payload
