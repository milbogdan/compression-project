from itertools import combinations
from gallager import gallager_b
from syndrome import syndrome

def gf2_nullspace_bruteforce(H):
    n = len(H[0])
    nullspace = []
    for x in range(1, 1<<n):
        v = [(x>>i)&1 for i in range(n)]
        s = syndrome(H, v)
        if all(si==0 for si in s):
            nullspace.append(v)
    return nullspace

def find_min_failure(H):
    n = len(H[0])
    for w in range(1, n+1):
        for comb in combinations(range(n), w):
            e = [0]*n
            for i in comb:
                e[i]=1
            received = e[:]
            _, ok, _ = gallager_b(H, received, iterations=50)
            if not ok:
                return e
    return None
