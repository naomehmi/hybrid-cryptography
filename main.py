from string import ascii_letters, digits
from random import random
from person import Sender, Receiver
from math import floor

LETTERS_AND_NUMBERS = ascii_letters + digits + '_'
TOTAL_CHARS = len(LETTERS_AND_NUMBERS)

message = "221111798NaomiPr" # 16 chars, combination of name and NIM
aes_key = ''.join([LETTERS_AND_NUMBERS[floor(random() * TOTAL_CHARS)] for _ in range(16)]) # random 16 char key

sender = Sender()
receiver = Receiver()

packet = sender.send_data_packet(aes_key, message, receiver.get_rsa_public_keys())
validity = receiver.receive_data_packet(packet, sender.get_schnorr_public_keys())