from concurrent.futures import ThreadPoolExecutor
import time

def parallel_prefix_sum(matrix_a):
    rows = len(matrix_a)
    cols = len(matrix_a[0])
    
    # Initialize the result matrix with zeros
    result = [[0] * cols for _ in range(rows)]
    
    # Function to compute prefix sum for a single row
    def compute_row_prefix_sum(row):
        result[row][0] = matrix_a[row][0]
        for col in range(1, cols):
            result[row][col] = result[row][col-1] + matrix_a[row][col]
    
    # Use ThreadPoolExecutor to parallelize row computations
    with ThreadPoolExecutor(max_workers=min(32, rows)) as executor:
        executor.map(compute_row_prefix_sum, range(rows))
    
    return result

# Example matrix
matrix_a = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]

start_time = time.time()

# Compute the parallel prefix sum
prefix_sum_matrix = parallel_prefix_sum(matrix_a)

end_time = time.time()

# Print the result
print(prefix_sum_matrix)
print("Time:", end_time - start_time)
