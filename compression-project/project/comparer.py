import os
import math

from entropy import calculate_entropy
from utils import file_size


class Comparer:
    def __init__(self, old_file, compressed_file, new_file):
        self.old_file = old_file
        self.compressed_file = compressed_file
        self.new_file = new_file

    def compare_files(self):
        print(f"{'File':<20} {'Size (bytes)':<15} {'Entropy':<10}")
        for f in [self.old_file, self.compressed_file, self.new_file]:
            size = file_size(f)
            entropy = calculate_entropy(f)
            print(f"{os.path.basename(f):<20} {size:<15} {entropy:<10.4f}")

        with open(self.old_file, "rb") as f1, open(self.new_file, "rb") as f2:
            same = f1.read() == f2.read()
        print(f"\nStari fajl == Novi fajl? {'DA' if same else 'NE'}")
