numbers = []


def citire_lista():
    global numbers
    numbers = [int(x) for x in input().split()]


def func1(x, i, j):
    for cnt in range(i, j):
        if numbers[cnt] > x:
            return cnt
    return -1


def is_sorted():
    for it in range(len(numbers)):
        res = func1(numbers[it], it + 1, len(numbers))
        if res != -1:
            return False
    return True


citire_lista()
if is_sorted():
    print("Da")
else:
    print("Nu")
