"""Polybius Şifresi (Polybius Karesi), alfabedeki harflerin iki boyutlu bir tabloya yerleştirilip sayısal koordinatlara 
dönüştürülmesine dayanan bir ikame (substitution) şifresidir. Antik Yunan tarihçisi Polybius tarafından geliştirilen 
bu yöntem, metinleri sayısal verilere dökerek görsel sinyallerle (örneğin meşalelerle) uzak mesafelere iletmek için 
tasarlanmıştır.

Adım 1: Polybius Karesini Oluşturma
Polybius Şifresi, genellikle 5x5'lik bir harf ızgarası (toplam 25 yuva) kullanır.
Harf Yerleşimi: İngiliz alfabesindeki 26 harfi 25 yuvaya sığdırmak için I ve J harfleri aynı kareye 
(genellikle 2,4 koordinatına) yerleştirilir.
Izgara Yapısı: Satır ve sütunlar 1'den 5'e kadar numaralandırılır.
Kare Nasıl Doldurulur: Harfler genellikle alfabedeki sırasına göre dizilir, ancak isteğe bağlı olarak 
bir anahtar kelime ile de başlatılabilir.

Adım 2: Mesajı Hazırlama
Şifrelemeden önce düz metin, karedeki karakterlere uygun hale getirilmelidir.
Küçük/Büyük Harf: Genellikle tüm harfler küçük harfe çevrilir.
J-I Dönüşümü: Metindeki tüm 'j' harfleri, karedeki yerini alması için 'i' harfine dönüştürülür.

Temizlik: Alfabe dışı karakterler (boşluklar, noktalamalar) genellikle işleme alınmaz veya kaldırılır.

Adım 3: Şifreleme Kuralları
Her harf, karedeki konumunu temsil eden iki rakamlı bir koordinat çiftine dönüştürülür.

Koordinat Sistemi: İlk rakam harfin bulunduğu satır numarasını, ikinci rakam ise sütun numarasını temsil eder.

Örnek: * 'a' harfi 1. satır ve 1. sütunda olduğu için şifreli metinde "11" olarak yazılır.
'm' harfi 3. satır ve 2. sütunda olduğu için "32" olarak yazılır.

Sonuç: "merhaba" kelimesi, her harf için bir sayı çifti olacak şekilde "32 15 42 23 11 12 11" formatına dönüşür.
Adım 4: Deşifreleme Kuralları (Decryption)
Deşifreleme işlemi, sayı çiftlerini tabloyu kullanarak tekrar harfe çevirme sürecidir:
Gruplama: Şifreli sayı dizisi ikişerli gruplara (çiftlere) ayrılır.
Tablodan Bulma: İlk rakam satır, ikinci rakam sütun olarak kabul edilerek tablodaki karşılık gelen harf seçilir.
Harf Çevrimi: Örneğin "24" çifti görüldüğünde, 2. satır 4. sütundaki 'i' harfi alınır."""

def polybius_sifrele(metin):
    metin = metin.lower().replace('j', 'i')
    sifreli_metin = ""
    tablo = {
        'a': '11', 'b': '12', 'c': '13', 'd': '14', 'e': '15',
        'f': '21', 'g': '22', 'h': '23', 'i': '24', 'k': '25',
        'l': '31', 'm': '32', 'n': '33', 'o': '34', 'p': '35',
        'q': '41', 'r': '42', 's': '43', 't': '44', 'u': '45',
        'v': '51', 'w': '52', 'x': '53', 'y': '54', 'z': '55'
    }
    for harf in metin:
        if harf in tablo:
            sifreli_metin += tablo[harf] + " "
    return sifreli_metin.strip()

def polybius_desifrele(sifre):
    tablo = {
        '11': 'a', '12': 'b', '13': 'c', '14': 'd', '15': 'e',
        '21': 'f', '22': 'g', '23': 'h', '24': 'i', '25': 'k',
        '31': 'l', '32': 'm', '33': 'n', '34': 'o', '35': 'p',
        '41': 'q', '42': 'r', '43': 's', '44': 't', '45': 'u',
        '51': 'v', '52': 'w', '53': 'x', '54': 'y', '55': 'z'
    }
    cozulmus_metin = ""
    for parca in sifre.split():
        if parca in tablo:
            cozulmus_metin += tablo[parca]
    return cozulmus_metin