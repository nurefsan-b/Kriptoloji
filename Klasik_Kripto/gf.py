class GaloisField:
    IRREDUCIBLE_POLY = 0x11b

    @staticmethod
    def add(a, b):
        return a ^ b

    @staticmethod
    def sub(a, b):
        return a ^ b

    @staticmethod
    def multiply(a, b):
        result = 0
        for i in range(8):
            if (b & 1) != 0:
                result ^= a
            
            hi_bit_set = (a & 0x80) != 0
            a <<= 1
            if hi_bit_set:
                a ^= GaloisField.IRREDUCIBLE_POLY
            b >>= 1
        return result & 0xFF

    @staticmethod
    def power(a, n):
        res = 1
        while n > 0:
            if n % 2 == 1:
                res = GaloisField.multiply(res, a)
            a = GaloisField.multiply(a, a)
            n //= 2
        return res

    @staticmethod
    def inverse(a):
        if a == 0:
            return 0
        return GaloisField.power(a, 254)
