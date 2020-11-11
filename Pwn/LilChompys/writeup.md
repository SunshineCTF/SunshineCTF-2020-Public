# [PWN 700] LilChompy's

Custom implementation of malloc/free and a UAF/double free vulnerability.


## How It Works

For details of the internals of this heap implementation, refer to [heap_internal.h](heap_internal.h), which
contains detailed documentation comments explaining the layout and structure of the various heap objects.

The challenge is a theme park designer software that allows the user to build various attractions on different
lots. Each attraction has a different kind as well as a name. The user may add a new attraction, demolish an
existing one, or rename an existing attraction. The only (intentional) vulnerability in this challenge is in
the rename command. As soon as the user selects a lot to rename, the name is freed. However, if the user then
enters an empty name, this function will error out and return before setting `fun->name` to either a valid
pointer or `NULL`. This leaves a dangling pointer to a freed heap object that previously held the name string.

After running my exploit 100 times locally, it got the flag 82 of those 100 times.


### Stage 0: The forward-looking setup

This stage is where the exploit enters the initial password. It also stores a fake heap metadata object in
the global password buffer for use later by stage 4. This uses a trick that's used by various other parts of
the exploit. Specifically, the `getInput()` function (and by extension, `getLine()`) keeps reading bytes until
a newline, which means that the line returned by `getInput()` can contain NUL bytes in the middle. This is
used to make the `strcmp()` on the password succeed while still having extra data after it.


### Stage 1: Leaking the base address of the heap arena

This is a fairly complicated stage as it sets up the heap layout in a way that's useful to leak a heap address
as well as for use throughout the rest of this exploit. Some info to keep in mind:

* Every allocation is a multiple of 0x10 bytes
* In between every allocation is a single heap metadata block of size 0x10 bytes
* The size of `struct Attraction` is 0x10 bytes
* The name allocation can be any of 0x10, 0x20, 0x30, or 0x40 bytes, as it's rounded up from the length of the
  input line (up to 50) to the nearest 0x10 bytes (which is 64 aka 0x40 bytes)
* Adjacent free blocks will be automatically coalesced into a single larger free block
* An allocation will always land in the smallest available free node that's large enough to hold the size

The steps taken in stage 1 are illustrated below:

![heap layout diagram](images/heap_diagram.jpg)

1. Allocate 3 Attraction & name objects, making some space in the heap.
2. Leaking `1.name` w/ the vulnerability and demolishing Attraction 2 (both struct and name), making a large
   free block. This leaves `1.name` as a dangling pointer to offset 0x40 within the heap.
3. Attraction 2 is now located at offset 0x40 in the heap (pointed to by `1.name`), and a hole of size 0x20 is
   left between `3.name` and 3.
4. Leak `2.name` w/ the bug, allocate object 4. Attraction 4 will land where `2.name` points, and `4.name`
   will land in that 0x20 sized hole that was made in step 3. Also shrink `3.name` from 0x40 to 0x30 bytes.
   This had to be done after allocating `4.name`, otherwise that freed space would've coalesced w/ the 0x20
   sized free chunk and ruined the layout.
5. Leak `4.name` w/ the bug, which will cause the freed 0x20 chunk to coalesce into a 0x30 chunk 0x10 bytes
   before where `4.name` still points. Then, allocate Attraction 5, so that the struct lands at the beginning
   of this 0x30 chunk. This makes `4.name` point to the HeapMetadata struct directly after Attraction 5 and
   directly before the free chunk of size 0x10. This is the key part of the setup, as metadata directly before
   free chunks contain pointers within the heap to other freed chunks (as part of the free tree). However,
   both the `smaller` and `bigger` fields of this metadata chunk will be `NULL` currently, so step 6 causes
   the `smaller` field to be set.
6. Demolish 3 to free up some space earlier in the heap, then reallocate `5.name` to be smaller so that it
   fits in the free space that was just made by demolishing 3. This leaves a 0x10 byte free chunk after
   `5.name`, which will be inserted as the `smaller` node in the free tree from the free node currently
   pointed to by `4.name`.

Now, just list the attractions, read the bytes from 4.name, and unpack the pointer bits to find a heap
address. Round it down to the beginning of the page and the base address of this heap arena is now leaked and
known!


### Stage 2: Leaking the base address of the main executable

The strategy here is to corrupt the `kind` field of an Attraction struct. Then, when it's listed,
`funToString[kind]` will result in reading a string pointer from somewhere else in the binary. The target here
is the `__dso_handle` symbol, which is a pointer that points to itself.

1. Resize `5.name` from 0x10 to 0x30 to have it coalesce with the 0x10 sized free chunk after it. This is
   important in order to control where the next 0x10 byte allocation will land.
2. Rename Attraction 2, which will actually result in freeing Attraction 4. The new name will be allocated in
   the same 0x10 sized chunk, which is pointed to by the dangling pointer `attractions[3]`. This name will be
   a fake Attraction struct whose `kind` field will be a negative index such that `funToString[kind]` will be
   `__dso_handle`, and the `name` field is just set to `NULL` for now.

Then, the attractions are listed, and the address of `__dso_handle` is leaked as Attraction 4's kind string.
This leaked address is used to calculate the base address of the main executable with ASLR applied.


### Stage 3: Leaking the base address of libc

To leak a pointer from the main binary to libc, a better leaking primitive is needed. Using an OOB `kind`
value only works if it can reach a pointer to a pointer to libc, which I did not easily find while developing
this exploit. The obvious approach here is to corrupt the `name` field of an Attraction struct to be the
address to read from. Renaming Attraction 2 like in the previous stage wouldn't work though, as the last byte
of the `name` pointer (which is also the last byte of the 0x10 sized Attraction struct) must be zero due to
how the `getLine` function works. To address this, the heap layout is adjusted so that `1.name` is a 0x30
sized allocation, and it overlaps Attraction 2, giving full control over that struct's fields.

1. Leak `2.name` using the bug, leaving a 0x10 sized free chunk directly after Attraction 2.
2. Rename Attraction 1 to a 0x30 sized allocation. `1.name` currently points to Attraction 2, so when it is
   freed, it will coalesce with the 0x10 sized free chunk that was made in the previous step. Then, the new
   name will start with a fake Attraction struct (0x10 bytes) whose `name` field points to `exe.got["puts"]`.

Now, the attractions are listed again, and this time Attraction 2's name leaks the address of `puts` in libc.


### Stage 4: Creating a fake heap region within the main executable

This stage is all about preparing to corrupt the `submitFuncs` array of function pointers. At the beginning
of this exploit in stage 0, a fake HeapMetadata struct was placed after the password in the global password
buffer. This metadata struct defines a single allocated block that's exactly large enough to span from the
middle of the `password` buffer to the end of the `line` buffer. The goal is to free this fake heap object to
add it to the free tree so that subsequent allocations may land in the main executable's global data section.

1. Rename Attraction 1 again to corrupt `2.name` to point to the fake heap object in the `password` buffer.
2. Leak `2.name` using the bug, but this time put the fake trailing HeapMetadata struct after the "2" input
   so that when the fake object is freed, the `cg_free` function doesn't crash.


### Stage 5: Allocate objects until a name overlaps the function pointers

At this stage, the free tree now contains 2 nodes: the fake object and the rest of the real heap arena. As the
fake object is smaller than the rest of the heap arena, the next allocations will come from this object. Some
calculations are performed to determine the correct ordering of allocation sizes such that a `name` allocation
will land exactly at the beginning of the `submitFuncs` global array of function pointers. This is used to
replace `submitFuncs[0]` with the address of the `system` function in libc.

Back in stage 2, Attraction 5 was renamed to contain the string "/bin/sh". It is also the only Attraction that
was created with `kind` set to 1 (`FUN_ROLLER_COASTER`). At this point, the exploit finishes by using the menu
command to submit the finalized theme park design for review. This command goes through each of the Attraction
objects and, based on the `kind` (but properly bounds checked), calls the corresponding function pointer from
`submitFuncs`, passing the Attraction's `name` as the first parameter. As the roller coaster function pointer
has been replaced with the address of `system`, when Attraction 5 is reached, it will actually call
`system("/bin/sh")`, resulting in a shell.
