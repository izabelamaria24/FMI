n = int(input())

if not n:  # daca n e 0, afisam 2 la puterea 0
    print(1)
    exit()

if not (n & (n-1)):  # daca n e deja putere de 2, returnam n
    print(n)
    exit()

msb = 0  # cel mai semnificativ bit
while n > 0:
    msb += 1
    n >>= 1

print(1 << msb)
