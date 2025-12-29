"""
Playfair Şifresi, bir yerine harf çiftlerini (digraphs) değiştirerek çalışan bir ikame (substitution) şifresidir.
Sezar Şifresi gibi tek harf yerine çiftlerle çalışması, şifrenin kırılmasını çok daha zor hale getirir.
Tek harfte 26 olasılık varken, harf çiftlerinde $26 \times 26 = 676$ olası kombinasyon vardır. 
Playfair, 1800'lerde büyük bir gelişmeydi.

Adım 1: Playfair Karesini Oluşturma
Playfair Şifresi, 5x5'lik bir harf ızgarası (toplam 25 yuva) kullanır.
İngiliz alfabesi 26 harf olduğu için, I ve J harfleri aynı kabul edilir (genellikle J, I ile değiştirilir).
Kare Nasıl Oluşturulur:
Gizli bir anahtar kelime veya ifade seçilir.
Bu anahtar kelime (yinelenenler atlanarak) ızgaraya yazılır.
Alfabenin kalan harfleri (I ve J birleştirilerek) sırayla doldurulur.

Adım 2: Mesajı Hazırlama
Şifrelemeden önce düz metin temizlenmeli ve harf çiftlerine ayrılmalıdır.
Kurallar:
Boşluk, noktalama ve sayıları kaldırın.
Tüm harfleri büyük harfe çevirin.
J harfini I ile değiştirin.
Metni çiftlere (digraphs) ayırın.
Bir çifttteki iki harf aynıysa (örneğin LL), aralarına bir X ekleyin (örneğin LX).
Eğer toplam harf sayısı tek ise, sonuna bir X ekleyin (dolgu/padding).

Adım 3: Şifreleme KurallarıHer harf çifti (A, T gibi) Playfair Karesi kullanılarak şifrelenir.
Üç olası durum vardır:
    Kural 1: 
Aynı Satır (Same Row)İki harf aynı satırdaysa, her harfi sağındaki harfle değiştirin 
satır sonuna gelindiğinde başa dönülür
    Kural 2: 
Aynı Sütun (Same Column)İki harf aynı sütundaysa, her harfi altındaki harfle değiştirin 
(sütun sonuna gelindiğinde başa dönülür)
    Kural 3: 
Dikdörtgen Kuralı (Rectangle Rule)Harfler bir dikdörtgenin köşelerini oluşturuyorsa, 
her harf kendi satırında ancak diğer harfin sütununda bulunan harfle değiştirilir (köşe değiştirme).
Adım 4: Deşifreleme Kuralları (Decryption)Deşifreleme, şifrelemenin tam tersidir:
Aynı Satır: Harfi solundaki harfle değiştirin.Aynı Sütun: Harfi üstündeki harfle değiştirin.
Dikdörtgen: Köşeleri tekrar değiştirin.Son olarak, yapay olarak eklenmiş X dolgu harfleri metinden çıkarılır.
"""
import string

def generate_playfair_square(key):
    key = "".join([c.upper() for c in key if c.isalpha()])
    key = key.replace("J", "I")
    seen = set()
    square = []
    for c in key + string.ascii_uppercase:
        if c not in seen and c != "J":
            seen.add(c)
            square.append(c)
    return [square[i * 5 : (i + 1) * 5] for i in range(5)]

def prepare_text(text, for_encrypt=True):
    text = "".join([c.upper() for c in text if c.isalpha()])
    text = text.replace("J", "I")
    result = ""
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i + 1] if i + 1 < len(text) else "X"
        if a == b:
            result += a + "X"
            i += 1
        else:
            result += a + b
            i += 2
    if len(result) % 2 != 0:
        result += "X"
    return result

def find_position(square, char):
    for i, row in enumerate(square):
        if char in row:
            return i, row.index(char)
    return None

def playfair_encrypt(plaintext, key):
    square = generate_playfair_square(key)
    text = prepare_text(plaintext)
    result = ""
    for i in range(0, len(text), 2):
        a, b = text[i], text[i + 1]
        r1, c1 = find_position(square, a)
        r2, c2 = find_position(square, b)
        if r1 == r2:  
            result += square[r1][(c1 + 1) % 5] + square[r2][(c2 + 1) % 5]
        elif c1 == c2: 
            result += square[(r1 + 1) % 5][c1] + square[(r2 + 1) % 5][c2]
        else:  
            result += square[r1][c2] + square[r2][c1]
    return result

def playfair_decrypt(ciphertext, key):
    square = generate_playfair_square(key)
    result = ""
    for i in range(0, len(ciphertext), 2):
        a, b = ciphertext[i], ciphertext[i + 1]
        r1, c1 = find_position(square, a)
        r2, c2 = find_position(square, b)
        if r1 == r2: 
            result += square[r1][(c1 - 1) % 5] + square[r2][(c2 - 1) % 5]
        elif c1 == c2: 
            result += square[(r1 - 1) % 5][c1] + square[(r2 - 1) % 5][c2]
        else:  
            result += square[r1][c2] + square[r2][c1]
    return result

