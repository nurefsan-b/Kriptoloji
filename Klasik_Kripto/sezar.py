alfabe="abcdefghijklmnopqrstuvwxyz"


def sifrele(metin,key):
    cipher_text=''
    metin=metin.lower()
    for x in metin:
        index=alfabe.find(x)
        index=(index+key)%len(alfabe)
        cipher_text=cipher_text+alfabe[index]
    return cipher_text

def desifrele(cipher_text,key):
    metin=''
    for x in cipher_text:
        index=alfabe.find(x)
        index=(index-key)%len(alfabe)
        metin=metin+alfabe[index]
    return metin
