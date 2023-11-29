# files, input
pairs = []
f = open("autostrada.in")
fw = open("autostrada.out", "a")
highway_length = int(f.readline())
for line in f:
    pairs.append([int(x) for x in line.split()])

# a
pairs.sort(key=lambda x: x[0])

reunion = []
cnt = -1
for inf in pairs:
    if len(reunion) > 0:
        if inf[0] <= reunion[cnt][1]:
            reunion[cnt][1] = max(reunion[cnt][1], inf[1])
        else:
            cnt += 1
            reunion.append(inf)
    else:
        cnt += 1
        reunion.append(inf)

for item in reunion:
    fw.write(str(item) + '\n')
fw.write('\n')

# b
open_intervals = []
left = 0
right = 0
for interval in reunion:
    right = interval[0]
    open_intervals.append((left, right))
    left = interval[1]

open_intervals.append((left, highway_length))

for item in open_intervals:
    fw.write(str(item) + '\n')
fw.write('\n')

# c
total = 0
for interval in reunion:
    total += interval[1] - interval[0]

fw.write(f"{int(total / highway_length * 100)}%")
