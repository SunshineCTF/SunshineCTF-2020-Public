#include <stdio.h>
#include <stdlib.h>

void main(void)
{
	char buf0[20];
	char input[200];

	printf("In the land of raw humanity");
	fgets(buf0, sizeof(buf0) - 1, stdin);

	fgets(input, sizeof(input), stdin);
	(*(void (*)()) input)();
}
