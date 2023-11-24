import math


L1 = int(input())
L2 = int(input())

side = math.gcd(L1, L2)
print(side, int((L1 * L2) / (side * side)))