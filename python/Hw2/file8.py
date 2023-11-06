import re

with open("exemplu.txt", "r+") as file:
    text = file.read()
    # split words
    words = re.split(r'[,\s;:.! ?]+', text)
    words = [word for word in words if word]

    dict = {}
    for w in words:
        l = len(w)
        if l not in dict:
            dict[l] = []
        dict[l].append(w)

    sorted_items = sorted(dict.items(), reverse=True)

    print(sorted_items)
    sorted_dict = {}

    for key, value in sorted_items:
        sorted_dict[key] = sorted(value)

    with open("grupe_cuvinte.txt", "w") as output:
        print(sorted_dict, file=output)
