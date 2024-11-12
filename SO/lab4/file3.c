#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/wait.h>

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
  if (argc < 2)
  {
    // error
    return 1;
  }

  // no of arguments - argc - 1
  pid_t pid;
  printf("Starting parent %d\n", getpid());

  for (int i = 1; i < argc; i++)
  {
    int current_number = atoi(argv[i]);
    
    pid = fork();

    if (pid < 0)
    {
      printf("Fork failed");
      return 1;
    } 

    if (pid == 0)
    {
      collatz_conjecture(current_number);
      printf("Done Parent %d Me %d\n", getppid(), getpid());
      return 0;
    } 
  }

  for (int i = 1; i < argc; i++)
  {
    wait(NULL);
  }

  printf("Done Parent %d Me %d\n", getppid(), getpid());

  return 0;
}
