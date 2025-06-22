from utils import inverse_mod, fast_mod_exp, generate_schnorr_pq, find_generator
from sha_256 import SHA_256_custom
from secrets import randbelow

class Schnorr:
    @staticmethod
    def key_gen():
        p, q = generate_schnorr_pq()
        g = find_generator(p, q)
        x = randbelow(q)
        inverse_mod_g = inverse_mod(g, p)
        y = fast_mod_exp(inverse_mod_g, x, p)

        # private = q, x
        # public = p g y
        return (q, x), (p, g, y)
        
    @staticmethod
    def sign(message: str, private_key: tuple[int, int], public_key: tuple[int, int, int]):
        q, x = private_key
        p, g, y = public_key
        k = randbelow(q) 
        r = fast_mod_exp(g, k, p)
        sha_service = SHA_256_custom()
        e = int(sha_service.hash(f"{message}|{r}"), 16)
        s = (k + x * e) % q
        return f"{e},{s}"

    @staticmethod
    def verify(message: str, signature: str, public_key: tuple[int, int, int])-> int:
        p, g, y = public_key
        e, s = map(int, signature.split(','))
        gs = fast_mod_exp(g, s, p)
        ye = fast_mod_exp(y, e, p)
        r = (gs * ye) % p
        sha_service = SHA_256_custom()
        ev = int(sha_service.hash(f"{message}|{r}"), 16)
        return ev