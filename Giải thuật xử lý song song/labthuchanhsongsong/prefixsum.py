import multiprocessing
import concurrent.futures
import numpy as np
import time
def reduce(A,start,end):
    sum = 0
    for i in range(start,end+1):
        sum += A[i]
    return sum
def Scan(A,arr_B,st,ed,offset):
    if(st==ed):
        arr_B[st]=offset+A[st]
    else:
        mid = st + (ed-st)//2
        left_sum = reduce(A,st,mid)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            left = executor.submit(Scan,A,arr_B,st,mid,offset)
            right = executor.submit(Scan,A,arr_B,mid+1,ed,offset+left_sum)
            left.result()
            right.result()
    return arr_B
def prefixsum(matrix):
    arr_B = matrix.copy()
    return Scan(matrix,arr_B,0,len(matrix)-1,0)
if __name__ == "__main__":
    # arrs = np.random.randint(-100, 100, 1000)
    arrs = [1,2,3,4,5,6]
    print("Mang co kich thuoc " + str(len(arrs)) + " có mảng " + str(np.array(arrs)))
    k = prefixsum(arrs)
    print("ket qua", k)