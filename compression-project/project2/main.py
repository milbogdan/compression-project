from matrix import generate_H, print_H
from utils import gf2_nullspace_bruteforce, find_min_failure
from syndrome import syndrome_table

n = 15
m = 9
wr = 5
wc = 3
seed = 61

def main():
    H = generate_H(n, m, wr, wc, seed)
    print("H matrica:")
    print_H(H)

    nullspace = gf2_nullspace_bruteforce(H)
    print("Broj nenultih kodnih reci (velicina nullspace):", len(nullspace))
    if nullspace:
        d = min(sum(v) for v in nullspace)
    else:
        d = None
    print("Kodna udaljenost (minimalna tezina nenultog kodne reci):", d)

    table = syndrome_table(H)
    print("Velicina tabele sindroma:", len(table))

    e_fail = find_min_failure(H)
    print("Minimalni vektor greske koji Gallager B ne moze da ispravi (prvi pronadjen):", e_fail,
          "tezina:", sum(e_fail) if e_fail else None)

    if d is not None:
        print("Uporedi: kodna udaljenost:", d)


if __name__ == "__main__":
    main()
