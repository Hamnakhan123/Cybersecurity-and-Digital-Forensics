#!/usr/bin/env bash
# Session 10 - Digital certificates in a lab: a private CA signs a device certificate.
# Uses only openssl, creates files in a temporary folder, and deletes them at the end.
# Run:  bash session-10_certificate_lab.sh
set -euo pipefail
D=$(mktemp -d); cd "$D"

# 1. Lab Certificate Authority: private key + self-signed root certificate
openssl req -x509 -newkey rsa:2048 -nodes -keyout ca.key -out ca.crt -days 365 \
  -subj "/CN=Lab Root CA/O=Network Lab" 2>/dev/null
# 2. Device (e.g. a router's HTTPS/SSH identity): key + certificate signing request
openssl req -newkey rsa:2048 -nodes -keyout r1.key -out r1.csr \
  -subj "/CN=r1.lab.local/O=Network Lab" 2>/dev/null
# 3. The CA signs the request -> device certificate
openssl x509 -req -in r1.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out r1.crt -days 90 2>/dev/null

echo "Device certificate fields:"
openssl x509 -in r1.crt -noout -subject -issuer | sed 's/^/  /'
openssl x509 -in r1.crt -noout -dates | sed 's/^/  /'      # 90-day validity window
echo "  key: $(openssl x509 -in r1.crt -noout -text | grep -o 'Public-Key: ([0-9]* bit)')"
echo
echo "Verify the chain (does a trusted CA vouch for this certificate?):"
openssl verify -CAfile ca.crt r1.crt | sed 's/^/  /'
echo
echo "Impostor test: a look-alike certificate for the same name, NOT issued by our CA"
openssl req -x509 -newkey rsa:2048 -nodes -keyout evil.key -out evil.crt -days 30 \
  -subj "/CN=r1.lab.local/O=Unknown" 2>/dev/null
openssl verify -CAfile ca.crt evil.crt 2>&1 | head -2 | sed 's/^/  /' || true
cd / && rm -rf "$D"
