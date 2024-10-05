import numpy as np
import time
import concurrent.futures
import multiprocessing

def cal_cell(current_row, current_col, matrix_a, matrix_b):
    return np.dot(matrix_a[current_row, :], matrix_b[:, current_col])
def cal_value(current_row, matrix_a, matrix_b, matrix_temp, row_offset):
    for current_col in range(matrix_b.shape[1]):
        matrix_temp[current_row - row_offset, current_col] = cal_cell(current_row, current_col, matrix_a, matrix_b)
def cal_sub_matrices(args):
    chunk, matrix_a, matrix_b = args
    matrix_temp = np.zeros((len(chunk), matrix_b.shape[1]))
    row_offset = chunk[0]
    for current_row in chunk:
        cal_value(current_row, matrix_a, matrix_b, matrix_temp, row_offset)
    return chunk[0], matrix_temp
def parallel_multiply_matrices(matrix_a, matrix_b):
    n = len(matrix_a)
    result_matrix = np.zeros((n, n))
    chunks = np.array_split(range(n), multiprocessing.cpu_count())  
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(cal_sub_matrices, (chunk, matrix_a, matrix_b)) for chunk in chunks]
        for future in concurrent.futures.as_completed(futures):
            start_idx, sub_matrix = future.result()
            result_matrix[start_idx:start_idx + sub_matrix.shape[0], :] = sub_matrix
    return result_matrix

if __name__ == "__main__":
    n = 10
    A = np.random.randint(1, 10, size=(n, n)).astype(np.int32)
    B = np.random.randint(1, 10, size=(n, n)).astype(np.int32)
    
    start = time.time()
    res = parallel_multiply_matrices(A, B)
    end = time.time()
    
    print(res)
    print(f"Time taken: {end - start}")
    
    res1 = np.dot(A, B)
    print(res1)
    
    if np.array_equal(res, res1):
        print("The matrices are equal.")
    else:
        print("The matrices are not equal.")
