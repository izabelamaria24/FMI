#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

#define NTHRS 5

typedef struct
{
  int cnt;
  int max_threads;
  pthread_mutex_t mutex;
  pthread_cond_t cond;
} barrier_t;

barrier_t barrier;

void init_barrier(barrier_t* barrier, int cnt_threads)
{
  barrier->cnt = 0;
  barrier->max_threads = cnt_threads;
  pthread_mutex_t mutex;
  pthread_cond_t cond;
  pthread_mutex_init(&barrier->mutex, NULL);
  pthread_cond_init(&barrier->cond, NULL);
}

void destroy_barrier(barrier_t* barrier)
{
  pthread_mutex_destroy(&barrier->mutex);
  pthread_cond_destroy(&barrier->cond);
}

void barrier_point()
{
  pthread_mutex_lock(&barrier.mutex);
  barrier.cnt++;

  if (barrier.cnt == barrier.max_threads)
  {
    barrier.cnt = 0;
    pthread_cond_broadcast(&barrier.cond);
  } else {
    while (pthread_cond_wait(&barrier.cond, &barrier.mutex) != 0);
  }

  pthread_mutex_unlock(&barrier.mutex);
}

void* tfun(void* arg)
{
  int thread_id = *(int*) arg;
  printf("%d reached the barrier\n", thread_id);
  free(arg);
  barrier_point();
  printf("%d passed the barrier\n", thread_id);
}


int main()
{
  init_barrier(&barrier, NTHRS);
  pthread_t threads[NTHRS];
  for (int i = 0; i < NTHRS; i++)
  {
    int* thread_id = malloc(sizeof(int));
    *thread_id = i;
    pthread_create(&threads[i], NULL, tfun, thread_id);
  }

  for (int i = 0; i < NTHRS; i++)
  {
    pthread_join(threads[i], NULL);
  }

  destroy_barrier(&barrier);

  return 0;
}
