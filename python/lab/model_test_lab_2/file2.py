f = open("concurs.in", "r")
concurenti = {}
concurent_anterior = ""

for line in f:
    if len(line.split()) == 1:
        concurenti[line.split()[0]] = {}
        concurent_anterior = line.split()[0]
    else:
        proba = line.split()[0]
        scoruri = line.split()[1:]
        concurenti[concurent_anterior][proba] = [float(scor) for scor in scoruri]


def cheie_sortare(elem):
    return elem[0], -elem[2], elem[1]


def rezultate(dict_concurenti, *nume_probe, n):
    probe = list(nume_probe)
    rezultat = []
    for key in dict_concurenti:
        for prob in probe:
            if prob in dict_concurenti[key]:
                if len(dict_concurenti[key][prob]) >= n:
                    dict_concurenti[key][prob].sort()
                    dict_concurenti[key][prob] = dict_concurenti[key][prob][1:-1]
                    rezultat.append((prob, key, round(sum(dict_concurenti[key][prob])
                                                      / len(dict_concurenti[key][prob]), 2),
                                     sorted(dict_concurenti[key][prob], reverse=True)))

    return sorted(rezultat, key=cheie_sortare)


print(rezultate(concurenti, 'trambulina', 'greutati', n=5))


def adaugare(dict_concurenti, nume_proba, nume_concurent, lista_nr):
    if nume_concurent not in dict_concurenti:
        return "Numele probei sau al concurentului nu exista!"
    else:
        exista = False
        for key in dict_concurenti:
            if nume_proba in dict_concurenti[key]:
                exista = True
                break
        if not exista:
            return "Numele probei sau al concurentului nu exista!"
        if nume_proba not in dict_concurenti[nume_concurent]:
            dict_concurenti[nume_concurent][nume_proba] = lista_nr
        else:
            dict_concurenti[nume_concurent][nume_proba].extend(lista_nr)

    return len(dict_concurenti[nume_concurent][nume_proba])


p = input()
c = input()
values = [float(val) for val in input().split()]
print(adaugare(concurenti, p, c, values))
print(concurenti)
