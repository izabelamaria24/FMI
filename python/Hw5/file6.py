n = int(input())
A = [int(k) for k in input().split()]

dp = [0 for i in range(n)]

dp[0] = 1
for i in range(1, n):
    for j in range(i):
        if A[i] > A[j]:
            dp[i] = max(dp[i], dp[j] + 1)

print(max(dp))
