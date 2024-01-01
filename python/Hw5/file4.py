n = int(input())
s = int(input())
A = [int(k) for k in input().split()]
dp = [[0 for i in range(0, s + 1)] for j in range(0, n + 1)]

for i in range(n + 1):
    dp[i][0] = 1

for i in range(1, n + 1):
    for j in range(1, s + 1):
        if j < A[i - 1]:
            dp[i][j] = dp[i - 1][j]
        else:
            dp[i][j] = dp[i - 1][j - A[i - 1]] + dp[i - 1][j]

result = []
line = n
col = s
while line > 0 and col > 0:
    if dp[line - 1][col]:
        line -= 1
    else:
        result.append(A[line - 1])
        line -= 1
        col -= A[line - 1]

print(result[::-1])
