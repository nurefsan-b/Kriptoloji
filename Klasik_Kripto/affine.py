import math

alfabe = "abcdefghijklmnopqrstuvwxyz"
m = len(alfabe)

# Modüler ters bulma (a^-1 mod m)
def mod_inverse(a, m):
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None

def affine_sifrele(plain_text, a, b):
    cipher_text = ""
    for char in plain_text.lower():
        if char in alfabe:
            x = alfabe.index(char)
            y = (a * x + b) % m
            cipher_text += alfabe[y]
    return cipher_text

def affine_desifrele(cipher_text, a, b):
    plain_text = ""
    a_inv = mod_inverse(a, m)
    if a_inv is None:
        raise ValueError(f"a={a} için mod {m} altında ters yok!")
    
    for char in cipher_text.lower():
        if char in alfabe:
            y = alfabe.index(char)
            x = (a_inv * (y - b)) % m
            plain_text += alfabe[x]
        else:
            plain_text += char
    return plain_text
