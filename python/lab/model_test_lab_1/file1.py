
import math

def citire_matrice(nume_fisier):
    f = open(nume_fisier, "r")
    n = int(f.readline())
    matrice = []
    linie = int(math.sqrt(n))
    for i in range(linie):
        res = []
        for j in range(linie):
            res.append(int(f.readline()))
        matrice.append(res)

    return matrice


def prelucrare_matrice(matrice):
    for i in range(len(matrice)):
        for j in range(len(matrice)):
            if i != j:
                matrice[i][j] -= matrice[i][i]

    matrice_modificata = []
    for i in range(len(matrice)):
        matrice_modificata.append([matrice[i][j] for j in range(len(matrice)) if j != i])

    return matrice_modificata


rezultat = prelucrare_matrice(citire_matrice("matrice.in"))
for line in rezultat:
    print(' '.join(map(str, line)))

M = citire_matrice("matrice.in")
k = int(input())
fw = open("numere.out", "a")

elemente = []
for linie in M:
    elemente.extend([coloana for coloana in linie if sum([int(c) for c in str(coloana)]) == k])

elemente.sort()
print(' '.join(map(str, elemente)))
