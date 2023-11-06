numbers = input().split()

result = 0
for x in numbers:
    result = result ^ int(x)

print(result)