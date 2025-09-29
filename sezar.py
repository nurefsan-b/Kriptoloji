alfabe="abcdefghijklmnopqrstuvwxyz"
key=4

def sifrele(metin):
    cipher_text=''
    metin=metin.lower()
    for x in metin:
        index=alfabe.find(x)
        index=(index+key)%len(alfabe)
        cipher_text=cipher_text+alfabe[index]
    return cipher_text

def desifrele(cipher_text):
    metin=''
    for x in cipher_text:
        index=alfabe.find(x)
        index=(index-key)%len(alfabe)
        metin=metin+alfabe[index]
    return metin

mesaj="merhaba"
sifreli_mesaj=sifrele(mesaj)
print("Şifreli mesaj:",sifreli_mesaj)
desifreli_mesaj=desifrele(sifreli_mesaj)
print("Deşifreli mesaj:",desifreli_mesaj)
