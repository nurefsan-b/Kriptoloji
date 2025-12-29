"""Rail Fence Şifresi (Çit/Zikzak Şifresi), harflerin yerlerinin değiştirilmesine (transposition) 
dayanan bir şifreleme yöntemidir. Adını, harflerin hayali bir çit (rail) üzerinde zikzaklar çizerek 
yerleştirilmesinden alır.

Adım 1: Şifreleme Mantığı (Zikzak Oluşturma)
Bu yöntemde bir 'Anahtar' (Ray Sayısı) belirlenir. Düz metin, bu raylar üzerinde aşağı-yukarı 
hareket eden bir dalga (zikzak) şeklinde yazılır.

Örnek Senaryo:
Metin: "merhaba", Anahtar (Ray Sayısı): 2
Yazım Şekli:
m . . . r . . . a . . . a   (1. Ray)
. e . h . b . 
. . . . . . . . . . . . .   (2. Ray - Boşluklar şematik)

Adım 2: Mesajı Hazırlama
Polybius'ta olduğu gibi, karmaşıklığı önlemek için genellikle boşluklar atılır.
Temizlik: Metindeki boşluklar kaldırılır, işlem genellikle ham karakterler üzerinden yapılır.

Adım 3: Şifreli Metni Oluşturma
Zikzak şeklinde yazılan harfler, satır satır (ray ray) okunarak yanyana dizilir.
Yukarıdaki örnek (2 ray) için okuma:
1. Satır: m, r, a, a -> "mraa"
2. Satır: e, h, b   -> "ehb"
Sonuç: "mraaehb"

Adım 4: Deşifreleme Kuralları (Decryption)
Deşifreleme işlemi, şifrelemedeki zikzak yolunu taklit etmeyi gerektirir:
Izgara Kurma: Şifreli metnin uzunluğu ve anahtar sayısı kadar boş bir matris oluşturulur.
Yolu İşaretleme: Zikzak hareketinin izleyeceği rotaya (hücrelere) işaret koyulur.
Doldurma: Şifreli metindeki harfler, satır sırasına göre bu işaretli yerlere yerleştirilir.
Okuma: Matris bu sefer zikzak yolu takip edilerek okunur ve düz metin elde edilir.
"""

def rail_fence_sifrele(metin, ray_sayisi):
    metin = metin.replace(" ", "")
    
    raylar = ['' for _ in range(ray_sayisi)]
    
    yon_asagi = False  
    satir = 0       

    for harf in metin:
        raylar[satir] += harf
        
        if satir == 0 or satir == ray_sayisi - 1:
            yon_asagi = not yon_asagi
        
        if yon_asagi:
            satir += 1
        else:
            satir -= 1
            
    return "".join(raylar)

def rail_fence_desifrele(sifre, ray_sayisi):
    matris = [['\n' for _ in range(len(sifre))] for _ in range(ray_sayisi)]
    yon_asagi = None
    satir, sutun = 0, 0
    
    for _ in range(len(sifre)):
        matris[satir][sutun] = '*'
        sutun += 1
        
        if satir == 0:
            yon_asagi = True
        if satir == ray_sayisi - 1:
            yon_asagi = False
            
        satir += 1 if yon_asagi else -1
        
    index = 0
    for r in range(ray_sayisi):
        for c in range(len(sifre)):
            if matris[r][c] == '*' and index < len(sifre):
                matris[r][c] = sifre[index]
                index += 1
 
    cozulmus_metin = []
    satir, sutun = 0, 0
    for _ in range(len(sifre)):
        cozulmus_metin.append(matris[satir][sutun])
        sutun += 1
        
        if satir == 0:
            yon_asagi = True
        if satir == ray_sayisi - 1:
            yon_asagi = False
            
        satir += 1 if yon_asagi else -1
        
    return "".join(cozulmus_metin)

if __name__ == "__main__":
    ornek_metin = "kriptoloji dersi"
    anahtar = 3
    
    sifreli = rail_fence_sifrele(ornek_metin, anahtar)
    print(f"Metin: {ornek_metin}")
    print(f"Şifreli: {sifreli}")
    
    cozulmus = rail_fence_desifrele(sifreli, anahtar)
    print(f"Çözülmüş: {cozulmus}")