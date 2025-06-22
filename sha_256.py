from utils import generate_hash_values, generate_rounded_values, right_rotate

class SHA_256_custom:
    k = generate_rounded_values()

    def hash(self, message: str):
        hashValues = generate_hash_values()

        # Convert message to binary
        message_bits = ''.join(format(ord(c), '08b') for c in message)
        original_length = len(message_bits)

        # Append '1' bit
        message_bits += '1'

        # Pad with zeros until length ≡ 448 mod 512
        while (len(message_bits) + 64) % 512 != 0:
            message_bits += '0'

        # Append original length as 64-bit big-endian integer
        message_bits += format(original_length, '064b')

        # Process in 512-bit blocks
        for i in range(0, len(message_bits), 512):
            block = message_bits[i:i+512]
            
            # Break block into sixteen 32-bit words (w0-w15)
            w = [int(block[j:j+32], 2) for j in range(0, 512, 32)]

            # Extend to 64 words (w16-w63)
            for j in range(16, 64):
                s0 = right_rotate(w[j-15], 7) ^ right_rotate(w[j-15], 18) ^ (w[j-15] >> 3)
                s1 = right_rotate(w[j-2], 17) ^ right_rotate(w[j-2], 19) ^ (w[j-2] >> 10)
                w.append((w[j-16] + s0 + w[j-7] + s1) & 0xFFFFFFFF)

            a, b, c, d, e, f, g, h = hashValues

            for j in range(64):
                S1 = right_rotate(e, 6) ^ right_rotate(e, 11) ^ right_rotate(e, 25)
                ch = (e & f) ^ (~e & g)
                temp1 = (h + S1 + ch + self.k[j] + w[j]) & 0xFFFFFFFF
                S0 = right_rotate(a, 2) ^ right_rotate(a, 13) ^ right_rotate(a, 22)
                maj = (a & b) ^ (a & c) ^ (b & c)
                temp2 = (S0 + maj) & 0xFFFFFFFF

                h = g
                g = f
                f = e
                e = (d + temp1) & 0xFFFFFFFF
                d = c
                c = b
                b = a
                a = (temp1 + temp2) & 0xFFFFFFFF

            # Add to hash values
            hashValues = [
                (hashValues[0] + a) & 0xFFFFFFFF,
                (hashValues[1] + b) & 0xFFFFFFFF,
                (hashValues[2] + c) & 0xFFFFFFFF,
                (hashValues[3] + d) & 0xFFFFFFFF,
                (hashValues[4] + e) & 0xFFFFFFFF,
                (hashValues[5] + f) & 0xFFFFFFFF,
                (hashValues[6] + g) & 0xFFFFFFFF,
                (hashValues[7] + h) & 0xFFFFFFFF,
            ]

        # Final digest
        digest = ''.join(format(hv, '08x') for hv in hashValues)
        return digest[:4]
from utils import generate_hash_values, generate_rounded_values, right_rotate

class SHA_256_custom:
    k = generate_rounded_values()

    def hash(self, message: str):
        hashValues = generate_hash_values()

        # Convert message to binary
        message_bits = ''.join(format(ord(c), '08b') for c in message)
        original_length = len(message_bits)

        # Append '1' bit
        message_bits += '1'

        # Pad with zeros until length ≡ 448 mod 512
        while (len(message_bits) + 64) % 512 != 0:
            message_bits += '0'

        # Append original length as 64-bit big-endian integer
        message_bits += format(original_length, '064b')

        # Process in 512-bit blocks
        for i in range(0, len(message_bits), 512):
            block = message_bits[i:i+512]
            
            # Break block into sixteen 32-bit words (w0-w15)
            w = [int(block[j:j+32], 2) for j in range(0, 512, 32)]

            # Extend to 64 words (w16-w63)
            for j in range(16, 64):
                s0 = right_rotate(w[j-15], 7) ^ right_rotate(w[j-15], 18) ^ (w[j-15] >> 3)
                s1 = right_rotate(w[j-2], 17) ^ right_rotate(w[j-2], 19) ^ (w[j-2] >> 10)
                w.append((w[j-16] + s0 + w[j-7] + s1) & 0xFFFFFFFF)

            a, b, c, d, e, f, g, h = hashValues

            for j in range(64):
                S1 = right_rotate(e, 6) ^ right_rotate(e, 11) ^ right_rotate(e, 25)
                ch = (e & f) ^ (~e & g)
                temp1 = (h + S1 + ch + self.k[j] + w[j]) & 0xFFFFFFFF
                S0 = right_rotate(a, 2) ^ right_rotate(a, 13) ^ right_rotate(a, 22)
                maj = (a & b) ^ (a & c) ^ (b & c)
                temp2 = (S0 + maj) & 0xFFFFFFFF

                h = g
                g = f
                f = e
                e = (d + temp1) & 0xFFFFFFFF
                d = c
                c = b
                b = a
                a = (temp1 + temp2) & 0xFFFFFFFF

            # Add to hash values
            hashValues = [
                (hashValues[0] + a) & 0xFFFFFFFF,
                (hashValues[1] + b) & 0xFFFFFFFF,
                (hashValues[2] + c) & 0xFFFFFFFF,
                (hashValues[3] + d) & 0xFFFFFFFF,
                (hashValues[4] + e) & 0xFFFFFFFF,
                (hashValues[5] + f) & 0xFFFFFFFF,
                (hashValues[6] + g) & 0xFFFFFFFF,
                (hashValues[7] + h) & 0xFFFFFFFF,
            ]

        # Final digest
        digest = ''.join(format(hv, '08x') for hv in hashValues)
        return digest[:4]