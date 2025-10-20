import random
from syndrome import syndrome

def gallager_b(H, received, iterations=50, th0=0.5, th1=0.5):
    m = len(H)
    n = len(H[0])
    x = received[:]
    col_counts = [sum(H[r][j] for r in range(m)) for j in range(n)]
    avg_col = int(round(sum(col_counts)/n))
    thr_low = int(avg_col * th0 + 1e-9)
    thr_high = int(avg_col * th1 + 1e-9)
    if thr_low < 1: thr_low = 1
    if thr_high <= thr_low: thr_high = thr_low + 1

    for it in range(iterations):
        syndrome_vec = syndrome(H, x)
        if all(s==0 for s in syndrome_vec):
            return x, True, it

        unsatisfied_counts = [0]*n
        for i in range(m):
            if syndrome_vec[i]==1:
                for j in range(n):
                    if H[i][j]:
                        unsatisfied_counts[j] += 1

        flipped = False
        for j in range(n):
            if unsatisfied_counts[j] >= thr_high:
                x[j] ^= 1
                flipped = True
            elif thr_low <= unsatisfied_counts[j] < thr_high:
                if random.random() < 0.5:
                    x[j] ^= 1
                    flipped = True
        if not flipped:
            break

    return x, all(si==0 for si in syndrome(H,x)), iterations
