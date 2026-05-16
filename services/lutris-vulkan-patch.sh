#!/bin/bash
# Soplos Linux - Fix Lutris Flatpak: vulkaninfo path (gpu.py patch)

GPU_PY=$(find ~/.local/share/flatpak/app/net.lutris.Lutris -name gpu.py 2>/dev/null | head -1)

if [ -z "$GPU_PY" ]; then
    echo "[INFO] gpu.py not found in Lutris Flatpak — skipping patch."
    exit 0
fi

if grep -q '/app/bin/vulkaninfo' "$GPU_PY"; then
    echo "[INFO] Patch already applied."
    exit 0
fi

cp "$GPU_PY" /tmp/gpu.py.bak
sed -i 's|/usr/bin/vulkaninfo|/app/bin/vulkaninfo|g' "$GPU_PY"

echo "[OK] Lutris Vulkan patch applied to $GPU_PY"
