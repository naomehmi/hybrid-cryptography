from utils import generate_aes_sbox, gf_mul

class AES_128:
    __Nb = 4  # Block size (4 words = 16 bytes)
    __Nk = 4  # Key length (4 words = 16 bytes)
    __Nr = 10 # Number of rounds
    __forwardSBox, __inverseSBox = generate_aes_sbox()
    
    def __init__(self, key: str):        
        self.__roundKeys = self.__key_scheduling([ord(c) for c in key])

    def __key_scheduling(self, key_bytes):
        def sub_word(word):
            return [self.__forwardSBox[b] for b in word]

        def rot_word(word):
            return word[1:] + word[:1]

        w = []
        for i in range(self.__Nk):
            w.append(key_bytes[4 * i : 4 * (i + 1)])

        rcon = 1
        for i in range(self.__Nk, self.__Nb * (self.__Nr + 1)):
            temp = w[i - 1][:]
            if i % self.__Nk == 0:
                temp = sub_word(rot_word(temp))
                temp[0] ^= rcon
                rcon = gf_mul(rcon, 2)
            w.append([a ^ b for a, b in zip(w[i - self.__Nk], temp)])

        # Convert to round key matrices
        round_keys = []
        for r in range(self.__Nr + 1):
            currentRound = []
            for c in range(4):
                currentRound.append([w[4 * r + c][row] for row in range(4)])
            round_keys.append(currentRound)
        return round_keys

    def encrypt(self, plaintext: str):
        stateArray = [ [ 0 for _ in range(4) ] for _ in range(4) ]
        
        # put plaintext into matrix
        for i in range(16):
            row = i % 4
            col = i // 4
            stateArray[col][row] = ord(plaintext[i])

        # add round key
        for i in range(4):
            for j in range(4):
                stateArray[i][j] ^= self.__roundKeys[0][i][j]

        for i in range(1, self.__Nr + 1):
            # sub bytes
            for j in range(4):
                for k in range(4):
                    stateArray[j][k] = self.__forwardSBox[stateArray[j][k]]
            
            # shift rows
            for r in range(1, 4):
                row = [stateArray[c][r] for c in range(4)]
                row = row[r:] + row[:r]
                for c in range(4):
                    stateArray[c][r] = row[c]
            
            # mix columns
            if (i != self.__Nr):
                for col in range(4):
                    a = stateArray[col]
                    temp = [
                        gf_mul(0x02, a[0]) ^ gf_mul(0x03, a[1]) ^ a[2] ^ a[3],
                        a[0] ^ gf_mul(0x02, a[1]) ^ gf_mul(0x03, a[2]) ^ a[3],
                        a[0] ^ a[1] ^ gf_mul(0x02, a[2]) ^ gf_mul(0x03, a[3]),
                        gf_mul(0x03, a[0]) ^ a[1] ^ a[2] ^ gf_mul(0x02, a[3]),
                    ]
                    for x in range(4):
                        stateArray[col][x] = temp[x]
    
            # add round key
            for j in range(4):
                for k in range(4):
                    stateArray[j][k] ^= self.__roundKeys[i][j][k]
            
        return ''.join(f'{stateArray[c][r]:02x}' for c in range(4) for r in range(4))
    
    def decrypt(self, cipherText: str):
        stateArray = [ [ 0 for _ in range(4) ] for _ in range(4) ]

        for i in range(0, 16 * 2, 2):
            row = (i // 2) % 4
            col = (i // 2) // 4
            stateArray[col][row] = int(cipherText[i:i+2], 16)

        # add round key
        for i in range(4):
            for j in range(4):
                stateArray[i][j] ^= self.__roundKeys[self.__Nr][i][j]

        for i in range(self.__Nr - 1, -1, -1):
            # inv shift rows
            for r in range (1, 4):
                row = [stateArray[c][r] for c in range(4)]
                row = row[-r:] + row[:-r]
                for c in range(4):
                    stateArray[c][r] = row[c]

            # inv sub bytes
            for j in range(4):
                for k in range(4):
                    stateArray[j][k] = self.__inverseSBox[stateArray[j][k]]

            # add round key
            for j in range(4):
                for k in range(4):
                    stateArray[j][k] ^= self.__roundKeys[i][j][k]

            # inv mix columns
            if (i != 0):
                for col in range(4):
                    a = stateArray[col]
                    temp = [
                        gf_mul(0x0e, a[0]) ^ gf_mul(0x0b, a[1]) ^ gf_mul(0x0d, a[2]) ^ gf_mul(0x09, a[3]),
                        gf_mul(0x09, a[0]) ^ gf_mul(0x0e, a[1]) ^ gf_mul(0x0b, a[2]) ^ gf_mul(0x0d, a[3]),
                        gf_mul(0x0d, a[0]) ^ gf_mul(0x09, a[1]) ^ gf_mul(0x0e, a[2]) ^ gf_mul(0x0b, a[3]),
                        gf_mul(0x0b, a[0]) ^ gf_mul(0x0d, a[1]) ^ gf_mul(0x09, a[2]) ^ gf_mul(0x0e, a[3]),
                    ]
                    for x in range(4):
                        stateArray[col][x] = temp[x]

        return ''.join(f'{chr(stateArray[c][r])}' for c in range(4) for r in range(4))