import multiprocessing
import random
import time

def mergesort_algorithm(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left_seq = arr[:mid]
    right_seq = arr[mid:]

    left_result = mergesort_algorithm(left_seq)
    right_result = mergesort_algorithm(right_seq)

    return merge(left_result, right_result)

def merge(left, right):
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    
    return result

def parallel_mergesort(arr):
    size = len(arr)
    if size <= 1:
        return arr
    mid = size // 2
    
    with multiprocessing.Pool(processes=2) as pool:
        left = pool.apply_async(mergesort_algorithm, (arr[:mid],))
        right = pool.apply_async(mergesort_algorithm, (arr[mid:],))
        
        left_result = left.get()
        right_result = right.get()

    return merge(left_result, right_result)

if __name__ == "__main__":
    array = [random.randint(-100000, 100000) for _ in range(100000)]
    start = time.time()
    new_arr = parallel_mergesort(array)
    end = time.time()
    print(new_arr[-10:])
