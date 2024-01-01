n = int(input())
s = int(input())
A = [int(k) for k in input().split()]

def backtrack(ind, currSum, result):
    for i in range(ind, n):
        if currSum + A[i] < s:
            result.append(A[i])
            backtrack(i + 1, currSum + A[i], result)
            result.pop()
        elif currSum + A[i] == s:
            result.append(A[i])
            print(result, sep='\n')
            result.pop()

backtrack(0, 0, [])
