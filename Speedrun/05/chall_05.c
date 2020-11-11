#include <stdio.h>
#include <stdlib.h>

void win(void)
{
	system("/bin/sh");
}

void main(void)
{

	char sample[20];

	puts("Race, life's greatest.");

	fgets(sample, sizeof(sample) - 1, stdin);
	
	vuln();
}

void vuln(void)
{
	char buf0[50];
	volatile int (*ptr)();
	char buf1[500];

	printf("Yes I'm going to win: %p\n", main);

	fgets(buf0, 100, stdin);

	ptr();
}

