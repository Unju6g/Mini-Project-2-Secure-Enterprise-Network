#!/usr/bin/env python3
"""Toy RSA: key generation, encryption, decryption, signing and why small keys fail.
Task 6 (Unit II). Run:  python3 rsa_demo.py [bits]   (default 16-bit primes)
NOT secure: textbook RSA, tiny keys, no padding. Real RSA >= 2048 bits with OAEP/PSS."""
import random, sys, math

def is_prime(n, k=20):                      # Miller-Rabin
    if n < 2: return False
    for p in (2, 3, 5, 7, 11, 13):
        if n % p == 0: return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2; s += 1
    for _ in range(k):
        x = pow(random.randrange(2, n - 1), d, n)
        if x in (1, n - 1): continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1: break
        else:
            return False
    return True

def gen_prime(bits):
    while True:
        p = random.getrandbits(bits) | (1 << (bits - 1)) | 1
        if is_prime(p): return p

def egcd(a, b):
    if b == 0: return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y

def modinv(a, m):
    g, x, _ = egcd(a, m)
    if g != 1: raise ValueError("no inverse")
    return x % m

def keygen(bits=16):
    p = gen_prime(bits)
    q = gen_prime(bits)
    while q == p: q = gen_prime(bits)
    n, phi = p * q, (p - 1) * (q - 1)
    e = next(c for c in (65537, 257, 17, 5, 3) if c < phi and math.gcd(c, phi) == 1)
    d = modinv(e, phi)
    return (e, n), (d, n), (p, q, phi)

def encrypt(msg, pub):
    e, n = pub
    return [pow(ord(ch), e, n) for ch in msg]        # char-by-char (toy only)

def decrypt(cipher, priv):
    d, n = priv
    return "".join(chr(pow(c, d, n)) for c in cipher)

def _h(msg, n):
    return sum(ord(c) * (i + 1) for i, c in enumerate(msg)) % n   # toy "hash"

def sign(msg, priv):
    d, n = priv
    return pow(_h(msg, n), d, n)

def verify(msg, sig, pub):
    e, n = pub
    return pow(sig, e, n) == _h(msg, n)

def factor(n):                                       # trial division attack
    for i in range(2, math.isqrt(n) + 1):
        if n % i == 0: return i, n // i

if __name__ == "__main__":
    bits = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    pub, priv, (p, q, phi) = keygen(bits)
    print(f"p={p}  q={q}\nn=p*q={pub[1]}  phi={phi}")
    print(f"Public key  (e,n) = {pub}\nPrivate key (d,n) = {priv}")
    msg = "WTC VPN OK"
    c = encrypt(msg, pub)
    print("\nPlaintext :", msg, "\nCiphertext:", c, "\nDecrypted :", decrypt(c, priv))
    s = sign(msg, priv)
    print("\nSignature :", s, "| verify:", verify(msg, s, pub), "| tampered:", verify("WTC VPN NO", s, pub))
    print("\nAttacker factors n ->", factor(pub[1]), "(instant for toy size; infeasible for 2048-bit n)")
