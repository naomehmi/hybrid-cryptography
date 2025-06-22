# cryptography hybrid assignment

## requirement

- AES 128 encryption and decryption
- RSA encryption and decryption 
- SHA 256 hashing
- Schnorr digital signing and verifying

## input

- original message, 16 chars combination of student ID and name
- AES key, 16 chars random string
- 16 to 32 bit integers for RSA and Schnorr keys 

## process

- sender encrypts original message using AES 128 algorithm 
- sender encrypts AES key using RSA algorithm (using receiver's public RSA key)
- sender signs hashed original message using SHA256 (take only first 4 characters) and Schnorr (using sender's private Schnorr key)
- sender sends receiver a concatenation of cipher message, cipher AES key, and digital signature
- receiver decrypts cipher AES key to get original AES 128 key using RSA algorithm (using receiver's private RSA key)
- receiver decrypts cipher message using the decrypted AES 128 key using AES 128 algorithm
- receiver hashes decrypted message using SHA 256
- receiver verifies signature using Schnorr (using sender's public Schnoor key)

## output

- validity of the message

## yaps

- tried my best to use oop smh
- utils function kinda overcrowded ngl
- generating prime numbers using a combination of sieve of erasthotenes algorithm and miller-rabin 