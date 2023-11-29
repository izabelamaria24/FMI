def generate_matrix(m, n):
    matrix = []
    for i in range(n):
        list = []
        for j in range(m):
            list.append(i + j)
        matrix.append(list)

    return matrix


# O(m*n)
def check1(matrix, x):
    for l in matrix:
        for c in l:
            if matrix[l][c] == x:
                return l, c
    return None


# O(m logn)
def check2(matrix, x):
    for i in range(len(matrix)):
        left = 0
        right = len(matrix[i])
        while left < right:
            mid = (left + right) // 2
            if matrix[i][mid] == x:
                return i, mid
            elif matrix[i][mid] < x:
                left = mid + 1
            else:
                right = mid - 1


# O(m + n)
def check3(matrix, x):
    # bottom left
    curr_line = len(matrix) - 1
    curr_col = 0
    while curr_line >= 0 and curr_col < len(matrix[0]):
        if matrix[curr_line][curr_col] == x:
            return curr_line, curr_col
        elif matrix[curr_line][curr_col] < x:
            curr_col += 1
        else:
            curr_line -= 1
    return None


print(generate_matrix(5, 5))
