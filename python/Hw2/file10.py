w = input()
wordsList = input().split()

for word in wordsList:
    if len(word) == len(w):
        print(f"{word}  ")
