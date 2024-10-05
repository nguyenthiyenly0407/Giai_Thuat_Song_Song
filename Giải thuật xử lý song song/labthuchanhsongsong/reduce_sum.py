import multiprocessing
def reduce_sum(A,start,end):
    if(start==end): 
        return A[start]
    else:
        mid = start + (end-start)//2
        left = reduce_sum(A,start,mid)
        right= reduce_sum(A,mid+1,end)
        return left+right
    
if __name__ == "__main__":
    A=[0,1,2,3,4,5,6,7,8]
    start = A[0]
    end = A[8]
    re= reduce_sum(A,start,end)
    print("ket qua", re)
