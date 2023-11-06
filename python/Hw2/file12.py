text = input()

uppercase = lowercase = sep = 0
for ch in text:
    if ch.isupper():
        uppercase += 1
    elif ch.islower():
        lowercase += 1
    elif not ch.isdigit():
        sep += 1

print(uppercase, lowercase, sep)
