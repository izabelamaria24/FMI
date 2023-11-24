n = int(input())
numbers = [int(x) for x in input().split()]

res = 0
for x in numbers:
    res ^= x

print(res)
