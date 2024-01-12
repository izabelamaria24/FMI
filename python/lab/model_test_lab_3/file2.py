dict_spiridusi = {}
f = open("spiridusi.in", "r")
for line in f:
    nume_spiridus = line.split(':')[0].strip()
    nume_jucarie = line.split(':')[1].split()
    cantitate = int(nume_jucarie[-1])
    nume_jucarie = ' '.join(nume_jucarie[0:-1])

    if nume_spiridus in dict_spiridusi:
        if nume_jucarie in dict_spiridusi[nume_spiridus]:
            dict_spiridusi[nume_spiridus][nume_jucarie] += cantitate
        else:
            dict_spiridusi[nume_spiridus][nume_jucarie] = cantitate
    else:
        dict_spiridusi[nume_spiridus] = {}
        dict_spiridusi[nume_spiridus][nume_jucarie] = cantitate


def cheie_sortare(elem):
    return -len(elem[1]), -elem[2], elem[0]

def top_spiridusi(dic, *nume_spiridusi, nr_minim):
    rezultat = []
    lista_spiridusi = list(nume_spiridusi)
    for spiridus in lista_spiridusi:
        rez_spiridus = []
        cantitate_totala = 0
        for jucarie in dic[spiridus]:
            if dic[spiridus][jucarie] >= nr_minim:
                rez_spiridus.append(jucarie)
                cantitate_totala += dic[spiridus][jucarie]

        if len(rez_spiridus) > 0:
            rezultat.append((spiridus, set(rez_spiridus), cantitate_totala))

    return sorted(rezultat, key=cheie_sortare)

print(top_spiridusi(dict_spiridusi, "Spiridus Harnic", "Spiridus Poznas", "Spiridus Jucaus", nr_minim=2))

def adauga_bucati(dic, nume_spiridus, nume_jucarie="", nrbucati=1):
    if nume_jucarie != "":
        if nume_jucarie in dic[nume_spiridus]:
            dic[nume_spiridus][nume_jucarie] += nrbucati
        else:
            dic[nume_spiridus][nume_jucarie] = nrbucati
    else:
        for jucarie in dic[nume_spiridus]:
            dic[nume_spiridus][jucarie] += nrbucati

    sum_jucarii = 0
    for jucarie in dic[nume_spiridus]:
        sum_jucarii += dic[nume_spiridus][jucarie]

    return sum_jucarii


s = input()
j = input()
print(dict_spiridusi)
print(adauga_bucati(dict_spiridusi, s, j))
print(dict_spiridusi)