# nr de aparitii ale unei valori intr o lista sortata crescator
list = [int(item) for item in input().split()]
x = int(input())

def search_occ(list, value, type):
    l = 0
    r = len(list) - 1
    res = -1
    while l <= r:
        m = (l + r) // 2
        if value > list[m]:
            l = m + 1
        elif value < list[m]:
            r = m - 1
        else:
            res = m
            if type == 0: # first occ
                r = m - 1
            else:
                l = m + 1 # last occ

    return res

first_occ = search_occ(list, x, 0)
last_occ = search_occ(list, x, 1)

if first_occ != -1 and last_occ != -1:
    print(last_occ - first_occ + 1)
else:
    print(f"value {x} not found in the provided list")