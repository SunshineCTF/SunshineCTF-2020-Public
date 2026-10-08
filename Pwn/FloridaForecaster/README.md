# [PWN] Florida Forecaster

Florida Forecaster is a pwnable challenge of easy-intermediate difficulty.

## Building

The challenge consists of a single C file, `signal_handler_overwrite.c`, and the file `build.sh` that contains compile options. Running `build.sh` should be sufficient to recreate the challenge binary.

A Docker image is also provided in `florida_forecaster.tar`, that contains an image (`florida_forecaster`) with two tags (`release` and `strace`). Both contain the same target binary and flag, but `strace` provides strace output to the terminal for debugging assistance. Challenge was tested using the command `docker run -p 0.0.0.0:20002:20002 florida_forecaster:release`. Docker image may be rebuilt with the included Dockerfile.

## Maintenance

There should not be any required maintenance. However, a solution written using Python 2 (sorry, not 3) and pwntools is available in `solution.py`.

See [writeup.md](writeup.md) for the solution.
