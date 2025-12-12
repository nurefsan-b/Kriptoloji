alfabe = 'abcdefghijklmnopqrstuvwxyz'

def substitution_sifrele(plain_text, key):
    plain_text = plain_text.lower()
    key = key.lower()

    cipher_text = ''
    for ch in plain_text:
        if ch in alfabe:
            idx = alfabe.index(ch)
            cipher_text += key[idx]
        else:
            cipher_text += ch
    return cipher_text

def substitution_desifrele(cipher_text, key):
    cipher_text = cipher_text.lower()
    key = key.lower()

    plain_text = ''
    for ch in cipher_text:
        if ch in key:
            idx = key.index(ch)
            plain_text += alfabe[idx]
        else:
            plain_text += ch
    return plain_text

if __name__ == "__main__":
    anahtar = "phqgiumeaylnofdxjkrcvstzwb" 
    metin = "IYIPAZARLAR"
    sifreli = substitution_sifrele(metin, anahtar)
    cozulmus = substitution_desifrele(sifreli, anahtar)

    print("Anahtar:", anahtar)
    print("Girdi:", metin)
    print("Şifreli:", sifreli)      
    print("Çözüldü:", cozulmus)
