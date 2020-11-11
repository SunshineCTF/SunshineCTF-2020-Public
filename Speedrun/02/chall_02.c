#include <stdio.h>
#include <stdlib.h>

void win(void)
{
	system("/bin/sh");
}

void vuln(void)
{
	char buf[50];
	gets(buf);

}

void main(void)
{

	char sample[20];

	puts("Went along the mountain side.");

	fgets(sample, sizeof(sample) - 1, stdin);
	
	vuln();
}
