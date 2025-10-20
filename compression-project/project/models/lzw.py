import os

class LZWBitWriter:
    def __init__(self, filename):
        self.file = open(filename, "wb")
        self.buffer = 0
        self.bits_filled = 0

    def write_code(self, code, bit_length):
        self.buffer = (self.buffer << bit_length) | code
        self.bits_filled += bit_length
        while self.bits_filled >= 8:
            self.bits_filled -= 8
            byte_to_write = (self.buffer >> self.bits_filled) & 0xFF
            self.file.write(bytes([byte_to_write]))
        self.buffer &= (1 << self.bits_filled) - 1

    def close(self):
        if self.bits_filled > 0:
            self.file.write(bytes([(self.buffer << (8 - self.bits_filled)) & 0xFF]))
        self.file.close()


class LZWBitReader:
    def __init__(self, filename):
        self.file = open(filename, "rb")
        self.buffer = 0
        self.bits_left = 0

    def read_code(self, bit_length):
        while self.bits_left < bit_length:
            byte = self.file.read(1)
            if not byte:
                return None
            self.buffer = (self.buffer << 8) | byte[0]
            self.bits_left += 8

        self.bits_left -= bit_length
        code = (self.buffer >> self.bits_left) & ((1 << bit_length) - 1)
        self.buffer &= (1 << self.bits_left) - 1
        return code

    def close(self):
        self.file.close()


class LZW:
    def __init__(self, max_bits=12):
        self.max_bits = max_bits
        self.max_table_size = 1 << max_bits
        self.eof_code = self.max_table_size - 1

    def encode(self, infile, outfile):
        writer = LZWBitWriter(outfile)
        with open(infile, "rb") as f:
            data = f.read()

        dictionary = {bytes([i]): i for i in range(256)}
        next_code = 256
        bit_length = 9
        current = bytes()

        for byte in data:
            current_plus = current + bytes([byte])
            if current_plus in dictionary:
                current = current_plus
            else:
                writer.write_code(dictionary[current], bit_length)
                if next_code < self.eof_code:
                    dictionary[current_plus] = next_code
                    next_code += 1
                    if next_code == (1 << bit_length) and bit_length < self.max_bits:
                        bit_length += 1
                current = bytes([byte])

        if current:
            writer.write_code(dictionary[current], bit_length)

        writer.write_code(self.eof_code, bit_length)
        writer.close()

    def decode(self, infile, outfile):
        reader = LZWBitReader(infile)
        dictionary = {i: bytes([i]) for i in range(256)}
        next_code = 256
        bit_length = 9

        code = reader.read_code(bit_length)
        if code is None or code == self.eof_code:
            return

        string = dictionary[code]
        output = bytearray(string)

        while True:
            code = reader.read_code(bit_length)
            if code is None or code == self.eof_code:
                break

            if code in dictionary:
                entry = dictionary[code]
            elif code == next_code:
                entry = string + string[:1]
            else:
                break

            output.extend(entry)

            if next_code < self.eof_code:
                dictionary[next_code] = string + entry[:1]
                next_code += 1
                if next_code == (1 << bit_length) and bit_length < self.max_bits:
                    bit_length += 1

            string = entry

        reader.close()
        with open(outfile, "wb") as f:
            f.write(output)
