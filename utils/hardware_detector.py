"""
Hardware detection module for Soplos Welcome.
Detects system hardware and recommends appropriate drivers.
"""

import subprocess
import re
import os
from gi.repository import GLib
from core.i18n_manager import _


def detect_gpu():
    """Detect GPU and recommend driver."""
    try:
        lspci_output = subprocess.check_output(['lspci'], stderr=subprocess.DEVNULL).decode('utf-8')
        
        # Store all detected GPUs
        nvidia_gpus = []
        amd_gpus = []
        intel_gpus = []
        
        for line in lspci_output.split('\n'):
            line_lower = line.lower()
            
            # Skip if not a display device
            if not any(k in line_lower for k in ['vga', '3d', 'display']):
                continue
            
            # NVIDIA GPU (word boundary to avoid false positives)
            if re.search(r'\bnvidia\b', line_lower):
                model = _extract_nvidia_model(line)
                driver = _recommend_nvidia_driver(model)
                nvidia_gpus.append({
                    'vendor': 'NVIDIA',
                    'model': model,
                    'recommended_driver': driver,
                    'type': _('Dedicated')
                })
            
            # AMD GPU (word boundaries for amd, ati, radeon)
            elif re.search(r'\b(amd|ati|radeon)\b', line_lower):
                model = _extract_amd_model(line)
                amd_gpus.append({
                    'vendor': 'AMD',
                    'model': model,
                    'recommended_driver': 'firmware-amd-graphics libgl1-mesa-dri mesa-vulkan-drivers',
                    'type': _('Dedicated/Integrated')
                })
            
            # Intel GPU (word boundary)
            elif re.search(r'\bintel\b', line_lower):
                model = _extract_intel_model(line)
                intel_gpus.append({
                    'vendor': 'Intel',
                    'model': model,
                    'recommended_driver': 'intel-media-va-driver mesa-vulkan-drivers',
                    'type': _('Integrated')
                })
        
        # Priority: NVIDIA > AMD > Intel
        # Return the most relevant GPU (dedicated over integrated)
        if nvidia_gpus:
            return nvidia_gpus[0]
        elif amd_gpus:
            return amd_gpus[0]
        elif intel_gpus:
            return intel_gpus[0]
        
        return {'vendor': _('Unknown'), 'model': _('Not detected'), 'recommended_driver': None, 'type': _('N/A')}
    
    except Exception as e:
        print(f"Error detecting GPU: {e}")
        return {'vendor': _('Error'), 'model': str(e), 'recommended_driver': None, 'type': _('N/A')}


def _extract_nvidia_model(line):
    """Extract NVIDIA GPU model from lspci line."""
    patterns = [
        r'GeForce\s+(RTX\s+\d+)',
        r'GeForce\s+(GTX\s+\d+)',
        r'GeForce\s+([^[(\n]+)',
        r'NVIDIA\s+([^[(\n]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, line, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    return "NVIDIA Unknown"


def _recommend_nvidia_driver(model):
    """Recommend NVIDIA driver based on model."""
    model_lower = model.lower()
    
    # RTX 50 series (Blackwell) - Requires driver 580+
    if any(s in model_lower for s in ['rtx 50', 'rtx50']):
        return 'nvidia-driver-580'
    
    # RTX 40 series (Ada Lovelace) - Requires driver 580+
    elif any(s in model_lower for s in ['rtx 40', 'rtx40']):
        return 'nvidia-driver-580'
    
    # RTX 30/20 series, GTX 16xx (Ampere, Turing) - Repo driver works
    elif any(s in model_lower for s in ['rtx 30', 'rtx 20', 'gtx 16']):
        return 'nvidia-driver'
    
    # GTX 10xx series (Pascal) - Repo driver works
    elif 'gtx 10' in model_lower:
        return 'nvidia-driver'
    
    # Legacy 470 (GTX 900/700/600, Kepler/Maxwell)
    elif any(s in model_lower for s in ['gtx 9', 'gtx 7', 'gtx 6']):
        return 'nvidia-driver-470'
    
    # Legacy 390 (GTX 400/500, Fermi)
    elif any(s in model_lower for s in ['gtx 5', 'gtx 4']):
        return 'nvidia-driver-390'
    
    # Legacy 340 (Very old: 8xxx, 9xxx, 2xx, 3xx)
    elif any(s in model_lower for s in ['gt ', 'gts', 'geforce 8', 'geforce 9']):
        return 'nvidia-driver-340'
    
    # Default - latest from NVIDIA (safer for unknown models)
    else:
        return 'nvidia-driver-580'


def _extract_amd_model(line):
    """Extract AMD GPU model from lspci line."""
    patterns = [
        r'Radeon\s+(RX\s+\d+)',
        r'Radeon\s+(R\d+)',
        r'Radeon\s+([^[(\n]+)',
        r'AMD\s+([^[(\n]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, line, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    return "AMD Unknown"


def _extract_intel_model(line):
    """Extract Intel GPU model from lspci line."""
    patterns = [
        r'UHD Graphics\s+(\d+)',
        r'HD Graphics\s+(\d+)',
        r'Iris\s+Xe\s+([^[(\n]+)',
        r'Iris\s+([^[(\n]+)',
        r'Intel\s+([^[(\n]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, line, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    return "Intel Unknown"


def detect_cpu():
    """Detect CPU information."""
    try:
        with open('/proc/cpuinfo', 'r') as f:
            cpuinfo = f.read()
        
        # Extract model name
        model_match = re.search(r'model name\s*:\s*(.+)', cpuinfo)
        model = model_match.group(1).strip() if model_match else _('Unknown')
        
        # Count cores and threads
        threads = len(re.findall(r'processor\s*:', cpuinfo))
        physical_cores = len(set(re.findall(r'core id\s*:\s*(\d+)', cpuinfo)))
        cores = physical_cores if physical_cores > 0 else threads
        
        return {
            'model': model,
            'cores': cores,
            'threads': threads
        }
    
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
        
        return {
            'total': f"{total_gb} GB",
            'available': f"{available_gb} GB"
        }
    
    except Exception as e:
        print(f"Error detecting memory: {e}")
        return {'total': _('Error'), 'available': _('Error')}


def detect_vm():
    """Detect if running in a virtual machine."""
    try:
        # Method 1: systemd-detect-virt
        result = subprocess.run(['systemd-detect-virt'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0 and result.stdout.strip() != 'none':
            vm_type = result.stdout.strip().title()
            return {
                'is_vm': True,
                'type': vm_type,
                'recommended_tools': _get_vm_tools(vm_type)
            }
        
        # Method 2: DMI
        dmi_files = [
            '/sys/class/dmi/id/sys_vendor',
            '/sys/class/dmi/id/product_name'
        ]
        
        for dmi_file in dmi_files:
            if os.path.exists(dmi_file):
                with open(dmi_file, 'r') as f:
                    content = f.read().lower()
                    if 'vmware' in content:
                        return {'is_vm': True, 'type': 'VMware', 'recommended_tools': 'open-vm-tools-desktop'}
                    elif 'virtualbox' in content:
                        return {'is_vm': True, 'type': 'VirtualBox', 'recommended_tools': 'Guest Additions'}
                    elif 'qemu' in content or 'kvm' in content:
                        return {'is_vm': True, 'type': 'QEMU/KVM', 'recommended_tools': 'qemu-guest-agent spice-vdagent'}
        
        return {'is_vm': False, 'type': None, 'recommended_tools': None}
    
    except Exception as e:
        print(f"Error detecting VM: {e}")
        return {'is_vm': False, 'type': None, 'recommended_tools': None}


def _get_vm_tools(vm_type):
    """Get recommended VM tools."""
    vm_lower = vm_type.lower()
    if 'vmware' in vm_lower:
        return 'open-vm-tools-desktop'
    elif 'virtualbox' in vm_lower or 'vbox' in vm_lower:
        return 'Guest Additions'
    elif 'qemu' in vm_lower or 'kvm' in vm_lower:
        return 'qemu-guest-agent spice-vdagent'
    else:
        return None


def detect_storage():
    """Detect storage devices."""
    try:
        result = subprocess.run(['lsblk', '-d', '-o', 'NAME,SIZE,TYPE'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            devices = []
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            for line in lines:
                parts = line.split()
                if len(parts) >= 3 and parts[2] == 'disk':
                    devices.append({
                        'name': parts[0],
                        'size': parts[1],
                        'type': _('Disk')
                    })
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
                if iface != 'lo':  # Ignore loopback
                    info = {'name': iface}
                    
                    # Determine type
                    if iface.startswith('wl'):
                        info['type'] = _('Wi-Fi')
                    elif iface.startswith('en') or iface.startswith('eth'):
                        info['type'] = _('Ethernet')
                    else:
                        info['type'] = _('Other')
                    
                    # Get MAC
                    mac_path = f'/sys/class/net/{iface}/address'
                    if os.path.exists(mac_path):
                        with open(mac_path, 'r') as f:
                            info['mac'] = f.read().strip()
                    
                    # Get status
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


def scan_hardware(update_status_cb, update_progress_cb, show_results_cb):
    """
    Scan all hardware and display results.
    
    Args:
        update_status_cb: Callback to update status text
        update_progress_cb: Callback to update progress (0.0-1.0)
        show_results_cb: Callback to show results dialog with hardware info dict
    """
    def scan_thread():
        results = {}
        
        # CPU
        GLib.idle_add(update_status_cb, _('Detecting CPU...'))
        GLib.idle_add(update_progress_cb, 0.1)
        results['cpu'] = detect_cpu()
        
        # Memory
        GLib.idle_add(update_status_cb, _('Detecting memory...'))
        GLib.idle_add(update_progress_cb, 0.2)
        results['memory'] = detect_memory()
        
        # GPU
        GLib.idle_add(update_status_cb, _('Detecting GPU...'))
        GLib.idle_add(update_progress_cb, 0.4)
        results['gpu'] = detect_gpu()
        
        # VM Detection
        GLib.idle_add(update_status_cb, _('Detecting virtual machine...'))
        GLib.idle_add(update_progress_cb, 0.6)
        results['vm_detection'] = detect_vm()
        
        # Storage
        GLib.idle_add(update_status_cb, _('Detecting storage...'))
        GLib.idle_add(update_progress_cb, 0.8)
        results['storage'] = detect_storage()
        
        # Network
        GLib.idle_add(update_status_cb, _('Detecting network...'))
        GLib.idle_add(update_progress_cb, 0.9)
        results['network'] = detect_network()
        
        # Show results
        GLib.idle_add(update_status_cb, _('Scan completed'))
        GLib.idle_add(update_progress_cb, 1.0)
        GLib.idle_add(show_results_cb, results)
    
    # Run scan in thread
    import threading
    thread = threading.Thread(target=scan_thread)
    thread.daemon = True
    thread.start()
