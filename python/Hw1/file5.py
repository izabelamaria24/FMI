import math

n = int(input())
mb = (1 << (1 + int(math.log(n, 2)))) - 1

complement = n ^ mb

result = 0
while complement > 0:
    if complement & 1:
        result += 1
    complement >>= 1

print(result)
