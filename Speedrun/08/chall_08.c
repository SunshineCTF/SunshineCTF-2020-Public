#include <stdio.h>
#include <stdlib.h>

long target[10];

void win(void) 
{
	system("/bin/sh");
}

void main(void)
{

	int idx;
	long value;

	scanf("%d", &idx);
	scanf("%ld", &value);
	
	target[idx] = value;

	puts("hi");

}

