f = open("punctaje.in", "r")
echipe = {}
nume_echipa_anterior = ""
for linie_fisier in f:
    if linie_fisier.split()[0] == "Echipa":
        nume_echipa = ' '.join([sir for sir in linie_fisier.split() if sir != "Echipa"])
        echipe[nume_echipa] = {}
        nume_echipa_anterior = nume_echipa
    else:
        participant = linie_fisier.split(':')
        echipe[nume_echipa_anterior][participant[0].strip()] = [int(scor) for scor in participant[1].split()]


def functie_sortare(elem):
    return -elem[3], elem[0], elem[1]

def premianti(dict_echipe, *scoruri, k):
    rezultat = []
    lista_scoruri = list(scoruri)

    for key_echipa in dict_echipe:
        for key_participant in dict_echipe[key_echipa]:
            valori = dict_echipe[key_echipa][key_participant]
            A = [val for val in valori if val in lista_scoruri]
            if len(A) >= k:
                rezultat.append((key_echipa, key_participant, sorted(A), round(sum(A) / len(A), 2)))

    return sorted(rezultat, key=functie_sortare)

def stergere(dict_echipe, nume_echipa, nume_membru):
    del dict_echipe[nume_echipa][nume_membru]
    jucatori_ramasi = [nume for nume in dict_echipe[nume_echipa]]
    if len(jucatori_ramasi) == 1:
        del dict_echipe[nume_echipa]
        return f"Am sters jucatorul {nume_membru} si echipa {nume_echipa}"

    return jucatori_ramasi

e = input()
j = input()

print(stergere(echipe, e, j))
print(echipe)