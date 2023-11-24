n = int(input())
numbers = [int(x) for x in input().split()]

min_res = numbers[0]
max_res = numbers[0]

for i in range(n//2 + 1):
    if numbers[i] < numbers[n - i - 1]:
        min_res = min(min_res, numbers[i])
        max_res = max(max_res, numbers[n - i - 1])
    print(i)

print(min_res, max_res)
