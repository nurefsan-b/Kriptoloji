alfabe='abcdefghijklmnopqrstuvwxyz'

def vigenere_sifreleme(plain_text,key):
    plain_text=plain_text.lower()
    key=key.lower()
    cipher_text=''
    key_index=0
    for karakter in plain_text:
        index=(alfabe.find(karakter)+alfabe.find(key[key_index]))%len(alfabe)
        cipher_text+=alfabe[index]
        key_index=key_index+1
        if key_index==len(key):
            key_index=0
    return cipher_text

def vigenere_desifreleme(cipher_text,key):
    cipher_text=cipher_text.lower()
    key=key.lower()
    plain_text=''
    key_index=0
    for karakter in cipher_text:
        index=(alfabe.find(karakter)-alfabe.find(key[key_index]))%len(alfabe)
        plain_text+=alfabe[index]
        key_index=key_index+1
        if key_index==len(key):
            key_index=0
    return plain_text