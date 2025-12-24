"""Pigpen Şifresi (Mason Şifresi), harflerin geometrik şekillerle değiştirildiği grafiksel bir 
ikame (substitution) şifresidir. Tarihsel olarak 18. yüzyılda Özgür Masonlar (Freemasons) 
tarafından kayıtlarını gizli tutmak için kullanılmıştır.

Adım 1: Izgara Sistemi (Grid Structure)
Pigpen şifresi alfabeyi 4 farklı ızgaraya böler:
1. Izgara (Noktasız): A-I harfleri, standart bir tic-tac-toe (XOX) tahtasına yerleştirilir.
2. Izgara (Noktalı): J-R harfleri, aynı tahtanın "noktalı" versiyonuna yerleştirilir.
3. Izgara (Çarpı): S-V harfleri, bir X şekline yerleştirilir.
4. Izgara (Noktalı Çarpı): W-Z harfleri, X şeklinin noktalı versiyonuna yerleştirilir.

Adım 2: Sembollerin Oluşumu
Her harf, içinde bulunduğu "hücrenin" sınır çizgileriyle temsil edilir.
Örnekler:
* 'a' harfi: 1. ızgaranın sol üst köşesindedir (bazı varyasyonlarda düzen değişebilir). 
  Standart düzende sağ ve alt çizgisi olan bir köşe şeklindedir (⌋).
* 'e' harfi: 1. ızgaranın tam ortasındadır, bu yüzden bir kare (□) ile temsil edilir.
* 'j' harfi: 'a' ile aynı şekle sahiptir ancak içinde bir nokta bulunur (⌋•).

Adım 3: Şifreleme ve Deşifreleme
Şifreleme: Metindeki her harf, ilgili geometrik şekle dönüştürülür.
Deşifreleme: Grafiksel şekiller tekrar harflere dönüştürülür.

Not: Bu kodda grafiksel şekilleri terminalde gösterebilmek için Unicode karakterler 
(Kutu Çizim Karakterleri) kullanılmıştır.
"""

def pigpen_sifrele(metin):
    metin = metin.lower()
    sifreli_metin = ""
    
    tablo = {
        'a': '⌋', 'b': '⊔', 'c': '⌊',
        'd': '⊐', 'e': '□', 'f': '⊏',
        'g': '┐', 'h': '⊓', 'i': '┌',
        
        'j': '⌋•', 'k': '⊔•', 'l': '⌊•',
        'm': '⊐•', 'n': '□•', 'o': '⊏•',
        'p': '┐•', 'q': '⊓•', 'r': '┌•',
        
        's': 'V',  't': '>', 
        'u': '<',  'v': '∧',
        
        'w': 'V•', 'x': '>•', 
        'y': '<•', 'z': '∧•'
    }
    
    for harf in metin:
        if harf in tablo:
            sifreli_metin += tablo[harf] + " "
        elif harf == " ":
            continue 
            
    return sifreli_metin.strip()

def pigpen_desifrele(sifre):
    tablo = {
        '⌋': 'a', '⊔': 'b', '⌊': 'c',
        '⊐': 'd', '□': 'e', '⊏': 'f',
        '┐': 'g', '⊓': 'h', '┌': 'i',
        
        '⌋•': 'j', '⊔•': 'k', '⌊•': 'l',
        '⊐•': 'm', '□•': 'n', '⊏•': 'o',
        '┐•': 'p', '⊓•': 'q', '┌•': 'r',
        
        'V': 's',  '>': 't', 
        '<': 'u',  '∧': 'v',
        
        'V•': 'w', '>•': 'x', 
        '<•': 'y', '∧•': 'z'
    }
    
    cozulmus_metin = ""
    for sembol in sifre.split():
        if sembol in tablo:
            cozulmus_metin += tablo[sembol]
            
    return cozulmus_metin

if __name__ == "__main__":
    ornek_metin = "gizli mesaj"
    
    print(f"Düz Metin: {ornek_metin}")
    
    sifreli = pigpen_sifrele(ornek_metin)
    print(f"Pigpen Şifreli: {sifreli}")
    
    cozulmus = pigpen_desifrele(sifreli)
    print(f"Çözülmüş Metin: {cozulmus}")