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
