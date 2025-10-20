
class LZ77BitWriter:
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

    def write_byte(self, byte):
        self.flush()
        self.file.write(bytes([byte]))

    def flush(self):
        if self.bits_filled > 0:
            self.file.write(bytes([self.buffer << (8 - self.bits_filled)]))
            self.buffer = 0
            self.bits_filled = 0

    def close(self):
        self.flush()
        self.file.close()


class LZ77BitReader:
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

    def read_byte(self):
        self.bits_left = 0
        b = self.file.read(1)
        if not b:
            return None
        return b[0]

    def close(self):
        self.file.close()


class LZ77:
    def __init__(self, window_size=4096, lookahead_size=15):
        self.window_size = window_size
        self.lookahead_size = lookahead_size

    def encode(self, infile, outfile):
        writer = LZ77BitWriter(outfile)
        with open(infile, "rb") as f:
            data = f.read()

        pos = 0
        while pos < len(data):
            match_len = 0
            match_dist = 0
            # longest match u windowu
            start_window = max(0, pos - self.window_size)
            for i in range(start_window, pos):
                length = 0
                while (length < self.lookahead_size and
                       pos + length < len(data) and
                       data[i + length] == data[pos + length]):
                    length += 1
                if length > match_len:
                    match_len = length
                    match_dist = pos - i

            if match_len >= 3:
                # flag = 1 (match)
                writer.write_bit(1)
                #  distance (12 bit) i length (4 bit)
                writer.write_bits(f'{match_dist:012b}')
                writer.write_bits(f'{match_len:04b}')
                pos += match_len
            else:
                # zapisujemo flag = 0 (literal)
                writer.write_bit(0)
                writer.write_byte(data[pos])
                pos += 1

        writer.close()

    def decode(self, infile, outfile):
        reader = LZ77BitReader(infile)
        out_data = bytearray()

        while True:
            flag = reader.read_bit()
            if flag is None:
                break
            if flag == 0:
                b = reader.read_byte()
                if b is None:
                    break
                out_data.append(b)
            else:
                # distance i length
                dist_bits = ''
                for _ in range(12):
                    bit = reader.read_bit()
                    if bit is None:
                        raise ValueError("Nepravilan LZ77 fajl")
                    dist_bits += str(bit)
                length_bits = ''
                for _ in range(4):
                    bit = reader.read_bit()
                    if bit is None:
                        raise ValueError("Nepravilan LZ77 fajl")
                    length_bits += str(bit)
                dist = int(dist_bits, 2)
                length = int(length_bits, 2)
                start = len(out_data) - dist
                for i in range(length):
                    out_data.append(out_data[start + i])

        reader.close()
        with open(outfile, "wb") as f:
            f.write(out_data)
