import heapq
from utils import frequency_table

class HuffmanBitWriter:
    def __init__(self, filename):
        self.file = open(filename, "wb")
        self.buffer = 0
        self.bits_filled = 0

    def write_bit(self, bit):
        self.buffer = (self.buffer << 1) | (bit & 1)
        self.bits_filled += 1
        if self.bits_filled == 8:
            self.file.write(bytes([self.buffer]))
            self.buffer = 0
            self.bits_filled = 0

    def write_bits(self, bits):
        for b in bits:
            self.write_bit(int(b))

    def flush(self):
        if self.bits_filled > 0:
            self.buffer <<= (8 - self.bits_filled)
            self.file.write(bytes([self.buffer]))
            self.buffer = 0
            self.bits_filled = 0

    def close(self):
        self.flush()
        self.file.close()


class HuffmanBitReader:
    def __init__(self, filename):
        self.file = open(filename, "rb")
        self.buffer = 0
        self.bits_left = 0

    def read_bit(self):
        if self.bits_left == 0:
            byte = self.file.read(1)
            if not byte:
                return None
            self.buffer = byte[0]
            self.bits_left = 8
        self.bits_left -= 1
        return (self.buffer >> self.bits_left) & 1

    def close(self):
        self.file.close()


class HuffmanNode:
    def __init__(self, symbol=None, freq=0, left=None, right=None):
        self.symbol = symbol
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq


class Huffman:

    def build_tree(self, freqs):
        heap = [HuffmanNode(sym, f) for sym, f in freqs.items()]
        heapq.heapify(heap)
        while len(heap) > 1:
            a = heapq.heappop(heap)
            b = heapq.heappop(heap)
            heapq.heappush(heap, HuffmanNode(None, a.freq + b.freq, a, b))
        return heap[0]

    def build_codes(self, node, prefix="", codebook=None):
        if codebook is None:
            codebook = {}
        if node.symbol is not None:
            codebook[node.symbol] = prefix
        else:
            self.build_codes(node.left, prefix + "0", codebook)
            self.build_codes(node.right, prefix + "1", codebook)
        return codebook

    def encode(self, infile, outfile):
        freqs = frequency_table(infile)
        root = self.build_tree(freqs)
        codes = self.build_codes(root)

        writer = HuffmanBitWriter(outfile)

        writer.file.write(len(freqs).to_bytes(2, "big"))
        for sym, f in freqs.items():
            writer.file.write(bytes([sym]))
            writer.file.write(f.to_bytes(4, "big"))

        with open(infile, "rb") as f:
            for b in f.read():
                writer.write_bits(codes[b])

        writer.close()

    def decode(self, infile, outfile):
        reader = HuffmanBitReader(infile)

        num_symbols_bytes = reader.file.read(2)
        if len(num_symbols_bytes) < 2:
            raise ValueError("Fajl nije validan Huffman fajl")
        num_symbols = int.from_bytes(num_symbols_bytes, "big")

        freqs = {}
        for _ in range(num_symbols):
            sym_bytes = reader.file.read(1)
            freq_bytes = reader.file.read(4)
            if len(sym_bytes) < 1 or len(freq_bytes) < 4:
                raise ValueError("Nepravilan format zaglavlja")
            sym = sym_bytes[0]
            freq = int.from_bytes(freq_bytes, "big")
            freqs[sym] = freq

        root = self.build_tree(freqs)
        total_symbols = sum(freqs.values())

        node = root
        count = 0
        with open(outfile, "wb") as out:
            while count < total_symbols:
                bit = reader.read_bit()
                if bit is None:
                    break
                node = node.left if bit == 0 else node.right
                if node.symbol is not None:
                    out.write(bytes([node.symbol]))
                    node = root
                    count += 1

        reader.close()
