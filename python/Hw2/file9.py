# method 1

with open("numere.txt", "r+") as file:
    numbers = file.read().split()
    digits = []
    for number in numbers:
        digits += [digit for digit in number]

    digits.sort()

    for i in range(len(digits)):
        if digits[i] != '0':
            digits[i], digits[0] = digits[0], digits[i]
            break

    resultMin = ''.join(digits)

    digits.sort(reverse=True)
    resultMax = ''.join(digits)

    print(resultMin, resultMax)
