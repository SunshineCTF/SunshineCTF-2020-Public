#include <stdio.h>
#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <errno.h>
#include <unistd.h>
#include <fcntl.h>
#include <endian.h>
#include <time.h>


char g_password[50];

static void write_all(int fd, const void* data, size_t size) {
	const char* p = data;
	size_t to_write = size;
	
	while (to_write != 0) {
		ssize_t bytes_written = write(fd, p, to_write);
		if (bytes_written <= 0) {
			exit(EXIT_FAILURE);
		}
		
		to_write -= bytes_written;
		p += bytes_written;
	}
}

static void write_str(int fd, const char* str) {
	write_all(fd, str, strlen(str));
}

static void print_str(const char* str) {
	write_str(STDOUT_FILENO, str);
}

static void load_password(void) {
	int fd = open("/dev/urandom", O_RDONLY);
	
	unsigned i;
	for(i = 0; i < sizeof(g_password) - 1; i++) {
		while(g_password[i] == '\0') {
			if(read(fd, &g_password[i], 1) != 1) {
				abort();
			}
			g_password[i] &= 0x7f;
		}
	}
	close(fd);
	
	g_password[sizeof(g_password) - 1] = '\0';
}

static int memcmp_timesafe(const char* a, const char* b, size_t size) {
	if(size == 0) {
		return 0;
	}
	
	int diff = 0;
	while(size--) {
		diff |= *b++ - *a++;
	}
	return diff;
}

static bool try_login(void) {
	print_str("USER\n");
	
	struct {
		char username[16];
		char* password;
	} cheeky = {
		.username = {0},
		.password = g_password
	};
	
	read(STDIN_FILENO, &cheeky.username, sizeof(cheeky.username));
	if(strcmp(cheeky.username, "admin") != 0) {
		print_str("BAD USER ");
		print_str(cheeky.username);
		print_str("\n");
		return false;
	}
	
	print_str("PASSWORD\n");
	
	uint64_t size = 0;
	read(STDIN_FILENO, &size, sizeof(size));
	size = be64toh(size);
	
	char* buffer = malloc(size + 1);
	read(STDIN_FILENO, buffer, size);
	
	buffer[size] = '\0';
	
	if(memcmp_timesafe(cheeky.password, buffer, strlen(cheeky.password)) == 0) {
		print_str("LOGIN SUCCESS\n");
		return true;
	}
	else {
		print_str("LOGIN FAIL\n");
		exit(EXIT_FAILURE);
	}
}

static void give_flag(void) {
	char flag[100] = {0};
	int fd = open("flag.txt", O_RDONLY);
	read(fd, flag, sizeof(flag) - 1);
	close(fd);
	
	print_str("FLAG ");
	print_str(flag);
	
	if(flag[strlen(flag) - 1] != '\n') {
		print_str("\n");
	}
	
	print_str("CONFIRM\n");
	char c = '\0';
	
	while(c != 'y') {
		if(read(STDIN_FILENO, &c, sizeof(c)) != sizeof(c)) {
			break;
		}
	}
}

int main(void) {
	load_password();
	
	print_str("HELLO\n");
	print_str("SERVER sunshine.space.center.local\n");
	
	int attempts = 3;
	while(attempts-- > 0) {
		if(try_login()) {
			give_flag();
			usleep(1000 * 100);
			return 0;
		}
		
		print_str("AGAIN\n");
	}
	
	print_str("LOCKOUT\n");
	return 0;
}
