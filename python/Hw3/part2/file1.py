def draw_matrix(n):
    m = [(n - 1) * [0] + [1] for i in range(1, n)]
    m.append(n * [1])

    for i in range(n - 2, -1, -1):
        for j in range(n - 2, -1, -1):
            m[i][j] = m[i + 1][j] + m[i][j + 1]
    return m


print(draw_matrix(4))