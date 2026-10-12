# Secure Enterprise Network for "Walchand Tech Campus"
Network Security – Mini Project 2 · Final Year (ECM) 2026-27

Two-site enterprise network (Head Office + Branch Office over an untrusted ISP) secured with IPsec VPN, AAA/RADIUS + 802.1X, LAN hardening, WLAN security, email security, plus Python crypto demos.

| Folder | Contents |
|---|---|
| `configs/` | IOS configs for HO-R1, BO-R1, ISP1, ISP2, HO-SW1, HO-SW2, BO-SW1 + insecure baseline |
| `scripts/` | `ciphers.py` (Caesar/Playfair/Hill/transposition), `rsa_demo.py` (toy RSA), `feistel_demo.py`, `gpg_demo.sh` (PGP) |
| `docs/` | Addressing + VLAN plan, threat analysis, vulnerability assessment, crypto notes, WLAN/email, ethics note, build guide, viva prep |
| `packet_tracer/` | Put your `.pkt` file here |
| `screenshots/` | Before/after screenshots and show outputs |
| `report/` | `Project_Report.md` (combined report) |

## Quick start
```bash
python3 scripts/ciphers.py      # Task 3
python3 scripts/rsa_demo.py     # Task 6 (optional arg: prime size in bits)
python3 scripts/feistel_demo.py # Task 5 support
bash scripts/gpg_demo.sh        # Task 12 (needs gpg)
```
Build the network following `docs/07_build_guide.md`, paste the configs from `configs/`, then save the `.pkt` into `packet_tracer/`.

## Task → file map
| Task | Where |
|---|---|
| 1 Threat analysis | docs/02 |
| 2 Plaintext capture | docs/07 (simulation steps) |
| 3 Cipher tool | scripts/ciphers.py |
| 4 SSH v2 | all configs |
| 5 Cipher comparison | docs/04, scripts/feistel_demo.py |
| 6 Toy RSA | scripts/rsa_demo.py |
| 7 Key distribution | docs/04 (PSK + optional CA) |
| 8 AAA + 802.1X | HO-SW2.txt, HO-R1.txt |
| 9 LAN hardening | HO-SW1/2.txt, HO-R1.txt ACLs |
| 10 Vulnerability assessment | docs/03 |
| 11 WLAN | docs/05 |
| 12 Email security | docs/05, scripts/gpg_demo.sh |
| 13 IPsec VPN | HO-R1.txt, BO-R1.txt |
| 14 Ethics note | docs/06 |

## Important
* The `.pkt` file and screenshots must be created in Packet Tracer by you; this repo gives you every config, script and document to build and explain them.
* Passwords/keys here are **lab values** – change them to your own and never reuse them anywhere real.
* All testing stays inside the simulator.
* Adjust addresses/ciphers to your group's assigned variation, and write your name, roll numbers and group at the top of the report.
