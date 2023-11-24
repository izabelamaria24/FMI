n = int(input())
numbers = [int(x) for x in input().split()]
perm = [i + 1 for i in range(n)]

res = 0
for x in numbers:
    res ^= x
for x in perm:
    res ^= x

print(res)