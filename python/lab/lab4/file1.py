import math

f = open("triplete_pitagoreice.txt", "w")

def ipotenuza(x, y):
    return math.sqrt(x * x + y * y)


b = int(input())
target = b ** 2

for i in range(b):
    c = ipotenuza(i + 1, b)
    if (i + 1) ** 2 + b ** 2 == int(c) ** 2:
        f.write(' '.join(map(str, [i + 1, b, int(c)])) + '\n')

f.close()

# (c - a)(c + a) = b^2 => produsele de 2 numere naturale care sunt egale cu b patrat
# a^2 + b^2 = c^2 => c = ipotenuza(a, b)
