import hashlib
import secrets
from Klasik_Kripto.ecc import EllipticCurve

class ECDSAManager:
    def __init__(self):
        self.curve = EllipticCurve()
        self.n = EllipticCurve.N
        self.g = (EllipticCurve.Gx, EllipticCurve.Gy)

    def _hash_message(self, message: str) -> int:
        message_bytes = message.encode('utf-8')
        hash_bytes = hashlib.sha256(message_bytes).digest()
        return int.from_bytes(hash_bytes, 'big')

    def sign(self, private_key: int, message: str):
        z = self._hash_message(message)
        while True:
            k = secrets.randbelow(self.n - 1) + 1
            point_p = self.curve.scalar_mult(k, self.g)
            r = point_p[0] % self.n
            if r == 0: continue
            
            try:
                k_inv = self.curve.inverse(k, self.n)
                s = (k_inv * (z + r * private_key)) % self.n
                if s != 0: return (r, s)
            except ValueError: continue

    def verify(self, public_key, message: str, signature: tuple) -> bool:
        r, s = signature
        if not (1 <= r < self.n) or not (1 <= s < self.n): return False
        z = self._hash_message(message)
        try:
            w = self.curve.inverse(s, self.n)
            u1 = (z * w) % self.n
            u2 = (r * w) % self.n
            p1 = self.curve.scalar_mult(u1, self.g)
            p2 = self.curve.scalar_mult(u2, public_key)
            point_p = self.curve.point_add(p1, p2)
            if point_p is None: return False
            return point_p[0] % self.n == r
        except: return False