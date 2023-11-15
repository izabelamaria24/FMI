import math


def count(coll, prop):
    return len([value for value in coll if prop(value)])


def prop_1(val):
    return val % 2 == 0


def prop_2(val):
    return val in "aeiouAEIOU"


def prop_3(val):
    return val[0] == val[1]


def prop_4(k):
    def aux(item):
        return len(item) == k
    return aux


def prop_5(y, t):
    def check_gcd(item):
        return math.gcd(item, y) == t
    return check_gcd
