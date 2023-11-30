f = open("cuvinte.txt")
f2 = open("cuv_sortare.txt", "a")

L = f.read().split()

def compareb(item):
    return len(item), item


def comparec(item):
    return len(item)


L.sort(reverse=True)
f2.write(str(L) + '\n')
L.sort(key=compareb)
f2.write(str(L) + '\n')
L.sort(key=comparec)
f2.write(str(L))
