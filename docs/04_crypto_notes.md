# 4. Cryptography Notes (Units I-III)

## 4.1 Why classical ciphers are weak (Task 3)
See `scripts/ciphers.py`. Caesar: 25 keys. Playfair: digraph statistics, 25! squares but still breakable. Hill: linear, falls to known-plaintext. Transposition: letter frequencies unchanged. None give integrity, key exchange or protection against modern attacks. IPsec uses AES (non-linear S-boxes, many rounds), HMAC-SHA integrity, DH key exchange and anti-replay.

## 4.2 DES / 3DES vs AES (Task 5)
| Property | DES | 3DES | AES |
|---|---|---|---|
| Structure | Feistel, 16 rounds | 3 x DES (EDE) | Substitution-permutation network |
| Block size | 64 | 64 | 128 |
| Key size | 56 (64 w/ parity) | 112/168 bits (effective ~112) | 128 / 192 / 256 |
| Status | Broken (brute force in hours, 1998 EFF) | Deprecated (Sweet32, slow) | Standard |
| Cisco keyword | `encryption des` | `encryption 3des` | `encryption aes 256` |
| Transform set | `esp-des` | `esp-3des` | `esp-aes 256` |

**Feistel structure:** split block into L,R; each round `L' = R`, `R' = L XOR F(R, K_i)`. Decryption uses the same network with the keys reversed; F need not be invertible (`scripts/feistel_demo.py`). DES = 16 rounds, 48-bit round keys from a 56-bit key; F = expansion, key XOR, 8 S-boxes, permutation.

**Strength of DES:** 2^56 keys; DES cracker broke it in < 1 day (1998); today minutes-hours on GPUs/FPGAs. Meet-in-the-middle makes 2DES only ~2^57; 3DES ~2^112.

**RSA key size:** 1024-bit is considered weak (≈80-bit security); 2048-bit ≈112-bit security (minimum); 3072-bit ≈128-bit. The project generates 2048-bit RSA for SSH. DH group 2 (1024-bit) is weak - use group 14 (2048-bit) if your IOS supports it (`group 14`); the configs use group 2 for Packet Tracer compatibility, mention this in the viva.

**Comparison test:** change `encryption aes 256` → `3des` → `des` on BOTH routers, `clear crypto sa`, re-ping, run `show crypto ipsec sa` and `show crypto isakmp policy`; screenshot each.

## 4.3 Toy RSA (Task 6)
`scripts/rsa_demo.py`: n = p·q, φ = (p-1)(q-1), choose e coprime to φ, d = e⁻¹ mod φ; C = M^e mod n; M = C^d mod n. Small n is factored instantly - that is why real keys are ≥ 2048 bits and use OAEP/PSS padding.

## 4.4 Key distribution (Task 7)
* **Used in Packet Tracer:** IKE Phase 1 uses a **pre-shared key** (`crypto isakmp key ... address ...`) for authentication; Diffie-Hellman (group 2) then derives the session keys so the PSK itself is never sent. Drawback: PSK must be distributed out-of-band and doesn't scale (n² keys).
* **Public-key distribution:** public keys are shared in X.509 certificates, signed by a CA.
* **Certificate chain:** end-entity cert (router) → issued by Intermediate CA → issued by Root CA (self-signed, trusted anchor). Verifier checks each signature, validity dates, revocation (CRL/OCSP) and name.
* **Optional (GNS3/CML) IOS CA:**
```
! CA router
ip http server
crypto pki server WTC-CA
 database level complete
 grant auto
 lifetime certificate 365
 no shutdown
! Client router
crypto pki trustpoint WTC-CA
 enrollment url http://<CA-IP>:80
 revocation-check none
 rsakeypair WTC-KEY 2048
crypto pki authenticate WTC-CA
crypto pki enroll WTC-CA
! IKE then uses:  crypto isakmp policy 10 / authentication rsa-sig
show crypto pki certificates
```
Use `grant auto` only in a lab (it auto-approves requests).
