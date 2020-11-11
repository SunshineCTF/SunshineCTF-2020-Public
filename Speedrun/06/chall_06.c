#include <stdio.h>
#include <stdlib.h>

void main(void)
{

	char sample[200];

	printf("Letting my armor fall again: %p\n", sample);

	fgets(sample, sizeof(sample) - 1, stdin);
	
	vuln();
}

void vuln(void)
{
	char buf0[50];
	volatile int (*ptr)();
	char buf1[500];

	puts("For saving me from all they've taken.");

	fgets(buf0, 100, stdin);

	ptr();
}

