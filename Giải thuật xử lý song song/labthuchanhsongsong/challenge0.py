from concurrent.futures import ThreadPoolExecutor

def parallel_prefix_sum(matrix_a):
    rows = len(matrix_a)
    cols = len(matrix_a[0])
    result = [[0] * cols for _ in range(rows)]

    def compute_column_prefix_sum(col):
        result[0][col] = matrix_a[0][col]
        for i in range(1, rows):
            result[i][col] = result[i - 1][col] + matrix_a[i][col]

    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(compute_column_prefix_sum, range(cols))

    for row in result:
        for j in range(1, cols):
            row[j] += row[j - 1]

    return result

matrix_a = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

prefix_sum_matrix = parallel_prefix_sum(matrix_a)