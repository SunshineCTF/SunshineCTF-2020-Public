#include <stdio.h>
#include <stdlib.h>

void vuln(void)
{
	char buf[100];

	printf("I'll make it: %p\n", buf);

	gets(buf);

}

void main(void)
{

	char sample[20];

	puts("Just in time.");

	fgets(sample, sizeof(sample) - 1, stdin);
	
	vuln();
}
