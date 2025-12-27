def hill_sifrele(metin, anahtar_matris):
    metin = ''.join([c.upper() for c in metin if c.isalpha()])
    
    n = len(anahtar_matris)
    
    dolgu = (n - len(metin) % n) % n
    metin += 'X' * dolgu
    
    sifreli_metin = ""
    
    for i in range(0, len(metin), n):
        blok = metin[i:i + n]
        blok_sayilar = [ord(c) - ord('A') for c in blok]
        
        sonuc = []
        for satir in range(n):
            toplam = 0
            for sutun in range(n):
                toplam += anahtar_matris[satir][sutun] * blok_sayilar[sutun]
            sonuc.append(toplam % 26)
        
        for s in sonuc:
            sifreli_metin += chr(s + ord('A'))
    
    return sifreli_metin


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


def _determinant_2x2(matris):
    return matris[0][0] * matris[1][1] - matris[0][1] * matris[1][0]


def _determinant_3x3(matris):
    return (matris[0][0] * (matris[1][1] * matris[2][2] - matris[1][2] * matris[2][1])
            - matris[0][1] * (matris[1][0] * matris[2][2] - matris[1][2] * matris[2][0])
            + matris[0][2] * (matris[1][0] * matris[2][1] - matris[1][1] * matris[2][0]))


def _ters_matris_2x2(matris):
    det = _determinant_2x2(matris) % 26
    det_tersi = _mod_tersi(det, 26)
    
    if det_tersi is None:
        return None
    
    ters = [
        [(matris[1][1] * det_tersi) % 26, ((-matris[0][1]) * det_tersi) % 26],
        [((-matris[1][0]) * det_tersi) % 26, (matris[0][0] * det_tersi) % 26]
    ]
    
    return ters


def _ters_matris_3x3(matris):
    det = _determinant_3x3(matris) % 26
    det_tersi = _mod_tersi(det, 26)
    
    if det_tersi is None:
        return None
    
    kofaktor = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    
    for i in range(3):
        for j in range(3):
            minor = []
            for mi in range(3):
                if mi == i:
                    continue
                satir = []
                for mj in range(3):
                    if mj == j:
                        continue
                    satir.append(matris[mi][mj])
                minor.append(satir)
            
            kofaktor[i][j] = ((-1) ** (i + j)) * _determinant_2x2(minor)
    
    adjoint = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for i in range(3):
        for j in range(3):
            adjoint[i][j] = kofaktor[j][i]
    
    ters = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for i in range(3):
        for j in range(3):
            ters[i][j] = (adjoint[i][j] * det_tersi) % 26
    
    return ters


def hill_desifre(sifreli_metin, anahtar_matris):
    n = len(anahtar_matris)
    
    if n == 2:
        ters_matris = _ters_matris_2x2(anahtar_matris)
    elif n == 3:
        ters_matris = _ters_matris_3x3(anahtar_matris)
    else:
        raise ValueError("Sadece 2x2 ve 3x3 matrisler destekleniyor")
    
    if ters_matris is None:
        raise ValueError("Anahtar matrisin tersi bulunamadı")
    
    sifreli_metin = ''.join([c.upper() for c in sifreli_metin if c.isalpha()])
    
    cozulmus_metin = ""
    
    for i in range(0, len(sifreli_metin), n):
        blok = sifreli_metin[i:i + n]
        blok_sayilar = [ord(c) - ord('A') for c in blok]
        
        sonuc = []
        for satir in range(n):
            toplam = 0
            for sutun in range(n):
                toplam += ters_matris[satir][sutun] * blok_sayilar[sutun]
            sonuc.append(toplam % 26)
        
        for s in sonuc:
            cozulmus_metin += chr(s + ord('A'))
    
    return cozulmus_metin
