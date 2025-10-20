import itertools

def syndrome(H, v):
    m = len(H)
    s = [0]*m
    for i in range(m):
        acc = 0
        for j in range(len(v)):
            acc ^= (H[i][j] & v[j])
        s[i] = acc
    return tuple(s)

def syndrome_table(H):
    n = len(H[0])
    m = len(H)
    table = {}
    for w in range(0, n+1):
        for comb in itertools.combinations(range(n), w):
            e = [0]*n
            for i in comb:
                e[i]=1
            s = syndrome(H, e)
            if s not in table or sum(e) < sum(table[s]):
                table[s] = e[:]
        if len(table) == (1<<m):
            break
    return table
