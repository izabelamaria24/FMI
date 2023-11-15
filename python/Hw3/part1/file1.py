def draw_matrix(n):
    m = [[i] + (i - 1) * [0] for i in range(1, n)]
    m.append([i for i in range(n, 0, -1)])

    for i in range(n - 2, 0, -1):
        for j in range(1, i + 1):
            m[i][j] = m[i + 1][j] + m[i + 1][j - 1] + m[i][j - 1]

    return m


def draw_matrix_right(m):
    max_cnt = max([len(str(max(line))) for line in m])

    for line in m:
        for elem in line:
            print(str(elem).rjust(max_cnt), end=' ')
        print()


size = int(input())
print(draw_matrix(size))
print(draw_matrix_right(draw_matrix(size)))
