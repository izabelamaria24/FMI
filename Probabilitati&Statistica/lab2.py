# In cate moduri pot aranja 3 carti pe 2 rafturi? -> nr total de functii, adica 2 la a 3 a
# Aranjam cu repetitie presupune nr de moduri in care aranjez n obiecte in m casute
# In cate moduri pot aranja 3 carti pe 5 rafturi astfel incat sa am cel mult o carte pe raft?
# Raspuns: A de 5 luate cate 3
# In cate moduri pot ocupa 3 rafturi din 5 cu 3 carti, cel mult o carte pe raft?
# Raspuns: functii bijectie: n!

# ex 1
import math

def calculate(lower_chars, upper_chars, digits, password_length):
    # a)
    cnt = pow(lower_chars + upper_chars + digits, password_length)

    # b)
    seconds = cnt / 1000000
    days = math.floor(seconds / 60 / 60 / 24)
    years = days / 365

    # c)
    return 7 / days


result = calculate(26, 26, 10, 8)
result2 = calculate(26, 26, 0, 8)
print(result)

# ex 2
# aranjamente de 62 luate cate 8
def calcul_aranjamente(n, m):
    return math.factorial(n) // math.factorial(n - m)


def calcul_combinari(n, m):
    return math.factorial(n) // (math.factorial(m) * math.factorial(n - m))


def passwords_distinct(lower_chars, upper_chars, digits, password_length):
    total_passwords = pow(lower_chars + upper_chars + digits, password_length)
    
    favorable_passwords1 = calcul_aranjamente((lower_chars + upper_chars + digits), password_length)
    starts_with_digits = digits * (calcul_aranjamente(lower_chars + upper_chars + digits - 1, 7))

    return favorable_passwords1 / total_passwords, (favorable_passwords1 - starts_with_digits) / total_passwords


print(passwords_distinct(26, 26, 10, 8))

# ex 3
def antivirus():
    return calcul_combinari(10, 3)


# ex 4

# a)
# combinari de 52 luate cate 5 -> moduri in care putem extrage orice 5 carti
# combinari de 6 luate cate 3 ori combinari de 17 luate cate 3 supra combinari de 20 luate cate 6

def obtine_calculatoare_reconditionionate(k):
    cazuri_totale = calcul_combinari(20, 6)
    cazuri_favorabile = calcul_combinari(7, k) * calcul_combinari(20 - k, 6 - k)
    
    return cazuri_favorabile / cazuri_totale

# b)

res = 0
nr = 0

for k in range(7):
    if res < obtine_calculatoare_reconditionionate(k):
        res = obtine_calculatoare_reconditionionate(k)
        nr = k

print(f"Cel mai probabil: {nr + 1}")    


# ex 5

# a)
def obtine_3_asi():
    extrageri_totale = calcul_combinari(52, 5)
    cazuri_favorabile = calcul_combinari(48, 2)
    
    return 4 * cazuri_favorabile / extrageri_totale


print(obtine_3_asi())

# b)
# 2 asi

