import concurrent.futures
import time

def matrix_mult_worker(args):
    chunk, flat_matrix_a, flat_matrix_b_transposed, num_cols_a, num_cols_b = args
    num_rows_a = len(chunk)
    result = [[0] * num_cols_b for _ in range(num_rows_a)]

    for i, row_idx in enumerate(chunk):
        for j in range(num_cols_b):
            for k in range(num_cols_a):
                result[i][j] += flat_matrix_a[row_idx * num_cols_a + k] * flat_matrix_b_transposed[j * num_cols_a + k]

    return result

def parallel_multiply_matrices(matrix_a, matrix_b):
    n = len(matrix_a)
    num_cols_a = len(matrix_a[0])
    num_cols_b = len(matrix_b[0])
    num_workers = 4  # Chỉ sử dụng 4 lõi CPU

    flat_matrix_a = [elem for row in matrix_a for elem in row]
    flat_matrix_b_transposed = [elem for row in zip(*matrix_b) for elem in row]

    chunk_size = n // num_workers
    chunks = [range(i * chunk_size, (i + 1) * chunk_size) for i in range(num_workers)]

    # Xử lý phần còn lại nếu n không chia hết cho num_workers
    if n % num_workers != 0:
        chunks.append(range(num_workers * chunk_size, n))

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        results = list(executor.map(matrix_mult_worker, [(chunk, flat_matrix_a, flat_matrix_b_transposed, num_cols_a, num_cols_b) for chunk in chunks]))

    matrix_result = []
    for result in results:
        matrix_result += result

    return matrix_result

if __name__ == "__main__":
    n = 1000
    A = [[1] * n for _ in range(n)]
    B = [[2] * n for _ in range(n)]

    start = time.time()
    res = parallel_multiply_matrices(A, B)
    end = time.time()

    print(f"Thời gian tốn: {end - start} giây")
