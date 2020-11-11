# [PWN TBD] OOMG SPACE!

Just a simple challenge based on a potentially surprising difference between
syscalls and normal functions. Syscalls that access invalid pointers do not
cause segfaults, but rather return an error code 14 (Bad address). The trick
for exploiting this challenge is to send a massive size that will cause the
`malloc(size + 1)` to fail and return `NULL`. After this, the code will
attempt to NUL-terminate the buffer by doing `buffer[size] = '\0'`. When the
`buffer` pointer is NULL, however, this is the same as doing
`*(char*)size = '\0'`, which results in writing a zero byte to a controlled
address.

The only issue is that ASLR is on, so a memory address must be leaked. This is
where the username input comes in, as it doesn't ensure the `username` buffer
is NUL-terminated, so when it prints out the bad username, it'll leak the
address of the password buffer.

The corruption target here is to just set the first byte of `g_password` to
zero, as this will result in `memcmp_timesafe` being called with a zero size,
resulting in a no-op success.

The challenge name is a hint, as the "OOM" part of "OOMG SPACE!" means
"out of memory", referring to how you need to try to allocate more memory than
would succeed.
