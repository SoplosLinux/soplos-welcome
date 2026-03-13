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
    
    def __init__(self, i18n_manager, theme_manager, environment_detector, parent_window, progress_bar, progress_label):
        super().__init__()
        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        
        self.i18n_manager = i18n_manager
        self.theme_manager = theme_manager
        self.environment_detector = environment_detector
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
        scan_label.set_markup(f'<span weight="bold" size="14000">{_("Hardware Detection")}</span>')
        scan_label.set_halign(Gtk.Align.START)
        self.drivers_box.pack_start(scan_label, False, False, 5)
        
        scan_btn = self._create_button(
            _("Scan Hardware"),
            _("Automatically detect hardware and recommend drivers")
        )
        scan_btn.connect("clicked", self._on_scan_hardware)
        self.drivers_box.pack_start(scan_btn, False, False, 5)
        
        # Separator
        self.drivers_box.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 10)
        
        # --- NVIDIA Section ---
        self._create_nvidia_section()
        
        # Separator
        self.drivers_box.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 10)
        
        # --- NVIDIA Hybrid Section ---
        self._create_nvidia_hybrid_section()
        
        # Separator
        self.drivers_box.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 10)
        
        # --- NVIDIA Extras Section ---
        self._create_nvidia_extras_section()
        
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
        
        # Row 0: Latest drivers (590, 580)
        nvidia_590 = self._create_button(
            _("NVIDIA 590 (Latest)"),
            _("Latest driver for RTX 50/40/30 series")
        )
        nvidia_590.connect("clicked", self._on_nvidia_cuda_repo_clicked, "590")
        grid.attach(nvidia_590, 0, 0, 1, 1)
        
        nvidia_580 = self._create_button(
            _("NVIDIA 580 (Production)"),
            _("Stable production driver for modern GPUs")
        )
        nvidia_580.connect("clicked", self._on_nvidia_cuda_repo_clicked, "580")
        grid.attach(nvidia_580, 1, 0, 1, 1)
        
        # Row 1: Repository driver + Legacy 470
        nvidia_550 = self._create_button(
            _("NVIDIA 550 (Repo)"),
            _("For RTX 30/20, GTX 16xx/10xx series")
        )
        nvidia_550.connect("clicked", self._on_nvidia_repo_clicked, "nvidia-driver")
        grid.attach(nvidia_550, 0, 1, 1, 1)
        
        nvidia_470 = self._create_button(
            _("NVIDIA 470 (Legacy)"),
            _("For Kepler/Maxwell GPUs (GTX 600-900 series)")
        )
        nvidia_470.connect("clicked", self._on_legacy_nvidia_clicked, "nvidia-tesla-470-driver")
        grid.attach(nvidia_470, 1, 1, 1, 1)
        
        # Row 2: Older legacy drivers (390, 340)
        nvidia_390 = self._create_button(
            _("NVIDIA 390 (Legacy)"),
            _("For Fermi GPUs (GTX 400-500 series)")
        )
        nvidia_390.connect("clicked", self._on_legacy_nvidia_clicked, "nvidia-legacy-390xx-driver")
        grid.attach(nvidia_390, 0, 2, 1, 1)
        
        nvidia_340 = self._create_button(
            _("NVIDIA 340 (Legacy)"),
            _("For very old GPUs (8xxx, 9xxx, 2xx, 3xx series)")
        )
        nvidia_340.connect("clicked", self._on_legacy_nvidia_clicked, "nvidia-legacy-340xx-driver")
        grid.attach(nvidia_340, 1, 2, 1, 1)
        
        # Row 3: Open source driver
        nouveau = self._create_button(
            _("Nouveau (Open Source)"),
            _("Free and open source NVIDIA driver")
        )
        nouveau.connect("clicked", self._on_driver_clicked, "xserver-xorg-video-nouveau")
        grid.attach(nouveau, 0, 3, 1, 1)
    
    def _create_nvidia_hybrid_section(self):
        """Create NVIDIA hybrid graphics section for laptops."""
        label = Gtk.Label()
        label.set_markup(f'<span weight="bold" size="14000">{_("Hybrid Graphics (Laptops)")}</span>')
        label.set_halign(Gtk.Align.START)
        self.drivers_box.pack_start(label, False, False, 5)
        
        desc_label = Gtk.Label()
        desc_label.set_markup(f'<span size="10000">{_("For laptops with Intel/AMD + NVIDIA graphics")}</span>')
        desc_label.set_halign(Gtk.Align.START)
        desc_label.get_style_context().add_class('dim-label')
        self.drivers_box.pack_start(desc_label, False, False, 0)
        
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        box.set_homogeneous(True)
        self.drivers_box.pack_start(box, False, False, 5)
        
        # PRIME Render Offload (battery saving)
        prime_offload_btn = self._create_button(
            _("PRIME Render Offload"),
            _("Use NVIDIA on demand (recommended, saves battery)")
        )
        prime_offload_btn.connect("clicked", self._on_hybrid_clicked, "offload")
        box.pack_start(prime_offload_btn, True, True, 0)
        
        # NVIDIA as primary (performance)
        nvidia_primary_btn = self._create_button(
            _("NVIDIA Primary"),
            _("Always use NVIDIA GPU (maximum performance)")
        )
        nvidia_primary_btn.connect("clicked", self._on_hybrid_clicked, "nvidia")
        box.pack_start(nvidia_primary_btn, True, True, 0)
        
        # Detect hybrid
        detect_hybrid_btn = self._create_button(
            _("Detect Hybrid Setup"),
            _("Check if you have a hybrid graphics laptop")
        )
        detect_hybrid_btn.connect("clicked", self._on_detect_hybrid_clicked)
        box.pack_start(detect_hybrid_btn, True, True, 0)
    
    def _create_nvidia_extras_section(self):
        """Create NVIDIA extras section (CUDA, OpenCL tools)."""
        label = Gtk.Label()
        label.set_markup(f'<span weight="bold" size="14000">{_("NVIDIA Extras")}</span>')
        label.set_halign(Gtk.Align.START)
        self.drivers_box.pack_start(label, False, False, 5)
        
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        box.set_homogeneous(True)
        self.drivers_box.pack_start(box, False, False, 5)
        
        davinci_btn = self._create_button(
            _("DaVinci Resolve Extras"),
            _("OpenCL and CUDA libraries for DaVinci Resolve")
        )
        davinci_btn.connect("clicked", self._on_nvidia_extras_clicked, "davinci")
        box.pack_start(davinci_btn, True, True, 0)
        
        blender_btn = self._create_button(
            _("Blender CUDA Toolkit"),
            _("CUDA toolkit for Blender GPU rendering")
        )
        blender_btn.connect("clicked", self._on_nvidia_extras_clicked, "blender")
        box.pack_start(blender_btn, True, True, 0)
    
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
        script = f"""#!/bin/bash
set -e
apt update
apt install -y {packages}
echo "Installation completed successfully."
"""
        self._run_script_as_root(script, f"install-{packages.split()[0]}.sh")
    
    def _on_legacy_nvidia_clicked(self, button, package_name):
        """Show warning about Debian Sid requirement before installing legacy drivers."""
        dialog = Gtk.MessageDialog(
            transient_for=self.parent_window,
            flags=0,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.YES_NO,
            text=_("Legacy Driver Support Required")
        )
        
        dialog.format_secondary_text(
            _("This legacy driver is only available in the unstable repositories.\n\n"
              "We will now open <b>Soplos Repo Selector</b> so you can temporarily enable "
              "the <b>Debian Sid (Unstable)</b> repository.\n\n"
              "After completing the driver installation, it is CRITICAL that you return "
              "to Soplos Repo Selector and disable Sid, or you may break your system "
              "during future updates.\n\n"
              "Do you want to enable Sid and continue with the installation?")
        )
        
        # Enable markup for the secondary text to support <b> tags
        dialog.get_message_area().get_children()[1].set_use_markup(True)

        response = dialog.run()
        dialog.destroy()

        if response == Gtk.ResponseType.YES:
            # Launch Soplos Repo Selector asynchronously
            try:
                import subprocess
                subprocess.Popen(['soplos-repo-selector'])
            except Exception as e:
                print(f"Failed to launch soplos-repo-selector: {e}")
                
            # Show a second dialog waiting for the user to finish with Repo Selector
            wait_dialog = Gtk.MessageDialog(
                transient_for=self.parent_window,
                flags=0,
                message_type=Gtk.MessageType.QUESTION,
                buttons=Gtk.ButtonsType.OK_CANCEL,
                text=_("Waiting for Soplos Repo Selector")
            )
            
            wait_dialog.format_secondary_text(
                _("Soplos Repo Selector has been opened.\n\n"
                  "1. Enable the <b>Debian Sid (Unstable)</b> repository.\n"
                  "2. Wait for the operation to finish and close Soplos Repo Selector.\n"
                  "3. Click <b>OK</b> below to begin the driver installation.\n\n"
                  "If you changed your mind, click Cancel.")
            )
            wait_dialog.get_message_area().get_children()[1].set_use_markup(True)
            
            wait_response = wait_dialog.run()
            wait_dialog.destroy()
            
            if wait_response == Gtk.ResponseType.OK:
                self._on_nvidia_repo_clicked(button, package_name)

    def _on_nvidia_repo_clicked(self, button, package):
        """Install NVIDIA driver from repository with proper configuration."""
        # Show confirmation dialog before proceeding
        confirm_dialog = Gtk.MessageDialog(
            transient_for=self.parent_window,
            flags=0,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.YES_NO,
            text=_("Confirm NVIDIA Driver Installation")
        )
        confirm_dialog.format_secondary_text(
            _("This will:\n\n"
              "1. Remove any existing NVIDIA drivers to prevent conflicts.\n"
              "2. Install the driver: {package}\n"
              "3. Install auxiliary tools (nvidia-smi, nvidia-settings).\n"
              "4. Regenerate initramfs.\n\n"
              "A system restart will be required after installation.\n\n"
              "Do you want to continue?").format(package=package)
        )
        response = confirm_dialog.run()
        confirm_dialog.destroy()
        if response != Gtk.ResponseType.YES:
            return

        script = f"""#!/bin/bash
        
set -e

echo "Installing NVIDIA driver from repository..."

# === CLEANUP EXISTING NVIDIA PACKAGES ===
echo "Removing existing NVIDIA packages to prevent conflicts..."
apt purge -y 'nvidia-driver*' 'nvidia-kernel*' 'libnvidia*' 'nvidia-modprobe' \
    'nvidia-settings' 'nvidia-smi' 'nvidia-opencl*' 'nvidia-cuda*' \
    'cuda-drivers*' 'xserver-xorg-video-nvidia*' 2>/dev/null || true
apt autoremove -y 2>/dev/null || true

# Install kernel headers
apt update
apt install -y linux-headers-$(uname -r)

# Install NVIDIA driver + auxiliary packages
apt install -y {package} nvidia-smi nvidia-settings nvidia-modprobe libglu1-mesa

# === BLACKLIST NOUVEAU IN MODPROBE ===
echo "Blacklisting nouveau in modprobe..."
mkdir -p /etc/modprobe.d
echo "blacklist nouveau" > /etc/modprobe.d/blacklist-nouveau.conf
echo "options nouveau modeset=0" >> /etc/modprobe.d/blacklist-nouveau.conf

# === CONFIGURE GRUB ===
echo "Configuring GRUB with nvidia-drm.modeset=1..."
if ! grep -q "nvidia-drm.modeset=1" /etc/default/grub; then
    sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT="\\([^"]*\\)"/GRUB_CMDLINE_LINUX_DEFAULT="\\1 nvidia-drm.modeset=1"/' /etc/default/grub
    update-grub
fi

# === CONFIGURE DRACUT/INITRAMFS ===
if command -v dracut >/dev/null 2>&1; then
    echo "Configuring Dracut..."
    mkdir -p /etc/dracut.conf.d
    echo 'omit_drivers+=" nouveau "' > /etc/dracut.conf.d/blacklist-nouveau.conf
    echo 'add_drivers+=" nvidia nvidia_modeset nvidia_uvm nvidia_drm "' > /etc/dracut.conf.d/nvidia.conf
    echo "Regenerating initramfs..."
    dracut --force
elif command -v update-initramfs >/dev/null 2>&1; then
    echo "Regenerating initramfs..."
    update-initramfs -u
fi

echo ""
echo "=== Installation completed ==="
echo "NVIDIA driver installed successfully."
echo "Auxiliary tools installed: nvidia-smi, nvidia-settings, nvidia-modprobe"
echo "IMPORTANT: Restart the system to apply the changes."
"""
        self._run_script_as_root(script, f"install-{package}.sh")

    
    def _on_nvidia_cuda_repo_clicked(self, button, version):
        """Install NVIDIA driver from official CUDA repository for Debian."""
        # Show confirmation dialog before proceeding
        confirm_dialog = Gtk.MessageDialog(
            transient_for=self.parent_window,
            flags=0,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.YES_NO,
            text=_("Confirm NVIDIA CUDA Driver Installation")
        )
        confirm_dialog.format_secondary_text(
            _("This will:\n\n"
              "1. Remove any existing NVIDIA drivers to prevent conflicts.\n"
              "2. Add the official NVIDIA CUDA repository.\n"
              "3. Install driver version {version} with auxiliary tools.\n"
              "4. Regenerate initramfs.\n\n"
              "A system restart will be required after installation.\n\n"
              "Do you want to continue?").format(version=version)
        )
        response = confirm_dialog.run()
        confirm_dialog.destroy()
        if response != Gtk.ResponseType.YES:
            return

        script = f"""#!/bin/bash
set -e

NVIDIA_VERSION="{version}"
# Dynamic repository selection (590+ uses debian13, 580 uses debian12)
if [ "$NVIDIA_VERSION" -ge 590 ]; then
    DISTRO="debian13"
else
    DISTRO="debian12"
fi

echo "=== NVIDIA $NVIDIA_VERSION Official CUDA Repository ($DISTRO) ==="
echo ""

echo "[1/6] Enabling contrib and non-free repos..."
# Enable contrib, non-free and non-free-firmware components
if command -v apt-get >/dev/null; then
    # Direct way for Debian systems
    sed -i 's/main$/main contrib non-free non-free-firmware/g' /etc/apt/sources.list || true
    # Also check .sources files (standard in Debian 12/13)
    find /etc/apt/sources.list.d/ -name "*.sources" -exec sed -i 's/Components: main/Components: main contrib non-free non-free-firmware/g' {{}} + || true
fi

# Initial update to ensure baseline is fresh
apt update || echo "Warning: apt update had some warnings, continuing..."

# Install kernel headers
apt install -y linux-headers-$(uname -r)

echo "[2/6] Cleaning up existing NVIDIA packages..."
# Remove existing NVIDIA packages to prevent conflicts
apt purge -y 'nvidia-driver*' 'nvidia-kernel*' 'libnvidia*' 'nvidia-modprobe' \
    'nvidia-settings' 'nvidia-smi' 'nvidia-opencl*' 'nvidia-cuda*' \
    'cuda-drivers*' 'xserver-xorg-video-nvidia*' 2>/dev/null || true
apt autoremove -y 2>/dev/null || true

echo "[3/6] Setting up NVIDIA Official Keyring Package..."
# The official way is to install the cuda-keyring.deb which configures the repo and keys automatically
TEMP_KEYRING_DEB=$(mktemp)
wget -q -O "$TEMP_KEYRING_DEB" https://developer.download.nvidia.com/compute/cuda/repos/$DISTRO/x86_64/cuda-keyring_1.1-1_all.deb

if [ -f "$TEMP_KEYRING_DEB" ] && [ -s "$TEMP_KEYRING_DEB" ]; then
    dpkg -i "$TEMP_KEYRING_DEB"
    rm -f "$TEMP_KEYRING_DEB"
else
    echo "ERROR: Failed to download NVIDIA keyring package."
    exit 1
fi

echo "[4/6] Updating package cache for NVIDIA Repository..."
# After installing the keyring deb, we update to see the new repository
apt update || echo "Apt update after keyring installation had some warnings..."

echo "[5/6] Installing NVIDIA Driver $NVIDIA_VERSION..."
# Validate that the requested driver version is available before installing
if apt-cache policy cuda-drivers-$NVIDIA_VERSION 2>/dev/null | grep -q 'Candidate:'; then
    CANDIDATE=$(apt-cache policy cuda-drivers-$NVIDIA_VERSION | grep 'Candidate:' | awk '{{print $2}}')
    if [ "$CANDIDATE" = "(none)" ]; then
        echo "ERROR: cuda-drivers-$NVIDIA_VERSION is not available in the configured repositories."
        echo "Available cuda-drivers packages:"
        apt-cache search 'cuda-drivers' 2>/dev/null || true
        echo ""
        echo "Please check that the repository for $DISTRO contains driver version $NVIDIA_VERSION."
        exit 1
    fi
    echo "Found cuda-drivers-$NVIDIA_VERSION (candidate: $CANDIDATE). Installing..."
    apt install -y cuda-drivers-$NVIDIA_VERSION
elif apt-cache policy nvidia-driver-$NVIDIA_VERSION 2>/dev/null | grep -q 'Candidate:'; then
    CANDIDATE=$(apt-cache policy nvidia-driver-$NVIDIA_VERSION | grep 'Candidate:' | awk '{{print $2}}')
    if [ "$CANDIDATE" = "(none)" ]; then
        echo "ERROR: nvidia-driver-$NVIDIA_VERSION is not available either."
        echo "Available nvidia-driver packages:"
        apt-cache search 'nvidia-driver' 2>/dev/null || true
        exit 1
    fi
    echo "Found nvidia-driver-$NVIDIA_VERSION (candidate: $CANDIDATE). Installing..."
    apt install -y nvidia-driver-$NVIDIA_VERSION
else
    echo "ERROR: No driver package found for version $NVIDIA_VERSION."
    echo ""
    echo "Available CUDA driver packages:"
    apt-cache search 'cuda-drivers' 2>/dev/null || echo "  (none found)"
    echo ""
    echo "Available NVIDIA driver packages:"
    apt-cache search 'nvidia-driver' 2>/dev/null || echo "  (none found)"
    exit 1
fi

# Install auxiliary packages
apt install -y nvidia-smi nvidia-settings nvidia-modprobe libglu1-mesa 2>/dev/null || \
    echo "Warning: Some auxiliary packages could not be installed (nvidia-smi, nvidia-settings)."

echo "[6/6] Configuring OS parameters..."
# === BLACKLIST NOUVEAU ===
echo "Blacklisting nouveau in modprobe..."
mkdir -p /etc/modprobe.d
cat > /etc/modprobe.d/blacklist-nouveau.conf << 'MODPROBE'
blacklist nouveau
options nouveau modeset=0
MODPROBE

# === CONFIGURE GRUB ===
echo "Configuring GRUB with nvidia-drm.modeset=1..."
if ! grep -q "nvidia-drm.modeset=1" /etc/default/grub; then
    sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT="\\([^"]*\\)"/GRUB_CMDLINE_LINUX_DEFAULT="\\1 nvidia-drm.modeset=1"/' /etc/default/grub
    DEBIAN_FRONTEND=noninteractive update-grub
fi

# === CONFIGURE DRACUT/INITRAMFS ===
if command -v dracut >/dev/null 2>&1; then
    echo "Configuring Dracut..."
    mkdir -p /etc/dracut.conf.d
    echo 'omit_drivers+=" nouveau "' > /etc/dracut.conf.d/blacklist-nouveau.conf
    echo 'add_drivers+=" nvidia nvidia_modeset nvidia_uvm nvidia_drm "' > /etc/dracut.conf.d/nvidia.conf
    echo "Regenerating initramfs..."
    dracut --force
elif command -v update-initramfs >/dev/null 2>&1; then
    echo "Regenerating initramfs..."
    update-initramfs -u
fi

echo ""
echo "=== Installation completed successfully ==="
echo "NVIDIA official driver $NVIDIA_VERSION has been installed."
echo "Auxiliary tools installed: nvidia-smi, nvidia-settings, nvidia-modprobe"
echo "IMPORTANT: Restart the system to apply the changes."
"""
        self._run_script_as_root(script, f"install-nvidia-cuda-{version}.sh")

    
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
        
        script = f"""#!/bin/bash
set -e
apt update
apt install -y {packages}
echo "Installation completed successfully."
"""
        self._run_script_as_root(script, script_name)
    
    def _on_vbox_clicked(self, button):
        """Install VirtualBox Guest Additions."""
        script = """#!/bin/bash
set -e

echo "Installing VirtualBox Guest Additions..."

# Install dependencies
apt update
apt install -y build-essential dkms linux-headers-$(uname -r)

# Create temp directory
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

# Download Guest Additions
wget -O VBoxGuestAdditions.iso "https://download.virtualbox.org/virtualbox/7.0.20/VBoxGuestAdditions_7.0.20.iso"

# Mount ISO
mkdir -p /tmp/vbox-mount
mount -o loop VBoxGuestAdditions.iso /tmp/vbox-mount

# Run installer
/tmp/vbox-mount/VBoxLinuxAdditions.run --nox11 || true

# Cleanup
umount /tmp/vbox-mount || true
rm -rf "$TEMP_DIR"

echo ""
echo "=== Installation completed ==="
echo "VirtualBox Guest Additions installed."
echo "IMPORTANT: Restart the system to apply the changes."
"""
        self._run_script_as_root(script, "install-vbox-guest.sh")
    
    def _run_script(self, script_content, script_name):
        """Create and run installation script (no root)."""
        script_path = f"/tmp/{script_name}"
        try:
            with open(script_path, "w") as f:
                f.write(script_content)
            os.chmod(script_path, 0o755)
            self.command_runner.run_command(script_path)
        except Exception as e:
            print(f"Error creating script {script_name}: {e}")
    
    def _run_script_as_root(self, script_content, script_name):
        """Create and run installation script with root privileges (single pkexec)."""
        script_path = f"/tmp/{script_name}"
        try:
            with open(script_path, "w") as f:
                f.write(script_content)
            os.chmod(script_path, 0o755)
            # Single pkexec authentication for entire script
            self.command_runner.run_command(f"pkexec bash {script_path}")
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
                title=_("System Information"),
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
                cpu_frame = Gtk.Frame(label=f"🖥️ {_('Processor')}")
                cpu_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
                cpu_box.set_margin_left(15)
                cpu_box.set_margin_right(15)
                cpu_box.set_margin_top(10)
                cpu_box.set_margin_bottom(10)
                
                cpu = results['cpu']
                cpu_label = Gtk.Label()
                cpu_label.set_markup(f"<b>{_('Model:')}</b> {cpu.get('model', 'N/A')}\n<b>{_('Cores:')}</b> {cpu.get('cores', 0)} | <b>{_('Threads:')}</b> {cpu.get('threads', 0)}")
                cpu_label.set_line_wrap(True)
                cpu_label.set_xalign(0)
                cpu_box.pack_start(cpu_label, False, False, 0)
                
                cpu_frame.add(cpu_box)
                main_box.pack_start(cpu_frame, False, False, 5)
            
            # GPU Section
            if results.get('gpu'):
                gpu_frame = Gtk.Frame(label=f"🎮 {_('Graphics Card')}")
                gpu_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
                gpu_box.set_margin_left(15)
                gpu_box.set_margin_right(15)
                gpu_box.set_margin_top(10)
                gpu_box.set_margin_bottom(10)
                
                gpu = results['gpu']
                gpu_label = Gtk.Label()
                gpu_label.set_markup(f"<b>{_('Vendor:')}</b> {gpu.get('vendor', 'N/A')}\n<b>{_('Model:')}</b> {gpu.get('model', 'N/A')}\n<b>{_('Type:')}</b> {gpu.get('type', 'N/A')}")
                gpu_label.set_line_wrap(True)
                gpu_label.set_xalign(0)
                gpu_box.pack_start(gpu_label, False, False, 0)
                
                # Recommended driver
                if gpu.get('recommended_driver'):
                    driver_label = Gtk.Label()
                    driver_label.set_markup(f"<b>{_('Recommended driver:')}</b> {gpu['recommended_driver']}")
                    driver_label.set_xalign(0)
                    driver_label.get_style_context().add_class("suggested-action")
                    gpu_box.pack_start(driver_label, False, False, 0)
                    
                    # Install button for recommended driver
                    install_gpu_btn = Gtk.Button(label=f"{_('Install')} {gpu['recommended_driver']}")
                    install_gpu_btn.get_style_context().add_class("suggested-action")
                    install_gpu_btn.connect("clicked", self._on_install_recommended_driver, 
                                           gpu['recommended_driver'], dialog)
                    gpu_box.pack_start(install_gpu_btn, False, False, 5)
                
                gpu_frame.add(gpu_box)
                main_box.pack_start(gpu_frame, False, False, 5)
            
            # Hybrid GPU Section
            if results.get('hybrid_gpu', {}).get('is_hybrid'):
                hybrid_frame = Gtk.Frame(label=f"🔀 {_('Hybrid Graphics Detected')}")
                hybrid_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
                hybrid_box.set_margin_left(15)
                hybrid_box.set_margin_right(15)
                hybrid_box.set_margin_top(10)
                hybrid_box.set_margin_bottom(10)
                
                hybrid = results['hybrid_gpu']
                hybrid_label = Gtk.Label()
                hybrid_label.set_markup(
                    f"<b>{_('Integrated:')}</b> {hybrid.get('integrated', 'N/A')}\n"
                    f"<b>{_('Dedicated:')}</b> {hybrid.get('dedicated', 'N/A')}"
                )
                hybrid_label.set_xalign(0)
                hybrid_box.pack_start(hybrid_label, False, False, 0)
                
                hybrid_info = Gtk.Label()
                hybrid_info.set_markup(f"<i>{_('Configure how your GPUs work together:')}</i>")
                hybrid_info.set_xalign(0)
                hybrid_box.pack_start(hybrid_info, False, False, 5)
                
                # Buttons box
                hybrid_btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
                
                # PRIME Offload button
                offload_btn = Gtk.Button(label=_("PRIME Render Offload"))
                offload_btn.set_tooltip_text(_("Use NVIDIA on demand (saves battery)"))
                offload_btn.connect("clicked", self._on_hybrid_clicked, "offload")
                offload_btn.connect("clicked", lambda x: dialog.destroy())
                hybrid_btn_box.pack_start(offload_btn, True, True, 0)
                
                # NVIDIA Primary button
                nvidia_btn = Gtk.Button(label=_("NVIDIA Primary"))
                nvidia_btn.set_tooltip_text(_("Always use NVIDIA (max performance)"))
                nvidia_btn.connect("clicked", self._on_hybrid_clicked, "nvidia")
                nvidia_btn.connect("clicked", lambda x: dialog.destroy())
                hybrid_btn_box.pack_start(nvidia_btn, True, True, 0)
                
                hybrid_box.pack_start(hybrid_btn_box, False, False, 5)
                hybrid_frame.add(hybrid_box)
                main_box.pack_start(hybrid_frame, False, False, 5)
            
            # Memory Section
            if results.get('memory'):
                mem_frame = Gtk.Frame(label=f"💾 {_('RAM Memory')}")
                mem_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
                mem_box.set_margin_left(15)
                mem_box.set_margin_right(15)
                mem_box.set_margin_top(10)
                mem_box.set_margin_bottom(10)
               
                mem = results['memory']
                mem_label = Gtk.Label()
                mem_label.set_markup(f"<b>{_('Total:')}</b> {mem.get('total', '0 GB')} | <b>{_('Available:')}</b> {mem.get('available', '0 GB')}")
                mem_label.set_xalign(0)
                mem_box.pack_start(mem_label, False, False, 0)
                
                mem_frame.add(mem_box)
                main_box.pack_start(mem_frame, False, False, 5)
            
            # VM Detection
            if results.get('vm_detection', {}).get('is_vm'):
                vm_frame = Gtk.Frame(label="🖥️ " + _("Virtual Machine"))
                vm_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
                vm_box.set_margin_left(15)
                vm_box.set_margin_right(15)
                vm_box.set_margin_top(10)
                vm_box.set_margin_bottom(10)
                
                vm = results['vm_detection']
                vm_label = Gtk.Label()
                vm_label.set_markup(f"<b>{_('Type:')}</b> {vm.get('type', _('N/A'))}")
                vm_label.set_xalign(0)
                vm_box.pack_start(vm_label, False, False, 0)
                
                if vm.get('recommended_tools'):
                    tools_label = Gtk.Label()
                    tools_label.set_markup(f"<b>{_('Recommended tools:')}</b> {vm['recommended_tools']}")
                    tools_label.set_xalign(0)
                    vm_box.pack_start(tools_label, False, False, 0)
                    
                    # Install button for VM tools
                    install_vm_btn = Gtk.Button(label=f"{_('Install')} {vm['recommended_tools']}")
                    install_vm_btn.get_style_context().add_class("suggested-action")
                    install_vm_btn.connect("clicked", self._on_driver_clicked, vm['recommended_tools'])
                    install_vm_btn.connect("clicked", lambda x: dialog.destroy())
                    vm_box.pack_start(install_vm_btn, False, False, 5)
                
                vm_frame.add(vm_box)
                main_box.pack_start(vm_frame, False, False, 5)
            
            # Storage
            if results.get('storage'):
                storage_frame = Gtk.Frame(label=f"💿 {_('Storage')}")
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
                net_frame = Gtk.Frame(label=f"🌐 {_('Network')}")
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
            close_btn = Gtk.Button(label=_("Close"))
            close_btn.connect("clicked", lambda x: dialog.destroy())
            dialog.get_action_area().pack_start(close_btn, False, False, 0)
            
            dialog.show_all()
        
        # Start scan
        scan_hardware(update_status, update_progress, show_results)
    
    def _on_install_recommended_driver(self, button, driver, dialog):
        """Install recommended driver from hardware scan."""
        dialog.destroy()
        
        # Route to appropriate installation method based on driver format
        if driver.startswith('nvidia-driver-580') or driver.startswith('nvidia-driver-590'):
            # CUDA Repo driver
            version = driver.split('-')[-1]
            self._on_nvidia_cuda_repo_clicked(button, version)
        elif driver.startswith('nvidia-legacy-') or driver.startswith('nvidia-tesla-'):
            # Legacy drivers from Sid
            self._on_legacy_nvidia_clicked(button, driver)
        elif driver.startswith('nvidia-driver'):
            # Standard Repo driver (550, etc)
            self._on_nvidia_repo_clicked(button, driver)
        else:
            # AMD, Intel, or other open source drivers
            self._on_driver_clicked(button, driver)
    
    def _on_detect_hybrid_clicked(self, button):
        """Detect if the system has hybrid graphics."""
        from utils.hardware_detector import detect_hybrid_gpu
        
        result = detect_hybrid_gpu()
        
        dialog = Gtk.MessageDialog(
            transient_for=self.parent_window,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=_("Hybrid Graphics Detection")
        )
        
        if result['is_hybrid']:
            dialog.format_secondary_text(
                _("Hybrid graphics detected!\n\n"
                  "Integrated GPU: {integrated}\n"
                  "Dedicated GPU: {dedicated}\n\n"
                  "You can configure PRIME Render Offload (saves battery) "
                  "or NVIDIA Primary (maximum performance).").format(
                    integrated=result.get('integrated', 'Unknown'),
                    dedicated=result.get('dedicated', 'Unknown')
                )
            )
        else:
            dialog.format_secondary_text(
                _("No hybrid graphics detected.\n\n"
                  "Your system has: {gpu}\n\n"
                  "Hybrid configuration is not needed.").format(
                    gpu=result.get('primary', 'Unknown GPU')
                )
            )
        
        dialog.run()
        dialog.destroy()
    
    def _on_hybrid_clicked(self, button, mode):
        """Configure hybrid graphics."""
        if mode == "offload":
            # PRIME Render Offload - Use NVIDIA on demand (works on Xorg and Wayland)
            script = """#!/bin/bash
set -e

echo "Configuring PRIME Render Offload..."

# Check if NVIDIA driver is installed
if ! command -v nvidia-smi &>/dev/null; then
    echo "ERROR: NVIDIA driver is not installed."
    echo "Please install the NVIDIA driver first."
    exit 1
fi

# Remove any existing NVIDIA primary configuration
echo "Removing NVIDIA primary configuration..."
rm -f /etc/X11/xorg.conf.d/10-nvidia-prime.conf
rm -f /etc/X11/xorg.conf
rm -f /etc/environment.d/10-nvidia-primary.conf
rm -f /etc/udev/rules.d/61-nvidia-prime.rules
rm -f /etc/udev/rules.d/61-gdm-nvidia.rules

# Restore default SDDM config if exists
if [ -f /etc/sddm.conf.d/10-wayland.conf ]; then
    rm -f /etc/sddm.conf.d/10-wayland.conf
fi

# Create script for running apps with NVIDIA (works on Xorg AND Wayland)
cat > /usr/local/bin/prime-run << 'PRIMERUN'
#!/bin/bash
# PRIME Render Offload - Run application with NVIDIA GPU
# Works on both Xorg and Wayland

export __NV_PRIME_RENDER_OFFLOAD=1
export __NV_PRIME_RENDER_OFFLOAD_PROVIDER=NVIDIA-G0
export __GLX_VENDOR_LIBRARY_NAME=nvidia
export __VK_LAYER_NV_optimus=NVIDIA_only

# For Wayland/EGL
export __EGL_VENDOR_LIBRARY_FILENAMES=/usr/share/glvnd/egl_vendor.d/10_nvidia.json
export GBM_BACKEND=nvidia-drm

exec "$@"
PRIMERUN
chmod +x /usr/local/bin/prime-run

# Create desktop entry for running apps with NVIDIA
mkdir -p /usr/share/applications
cat > /usr/share/applications/prime-run.desktop << 'DESKTOP'
[Desktop Entry]
Name=Run with NVIDIA GPU
Comment=Run application using the NVIDIA GPU
Exec=prime-run %f
Icon=nvidia
Terminal=false
Type=Application
NoDisplay=true
DESKTOP

echo ""
echo "=== Configuration complete ==="
echo "PRIME Render Offload configured."
echo ""
echo "Works on both Xorg and Wayland."
echo ""
echo "To run an application with NVIDIA GPU, use:"
echo "  prime-run <application>"
echo ""
echo "Examples:"
echo "  prime-run glxgears"
echo "  prime-run steam"
echo "  prime-run blender"
echo ""
echo "No reboot required. You can use prime-run immediately."
"""
            self._run_script_as_root(script, "configure-prime-offload.sh")
        
        elif mode == "nvidia":
            # Get current desktop environment and display protocol
            de = self.environment_detector.desktop_environment.value
            protocol = self.environment_detector.display_protocol.value
            
            # NVIDIA as primary GPU - Adapts to detected environment
            script = f"""#!/bin/bash
set -e

# Detected environment: {de} on {protocol}
DESKTOP_ENV="{de}"

echo "Configuring NVIDIA as primary GPU..."
echo "Detected desktop: $DESKTOP_ENV"

# Check if NVIDIA driver is installed
if ! command -v nvidia-smi &>/dev/null; then
    echo "ERROR: NVIDIA driver is not installed."
    echo "Please install the NVIDIA driver first."
    exit 1
fi

# Check driver version for Wayland GBM support (495+)
DRIVER_VERSION=$(nvidia-smi --query-gpu=driver_version --format=csv,noheader 2>/dev/null | head -1 | cut -d. -f1)
echo "Detected NVIDIA driver version: $DRIVER_VERSION"

# Ensure nvidia-drm.modeset=1 is set (required for Wayland and proper X11)
if ! grep -q "nvidia-drm.modeset=1" /etc/default/grub; then
    echo "Adding nvidia-drm.modeset=1 to GRUB..."
    sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT="\\([^"]*\\)"/GRUB_CMDLINE_LINUX_DEFAULT="\\1 nvidia-drm.modeset=1"/' /etc/default/grub
    update-grub
fi

# Create environment file for NVIDIA as primary (works for all DEs)
echo "Setting up environment variables..."
mkdir -p /etc/environment.d
cat > /etc/environment.d/10-nvidia-primary.conf << 'ENVCONF'
# NVIDIA as primary GPU - Works on X11 and Wayland
__EGL_VENDOR_LIBRARY_FILENAMES=/usr/share/glvnd/egl_vendor.d/10_nvidia.json
GBM_BACKEND=nvidia-drm
__GLX_VENDOR_LIBRARY_NAME=nvidia
ENVCONF

# Configure based on detected desktop environment
case "$DESKTOP_ENV" in
    "gnome")
        echo "Configuring for GNOME (GDM3)..."
        if [ -f /etc/gdm3/custom.conf ]; then
            # Enable Wayland with NVIDIA (driver 495+ required)
            sed -i '/WaylandEnable=false/d' /etc/gdm3/custom.conf
            # Udev rule for Wayland with NVIDIA
            mkdir -p /etc/udev/rules.d
            echo 'ENV{{DRIVER}}=="nvidia", RUN+="/usr/bin/gdm-runtime-config set daemon WaylandEnable true"' > /etc/udev/rules.d/61-gdm-nvidia.rules
        fi
        ;;
    "kde")
        echo "Configuring for KDE Plasma (SDDM)..."
        # SDDM supports both X11 and Wayland sessions
        # User can choose at login screen, no forced config needed
        # But we ensure Wayland is available
        if [ -d /etc/sddm.conf.d ]; then
            mkdir -p /etc/sddm.conf.d
            # Don't force Wayland, let user choose at login
            cat > /etc/sddm.conf.d/10-nvidia.conf << 'SDDMCONF'
[General]
# Both X11 and Wayland sessions available at login
SDDMCONF
        fi
        ;;
    "xfce")
        echo "Configuring for Xfce (LightDM)..."
        # Xfce only supports X11, configure Xorg properly
        if [ -f /etc/lightdm/lightdm.conf ]; then
            echo "LightDM detected - X11 only, no additional configuration needed."
        fi
        ;;
    *)
        echo "Unknown desktop environment, applying generic configuration..."
        ;;
esac

# Xorg configuration (needed for X11 sessions in all DEs)
echo "Creating Xorg configuration..."
mkdir -p /etc/X11/xorg.conf.d
cat > /etc/X11/xorg.conf.d/10-nvidia-prime.conf << 'XORGCONF'
Section "OutputClass"
    Identifier "nvidia"
    MatchDriver "nvidia-drm"
    Driver "nvidia"
    Option "AllowEmptyInitialConfiguration"
    Option "PrimaryGPU" "yes"
    ModulePath "/usr/lib/x86_64-linux-gnu/nvidia/xorg"
EndSection
XORGCONF

# Regenerate initramfs
echo "Regenerating initramfs..."
dracut --force 2>/dev/null || update-initramfs -u 2>/dev/null || true

echo ""
echo "=== Configuration complete ==="
echo "NVIDIA configured as primary GPU for $DESKTOP_ENV."
echo ""
if [ "$DESKTOP_ENV" = "xfce" ]; then
    echo "Xfce uses X11 only."
else
    echo "Both X11 and Wayland sessions are available."
    echo "Wayland requires driver version 495+ (yours: $DRIVER_VERSION)"
fi
echo ""
echo "IMPORTANT: Restart the system to apply changes."
"""
            self._run_script_as_root(script, "configure-nvidia-primary.sh")
