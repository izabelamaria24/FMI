# a
def citire_numere(nume_fisier):
    f = open(nume_fisier)
    L = []
    for line in f:
        L.append([int(x) for x in line.split()])
    return L


# b
def prelucrare_lista(L):
    for list in L:
        minimum = min(list)
        while minimum in list:
            list.remove(minimum)

    lengths = [len(list) for list in L]
    m = min(lengths)

    L = [list[:m] for list in L]
    return L

# c
matrix = citire_numere("numere.in")
print(prelucrare_lista(matrix))


# d
k = int(input())
fw = open("cifre.out", "a")

res_k = []
for line in matrix:
    for elem in line:
        if len(str(elem)) == k:
            res_k.append(elem)

res_k = sorted(set(res_k), reverse=True)

if not res_k:
    fw.write("Imposibil!")
else:
    fw.write(str(res_k))
