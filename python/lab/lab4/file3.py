

def negative_pozitive(numbers):
    return [x for x in numbers if x < 0], [x for x in numbers if x > 0]


file_name = input()
f = open(f"{file_name}.txt", "w")

for x in negative_pozitive([1, 1, -2, -3]):
    f.write(' '.join(map(str, sorted(x))) + '\n')
