

def cautare(x, L, cmpValori):
    for i in range(len(L) - 1, 0, -1):
        if cmpValori(L[i], x):
            return i


def cmp(x, y):
    return x == y
