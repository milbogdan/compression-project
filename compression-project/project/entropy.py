import math

def calculate_entropy(filename: str) -> float:
    with open(filename, "rb") as f:
        data = f.read()
    N = len(data)
    if N == 0:
        return 0.0

    freq = [0] * 256
    for b in data:
        freq[b] += 1

    entropy = 0.0
    for n in freq:
        if n > 0:
            p = n / N
            entropy -= p * math.log2(p)
    return entropy
