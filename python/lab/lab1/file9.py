n = int(input())
k = int(input())
b = int(input())

aux = n & (1 << (k - 1))

# daca n are bit 0 pe pozitia k
if aux == 0:
    if b == 1:
        print(n ^ (1 << (k - 1)))
    else:
        print(n)
else:
    if b == 1:
        print(n)
    else:
        print(n ^ (1 << (k - 1)))
