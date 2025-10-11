from Klasik_Kripto.sezar import sifrele as sezar_sifrele, desifrele as sezar_desifrele
from Klasik_Kripto.vigenere import vigenere_sifreleme, vigenere_desifreleme
from Klasik_Kripto.substitution import substitution_sifrele, substitution_desifrele
from Klasik_Kripto.affine import affine_sifrele, affine_desifrele

class CryptoMethods:
    @staticmethod
    def encrypt(method: str, text: str, key: str) -> str:
        try:
            if method == "caesar":
                return sezar_sifrele(text, int(key))
            elif method == "vigenere":
                return vigenere_sifreleme(text, key)
            elif method == "substitution":
                return substitution_sifrele(text, key)
            elif method == "affine":
                a, b = map(int, key.split(','))
                return affine_sifrele(text, a, b)
            else:
                raise ValueError(f"Unsupported encryption method: {method}")
        except Exception as e:
            print(f"Encryption error: {str(e)}")
            return text

    @staticmethod
    def decrypt(method: str, text: str, key: str) -> str:
        try:
            if method == "caesar":
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
            else:
                raise ValueError(f"Desteklenmeyen şifreleme yöntemi: {method}")
        except Exception as e:
            raise ValueError(f"Deşifreleme hatası: {str(e)}")