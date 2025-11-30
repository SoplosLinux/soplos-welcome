#!/usr/bin/env bash
# Soplos Gaming Performance Wrapper
# Basado en game-performance de CachyOS
# Cambia temporalmente el perfil de energía a "performance" al lanzar juegos

if ! command -v powerprofilesctl &>/dev/null; then
    echo "Error: powerprofilesctl no encontrado" >&2
    echo "Instala: sudo apt install power-profiles-daemon" >&2
    exit 1
fi

# Verificar soporte de perfil performance
if ! powerprofilesctl list | grep -q 'performance:'; then
    echo "Advertencia: Tu CPU no soporta el perfil performance" >&2
    echo "Ejecutando sin optimización de perfil de energía..." >&2
    exec "$@"
fi

# Lanzar con perfil performance e inhibir suspensión
exec systemd-inhibit --why "Soplos Gaming Mode activo" powerprofilesctl launch \
    -p performance -r "Lanzado con Soplos Gaming Performance" -- "$@"
