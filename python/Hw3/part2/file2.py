import string


def gen_funct(coll, prop):
    res = []

    for i in range(len(coll)):
        if prop(coll[i]) is True:
            res.append(i)

    return res


def prop_1(val):
    return val > 0


def prop_2(ch):
    return ch in string.punctuation


def prop_3(s):
    def aux(x):
        return sorted(x) == sorted(s)
    return aux


def prop_4(n, s):
    def cnt_digits(number):
        return len(str(number)) == n and sum([int(ch) for ch in str(number)]) == s
    return cnt_digits


print(gen_funct([1213, 123, 1234, 1213], prop_4(4,7)))
