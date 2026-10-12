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
