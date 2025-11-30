"""
Drivers tab for Soplos Welcome.
Handles hardware driver detection and installation.
"""

import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

from core.i18n_manager import _
from utils.command_runner import CommandRunner


class DriversTab(Gtk.ScrolledWindow):
    """
    Hardware drivers management tab.
    """
    
    def __init__(self, i18n_manager, theme_manager, parent_window, progress_bar, progress_label):
        super().__init__()
        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        
        self.i18n_manager = i18n_manager
        self.theme_manager = theme_manager
        self.parent_window = parent_window
        self.progress_bar = progress_bar
        self.progress_label = progress_label
        
        # Create CommandRunner
        self.command_runner = CommandRunner(self.progress_bar, self.progress_label, self.parent_window)
        
        # Main container
        self.drivers_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.drivers_box.set_margin_left(20)
        self.drivers_box.set_margin_right(20)
        self.drivers_box.set_margin_top(20)
        self.drivers_box.set_margin_bottom(20)
        
        self.add(self.drivers_box)
        self._create_ui()
    
    def _create_ui(self):
        """Create the drivers tab interface."""
        # Header
        header = Gtk.Label()
        header.set_markup(f'<span size="20000" weight="bold">{_("Hardware Drivers")}</span>')
        header.set_halign(Gtk.Align.START)
        self.drivers_box.pack_start(header, False, False, 0)
        
        subtitle = Gtk.Label()
        subtitle.set_markup(f'<span size="12000">{_("Install and manage graphics drivers and hardware support")}</span>')
        subtitle.set_halign(Gtk.Align.START)
        subtitle.get_style_context().add_class('dim-label')
        self.drivers_box.pack_start(subtitle, False, False, 0)
        
        # Separator
        self.drivers_box.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 10)
        
        # --- Hardware Scan Button (at the top for easy access) ---
        scan_label = Gtk.Label()
        scan_label.set_markup(f'<span weight="bold" size="14000">{_("Detección de Hardware")}</span>')
        scan_label.set_halign(Gtk.Align.START)
        self.drivers_box.pack_start(scan_label, False, False, 5)
        
        scan_btn = self._create_button(
            _("Escanear Hardware"),
            _("Detecta automáticamente el hardware y recomienda drivers")
        )
        scan_btn.connect("clicked", self._on_scan_hardware)
        self.drivers_box.pack_start(scan_btn, False, False, 5)
        
        # Separator
        self.drivers_box.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 10)
        
        # --- NVIDIA Section ---
        self._create_nvidia_section()
        
        # Separator
        self.drivers_box.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 10)
        
        # --- AMD Section ---
        self._create_amd_section()
        
        # Separator
        self.drivers_box.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 10)
        
        # --- Wi-Fi Section ---
        self._create_wifi_section()
        
        # Separator
        self.drivers_box.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 10)
        
        # --- Other Drivers Section ---
        self._create_other_section()
        
        # Separator
        self.drivers_box.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 10)
        
        # --- VM Tools Section ---
        self._create_vm_section()
        
        self.show_all()
    
    def _create_nvidia_section(self):
        """Create NVIDIA drivers section."""
        label = Gtk.Label()
        label.set_markup(f'<span weight="bold" size="14000">{_("NVIDIA Graphics Drivers")}</span>')
        label.set_halign(Gtk.Align.START)
        self.drivers_box.pack_start(label, False, False, 5)
        
        # Grid for NVIDIA buttons
        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        grid.set_column_homogeneous(True)
        self.drivers_box.pack_start(grid, False, False, 5)
        
        # Row 1: Current drivers
        nvidia_latest = self._create_button(
            _("NVIDIA Latest (550)"),
            _("Latest driver from repository (RTX/GTX 16xx and newer)")
        )
        nvidia_latest.connect("clicked", self._on_nvidia_repo_clicked, "nvidia-driver")
        grid.attach(nvidia_latest, 0, 0, 1, 1)
        
        nvidia_470 = self._create_button(
            _("NVIDIA 470 (Legacy)"),
            _("For Kepler GPUs (GTX 600-700 series)")
        )
        nvidia_470.connect("clicked", self._on_nvidia_run_clicked, "470.256.02")
        grid.attach(nvidia_470, 1, 0, 1, 1)
        
        # Row 2: Legacy drivers
        nvidia_390 = self._create_button(
            _("NVIDIA 390 (Legacy)"),
            _("For Fermi GPUs (GTX 400-500 series)")
        )
        nvidia_390.connect("clicked", self._on_nvidia_run_clicked, "390.157")
        grid.attach(nvidia_390, 0, 1, 1, 1)
        
        nvidia_340 = self._create_button(
            _("NVIDIA 340 (Legacy)"),
            _("For very old GPUs (8xxx, 9xxx, 2xx, 3xx series)")
        )
        nvidia_340.connect("clicked", self._on_nvidia_run_clicked, "340.108")
        grid.attach(nvidia_340, 1, 1, 1, 1)
        
        # Row 3: Open source
        nouveau = self._create_button(
            _("Nouveau (Open Source)"),
            _("Free and open source NVIDIA driver")
        )
        nouveau.connect("clicked", self._on_driver_clicked, "xserver-xorg-video-nouveau")
        grid.attach(nouveau, 0, 2, 2, 1)
        
        # Row 4: DaVinci/Blender extras
        davinci_btn = self._create_button(
            _("DaVinci Resolve Extras"),
            _("OpenCL and CUDA libraries for DaVinci Resolve")
        )
        davinci_btn.connect("clicked", self._on_nvidia_extras_clicked, "davinci")
        grid.attach(davinci_btn, 0, 3, 1, 1)
        
        blender_btn = self._create_button(
            _("Blender CUDA Toolkit"),
            _("CUDA toolkit for Blender GPU rendering")
        )
        blender_btn.connect("clicked", self._on_nvidia_extras_clicked, "blender")
        grid.attach(blender_btn, 1, 3, 1, 1)
    
    def _create_amd_section(self):
        """Create AMD drivers section."""
        label = Gtk.Label()
        label.set_markup(f'<span weight="bold" size="14000">{_("AMD Graphics Drivers")}</span>')
        label.set_halign(Gtk.Align.START)
        self.drivers_box.pack_start(label, False, False, 5)
        
        amd_btn = self._create_button(
            _("AMD Radeon (Open Source)"),
            _("Free drivers for all AMD GPUs")
        )
        amd_btn.connect("clicked", self._on_driver_clicked, 
                       "firmware-amd-graphics libgl1-mesa-dri libglx-mesa0 mesa-vulkan-drivers xserver-xorg-video-all")
        self.drivers_box.pack_start(amd_btn, False, False, 5)
    
    def _create_wifi_section(self):
        """Create Wi-Fi drivers section."""
        label = Gtk.Label()
        label.set_markup(f'<span weight="bold" size="14000">{_("Wi-Fi Drivers")}</span>')
        label.set_halign(Gtk.Align.START)
        self.drivers_box.pack_start(label, False, False, 5)
        
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        box.set_homogeneous(True)
        self.drivers_box.pack_start(box, False, False, 5)
        
        intel_wifi = self._create_button(_("Intel Wi-Fi"), _("Intel wireless cards"))
        intel_wifi.connect("clicked", self._on_driver_clicked, "firmware-iwlwifi")
        box.pack_start(intel_wifi, True, True, 0)
        
        realtek_wifi = self._create_button(_("Realtek Wi-Fi"), _("Realtek wireless cards"))
        realtek_wifi.connect("clicked", self._on_driver_clicked, "firmware-realtek")
        box.pack_start(realtek_wifi, True, True, 0)
        
        broadcom_wifi = self._create_button(_("Broadcom Wi-Fi"), _("Broadcom wireless cards"))
        broadcom_wifi.connect("clicked", self._on_driver_clicked, "firmware-b43-installer")
        box.pack_start(broadcom_wifi, True, True, 0)
    
    def _create_other_section(self):
        """Create other drivers section."""
        label = Gtk.Label()
        label.set_markup(f'<span weight="bold" size="14000">{_("Other Drivers")}</span>')
        label.set_halign(Gtk.Align.START)
        self.drivers_box.pack_start(label, False, False, 5)
        
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        box.set_homogeneous(True)
        self.drivers_box.pack_start(box, False, False, 5)
        
        printer_btn = self._create_button(_("Printers"), _("Printer drivers"))
        printer_btn.connect("clicked", self._on_driver_clicked, "printer-driver-all")
        box.pack_start(printer_btn, True, True, 0)
        
        bluetooth_btn = self._create_button(_("Bluetooth"), _("Bluetooth support"))
        bluetooth_btn.connect("clicked", self._on_driver_clicked, "bluetooth bluez bluez-tools blueman")
        box.pack_start(bluetooth_btn, True, True, 0)
    
    def _create_vm_section(self):
        """Create VM tools section."""
        label = Gtk.Label()
        label.set_markup(f'<span weight="bold" size="14000">{_("Virtual Machine Tools")}</span>')
        label.set_halign(Gtk.Align.START)
        self.drivers_box.pack_start(label, False, False, 5)
        
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        box.set_homogeneous(True)
        self.drivers_box.pack_start(box, False, False, 5)
        
        vmware_btn = self._create_button(_("VMware Tools"), _("For VMware virtual machines"))
        vmware_btn.connect("clicked", self._on_driver_clicked, "open-vm-tools-desktop")
        box.pack_start(vmware_btn, True, True, 0)
        
        qemu_btn = self._create_button(_("QEMU/KVM Tools"), _("For QEMU/KVM virtual machines"))
        qemu_btn.connect("clicked", self._on_driver_clicked, 
                        "qemu-guest-agent spice-vdagent spice-webdavd xserver-xspice")
        box.pack_start(qemu_btn, True, True, 0)
        
        vbox_btn = self._create_button(_("VirtualBox Guest"), _("For VirtualBox virtual machines"))
        vbox_btn.connect("clicked", self._on_vbox_clicked)
        box.pack_start(vbox_btn, True, True, 0)
    
    def _create_button(self, label, tooltip):
        """Create a driver button with tooltip."""
        button = Gtk.Button(label=label)
        button.set_tooltip_text(tooltip)
        button.set_size_request(200, 40)
        return button
    
    def _on_driver_clicked(self, button, packages):
        """Install driver from repository."""
        script = f"pkexec apt install -y {packages}"
        self._run_script(script, f"install-{packages.split()[0]}.sh")
    
    def _on_nvidia_repo_clicked(self, button, package):
        """Install NVIDIA driver from repository with proper configuration."""
        script = f"""#!/bin/bash
set -e

echo "Installing NVIDIA driver from repository..."

# Install kernel headers
pkexec apt update
pkexec apt install -y linux-headers-$(uname -r)

# Install NVIDIA driver
pkexec apt install -y {package}

# Configure for Dracut
pkexec mkdir -p /etc/dracut.conf.d
echo 'omit_drivers+=" nouveau "' | pkexec tee /etc/dracut.conf.d/blacklist-nouveau.conf
echo 'add_drivers+=" nvidia nvidia_modeset nvidia_uvm nvidia_drm "' | pkexec tee /etc/dracut.conf.d/nvidia.conf

# Regenerate initramfs
pkexec dracut --force

echo "NVIDIA driver installed. Please reboot to apply changes."
"""
        self._run_script(script, f"install-{package}.sh")
    
    def _on_nvidia_run_clicked(self, button, version):
        """Download and install NVIDIA driver from .run file."""
        script = f"""#!/bin/bash
set -e

echo "Installing NVIDIA {version} driver..."

# Install dependencies
pkexec apt update
pkexec apt install -y build-essential dkms linux-headers-$(uname -r)

# Download driver
cd /tmp
wget -O nvidia.run https://us.download.nvidia.com/XFree86/Linux-x86_64/{version}/NVIDIA-Linux-x86_64-{version}.run

# Make executable
chmod +x nvidia.run

# Install driver
pkexec ./nvidia.run --silent --dkms --no-questions

# Configure Dracut - Blacklist nouveau
echo "Configuring Dracut to blacklist nouveau..."
pkexec mkdir -p /etc/dracut.conf.d
echo 'omit_drivers+=" nouveau "' | pkexec tee /etc/dracut.conf.d/blacklist-nouveau.conf

# Configure Dracut - Include NVIDIA modules
echo "Configuring NVIDIA modules in Dracut..."
echo 'add_drivers+=" nvidia nvidia_modeset nvidia_uvm nvidia_drm "' | pkexec tee /etc/dracut.conf.d/nvidia.conf

# Regenerate initramfs with Dracut
echo "Regenerating initramfs..."
pkexec dracut --force

# Cleanup
rm -f nvidia.run

echo ""
echo "===  Installation completed ==="
echo "NVIDIA {version} driver installed successfully."
echo "IMPORTANT: Restart the system to apply the changes."
echo "After restart, verify with: nvidia-smi"
"""
        self._run_script(script, f"install-nvidia-{version}.sh")
    
    def _on_nvidia_extras_clicked(self, button, mode):
        """Install additional NVIDIA support for DaVinci Resolve or Blender."""
        if mode == "davinci":
            packages = "nvidia-opencl-icd libcuda1 libglu1-mesa libnvidia-encode1"
            script_name = "install-nvidia-davinci-extras.sh"
        elif mode == "blender":
            packages = "nvidia-cuda-toolkit"
            script_name = "install-nvidia-blender-cuda.sh"
        else:
            return
        
        script = f"pkexec apt install -y {packages}"
        self._run_script(script, script_name)
    
    def _on_vbox_clicked(self, button):
        """Install VirtualBox Guest Additions."""
        script = """#!/bin/bash
set -e

echo "Installing VirtualBox Guest Additions..."

# Install dependencies
pkexec apt update
pkexec apt install -y build-essential dkms linux-headers-$(uname -r)

# Create temp directory
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

# Download Guest Additions
wget -O VBoxGuestAdditions.iso "https://download.virtualbox.org/virtualbox/7.0.20/VBoxGuestAdditions_7.0.20.iso"

# Mount ISO
mkdir -p /tmp/vbox-mount
pkexec mount -o loop VBoxGuestAdditions.iso /tmp/vbox-mount

# Run installer
pkexec /tmp/vbox-mount/VBoxLinuxAdditions.run --nox11

# Cleanup
pkexec umount /tmp/vbox-mount || true
rm -rf "$TEMP_DIR"

echo "VirtualBox Guest Additions installed. Please reboot to apply changes."
"""
        self._run_script(script, "install-vbox-guest.sh")
    
    def _run_script(self, script_content, script_name):
        """Create and run installation script."""
        script_path = f"/tmp/{script_name}"
        try:
            with open(script_path, "w") as f:
                f.write(script_content)
            os.chmod(script_path, 0o755)
            self.command_runner.run_command(script_path)
        except Exception as e:
            print(f"Error creating script {script_name}: {e}")
    
    def _on_scan_hardware(self, button):
        """Scan hardware and show results."""
        from utils.hardware_detector import scan_hardware
        
        def update_status(text):
            self.progress_label.set_text(text)
        
        def update_progress(fraction):
            self.progress_bar.set_fraction(fraction)
        
        def show_results(results):
            # Hide progress
            self.progress_bar.set_fraction(0.0)
            
            # Create dialog
            dialog = Gtk.Dialog(
                title=_("Información del Sistema"),
                parent=self.parent_window,
                flags=0
            )
            dialog.set_default_size(700, 600)
            
            # Scrolled window
            scrolled = Gtk.ScrolledWindow()
            scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
            content_box = dialog.get_content_area()
            content_box.pack_start(scrolled, True, True, 0)
            
            # Main container
            main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
            main_box.set_margin_left(20)
            main_box.set_margin_right(20)
            main_box.set_margin_top(20)
            main_box.set_margin_bottom(20)
            scrolled.add(main_box)
            
            # CPU Section
            if results.get('cpu'):
                cpu_frame = Gtk.Frame(label="🖥️ Procesador")
                cpu_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
                cpu_box.set_margin_left(15)
                cpu_box.set_margin_right(15)
                cpu_box.set_margin_top(10)
                cpu_box.set_margin_bottom(10)
                
                cpu = results['cpu']
                cpu_label = Gtk.Label()
                cpu_label.set_markup(f"<b>Modelo:</b> {cpu.get('model', 'N/A')}\n<b>Núcleos:</b> {cpu.get('cores', 0)} | <b>Hilos:</b> {cpu.get('threads', 0)}")
                cpu_label.set_line_wrap(True)
                cpu_label.set_xalign(0)
                cpu_box.pack_start(cpu_label, False, False, 0)
                
                cpu_frame.add(cpu_box)
                main_box.pack_start(cpu_frame, False, False, 5)
            
            # GPU Section
            if results.get('gpu'):
                gpu_frame = Gtk.Frame(label="🎮 Tarjeta Gráfica")
                gpu_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
                gpu_box.set_margin_left(15)
                gpu_box.set_margin_right(15)
                gpu_box.set_margin_top(10)
                gpu_box.set_margin_bottom(10)
                
                gpu = results['gpu']
                gpu_label = Gtk.Label()
                gpu_label.set_markup(f"<b>Fabricante:</b> {gpu.get('vendor', 'N/A')}\n<b>Modelo:</b> {gpu.get('model', 'N/A')}\n<b>Tipo:</b> {gpu.get('type', 'N/A')}")
                gpu_label.set_line_wrap(True)
                gpu_label.set_xalign(0)
                gpu_box.pack_start(gpu_label, False, False, 0)
                
                # Recommended driver
                if gpu.get('recommended_driver'):
                    driver_label = Gtk.Label()
                    driver_label.set_markup(f"<b>Driver recomendado:</b> {gpu['recommended_driver']}")
                    driver_label.set_xalign(0)
                    driver_label.get_style_context().add_class("suggested-action")
                    gpu_box.pack_start(driver_label, False, False, 0)
                    
                    # Install button for recommended driver
                    install_gpu_btn = Gtk.Button(label=f"Instalar {gpu['recommended_driver']}")
                    install_gpu_btn.get_style_context().add_class("suggested-action")
                    install_gpu_btn.connect("clicked", self._on_install_recommended_driver, 
                                           gpu['recommended_driver'], dialog)
                    gpu_box.pack_start(install_gpu_btn, False, False, 5)
                
                gpu_frame.add(gpu_box)
                main_box.pack_start(gpu_frame, False, False, 5)
            
            # Memory Section
            if results.get('memory'):
                mem_frame = Gtk.Frame(label="💾 Memoria RAM")
                mem_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
                mem_box.set_margin_left(15)
                mem_box.set_margin_right(15)
                mem_box.set_margin_top(10)
                mem_box.set_margin_bottom(10)
               
                mem = results['memory']
                mem_label = Gtk.Label()
                mem_label.set_markup(f"<b>Total:</b> {mem.get('total', 'N/A')} | <b>Disponible:</b> {mem.get('available', 'N/A')}")
                mem_label.set_xalign(0)
                mem_box.pack_start(mem_label, False, False, 0)
                
                mem_frame.add(mem_box)
                main_box.pack_start(mem_frame, False, False, 5)
            
            # VM Detection
            if results.get('vm_detection', {}).get('is_vm'):
                vm_frame = Gtk.Frame(label="🖥️ Máquina Virtual")
                vm_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
                vm_box.set_margin_left(15)
                vm_box.set_margin_right(15)
                vm_box.set_margin_top(10)
                vm_box.set_margin_bottom(10)
                
                vm = results['vm_detection']
                vm_label = Gtk.Label()
                vm_label.set_markup(f"<b>Tipo:</b> {vm.get('type', 'N/A')}")
                vm_label.set_xalign(0)
                vm_box.pack_start(vm_label, False, False, 0)
                
                if vm.get('recommended_tools'):
                    tools_label = Gtk.Label()
                    tools_label.set_markup(f"<b>Herramientas recomendadas:</b> {vm['recommended_tools']}")
                    tools_label.set_xalign(0)
                    vm_box.pack_start(tools_label, False, False, 0)
                    
                    # Install button for VM tools
                    install_vm_btn = Gtk.Button(label=f"Instalar {vm['recommended_tools']}")
                    install_vm_btn.get_style_context().add_class("suggested-action")
                    install_vm_btn.connect("clicked", self._on_driver_clicked, vm['recommended_tools'])
                    install_vm_btn.connect("clicked", lambda x: dialog.destroy())
                    vm_box.pack_start(install_vm_btn, False, False, 5)
                
                vm_frame.add(vm_box)
                main_box.pack_start(vm_frame, False, False, 5)
            
            # Storage
            if results.get('storage'):
                storage_frame = Gtk.Frame(label="💿 Almacenamiento")
                storage_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
                storage_box.set_margin_left(15)
                storage_box.set_margin_right(15)
                storage_box.set_margin_top(10)
                storage_box.set_margin_bottom(10)
                
                for device in results['storage']:
                    dev_label = Gtk.Label()
                    dev_label.set_markup(f"• <b>{device.get('name', 'N/A')}:</b> {device.get('size', 'N/A')}")
                    dev_label.set_xalign(0)
                    storage_box.pack_start(dev_label, False, False, 0)
                
                storage_frame.add(storage_box)
                main_box.pack_start(storage_frame, False, False, 5)
            
            # Network
            if results.get('network'):
                net_frame = Gtk.Frame(label="🌐 Red")
                net_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
                net_box.set_margin_left(15)
                net_box.set_margin_right(15)
                net_box.set_margin_top(10)
                net_box.set_margin_bottom(10)
                
                for iface in results['network']:
                    iface_label = Gtk.Label()
                    iface_text = f"• <b>{iface.get('name', 'N/A')}:</b> {iface.get('type', 'N/A')}"
                    if iface.get('status'):
                        iface_text += f" - {iface['status']}"
                    iface_label.set_markup(iface_text)
                    iface_label.set_xalign(0)
                    net_box.pack_start(iface_label, False, False, 0)
                
                net_frame.add(net_box)
                main_box.pack_start(net_frame, False, False, 5)
            
            # Close button
            close_btn = Gtk.Button(label=_("Cerrar"))
            close_btn.connect("clicked", lambda x: dialog.destroy())
            dialog.get_action_area().pack_start(close_btn, False, False, 0)
            
            dialog.show_all()
        
        # Start scan
        scan_hardware(update_status, update_progress, show_results)
    
    def _on_install_recommended_driver(self, button, driver, dialog):
        """Install recommended driver from hardware scan."""
        dialog.destroy()
        
        # Check if it's NVIDIA driver from .run or from repo
        if driver.startswith('nvidia-driver-') and driver != 'nvidia-driver':
            # Legacy driver, install from .run
            version_map = {
                'nvidia-driver-470': '470.256.02',
                'nvidia-driver-390': '390.157',
                'nvidia-driver-340': '340.108'
            }
            if driver in version_map:
                self._on_nvidia_run_clicked(button, version_map[driver])
        elif driver == 'nvidia-driver':
            # Latest from repo
            self._on_nvidia_repo_clicked(button, driver)
        else:
            # AMD, Intel, or other drivers
            self._on_driver_clicked(button, driver)
