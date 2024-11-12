#include <stdio.h>
#include <string.h>
#include <pthread.h>
#include <errno.h>

void* hello(void* v)
{
  char *str = (char*)v;
  int length = strlen(str);

  for (int i = 0; i < length / 2; i++)
  {
    char temp = str[i];
    str[i] = str[length - i - 1];
    str[length - i - 1] = temp;
  }

  return (void*)str;
}

int main(int argc, char* argv[])
{

    if (argc < 2) return 0;

    char* str = argv[1];

    pthread_t thr;
    if (pthread_create(&thr, NULL, hello, (void*)str))
    {
      perror(NULL);
      return errno;
    }
    
    void* res;
    if (pthread_join(thr, &res))
    {
      perror(NULL);
      return errno;
    }

    printf("Inverted string: %s\n", (char*)res);

    return 0;
}
