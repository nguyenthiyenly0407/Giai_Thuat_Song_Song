import multiprocessing
import os

def read_input_file(filepath):
    with open(filepath, 'r') as file:
        data = file.readlines()
    matrices = [list(map(int, line.strip().split())) for line in data]
    return matrices

def read_kernel_file(filepath):
    with open(filepath, 'r') as file:
        kernel = list(map(int, file.readline().strip().split()))
    return kernel

def reshape_matrix(flat_matrix):
    size = int(len(flat_matrix) ** 0.5)
    matrix = []
    for i in range(size):
        matrix.append(flat_matrix[i*size:(i+1)*size])
    return matrix

def reshape_kernel(flat_kernel):
    return [flat_kernel[i*3:(i+1)*3] for i in range(3)]

def pad_matrix(matrix):
    size = len(matrix)
    padded_matrix = [[0] * (size + 2) for _ in range(size + 2)]
    for i in range(size):
        for j in range(size):
            padded_matrix[i + 1][j + 1] = matrix[i][j]
    return padded_matrix

def convolve_matrix(matrix, kernel):
    size = len(matrix)
    padded_matrix = pad_matrix(matrix)
    result = [[0] * size for _ in range(size)]
    
    for i in range(size):
        for j in range(size):
            sum_val = 0
            for ki in range(3):
                for kj in range(3):
                    sum_val += padded_matrix[i + ki][j + kj] * kernel[ki][kj]
            result[i][j] = sum_val
    
    return result

def process_matrix(matrix, kernel):
    matrix = reshape_matrix(matrix)
    result = convolve_matrix(matrix, kernel)
    return [elem for row in result for elem in row]

def parallel_convolution(filepath_input, filepath_kernel):
    matrices = read_input_file(filepath_input)
    kernel = reshape_kernel(read_kernel_file(filepath_kernel))

    with multiprocessing.Pool() as pool:
        results = pool.starmap(process_matrix, [(matrix, kernel) for matrix in matrices])
    
    return results

# Example usage
if __name__ == '__main__':
    input_file = 'D:/Documents/cube_A.txt'
    kernel_file = 'D:/Documents/kernel.txt'
    result = parallel_convolution(input_file, kernel_file)
    for line in result:
        print(line)
