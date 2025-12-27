def rotate_sifrele(metin, anahtar):
    sifreli_metin = ""

    for char in metin:
        if char.isalpha():
            ascii_offset = ord('A') if char.isupper() else ord('a')
            yeni_char = chr((ord(char) - ascii_offset + anahtar) % 26 + ascii_offset)
            sifreli_metin += yeni_char
        else:
            sifreli_metin += char

    return sifreli_metin


def rotate_desifre(sifreli_metin, anahtar):
    return rotate_sifrele(sifreli_metin, -anahtar)