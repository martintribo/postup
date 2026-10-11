#!/bin/bash
# Install the user systemd timer. Run as main on dev-vm.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
UNIT_DIR="${HOME}/.config/systemd/user"
mkdir -p "$UNIT_DIR"
cp -f "$ROOT/postup-r2-killswitch.service" "$UNIT_DIR/"
cp -f "$ROOT/postup-r2-killswitch.timer" "$UNIT_DIR/"
chmod 644 "$UNIT_DIR/postup-r2-killswitch.service" "$UNIT_DIR/postup-r2-killswitch.timer"
if [[ ! -f "${HOME}/.config/postup/killswitch.env" ]]; then
  install -m 600 "$ROOT/killswitch.env.example" "${HOME}/.config/postup/killswitch.env"
fi
mkdir -p "${HOME}/.config/postup/killswitch"
chmod 700 "${HOME}/.config/postup/killswitch"
systemctl --user daemon-reload
systemctl --user enable --now postup-r2-killswitch.timer
systemctl --user start postup-r2-killswitch.service || true
systemctl --user list-timers --all | grep -e postup-r2-killswitch -e NEXT || true
echo "installed. logs: journalctl --user -u postup-r2-killswitch.service -n 50"
