#include <stdio.h>
#include <stdlib.h>

void win(int param)
{
	system("/bin/sh");
}

void vuln(void)
{
	char buf[200];

	fgets(buf, sizeof(buf) - 1, stdin);

	printf(buf);

	fflush(stdin);
}

void main(void)
{

	char sample[20];

	printf("So indeed \n");

	fgets(sample, sizeof(sample) - 1, stdin);

	vuln();
}
