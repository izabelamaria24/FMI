# a
f = open("cinema.in")
movies = {}
for line in f:
    format_line = line.rstrip('\n').split(' % ')
    item = {"film": format_line[1], "time": {"h": format_line[2].split(":")[0], "m": format_line[2].split(":")[1]}}
    if format_line[0] in movies:
        movies[format_line[0]].append(item)
    else:
        movies[format_line[0]] = [item]


# b
def sterge_ore(movies_list, cinema, film, ore):
    for item in movies_list[cinema]:
        if item['film'] == film and item['time']['h'] + ':' + item['time']['m'] in ore:
            movies_list[cinema].remove(item)

    return movies_list


nume_film = input()
nume_cinema = input()
ora = input()
print(sterge_ore(movies, nume_cinema, nume_film, {ora}))


# c
def cinema_film(movies_list, *cinematografe, ora_minima, ora_maxima):
    
