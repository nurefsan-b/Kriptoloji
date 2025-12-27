def _sol_dondur(n, b):
    return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF


def sha1_sifrele(mesaj):
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0

    if isinstance(mesaj, str):
        mesaj = mesaj.encode('utf-8')
    
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
            w.append(_sol_dondur(w[j - 3] ^ w[j - 8] ^ w[j - 14] ^ w[j - 16], 1))
        
        a, b, c, d, e = h0, h1, h2, h3, h4
        
    
        for j in range(80):
            if 0 <= j <= 19:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif 20 <= j <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= j <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            else:
                f = b ^ c ^ d
                k = 0xCA62C1D6
            
            temp = (_sol_dondur(a, 5) + f + e + k + w[j]) & 0xFFFFFFFF
            e = d
            d = c
            c = _sol_dondur(b, 30)
            b = a
            a = temp
        
        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF
    
    return '{:08x}{:08x}{:08x}{:08x}{:08x}'.format(h0, h1, h2, h3, h4)
