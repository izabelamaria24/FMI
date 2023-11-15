def len_n(*strings, n):
    return [s for s in strings if len(s) == n]


print(len_n("abc", "adad", "abc", n=3))