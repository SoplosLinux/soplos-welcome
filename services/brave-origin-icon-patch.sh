#!/bin/bash
# Soplos Linux - Brave Origin: replace bundled orange icon with black icon
# Arg $1: path to brave-origin-icons directory (NxN/apps/brave-origin.png structure)
# Must run as root (called from pkexec install script)

ICONS_SRC="${1}"

if [ -z "$ICONS_SRC" ] || [ ! -d "$ICONS_SRC" ]; then
    echo "[ERROR] Icons source directory not found: $ICONS_SRC"
    exit 1
fi

for size in 16 24 32 48 64 128 256; do
    src="$ICONS_SRC/${size}x${size}/apps/brave-origin.png"
    if [ ! -f "$src" ]; then
        echo "[WARN] Missing icon size ${size}: $src"
        continue
    fi

    # Install into hicolor theme
    dest_dir="/usr/share/icons/hicolor/${size}x${size}/apps"
    mkdir -p "$dest_dir"
    cp "$src" "$dest_dir/brave-origin.png"

    # Replace /opt source so postinst restores the black icon on package updates
    opt_dest="/opt/brave.com/brave-origin/product_logo_${size}.png"
    if [ -f "$opt_dest" ]; then
        cp "$src" "$opt_dest"
    fi
done

# Patch .desktop files: use absolute path so KDE Kickoff ignores sycoca cache
for desktop in /usr/share/applications/brave-origin.desktop \
               /usr/share/applications/com.brave.Origin.desktop; do
    if [ -f "$desktop" ]; then
        sed -i 's|^Icon=brave-origin$|Icon=/usr/share/icons/hicolor/256x256/apps/brave-origin.png|' "$desktop"
        echo "[OK] Patched $desktop"
    fi
done

# Refresh icon cache
gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true

# KDE only
if command -v kbuildsycoca6 &>/dev/null; then
    kbuildsycoca6 --noincremental 2>/dev/null || true
fi

echo "[OK] Brave Origin icon patch complete"
