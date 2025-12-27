def route_sifrele(metin, satir_sayisi, sutun_sayisi):
    toplam = satir_sayisi * sutun_sayisi
    dolgu = toplam - len(metin)
    if dolgu > 0:
        metin += 'X' * dolgu
    
    matris = []
    index = 0
    for i in range(satir_sayisi):
        satir = []
        for j in range(sutun_sayisi):
            if index < len(metin):
                satir.append(metin[index])
                index += 1
            else:
                satir.append('X')
        matris.append(satir)
    
    sifreli_metin = ""
    ust, alt = 0, satir_sayisi - 1
    sol, sag = 0, sutun_sayisi - 1
    
    while ust <= alt and sol <= sag:
        for i in range(sol, sag + 1):
            sifreli_metin += matris[ust][i]
        ust += 1
        
        for i in range(ust, alt + 1):
            sifreli_metin += matris[i][sag]
        sag -= 1
        
        if ust <= alt:
            for i in range(sag, sol - 1, -1):
                sifreli_metin += matris[alt][i]
            alt -= 1
        
        if sol <= sag:
            for i in range(alt, ust - 1, -1):
                sifreli_metin += matris[i][sol]
            sol += 1
    
    return sifreli_metin


def route_desifre(sifreli_metin, satir_sayisi, sutun_sayisi):
    toplam = satir_sayisi * sutun_sayisi
    
    matris = [['' for _ in range(sutun_sayisi)] for _ in range(satir_sayisi)]
    
    ust, alt = 0, satir_sayisi - 1
    sol, sag = 0, sutun_sayisi - 1
    index = 0
    
    while ust <= alt and sol <= sag and index < len(sifreli_metin):
        for i in range(sol, sag + 1):
            if index < len(sifreli_metin):
                matris[ust][i] = sifreli_metin[index]
                index += 1
        ust += 1
        
        for i in range(ust, alt + 1):
            if index < len(sifreli_metin):
                matris[i][sag] = sifreli_metin[index]
                index += 1
        sag -= 1
        
        if ust <= alt:
            for i in range(sag, sol - 1, -1):
                if index < len(sifreli_metin):
                    matris[alt][i] = sifreli_metin[index]
                    index += 1
            alt -= 1
        
        if sol <= sag:
            for i in range(alt, ust - 1, -1):
                if index < len(sifreli_metin):
                    matris[i][sol] = sifreli_metin[index]
                    index += 1
            sol += 1
    
    cozulmus_metin = ""
    for satir in matris:
        for char in satir:
            cozulmus_metin += char
    
    cozulmus_metin = cozulmus_metin.rstrip('X')
    
    return cozulmus_metin
