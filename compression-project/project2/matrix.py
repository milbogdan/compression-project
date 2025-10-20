import random

def generate_H(n, m, wr, wc, seed=0):
    random.seed(seed)
    H = [[0]*n for _ in range(m)]
    for i in range(m):
        cols = random.sample(range(n), wr)
        for c in cols:
            H[i][c] = 1
    col_counts = [sum(H[r][c] for r in range(m)) for c in range(n)]
    it = 0
    max_iter = 20000
    while (any(cc != wc for cc in col_counts) and it < max_iter):
        too_many = [i for i,c in enumerate(col_counts) if c > wc]
        too_few = [i for i,c in enumerate(col_counts) if c < wc]
        if not too_many or not too_few:
            break
        c1 = random.choice(too_many)
        c2 = random.choice(too_few)
        rows = [r for r in range(m) if H[r][c1]==1 and H[r][c2]==0]
        if not rows:
            it += 1
            continue
        r = random.choice(rows)
        H[r][c1] = 0
        H[r][c2] = 1
        col_counts[c1] -= 1
        col_counts[c2] += 1
        it += 1
    if not all(cc == wc for cc in col_counts):
        print("UPOZORENJE: nije uspelo postici tacan wc za sve kolone; kolonske tezine:", col_counts)
    return H

def print_H(H):
    for row in H:
        print("".join(str(x) for x in row))
