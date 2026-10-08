# Name of program to build
TARGETS := florida_forecaster florida_forecaster.debug

# Compiler mitigations and other settings
BITS := 64
ASLR := 1
NX := 1
CANARY := 1
RELRO := 1

# Keep a debug version for the solve script to use
florida_forecaster_STRIP := 1
florida_forecaster.debug_DEBUG := 1

# Use 4 KB PIE segment alignment (as in 2020). Modern toolchains default to 2 MB
# text-segment alignment, which changes the low address bits from the original
# binary and breaks the intended solution.
LDFLAGS := -Wl,-z,max-page-size=0x1000

# Ubuntu version used by PwnableHarness at the time of SunshineCTF 2020
UBUNTU_VERSION := 16.04

# Deployment settings
DOCKER_IMAGE := sun20-florida-forecaster
DOCKER_PORTS := 20002

# Optionally disable PwnableHarness's time limit for this challenge
#DOCKER_TIMELIMIT := 0

# Files to publish
PUBLISH_BUILD := $(firstword $(TARGETS))

# `pwnmake check`: the solver retries and includes a ~30s wait, so allow more
# time than the 120s default.
CHECK_TIMEOUT := 300
$(call ctf_check_slow,$(DIR),$(DOCKER_PORTS),python3 solution.py)
