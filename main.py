from string import ascii_letters, digits
from random import random
from person import Person
from math import floor
from textwrap import wrap
from aes_128 import AES_128
from rsa import RSA
from sha_256 import SHA_256_custom
from schnorr import Schnorr
from steganography import hide_data_in_image, extract_data_from_image
import tkinter as tk
from tkinter import filedialog

def print_step(a_msg=[""], b_msg=[""], width=60):
    if (len(a_msg) != len(b_msg)):
        raise ("The amount of strings are not the same.")
    
    for i in range(len(a_msg)):
        if (a_msg[i] == '' and b_msg[i] == ''):
            print(f"| {'':<{width}} | {'':<{width}} |")
            continue

        a_lines = wrap(a_msg[i], width)
        b_lines = wrap(b_msg[i], width)
        max_lines = max(len(a_lines), len(b_lines))
        
        for i in range(max_lines):
            a_line = a_lines[i] if i < len(a_lines) else ""
            b_line = b_lines[i] if i < len(b_lines) else ""
            print(f"| {a_line:<{width}} | {b_line:<{width}} |")

LETTERS_AND_NUMBERS = ascii_letters + digits + '_'
TOTAL_CHARS = len(LETTERS_AND_NUMBERS)

while True:
    try:
        print()
        print("=" * 127)
        print_step(["Alice (A)"], ["Bob (B)"])
        print("=" * 127)

        print_step(["Input Message from Alice"])
        print_step([
            "- If the message is shorter than 16 characters, the message will be padded with zeros", 
            "- If the message is longer than 16 characters, only the first 16 characters are taken",
            ""
        ], ["", "", ""])

        message = input("| Message: ").strip()

        print_step()

        if (message == ''):
            print_step(["Message is required"])
            continue
    
        if ('|' in message):
            print_step(["| character not allowed"])

        message = message[:16].zfill(16)
        
        alice = Person()
        bob = Person()

        print_step(alice.print_keys(), bob.print_keys())
        print_step()

        print_step(["Encrypting the message with AES128"])
        print_step(["Key Generation:"])
        print_step([
            "- If the key length is shorter than 16 characters, the key will be padded with zeros",
            "- If the key length is longer than 16 characters, only the first 16 characters are taken",
            "- If the user leaves the input empty, a random 16-character key will be generated"
        ], ["", "", ""])
        print_step()

        aes_key = input("| AES128 Key: ").strip()

        if (aes_key == ''):
            aes_key = ''.join([LETTERS_AND_NUMBERS[floor(random() * TOTAL_CHARS)] for _ in range(16)])
        
        if ('|' in aes_key):
            print_step(["| character not allowed"])
        
        aes_key = aes_key[:16].zfill(16)
        
        print_step(["Alice encrypts message using AES128"])
        alice_aes_service = AES_128(aes_key)
        encrypted_message = alice_aes_service.encrypt(message)
        print_step()
        print_step([f"Original Message: {message}"])
        print_step([f"Encrypted Message: {encrypted_message}"])
        print_step()
        
        print_step(["Alice encrypts the AES key with Bob's public RSA key"])
        encrypted_key = RSA.encrypt(aes_key, bob.get_rsa_public_keys())
        print_step()
        print_step([f"Original AES Key: {aes_key}"])
        print_step([f"Encrypted AES Key: {encrypted_key}"])
        print_step()

        print_step(["Alice hashes the original message using SHA256"])
        print_step(["(Taking only the first 4 characters of the hash)"])
        alice_sha_service = SHA_256_custom()
        digest = alice_sha_service.hash(message)
        print_step()
        print_step([f"Original Message: {message}"])
        print_step([f"Message Digest: {digest}"])
        print_step()

        print_step(["Alice signs the digest using her private Schnorr key"])
        digital_signature = alice.sign_message(digest)
        print_step()
        print_step([f"Digest: {digest}"])
        print_step([f"Digital Signature: {digital_signature}"])
        print_step()

        print_step(["Data Packet to be Sent"])
        data_packet = f"{encrypted_key}|{encrypted_message}|{digital_signature}"
        print_step(["format: encrypted key|encrypted message|digital signature"])
        print_step()
        print_step([data_packet])
        print_step()

        break
    except:
        continue

root = tk.Tk()
root.withdraw()  # Hide the main Tk window
root.update() 

while True:
    try:
        input_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("PNG images", "*.png"), ("BMP images", "*.bmp"), ("JPG images", "*.jpg"), ("JPEG images", "*.jpeg")]
        )
        print_step(["Alice Hides Data Packet inside Image (input.png)"])

        if not input_path:
            print_step("Please pick an image")
            continue

        hide_data_in_image(input_path, "output.png", data_packet)
        print_step(["Generated Image: output.png"])
        print_step()

        print_step(["-"*59 + ">"], ["Bob Receives output.png"])
        print_step()

        print_step([""], ["Bob Extracts the Data from output.png"])
        decoded_data = extract_data_from_image("output.png")
        print_step()
        print_step([""], [f"Extracted Data: {decoded_data}"])\
        
        encrypted_key, encrypted_message, digital_signature = decoded_data.split('|')
        digital_signature = digital_signature[:-1] # Remove EOF market

        print_step(["", "", ""], [
            f"Encrypted Key: {encrypted_key}",
            f"Encrypted Message: {encrypted_message}",
            f"Digital Signature: {digital_signature}",
        ])
        print_step()

        print_step([""], ["Bob Decrypts the AES Key with His Private RSA Key"])
        decrypted_key = bob.decrypt_aes_key(encrypted_key)
        print_step([""], [f"Encrypted AES Key: {encrypted_key}"])
        print_step([""], [f"Decrypted AES Key: {decrypted_key}"])
        print_step()

        print_step([""], [f"Bob Decrypts the Message with the Decrypted AES Key"])
        bob_aes_service = AES_128(decrypted_key)
        decrypted_message = bob_aes_service.decrypt(encrypted_message)
        print_step([""], [f"Encrypted Message: {encrypted_message}"])
        print_step([""], [f"Decrypted Message: {decrypted_message}"])
        print_step()
        
        print_step([""], [f"Bob Hashes the Decrypted Message"])
        bob_sha_service = SHA_256_custom()
        digest = bob_sha_service.hash(decrypted_message)
        print_step([""], [f"Original Message: {decrypted_message}"])
        print_step([""], [f"Message Digest: {digest}"])
        print_step()

        print_step([""], [f"Bob Verifies the Signature with Alice's Public Schnorr Key"])
        verification = Schnorr.verify(digest, digital_signature, alice.get_schnorr_public_keys())
        print_step([""], [f"Alice's Signature: {digital_signature}"])
        print_step([""], [f"Verification: {verification}"])

        print_step([""], [f"Thus, the message is: {'VALID' if int(digital_signature.split(',')[0]) == verification else 'NOT VALID'}"])
        print("=" * 127)
    
        break
    except:
        continue