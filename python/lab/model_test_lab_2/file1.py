def citire_siruri(nume_fisier):
    f = open(nume_fisier, "r")
    lista = []
    for line in f:
        lista.append(line.split())
    return lista


def nr_vocale(str):
    vocale = "aeiouAEIOU"
    cnt = 0
    for ch in str:
        if ch in vocale:
            cnt += 1

    return cnt


def prelucrare_siruri(L, n):
    for lista in L:
        cuv = ""
        for cuvant in lista:
            cuv += cuvant[-1]
        lista.append(cuv)

    for i in range(len(L)):
        L[i] = [item for item in L[i] if nr_vocale(item) >= n]

    return L


lista_prelucrata = prelucrare_siruri(citire_siruri("cuvinte.in"), 3)
for lista in lista_prelucrata:
    print(' '.join(lista))


w = input()
fw = open("cuvinte.out", "a")
exista = False


set_cuvinte = []
for lista in citire_siruri("cuvinte.in"):
    for cuv in lista:
        if w in cuv:
            set_cuvinte.append(cuv)
            exista = True

set_cuvinte = set(set_cuvinte)
lista_cuvinte = list(set_cuvinte)
lista_cuvinte.sort()

if not exista:
    fw.write("Imposibil!")
else:
    fw.write(' '.join(lista_cuvinte))