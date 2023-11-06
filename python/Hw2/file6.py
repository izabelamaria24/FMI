
# compare sorted lists of characters
string1 = input()
string2 = input()

if len(string1) != len(string2):
    print('NU')
    exit(0)

# print(sorted(string1))

if sorted(string1) == sorted(string2):
    print('Anagrame')
else:
    print('NU')
