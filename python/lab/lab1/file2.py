n = int(input())
curs_valutar = [float(x) for x in input().split()]

res = 0
for i in range(n - 1):
    res = max(res, abs(curs_valutar[i + 1] - curs_valutar[i]))

print(res)
