# Informe técnico — soplos-welcome: bugs drivers NVIDIA 590/610 y limpieza DKMS

## Contexto

Repositorio: https://github.com/SoplosLinux/soplos-welcome  
Archivo afectado: `ui/tabs/drivers_tab.py`  
Versión actual: 2.0.9-3  
Sistema base: Debian Testing (Forky/Trixie)  
Máquina de prueba: MSI GE60 2QE Apache Pro (i7-4720HQ, GTX 960M), kernel 7.1.1-soplos-bore-ntsync

---

## Bug 1 — Comillas mal escapadas en `repo_setup` para 590 y 610

### Ubicación

`_on_nvidia_cuda_repo_clicked()`, bloques `elif version == "590"` y `else` (610).

### Problema

El bloque `repo_setup` para 590 y 610 termina con:

```python
rm -rf \"$TEMP_DIR\\\"\"""
```

Dentro de una f-string con `"""`, esta secuencia de escapes genera bash inválido. La línea resultante en el script es:

```bash
rm -rf "$TEMP_DIR""
```

Bash lo interpreta como dos strings concatenadas. No provoca error fatal, pero si `wget` falla antes (timeout, repo no disponible), `set -e` aborta el script dejando el sistema a medias sin limpiar `$TEMP_DIR`. En la práctica los usuarios ven que el botón no hace nada visible porque el script muere silenciosamente.

### Fix

Cambiar ambos bloques a raw strings `r"""..."""` eliminando todos los escapes manuales:

```python
elif version == "590":
    repo_setup = r"""TEMP_DIR=$(mktemp -d)
wget -q -O "$TEMP_DIR/cuda-keyring.deb" \
    https://developer.download.nvidia.com/compute/cuda/repos/debian13/x86_64/cuda-keyring_1.1-1_all.deb
if [ ! -s "$TEMP_DIR/cuda-keyring.deb" ]; then
    echo "ERROR: Failed to download cuda-keyring."
    rm -rf "$TEMP_DIR"
    exit 1
fi
dpkg -i "$TEMP_DIR/cuda-keyring.deb"
rm -rf "$TEMP_DIR"
"""
    install_driver = "apt install -y nvidia-driver-pinning-590\napt install -y cuda-drivers-590"
    repo_cleanup = ""
else:  # 610
    repo_setup = r"""TEMP_DIR=$(mktemp -d)
wget -q -O "$TEMP_DIR/cuda-keyring.deb" \
    https://developer.download.nvidia.com/compute/cuda/repos/debian13/x86_64/cuda-keyring_1.1-1_all.deb
if [ ! -s "$TEMP_DIR/cuda-keyring.deb" ]; then
    echo "ERROR: Failed to download cuda-keyring."
    rm -rf "$TEMP_DIR"
    exit 1
fi
dpkg -i "$TEMP_DIR/cuda-keyring.deb"
rm -rf "$TEMP_DIR"
"""
    install_driver = "apt install -y nvidia-driver-pinning-610\napt install -y cuda-drivers-610"
    repo_cleanup = ""
```

---

## Bug 2 — El script de desinstalación no limpia los módulos DKMS del kernel

### Problema

`_on_uninstall_nvidia_clicked()` ejecuta `apt purge 'nvidia*' 'cuda*'` pero no elimina los módulos NVIDIA ya compilados e instalados en los kernels. Cuando el usuario instala después una versión diferente (ej. instala 610, luego intenta volver a 580), DKMS rechaza instalar el 580 porque encuentra módulos del 610 con versión superior ya presentes en el kernel:

```
Error! Module version 580.167.08 for nvidia.ko.xz
is not newer than what is already found in kernel 7.1.1-soplos-bore-ntsync (610.43.02).
You may override by specifying --force.
Error! Installation aborted.
```

Esto bloquea `dpkg --configure -a` en un bucle de error, dejando `nvidia-kernel-dkms`, `nvidia-driver` y `cuda-drivers-580` en estado `not configured`.

### Fix

Añadir al script de desinstalación, antes del `apt purge`, la limpieza explícita de DKMS y de los módulos compilados en todos los kernels presentes:

```bash
echo "[0/6] Removing NVIDIA DKMS modules from all kernels..."
# Remove all NVIDIA entries from DKMS tree
for entry in $(dkms status | grep -i nvidia | awk -F'[:,]' '{print $1"/"$2}' | tr -d ' '); do
    dkms remove "$entry" --all 2>/dev/null || true
done

# Force-remove compiled modules from all installed kernels
for kver in $(ls /lib/modules/); do
    rm -f /lib/modules/$kver/updates/dkms/nvidia*.ko*
    rm -f /lib/modules/$kver/updates/dkms/nvidia-*.ko*
    depmod -a "$kver" 2>/dev/null || true
done

rm -rf /var/lib/dkms/nvidia*
```

Este bloque debe ir **antes** del paso `[1/6] Fixing any interrupted dpkg state`.

---

## Bug 3 — `_on_nvidia_cuda_repo_clicked` no limpia DKMS antes de instalar

### Problema

El script de instalación de 580/590/610 ejecuta `apt purge 'nvidia*' 'cuda*'` al inicio (paso `[1/5]`), pero tampoco limpia DKMS ni los módulos compilados. Si el usuario tenía otra versión previamente instalada, el DKMS del paquete nuevo falla igual que en el Bug 2.

### Fix

Añadir el mismo bloque de limpieza DKMS del Bug 2 al inicio del script en `_on_nvidia_cuda_repo_clicked`, justo antes del `apt purge` existente:

```bash
echo "[0/5] Removing NVIDIA DKMS modules from all kernels..."
for entry in $(dkms status | grep -i nvidia | awk -F'[:,]' '{print $1"/"$2}' | tr -d ' '); do
    dkms remove "$entry" --all 2>/dev/null || true
done
for kver in $(ls /lib/modules/); do
    rm -f /lib/modules/$kver/updates/dkms/nvidia*.ko*
    depmod -a "$kver" 2>/dev/null || true
done
rm -rf /var/lib/dkms/nvidia*
```

Lo mismo aplica a `_on_nvidia_repo_clicked` (driver 550 desde repo Debian).

---

## Estado del MSI durante la sesión de diagnóstico

- El usuario había instalado el driver 610 desde el Welcome (funcionó la instalación)
- Al intentar volver al 580, el Welcome ejecutó purge pero dejó los módulos 610.43.02 compilados en el kernel
- `nvidia-kernel-dkms 580.167.08-1`, `nvidia-driver` y `cuda-drivers-580` quedaron en estado `not configured`
- `apt update && full-upgrade` fallaba en bucle al intentar configurar esos paquetes
- Solución manual aplicada: `rm -f` de módulos en `/lib/modules/7.1.0-soplos-bore-ntsync/updates/dkms/` + `depmod -a` + `dpkg --configure -a`
- El kernel activo en producción es **7.1.1-soplos-bore-ntsync**, no el 7.1.0

---

## Resumen de cambios necesarios en `drivers_tab.py`

1. `_on_nvidia_cuda_repo_clicked`: reescribir `repo_setup` de 590 y 610 con raw strings para corregir las comillas mal escapadas
2. `_on_uninstall_nvidia_clicked`: añadir limpieza DKMS y módulos de kernel antes del `apt purge`
3. `_on_nvidia_cuda_repo_clicked`: añadir limpieza DKMS al inicio del script de instalación
4. `_on_nvidia_repo_clicked`: añadir limpieza DKMS al inicio del script de instalación
