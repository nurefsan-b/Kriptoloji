import secrets

class EllipticCurve:
    P = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
    A = -3
    B = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
    Gx = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
    Gy = 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5
    N = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551

    def __init__(self):
        pass

    @staticmethod
    def inverse(num, mod):
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            else:
                gcd, x, y = extended_gcd(b % a, a)
                return gcd, y - (b // a) * x, x
        
        gcd, x, y = extended_gcd(num % mod, mod)
        if gcd != 1:
            raise ValueError("Modular inverse does not exist")
        return (x % mod + mod) % mod

    @staticmethod
    def point_add(p1, p2):
        if p1 is None:
            return p2
        if p2 is None:
            return p1
        
        x1, y1 = p1
        x2, y2 = p2
        
        if x1 == x2 and y1 != y2:
            return None
        
        if x1 == x2:
            m = (3 * x1 * x1 + EllipticCurve.A) * EllipticCurve.inverse(2 * y1, EllipticCurve.P)
        else:
            m = (y1 - y2) * EllipticCurve.inverse(x1 - x2, EllipticCurve.P)
            
        m = m % EllipticCurve.P
        x3 = (m * m - x1 - x2) % EllipticCurve.P
        y3 = (m * (x1 - x3) - y1) % EllipticCurve.P
        
        return (x3, y3)

    @staticmethod
    def scalar_mult(k, point):
        res = None
        addend = point
        
        while k:
            if k & 1:
                res = EllipticCurve.point_add(res, addend)
            addend = EllipticCurve.point_add(addend, addend)
            k >>= 1
        
        return res

    @staticmethod
    def generate_keypair():
        private_key = secrets.randbelow(EllipticCurve.N - 1) + 1
        public_key = EllipticCurve.scalar_mult(private_key, (EllipticCurve.Gx, EllipticCurve.Gy))
        return private_key, public_key
