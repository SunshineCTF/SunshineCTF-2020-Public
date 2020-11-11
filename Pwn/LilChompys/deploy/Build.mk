# This file builds the actual Docker image with the real flag that runs on the server
DOCKERFILE := $(DIR)/Dockerfile
DOCKER_IMAGE_CUSTOM := true
DOCKER_IMAGE := lilchompys
DOCKER_BUILD_DEPS := docker-build[$(CHOMPY_DOCKER_IMAGE).release]
DOCKER_BUILD_ARGS := --build-arg "CHOMPY_DIR=$(CHOMPY_DIR)"

# This must be the same as the port for lilchompys-redacted
DOCKER_PORTS := 20003
