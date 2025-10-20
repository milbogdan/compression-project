import os

def frequency_table(filename):
    with open(filename, "rb") as f:
        data = f.read()
    freq = {}
    for b in data:
        freq[b] = freq.get(b, 0) + 1
    return freq

def file_size(file_path):
    return os.path.getsize(file_path)

