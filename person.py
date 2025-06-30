from aes_128 import AES_128
from rsa import RSA
from schnorr import Schnorr
from sha_256 import SHA_256_custom

class Person: 
    def __init__(self):
        self.__schnorr_private_key, self.__schnorr_public_key = Schnorr.key_gen()
        self.__rsa_private_key, self.__rsa_public_key = RSA().key_gen()

    def print_keys(self) -> list[str]:
        return [
            "RSA KEYS",
            "--------",
            "",
            "Private",
            f"p: {self.__rsa_private_key[0]}",
            f"q: {self.__rsa_private_key[1]}",
            f"d: {self.__rsa_private_key[2]}",
            "",
            "Public",
            f"n: {self.__rsa_public_key[0]}",
            f"e: {self.__rsa_public_key[1]}",
            "",
            "SCHNORR KEYS",
            "------------",
            "",
            "Private",
            f"q: {self.__schnorr_private_key[0]}",
            f"x: {self.__schnorr_private_key[1]}",
            "",
            "Public",
            f"p: {self.__schnorr_public_key[0]}",
            f"g: {self.__schnorr_public_key[1]}",
            f"y: {self.__schnorr_public_key[2]}",
        ]

    def get_schnorr_public_keys(self) -> tuple[int, int, int]:
        return self.__schnorr_public_key
    
    def get_rsa_public_keys(self) -> tuple[int, int]:
        return self.__rsa_public_key
    
    def sign_message(self, digest: str) -> str:
        digital_signature = Schnorr.sign(digest, self.__schnorr_private_key, self.__schnorr_public_key)
        return digital_signature
    
    def decrypt_aes_key(self, aes_encrypted_key: str) -> str:
        aes_decrypted_key = RSA.decrypt(aes_encrypted_key, self.__rsa_private_key)
        return aes_decrypted_key