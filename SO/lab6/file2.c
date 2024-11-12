#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>

typedef struct thread_arg
{
  int n, m, p; // the dimensions
  int **A, **B, **C; // the matrices
  int i, j; // the position
} thread_arg;

void* compute_matrix_elem(void *v)
{
  thread_arg* thread_info = (thread_arg*)v;
  int res = 0;
  
  for (int i = 0; i < thread_info->m; i++)
  {
    res += thread_info->A[thread_info->i][i] * thread_info->B[i][thread_info->j];
  }
  
  thread_info->C[thread_info->i][thread_info->j] = res;
  
  return NULL;
}

int main()
{
  int n, m, p;
  printf("Please provide dimensions for the 2 given matrices: (A of size n x m and B of size m * p).");
  scanf("%d %d %d", &n, &m, &p);

  int **A = (int**)malloc(n * sizeof(int*));
  int **B = (int**)malloc(m * sizeof(int*));
  int **C = (int**)malloc(p * sizeof(int*));

  for (int i = 0; i < n; i++)
  {
    A[i] = (int*)malloc(m * sizeof(int));
  }

  for (int i = 0; i < m; i++)
  {
    B[i] = (int*)malloc(p * sizeof(int));
  }

  for (int i = 0; i < n; i++)
  {
    C[i] = (int*)malloc(p * sizeof(int));
  }

  printf("Matrix A (%d x %d): ", n, m);
  for (int i = 0; i < n; i++)
  {
    for (int j = 0; j < m; j++)
    {
      scanf("%d", &A[i][j]);
    }
  }

  printf("Matrix B (%d x %d): ", m, p);
  for (int i = 0; i < m; i++)
  {
    for (int j = 0; j < p; j++)
    {
      scanf("%d", &B[i][j]);
    }
  }

  pthread_t threads[n * p];
  thread_arg threads_data[n * p];

  int cnt = 0;
  for (int i = 0; i < n; i++)
  {
    for (int j = 0; j < p; j++)
    {
      
      threads_data[cnt] = (thread_arg){ .A = A, .B = B, .C = C, .m = m, .n = n, .p = p, .i = i, .j = j };
      if (pthread_create(&threads[cnt], NULL, compute_matrix_elem, &threads_data[cnt]))
      {
        perror("Failed to create thread");
        exit(1);
      }

      cnt++;
    }
  }

  for (int i = 0; i < n * p; i++)
  {
    pthread_join(threads[i], NULL);
  }
  
  printf("Matrix C: \n");
  for (int i = 0; i < n; i++)
  {
    for (int j = 0; j < p; j++)
    {
      printf("%d ", C[i][j]);
    }
    printf("\n");
  }
  
  for (int i = 0; i < n; i++)
  {
    free(A[i]);
    free(C[i]);
  }
  for (int i = 0; i < m; i++)
  {
    free(B[i]);
  }

  free(A);
  free(B);
  free(C);

  return 0;
}
