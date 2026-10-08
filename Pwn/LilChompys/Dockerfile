# The base image's ONBUILD steps (triggered at this FROM) copy the challenge
# binary into /home/$CHALLENGE_NAME/. The binary links against libcageheap.so
# with an RPATH of $ORIGIN, so the library must live in that same directory.
FROM c0deh4cker/pwnableharness:base-16.04-v2.1

ARG CHALLENGE_NAME
ARG LIBCAGEHEAP
COPY $LIBCAGEHEAP /home/$CHALLENGE_NAME/libcageheap.so
RUN chmod 0755 /home/$CHALLENGE_NAME/libcageheap.so
