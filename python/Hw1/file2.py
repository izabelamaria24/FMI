n = int(input())
numbers = input().split()

# fiecare element apare de un nr par de ori in total (in toate submultimile), deci, aplicand XOR vom obtine 0

if n > 1:
    print(0)
else:
    # daca avem doar un element in sir, rezultatul va fi acel nr (apare de nr impar de ori)
    print(numbers[0])
