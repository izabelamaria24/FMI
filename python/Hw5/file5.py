n = int(input())
A = [int(k) for k in input().split()]

def generate_subsets(cnt, result):
    if len(result) > 0:
        print(result)

    for i in range(cnt, n):
        if (not result or result[-1] < A[i]):
            result.append(A[i])
            generate_subsets(i + 1, result)
            result.pop()


generate_subsets(0, [])
