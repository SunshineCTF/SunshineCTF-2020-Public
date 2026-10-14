# [PWN] LilChompy's

## Challenge files to publish for players

Two files are shared with players, both produced by `pwnmake publish`:

* The exact `libc.so` used in the server's Docker container
  (`lilchompys-libc.so`).
* An archive (`lilchompys.tar.gz`) which contains:
  - The challenge binary (`lilchompys`), compiled with debug symbols, and
    `lilchompys.debug` (built with extra on-stream debug output)
  - The custom heap implementation library (`libcageheap.so`), compiled with debug
    symbols and debug functionality
  - Full source code for both of these binaries
  - Related files needed to build these items:
    + `Build.mk`
    + `BUILDING.md`
    + `Dockerfile`

In 2020 players also got an exported Docker image without the flag
(`docker-image-redacted.tar.gz`); that is no longer published. The archive plus
`BUILDING.md` is enough to build and run the challenge locally.


## Deployment

This challenge is built and deployed with PwnableHarness. `Build.mk` builds the
binaries and the allocator library and produces one Docker image,
`sun20-lilchompys`, which contains the real flag (`flag.txt` here) and listens on
port 20004. `pwnmake docker-start` runs it; `pwnmake check` builds it, runs
`solve.py` against it and tears it down.
