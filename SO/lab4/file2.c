#include <stdio.h>
#include <stdlib.h>

void collatz_conjecture(int number)
{
  printf("%d: ", number);
  while (number != 1)
  {
    printf("%d ", number);

    if (number % 2 == 0) number /= 2;
    else number = number * 3 + 1;
  }

  printf("1.\n");
}

int main(int argc, char *argv[])
{
  if (argc != 2) 
  {
    // error
    return 1;
  }
  
  int starting_number = atoi(argv[1]);

  if (starting_number <= 0) 
  {
    printf("The number must be greater than 0");
    return 1;
  }

  pid_t pid;
  pid = fork();

  if (pid < 0)
  {
    printf("Fork failed");
    return 1;
  }

  if (pid == 0)
  {
    // child process
    collatz_conjecture(starting_number);
  } else 
  {
    wait(NULL);
    printf("Child %d finished\n", pid);
  }

  return 0;
}
