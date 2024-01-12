import math


def citire_liste(nume_fisier):
    f = open(nume_fisier, "r")
    n = int(f.readline())
    continut_fisier = []
    rezultat = []

    linie = f.readline()
    while linie != '':
        continut_fisier.append(linie.split())
        linie = f.readline()

    for i in range(n):
        listai = []
        for elem in continut_fisier:
            if int(elem[1]) == i:
                listai.append(int(elem[0]))
        rezultat.append(listai)

    return rezultat


def prelucrare_liste(L, x):
   for i in range(len(L)):
       L[i] = [item for item in L[i] if item != x]

   lista_modificata = []
   for sublista in L:
       if len(sublista) > 1:
           lista_modificata.append(sublista)

   return lista_modificata


lista_rez = prelucrare_liste(citire_liste("liste.in"), 0)
for sublista_rez in lista_rez:
    print(' '.join(map(str, sublista_rez)))

lista = citire_liste("liste.in")
k = int(input())
fw = open("divizori.out", "a")

elem_afisare = []
for sublista in lista:
    for elem in sublista:
        divizori = 0
        for i in range(1, int(math.sqrt(elem)) + 1):
            if elem % i == 0:
                divizori += 2
        if int(math.sqrt(elem)) * int(math.sqrt(elem)) == elem:
            divizori -= 1
        if divizori == k:
            elem_afisare.append(elem)

elem_afisare = set(elem_afisare)
elem_afisare = list(elem_afisare)
elem_afisare.sort(reverse=True)

for elem in elem_afisare:
    fw.write(f'{str(elem)}\n')
