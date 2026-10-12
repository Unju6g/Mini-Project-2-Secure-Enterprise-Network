# 9. Viva Preparation (every member must explain every part)

1. Why does IPsec use tunnel mode between sites? (hides inner IPs, router-to-router)
2. Difference between IKE Phase 1 and Phase 2? (P1: secure ISAKMP SA, auth + DH; P2: IPsec SAs for ESP)
3. What is "interesting traffic"? (ACL 110: permit HO LAN ↔ BO LAN; must be mirror images)
4. AH vs ESP? (AH integrity only, breaks with NAT; ESP encrypts + authenticates)
5. Why must the PSK match and why isn't it sent? (authentication input; DH + hash proves knowledge)
6. How does 802.1X work? (supplicant, authenticator, RADIUS; EAPOL; port blocked until success)
7. DHCP snooping: trusted vs untrusted ports? binding table? (trust uplinks only)
8. Why native VLAN 999 and `nonegotiate`? (VLAN hopping/double tagging)
9. Feistel structure; why DES is broken; why AES? 3DES?
10. RSA: how are e, d, n chosen? Why 2048? Why is textbook RSA insecure?
11. WEP vs WPA vs WPA2; Personal vs Enterprise.
12. How does PGP give confidentiality and non-repudiation?
13. Passive vs active attacks; map one to a service and mechanism.
14. Show `show crypto ipsec sa` and explain encaps/decaps/SPI.
15. Legal limits of testing; what makes an ethical hacker "ethical"?
