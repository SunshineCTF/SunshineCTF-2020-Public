# [PWN 250] Florida Forecaster

Florida Forecaster is a pwnable challenge of easy-intermediate difficulty.

## Intended solution

The binary should have all mitigations enabled, and specifically should include stack canaries and position independence. There is a stack based buffer overflow in the 'automated test' menu option, where the test data read in with `scanf("%s")` is not correctly limited with a width specifier.

Since stack canaries are enabled, a traditional return address overwrite will not succeed as it will fail the canary check upon function return. However, there is a signal handler function pointer on the stack in the frame below. The main function does some trickery that will expose a stack address available as a global variable that can be registered as a callback function to `signal(SIGALRM)`. 

There is a "win" function available that will display the contents of the flag file. Thus, successful exploitation requires overflowing the buffer with "test data," but not allowing the function to return (i.e., not providing an answer to the "Does it match?" question). This will cause the `alarm()` to fire after 30 seconds, which prints a message and then restores the old callback function (which we overwrote with test data) from `main`'s stack frame, which will fire again after the next timer expiration.

To bypass the position independence of this binary, there is an info leak hidden in the "forecast parameters" - if the first parameter is positive, the second parameter is negative, and they XOR to the value `0xc0c0c0c0`, an address will be 'leaked.' This can be used to calculate an offset and obtain the real address of the "win" function.

The main 'gotcha' with this is that overflowing the exact amount of the function pointer will cause a null byte to be written to the `local_signal_struct.delay` field. This causes the call to be `alarm(0)`, which cancels all alarms and will not allow exploitation. Similarly, overflowing too much will cause `alarm` to be called with a large integer, meaning it will take an excessive amount of time for the exploit to actually fire. Thus, contestants must overwrite the `delay` field with a reasonable value.

## Building

The challenge consists of a single C file, `signal_handler_overwrite.c`, and the file `build.sh` that contains compile options. Running `build.sh` should be sufficient to recreate the challenge binary.

A Docker image is also provided in `florida_forecaster.tar`, that contains an image (`florida_forecaster`) with two tags (`release` and `strace`). Both contain the same target binary and flag, but `strace` provides strace output to the terminal for debugging assistance. Challenge was tested using the command `docker run -p 0.0.0.0:20002:20002 florida_forecaster:release`. Docker image may be rebuilt with the included Dockerfile.

## Maintenance

There should not be any required maintenance. However, a solution written using Python 2 (sorry, not 3) and pwntools is available in `solution.py`. 
