class DES:
    def __init__(self):
        self._init_tables()
        self._generate_ip_inv()

    def _init_tables(self):
        self.IP = []
        for i in [58, 60, 62, 64, 57, 59, 61, 63]:
            for j in range(8):
                self.IP.append(i - 8 * j)

        self.E = []
        for i in range(8):
            base = 4 * i
            left = 32 if base == 0 else base
            self.E.append(left)
            for k in range(1, 5):
                self.E.append(base + k)
            right = 1 if base + 5 == 33 else base + 5
            self.E.append(right)

        p_data = "16 7 20 21 29 12 28 17 1 15 23 26 5 18 31 10 2 8 24 14 32 27 3 9 19 13 30 6 22 11 4 25"
        self.P = [int(x) for x in p_data.split()]

        pc1_data = "57 49 41 33 25 17 9 1 58 50 42 34 26 18 10 2 59 51 43 35 27 19 11 3 60 52 44 36 63 55 47 39 31 23 15 7 62 54 46 38 30 22 14 6 61 53 45 37 29 21 13 5 28 20 12 4"
        self.PC1 = [int(x) for x in pc1_data.split()]

        pc2_data = "14 17 11 24 1 5 3 28 15 6 21 10 23 19 12 4 26 8 16 7 27 20 13 2 41 52 31 37 47 55 30 40 51 45 33 48 44 49 39 56 34 53 46 42 50 36 29 32"
        self.PC2 = [int(x) for x in pc2_data.split()]

        self.SHIFT = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

        flat_sboxes = [
            14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7, 0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8, 4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0, 15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13,
            15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10, 3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5, 0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15, 13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9,
            10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8, 13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1, 13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7, 1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12,
            7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15, 13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9, 10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4, 3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14,
            2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9, 14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6, 4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14, 11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3,
            12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11, 10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8, 9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6, 4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13,
            4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1, 13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6, 1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2, 6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12,
            13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7, 1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2, 7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8, 2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11
        ]
        
        self.SBOX = []
        idx = 0
        for s in range(8):
            sbox = []
            for r in range(4):
                row = []
                for c in range(16):
                    row.append(flat_sboxes[idx])
                    idx += 1
                sbox.append(row)
            self.SBOX.append(sbox)

    def _generate_ip_inv(self):
        self.IP_INV = [0] * 64
        for i in range(64):
            v = self.IP[i]
            self.IP_INV[v - 1] = i + 1

    def _str_to_bits(self, s):
        bits = []
        for char in s:
            for i in range(7, -1, -1):
                bits.append((ord(char) >> i) & 1)
        return bits

    def _bits_to_str(self, bits):
        chars = []
        for i in range(0, len(bits), 8):
            byte = 0
            for j in range(8):
                byte = (byte << 1) | bits[i + j]
            chars.append(chr(byte))
        return ''.join(chars)

    def _bits_to_hex(self, bits):
        hex_str = ''
        for i in range(0, len(bits), 4):
            val = 0
            for j in range(4):
                val = (val << 1) | bits[i + j]
            hex_str += format(val, 'x')
        return hex_str

    def _hex_to_bits(self, hex_str):
        bits = []
        for char in hex_str:
            val = int(char, 16)
            for i in range(3, -1, -1):
                bits.append((val >> i) & 1)
        return bits

    def _permute(self, bits, table):
        return [bits[i - 1] for i in table]

    def _left_shift(self, bits, n):
        return bits[n:] + bits[:n]

    def _xor(self, bits1, bits2):
        return [b1 ^ b2 for b1, b2 in zip(bits1, bits2)]

    def _generate_keys(self, key_bits):
        key_56 = self._permute(key_bits, self.PC1)
        left = key_56[:28]
        right = key_56[28:]
        
        keys = []
        for shift in self.SHIFT:
            left = self._left_shift(left, shift)
            right = self._left_shift(right, shift)
            keys.append(self._permute(left + right, self.PC2))
        
        return keys

    def _f_function(self, right, key):
        expanded = self._permute(right, self.E)
        xored = self._xor(expanded, key)
        
        output = []
        for i in range(8):
            block = xored[i * 6:(i + 1) * 6]
            row = (block[0] << 1) | block[5]
            col = (block[1] << 3) | (block[2] << 2) | (block[3] << 1) | block[4]
            val = self.SBOX[i][row][col]
            for j in range(3, -1, -1):
                output.append((val >> j) & 1)
        
        return self._permute(output, self.P)

    def _des_block(self, block_bits, keys, decrypt=False):
        permuted = self._permute(block_bits, self.IP)
        left = permuted[:32]
        right = permuted[32:]
        
        key_order = range(15, -1, -1) if decrypt else range(16)
        
        for i in key_order:
            new_right = self._xor(left, self._f_function(right, keys[i]))
            left = right
            right = new_right
        
        combined = right + left
        return self._permute(combined, self.IP_INV)

    def encrypt_text(self, metin, anahtar):
        while len(anahtar) < 8:
            anahtar += anahtar
        anahtar = anahtar[:8]
        
        pad_len = 8 - (len(metin) % 8)
        metin += chr(pad_len) * pad_len
        
        key_bits = self._str_to_bits(anahtar)
        keys = self._generate_keys(key_bits)
        
        sifreli = ''
        for i in range(0, len(metin), 8):
            block = metin[i:i + 8]
            block_bits = self._str_to_bits(block)
            encrypted_bits = self._des_block(block_bits, keys, decrypt=False)
            sifreli += self._bits_to_hex(encrypted_bits)
        
        return sifreli

    def decrypt_hex(self, sifreli_hex, anahtar):
        while len(anahtar) < 8:
            anahtar += anahtar
        anahtar = anahtar[:8]
        
        key_bits = self._str_to_bits(anahtar)
        keys = self._generate_keys(key_bits)
        
        bits = self._hex_to_bits(sifreli_hex)
        
        cozulmus = ''
        for i in range(0, len(bits), 64):
            block_bits = bits[i:i + 64]
            decrypted_bits = self._des_block(block_bits, keys, decrypt=True)
            cozulmus += self._bits_to_str(decrypted_bits)
        
        pad_len = ord(cozulmus[-1])
        return cozulmus[:-pad_len]


def des_sifrele(metin, anahtar):
    des = DES()
    return des.encrypt_text(metin, anahtar)

def des_desifre(sifreli_hex, anahtar):
    des = DES()
    return des.decrypt_hex(sifreli_hex, anahtar)
