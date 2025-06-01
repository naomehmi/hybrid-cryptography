from utils import inverse_mod, fast_mod_exp, generate_valid_d, generate_large_primes

class RSA:
    @staticmethod
    def key_gen():
        p, q = generate_large_primes(31, 2)
        n = p * q
        totient_n = (p-1) * (q-1)
        d = generate_valid_d(p, q, totient_n)
        e = inverse_mod(d, totient_n)

        # private = p, q, d
        # public = n, d
        return (p, q, d), (n, e)

    @staticmethod
    def encrypt(plaintext: str, public_key: tuple[int, int]):
        n, e = public_key
        b = n.bit_length() - 1
        plaintextBin = ''.join([format(ord(p), '08b') for p in plaintext])
        
        # divide into b blocks
        m = [ int(plaintextBin[i:i+b].ljust(b, '0'), 2) for i in range(0, len(plaintextBin), b) ]        
        c = [ fast_mod_exp(i, e, n) for i in m ]
        return ','.join(map(str, c))
    
    @staticmethod
    def decrypt(cipherText: str, private_key: tuple[int, int, int]):
        p, q, d = private_key
        n = p * q
        b = n.bit_length() - 1
        cipherBlocks = list(map(int, cipherText.split(',')))
        m = [ fast_mod_exp(i, d, n) for i in cipherBlocks ]
        plaintextBin = ''.join([format(i, f"0{b}b") for i in m])
        plaintextAscii = [ int(plaintextBin[i:i+8], 2) for i in range(0, len(plaintextBin), 8) ]
        plaintext = ''.join([chr(i) for i in plaintextAscii])
        return plaintext