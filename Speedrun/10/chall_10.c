#include <stdio.h>
#include <stdlib.h>

void win(int param)
{
	if (param == 0xdeadbeef) {
		system("/bin/sh");
	}
}

void vuln(void)
{
	char buf[50];
	gets(buf);

}

void main(void)
{

	char sample[20];

	puts("Don't waste your time, or...");

	fgets(sample, sizeof(sample) - 1, stdin);
	
	vuln();
}
