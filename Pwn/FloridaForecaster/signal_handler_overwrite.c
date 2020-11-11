#include <fcntl.h>
#include <signal.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

char *forecasts[] = {
  "will attack a McDonald's employee for not getting a straw",
  "will crash his lawn mower into a police car and claim the cops poisoned him",
  "will pull a gator from his yoga pants during a traffic stop",
  "will call 911 to report his roommate stole his weed",
  "will be accused of giving beer to an alligator",
  "will find a boa constrictor in his car engine",
  "will find a WWII grenade, put it in his truck, and drive to Taco Bell",
  "will lick a camera-enabled doorbell",
  "will find an iguana in his toilet",
  "will steal $6,000 worth of sunglasses"
};

typedef void (*sighandler_t)(int);

// Kind of brutal. Must send a non-zero byte after overflow, or
// delay gets overwritten to 0 (null-terminated from scanf()).
// alarm(0) will cancel outstanding timers...
struct signal_struct {
  sighandler_t callback;
  unsigned int delay;
};

// Global old handler storage
// Workaround to make a stack address globally available for signal handler
struct signal_struct *old_handler_info;

void win(void) {
  char c = 0;
  int fd;

  if ((fd = open("./flag.txt", O_RDONLY)) == -1) {
    printf("Error opening flag.txt\n");
    exit(1);
  }

  while (read(fd, &c, 1) == 1) {
    printf("%c", c);
  }

  exit(0);
}

void timeout_handler(int num) {
  printf("Hey, you are taking too long\n");
  printf("I'm only going to warn you once...\n");
  // Restore old handler
  // printf("callback: %p\ndelay: %x\n", old_handler_info->callback, old_handler_info->delay);
  signal(SIGALRM, old_handler_info->callback);
  alarm(old_handler_info->delay);
}

void vulnerable_function(void) {
  char buf[100] = {0};
  int number = 0;
  char matched = 0;

  printf("Enter test data\n");
  if (scanf(" %s", buf) != 1) {
    exit(1);
  }

  printf("Received test data: %s\n", buf);
  printf("Does it match (y/n)?\n");

  if (scanf(" %c", &matched) != 1) {
    exit(1);
  }

  if (matched != 'y') {
    printf("Uh-oh! Alert your local data scientist!\n");
    exit(1);
  }

  printf("Program operating normally\n\n");
}

int get_user_int(void) {
  int value = 0;

  if (scanf("%d", &value) != 1) {
    printf("You've lost my trust...\n");
    exit(1);
  }

  return value;
}

void calculate(void) {
  int left = 0;
  int right = 0;
  int result = 0;
  char *prediction = 0;

  printf("Enter first forecast parameter (integer): ");
  left = get_user_int();

  printf("Enter second forecast parameter (integer): ");
  right = get_user_int();

  result = left ^ right;

  // Debug functionality. Leak an address, must calculate addr of win()
  if (left > 0 && right < 0 && result == 0xc0c0c0c0) {
        printf("%p\n", vulnerable_function);
  }
  else {
    prediction = forecasts[result % 10];
    printf("\nA Florida man %s\n\n", prediction);
  }

}

void greet(void) {
  char *frame = "============================";
  printf("%s\n", frame);
  printf("FLORIDA MAN FORECAST MACHINE\n");
  printf("%s\n", frame);
}

void print_help(void) {
  printf("Concerned about how Florida Man might ruin your vacation with his crazy antics?\n\n");
  printf("Our proprietary machine learning wizardry analyzes conditions based on two simple forecast parameters,\n");
  printf("informing you what to expect during your visit to our great state.\n\n");
  printf("If you doubt your forecasts, feel free to run our automated* tests\n");
  printf("\n* Hey, Rob, you automated those tests, right?\n");
}

void prompt(void) {
  printf("1) Help\n");
  printf("2) Test processing unit\n");
  printf("3) Forecast\n");
  printf("4) Exit\n");
  printf("\nChoice: ");
}

int main() {

  struct signal_struct local_signal_struct = {
    .callback = 0,
    .delay = 5,
  };

  char choice = 0;
  
  // Disable buffering, easier to pwntools
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);

  // Setup sighandler to eventually overwrite
  old_handler_info = &local_signal_struct;
  local_signal_struct.callback = signal(SIGALRM, timeout_handler);

  greet();

  while(1) {
    alarm(30);

    prompt();
    if (scanf(" %c", &choice) != 1) {
      exit(1);
    }

    switch(choice) {
      case '1':
        print_help();
        break;

      case '2':
        vulnerable_function();
        break;

      case '3':
        calculate();
        break;

      case '4':
        exit(0);

      default:
        printf("Invalid choice");
        continue;
    }

  };
}
