import concurrent.futures
import random

def parallel_reduce(A, start, end):
    if start == end:
        return A[start]
    else:
        mid = int((start + end + 1) / 2)
        left_result = parallel_reduce(A, start, mid - 1)
        right_result = parallel_reduce(A, mid, end)
        return left_result + right_result

def scan(A, arr_B, s, t, offset):
    if s == t:
        arr_B[s] = offset + A[s]
    else:
        mid = (s + t - 1) // 2

        with concurrent.futures.ThreadPoolExecutor() as executor:
            left_result = executor.submit(scan, A, arr_B, s, mid, offset)
            left_sum = parallel_reduce(A, s, mid)

            right_result = executor.submit(scan, A, arr_B, mid + 1, t, offset + left_sum)

           
            left_result.result()
            right_result.result()
    return arr_B

def parallel_prefix_sum(matrix_a):
    arr_B = matrix_a.copy()
    return scan(matrix_a, arr_B, 0, len(matrix_a) - 1, 0)

def insert_value_arrs(args):
    index, current_arr, new_arr = args
    for i in range(len(current_arr)):
        new_arr[index + i] = current_arr[i]

def flatten_algorithm(arrs, sizeOfArrs):
    getSizeOfArrs = [0]
    sumSizeArrs = 0
    for arr in arrs:
        getSizeOfArrs.append(len(arr))
        sumSizeArrs += len(arr)
    getSizeOfArrs.remove(getSizeOfArrs[len(getSizeOfArrs) - 1])
    getSizeOfArrs = list(parallel_prefix_sum(getSizeOfArrs))
    tuple_arrs = []
    flatten_arrs = [0] * sumSizeArrs

    for index in range(len(getSizeOfArrs)):
        tuple_arr = (getSizeOfArrs[index], arrs[index], flatten_arrs)
        tuple_arrs.append(tuple_arr)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(insert_value_arrs, tuple_arrs)

    return flatten_arrs


array_2d = [[random.randint(0, 100) for _ in range(10000)] for _ in range(1000)]


flattened_array = flatten_algorithm(array_2d, len(array_2d))

# Print the size of the resulting array
print(len(flattened_array))