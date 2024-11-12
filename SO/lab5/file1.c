#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <sys/wait.h>

void collatz_conjecture(int start, int *collatz_arr)
{
  int cnt = 0;
  collatz_arr[cnt++] = start;
  while (start != 1) 
  {
    if (start % 2 == 0) start /= 2;
    else start = start * 3 + 1;
    collatz_arr[cnt++] = start;
  }

  collatz_arr[cnt] = -1;
}

int main(int argc, char *argv[])
{
  pid_t pid;

  // shared memory
  const char* shm_name = "collatz";
  int shm_fd;
  shm_fd = shm_open(shm_name, O_CREAT|O_RDWR, S_IRUSR|S_IWUSR);
  if (shm_fd < 0)
  {
    // shared memory failed to be created
    perror(NULL);
    return errno;
  }
  
  const int page_size = 4096;
  size_t shm_size = page_size * (argc - 1);
  if (ftruncate(shm_fd, shm_size) == -1)
  {
    perror(NULL);
    shm_unlink(shm_name);
    return errno;
  }

  // the shared memory pointer starts at byte 0 and points to the
  // entire memory zone
  printf("Starting parent %d\n", getpid());  
  for (int i = 1; i < argc; i++)
  {
    pid = fork();

    if (pid < 0)
    {
      // error -> fork failed
      return 0;
    }

    if (pid == 0)
    {
      // child process
      
      void* shm_ptr = mmap(0, page_size, PROT_WRITE, MAP_SHARED, shm_fd, 
                          page_size * (i - 1));
      if (shm_ptr == MAP_FAILED)
      {
        perror("mmap in child process");
        return errno;
      }
      
      int *collatz_arr = (int *)shm_ptr;
      collatz_conjecture(atoi(argv[i]), collatz_arr);

      munmap(shm_ptr, page_size);

      printf("Done Parent %d Me %d \n", getppid(), getpid());
      return 0;
    }
  }

  for (int i = 1; i < argc; i++)
  {
    // wait for all child processes to finish
    wait(NULL);
  }

  // after all child processes finished, read from the shared memory object and print the results
  //
  void* shm_ptr = mmap(0, shm_size, PROT_READ, MAP_SHARED, shm_fd, 0);
  if (shm_ptr == MAP_FAILED)
  {
    perror("mmap in parent");
    return errno;
  }

  for (int i = 1; i < argc; i++)
  {
    int cnt = 0;
    int *arr = (int *)((char*)shm_ptr + page_size * (i - 1));
    
    printf("%d:", atoi(argv[i]));

    while (arr[cnt] != -1)
    {
      printf(" %d", arr[cnt]);
      cnt++;
    }

    printf(".\n");
  }
  
  munmap(shm_ptr, shm_size);
  shm_unlink(shm_name);
  printf("Done Parent %d Me %d \n", getppid(), getpid());
  return 0;
}
