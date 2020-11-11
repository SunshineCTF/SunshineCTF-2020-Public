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

# Deployment settings
DOCKER_IMAGE := florida-forecaster
DOCKER_PORTS := 20002

# Disable PwnableHarness's time limit because the challenge revolves
# around exploiting a SIGALRM handler
#DOCKER_TIMELIMIT := 0

# Files to publish
PUBLISH_BUILD := $(firstword $(TARGETS))

# For archive.sunshinectf.org: Publish the port number as port.txt
$(call publish_port,$(DIR))
