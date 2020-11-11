#include <stdio.h>
#include <stdlib.h>

void win(void)
{
	system("/bin/sh");
}

void vuln(void)
{
	char buf0[50];
	volatile int (*ptr)();
	char buf1[500];

	fgets(buf0, 100, stdin);

	ptr();
}

void main(void)
{

	char sample[20];

	puts("Like some kind of madness, was taking control.");

	fgets(sample, sizeof(sample) - 1, stdin);
	
	vuln();
}
