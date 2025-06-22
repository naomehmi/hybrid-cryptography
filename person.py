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
    
    def send_data_packet(self, aes_key: str, message: str, receiver: "Person"):
        rsa_public_keys = receiver.get_rsa_public_keys()
        
        aes_service = AES_128(aes_key)
        sha_service = SHA_256_custom()

        cipher_text = aes_service.encrypt(message)
        cipher_key = RSA.encrypt(aes_key, rsa_public_keys)
        
        digest = sha_service.hash(message)
        digital_signature = Schnorr.sign(digest, self.__schnorr_private_key, self.__schnorr_public_key)

        packet = f"{cipher_key}|{cipher_text}|{digital_signature}"
        return packet
    
    def receive_data_packet(self, data_packet: str, signee: "Person"):
        schnorr_public_keys = signee.get_schnorr_public_keys()

        cipher_key, cipher_text, digital_signature = data_packet.split('|')
        aes_decrypted_key = RSA.decrypt(cipher_key, self.__rsa_private_key)
        
        aes_service = AES_128(aes_decrypted_key)
        sha_service = SHA_256_custom()
        
        message = aes_service.decrypt(cipher_text)
        hashed_message = sha_service.hash(message)
        verify = Schnorr.verify(hashed_message, digital_signature, schnorr_public_keys)

        if (verify):
            return 'valid'
        
        return 'invalid'