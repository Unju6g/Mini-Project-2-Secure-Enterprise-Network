#!/usr/bin/env python3
"""Classical ciphers: Caesar, Playfair, Hill (2x2) and Columnar Transposition.
Task 3 (Unit I). Run:  python3 ciphers.py
These are for LEARNING ONLY - all are trivially breakable."""
import string

ALPHA = string.ascii_uppercase

def clean(text):
    return "".join(c for c in text.upper() if c.isalpha())

# ---------------- Caesar ----------------
def caesar_encrypt(text, shift):
    return "".join(ALPHA[(ALPHA.index(c) + shift) % 26] if c in ALPHA else c for c in text.upper())

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

def caesar_bruteforce(ct):
    """Only 25 keys -> attacker simply tries all of them."""
    return {k: caesar_decrypt(ct, k) for k in range(1, 26)}

# ---------------- Playfair ----------------
def playfair_square(key):
    seen, sq = set(), []
    for c in clean(key).replace("J", "I") + ALPHA.replace("J", ""):
        if c not in seen:
            seen.add(c); sq.append(c)
    return [sq[i:i + 5] for i in range(0, 25, 5)]

def _pos(sq, ch):
    for r in range(5):
        for c in range(5):
            if sq[r][c] == ch:
                return r, c

def playfair_prepare(text):
    text = clean(text).replace("J", "I")
    out, i = [], 0
    while i < len(text):
        a = text[i]
        b = text[i + 1] if i + 1 < len(text) else "X"
        if a == b:
            out.append((a, "X")); i += 1
        else:
            out.append((a, b)); i += 2
    return out

def playfair(text, key, decrypt=False):
    sq, d, res = playfair_square(key), (-1 if decrypt else 1), []
    pairs = [(text[i], text[i + 1]) for i in range(0, len(text), 2)] if decrypt else playfair_prepare(text)
    for a, b in pairs:
        r1, c1 = _pos(sq, a); r2, c2 = _pos(sq, b)
        if r1 == r2:
            res += [sq[r1][(c1 + d) % 5], sq[r2][(c2 + d) % 5]]
        elif c1 == c2:
            res += [sq[(r1 + d) % 5][c1], sq[(r2 + d) % 5][c2]]
        else:
            res += [sq[r1][c2], sq[r2][c1]]
    return "".join(res)

# ---------------- Hill 2x2 ----------------
def _inv_mod(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError("matrix not invertible mod 26 - choose another key")

def hill(text, key, decrypt=False):
    (a, b), (c, d) = key
    det = (a * d - b * c) % 26
    if decrypt:
        di = _inv_mod(det, 26)
        a, b, c, d = (d * di) % 26, (-b * di) % 26, (-c * di) % 26, (a * di) % 26
    else:
        _inv_mod(det, 26)  # validity check
    t = clean(text)
    if len(t) % 2:
        t += "X"
    out = []
    for i in range(0, len(t), 2):
        x, y = ALPHA.index(t[i]), ALPHA.index(t[i + 1])
        out.append(ALPHA[(a * x + b * y) % 26] + ALPHA[(c * x + d * y) % 26])
    return "".join(out)

# ---------------- Columnar transposition ----------------
def _order(key):
    return sorted(range(len(key)), key=lambda i: (key[i], i))

def columnar_encrypt(text, key):
    t = clean(text); key = key.upper()
    t += "X" * (-len(t) % len(key))
    rows = [t[i:i + len(key)] for i in range(0, len(t), len(key))]
    return "".join("".join(r[col] for r in rows) for col in _order(key))

def columnar_decrypt(ct, key):
    key = key.upper(); n, rows = len(key), len(ct) // len(key)
    cols, pos = {}, 0
    for col in _order(key):
        cols[col] = ct[pos:pos + rows]; pos += rows
    return "".join(cols[c][r] for r in range(rows) for c in range(n))

if __name__ == "__main__":
    msg = "WALCHAND TECH CAMPUS VPN KEY IS SECRET"
    print("Plaintext      :", msg)

    ct = caesar_encrypt(msg, 3)
    print("\n[Caesar shift=3]", ct, "->", caesar_decrypt(ct, 3))
    print("  brute force (first 3 of 25 keys):", list(caesar_bruteforce(ct).items())[:3])

    ct = playfair(msg, "MONARCHY")
    print("\n[Playfair key=MONARCHY]", ct, "->", playfair(ct, "MONARCHY", True))

    key = [[3, 3], [2, 5]]
    ct = hill(msg, key)
    print("\n[Hill 2x2 key=[[3,3],[2,5]]]", ct, "->", hill(ct, key, True))

    ct = columnar_encrypt(msg, "ZEBRA")
    print("\n[Columnar key=ZEBRA]", ct, "->", columnar_decrypt(ct, "ZEBRA"))

    print("""
WHY THESE ARE WEAK vs IPsec (AES-256 + SHA-HMAC + DH):
 * Tiny key space: Caesar has 25 keys; Playfair/Hill/transposition fall to
   frequency analysis, digraph statistics or known-plaintext (Hill is linear).
 * Substitution keeps letter statistics; transposition keeps letter frequencies.
 * No integrity/authentication: attacker can modify ciphertext undetected.
 * No key exchange: both sides must already share the key secretly.
 * AES: 128/192/256-bit key, 10-14 rounds of non-linear S-box + diffusion,
   designed against known-plaintext, differential and linear cryptanalysis.
   IPsec adds ESP-HMAC integrity, anti-replay and IKE (DH) key exchange.""")
