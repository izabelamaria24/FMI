import re

text = input()
words = re.split(r'[\s,.!:;?]', text)
words = [word for word in words if word]

dict = {}
cnt = 0
for word in words:
    if word not in dict:
        cnt += 1
    dict[word] = 1

print(cnt)
