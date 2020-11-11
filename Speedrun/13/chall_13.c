#include <stdio.h>
#include <stdlib.h>

char *binsh = "/bin/sh";

void systemFunc(int param)
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

	puts("Keep on writing");

	fgets(sample, sizeof(sample) - 1, stdin);
	
	vuln();
}
