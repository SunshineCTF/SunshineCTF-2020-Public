TARGET := oomg_space

BITS := 64

# Ubuntu version used by PwnableHarness at the time of SunshineCTF 2020
UBUNTU_VERSION := 16.04

ASLR := 1
NX := 1
RELRO := 1
CANARY := 1
STRIP := 1

DOCKER_IMAGE := sun20-oomg-space
DOCKER_PORTS := 20003
DOCKER_TIMELIMIT := 30

PUBLISH_BUILD := $(TARGET)

# `pwnmake check`: run the exploit and verify it prints the flag
$(call ctf_check,$(DIR),$(DOCKER_PORTS),python3 solve.py)
