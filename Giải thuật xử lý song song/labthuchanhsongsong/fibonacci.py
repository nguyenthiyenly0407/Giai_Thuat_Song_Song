
import concurrent.futures
import multiprocessing

def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

def parallel_fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    elif n % 2 == 0:
        k = n // 2
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            fib_k, fib_k1 = pool.map(fibonacci, [k, k + 1])
            return fib_k * (2 * fib_k1 - fib_k)
    else:
        k = (n - 1) // 2
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            fib_k, fib_k1 = pool.map(fibonacci, [k, k + 1])
            return fib_k * fib_k + fib_k1 * fib_k1

if __name__ == "__main__":
    n = 2
    fibo = parallel_fibonacci(n)
    print("Kết quả:", fibo)
