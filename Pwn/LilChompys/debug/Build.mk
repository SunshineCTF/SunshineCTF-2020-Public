# This file adds the debug build of the challenge binary to the Docker image
DOCKERFILE := $(DIR)/Dockerfile
DOCKER_IMAGE_CUSTOM := true
DOCKER_IMAGE := $(CHOMPY_DOCKER_IMAGE)
DOCKER_IMAGE_TAG := debug
DOCKER_BUILD_DEPS := docker-build[$(CHOMPY_DOCKER_IMAGE).release]
DOCKER_BUILD_ARGS := --build-arg "CHOMPY_BUILD=$(CHOMPY_BUILD)"
DOCKER_BUILD_ONLY := 1

# This must be the same as the port for lilchompys-redacted
DOCKER_PORTS := 20003
