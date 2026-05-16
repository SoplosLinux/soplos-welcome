#!/bin/bash
# Soplos Linux - PPSSPP Flatpak: link binary as Lutris runner

LUTRIS_RUNNER_DIR="$HOME/.var/app/net.lutris.Lutris/data/lutris/runners/ppsspp"
LUTRIS_BINARY="$LUTRIS_RUNNER_DIR/PPSSPPSDL"

# Check if Lutris Flatpak is installed
if ! flatpak info net.lutris.Lutris &>/dev/null; then
    echo "[INFO] Lutris Flatpak not installed — skipping runner symlink."
    exit 0
fi

# Find PPSSPP binary inside Flatpak installation
PPSSPP_BIN=$(find "$HOME/.local/share/flatpak/app/org.ppsspp.PPSSPP" -name "PPSSPPSDL" -type f 2>/dev/null | head -1)

if [ -z "$PPSSPP_BIN" ]; then
    echo "[INFO] PPSSPP Flatpak binary not found — skipping runner symlink."
    exit 0
fi

mkdir -p "$LUTRIS_RUNNER_DIR"

# Back up existing Lutris PPSSPP binary if present and not already a symlink
if [ -f "$LUTRIS_BINARY" ] && [ ! -L "$LUTRIS_BINARY" ]; then
    mv "$LUTRIS_BINARY" "${LUTRIS_BINARY}.bak"
    echo "[OK] Backed up existing Lutris PPSSPPSDL to PPSSPPSDL.bak"
fi

# Create symlink if it doesn't exist yet
if [ ! -L "$LUTRIS_BINARY" ]; then
    ln -s "$PPSSPP_BIN" "$LUTRIS_BINARY"
    echo "[OK] Symlink created: $LUTRIS_BINARY -> $PPSSPP_BIN"
else
    echo "[INFO] Symlink already exists — skipping."
fi
