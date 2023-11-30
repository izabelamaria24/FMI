def func1(k):
    def callb(x):
        return x < k
    return callb


kfunct = func1(6)
print(kfunct(3))


L = [5, 4, 3, 2, 1]
for i in range(len(L) - 1):
    ifunct = func1(L[i])
    for j in range(i + 1, len(L)):
        if ifunct(L[j]):
            L[i], L[j] = L[j], L[i]

print(L)
