# 8. If your Packet Tracer version lacks a feature
The brief says to check early and tell the instructor. Fallbacks (document them in the report):
| Feature | Fallback |
|---|---|
| 802.1X on switch | Use `dot1x port-control auto` syntax; if absent, show config + RADIUS server user list + explain EAP flow (supplicant → authenticator → RADIUS) |
| WPA2-Enterprise on AP | Show RADIUS server config and AP security screen if available; otherwise show WPA2-PSK and explain EAP-PEAP/TLS |
| AES-256 / group 14 in IKE | Use `esp-aes 128` / group 2 |
| IOS CA / X.509 | Do the optional part in GNS3/CML or explain the trustpoint config in `docs/04` |
| DHCP snooping / port-security syntax | Use `show run` to confirm which commands are accepted; keep what works |
