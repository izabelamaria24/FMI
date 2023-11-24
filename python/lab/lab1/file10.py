n = int(input())
# 0000000000
subsets = []

for i in range(2 ** n):
    subset = []
    for j in range(n):
        if i & (1 << j):
            subset.append(j + 1)
    subsets.append(subset)

print(subsets)