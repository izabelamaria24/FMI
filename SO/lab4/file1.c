#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main()
{
  pid_t pid;

  pid = fork();

  if (pid < 0)
  {
    // fork failed
    return 0;
  }
  
  if (pid == 0)
  {
    // child process 
    char *argv[] = {"ls", NULL};
    execve("/bin/ls", argv, NULL);
    perror(NULL);
  } else  
  {
    printf("My PID = %d, Child PID = %d\n", getpid(), pid);

    wait(NULL);

    printf("Child %d finished\n", pid);
  }
  
  return 0;
}
