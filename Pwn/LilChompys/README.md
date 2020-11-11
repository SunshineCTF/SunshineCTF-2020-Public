# [PWN 700] LilChompy's

## Challenge files to publish for players

A lot of files are shared with players as part of this challenge:

* The exact `libc.so` used in the server's Docker container.
* An exported archive of the challenge's Docker container but without the flag
  (`docker-image-redacted.tar.gz`)
* An archive (`lilchompys.tar.gz`) which contains:
  - The challenge binary (`lilchompys`), compiled with debug symbols
  - The custom heap implementation library (`libcageheap.so`), compiled with debug
    symbols and debug functionality
  - Full source code for both of these binaries
  - Related files needed to build these items:
    + `Build.mk`
    + `BUILDING.md`
    + `Dockerfile`

The PwnableHarness project is already configured to automatically build and publish
these files when `make publish` is run from the PwnableHarness directory.


## Deployment

This challenge is designed to be built and deployed using PwnableHarness. If the
Docker containers should be run outside of PwnableHarness (such as in GCP), be aware
of this potentially confusing aspect. There are two separate Docker images produced
by this project, `lilchompys-redacted` and `lilchompys`.

* `lilchompys-redacted` is the Docker image produced by this directory's `Build.mk`
  file, and it is the one that's exported as `docker-image-redacted.tar.gz` to be
  shared with players. It does not contain the real flag and should not be run on
  the challenge servers.
* `lilchompys` is the Docker image produced by the `deploy/Build.mk` file. This is
  the real, private Docker image which contains the real flag and should be run as
  the challenge server.
