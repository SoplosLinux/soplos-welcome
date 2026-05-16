#!/bin/bash
# Soplos Linux - Fix audio DaVinci Resolve sin dispositivo de captura

CONF_DIR="/etc/pipewire/pipewire-pulse.conf.d"
CONF_FILE="$CONF_DIR/virtual-mic.conf"

if arecord -l 2>/dev/null | grep -q "card"; then
    echo "[INFO] Dispositivo de captura detectado. Parche no necesario."
    exit 0
fi

mkdir -p "$CONF_DIR"

cat > "$CONF_FILE" << 'EOF'
pulse.cmd = [
    { cmd = "load-module" args = "module-null-sink sink_name=virtmic sink_properties=device.description=VirtualMic" flags = [] }
    { cmd = "load-module" args = "module-virtual-source source_name=virtmic master=virtmic.monitor source_properties=device.description=VirtualMic" flags = [] }
]
EOF

echo "[OK] $CONF_FILE instalado."
