n = input()

max_res = ''.join(sorted(n, reverse=True))
min_res = sorted(n)

cnt = 0
while min_res[cnt] == '0':
    cnt += 1

min_res[0], min_res[cnt] = min_res[cnt], min_res[0]
min_res = ''.join(min_res)

print(max_res, min_res)
