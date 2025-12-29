import math

class SHA256:
    def __init__(self):
        self._generate_constants()

    def _get_fractional_bits(self, n, root_power):
        root = n ** (1 / root_power)
        frac = root - int(root)
        return int(frac * (2 ** 32)) & 0xFFFFFFFF

    def _generate_primes(self, count):
        primes = []
        n = 2
        while len(primes) < count:
            if all(n % p != 0 for p in primes if p * p <= n):
                primes.append(n)
            n += 1
        return primes

    def _generate_constants(self):
        primes_64 = self._generate_primes(64)
        
        self.K = [self._get_fractional_bits(p, 3) for p in primes_64]
        
        self.H_INIT = [self._get_fractional_bits(p, 2) for p in primes_64[:8]]

    def _rotr(self, n, b):
        return ((n >> b) | (n << (32 - b))) & 0xFFFFFFFF

    def _shr(self, n, b):
        return n >> b

    def hash(self, mesaj):
        if isinstance(mesaj, str):
            mesaj = mesaj.encode('utf-8')
        
        H = list(self.H_INIT)
        
        mesaj_uzunlugu = len(mesaj) * 8
        mesaj += b'\x80'
        
        while (len(mesaj) * 8) % 512 != 448:
            mesaj += b'\x00'
        
        mesaj += mesaj_uzunlugu.to_bytes(8, byteorder='big')
        
        for i in range(0, len(mesaj), 64):
            blok = mesaj[i:i + 64]
            
            w = []
            for j in range(16):
                w.append(int.from_bytes(blok[j * 4:(j + 1) * 4], byteorder='big'))
            
            for j in range(16, 64):
                s0 = self._rotr(w[j - 15], 7) ^ self._rotr(w[j - 15], 18) ^ self._shr(w[j - 15], 3)
                s1 = self._rotr(w[j - 2], 17) ^ self._rotr(w[j - 2], 19) ^ self._shr(w[j - 2], 10)
                w.append((w[j - 16] + s0 + w[j - 7] + s1) & 0xFFFFFFFF)
            
            a, b, c, d, e, f, g, h = H
            
            for j in range(64):
                S1 = self._rotr(e, 6) ^ self._rotr(e, 11) ^ self._rotr(e, 25)
                ch = (e & f) ^ ((~e) & g)
                temp1 = (h + S1 + ch + self.K[j] + w[j]) & 0xFFFFFFFF
                S0 = self._rotr(a, 2) ^ self._rotr(a, 13) ^ self._rotr(a, 22)
                maj = (a & b) ^ (a & c) ^ (b & c)
                temp2 = (S0 + maj) & 0xFFFFFFFF
                
                h = g
                g = f
                f = e
                e = (d + temp1) & 0xFFFFFFFF
                d = c
                c = b
                b = a
                a = (temp1 + temp2) & 0xFFFFFFFF
            
            H[0] = (H[0] + a) & 0xFFFFFFFF
            H[1] = (H[1] + b) & 0xFFFFFFFF
            H[2] = (H[2] + c) & 0xFFFFFFFF
            H[3] = (H[3] + d) & 0xFFFFFFFF
            H[4] = (H[4] + e) & 0xFFFFFFFF
            H[5] = (H[5] + f) & 0xFFFFFFFF
            H[6] = (H[6] + g) & 0xFFFFFFFF
            H[7] = (H[7] + h) & 0xFFFFFFFF
        
        return '{:08x}{:08x}{:08x}{:08x}{:08x}{:08x}{:08x}{:08x}'.format(*H)


def sha2_sifrele(mesaj):
    sha = SHA256()
    return sha.hash(mesaj)

