#!/usr/bin/env bash
# Task 12: PGP demo with GnuPG on a lab machine. Two users (alice@HO, bob@BO) in separate keyrings.
# Run:  bash gpg_demo.sh      (needs gpg installed; works fully offline)
set -e
W=$(mktemp -d); A="$W/alice"; B="$W/bob"; mkdir -m 700 "$A" "$B"
gen() { gpg --homedir "$1" --batch --passphrase '' --quick-generate-key "$2" rsa2048 default 1y 2>/dev/null; }
gen "$A" "Alice HO <alice@walchand.local>"
gen "$B" "Bob BO <bob@walchand.local>"

# 1) Public keys are exchanged (this is key distribution: only PUBLIC keys travel)
gpg --homedir "$A" --armor --export alice@walchand.local > "$W/alice.pub"
gpg --homedir "$B" --armor --export bob@walchand.local   > "$W/bob.pub"
gpg --homedir "$A" --import "$W/bob.pub" 2>/dev/null
gpg --homedir "$B" --import "$W/alice.pub" 2>/dev/null
# (lab shortcut) trust imported keys so gpg does not prompt
echo "$(gpg --homedir "$A" --with-colons --fingerprint bob@walchand.local | awk -F: '/^fpr/{print $10; exit}'):6:" | gpg --homedir "$A" --import-ownertrust 2>/dev/null
echo "$(gpg --homedir "$B" --with-colons --fingerprint alice@walchand.local | awk -F: '/^fpr/{print $10; exit}'):6:" | gpg --homedir "$B" --import-ownertrust 2>/dev/null

# 2) Alice signs + encrypts for Bob
echo "Salary file will be sent Friday. VPN PSK is WalchandVPN2026" > "$W/mail.txt"
gpg --homedir "$A" --armor --sign --encrypt -r bob@walchand.local --trust-model always \
    -u alice@walchand.local -o "$W/mail.txt.asc" "$W/mail.txt" 2>/dev/null
echo "=== What a sniffer on the ISP/SMTP path would see (ciphertext) ==="
head -n 8 "$W/mail.txt.asc"; echo "..."

# 3) Bob decrypts and verifies Alice's signature
echo "=== Bob decrypts + verifies ==="
gpg --homedir "$B" --decrypt "$W/mail.txt.asc"

# 4) Eve (no private key) cannot decrypt
mkdir -m 700 "$W/eve"
echo "=== Eve tries ==="
gpg --homedir "$W/eve" --decrypt "$W/mail.txt.asc" 2>&1 | tail -n 2 || true
echo "Work dir: $W"
