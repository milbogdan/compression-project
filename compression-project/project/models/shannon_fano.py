from utils import frequency_table

class SFBitWriter:
    def __init__(self, filename):
        self.file = open(filename, "wb")
        self.buffer = 0
        self.bits_filled = 0

    def write_bit(self, bit):
        self.buffer = (self.buffer << 1) | (bit & 1)
        self.bits_filled += 1
        if self.bits_filled == 8:
            self.flush()

    def write_bits(self, bits):
        for b in bits:
            self.write_bit(int(b))

    def flush(self):
        if self.bits_filled > 0:
            self.file.write(bytes([self.buffer << (8 - self.bits_filled)]))
            self.buffer = 0
            self.bits_filled = 0

    def close(self):
        self.flush()
        self.file.close()


class SFBitReader:
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


class ShannonFano:
    def build_tree(self, symbols):
        if len(symbols) == 0:
            return None
        if len(symbols) == 1:
            return symbols[0]
        total = sum(freq for _, freq in symbols)
        acc = 0
        for i, (_, freq) in enumerate(symbols):
            acc += freq
            if acc >= total / 2:
                break
        left = self.build_tree(symbols[:i+1])
        right = self.build_tree(symbols[i+1:])
        return (left, right)

    def build_codes(self, tree, prefix="", codebook=None):
        if codebook is None:
            codebook = {}
        if isinstance(tree, tuple) and len(tree) == 2 and isinstance(tree[1], int):
            symbol = tree[0]
            codebook[symbol] = prefix
        else:
            if tree[0]:
                self.build_codes(tree[0], prefix + "0", codebook)
            if tree[1]:
                self.build_codes(tree[1], prefix + "1", codebook)
        return codebook

    def encode(self, infile, outfile):
        freqs = frequency_table(infile)
        symbols = sorted(freqs.items(), key=lambda x: x[1], reverse=True)
        tree = self.build_tree(symbols)
        codes = self.build_codes(tree)

        writer = SFBitWriter(outfile)

        writer.file.write(len(freqs).to_bytes(2, "big"))
        for sym, freq in freqs.items():
            writer.file.write(bytes([sym]))
            writer.file.write(freq.to_bytes(4, "big"))

        with open(infile, "rb") as f:
            for b in f.read():
                writer.write_bits(codes[b])
        writer.close()

    def decode(self, infile, outfile):
        reader = SFBitReader(infile)

        num_symbols_bytes = reader.file.read(2)
        if len(num_symbols_bytes) < 2:
            raise ValueError("Nepravilan SF fajl")
        num_symbols = int.from_bytes(num_symbols_bytes, "big")

        freqs = {}
        for _ in range(num_symbols):
            sym_bytes = reader.file.read(1)
            freq_bytes = reader.file.read(4)
            if len(sym_bytes) < 1 or len(freq_bytes) < 4:
                raise ValueError("Nepravilan SF fajl")
            sym = sym_bytes[0]
            freq = int.from_bytes(freq_bytes, "big")
            freqs[sym] = freq


        symbols = sorted(freqs.items(), key=lambda x: x[1], reverse=True)
        tree = self.build_tree(symbols)
        codes = self.build_codes(tree)

        inv_codes = {v: k for k, v in codes.items()}

        current_bits = ""
        with open(outfile, "wb") as out:
            while True:
                bit = reader.read_bit()
                if bit is None:
                    break
                current_bits += str(bit)
                if current_bits in inv_codes:
                    out.write(bytes([inv_codes[current_bits]]))
                    current_bits = ""

        reader.close()
