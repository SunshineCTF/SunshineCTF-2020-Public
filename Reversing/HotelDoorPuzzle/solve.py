# Angr script written by other people
import angr
import claripy

FLAG_LEN = 29
STDIN_FD = 0

# base_addr = 0x100000 # To match addresses to Ghidra
base_addr = 0

proj = angr.Project("./attachments/hotel_key_puzzle", main_opts={'base_addr': base_addr}) 

flag_chars = [claripy.BVS('sun{%d}' % i, 8) for i in range(FLAG_LEN)]
flag = claripy.Concat( *flag_chars + [claripy.BVV(b'\n')]) # Add \n for scanf() to accept the input

state = proj.factory.full_init_state(
        args=['./attachments/hotel_key_puzzle'],
        add_options=angr.options.unicorn,
        stdin=flag,
)

# Add constraints that all characters are printable
for k in flag_chars:
    state.solver.add(k >= ord('!'))
    state.solver.add(k <= ord('~'))

simgr = proj.factory.simulation_manager(state)
find_addr  = 0x22ba # SUCCESS
avoid_addr = 0x22c8 # FAILURE
simgr.explore(find=find_addr, avoid=avoid_addr)

if (len(simgr.found) > 0):
    for found in simgr.found:
        print(found.posix.dumps(STDIN_FD).decode('utf-8').strip())
