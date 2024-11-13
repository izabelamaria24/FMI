#include <stdio.h>
#include <pthread.h>
#include <time.h>
#include <stdlib.h>

#define MAX_RESOURCES 5
int available_resources = MAX_RESOURCES;
pthread_mutex_t mutex;

int decrease_count(int count)
{
  pthread_mutex_lock(&mutex);
  if (available_resources < count)
  {
    pthread_mutex_unlock(&mutex);
    return -1;
  } else 
  {
    available_resources -= count;
    printf("Got %d resources %d remaining\n", count, available_resources);
  }
  pthread_mutex_unlock(&mutex);
  return 0;
}

int increase_count(int count)
{
  pthread_mutex_lock(&mutex);
  available_resources += count;
  printf("Released %d resources %d remaining\n", count, available_resources);
  pthread_mutex_unlock(&mutex);
  return 0;
}

void* thread_func(void* arg)
{
  int thread_id = *(int*)arg;

  int cnt_requested_resources = (rand() % MAX_RESOURCES) + 1;
  free(arg);

  if (decrease_count(cnt_requested_resources) == 0)
  {
    increase_count(cnt_requested_resources);
  }
  return NULL;
}

int main()
{
  srand(time(NULL));
  pthread_mutex_init(&mutex, NULL);
  int num_threads = 10;
  pthread_t threads[num_threads];

  for (int i = 0; i < num_threads; i++)
  {
    int* thread_id = malloc(sizeof(int));
    *thread_id = i;

    pthread_create(&threads[i], NULL, thread_func, thread_id);
  }

  for (int i = 0; i < num_threads; i++)
  {
    pthread_join(threads[i], NULL);
  }

  pthread_mutex_destroy(&mutex);
  
  return 0;
}
