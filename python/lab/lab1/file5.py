a = int(input())
b = int(input())

fib1 = 1
fib2 = 1
while fib2 < a:
    aux = fib2
    fib2 += fib1
    fib1 = aux

print(fib2)