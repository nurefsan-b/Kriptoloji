from Klasik_Kripto.gf import GaloisField

class SBoxGenerator:
    @staticmethod
    def _rotl8(x, shift):
        return ((x << shift) | (x >> (8 - shift))) & 0xFF

    @staticmethod
    def generate():
        sbox = [0] * 256
        inv_sbox = [0] * 256
        
        c = 0x63
        
        for i in range(256):
            s = GaloisField.inverse(i)
            s_affine = s ^ \
                       SBoxGenerator._rotl8(s, 1) ^ \
                       SBoxGenerator._rotl8(s, 2) ^ \
                       SBoxGenerator._rotl8(s, 3) ^ \
                       SBoxGenerator._rotl8(s, 4) ^ \
                       c
            sbox[i] = s_affine
            inv_sbox[s_affine] = i
            
        return sbox, inv_sbox
