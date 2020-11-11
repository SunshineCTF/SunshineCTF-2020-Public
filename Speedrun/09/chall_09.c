#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char key[50] = "\x79\x17\x46\x55\x10\x53\x5f\x5d\x55\x10\x58\x55\x42\x55\x10\x44\x5f\x3a";

void win(void) 
{
	system("/bin/sh");
}

void main(void)
{

	char input[50];

	fgets(input, sizeof(input) - 1, stdin);

	if (strlen(input) == strlen(key)) {
		for (int i = 0; i < strlen(key); i++) {
			if ((input[i] ^ 0x30) != key[i]) {
				exit(0);
			}
		}
		system("/bin/sh");
	}
}

