#include <stdio.h>
#include <stdlib.h>

void main(void)
{

	char buf[50];
	int target0;
	int target1;

	puts("This is the only one");

	gets(buf);

	if (target0 == 0xfacade)
	{
		system("/bin/sh");
	}

	if (target1 == 0xfacade)
	{
		system("/bin/sh");
	}
}

