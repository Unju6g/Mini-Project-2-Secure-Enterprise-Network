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
