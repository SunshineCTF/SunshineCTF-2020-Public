#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <inttypes.h>
#include <time.h>

void win(void) 
{
	char out;
	FILE *fp;
	fp = fopen("flag.txt", "rb");

	if (fp == NULL) {
		puts("Could not open flag file.");
		exit(0);
	}

	do
	{
		out = fgetc(fp);
		putchar(out);
	} while (out != EOF);
}

void main(void)
{

	uint32_t x, answer;

	srand(time(0));
	answer = rand();

	scanf("%" SCNd32, &x);
	if (answer == x) {
		win();
	}
	
	else {
		printf("Got: %d\nExpected: %d\n", x, answer);
	}
}

