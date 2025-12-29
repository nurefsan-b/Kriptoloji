from Klasik_Kripto.hill import hill_sifrele, hill_desifre
from Klasik_Kripto.rotate import rotate_sifrele, rotate_desifre
from Klasik_Kripto.sha1 import sha1_sifrele
from Klasik_Kripto.sha2 import sha2_sifrele
from Klasik_Kripto.aes import aes_sifrele, aes_desifre
from Klasik_Kripto.rsa import rsa_sifrele_metin, rsa_desifre_metin, rsa_anahtar_uret, rsa_imzala, rsa_dogrula
from Klasik_Kripto.columnar import columnar_sifrele, columnar_desifre
from Klasik_Kripto.ecc import EllipticCurve
from Klasik_Kripto.des import des_sifrele, des_desifre
from Klasik_Kripto.route import route_sifrele, route_desifre
from Klasik_Kripto.sezar import sifrele as sezar_sifrele, desifrele as sezar_desifrele
from Klasik_Kripto.vigenere import vigenere_sifreleme, vigenere_desifreleme
from Klasik_Kripto.substitution import substitution_sifrele, substitution_desifrele
from Klasik_Kripto.affine import affine_sifrele, affine_desifrele
from Klasik_Kripto.playfair import playfair_encrypt, playfair_decrypt
from Klasik_Kripto.polybius import polybius_sifrele, polybius_desifrele
from Klasik_Kripto.rail_fence import rail_fence_sifrele, rail_fence_desifrele
from Klasik_Kripto.pigpen import pigpen_sifrele, pigpen_desifrele
from Klasik_Kripto.pigpen import pigpen_sifrele, pigpen_desifrele
from Crypto.Cipher import AES as LibAES
from Crypto.Cipher import DES as LibDES
from Crypto.Util.Padding import unpad
import base64

def aes_desifre_lib(ciphertext_b64, key):
    try:
        if len(key) not in [16, 24, 32]:
             key = (key + '\0'*16)[:16]
        
        key_bytes = key.encode('utf-8')
        cipher = LibAES.new(key_bytes, LibAES.MODE_ECB)
        data = base64.b64decode(ciphertext_b64)
        decrypted = cipher.decrypt(data)
        return unpad(decrypted, LibAES.block_size).decode('utf-8')
    except Exception as e:
        return f"Library Decryption Error: {e}"

def des_desifre_lib(ciphertext_b64, key):
    try:
        if len(key) != 8:
             key = (key + '\0'*8)[:8]
        
        key_bytes = key.encode('utf-8')
        cipher = LibDES.new(key_bytes, LibDES.MODE_ECB)
        data = base64.b64decode(ciphertext_b64)
        decrypted = cipher.decrypt(data)
        return unpad(decrypted, LibDES.block_size).decode('utf-8')
    except Exception as e:
        return f"Library Decryption Error: {e}"

class CryptoMethods:
    @staticmethod
    def generate_ecc_keypair():
        return EllipticCurve.generate_keypair()

    @staticmethod
    def compute_ecdh_secret(private_key, other_public_key):
        secret_point = EllipticCurve.scalar_mult(private_key, other_public_key)
        return str(secret_point[0]) 

    @staticmethod
    def sign_message(text, private_key):
        return rsa_imzala(text, private_key)

    @staticmethod
    def verify_signature(text, signature, public_key):
        return rsa_dogrula(text, signature, public_key)

    @staticmethod
    def encrypt(method: str, text: str, key: str) -> str:
        try:
            if method == "hill":
                degerler = list(map(int, key.split(',')))
                if len(degerler) == 4:
                    matris = [[degerler[0], degerler[1]], [degerler[2], degerler[3]]]
                elif len(degerler) == 9:
                    matris = [
                        [degerler[0], degerler[1], degerler[2]],
                        [degerler[3], degerler[4], degerler[5]],
                        [degerler[6], degerler[7], degerler[8]]
                    ]
                else:
                    raise ValueError("Hill anahtarı 4 (2x2) veya 9 (3x3) değer olmalıdır!")
                return hill_sifrele(text, matris)
            elif method == "rotate":
                return rotate_sifrele(text, int(key))
            elif method == "sha1":
                return sha1_sifrele(text)
            elif method == "sha2":
                return sha2_sifrele(text)
            elif method == "aes":
                return aes_sifrele(text, key)
            elif method == "rsa":
                e, n = map(int, key.split(','))
                public_key = (e, n)
                return rsa_sifrele_metin(text, public_key)
            elif method == "columnar":
                return columnar_sifrele(text, key)
            elif method == "des":
                return des_sifrele(text, key)
            elif method == "route":
                try:
                    r, c = map(int, key.split(','))
                    return route_sifrele(text, r, c)
                except ValueError:
                    raise ValueError("Route cipher requires key format 'rows,cols' (e.g. 4,5)")
            elif method == "caesar":
                return sezar_sifrele(text, int(key))
            elif method == "vigenere":
                return vigenere_sifreleme(text, key)
            elif method == "substitution":
                return substitution_sifrele(text, key)
            elif method == "affine":
                a, b = map(int, key.split(','))
                return affine_sifrele(text, a, b)
            elif method == "playfair":
                return playfair_encrypt(text, key)
            elif method == "polybius":
                return polybius_sifrele(text)
            elif method == "rail_fence":
                return rail_fence_sifrele(text, int(key))
            elif method == "pigpen":
                return pigpen_sifrele(text)
            else:
                raise ValueError(f"Unsupported encryption method: {method}")
        except Exception as e:
            print(f"Encryption error: {str(e)}")
            raise ValueError(f"Şifreleme hatası: {str(e)}")

    @staticmethod
    def decrypt(method: str, text: str, key: str, implementation: str = 'manual') -> str:
        try:
            if method == "hill":
                degerler = list(map(int, key.split(',')))
                if len(degerler) == 4:
                    matris = [[degerler[0], degerler[1]], [degerler[2], degerler[3]]]
                elif len(degerler) == 9:
                    matris = [
                        [degerler[0], degerler[1], degerler[2]],
                        [degerler[3], degerler[4], degerler[5]],
                        [degerler[6], degerler[7], degerler[8]]
                    ]
                else:
                    raise ValueError("Hill anahtarı 4 (2x2) veya 9 (3x3) değer olmalıdır!")
                return hill_desifre(text, matris)
            elif method == "rotate":
                return rotate_desifre(text, int(key))
            elif method == "aes":
                if implementation == "library":
                    return aes_desifre_lib(text, key)
                return aes_desifre(text, key)
            elif method == "rsa":
                d, n = map(int, key.split(','))
                private_key = (d, n)
                return rsa_desifre_metin(text, private_key)
            elif method == "columnar":
                return columnar_desifre(text, key)
            elif method == "des":
                if implementation == "library":
                    return des_desifre_lib(text, key)
                return des_desifre(text, key)
            elif method == "route":
                try:
                    r, c = map(int, key.split(','))
                    return route_desifre(text, r, c)
                except ValueError:
                    raise ValueError("Route cipher requires key format 'rows,cols' (e.g. 4,5)")
            elif method == "caesar":
                return sezar_desifrele(text, int(key))
            elif method == "vigenere":
                return vigenere_desifreleme(text, key)
            elif method == "substitution":
                if len(key) != 26:
                    raise ValueError("Substitution anahtarı 26 karakterli olmalıdır!")
                return substitution_desifrele(text, key)
            elif method == "affine":
                try:
                    a, b = map(int, key.split(','))
                    return affine_desifrele(text, a, b)
                except ValueError:
                    raise ValueError("Affine anahtarı 'a,b' formatında olmalıdır!")
            elif method == "playfair":
                return playfair_decrypt(text, key)
            elif method == "polybius":
                return polybius_desifrele(text)
            elif method == "rail_fence":
                return rail_fence_desifrele(text, int(key))
            elif method == "pigpen":
                return pigpen_desifrele(text)
            else:
                raise ValueError(f"Desteklenmeyen şifreleme yöntemi: {method}")
        except Exception as e:
            raise ValueError(f"Deşifreleme hatası: {str(e)}")