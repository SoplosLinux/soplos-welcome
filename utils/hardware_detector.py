"""
Hardware detection module for Soplos Welcome.
Detects system hardware and recommends appropriate drivers.
"""

import subprocess
import re
import os
import threading
from gi.repository import GLib
from core.i18n_manager import _


def _get_lspci_output():
    """Run lspci once and return output."""
    try:
        return subprocess.check_output(['lspci'], stderr=subprocess.DEVNULL).decode('utf-8')
    except Exception:
        return ''


def _get_lsusb_output():
    """Run lsusb once and return output."""
    try:
        return subprocess.check_output(['lsusb'], stderr=subprocess.DEVNULL).decode('utf-8')
    except Exception:
        return ''


def _is_package_installed(package):
    """Check if a dpkg package is installed."""
    try:
        result = subprocess.run(
            ['dpkg', '-s', package],
            capture_output=True, text=True
        )
        return 'Status: install ok installed' in result.stdout
    except Exception:
        return False


def _packages_status(required_packages):
    """Check status of a list of required packages. Returns (status, missing_list)."""
    missing = [p for p in required_packages if not _is_package_installed(p)]
    if not missing:
        return 'installed', []
    elif len(missing) == len(required_packages):
        return 'missing', missing
    else:
        return 'partial', missing


def _detect_installed_nvidia_driver():
    """Return major version string of installed NVIDIA driver, or None."""
    try:
        result = subprocess.run(
            ['nvidia-smi', '--query-gpu=driver_version', '--format=csv,noheader'],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.strip().split('.')[0]
            if version.isdigit():
                return version
    except Exception:
        pass

    try:
        result = subprocess.run(['dpkg', '-l'], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if not line.startswith('ii'):
                continue
            parts = line.split()
            if len(parts) >= 2 and re.fullmatch(r'nvidia-driver-(\d+)', parts[1]):
                return re.search(r'\d+', parts[1]).group()
    except Exception:
        pass

    return None


def _nvidia_driver_status(recommended_driver):
    """Check NVIDIA driver status. Returns (status, missing_packages, installed_version)."""
    installed_version = _detect_installed_nvidia_driver()

    if recommended_driver == 'nouveau':
        installed = _is_package_installed('xserver-xorg-video-nouveau')
        return (
            'installed' if installed else 'missing',
            [] if installed else ['xserver-xorg-video-nouveau'],
            None
        )

    if recommended_driver.startswith('nvidia-driver-'):
        rec_ver = re.search(r'(\d+)$', recommended_driver)
        rec_ver = rec_ver.group(1) if rec_ver else None
        if rec_ver and installed_version == rec_ver:
            return 'installed', [], installed_version
        elif installed_version:
            return 'different_version', [recommended_driver], installed_version
        else:
            return 'missing', [recommended_driver], None

    if recommended_driver == 'nvidia-driver':
        installed = _is_package_installed('nvidia-driver')
        if installed:
            return 'installed', [], installed_version
        elif installed_version:
            return 'different_version', ['nvidia-driver'], installed_version
        else:
            return 'missing', ['nvidia-driver'], None

    # Legacy drivers (nvidia-tesla-470-driver, nvidia-legacy-390xx-driver, etc.)
    installed = _is_package_installed(recommended_driver)
    return (
        'installed' if installed else 'missing',
        [] if installed else [recommended_driver],
        installed_version
    )


# ─────────────────────────── GPU ───────────────────────────

def _extract_nvidia_model(line):
    for pattern in [r'GeForce\s+(RTX\s+\d+)', r'GeForce\s+(GTX\s+\d+)',
                    r'GeForce\s+([^[(\n]+)', r'NVIDIA\s+([^[(\n]+)']:
        m = re.search(pattern, line, re.IGNORECASE)
        if m:
            return m.group(1).strip()
    return 'NVIDIA Unknown'


def _extract_amd_model(line):
    for pattern in [r'Radeon\s+(RX\s+\d+)', r'Radeon\s+(R\d+)',
                    r'Radeon\s+([^[(\n]+)', r'AMD\s+([^[(\n]+)']:
        m = re.search(pattern, line, re.IGNORECASE)
        if m:
            return m.group(1).strip()
    return 'AMD Unknown'


def _extract_intel_model(line):
    for pattern in [r'UHD Graphics\s+(\d+)', r'HD Graphics\s+(\d+)',
                    r'Iris\s+Xe\s+([^[(\n]+)', r'Iris\s+([^[(\n]+)',
                    r'Intel\s+([^[(\n]+)']:
        m = re.search(pattern, line, re.IGNORECASE)
        if m:
            return m.group(1).strip()
    return 'Intel Unknown'


def _recommend_nvidia_driver(model):
    model_lower = model.lower()

    if any(s in model_lower for s in ['rtx 50', 'rtx50', 'rtx 5090', 'rtx 5080', 'rtx 5070']):
        return 'nvidia-driver-610'
    if any(s in model_lower for s in ['rtx 40', 'rtx40', 'rtx 4090', 'rtx 4080', 'rtx 4070', 'rtx 4060']):
        return 'nvidia-driver-580'
    if any(s in model_lower for s in ['gtx 16', 'gtx16', 'gtx 1650', 'gtx 1660',
                                       'mx550', 'mx 550', 'mx450', 'mx 450']):
        return 'nvidia-driver-590'
    if any(s in model_lower for s in ['rtx 30', 'rtx30', 'rtx 3090', 'rtx 3080', 'rtx 3070', 'rtx 3060', 'rtx 3050',
                                       'rtx 20', 'rtx20',
                                       'gtx 10', 'gtx10', 'gtx 1080', 'gtx 1070', 'gtx 1060', 'gtx 1050', 'gt 1030',
                                       'mx350', 'mx 350', 'mx330', 'mx 330']):
        return 'nvidia-driver'
    if any(s in model_lower for s in ['gtx 9', 'gtx 980', 'gtx 970', 'gtx 960', 'gtx 950',
                                       'gtx 8', 'gtx 880', 'gtx 870', 'gtx 860', 'gtx 850',
                                       '920m', '930m', '940m', '920mx', '930mx', '940mx',
                                       '910m', '820m', '840m', '750m', '960m', '970m', '980m']):
        return 'nvidia-driver-580'
    if any(s in model_lower for s in ['gtx 7', 'gtx 780', 'gtx 770', 'gtx 760', 'gtx 750',
                                       'gtx 6', 'gtx 680', 'gtx 670', 'gtx 660', 'gtx 650',
                                       'gt 710', 'gt 720', 'gt 730', 'gt 740',
                                       'mx250', 'mx 250', 'mx230', 'mx 230',
                                       'mx150', 'mx 150', 'mx130', 'mx 130', 'mx110', 'mx 110', '650m']):
        return 'nvidia-tesla-470-driver'
    if any(s in model_lower for s in ['gtx 580', 'gtx 570', 'gtx 560', 'gtx 550',
                                       'gtx 480', 'gtx 470', 'gtx 460', 'gtx 450',
                                       'gtx 555', 'gtx 520', 'gtx 510',
                                       'gt 640', 'gt 630', 'gt 620', 'gt 610',
                                       'gt 545', 'gt 530', 'gt 520', 'gt 440', 'gt 430', 'gts 450']):
        return 'nvidia-legacy-390xx-driver'
    if any(s in model_lower for s in ['geforce 8', 'geforce 9', 'geforce 2', 'geforce 3',
                                       '8400', '8600', '8800', '9400', '9500', '9600', '9800',
                                       'gts ', '320m', '330m', 'quadro fx', 'quadro nvs', 'nforce']):
        return 'nouveau'
    if any(s in model_lower for s in ['quadro', 'tesla', 'a100', 'a40', 'a30', 'a10', 'rtx a']):
        return 'nvidia-driver'
    return 'nvidia-driver'


def detect_all_gpus(lspci_output=None):
    """Detect all GPUs. Returns list of dicts with driver_status info."""
    try:
        if lspci_output is None:
            lspci_output = _get_lspci_output()

        gpus = []
        nvidia_version_checked = False
        nvidia_installed_version = None

        for line in lspci_output.split('\n'):
            line_lower = line.lower()

            if not any(k in line_lower for k in ['vga', '3d', 'display']):
                continue

            # Virtual GPU — no real driver needed
            if any(k in line_lower for k in ['vmware svga', 'virtualbox graphics', 'vbox graphics',
                                              'qxl paravirtual', 'bochs vbe', 'virtio gpu', 'red hat qxl']):
                if 'vmware' in line_lower:
                    model = 'VMware SVGA II'
                elif 'virtualbox' in line_lower or 'vbox' in line_lower:
                    model = 'VirtualBox VGA'
                elif 'qxl' in line_lower or 'red hat' in line_lower:
                    model = 'QXL (QEMU/KVM)'
                elif 'virtio' in line_lower:
                    model = 'VirtIO GPU'
                else:
                    model = 'Virtual GPU'
                gpus.append({
                    'vendor': 'Virtual',
                    'model': model,
                    'type': _('Virtual'),
                    'recommended_driver': None,
                    'driver_status': 'installed',
                    'missing_packages': [],
                    'installed_driver_version': None
                })

            # NVIDIA
            elif re.search(r'\bnvidia\b', line_lower):
                model = _extract_nvidia_model(line)
                recommended = _recommend_nvidia_driver(model)
                if not nvidia_version_checked:
                    nvidia_installed_version = _detect_installed_nvidia_driver()
                    nvidia_version_checked = True
                status, missing, installed_ver = _nvidia_driver_status(recommended)
                gpus.append({
                    'vendor': 'NVIDIA',
                    'model': model,
                    'type': _('Dedicated'),
                    'recommended_driver': recommended,
                    'driver_status': status,
                    'missing_packages': missing,
                    'installed_driver_version': installed_ver or nvidia_installed_version
                })

            # AMD
            elif re.search(r'\b(amd|ati|radeon)\b', line_lower):
                model = _extract_amd_model(line)
                required = ['firmware-amd-graphics', 'libgl1-mesa-dri', 'libglx-mesa0',
                            'mesa-vulkan-drivers', 'xserver-xorg-video-all']
                status, missing = _packages_status(required)
                gpus.append({
                    'vendor': 'AMD',
                    'model': model,
                    'type': _('Dedicated/Integrated'),
                    'recommended_driver': ' '.join(required),
                    'driver_status': status,
                    'missing_packages': missing,
                    'installed_driver_version': None
                })

            # Intel
            elif re.search(r'\bintel\b', line_lower):
                model = _extract_intel_model(line)
                required = ['intel-media-va-driver', 'mesa-vulkan-drivers']
                status, missing = _packages_status(required)
                gpus.append({
                    'vendor': 'Intel',
                    'model': model,
                    'type': _('Integrated'),
                    'recommended_driver': ' '.join(required),
                    'driver_status': status,
                    'missing_packages': missing,
                    'installed_driver_version': None
                })

        return gpus

    except Exception as e:
        print(f"Error detecting GPUs: {e}")
        return []


# Keep for backwards compatibility (used by _on_detect_hybrid_clicked indirectly)
def detect_gpu(lspci_output=None):
    """Return primary GPU dict (for backwards compatibility)."""
    gpus = detect_all_gpus(lspci_output)
    for vendor in ('NVIDIA', 'AMD', 'Intel'):
        for gpu in gpus:
            if gpu['vendor'] == vendor:
                return gpu
    return gpus[0] if gpus else {
        'vendor': _('Unknown'), 'model': _('Not detected'),
        'recommended_driver': None, 'type': _('N/A'),
        'driver_status': 'missing', 'missing_packages': []
    }


def detect_hybrid_gpu(lspci_output=None):
    """Detect if the system has hybrid graphics (integrated + dedicated)."""
    try:
        if lspci_output is None:
            lspci_output = _get_lspci_output()

        nvidia_gpu = None
        intel_gpu = None
        amd_igpu = None

        for line in lspci_output.split('\n'):
            line_lower = line.lower()

            if not any(k in line_lower for k in ['vga', '3d', 'display']):
                continue

            if re.search(r'\bnvidia\b', line_lower):
                nvidia_gpu = f"NVIDIA {_extract_nvidia_model(line)}"
            elif re.search(r'\bintel\b', line_lower):
                intel_gpu = f"Intel {_extract_intel_model(line)}"
            elif re.search(r'\b(amd|ati|radeon)\b', line_lower):
                model = _extract_amd_model(line)
                model_lower = model.lower()
                if not any(s in model_lower for s in ['rx ', 'vega', 'vii', 'radeon pro']):
                    amd_igpu = f"AMD {model}"

        if intel_gpu and nvidia_gpu:
            return {'is_hybrid': True, 'integrated': intel_gpu, 'dedicated': nvidia_gpu}
        elif amd_igpu and nvidia_gpu:
            return {'is_hybrid': True, 'integrated': amd_igpu, 'dedicated': nvidia_gpu}

        primary = nvidia_gpu or intel_gpu or amd_igpu or _('Unknown')
        return {'is_hybrid': False, 'primary': primary}

    except Exception as e:
        print(f"Error detecting hybrid GPU: {e}")
        return {'is_hybrid': False, 'primary': _('Detection error')}


# ─────────────────────────── Wi-Fi ───────────────────────────

def _identify_wifi_vendor(line_lower):
    """Return (vendor_name, firmware_package) for a Wi-Fi device string."""
    if 'intel' in line_lower:
        return 'Intel', 'firmware-iwlwifi'
    elif 'realtek' in line_lower:
        return 'Realtek', 'firmware-realtek'
    elif 'broadcom' in line_lower or 'bcm' in line_lower:
        return 'Broadcom', 'firmware-b43-installer'
    elif 'atheros' in line_lower or 'qualcomm' in line_lower:
        return 'Atheros/Qualcomm', 'firmware-atheros'
    elif 'ralink' in line_lower or 'mediatek' in line_lower:
        return 'Ralink/MediaTek', 'firmware-ralink'
    elif 'marvell' in line_lower:
        return 'Marvell', 'firmware-libertas'
    else:
        return None, None


def detect_wifi(lspci_output=None, lsusb_output=None):
    """Detect Wi-Fi adapters and check firmware status."""
    try:
        if lspci_output is None:
            lspci_output = _get_lspci_output()
        if lsusb_output is None:
            lsusb_output = _get_lsusb_output()

        adapters = []
        seen = set()
        wifi_keywords = ['wireless', 'wifi', '802.11', 'wlan', 'wi-fi']

        for line in lspci_output.split('\n'):
            line_lower = line.lower()
            if not any(k in line_lower for k in wifi_keywords):
                continue
            vendor, firmware = _identify_wifi_vendor(line_lower)
            if not vendor:
                vendor = 'Unknown'
            key = (vendor, firmware)
            if key in seen:
                continue
            seen.add(key)
            missing = [firmware] if firmware and not _is_package_installed(firmware) else []
            adapters.append({
                'model': line.split(':')[-1].strip()[:60],
                'vendor': vendor,
                'firmware_package': firmware,
                'driver_status': 'missing' if missing else 'installed',
                'missing_packages': missing
            })

        for line in lsusb_output.split('\n'):
            line_lower = line.lower()
            if not any(k in line_lower for k in wifi_keywords):
                continue
            vendor, firmware = _identify_wifi_vendor(line_lower)
            if not vendor:
                vendor = 'Unknown'
            key = (vendor, firmware)
            if key in seen:
                continue
            seen.add(key)
            model = line.split(':', 3)[-1].strip()[:60] if ':' in line else line.strip()[:60]
            missing = [firmware] if firmware and not _is_package_installed(firmware) else []
            adapters.append({
                'model': model,
                'vendor': vendor,
                'firmware_package': firmware,
                'driver_status': 'missing' if missing else 'installed',
                'missing_packages': missing
            })

        return adapters

    except Exception as e:
        print(f"Error detecting Wi-Fi: {e}")
        return []


# ─────────────────────────── Audio ───────────────────────────

def detect_audio(lspci_output=None):
    """Detect audio devices and check driver status."""
    try:
        if lspci_output is None:
            lspci_output = _get_lspci_output()

        devices = []
        audio_keywords = ['audio', 'sound', 'multimedia audio', 'high definition audio', 'ac97']

        for line in lspci_output.split('\n'):
            line_lower = line.lower()
            if not any(k in line_lower for k in audio_keywords):
                continue

            model = line.split(':')[-1].strip()[:60]
            has_alsa = _is_package_installed('alsa-utils')
            has_server = (_is_package_installed('pulseaudio') or
                          _is_package_installed('pipewire-pulse') or
                          _is_package_installed('pipewire'))

            if has_alsa and has_server:
                status = 'installed'
                missing = []
            elif has_alsa:
                status = 'partial'
                missing = ['pulseaudio']
            else:
                status = 'missing'
                missing = ['alsa-utils', 'pulseaudio']

            devices.append({
                'model': model,
                'driver_status': status,
                'missing_packages': missing,
                'required_packages': ['alsa-utils', 'pulseaudio']
            })

        return devices

    except Exception as e:
        print(f"Error detecting audio: {e}")
        return []


# ─────────────────────────── Bluetooth ───────────────────────────

def detect_bluetooth(lsusb_output=None, lspci_output=None):
    """Detect Bluetooth hardware and check driver status."""
    try:
        if lsusb_output is None:
            lsusb_output = _get_lsusb_output()
        if lspci_output is None:
            lspci_output = _get_lspci_output()

        detected = False
        model = None

        for line in lsusb_output.split('\n'):
            if 'bluetooth' in line.lower():
                detected = True
                model = (line.split(':', 3)[-1].strip()[:50]
                         if ':' in line else 'Bluetooth USB')
                break

        if not detected:
            for line in lspci_output.split('\n'):
                if 'bluetooth' in line.lower():
                    detected = True
                    model = line.split(':')[-1].strip()[:50]
                    break

        if not detected:
            return None

        required = ['bluetooth', 'bluez']
        status, missing = _packages_status(required)

        return {
            'model': model or 'Bluetooth Controller',
            'driver_status': status,
            'missing_packages': missing,
            'required_packages': required
        }

    except Exception as e:
        print(f"Error detecting Bluetooth: {e}")
        return None


# ─────────────────────────── Printers ───────────────────────────

def detect_printers(lsusb_output=None):
    """Detect USB printers and check driver status."""
    try:
        if lsusb_output is None:
            lsusb_output = _get_lsusb_output()

        detected = False
        model = None

        for line in lsusb_output.split('\n'):
            if 'printer' in line.lower():
                detected = True
                model = (line.split(':', 3)[-1].strip()[:50]
                         if ':' in line else 'USB Printer')
                break

        if not detected:
            return None

        required = ['cups', 'printer-driver-all']
        status, missing = _packages_status(required)

        return {
            'model': model or 'USB Printer',
            'driver_status': status,
            'missing_packages': missing,
            'required_packages': required
        }

    except Exception as e:
        print(f"Error detecting printers: {e}")
        return None


# ─────────────────────────── VM ───────────────────────────

def _get_vm_required_packages(vm_lower):
    if 'vmware' in vm_lower:
        return ['open-vm-tools', 'open-vm-tools-desktop']
    elif 'kvm' in vm_lower or 'qemu' in vm_lower:
        return ['qemu-guest-agent', 'spice-vdagent']
    elif 'microsoft' in vm_lower:
        return ['hyperv-daemons']
    else:
        return []


def detect_vm():
    """Detect VM type and check whether guest tools are installed."""
    try:
        vm_raw = None

        result = subprocess.run(['systemd-detect-virt'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0 and result.stdout.strip() != 'none':
            vm_raw = result.stdout.strip().lower()

        if not vm_raw:
            for dmi_file in ['/sys/class/dmi/id/sys_vendor', '/sys/class/dmi/id/product_name']:
                if os.path.exists(dmi_file):
                    with open(dmi_file, 'r') as f:
                        content = f.read().lower()
                    if 'vmware' in content:
                        vm_raw = 'vmware'
                    elif 'virtualbox' in content:
                        vm_raw = 'oracle'
                    elif 'qemu' in content or 'kvm' in content:
                        vm_raw = 'kvm'
                    if vm_raw:
                        break

        if not vm_raw:
            return {'is_vm': False, 'type': None}

        # Human-readable name and install key
        if 'vmware' in vm_raw:
            display = 'VMware'
            vm_key = 'vmware'
        elif 'oracle' in vm_raw or 'virtualbox' in vm_raw:
            display = 'VirtualBox'
            vm_key = 'vbox'
        elif 'kvm' in vm_raw or 'qemu' in vm_raw:
            display = 'QEMU/KVM'
            vm_key = 'qemu'
        elif 'microsoft' in vm_raw:
            display = 'Hyper-V'
            vm_key = 'hyperv'
        else:
            display = vm_raw.title()
            vm_key = 'other'

        # VirtualBox: check vboxadd service (not an apt package)
        if vm_key == 'vbox':
            try:
                r = subprocess.run(['systemctl', 'is-enabled', 'vboxadd'],
                                   capture_output=True, text=True, timeout=5)
                vbox_ok = (r.returncode == 0)
            except Exception:
                vbox_ok = False
            return {
                'is_vm': True,
                'type': display,
                'vm_key': vm_key,
                'driver_status': 'installed' if vbox_ok else 'missing',
                'missing_packages': [] if vbox_ok else ['VirtualBox Guest Additions'],
                'required_packages': ['VirtualBox Guest Additions']
            }

        required = _get_vm_required_packages(vm_raw)
        if required:
            status, missing = _packages_status(required)
        else:
            status, missing = 'installed', []

        return {
            'is_vm': True,
            'type': display,
            'vm_key': vm_key,
            'driver_status': status,
            'missing_packages': missing,
            'required_packages': required
        }

    except Exception as e:
        print(f"Error detecting VM: {e}")
        return {'is_vm': False, 'type': None}


# ─────────────────────────── Unnecessary software ───────────────────────────

def _get_installed_packages_matching(pattern):
    """Return installed package names matching a regex, via dpkg pattern
    match — not a fixed list, so new driver/CUDA/ROCm package names from
    future releases are still caught without updating this code."""
    try:
        result = subprocess.run(['dpkg', '-l'], capture_output=True, text=True)
        pkgs = []
        for line in result.stdout.split('\n'):
            if not line.startswith('ii'):
                continue
            parts = line.split()
            if len(parts) >= 2 and re.match(pattern, parts[1], re.IGNORECASE):
                pkgs.append(parts[1])
        return pkgs
    except Exception:
        return []


def _get_installed_from_list(names):
    """Return the subset of `names` that are actually installed."""
    return [p for p in names if _is_package_installed(p)]


def _is_vboxadd_enabled():
    """Same check already used in detect_vm() — VirtualBox Guest Additions
    are installed via the official .run installer, never as an apt package,
    so presence is checked via the systemd service it registers."""
    try:
        r = subprocess.run(['systemctl', 'is-enabled', 'vboxadd'],
                            capture_output=True, text=True, timeout=5)
        return r.returncode == 0
    except Exception:
        return False


def detect_unnecessary_software(results):
    """
    Detects installed software that doesn't match the hardware actually
    present on this machine, using the same scan `results` dict that
    scan_hardware() assembles (needs 'gpus', 'wifi' and 'vm_detection'
    already populated):
      - NVIDIA driver/CUDA packages installed but no NVIDIA GPU detected.
      - AMD GPU/ROCm packages installed but no AMD GPU detected.
      - Broadcom proprietary WiFi driver installed but no Broadcom WiFi
        adapter detected.
      - VM guest tools (open-vm-tools, qemu-guest-agent, spice-*,
        hyperv-daemons) installed but this machine is not a VM at all.
      - VirtualBox Guest Additions active but this machine is not a VM.

    Deliberately does NOT check printers/Bluetooth/generic Intel packages:
    those are commonly kept installed even without hardware currently
    attached (removable peripherals, or bundled by default), so flagging
    them would be a false positive, not a real "unused driver".

    Returns a list of {'name', 'detail', 'packages', 'action'} — 'action'
    tells the UI which existing uninstall flow to reuse: 'nvidia', 'vbox',
    or 'generic' (plain apt purge of 'packages', via the already-fixed
    _on_remove_driver_clicked).
    """
    findings = []
    gpus = results.get('gpus', [])
    wifi_adapters = results.get('wifi', [])
    vm_info = results.get('vm_detection', {})

    gpu_vendors = {g.get('vendor', '').upper() for g in gpus}
    wifi_vendors = {w.get('vendor', '') for w in wifi_adapters}

    # NVIDIA
    if 'NVIDIA' not in gpu_vendors:
        pkgs = _get_installed_packages_matching(r'^(nvidia|libnvidia|cuda)')
        if pkgs:
            findings.append({
                'name': _('NVIDIA / CUDA packages'),
                'detail': _('{} package(s) installed, no NVIDIA GPU detected').format(len(pkgs)),
                'packages': pkgs,
                'action': 'nvidia',
            })

    # AMD
    if 'AMD' not in gpu_vendors:
        pkgs = _get_installed_from_list([
            'xserver-xorg-video-amdgpu', 'xserver-xorg-video-ati',
            'xserver-xorg-video-radeon', 'radeontop',
        ]) + _get_installed_packages_matching(r'^rocm')
        if pkgs:
            findings.append({
                'name': _('AMD GPU / ROCm packages'),
                'detail': _('{} package(s) installed, no AMD GPU detected').format(len(pkgs)),
                'packages': pkgs,
                'action': 'generic',
            })

    # Broadcom proprietary WiFi driver
    if 'Broadcom' not in wifi_vendors:
        pkgs = _get_installed_from_list([
            'broadcom-sta-dkms', 'bcmwl-kernel-source', 'firmware-b43-installer',
        ])
        if pkgs:
            findings.append({
                'name': _('Broadcom WiFi driver'),
                'detail': _('{} package(s) installed, no Broadcom WiFi adapter detected').format(len(pkgs)),
                'packages': pkgs,
                'action': 'generic',
            })

    # VM guest tools (any hypervisor) when this is not a VM at all
    if not vm_info.get('is_vm'):
        pkgs = _get_installed_from_list([
            'open-vm-tools', 'open-vm-tools-desktop',
            'qemu-guest-agent', 'spice-vdagent', 'spice-webdavd',
            'hyperv-daemons',
        ])
        if pkgs:
            findings.append({
                'name': _('Virtual machine guest tools'),
                'detail': _('{} package(s) installed, but this machine is not a virtual machine').format(len(pkgs)),
                'packages': pkgs,
                'action': 'generic',
            })

        if _is_vboxadd_enabled():
            findings.append({
                'name': _('VirtualBox Guest Additions'),
                'detail': _('Active, but this machine is not running inside a virtual machine'),
                'packages': [],
                'action': 'vbox',
            })

    return findings


# ─────────────────────────── CPU / RAM / Storage / Network ───────────────────────────

def detect_cpu():
    """Detect CPU information."""
    try:
        with open('/proc/cpuinfo', 'r') as f:
            cpuinfo = f.read()
        model_match = re.search(r'model name\s*:\s*(.+)', cpuinfo)
        model = model_match.group(1).strip() if model_match else _('Unknown')
        threads = len(re.findall(r'processor\s*:', cpuinfo))
        physical_cores = len(set(re.findall(r'core id\s*:\s*(\d+)', cpuinfo)))
        cores = physical_cores if physical_cores > 0 else threads
        return {'model': model, 'cores': cores, 'threads': threads}
    except Exception as e:
        print(f"Error detecting CPU: {e}")
        return {'model': _('Error'), 'cores': 0, 'threads': 0}


def detect_memory():
    """Detect RAM information."""
    try:
        with open('/proc/meminfo', 'r') as f:
            meminfo = f.read()
        total_match = re.search(r'MemTotal:\s*(\d+)\s*kB', meminfo)
        available_match = re.search(r'MemAvailable:\s*(\d+)\s*kB', meminfo)
        total_gb = int(total_match.group(1)) // 1024 // 1024 if total_match else 0
        available_gb = int(available_match.group(1)) // 1024 // 1024 if available_match else 0
        return {'total': f"{total_gb} GB", 'available': f"{available_gb} GB"}
    except Exception as e:
        print(f"Error detecting memory: {e}")
        return {'total': _('Error'), 'available': _('Error')}


def detect_storage():
    """Detect storage devices."""
    try:
        result = subprocess.run(['lsblk', '-d', '-o', 'NAME,SIZE,TYPE'],
                                capture_output=True, text=True)
        if result.returncode == 0:
            devices = []
            for line in result.stdout.strip().split('\n')[1:]:
                parts = line.split()
                if len(parts) >= 3 and parts[2] == 'disk':
                    devices.append({'name': parts[0], 'size': parts[1], 'type': _('Disk')})
            return devices
        return []
    except Exception as e:
        print(f"Error detecting storage: {e}")
        return []


def detect_network():
    """Detect network interfaces."""
    try:
        interfaces = []
        if os.path.exists('/sys/class/net'):
            for iface in os.listdir('/sys/class/net'):
                if iface == 'lo':
                    continue
                info = {'name': iface}
                if iface.startswith('wl'):
                    info['type'] = _('Wi-Fi')
                elif iface.startswith('en') or iface.startswith('eth'):
                    info['type'] = _('Ethernet')
                else:
                    info['type'] = _('Other')
                mac_path = f'/sys/class/net/{iface}/address'
                if os.path.exists(mac_path):
                    with open(mac_path, 'r') as f:
                        info['mac'] = f.read().strip()
                state_path = f'/sys/class/net/{iface}/operstate'
                if os.path.exists(state_path):
                    with open(state_path, 'r') as f:
                        state = f.read().strip()
                        info['status'] = _('Connected') if state == 'up' else _('Disconnected')
                interfaces.append(info)
        return interfaces
    except Exception as e:
        print(f"Error detecting network: {e}")
        return []


# ─────────────────────────── Main scan ───────────────────────────

def scan_hardware(update_status_cb, update_progress_cb, show_results_cb):
    """
    Scan all hardware and driver status in a background thread.
    Calls show_results_cb(results) on the GTK main thread when done.
    """

    def scan_thread():
        results = {}

        GLib.idle_add(update_status_cb, _('Detecting hardware...'))
        GLib.idle_add(update_progress_cb, 0.05)
        lspci_output = _get_lspci_output()
        lsusb_output = _get_lsusb_output()

        GLib.idle_add(update_status_cb, _('Detecting CPU...'))
        GLib.idle_add(update_progress_cb, 0.1)
        results['cpu'] = detect_cpu()

        GLib.idle_add(update_status_cb, _('Detecting memory...'))
        GLib.idle_add(update_progress_cb, 0.2)
        results['memory'] = detect_memory()

        GLib.idle_add(update_status_cb, _('Detecting GPU...'))
        GLib.idle_add(update_progress_cb, 0.3)
        results['gpus'] = detect_all_gpus(lspci_output)

        GLib.idle_add(update_status_cb, _('Detecting hybrid graphics...'))
        GLib.idle_add(update_progress_cb, 0.38)
        results['hybrid_gpu'] = detect_hybrid_gpu(lspci_output)

        GLib.idle_add(update_status_cb, _('Detecting Wi-Fi...'))
        GLib.idle_add(update_progress_cb, 0.46)
        results['wifi'] = detect_wifi(lspci_output, lsusb_output)

        GLib.idle_add(update_status_cb, _('Detecting audio...'))
        GLib.idle_add(update_progress_cb, 0.54)
        results['audio'] = detect_audio(lspci_output)

        GLib.idle_add(update_status_cb, _('Detecting Bluetooth...'))
        GLib.idle_add(update_progress_cb, 0.62)
        results['bluetooth'] = detect_bluetooth(lsusb_output, lspci_output)

        GLib.idle_add(update_status_cb, _('Detecting printers...'))
        GLib.idle_add(update_progress_cb, 0.70)
        results['printers'] = detect_printers(lsusb_output)

        GLib.idle_add(update_status_cb, _('Detecting virtual machine...'))
        GLib.idle_add(update_progress_cb, 0.78)
        results['vm_detection'] = detect_vm()

        GLib.idle_add(update_status_cb, _('Checking for unnecessary software...'))
        GLib.idle_add(update_progress_cb, 0.82)
        results['unnecessary_software'] = detect_unnecessary_software(results)

        GLib.idle_add(update_status_cb, _('Detecting storage...'))
        GLib.idle_add(update_progress_cb, 0.86)
        results['storage'] = detect_storage()

        GLib.idle_add(update_status_cb, _('Detecting network...'))
        GLib.idle_add(update_progress_cb, 0.94)
        results['network'] = detect_network()

        GLib.idle_add(update_status_cb, _('Scan completed'))
        GLib.idle_add(update_progress_cb, 1.0)
        GLib.idle_add(show_results_cb, results)

    t = threading.Thread(target=scan_thread, daemon=True)
    t.start()
