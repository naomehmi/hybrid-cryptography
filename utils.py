from math import floor, isqrt, sqrt
from random import randrange, getrandbits
from secrets import randbelow

def rotate_left(n: int, d: int, max_bits=8):
    d %= max_bits 
    return ((n << d) | (n >> (max_bits - d))) & ((1 << max_bits) - 1)

def right_rotate(n: int, d: int,max_bits=32):
    return ((n >> d) | (n << (max_bits - d))) & 0xFFFFFFFF

def fast_mod_exp(b: int, exp: int, m: int):
    res = 1
    while exp > 1:
        if exp & 1:
            res = (res * b) % m
        b = b ** 2 % m
        exp >>= 1
    return (b * res) % m

def inverse_mod(n: int, m: int):
    r0, r1 = m, n
    t0, t1 = 0, 1

    while r1 != 0:
        q = r0 // r1
        r = r0 % r1

        r0 = r1
        r1 = r

        t = t0 - t1 * q
        t0 = t1
        t1 = t

    if (t0 < 0):
        t0 += m

    return t0

def gcd(a: int, b: int):
  if b == 0:
    return a
  return gcd(b, a % b)

def factorize(n: int):
    factors = set()
    for i in range(2, isqrt(n) + 1):
        while n % i == 0:
            factors.add(i)
            n //= i
    if n > 1:
        factors.add(n)
    return factors

def find_generator(p: int, q: int):
    for h in range(2, p):
        g = fast_mod_exp(h, (p - 1) // q, p)
        if g != 1:
            return g
    raise ValueError("No generator found")

# === PRIME NUMBER GENERATION === 
def sieve(limit: int):
    is_prime = [True] * (limit + 1)
    is_prime[0:2] = [False, False]
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, limit+1, i):
                is_prime[j] = False
    return [i for i, val in enumerate(is_prime) if val]

def is_probable_prime(n: int, k: int = 5):  # Miller-Rabin
    if n < 2:
        return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:
        if n % p == 0:
            return n == p
    r, d = 0, n - 1
    while d % 2 == 0:
        d //= 2
        r += 1
    for _ in range(k):
        a = randrange(2, n - 1)
        x = fast_mod_exp(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = fast_mod_exp(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

small_primes = sieve(10**7)

def is_prime(n: int):
    limit = int(n**0.5) + 1
    for p in small_primes:
        if p > limit:
            break
        if n % p == 0:
            return False
    return is_probable_prime(n)

def generate_large_primes(bit_length: int, count: int) -> list[int]:
    result = []
    while len(result) < count:
        n = getrandbits(bit_length) | 1  # ensure odd
        if is_prime(n):
            result.append(n)
    return result

# === AES UTILS ===
def gf_mul(a: int, b: int):
    result = 0
    for _ in range(8):
        if b & 1:
            result ^= a
        high_bit_set = a & 0x80
        a <<= 1
        if high_bit_set:
            a ^= 0x11B
        a &= 0xFF
        b >>= 1
    return result

def gf_inverse(a: int):
    if a == 0:
        return 0  # Defined in AES

    r0, r1 = 0x11B, a
    t0, t1 = 0, 1

    while r1 != 0:
        q = 0
        deg_r0 = r0.bit_length() - 1
        deg_r1 = r1.bit_length() - 1
        while deg_r0 >= deg_r1:
            shift = deg_r0 - deg_r1
            q ^= (1 << shift)
            r0 ^= r1 << shift
            t0 ^= t1 << shift
            deg_r0 = r0.bit_length() - 1

        r0, r1 = r1, r0
        t0, t1 = t1, t0

    return t0 & 0xFF

def generate_aes_sbox():
    forwardSBox = [0] * 256
    inverseSBox = [0] * 256

    for i in range(256):
        inv = gf_inverse(i)
        s = inv
        for r in range(1, 5):
            s ^= rotate_left(inv, r)
        s ^= 0x63
        forwardSBox[i] = s
        inverseSBox[s] = i

    return forwardSBox, inverseSBox

# === RSA UTILS ===
def generate_valid_d(p: int, q: int, totient_n: int):
    lower = max(p, q) + 1
    upper = totient_n - 1
    while True:
        d = randbelow(upper - lower + 1) + lower  # [lower, upper]
        if gcd(d, totient_n) == 1:
            return d

# === SHA UTILS === 
def generate_hash_values():
    first8Primes = sieve(19)
    hashValues = []

    for primeNum in first8Primes:
        squareRootOfPrimeNum = sqrt(primeNum)
        squareRootOfPrimeNum = squareRootOfPrimeNum - floor(squareRootOfPrimeNum)

        rootPrimeBinary = '0b'        
        for _ in range (32):
            squareRootOfPrimeNum *= 2
            floorOfRoot = floor(squareRootOfPrimeNum)
            squareRootOfPrimeNum = squareRootOfPrimeNum - floorOfRoot
            
            rootPrimeBinary += str(floorOfRoot)

        hashValues.append(int(rootPrimeBinary, 2))
    
    return hashValues

def generate_rounded_values():
    first64Primes = sieve(311)
    roundedValues = []

    for primeNum in first64Primes:
        cubeRootOfPrimeNum = pow(primeNum, 1/3)
        cubeRootOfPrimeNum = cubeRootOfPrimeNum - floor(cubeRootOfPrimeNum)

        rootPrimeBinary = '0b'        
        for _ in range (32):
            cubeRootOfPrimeNum *= 2
            floorOfRoot = floor(cubeRootOfPrimeNum)
            cubeRootOfPrimeNum = cubeRootOfPrimeNum - floorOfRoot
            
            rootPrimeBinary += str(floorOfRoot)

        roundedValues.append(int(rootPrimeBinary, 2))
    
    return roundedValues

# === SCHNORR UTILS ===
def generate_schnorr_pq(q_bits: int = 16, p_bits: int = 32, max_attempts: int = 10000):
    while True:
        q = randrange(2**(q_bits-1), 2**q_bits)
        if not is_prime(q):
            continue

        # Try to find k such that p = kq + 1 is prime
        for _ in range(max_attempts):
            k = randrange(2**(p_bits - q_bits - 1), 2**(p_bits - q_bits))
            p = k * q + 1
            if is_prime(p):
                return p, q