import argparse

from comparer import Comparer
from entropy import calculate_entropy
from models.shannon_fano import ShannonFano
from models.huffman import Huffman
from models.lz77 import LZ77
from models.lzw import LZW

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--entropy", help="Izračunavanje entropije fajla")
    parser.add_argument("--encode", choices=["sf", "huffman", "lz77", "lzw"], help="Kompresija fajla")
    parser.add_argument("--decode", choices=["sf", "huffman", "lz77", "lzw"], help="Dekompresija fajla")
    parser.add_argument("--infile", help="Ulazni fajl")
    parser.add_argument("--outfile", help="Izlazni fajl")
    parser.add_argument("--compare", nargs=3, metavar=("OLD", "COMPRESSED", "NEW"))

    args = parser.parse_args()

    if args.entropy:
        print(f"Entropija {args.entropy}: {calculate_entropy(args.entropy):.4f} bita/znaku")

    elif args.encode and args.infile and args.outfile:
        if args.encode == "sf":
            ShannonFano().encode(args.infile, args.outfile)
        elif args.encode == "huffman":
            Huffman().encode(args.infile, args.outfile)
        elif args.encode == "lz77":
            LZ77().encode(args.infile, args.outfile)
        elif args.encode == "lzw":
            LZW().encode(args.infile, args.outfile)
        print("Kompresija zavrsena.")

    elif args.decode and args.infile and args.outfile:
        if args.decode == "sf":
            ShannonFano().decode(args.infile, args.outfile)
        elif args.decode == "huffman":
            Huffman().decode(args.infile, args.outfile)
        elif args.decode == "lz77":
            LZ77().decode(args.infile, args.outfile)
        elif args.decode == "lzw":
            LZW().decode(args.infile, args.outfile)
        print("Dekompresija zavrsena.")

    elif args.compare:
        old_file, compressed_file, new_file = args.compare
        comparer = Comparer(old_file, compressed_file, new_file)
        comparer.compare_files()

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
