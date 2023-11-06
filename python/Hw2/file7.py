
def find_perm(s1, s2):
    dict = {}
    for i in range(len(s1)):
        pos = s2.index(s1[i]) + 1
        dict[i + 1] = pos
        s2.replace(s1[i], '-', 1)

    return dict


string1 = input()
string2 = input()

anagrams = False
if sorted(string1) == sorted(string2):
    anagrams = True

print(list(find_perm(string1, string2).items()))
print(list(find_perm(string2, string1).items()))
