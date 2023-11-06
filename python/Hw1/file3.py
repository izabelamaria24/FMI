x = int(input())
y = int(input())

xorResult = x ^ y
bitsOfOne = 0

while xorResult > 0:
    bitsOfOne += xorResult & 1
    xorResult >>= 1

print(bitsOfOne)
