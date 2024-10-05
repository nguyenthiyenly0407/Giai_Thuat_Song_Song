import concurrent.futures
from collections import Counter
import os
def count_chars_in_chunk(chunk):  
    filtered_chunk = chunk.replace('\n', '')  
    return Counter(filtered_chunk)
def read_file_in_chunks(filepath, chunk_size=1024*1024):  
    with open(filepath, 'r') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            yield chunk
def parallel_char_count(filepath):
    final_counts = Counter()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(count_chars_in_chunk, chunk) for chunk in read_file_in_chunks(filepath)]
        for future in concurrent.futures.as_completed(futures):
            final_counts.update(future.result())  
    return dict(final_counts)

# Example usage
filepath = 'D:/Documents/challenge4.txt'

# Kiểm tra xem tệp tin có tồn tại hay không
if os.path.exists(filepath):
    char_counts = parallel_char_count(filepath)
    print(char_counts)
else:
    print(f"File not found: {filepath}")
