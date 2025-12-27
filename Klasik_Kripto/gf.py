class GaloisField:
    IRREDUCIBLE_POLY = 0x11b

    @staticmethod
    def add(a, b):
        """Adds two numbers in GF(2^8)."""
        return a ^ b

    @staticmethod
    def sub(a, b):
        """Subtracts two numbers in GF(2^8)."""
        return a ^ b

    @staticmethod
    def multiply(a, b):
        """Multiplies two numbers in GF(2^8) modulo the irreducible polynomial."""
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
        """Exponentiation in GF(2^8)."""
        res = 1
        while n > 0:
            if n % 2 == 1:
                res = GaloisField.multiply(res, a)
            a = GaloisField.multiply(a, a)
            n //= 2
        return res

    @staticmethod
    def inverse(a):
        """Finds the multiplicative inverse of a number in GF(2^8)."""
        if a == 0:
            return 0
        return GaloisField.power(a, 254)
