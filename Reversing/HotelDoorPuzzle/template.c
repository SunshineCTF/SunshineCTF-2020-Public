#include <stdio.h>
#include <string.h>

int check_flag(char *flag)
{
  {% for line in check_code %}
  {{ line }}
  {% endfor %}
  return 1;
}

int main(void){
  printf("Hotel Orlando Door Puzzle v1\n");
  printf("----------------------------\n");
  printf("This puzzle, provided by Hotel Orlando, is in place to give the bellhops enough time to get your luggage to you.\n");
  printf("We have really slow bellhops and so we had to put a serious _time sink_ in front of you.\n");
  printf("Have fun with this puzzle while we get your luggage to you!\n");
  printf("\n\t-Hotel Orlando Bellhop and Stalling Service\n\n");
  char user_input[60];

  puts("Your guess, if you would be so kind: ");
  fscanf(stdin, "%60s", user_input);

  if(check_flag(user_input) == 1)
  {
    puts("I see you found the key, hopefully your bags are in your room by this point.");
  }
  else
  {
    puts("Sadly, that is the incorrect key. If you would like, you could also sit in our lobby and wait.");
  }
}
