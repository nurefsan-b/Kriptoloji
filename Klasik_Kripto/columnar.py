def columnar_sifrele(metin, anahtar):
    anahtar_sirasi = []
    sorted_anahtar = sorted(enumerate(anahtar), key=lambda x: x[1])
    for i, (orijinal_index, _) in enumerate(sorted_anahtar):
        anahtar_sirasi.append(orijinal_index)
    
    sutun_sayisi = len(anahtar)
    
    dolgu = (sutun_sayisi - len(metin) % sutun_sayisi) % sutun_sayisi
    metin += 'X' * dolgu
    
    satir_sayisi = len(metin) // sutun_sayisi
    
    matris = []
    for i in range(satir_sayisi):
        satir = metin[i * sutun_sayisi:(i + 1) * sutun_sayisi]
        matris.append(list(satir))
    
    sifreli_metin = ""
    for i in range(sutun_sayisi):
        sutun_index = anahtar_sirasi.index(i)
        for satir in matris:
            sifreli_metin += satir[sutun_index]
    
    return sifreli_metin


def columnar_desifre(sifreli_metin, anahtar):
    anahtar_sirasi = []
    sorted_anahtar = sorted(enumerate(anahtar), key=lambda x: x[1])
    for i, (orijinal_index, _) in enumerate(sorted_anahtar):
        anahtar_sirasi.append(orijinal_index)
    
    sutun_sayisi = len(anahtar)
    satir_sayisi = len(sifreli_metin) // sutun_sayisi
    
    sutunlar = []
    for i in range(sutun_sayisi):
        sutunlar.append([''] * satir_sayisi)
    
    index = 0
    for i in range(sutun_sayisi):
        sutun_index = anahtar_sirasi.index(i)
        for j in range(satir_sayisi):
            sutunlar[sutun_index][j] = sifreli_metin[index]
            index += 1
    
    cozulmus_metin = ""
    for i in range(satir_sayisi):
        for j in range(sutun_sayisi):
            cozulmus_metin += sutunlar[j][i]
    
    cozulmus_metin = cozulmus_metin.rstrip('X')
    
    return cozulmus_metin
