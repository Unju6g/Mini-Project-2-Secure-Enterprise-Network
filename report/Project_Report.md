# Secure Enterprise Network for "Walchand Tech Campus"
**Course:** Network Security · **Mini Project-2** · Final Year (ECM) 2026-27
**Group & Batch no.:** ____  **Names:** ____  **Roll Nos.:** ____  **Date:** ____

## Abstract & Objective
Design, build and secure a two-site (Head Office / Branch Office) enterprise network on a Cisco platform over an untrusted ISP, applying cryptography, key management, access control, wireless, email and IP security. Site-to-site traffic is protected with an IPsec ESP tunnel; users and devices are authenticated with AAA/RADIUS and 802.1X; the LAN is hardened with VLANs, ACLs, port-security and DHCP snooping; and the network is assessed before and after hardening.

---
# 1. IP Addressing Plan, VLAN Table and Topology

## 1.1 VLAN table (Head Office)
| VLAN | Name | Subnet | Gateway (HO-R1 sub-if) | Purpose |
|---|---|---|---|---|
| 10 | ADMIN | 192.168.10.0/24 | 192.168.10.1 | Admin PCs (full access, 802.1X) |
| 20 | STAFF | 192.168.20.0/24 | 192.168.20.1 | Staff PCs + Staff Wi-Fi (802.1X / WPA2-Ent) |
| 30 | GUEST | 192.168.30.0/24 | 192.168.30.1 | Guest PCs + Guest Wi-Fi + attacker PC (restricted) |
| 40 | SERVER | 192.168.40.0/24 | 192.168.40.1 | AAA/RADIUS, web, email server |
| 99 | MGMT | 192.168.99.0/24 | 192.168.99.1 | Switch/AP management (SVIs) |
| 999 | BLACKHOLE | none | none | Native VLAN on trunks + unused ports |

Branch Office: single LAN 172.16.10.0/24 (no VLANs needed).

## 1.2 Device / interface addressing
| Device | Interface | Address | Connected to |
|---|---|---|---|
| HO-R1 | Gi0/0.10 / .20 / .30 / .40 / .99 | 192.168.{10,20,30,40,99}.1/24 | HO-SW1 Gi0/1 (trunk) |
| HO-R1 | Gi0/1 | 200.1.1.1/30 | ISP1 Gi0/0 |
| ISP1 | Gi0/0 | 200.1.1.2/30 | HO-R1 |
| ISP1 | Gi0/1 | 200.2.2.1/30 | ISP2 Gi0/0 |
| ISP2 | Gi0/0 | 200.2.2.2/30 | ISP1 |
| ISP2 | Gi0/1 | 200.3.3.2/30 | BO-R1 Gi0/1 |
| BO-R1 | Gi0/1 | 200.3.3.1/30 | ISP2 |
| BO-R1 | Gi0/0 | 172.16.10.1/24 | BO-SW1 Fa0/24 |
| HO-SW1 | Vlan99 | 192.168.99.2/24 | gw 192.168.99.1 |
| HO-SW2 | Vlan99 | 192.168.99.3/24 | gw 192.168.99.1 |
| BO-SW1 | Vlan1 | 172.16.10.2/24 | gw 172.16.10.1 |
| Server (AAA/Web/Mail) | Fa0 | 192.168.40.10/24 (static) | HO-SW1 Fa0/1, gw 192.168.40.1 |
| AP-STAFF | mgmt | DHCP (VLAN 20) | HO-SW1 Fa0/2 |
| AP-GUEST | mgmt | DHCP (VLAN 30) | HO-SW1 Fa0/3 |
| Admin PCs | DHCP | 192.168.10.21+ | HO-SW2 Fa0/1-2 |
| Staff PCs | DHCP | 192.168.20.21+ | HO-SW2 Fa0/3-4 |
| Guest PC / Attacker | DHCP | 192.168.30.21+ | HO-SW2 Fa0/5-7 |
| BO PCs | DHCP | 172.16.10.21+ | BO-SW1 Fa0/1-4 |

## 1.3 Switch port map
**HO-SW1:** Gi0/1 trunk→HO-R1 · Gi0/2 trunk→HO-SW2 · Fa0/1 Server(V40) · Fa0/2 AP-STAFF(V20) · Fa0/3 AP-GUEST(V30)
**HO-SW2:** Gi0/1 trunk→HO-SW1 · Fa0/1-2 Admin(V10) · Fa0/3-4 Staff(V20) · Fa0/5-6 Guest(V30) · Fa0/7 Attacker(V30)
**BO-SW1:** Fa0/24 uplink→BO-R1 · Fa0/1-4 BO PCs

## 1.4 Topology (text diagram)
```
                         [AP-STAFF]  [AP-GUEST]
                              \         /
 [Admin PCs]--[HO-SW2]==trunk==[HO-SW1]--[Server 192.168.40.10]
 [Staff PCs]--   |                 ||trunk
 [Guest PC ]--   |                 ||
 [Attacker ]--                  [HO-R1]Gi0/1 200.1.1.1
                                    |
                                  [ISP1]200.2.2.1 ---- 200.2.2.2[ISP2]
                                                                   |200.3.3.2
                                                              200.3.3.1
                                                               [BO-R1]--[BO-SW1]--[BO PCs]
          <========== IPsec ESP tunnel HO-R1 <-> BO-R1 across ISP ==========>
```
Add the Packet Tracer screenshot of your final topology in `screenshots/topology.png`.

## 1.5 Group variation
Your instructor gives each group a variation (different subnets, cipher suite or VLAN count). Change the values consistently in the configs here (search & replace) and update these tables.

---

# 2. Threat Analysis (Unit I)

## 2.1 Assets
Server (RADIUS, web, mail), HO/BO LAN traffic, switch/router configs, credentials, Wi-Fi.

## 2.2 Attack → OSI security service → mechanism (X.800)
| # | Attack (type) | Where in topology | Violated property | OSI security service | Security mechanism | Control in this project |
|---|---|---|---|---|---|---|
| 1 | Sniffing Telnet/HTTP/SMTP (passive) | LAN, ISP path | Confidentiality | Data confidentiality | Encipherment | SSHv2, IPsec ESP, PGP, WPA2 |
| 2 | Traffic analysis (passive) | ISP | Confidentiality | Traffic-flow confidentiality | Encipherment (tunnel mode), traffic padding | IPsec tunnel mode hides inner IPs |
| 3 | MAC/IP spoofing (active) | Access ports | Authenticity | Peer-entity & data-origin authentication | Authentication exchange, digital signature | 802.1X, port-security, DHCP snooping |
| 4 | Rogue DHCP server (active) | VLANs | Authenticity/availability | Authentication, access control | Access control | DHCP snooping trust ports |
| 5 | DoS / DHCP starvation / SYN flood (active) | Server, DHCP | Availability | Availability | Access control, routing control | Snooping rate-limit, port-security max MAC, ACLs |
| 6 | Man-in-the-middle / modification (active) | ISP, LAN | Integrity | Data integrity | Hash/HMAC, signature | ESP-HMAC-SHA, PGP signature |
| 7 | Replay (active) | ISP | Integrity/authenticity | Data-origin authentication | Sequence numbers | IPsec anti-replay |
| 8 | Unauthorised access by Guest/attacker (active) | VLAN 30 → VLAN 10/40 | Access control | Access control | Access control lists | VLAN segmentation + GUEST-IN ACL |
| 9 | Password guessing on device (active) | Router/switch vty | Authenticity | Authentication | Authentication exchange | AAA, strong secrets, vty ACL, SSH retries |
| 10 | VLAN hopping (active) | Trunks | Access control | Access control | Access control | native VLAN 999, nonegotiate, allowed list |
| 11 | Rogue AP / weak Wi-Fi key (active) | WLAN | Confidentiality/authenticity | Authentication, confidentiality | Encipherment + authentication | WPA2-Personal (strong PSK), WPA2-Enterprise |
| 12 | Repudiation of e-mail (active) | Mail | Non-repudiation | Non-repudiation | Digital signature | PGP/S-MIME signature |

Passive = release of message contents, traffic analysis. Active = masquerade, replay, modification, DoS.

## 2.3 Network security model
```
 Sender (HO/BO host)                                        Receiver
 +-----------------+      +------------------------+      +-----------------+
 | message -> [Security|    untrusted ISP / LAN      |[Security -> message |
 |            transformation]=== channel ===[ opponent: sniffer, spoofer, MITM ]===[transformation]|
 |   secret info (keys: PSK, RSA, SSH key, PGP key) shared via     |
 +-----------------+      |  TRUSTED THIRD PARTY (RADIUS server / CA / IKE) |
                          +------------------------+
```
Four tasks of the model: (1) design the transformation (AES-ESP), (2) generate secret info (IKE/DH, RSA), (3) distribute secrets (PSK / X.509 / PGP key exchange), (4) specify the protocol (IKE+ESP, SSH, 802.1X/EAP).

**Network access security model** (for LAN/Wi-Fi): a *gatekeeper* (802.1X authenticator = switch/AP + RADIUS) with *internal controls* (ACLs, VLANs) blocks unauthorised access (hackers, rogue devices).

---

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

---

# 3. Vulnerability Assessment & Hardening (Task 10 - conceptual, inside simulator only)

## 3.1 Method
1. **Ping sweep:** from the attacker PC (VLAN 30) `ping` 192.168.10.1, .10.x, .20.x, .40.10, .99.x and 172.16.10.x. Record which answer (before: all; after: only allowed).
2. **Port/service review (show commands):** `show running-config | include (telnet|http|password)`, `show ip ssh`, `show control-plane`/`show ip sockets`, `show ip interface brief`, `show vlan brief`, `show access-lists` (hit counters), `show port-security`, `show ip dhcp snooping`.
3. **Server service review:** Server → Services tab: list HTTP, SMTP/POP3, DNS, RADIUS on/off.
4. Record before → fix → verify.

## 3.2 Findings and fixes
| # | Weakness found (before) | Evidence | Risk | Fix applied | Verification |
|---|---|---|---|---|---|
| 1 | Default/weak passwords (`cisco`), plaintext enable | `show run` shows `enable password cisco` | Device takeover | `enable secret`, `service password-encryption`, AAA local user, strong passwords | `show run | include secret` |
| 2 | Telnet enabled on vty | `show run` → `transport input telnet`; Telnet works from attacker | Credentials sniffable | SSHv2 + `transport input ssh`, RSA 2048 | `show ip ssh`; telnet refused |
| 3 | HTTP server enabled on routers | `ip http server` | Attack surface | `no ip http server` | `show run | include http` |
| 4 | No VLAN isolation (all in VLAN 1) | Attacker pings Admin/Server | Lateral movement | VLANs 10/20/30/40/99 + router-on-a-stick | `show vlan brief`, ping fails |
| 5 | No ACLs: Guest reaches internal nets | Ping sweep succeeds | Data exposure | `GUEST-IN`, `STAFF-IN`, `MGMT-ONLY` | `show access-lists` hit counters rise on deny lines |
| 6 | Any device can plug into any port | Attacker PC gets IP | Rogue access | 802.1X on Admin/Staff ports, port-security sticky | `show dot1x all`, `show port-security` |
| 7 | MAC flooding / rogue DHCP possible | No snooping | MITM, DoS | DHCP snooping + rate limit + trusted ports | `show ip dhcp snooping` |
| 8 | VLAN 1 native / DTP | default trunk | VLAN hopping | native 999, `nonegotiate`, allowed list, unused ports shutdown | `show interfaces trunk` |
| 9 | Branch-HO traffic in clear over ISP | Simulation mode: readable payload | Eavesdrop/modify | IPsec ESP AES-256/SHA | `show crypto ipsec sa` encaps/decaps counters, ESP in simulation |
| 10 | Open SSID / weak PSK (`12345678`) | AP config | Free access, key cracking | WPA2-PSK long passphrase (guest), WPA2-Enterprise (staff) | Client join test |
| 11 | Mail & HTTP plaintext | Simulation capture | Disclosure | PGP/S-MIME, HTTPS (conceptual) | GPG demo |
| 12 | Default RADIUS secret | Server config | Spoofed auth | Unique shared secret per client | Auth test |
| 13 | Unused ports open | `show ip int brief` | Physical intrusion | `shutdown` + VLAN 999 | `show interfaces status` |

## 3.3 Ping-sweep result sheet (fill in)
| Source | Target | Before | After | Reason |
|---|---|---|---|---|
| Attacker (V30) | 192.168.10.x (Admin) | OK | Fail | GUEST-IN deny |
| Attacker | 192.168.40.10 TCP/80 | OK | OK | permitted web |
| Attacker | 192.168.40.10 ICMP | OK | Fail | not permitted |
| Attacker | 172.16.10.x (BO) | OK | Fail | GUEST-IN deny |
| Staff | 192.168.10.x | OK | Fail | STAFF-IN deny |
| Admin | BO LAN | OK | OK (via IPsec) | interesting traffic |

---

# 5. Wireless and Email Security (Unit V)

## 5.1 WLAN configuration (Task 11)
| SSID | Device | Mode | Settings |
|---|---|---|---|
| WTC-Guest | AP-GUEST (VLAN 30 port) | WPA2-Personal (PSK, AES/CCMP) | Authentication: WPA2-PSK, Encryption AES, PSK `Gu3st#WTC2026!` (≥ 12 chars) |
| WTC-Staff | AP-STAFF (VLAN 20 port) | WPA2-Enterprise (RADIUS) | Authentication: WPA2, RADIUS server IP 192.168.40.10, port 1812, shared secret `Rad1us2026`, AES |

Packet Tracer: Access Point-PT → Config → Port 1 (SSID, authentication). Server → Services → AAA: add the AP as a client (name, IP, secret) and users (`staff1` / `Staff@123`). Wireless laptops: add a wireless card (PT-LAPTOP-NM-1W) and set the SSID + credentials. If Packet Tracer shows only PSK for your AP model, use a Wireless Router (WRT300N) for the guest SSID, and describe the enterprise config with screenshots of the RADIUS server.

**Weak-configuration example:** SSID `WTC-Open` with *no security* or PSK `12345678`. Show that any laptop associates without credentials / a dictionary attack would recover the PSK. Then show the fix above.

## 5.2 WEP vs WPA vs WPA2
| | WEP | WPA | WPA2 |
|---|---|---|---|
| Cipher | RC4 | RC4 + TKIP | AES-CCMP |
| Key | 40/104-bit static + 24-bit IV | per-packet key (TKIP) | 128-bit AES |
| Integrity | CRC-32 (linear, forgeable) | Michael MIC | CCM MAC |
| Auth | Open/shared key | PSK or 802.1X | PSK or 802.1X |
| Status | Broken in minutes (IV reuse, FMS/PTW) | Deprecated | Secure with strong key (KRACK patched); WPA3 successor |

Personal = one shared PSK (offline dictionary attack risk). Enterprise = 802.1X/EAP + RADIUS, per-user credentials.

## 5.3 Email security (Task 12)
1. **Server → Services → EMAIL:** domain `walchand.local`; users `alice` and `bob`. Clients: PC → Desktop → Email, SMTP/POP3 server 192.168.40.10.
2. **Simulation mode:** filter SMTP and POP3, send a mail, open the PDU details: body and password appear in clear text. Screenshot.
3. **PGP:** run `bash scripts/gpg_demo.sh` on a Linux/WSL lab machine. It creates Alice/Bob keys, exchanges public keys, signs + encrypts, shows what a sniffer would see (ASCII-armored ciphertext), decrypts and verifies, and shows that an eavesdropper (Eve) cannot.
4. **How PGP removes the exposure:** the message is encrypted with a random symmetric session key, which is encrypted with Bob's public RSA key (confidentiality); Alice's private key signs a hash (integrity, authentication, non-repudiation). Mail servers and the ISP only carry ciphertext. S/MIME does the same with X.509 certificates instead of the PGP web of trust.

---

# 6. Ethical Hacking Note (Task 14)

**Legal limits.** Security testing is lawful only with *explicit, written authorisation* from the system owner. Without it, scanning, probing, password guessing, sniffing or exploiting is a crime under the Information Technology Act, 2000 in India (e.g. Sec. 43 unauthorised access/damage, Sec. 66 computer-related offences, Sec. 66C identity theft, Sec. 72 breach of confidentiality) and under laws such as the CFAA (USA) and the Computer Misuse Act (UK). The DPDP Act, 2023 adds duties on handling personal data found during testing. Authorisation does not cover systems outside the agreed scope, and a contract does not make illegal acts legal.

**Ethical limits.** Stay inside the agreed scope, time window and rules of engagement; avoid destructive tests (DoS, data deletion) unless approved; protect any data seen (minimise, never copy or share it); disclose findings only to the client; follow responsible/coordinated disclosure for third-party flaws; never accept payment for silence or take advantage of access.

**Role of an ethical hacker.** Thinks like an attacker to find weaknesses before criminals do: reconnaissance, scanning, vulnerability analysis, controlled exploitation to prove impact, and reporting. Differs from a black-hat (no permission, malicious intent) and from a grey-hat (no permission, maybe good intent, still unlawful).

**Responsibilities.** (1) Get a signed scope/authorisation (NDA, rules of engagement). (2) Do no harm; back up and restore. (3) Maintain confidentiality, integrity of evidence. (4) Report honestly with risk ratings and remediation advice, including what was *not* tested. (5) Remove tools/accounts, retest fixes. (6) Keep learning and follow codes of conduct (EC-Council CEH, (ISC)² ethics).

**In this project:** all testing (ping sweep, sniffing, the "attacker" PC) is performed only inside the Packet Tracer simulation. No real network, system or Wi-Fi is scanned or attacked, as required by the lab rules.

---

# 7. IPsec Site-to-Site VPN (Task 13)
Configured in `configs/HO-R1.txt` and `configs/BO-R1.txt`.
* **IKE Phase 1:** ISAKMP policy 10 – AES-256, SHA-1, pre-shared key, DH group 2, lifetime 86400 s.
* **IKE Phase 2:** transform set `WTC-TS` = `esp-aes 256 esp-sha-hmac`, tunnel mode.
* **Interesting traffic:** ACL 110 (HO LAN 192.168.0.0/16 ↔ BO LAN 172.16.10.0/24, mirrored on BO).
* **Crypto map** `WTC-MAP` applied to the ISP-facing interface.
* **Verification:** `show crypto isakmp sa`, `show crypto ipsec sa` (encaps/decaps counters), Simulation mode shows ESP between 200.1.1.1 and 200.3.3.1 with unreadable payload.

_Insert screenshots: before (clear ICMP across ISP) and after (ESP)._

# 8. AAA, 802.1X and LAN Hardening (Tasks 8-9)
RADIUS server 192.168.40.10; `aaa authentication login default group radius local` on all devices; 802.1X (`dot1x system-auth-control`, `authentication port-control auto`) on HO-SW2 Admin/Staff ports; port-security (sticky, max 2/1), DHCP snooping on VLANs 10/20/30, native VLAN 999, unused ports shut; ACLs GUEST-IN, STAFF-IN, MGMT-ONLY.

_Insert screenshots: `show dot1x all`, `show port-security`, `show ip dhcp snooping`, `show access-lists` with hit counters._

# 9. Secure Management (Task 4)
SSHv2 with 2048-bit RSA on every device, Telnet disabled (`transport input ssh`), `enable secret`, password encryption, exec-timeout, vty ACL.

# 10. Python Tools (Tasks 3, 5, 6)
`scripts/ciphers.py`, `scripts/rsa_demo.py`, `scripts/feistel_demo.py` – include output screenshots.

# 11. Conclusion
The final design encrypts all inter-site traffic, authenticates users, devices and Wi-Fi clients, isolates VLANs, protects management access and removes the weaknesses found in the baseline. Limitations: simulator feature set (EAP-MD5 instead of PEAP, DH group 2, PSK instead of certificates). Future work: certificate-based IKE with a CA, HTTPS, IPS/firewall, NAT with VPN exemption.

# References
W. Stallings, *Cryptography and Network Security*; Cisco IOS Security Configuration Guides; RFC 4301/4303 (IPsec/ESP), RFC 2409/7296 (IKE), IEEE 802.1X-2020, IEEE 802.11i; NIST SP 800-57, 800-77.
