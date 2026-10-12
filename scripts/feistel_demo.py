#!/usr/bin/env python3
"""Toy Feistel network (the structure inside DES/3DES). Task 5 support.
Decryption = same network with round keys reversed."""
import hashlib

def F(half, key):
    return int.from_bytes(hashlib.sha256(half.to_bytes(4, "big") + key).digest()[:4], "big")

def feistel(block, keys):
    L, R = block >> 32, block & 0xFFFFFFFF
    for k in keys:
        L, R = R, L ^ F(R, k)
    return (R << 32) | L                      # final swap

if __name__ == "__main__":
    keys = [bytes([i]) * 4 for i in range(1, 9)]       # 8 rounds
    pt = 0x4D41494E5F544543                              # 64-bit block ("MAIN_TEC")
    ct = feistel(pt, keys)
    print(f"plaintext  {pt:016X}\nciphertext {ct:016X}\ndecrypted  {feistel(ct, keys[::-1]):016X}")
    print("F need not be invertible - Feistel is invertible anyway.")
