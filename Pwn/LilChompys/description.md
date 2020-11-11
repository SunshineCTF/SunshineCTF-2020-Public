While browsing around some Shodan queries, I stumbled across an access
terminal to a theme park designer tool hosted by BSides Orlando! It appears
that the filthy organizers are trying to contract someone to design a new
park for them called Lil Chompy's. Everyone loves Lil Chompy the gator, but
I think he deserves to live freely outside of an alligator pit!

Help me free Lil Chompy from the clutches of those BSides Orlando fools by
gaining access to their server so we can halt planning and construction of
this theme park!

`nc chal.2020.sunshinectf.org 20003`

Note:

You can run the exact Docker container (w/o the flag of course) as is running
on the challenge server with this command:

`docker run -p 20003:20003 -itd kjcolley7/lilchompys-redacted:release`

There's also the `debug` tag which swaps out `lilchompys` with a version of it
built with `CHOMPY_DEBUG=1` (in the archive as `lilchompys.debug`):

`docker run -p 20003:20003 -itd kjcolley7/lilchompys-redacted:debug`

* [lilchompys.tar.gz](https://chal.2020.sunshinectf.org/218ad968dfae82f5/lilchompys.tar.gz)
* [lilchompys-libc.so](https://chal.2020.sunshinectf.org/218ad968dfae82f5/lilchompys-libc.so)

Author: kcolley
