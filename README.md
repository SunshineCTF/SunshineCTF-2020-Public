SunshineCTF 2020 Challenges
-----

This is the public release of the challenges from SunshineCTF 2020. Unless otherwise specified, all challenges are released under the MIT license.

## How to build/deploy Pwn, Speedrun, and Pegasus challenges

```bash
git clone https://github.com/C0deH4cker/PwnableHarness.git && cd PwnableHarness
git clone --recursive https://github.com/HackUCF/SunshineCTF-2020-Public.git sun20 && cd sun20
```

* To compile all binaries: `make`
* To build Docker images for all server-based challenges: `make docker-build`
* To run Docker containers for all server-based challenges: `make docker-start`
* To publish all build artifacts that should be distributed to players to the `publish` folder/symlink: `make publish`
* The Pegasus directory also adds:
  * `make check`: Run test suite for assembler and emulator
  * `make solve`: Run solution scripts for all challenges, using `localhost` for server challenges
  * `make solve SERVER=<address>`: Run solution scripts for all challenges using the provided IP/hostname as the target server

Most of the server-based challenges will be deployed to https://ctf.hackucf.org soon.
