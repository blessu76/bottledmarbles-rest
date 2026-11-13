#!/bin/bash
# Installs the journal gate: copies ops/gate_publish.py to ~/.ipe/bin, renders the plist into ~/Library/LaunchAgents, (re)loads it.
# The gate calls scripts/publish_next.py in the dedicated clone ~/.ipe/bottledmarbles-publish/repo (create it once:
#   git clone <origin of bottledmarbles-rest> ~/.ipe/bottledmarbles-publish/repo).  Re-run after any change to ops/.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
LABEL=rest.ipe.bottledmarbles.journal-gate
DEST="$HOME/Library/LaunchAgents/$LABEL.plist"
mkdir -p "$HOME/.ipe/bin" "$HOME/.ipe/logs" "$HOME/.ipe/queue/bottledmarbles"
install -m 755 "$HERE/gate_publish.py" "$HOME/.ipe/bin/bottledmarbles_gate.py"
sed "s#__HOME__#$HOME#g" "$HERE/$LABEL.plist" > "$DEST"
plutil -lint "$DEST" >/dev/null
launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$DEST"
launchctl list | grep "$LABEL"
