# 7. Packet Tracer Build Guide (step by step)

Use Packet Tracer 8.x. Devices: 4 × 2911 (HO-R1, BO-R1, ISP1, ISP2), 3 × 2960 (HO-SW1, HO-SW2, BO-SW1), 2 × Access Point-PT (or 1 Access Point + 1 WRT300N), Server-PT, PCs/Laptops (2 Admin, 2 Staff, 1 Guest, 1 Attacker, 2 BO, 1 wireless laptop each for staff/guest).

## Order
1. **Place & cable** per `docs/01` (straight-through copper; Gi0/0 HO-R1 ↔ HO-SW1 Gi0/1; HO-SW1 Gi0/2 ↔ HO-SW2 Gi0/1; etc.).
2. **Baseline first (BEFORE screenshots):** paste ISP1/ISP2 configs, then give HO/BO routers basic addressing + the lines from `configs/BASELINE_insecure.txt`. Everything in VLAN 1. Capture:
   * Task 2: Simulation mode → filter **Telnet/HTTP** → PC Telnet to router / browse server http → open PDU → clear-text username/password. Screenshot.
   * Ping HO↔BO LAN in simulation: payload visible crossing ISP (no IPsec). Screenshot.
   * Ping sweep from attacker (all succeed). `show run` weak items.
3. **Apply hardening:** paste `HO-SW1`, `HO-SW2`, `BO-SW1`, `HO-R1`, `BO-R1` configs. (Routers: enable `securityk9` license + reload before the crypto section.)
4. **Server (192.168.40.10/24, gw .1):** Services → HTTP on; EMAIL (SMTP/POP3) on; DNS on; AAA on: clients = HO-SW2 (192.168.99.3), HO-SW1 (192.168.99.2), HO-R1 (192.168.99.1), BO-R1, APs; secret `Rad1us2026`; users `admin1`, `staff1`, `bo1`.
5. **802.1X on PCs:** PC → Config → FastEthernet0 → Authentication: enable, MD5, username/password of RADIUS user.
6. **Wireless:** `docs/05`.
7. **Verify (AFTER screenshots)** below.

## Verification commands (screenshot each)
```
HO-R1#  show crypto isakmp sa            ! QM_IDLE / ACTIVE
HO-R1#  show crypto ipsec sa             ! #pkts encaps/decaps > 0
HO-R1#  show crypto isakmp policy
HO-R1#  show access-lists                ! hit counters on deny lines
HO-R1#  show ip route
HO-SW2# show dot1x all  |  show authentication sessions
HO-SW2# show port-security  |  show port-security interface fa0/1
HO-SW1# show ip dhcp snooping  |  show ip dhcp snooping binding
HO-SW1# show interfaces trunk  |  show vlan brief
ALL#    show ip ssh  |  show run | include transport
```
Trigger the tunnel first: ping from a BO PC to 192.168.10.x (first packets may time out while IKE negotiates).

**Simulation mode ESP proof:** Event list filters → ICMP, ESP, ISAKMP; ping BO PC → Admin PC; click the packet when it is at ISP1 → OSI layers show **ESP** (IP protocol 50) with encrypted payload, outer IPs 200.3.3.1 → 200.1.1.1.

**Negative tests:** (a) Guest/attacker ping Admin → blocked, ACL counter increases. (b) Plug attacker into Fa0/1 → port err-disabled/802.1X unauthorised. (c) Rogue DHCP server on an access port → snooping drops. (d) `telnet` to router → refused.

## Deliverable checklist
- [ ] `packet_tracer/WalchandTechCampus.pkt` (save it yourself - Packet Tracer cannot be generated outside the app)
- [ ] configs in `configs/` (export with `show running-config` after your final changes; pasted versions here are the source)
- [ ] screenshots in `screenshots/` (topology, before/after, show outputs, simulation ESP)
- [ ] `report/Project_Report.md` → export to PDF/DOCX (10-15 pages)
- [ ] Python scripts run + screenshot of output
- [ ] 10-minute demo + viva practice (`docs/09_viva_prep.md`)
