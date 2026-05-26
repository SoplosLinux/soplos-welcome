#!/bin/bash
# Soplos Linux - Fix Lutris Flatpak: vulkaninfo path (gpu.py patch)

GPU_PY=$(find -L ~/.local/share/flatpak/app/net.lutris.Lutris/x86_64/stable/active -name gpu.py 2>/dev/null | head -1)
# Fallback: search all architectures/branches if the standard path is missing
if [ -z "$GPU_PY" ]; then
    GPU_PY=$(find -L ~/.local/share/flatpak/app/net.lutris.Lutris -path "*/active/*" -name gpu.py 2>/dev/null | head -1)
fi

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
