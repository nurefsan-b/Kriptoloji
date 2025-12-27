import secrets
from Klasik_Kripto.sha2 import sha2_sifrele

def _gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def _mod_tersi(a, m):
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    gcd, x, _ = extended_gcd(a % m, m)
    if gcd != 1:
        return None
    return (x % m + m) % m


def _asal_mi(n, k=5):
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    def tanik_testi(a):
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            return True
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                return True
        return False
    
    for _ in range(k):
        a = secrets.randbelow(n - 4) + 2
        if not tanik_testi(a):
            return False
    return True


def _rastgele_asal(bit_uzunlugu):
    while True:
        n = secrets.randbits(bit_uzunlugu)
        n |= (1 << (bit_uzunlugu - 1)) | 1
        
        if _asal_mi(n):
            return n


def rsa_anahtar_uret(bit_uzunlugu=512):
    p = _rastgele_asal(bit_uzunlugu // 2)
    q = _rastgele_asal(bit_uzunlugu // 2)
    
    while p == q:
        q = _rastgele_asal(bit_uzunlugu // 2)
    
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = 65537
    while _gcd(e, phi) != 1:
        e += 2
    
    d = _mod_tersi(e, phi)
    
    return (e, n), (d, n)


def rsa_sifrele(metin, public_key):
    """
    Standart RSA şifreleme (Textbook).
    Güvenlik için PKCS#1 padding kullanılmalıdır, bu eğitim amaçlıdır.
    """
    e, n = public_key
    sifreli = []
    for char in metin:
        m = ord(char)
        c = pow(m, e, n)
        sifreli.append(c)
    return sifreli


def rsa_desifre(sifreli_liste, private_key):
    d, n = private_key
    cozulmus_metin = ""
    for c in sifreli_liste:
        m = pow(c, d, n)
        cozulmus_metin += chr(m)
    return cozulmus_metin


def rsa_sifrele_metin(metin, public_key):
    sifreli = rsa_sifrele(metin, public_key)
    return ','.join(map(str, sifreli))


def rsa_desifre_metin(sifreli_metin, private_key):
    sifreli_liste = [int(x) for x in sifreli_metin.split(',')]
    return rsa_desifre(sifreli_liste, private_key)


def rsa_imzala(metin, private_key):
    """
    Mesajı imzalar. (Hash + RSA Sign)
    """
    d, n = private_key
    ozet_hex = sha2_sifrele(metin)
    ozet_int = int(ozet_hex, 16)
    
    imza = pow(ozet_int, d, n)
    return hex(imza)[2:]


def rsa_dogrula(metin, imza_hex, public_key):
    """
    İmzayı doğrular.
    """
    e, n = public_key
    imza_int = int(imza_hex, 16)
    
    ozet_int_verify = pow(imza_int, e, n)
    
    ozet_hex = sha2_sifrele(metin)
    ozet_int_original = int(ozet_hex, 16)
    
    return ozet_int_verify == ozet_int_original
