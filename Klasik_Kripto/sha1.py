import math

class SHA1:
    def __init__(self):
        self._generate_constants()

    def _get_fractional_bits(self, n, root_power, scalar=1.0):
        val = scalar * (n ** (1 / root_power))

        return int(val * (2 ** 30)) & 0xFFFFFFFF

    def _generate_constants(self):

        self.Ks = [
            int(math.sqrt(2) * (2 ** 30)) & 0xFFFFFFFF,
            int(math.sqrt(3) * (2 ** 30)) & 0xFFFFFFFF,
            int(math.sqrt(5) * (2 ** 30)) & 0xFFFFFFFF,
            int(math.sqrt(10) * (2 ** 30)) & 0xFFFFFFFF
        ]
    
        self.H_INIT = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]

    def _rotl(self, n, b):
        return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF

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
            
            for j in range(16, 80):
                w.append(self._rotl(w[j - 3] ^ w[j - 8] ^ w[j - 14] ^ w[j - 16], 1))
            
            a, b, c, d, e = H
            
            for j in range(80):
                if 0 <= j <= 19:
                    f = (b & c) | ((~b) & d)
                    k = self.Ks[0]
                elif 20 <= j <= 39:
                    f = b ^ c ^ d
                    k = self.Ks[1]
                elif 40 <= j <= 59:
                    f = (b & c) | (b & d) | (c & d)
                    k = self.Ks[2]
                else:
                    f = b ^ c ^ d
                    k = self.Ks[3]
                
                temp = (self._rotl(a, 5) + f + e + k + w[j]) & 0xFFFFFFFF
                e = d
                d = c
                c = self._rotl(b, 30)
                b = a
                a = temp
            
            H[0] = (H[0] + a) & 0xFFFFFFFF
            H[1] = (H[1] + b) & 0xFFFFFFFF
            H[2] = (H[2] + c) & 0xFFFFFFFF
            H[3] = (H[3] + d) & 0xFFFFFFFF
            H[4] = (H[4] + e) & 0xFFFFFFFF
        
        return '{:08x}{:08x}{:08x}{:08x}{:08x}'.format(*H)

def sha1_sifrele(mesaj):
    sha = SHA1()
    return sha.hash(mesaj)
