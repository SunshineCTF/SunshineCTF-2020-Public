# LilChompy's: challenge with a custom heap allocator (libcageheap.so). A single
# PwnableHarness project builds the challenge binary + its allocator library and
# runs the real challenge (with the real flag) in one Docker image.

CHOMPY_DIR := $(DIR)
CHOMPY_BUILD := $(BUILD_DIR)

# List of targets to build
TARGETS := lilchompys lilchompys.debug libcageheap.so

# Build settings applied to all targets in this directory
CFLAGS := -Wall -Wextra
BITS := 64
ASLR := 1
NX := 1
CANARY := 1
RELRO := 1
DEBUG := 1

# Challenge originally ran on the PwnableHarness base image, which was Ubuntu
# 16.04 (glibc 2.23) in 2020. The published libc must match what runs here.
UBUNTU_VERSION := 16.04

# Build libcageheap.so in debug mode
libcageheap.so_SRCS := heap.c compat.c heap_debug.c
libcageheap.so := 1

# Its asserts embed __FILE__, which is the source path relative to wherever
# pwnmake runs (Pwn/LilChompys/heap.c here, a longer path from a parent
# workspace). That changes the library's layout, so the published handout
# wouldn't match a server built elsewhere. gcc 5 has no -fmacro-prefix-map, so
# pin __FILE__ instead.
libcageheap.so_CFLAGS := $(CFLAGS) -Wno-builtin-macro-redefined -D__FILE__='"libcageheap"'

# Build a release version of the lilchompys binary (still has symbols because
# DEBUG := 1 above; the solver reads symbols from this binary)
lilchompys_SRCS := lilchompys.c
lilchompys_LIBS := $(CHOMPY_BUILD)/libcageheap.so

# Build a debug version of the lilchompys binary (extra on-stream debug output)
lilchompys.debug_SRCS := lilchompys.c
lilchompys.debug_LIBS := $(CHOMPY_BUILD)/libcageheap.so
lilchompys.debug_CFLAGS := -DCHOMPY_DEBUG=1

# The executable leaks &__dso_handle by printing it with %s, so the leak is cut
# short at any zero byte in the randomized address. The default 2 MB segment
# alignment leaves the leak's third byte (base bits 21-23, +0x20) zero 1 run in
# 8. Aligning segments to 64 KB zeroes the base's low 16 bits instead, so the
# two low address bytes are fixed and non-zero and only the upper bytes (~1/256
# each) can truncate it -- about 1 failure in 30. (The solver also retries on a
# fresh connection, so a short leak is never fatal; this just makes most runs
# succeed first try.)
lilchompys_LDFLAGS := -Wl,-z,max-page-size=0x10000
lilchompys.debug_LDFLAGS := -Wl,-z,max-page-size=0x10000


# Deployment: single real image with the real flag (flag.txt in this directory).
DOCKER_IMAGE := sun20-lilchompys
DOCKER_PORTS := 20004
DOCKER_TIMELIMIT := 30

# A custom Dockerfile is needed so that libcageheap.so is installed next to the
# challenge binary (the binary's RPATH is $ORIGIN). Pass the built library path.
DOCKER_BUILD_ARGS := --build-arg "LIBCAGEHEAP=$(CHOMPY_BUILD)/libcageheap.so"
DOCKER_BUILD_DEPS := $(CHOMPY_BUILD)/libcageheap.so


# List of files to publish for players
PUBLISH_BUILD := lilchompys lilchompys.debug libcageheap.so
PUBLISH_LIBC := lilchompys-libc.so
PUBLISH := lilchompys.c heap.c compat.c heap_debug.c \
	heap.h heap_internal.h compat.h heap_debug.h \
	Build.mk Dockerfile BUILDING.md

# `pwnmake check`: the solver takes a while; allow extra headroom.
CHECK_TIMEOUT := 240
$(call ctf_check_slow,$(DIR),$(DOCKER_PORTS),python3 solve.py)
