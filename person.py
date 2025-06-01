from aes_128 import AES_128
from rsa import RSA
from schnorr import Schnorr
from sha_256 import SHA_256_custom

class Sender:
    __schnorr_private_key, __schnorr_public_key = Schnorr.key_gen()

    def get_schnorr_public_keys(self) -> tuple[int, int, int]:
        return self.__schnorr_public_key

    def send_data_packet(self, aes_key: str, message: str, rsa_public_keys: tuple[int, int]):
        aes_service = AES_128(aes_key)
        sha_service = SHA_256_custom()

        cipher_text = aes_service.encrypt(message)
        cipher_key = RSA.encrypt(aes_key, rsa_public_keys)
        
        digest = sha_service.hash(message)
        digital_signature = Schnorr.sign(digest, self.__schnorr_private_key, self.__schnorr_public_key)

        packet = f"{cipher_key}|{cipher_text}|{digital_signature}"
        return packet

class Receiver:
    __rsa_private_key, __rsa_public_key = RSA.key_gen()

    def get_rsa_public_keys(self) -> tuple[int, int]:
        return self.__rsa_public_key

    def receive_data_packet(self, data_packet: str, schnorr_public_keys: tuple[int, int, int]):
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