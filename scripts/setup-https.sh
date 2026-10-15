#!/bin/bash
# Fetch TLS certs from Tailscale for HTTPS dev server
set -e

DOMAIN=$(tailscale status --json | python3 -c "import sys,json; print(json.load(sys.stdin)['Self']['DNSName'].rstrip('.'))")

if [ -z "$DOMAIN" ]; then
  echo "Error: Could not determine Tailscale domain"
  exit 1
fi

mkdir -p certs

echo "Fetching TLS cert for $DOMAIN..."
sudo tailscale cert --cert-file certs/dev.crt --key-file certs/dev.key "$DOMAIN"

# Make readable by current user
sudo chown "$USER" certs/dev.crt certs/dev.key

echo "Certs saved to certs/dev.crt and certs/dev.key"
echo "Run 'npm run dev:https' to start the HTTPS dev server"
