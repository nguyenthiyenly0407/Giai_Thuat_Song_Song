import concurrent.futures
import numpy as np
import time
import multiprocessing

def parallel_prefix_sum(array_a):
    def sum_couple(arr_index, arrs, couple_arrs):
        for i in range(len(arr_index)):
            index = arr_index[i]
            couple_arrs[index] = arrs[2*index] + arrs[2*index + 1]

    def assign_value_new_arrs(old_arrs, old_res_arrs, new_arrs, array_index):
        for index in range(len(array_index)):
            current_pos = array_index[index]
            if current_pos!= 0:
                if current_pos % 2:
                    new_arrs[current_pos] = old_res_arrs[current_pos // 2]
                else:
                    new_arrs[current_pos] = old_arrs[current_pos] + old_res_arrs[(current_pos // 2) - 1]

    sizeOfArrs = len(array_a)
    if sizeOfArrs == 1:
        return array_a

    sum_couple_arrs = np.zeros(sizeOfArrs // 2, dtype=np.int64)
    tuple_arrs_sum_couple = []

    # Divide the work among threads for sum_couple
    if len(sum_couple_arrs) <= multiprocessing.cpu_count():
        devide_sum_couple = np.array_split(list(range(len(sum_couple_arrs))), multiprocessing.cpu_count())
        for index in range(len(devide_sum_couple)):
            tuple_arrs_sum_couple.append((devide_sum_couple[index], array_a, sum_couple_arrs))
    else:
        tuple_arrs_sum_couple.append((list(range(len(sum_couple_arrs))), array_a, sum_couple_arrs))

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(lambda x: sum_couple(*x), tuple_arrs_sum_couple)

    new_res_arrs = parallel_prefix_sum(sum_couple_arrs)

    new_arrs = array_a.copy()
    tuple_arrs_assign_value = []

    # Divide the work among threads for assign_value_new_arrs
    if len(array_a) <= multiprocessing.cpu_count():
        devide_arr = np.array_split(list(range(len(array_a))), multiprocessing.cpu_count())
        for index in range(len(devide_arr)):
            tuple_arrs_assign_value.append((array_a, new_res_arrs, new_arrs, devide_arr[index]))
    else:
        tuple_arrs_assign_value.append((array_a, new_res_arrs, new_arrs, list(range(len(array_a)))))

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(lambda x: assign_value_new_arrs(*x), tuple_arrs_assign_value)

    return new_arrs

# Example usage
array_a = np.random.randint(0, 100, 1000000000)  # Replace with your array
print("Initial array size:", array_a.nbytes)
print("Number of elements in the original array:", len(array_a))

start_time = time.time()
result = parallel_prefix_sum(array_a)
print("Array after prefix sum:", result)

if np.array_equal(array_a, result):
    print("The two arrays are equal")
else:
    print("The two arrays are not equal")

print("Run time:", time.time() - start_time)