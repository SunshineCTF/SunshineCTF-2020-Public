CHAL := $(notdir $(DIR))

# Build every speedrun challenge FROM SOURCE with PwnableHarness. When it
# compiles a binary itself, PwnableHarness automatically links in
# stdio_unbuffer.c (an __attribute__((constructor)) that disables stdout/stderr
# buffering before main). That replaces the old LD_PRELOAD "unbuffer.so" that we
# used to --inject when shipping the prebuilt binaries, so no preload / custom
# Dockerfile is needed here anymore.

# All challenges build and run on Ubuntu 22.04. Its gcc defaults (PIE +
# full RELRO + stack-protector-strong) match the "modern-gcc" mitigations seen
# in the originally distributed 2020 binaries; each challenge then overrides the
# individual knobs below to reproduce its exact checksec profile.
UBUNTU_VERSION := 22.04

# Per-challenge mitigation table, derived from each challenge's original 2020
# gcc flags (see each NN/Makefile) and the distributed binary's `checksec`:
#   columns: BITS PIE RELRO NX CANARY
#     BITS   : 32 (-m32 / i386) or 64
#     PIE    : 1 (PIE) or 0 (-no-pie)
#     RELRO  : 1 (full) / partial (compiler default) / 0 (-z norelro)
#     NX     : 1 (noexecstack) or 0 (-z execstack)
#     CANARY : 1 (stack protector) or 0 (-fno-stack-protector)
#
# Note on #14: its Makefile uses -fno-stack-protector (so CANARY=0 here), but
# checksec reports "canary found" purely because static glibc pulls in
# __stack_chk_fail. It is handled as a static build below.
MIT_00 := 64 1 1       1 0
MIT_01 := 64 1 1       1 0
MIT_02 := 32 0 partial 1 0
MIT_03 := 64 1 1       0 0
MIT_04 := 64 0 partial 1 0
MIT_05 := 64 1 1       1 0
MIT_06 := 64 1 1       0 0
MIT_07 := 64 1 1       0 1
MIT_08 := 64 0 0       1 0
MIT_09 := 64 1 1       1 1
MIT_10 := 32 0 partial 1 0
MIT_11 := 32 0 0       1 0
MIT_12 := 32 1 0       1 0
MIT_13 := 32 0 partial 1 0
MIT_14 := 64 0 partial 1 0
MIT_15 := 64 1 1       0 0
MIT_16 := 64 1 1       1 1
MIT_17 := 64 1 1       1 1

_MIT   := $(MIT_$(CHAL))
BITS   := $(word 1,$(_MIT))
PIE    := $(word 2,$(_MIT))
RELRO  := $(word 3,$(_MIT))
NX     := $(word 4,$(_MIT))
CANARY := $(word 5,$(_MIT))

# Build the challenge executable from its C source.
TARGET := chall_$(CHAL)
SRCS := chall_$(CHAL).c

# #14 is a static binary (original: -static). NO_RPATH avoids adding an rpath,
# which is meaningless for a static executable.
ifeq "$(CHAL)" "14"
LDFLAGS := -static
NO_RPATH := 1
endif

DOCKER_IMAGE := sun20-speedrun-$(CHAL)
# port = 20 6 nn (c=6 speedrun), nn = speedrun number
DOCKER_PORTS := 206$(CHAL)
DOCKER_TIMELIMIT := 30
DOCKER_CHALLENGE_NAME := chall_$(CHAL)
# DOCKER_CHALLENGE_PATH is intentionally left unset so PwnableHarness defaults it
# to the from-source build product ($(BUILD_DIR)/chall_$(CHAL)). (The old value
# $(DIR)/chall_$(CHAL) pointed at the committed prebuilt, which is no longer the
# deployed binary.)

# Publish the from-source build (this is now the canonical binary that players
# get, not a committed prebuilt). None of the speedrun solvers depend on a
# specific remote libc, so PUBLISH_LIBC is not needed for any of them.
PUBLISH_BUILD := chall_$(CHAL)

# `pwnmake check`: run each speedrun exploit and verify it prints the flag.
# This file is shared across all 18 challenges (via Speedrun/Build.mk's BUILD_MK
# override), so $(DIR)=Speedrun/NN and $(CHAL)=NN resolve per challenge, giving
# port 206NN and a check registered as check[Speedrun/NN].
# PYTHONPATH=.. lets the solvers that `import sf` find Speedrun/sf.py when run
# from the challenge directory.
$(call ctf_check,$(DIR),206$(CHAL),env PYTHONPATH=.. python3 exploit.py)
