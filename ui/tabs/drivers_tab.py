"""
Drivers tab for Soplos Welcome.
Handles hardware driver detection and installation.
"""

import gi
import os
import subprocess
import threading
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

from core.i18n_manager import _
from config.paths import ASSETS_DIR
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

        # key → {'button', 'handler_id', 'base_label', 'install_fn', 'uninstall_fn', 'check_fn'}
        self._driver_buttons = {}

        # Main container
        self.drivers_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.drivers_box.set_margin_left(20)
        self.drivers_box.set_margin_right(20)
        self.drivers_box.set_margin_top(20)
        self.drivers_box.set_margin_bottom(20)
        
        self.add(self.drivers_box)
        self._create_ui()
        self._refresh_driver_status()
    
    def _create_ui(self):
        """Create the drivers tab interface."""
        # Header
        header = Gtk.Label()
        header.set_markup(f'<span size="20000" weight="bold">{_("Hardware Drivers")}</span>')
        header.set_halign(Gtk.Align.START)
        self.drivers_box.pack_start(header, False, False, 0)
        
        subtitle = Gtk.Label()
        subtitle.set_markup(f'<span size="12000">{_("Install and manage all hardware drivers: graphics, Wi-Fi, audio, Bluetooth, printers and more")}</span>')
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

        # --- AMD Extras Section ---
        self._create_amd_extras_section()

        # Separator
        self.drivers_box.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 10)

        # --- Intel Extras Section ---
        self._create_intel_extras_section()

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

        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        grid.set_column_homogeneous(True)
        self.drivers_box.pack_start(grid, False, False, 5)

        # Row 0
        nvidia_610 = self._create_button(
            _("NVIDIA 610 (Latest)"),
            _("Blackwell and newer: RTX 50/60 series and latest hardware")
        )
        grid.attach(nvidia_610, 0, 0, 1, 1)
        self._driver_buttons['nvidia_610'] = {
            'button': nvidia_610, 'handler_id': None,
            'base_label': _("NVIDIA 610 (Latest)"),
            'install_fn': lambda b: self._on_nvidia_cuda_repo_clicked(b, '610'),
            'uninstall_fn': lambda b: self._on_uninstall_nvidia_clicked(b),
            'check_fn': lambda: self._get_nvidia_active_version() == '610',
        }

        nvidia_590 = self._create_button(
            _("NVIDIA 590 (Stable)"),
            _("Turing and newer: GTX 1650/1660, RTX 20/30/40/50 series")
        )
        grid.attach(nvidia_590, 1, 0, 1, 1)
        self._driver_buttons['nvidia_590'] = {
            'button': nvidia_590, 'handler_id': None,
            'base_label': _("NVIDIA 590 (Stable)"),
            'install_fn': lambda b: self._on_nvidia_cuda_repo_clicked(b, '590'),
            'uninstall_fn': lambda b: self._on_uninstall_nvidia_clicked(b),
            'check_fn': lambda: self._get_nvidia_active_version() == '590',
        }

        # Row 1
        nvidia_580 = self._create_button(
            _("NVIDIA 580 (Production)"),
            _("Universal driver: Maxwell to Blackwell (GTX 900 → RTX 5000)")
        )
        grid.attach(nvidia_580, 0, 1, 1, 1)
        self._driver_buttons['nvidia_580'] = {
            'button': nvidia_580, 'handler_id': None,
            'base_label': _("NVIDIA 580 (Production)"),
            'install_fn': lambda b: self._on_nvidia_cuda_repo_clicked(b, '580'),
            'uninstall_fn': lambda b: self._on_uninstall_nvidia_clicked(b),
            'check_fn': lambda: self._get_nvidia_active_version() == '580',
        }

        nvidia_550 = self._create_button(
            _("NVIDIA 550 (Repo)"),
            _("Maxwell to Ada Lovelace (GTX 900, GTX 10xx/16xx, RTX 20/30/40)")
        )
        grid.attach(nvidia_550, 1, 1, 1, 1)
        self._driver_buttons['nvidia_550'] = {
            'button': nvidia_550, 'handler_id': None,
            'base_label': _("NVIDIA 550 (Repo)"),
            'install_fn': lambda b: self._on_nvidia_repo_clicked(b, 'nvidia-driver'),
            'uninstall_fn': lambda b: self._on_uninstall_nvidia_clicked(b),
            'check_fn': lambda: self._get_nvidia_active_version() == '550',
        }

        # Row 2
        nvidia_470 = self._create_button(
            _("NVIDIA 470 (Legacy)"),
            _("Kepler to Ampere (GTX 600/700/900/10xx, RTX 20/30 series)")
        )
        grid.attach(nvidia_470, 0, 2, 1, 1)
        self._driver_buttons['nvidia_470'] = {
            'button': nvidia_470, 'handler_id': None,
            'base_label': _("NVIDIA 470 (Legacy)"),
            'install_fn': lambda b: self._on_legacy_nvidia_clicked(b, 'nvidia-tesla-470-driver'),
            'uninstall_fn': lambda b: self._on_uninstall_nvidia_clicked(b),
            'check_fn': lambda: self._is_package_installed('nvidia-tesla-470-driver'),
        }

        nvidia_390 = self._create_button(
            _("NVIDIA 390 (Legacy)"),
            _("Fermi and Kepler (GTX 400/500/600/700 series)")
        )
        grid.attach(nvidia_390, 1, 2, 1, 1)
        self._driver_buttons['nvidia_390'] = {
            'button': nvidia_390, 'handler_id': None,
            'base_label': _("NVIDIA 390 (Legacy)"),
            'install_fn': lambda b: self._on_legacy_nvidia_clicked(b, 'nvidia-legacy-390xx-driver'),
            'uninstall_fn': lambda b: self._on_uninstall_nvidia_clicked(b),
            'check_fn': lambda: self._is_package_installed('nvidia-legacy-390xx-driver'),
        }

        # Row 3
        nvidia_340 = self._create_button(
            _("NVIDIA 340 (Legacy)"),
            _("Tesla architecture (GeForce 8/9/100/200/300 series)")
        )
        grid.attach(nvidia_340, 0, 3, 1, 1)
        self._driver_buttons['nvidia_340'] = {
            'button': nvidia_340, 'handler_id': None,
            'base_label': _("NVIDIA 340 (Legacy)"),
            'install_fn': lambda b: self._on_legacy_nvidia_clicked(b, 'nvidia-legacy-340xx-driver'),
            'uninstall_fn': lambda b: self._on_uninstall_nvidia_clicked(b),
            'check_fn': lambda: self._is_package_installed('nvidia-legacy-340xx-driver'),
        }

        nouveau = self._create_button(
            _("Nouveau (Open Source)"),
            _("Free and open source NVIDIA driver")
        )
        grid.attach(nouveau, 1, 3, 1, 1)
        self._driver_buttons['nouveau'] = {
            'button': nouveau, 'handler_id': None,
            'base_label': _("Nouveau (Open Source)"),
            'install_fn': lambda b: self._on_driver_clicked(b, 'xserver-xorg-video-nouveau'),
            'uninstall_fn': lambda b: self._on_remove_driver_clicked(b, 'xserver-xorg-video-nouveau'),
            'check_fn': lambda: self._is_nouveau_active(),
        }

        # Row 4
        uninstall_nvidia = self._create_button(
            _("Uninstall NVIDIA Drivers"),
            _("Remove all NVIDIA packages completely before switching drivers")
        )
        uninstall_nvidia.connect("clicked", self._on_uninstall_nvidia_clicked)
        grid.attach(uninstall_nvidia, 0, 4, 2, 1)
    
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
        
        davinci_pkgs = "nvidia-opencl-icd libcuda1 libglu1-mesa libnvidia-encode1"
        davinci_btn = self._create_button(
            _("DaVinci Resolve Extras"),
            _("OpenCL and CUDA libraries for DaVinci Resolve")
        )
        box.pack_start(davinci_btn, True, True, 0)
        self._driver_buttons['nvidia_davinci'] = {
            'button': davinci_btn, 'handler_id': None,
            'base_label': _("DaVinci Resolve Extras"),
            'install_fn': lambda b: self._on_nvidia_extras_clicked(b, 'davinci'),
            'uninstall_fn': lambda b: self._on_remove_driver_clicked(b, davinci_pkgs),
            'check_fn': lambda: self._is_package_installed('nvidia-opencl-icd'),
        }

        blender_btn = self._create_button(
            _("Blender CUDA Toolkit"),
            _("CUDA toolkit for Blender GPU rendering")
        )
        box.pack_start(blender_btn, True, True, 0)
        self._driver_buttons['nvidia_blender'] = {
            'button': blender_btn, 'handler_id': None,
            'base_label': _("Blender CUDA Toolkit"),
            'install_fn': lambda b: self._on_nvidia_extras_clicked(b, 'blender'),
            'uninstall_fn': lambda b: self._on_remove_driver_clicked(b, 'nvidia-cuda-toolkit'),
            'check_fn': lambda: self._is_package_installed('nvidia-cuda-toolkit'),
        }

        cuda12_btn = self._create_button(
            _("CUDA 12 Toolkit"),
            _("Full CUDA 12 toolkit for PyTorch, TensorFlow and GPU computing")
        )
        box.pack_start(cuda12_btn, True, True, 0)
        self._driver_buttons['cuda12'] = {
            'button': cuda12_btn, 'handler_id': None,
            'base_label': _("CUDA 12 Toolkit"),
            'install_fn': lambda b: self._on_cuda12_clicked(b, 'install'),
            'uninstall_fn': lambda b: self._on_cuda12_clicked(b, 'uninstall'),
            'check_fn': lambda: self._is_cuda12_installed(),
        }

        open_btn = self._create_button(
            _("Open Kernel Modules"),
            _("Switch to NVIDIA open source kernel modules (Turing+ / RTX 20 and newer)")
        )
        box.pack_start(open_btn, True, True, 0)
        self._driver_buttons['nvidia_open'] = {
            'button': open_btn, 'handler_id': None,
            'base_label': _("Open Kernel Modules"),
            'install_fn': lambda b: self._on_nvidia_open_clicked(b, 'install'),
            'uninstall_fn': lambda b: self._on_nvidia_open_clicked(b, 'uninstall'),
            'check_fn': lambda: self._is_package_installed('nvidia-kernel-open-dkms'),
        }
    
    def _create_amd_section(self):
        """Create AMD drivers section."""
        label = Gtk.Label()
        label.set_markup(f'<span weight="bold" size="14000">{_("AMD Graphics Drivers")}</span>')
        label.set_halign(Gtk.Align.START)
        self.drivers_box.pack_start(label, False, False, 5)

        amd_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        amd_box.set_homogeneous(True)
        self.drivers_box.pack_start(amd_box, False, False, 5)

        amd_pkgs = "firmware-amd-graphics libgl1-mesa-dri libglx-mesa0 mesa-vulkan-drivers xserver-xorg-video-all"
        amd_btn = self._create_button(
            _("AMD Radeon (Open Source)"),
            _("Free drivers for all AMD GPUs")
        )
        amd_box.pack_start(amd_btn, True, True, 0)
        self._driver_buttons['amd'] = {
            'button': amd_btn, 'handler_id': None,
            'base_label': _("AMD Radeon (Open Source)"),
            'install_fn': lambda b: self._on_driver_clicked(b, amd_pkgs),
            'uninstall_fn': lambda b: self._on_remove_driver_clicked(b, amd_pkgs),
            'check_fn': lambda: self._is_amd_driver_installed(),
        }

    
    def _create_amd_extras_section(self):
        """Create AMD Extras section (ROCm OpenCL and full ROCm suite)."""
        label = Gtk.Label()
        label.set_markup(f'<span weight="bold" size="14000">{_("AMD Extras")}</span>')
        label.set_halign(Gtk.Align.START)
        self.drivers_box.pack_start(label, False, False, 5)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        box.set_homogeneous(True)
        self.drivers_box.pack_start(box, False, False, 5)

        rocm_opencl_btn = self._create_button(
            _("ROCm OpenCL"),
            _("OpenCL runtime for AMD GPUs (RDNA1+) — DaVinci Resolve, Blender HIP, GPU compute")
        )
        box.pack_start(rocm_opencl_btn, True, True, 0)
        self._driver_buttons['rocm_opencl'] = {
            'button': rocm_opencl_btn, 'handler_id': None,
            'base_label': _("ROCm OpenCL"),
            'install_fn': lambda b: self._on_rocm_clicked(b, 'opencl'),
            'uninstall_fn': lambda b: self._on_rocm_clicked(b, 'uninstall'),
            'check_fn': lambda: self._is_package_installed('rocm-opencl-runtime'),
        }

        rocm_full_btn = self._create_button(
            _("ROCm Full Suite"),
            _("Complete ROCm platform for AI/ML development with PyTorch and TensorFlow on AMD GPU")
        )
        box.pack_start(rocm_full_btn, True, True, 0)
        self._driver_buttons['rocm_full'] = {
            'button': rocm_full_btn, 'handler_id': None,
            'base_label': _("ROCm Full Suite"),
            'install_fn': lambda b: self._on_rocm_clicked(b, 'full'),
            'uninstall_fn': lambda b: self._on_rocm_clicked(b, 'uninstall'),
            'check_fn': lambda: self._is_package_installed('rocm'),
        }

    def _create_intel_extras_section(self):
        """Create Intel Extras section (oneAPI Base Toolkit)."""
        label = Gtk.Label()
        label.set_markup(f'<span weight="bold" size="14000">{_("Intel Extras")}</span>')
        label.set_halign(Gtk.Align.START)
        self.drivers_box.pack_start(label, False, False, 5)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        box.set_homogeneous(True)
        self.drivers_box.pack_start(box, False, False, 5)

        oneapi_btn = self._create_button(
            _("Intel oneAPI Base Toolkit"),
            _("DPC++ compiler, MKL, TBB, VTune — for Intel Arc GPU and CPU computing")
        )
        box.pack_start(oneapi_btn, True, True, 0)
        self._driver_buttons['oneapi'] = {
            'button': oneapi_btn, 'handler_id': None,
            'base_label': _("Intel oneAPI Base Toolkit"),
            'install_fn': lambda b: self._on_oneapi_clicked(b, 'install'),
            'uninstall_fn': lambda b: self._on_oneapi_clicked(b, 'uninstall'),
            'check_fn': lambda: os.path.exists('/opt/intel/oneapi/setvars.sh'),
        }

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
        box.pack_start(intel_wifi, True, True, 0)
        self._driver_buttons['wifi_intel'] = {
            'button': intel_wifi, 'handler_id': None,
            'base_label': _("Intel Wi-Fi"),
            'install_fn': lambda b: self._on_driver_clicked(b, 'firmware-iwlwifi'),
            'uninstall_fn': lambda b: self._on_remove_driver_clicked(b, 'firmware-iwlwifi'),
            'check_fn': lambda: self._is_package_installed('firmware-iwlwifi') and self._is_module_loaded('iwlwifi'),
        }

        realtek_wifi = self._create_button(_("Realtek Wi-Fi"), _("Realtek wireless cards"))
        box.pack_start(realtek_wifi, True, True, 0)
        self._driver_buttons['wifi_realtek'] = {
            'button': realtek_wifi, 'handler_id': None,
            'base_label': _("Realtek Wi-Fi"),
            'install_fn': lambda b: self._on_driver_clicked(b, 'firmware-realtek'),
            'uninstall_fn': lambda b: self._on_remove_driver_clicked(b, 'firmware-realtek'),
            'check_fn': lambda: self._is_package_installed('firmware-realtek') and self._is_module_loaded('r8169', 'rtl8xxxu', 'r8188eu', 'rtw88_8822be', 'rtw89_pci'),
        }

        broadcom_wifi = self._create_button(_("Broadcom Wi-Fi"), _("Broadcom wireless cards"))
        box.pack_start(broadcom_wifi, True, True, 0)
        self._driver_buttons['wifi_broadcom'] = {
            'button': broadcom_wifi, 'handler_id': None,
            'base_label': _("Broadcom Wi-Fi"),
            'install_fn': lambda b: self._on_driver_clicked(b, 'firmware-b43-installer'),
            'uninstall_fn': lambda b: self._on_remove_driver_clicked(b, 'firmware-b43-installer'),
            'check_fn': lambda: self._is_package_installed('firmware-b43-installer'),
        }

        repair_btn = self._create_button(
            _("Repair Wi-Fi"),
            _("Reload Wi-Fi driver and restart NetworkManager — fixes connection lost after reboot")
        )
        repair_btn.connect("clicked", self._on_repair_wifi_clicked)
        self.drivers_box.pack_start(repair_btn, False, False, 0)
    
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
        box.pack_start(printer_btn, True, True, 0)
        self._driver_buttons['printers'] = {
            'button': printer_btn, 'handler_id': None,
            'base_label': _("Printers"),
            'install_fn': lambda b: self._on_driver_clicked(b, 'printer-driver-all'),
            'uninstall_fn': lambda b: self._on_remove_driver_clicked(b, 'printer-driver-all'),
            'check_fn': lambda: self._is_package_installed('printer-driver-all'),
        }

        bt_pkgs = "bluetooth bluez bluez-tools blueman"
        bluetooth_btn = self._create_button(_("Bluetooth"), _("Bluetooth support"))
        box.pack_start(bluetooth_btn, True, True, 0)
        self._driver_buttons['bluetooth'] = {
            'button': bluetooth_btn, 'handler_id': None,
            'base_label': _("Bluetooth"),
            'install_fn': lambda b: self._on_driver_clicked(b, bt_pkgs),
            'uninstall_fn': lambda b: self._on_remove_driver_clicked(b, bt_pkgs),
            'check_fn': lambda: self._is_package_installed('bluetooth'),
        }
    
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
        box.pack_start(vmware_btn, True, True, 0)
        self._driver_buttons['vmware'] = {
            'button': vmware_btn, 'handler_id': None,
            'base_label': _("VMware Tools"),
            'install_fn': lambda b: self._on_driver_clicked(b, 'open-vm-tools-desktop'),
            'uninstall_fn': lambda b: self._on_remove_driver_clicked(b, 'open-vm-tools-desktop'),
            'check_fn': lambda: self._is_package_installed('open-vm-tools-desktop'),
        }

        qemu_pkgs = "qemu-guest-agent spice-vdagent spice-webdavd xserver-xspice"
        qemu_btn = self._create_button(_("QEMU/KVM Tools"), _("For QEMU/KVM virtual machines"))
        box.pack_start(qemu_btn, True, True, 0)
        self._driver_buttons['qemu'] = {
            'button': qemu_btn, 'handler_id': None,
            'base_label': _("QEMU/KVM Tools"),
            'install_fn': lambda b: self._on_driver_clicked(b, qemu_pkgs),
            'uninstall_fn': lambda b: self._on_remove_driver_clicked(b, qemu_pkgs),
            'check_fn': lambda: self._is_package_installed('qemu-guest-agent'),
        }

        def _check_vbox():
            try:
                r = subprocess.run(['systemctl', 'is-enabled', 'vboxadd'],
                                   capture_output=True, text=True)
                return r.returncode == 0
            except Exception:
                return False

        vbox_btn = self._create_button(_("VirtualBox Guest"), _("For VirtualBox virtual machines"))
        box.pack_start(vbox_btn, True, True, 0)
        self._driver_buttons['vbox'] = {
            'button': vbox_btn, 'handler_id': None,
            'base_label': _("VirtualBox Guest"),
            'install_fn': lambda b: self._on_vbox_clicked(b),
            'uninstall_fn': lambda b: self._on_remove_driver_clicked(b, 'virtualbox-guest-utils virtualbox-guest-x11'),
            'check_fn': _check_vbox,
        }
    
    # === DRIVER DETECTION ===

    def _detect_wifi_driver(self):
        """Return (iface, driver) detecting the Wi-Fi module by any available method.

        Strategy 1 — sysfs: works when the interface is up and driver loaded normally.
        Strategy 2 — iw dev: works when the interface is down but module is loaded.
        Strategy 3 — lspci -k: works even when the module is NOT loaded (broken state
                     after reboot), which is exactly the case this button is meant to fix.
        Returns (iface_or_None, driver) — driver is always set if hardware is found.
        """
        import glob

        # Strategy 1: sysfs wireless subdir + device/driver symlink
        for path in glob.glob('/sys/class/net/*/wireless'):
            iface = os.path.basename(os.path.dirname(path))
            driver_link = f'/sys/class/net/{iface}/device/driver'
            try:
                if os.path.islink(driver_link):
                    driver = os.path.basename(os.readlink(driver_link))
                    return iface, driver
            except Exception:
                pass

        # Strategy 2: iw dev (interface exists but may be down)
        try:
            result = subprocess.run(['iw', 'dev'], capture_output=True, text=True)
            for line in result.stdout.splitlines():
                line = line.strip()
                if line.startswith('Interface '):
                    iface = line.split()[1]
                    driver_link = f'/sys/class/net/{iface}/device/driver'
                    try:
                        if os.path.islink(driver_link):
                            driver = os.path.basename(os.readlink(driver_link))
                            return iface, driver
                    except Exception:
                        pass
        except Exception:
            pass

        # Strategy 3: lspci -k — detects the module even when not loaded
        # This is the critical fallback for the "no WiFi after reboot" case
        try:
            result = subprocess.run(['lspci', '-k'], capture_output=True, text=True)
            lines = result.stdout.splitlines()
            in_wifi = False
            for line in lines:
                lower = line.lower()
                if any(k in lower for k in ('network controller', 'wireless', 'wifi', 'wi-fi')):
                    in_wifi = True
                elif line and not line.startswith('\t') and not line.startswith(' '):
                    in_wifi = False
                if in_wifi:
                    if 'kernel modules:' in lower:
                        modules = line.split(':', 1)[1].strip().split(',')
                        driver = modules[0].strip()
                        if driver:
                            return None, driver
                    elif 'kernel driver in use:' in lower:
                        driver = line.split(':', 1)[1].strip()
                        if driver:
                            return None, driver
        except Exception:
            pass

        return None, None

    def _on_repair_wifi_clicked(self, button):
        """Reload the Wi-Fi driver and restart NetworkManager."""
        button.set_sensitive(False)
        self.progress_label.set_text(_("Detecting Wi-Fi hardware..."))

        def _detect():
            iface, driver = self._detect_wifi_driver()
            GLib.idle_add(_on_detected, iface, driver)

        def _on_detected(iface, driver):
            button.set_sensitive(True)
            self.progress_label.set_text("")

            if not driver:
                dialog = Gtk.MessageDialog(
                    transient_for=self.parent_window,
                    flags=0,
                    message_type=Gtk.MessageType.WARNING,
                    buttons=Gtk.ButtonsType.OK,
                    text=_("No Wi-Fi Interface Found")
                )
                dialog.format_secondary_text(
                    _("No active Wi-Fi interface was detected.\nMake sure your Wi-Fi card is connected and recognized by the system.")
                )
                dialog.run()
                dialog.destroy()
                return

            dialog = Gtk.MessageDialog(
                transient_for=self.parent_window,
                flags=0,
                message_type=Gtk.MessageType.QUESTION,
                buttons=Gtk.ButtonsType.YES_NO,
                text=_("Repair Wi-Fi Connection")
            )
            dialog.format_secondary_text(
                _("Detected driver: {driver}  |  Interface: {iface}\n\n"
                  "This will:\n"
                  "  • Unload and reload the Wi-Fi kernel module\n"
                  "  • Restart NetworkManager\n\n"
                  "Your network connection will be briefly interrupted.\n"
                  "Proceed?").format(driver=driver, iface=iface if iface else _("not loaded"))
            )
            response = dialog.run()
            dialog.destroy()

            if response == Gtk.ResponseType.YES:
                script = f"""#!/bin/bash
modprobe -r {driver} 2>/dev/null || true
sleep 1
modprobe {driver}
systemctl restart NetworkManager
echo "Wi-Fi repair completed. Driver: {driver}"
"""
                self._run_script_as_root(script, "repair-wifi.sh")

        threading.Thread(target=_detect, daemon=True).start()

    def _is_nouveau_active(self):
        """Return True only if nouveau package is installed AND not blacklisted."""
        if not self._is_package_installed('xserver-xorg-video-nouveau'):
            return False
        import glob
        try:
            for conf in glob.glob('/etc/modprobe.d/*.conf'):
                try:
                    with open(conf) as f:
                        if 'blacklist nouveau' in f.read():
                            return False
                except Exception:
                    pass
        except Exception:
            pass
        return True

    def _is_amd_driver_installed(self):
        """Return True only if the full AMD driver stack installed by this app is present."""
        return (
            self._is_package_installed('firmware-amd-graphics') and
            self._is_package_installed('mesa-vulkan-drivers') and
            self._is_package_installed('xserver-xorg-video-all')
        )

    def _is_module_loaded(self, *module_names):
        """Return True if any of the given kernel modules are currently loaded."""
        try:
            result = subprocess.run(['lsmod'], capture_output=True, text=True)
            for name in module_names:
                if name in result.stdout:
                    return True
        except Exception:
            pass
        return False

    def _is_package_installed(self, package):
        """Check if a dpkg package is installed."""
        try:
            result = subprocess.run(
                ['dpkg', '-s', package],
                capture_output=True, text=True
            )
            return 'Status: install ok installed' in result.stdout
        except Exception:
            return False

    def _get_nvidia_active_version(self):
        """Return major version string of active NVIDIA driver (e.g. '590'), or None."""
        # nvidia-smi: works regardless of how the driver was installed
        try:
            result = subprocess.run(
                ['nvidia-smi', '--query-gpu=driver_version', '--format=csv,noheader'],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                ver = result.stdout.strip().split('.')[0]
                if ver.isdigit():
                    return ver
        except Exception:
            pass
        # Fallback: scan dpkg only if NVIDIA hardware is present (e.g. first boot with nouveau)
        try:
            lspci = subprocess.run(['lspci'], capture_output=True, text=True)
            if not any(k in lspci.stdout for k in ('NVIDIA', 'GeForce', 'Quadro', 'Tesla')):
                return None
        except Exception:
            return None
        try:
            import re
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

    def _apply_driver_state(self, key, installed):
        """Update button label, style and signal handler. Runs on GTK thread."""
        info = self._driver_buttons.get(key)
        if not info:
            return
        button = info['button']

        # Disconnect previous handler
        if info.get('handler_id') is not None:
            try:
                button.disconnect(info['handler_id'])
            except Exception:
                pass

        if installed:
            button.set_label(f"✓  {info['base_label']}")
            info['handler_id'] = button.connect('clicked', info['uninstall_fn'])
        else:
            button.set_label(info['base_label'])
            info['handler_id'] = button.connect('clicked', info['install_fn'])

    def _refresh_driver_status(self):
        """Check all registered driver buttons in background and update their state."""
        def _check():
            for key, info in list(self._driver_buttons.items()):
                try:
                    installed = info['check_fn']()
                    GLib.idle_add(self._apply_driver_state, key, installed)
                except Exception as e:
                    print(f"Error checking driver {key}: {e}")

        threading.Thread(target=_check, daemon=True).start()

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
        self._run_script_as_root(script, f"install-{packages.split()[0]}.sh",
                                 self._refresh_driver_status)

    def _on_remove_driver_clicked(self, button, packages):
        """Remove driver packages."""
        script = f"""#!/bin/bash
set -e
apt remove -y {packages}
apt autoremove -y
echo "Removal completed successfully."
"""
        self._run_script_as_root(script, f"uninstall-{packages.split()[0]}.sh",
                                 self._refresh_driver_status)
    
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

# === CLEANUP DKMS MODULES ===
echo "Removing NVIDIA DKMS modules from all kernels..."
for entry in $(dkms status | grep -i nvidia | awk -F'[:,]' '{{print $1"/"$2}}' | tr -d ' '); do
    dkms remove --force "$entry" --all 2>/dev/null || true
done
for kver in $(ls /lib/modules/); do
    rm -f /lib/modules/$kver/updates/dkms/nvidia*.ko*
    depmod -a "$kver" 2>/dev/null || true
done
rm -rf /var/lib/dkms/nvidia*

# === CLEANUP EXISTING NVIDIA PACKAGES ===
echo "Removing existing NVIDIA packages to prevent conflicts..."
apt purge -y 'nvidia-driver*' 'nvidia-kernel*' 'libnvidia*' 'nvidia-modprobe' \
    'nvidia-settings' 'nvidia-smi' 'nvidia-opencl*' 'nvidia-cuda*' \
    'cuda-drivers*' 'xserver-xorg-video-nvidia*' 2>/dev/null || true
apt autoremove -y 2>/dev/null || true

# Install kernel headers and DKMS build dependencies
apt update
apt install -y dkms build-essential linux-headers-$(uname -r)

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
        self._run_script_as_root(script, f"install-{package}.sh", self._refresh_driver_status)

    
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

        distro = "debian12" if version == "580" else "debian13"
        if version == "580":
            # debian12 CUDA repo usa SHA1 en las binding signatures de su clave GPG.
            # sqv (usado por Debian 13) rechaza SHA1 desde 2026-02-01, así que
            # no podemos usar cuda-keyring. Añadimos el repo con trusted=yes.
            repo_setup = """echo "deb [trusted=yes] https://developer.download.nvidia.com/compute/cuda/repos/debian12/x86_64/ /" \\
    > /etc/apt/sources.list.d/cuda-debian12-x86_64.list
trap 'rm -f /etc/apt/sources.list.d/cuda-debian12-x86_64.list' EXIT"""
            install_driver = "apt install -y nvidia-driver-pinning-580\napt install -y --allow-downgrades cuda-drivers-580"
            repo_cleanup = """trap - EXIT
rm -f /etc/apt/sources.list.d/cuda-debian12-x86_64.list
apt update -q"""
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
            install_driver = "apt install -y nvidia-driver-pinning-590\napt install -y cuda-drivers-590 nvidia-kernel-open-dkms"
            repo_cleanup = ""
        else:
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
            install_driver = "apt install -y nvidia-driver-pinning-610\napt install -y cuda-drivers-610 nvidia-kernel-open-dkms"
            repo_cleanup = ""

        script = f"""#!/bin/bash

set -e
NVIDIA_VERSION="{version}"
DISTRO="{distro}"
LOG="/tmp/nvidia-install-$NVIDIA_VERSION.log"
exec > >(tee -a "$LOG") 2>&1

echo "=== NVIDIA $NVIDIA_VERSION Official CUDA Repository ($DISTRO) ==="
echo ""

echo "[0/6] Removing NVIDIA DKMS modules from all kernels..."
for entry in $(dkms status | grep -i nvidia | awk -F'[:,]' '{{print $1"/"$2}}' | tr -d ' '); do
    dkms remove --force "$entry" --all 2>/dev/null || true
done
for kver in $(ls /lib/modules/); do
    rm -f /lib/modules/$kver/updates/dkms/nvidia*.ko*
    depmod -a "$kver" 2>/dev/null || true
done
rm -rf /var/lib/dkms/nvidia*

echo "[1/6] Removing existing NVIDIA/CUDA packages..."
rm -f /etc/dracut.conf.d/nvidia.conf
rm -f /etc/dracut.conf.d/blacklist-nouveau.conf
rm -f /etc/modprobe.d/blacklist-nouveau.conf
rm -f /etc/apt/apt.conf.d/99nvidia-sha1-exception
apt purge -y 'nvidia*' 'cuda*' 'libnvidia*' 2>/dev/null || true
apt autoremove -y 2>/dev/null || true
apt -f install -y 2>/dev/null || true

echo "[2/6] Installing kernel headers and DKMS build dependencies..."
apt install -y dkms build-essential
if apt-cache show linux-headers-$(uname -r) &>/dev/null; then
    apt install -y linux-headers-$(uname -r)
else
    echo "Custom kernel detected, headers already present, skipping."
fi

echo "[3/6] Setting up NVIDIA CUDA repository ($DISTRO)..."
{repo_setup}

echo "[4/6] Installing NVIDIA Driver $NVIDIA_VERSION..."
apt update
{install_driver}
{repo_cleanup}

echo "[5/6] Blacklisting nouveau and regenerating initramfs..."
mkdir -p /etc/modprobe.d
cat > /etc/modprobe.d/blacklist-nouveau.conf << 'MODPROBE'
blacklist nouveau
options nouveau modeset=0
MODPROBE

if command -v dracut >/dev/null 2>&1; then
    mkdir -p /etc/dracut.conf.d
    echo 'omit_drivers+=" nouveau "' > /etc/dracut.conf.d/blacklist-nouveau.conf
    echo 'add_drivers+=" nvidia nvidia_modeset nvidia_uvm nvidia_drm "' > /etc/dracut.conf.d/nvidia.conf
    dracut --force
elif command -v update-initramfs >/dev/null 2>&1; then
    update-initramfs -u
fi

echo "[+] Configuring GRUB with nvidia-drm.modeset=1..."
if ! grep -q "nvidia-drm.modeset=1" /etc/default/grub; then
    sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT="\\([^"]*\\)"/GRUB_CMDLINE_LINUX_DEFAULT="\\1 nvidia-drm.modeset=1"/' /etc/default/grub
fi
update-grub

echo ""
echo "[6/6] Done."
echo "=== Installation completed successfully ==="
echo "NVIDIA driver $NVIDIA_VERSION installed. Restart to apply changes."
"""
        self._run_script_as_root(script, f"install-nvidia-cuda-{version}.sh", self._refresh_driver_status)

    
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
        self._run_script_as_root(script, script_name, self._refresh_driver_status)

    def _on_rocm_clicked(self, button, mode):
        """Install or remove ROCm from the official AMD repository."""
        if mode == 'uninstall':
            confirm_dialog = Gtk.MessageDialog(
                transient_for=self.parent_window,
                flags=0,
                message_type=Gtk.MessageType.WARNING,
                buttons=Gtk.ButtonsType.YES_NO,
                text=_("Remove ROCm")
            )
            confirm_dialog.format_secondary_text(
                _("This will remove all ROCm packages and the AMD ROCm repository.\n\n"
                  "Do you want to continue?")
            )
            response = confirm_dialog.run()
            confirm_dialog.destroy()
            if response != Gtk.ResponseType.YES:
                return

            script = """#!/bin/bash
set -e
echo "=== Removing ROCm ==="
apt purge -y 'rocm*' 'hip*' 'hsa*' 'comgr*' 'rocblas*' 'rocsolver*' 2>/dev/null || true
apt autoremove -y 2>/dev/null || true
rm -f /etc/apt/sources.list.d/rocm.list
rm -f /etc/apt/keyrings/rocm.gpg
apt update -q
echo "[+] ROCm removed successfully."
"""
            self._run_script_as_root(script, "remove-rocm.sh", self._refresh_driver_status)
            return

        pkg = 'rocm-opencl-runtime' if mode == 'opencl' else 'rocm'
        label = _("ROCm OpenCL") if mode == 'opencl' else _("ROCm Full Suite")
        size_note = _("~200 MB download.") if mode == 'opencl' else _("Several GB download — this may take a while.")

        confirm_dialog = Gtk.MessageDialog(
            transient_for=self.parent_window,
            flags=0,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.YES_NO,
            text=_("Confirm ROCm Installation — {label}").format(label=label)
        )
        confirm_dialog.format_secondary_text(
            _("This will:\n\n"
              "1. Add the official AMD ROCm repository.\n"
              "2. Install {label}.\n"
              "3. Add your user to the render and video groups.\n\n"
              "Requires an AMD GPU (RDNA1 or newer: RX 5000+, Radeon 600M/700M series).\n"
              "Not compatible with older GCN GPUs.\n\n"
              "{size}\n\n"
              "A session restart will be required after installation.\n\n"
              "Do you want to continue?").format(label=label, size=size_note)
        )
        response = confirm_dialog.run()
        confirm_dialog.destroy()
        if response != Gtk.ResponseType.YES:
            return

        script = f"""#!/bin/bash
set -e
LOG="/tmp/rocm-install.log"
exec > >(tee -a "$LOG") 2>&1

echo "=== AMD ROCm Installation ({label}) ==="
echo ""

echo "[1/4] Setting up AMD ROCm repository..."
mkdir -p /etc/apt/keyrings
curl -fsSL https://repo.radeon.com/rocm/rocm.gpg.key | gpg --dearmor -o /etc/apt/keyrings/rocm.gpg

CODENAME=$(. /etc/os-release && echo "$VERSION_CODENAME")
case "$CODENAME" in
    trixie) ROCM_DISTRO="trixie" ;;
    forky)  ROCM_DISTRO="forky"  ;;
    *)      ROCM_DISTRO="trixie" ;;
esac

echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/rocm/apt/6.4 $ROCM_DISTRO main" \\
    > /etc/apt/sources.list.d/rocm.list

echo "[2/4] Updating package lists..."
apt update

echo "[3/4] Installing {label}..."
apt install -y {pkg}

echo "[4/4] Adding user to render and video groups..."
REAL_USER=$(getent passwd $PKEXEC_UID | cut -d: -f1)
usermod -aG render,video "$REAL_USER"

echo ""
echo "=== Installation completed successfully ==="
echo "ROCm installed. Please restart your session to apply group membership."
"""
        self._run_script_as_root(script, f"install-rocm-{mode}.sh", self._refresh_driver_status)

    def _is_turing_plus(self):
        """Return True if the detected NVIDIA GPU supports open kernel modules (Turing+)."""
        try:
            from utils.hardware_detector import detect_all_gpus
            gpus = detect_all_gpus()
            for gpu in gpus:
                if gpu.get('vendor', '').upper() != 'NVIDIA':
                    continue
                model = gpu.get('model', '').lower()
                turing_plus = [
                    'rtx 20', 'rtx20', 'rtx 30', 'rtx30', 'rtx 40', 'rtx40',
                    'rtx 50', 'rtx50', 'gtx 16', 'gtx16', 'gtx 1650', 'gtx 1660',
                    'mx550', 'mx 550', 'mx450', 'mx 450',
                    'a100', 'a40', 'a30', 'a10', 'rtx a',
                ]
                if any(s in model for s in turing_plus):
                    return True
        except Exception:
            pass
        return False

    def _is_cuda12_installed(self):
        """Check if CUDA 12 toolkit is installed."""
        return os.path.exists('/usr/local/cuda/bin/nvcc')

    def _on_nvidia_open_clicked(self, button, mode):
        """Switch between proprietary and open NVIDIA kernel modules."""
        if mode == 'uninstall':
            confirm_dialog = Gtk.MessageDialog(
                transient_for=self.parent_window,
                flags=0,
                message_type=Gtk.MessageType.WARNING,
                buttons=Gtk.ButtonsType.YES_NO,
                text=_("Switch to Proprietary Kernel Module")
            )
            confirm_dialog.format_secondary_text(
                _("This will replace the open kernel module with the proprietary NVIDIA kernel module.\n\n"
                  "A system restart will be required.\n\n"
                  "Do you want to continue?")
            )
            response = confirm_dialog.run()
            confirm_dialog.destroy()
            if response != Gtk.ResponseType.YES:
                return

            script = """#!/bin/bash
set -e
echo "=== Switching to proprietary NVIDIA kernel module ==="
apt install -y nvidia-kernel-dkms
apt purge -y nvidia-kernel-open-dkms 2>/dev/null || true
echo "[+] Done. Restart required."
"""
            self._run_script_as_root(script, "nvidia-proprietary-module.sh", self._refresh_driver_status)
            return

        if not self._is_turing_plus():
            error_dialog = Gtk.MessageDialog(
                transient_for=self.parent_window,
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text=_("Incompatible GPU")
            )
            error_dialog.format_secondary_text(
                _("Open kernel modules require a Turing or newer GPU (RTX 20 series, GTX 1650/1660 or newer).\n\n"
                  "Your GPU is not compatible with this option.")
            )
            error_dialog.run()
            error_dialog.destroy()
            return

        confirm_dialog = Gtk.MessageDialog(
            transient_for=self.parent_window,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.YES_NO,
            text=_("Switch to Open Kernel Modules")
        )
        confirm_dialog.format_secondary_text(
            _("This will replace the proprietary NVIDIA kernel module with the official open source version.\n\n"
              "Recommended for RTX 30 series and newer. Requires a NVIDIA driver already installed.\n\n"
              "A system restart will be required.\n\n"
              "Do you want to continue?")
        )
        response = confirm_dialog.run()
        confirm_dialog.destroy()
        if response != Gtk.ResponseType.YES:
            return

        script = """#!/bin/bash
set -e
echo "=== Switching to NVIDIA open kernel modules ==="
apt install -y nvidia-kernel-open-dkms
apt purge -y nvidia-kernel-dkms 2>/dev/null || true
echo "[+] Done. Restart required."
"""
        self._run_script_as_root(script, "nvidia-open-module.sh", self._refresh_driver_status)

    def _on_cuda12_clicked(self, button, mode):
        """Install or remove CUDA 12 Toolkit from the NVIDIA debian12 repository."""
        if mode == 'uninstall':
            confirm_dialog = Gtk.MessageDialog(
                transient_for=self.parent_window,
                flags=0,
                message_type=Gtk.MessageType.WARNING,
                buttons=Gtk.ButtonsType.YES_NO,
                text=_("Remove CUDA 12 Toolkit")
            )
            confirm_dialog.format_secondary_text(
                _("This will remove all CUDA 12 packages and the NVIDIA CUDA repository.\n\n"
                  "Do you want to continue?")
            )
            response = confirm_dialog.run()
            confirm_dialog.destroy()
            if response != Gtk.ResponseType.YES:
                return

            script = """#!/bin/bash
set -e
echo "=== Removing CUDA 12 Toolkit ==="
apt purge -y 'cuda-toolkit-12*' 'cuda-compiler-12*' 'cuda-libraries-12*' \
    'cuda-tools-12*' 'cuda-documentation-12*' 'cuda-nvml-dev-12*' 2>/dev/null || true
apt autoremove -y 2>/dev/null || true
rm -f /etc/apt/sources.list.d/cuda-debian12-x86_64.list
apt update -q
echo "[+] CUDA 12 Toolkit removed successfully."
"""
            self._run_script_as_root(script, "remove-cuda12.sh", self._refresh_driver_status)
            return

        confirm_dialog = Gtk.MessageDialog(
            transient_for=self.parent_window,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.YES_NO,
            text=_("Confirm CUDA 12 Toolkit Installation")
        )
        confirm_dialog.format_secondary_text(
            _("This will:\n\n"
              "1. Add the NVIDIA CUDA repository.\n"
              "2. Install CUDA 12 Toolkit (nvcc, cuBLAS, cuDNN, CUDA libraries).\n\n"
              "Compatible with PyTorch and TensorFlow cu12 builds.\n"
              "Requires an NVIDIA GPU with a driver already installed.\n\n"
              "Several GB download — this may take a while.\n\n"
              "Do you want to continue?")
        )
        response = confirm_dialog.run()
        confirm_dialog.destroy()
        if response != Gtk.ResponseType.YES:
            return

        script = """#!/bin/bash
set -e
LOG="/tmp/cuda12-install.log"
exec > >(tee -a "$LOG") 2>&1

echo "=== CUDA 12 Toolkit Installation ==="
echo ""

echo "[1/3] Setting up NVIDIA CUDA repository..."
echo "deb [trusted=yes] https://developer.download.nvidia.com/compute/cuda/repos/debian12/x86_64/ /" \\
    > /etc/apt/sources.list.d/cuda-debian12-x86_64.list

echo "[2/3] Updating package lists..."
apt update

echo "[3/3] Installing CUDA 12 Toolkit..."
apt install -y cuda-toolkit-12

echo ""
echo "=== Installation completed successfully ==="
echo "CUDA 12 Toolkit installed. Run 'nvcc --version' to verify."
"""
        self._run_script_as_root(script, "install-cuda12.sh", self._refresh_driver_status)

    def _on_oneapi_clicked(self, button, mode):
        """Install or remove Intel oneAPI Base Toolkit."""
        if mode == 'uninstall':
            confirm_dialog = Gtk.MessageDialog(
                transient_for=self.parent_window,
                flags=0,
                message_type=Gtk.MessageType.WARNING,
                buttons=Gtk.ButtonsType.YES_NO,
                text=_("Remove Intel oneAPI")
            )
            confirm_dialog.format_secondary_text(
                _("This will remove the Intel oneAPI Base Toolkit and its repository.\n\n"
                  "Do you want to continue?")
            )
            response = confirm_dialog.run()
            confirm_dialog.destroy()
            if response != Gtk.ResponseType.YES:
                return

            script = """#!/bin/bash
set -e
echo "=== Removing Intel oneAPI Base Toolkit ==="
apt purge -y 'intel-basekit*' 'intel-oneapi-*' 2>/dev/null || true
apt autoremove -y 2>/dev/null || true
rm -f /etc/apt/sources.list.d/intel-oneapi.list
rm -f /etc/apt/keyrings/intel-oneapi.gpg
apt update -q
echo "[+] Intel oneAPI removed successfully."
"""
            self._run_script_as_root(script, "remove-oneapi.sh", self._refresh_driver_status)
            return

        confirm_dialog = Gtk.MessageDialog(
            transient_for=self.parent_window,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.YES_NO,
            text=_("Confirm Intel oneAPI Installation")
        )
        confirm_dialog.format_secondary_text(
            _("This will:\n\n"
              "1. Add the official Intel oneAPI repository.\n"
              "2. Install Intel oneAPI Base Toolkit (DPC++ compiler, MKL, TBB, VTune, Advisor).\n\n"
              "Recommended for Intel Arc GPU users and Intel CPU-accelerated computing.\n\n"
              "Several GB download — this may take a while.\n\n"
              "Do you want to continue?")
        )
        response = confirm_dialog.run()
        confirm_dialog.destroy()
        if response != Gtk.ResponseType.YES:
            return

        script = """#!/bin/bash
set -e
LOG="/tmp/oneapi-install.log"
exec > >(tee -a "$LOG") 2>&1

echo "=== Intel oneAPI Base Toolkit Installation ==="
echo ""

echo "[1/3] Setting up Intel oneAPI repository..."
mkdir -p /etc/apt/keyrings
curl -fsSL https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB \\
    | gpg --dearmor -o /etc/apt/keyrings/intel-oneapi.gpg
echo "deb [signed-by=/etc/apt/keyrings/intel-oneapi.gpg] https://apt.repos.intel.com/oneapi all main" \\
    > /etc/apt/sources.list.d/intel-oneapi.list

echo "[2/3] Updating package lists..."
apt update

echo "[3/3] Installing Intel oneAPI Base Toolkit..."
apt install -y intel-basekit

echo ""
echo "=== Installation completed successfully ==="
echo "Run 'source /opt/intel/oneapi/setvars.sh' to activate the environment."
"""
        self._run_script_as_root(script, "install-oneapi.sh", self._refresh_driver_status)

    def _on_vbox_clicked(self, button):
        """Install VirtualBox Guest Additions."""
        vbox_run = os.path.join(ASSETS_DIR, "vbox", "VBoxLinuxAdditions.run")
        script = f"""#!/bin/bash

echo "Installing VirtualBox Guest Additions..."

# Install dependencies
apt update
apt install -y build-essential dkms linux-headers-$(uname -r)

# Run installer (non-zero exit expected when not running inside VirtualBox)
"{vbox_run}" || true

echo ""
echo "=== Installation completed ==="
echo "VirtualBox Guest Additions installed."
echo "IMPORTANT: Restart the system to apply the changes."
"""
        self._run_script_as_root(script, "install-vbox-guest.sh", self._refresh_driver_status)
    
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
    
    def _run_script_as_root(self, script_content, script_name, on_complete=None):
        """Create and run installation script with root privileges (single pkexec)."""
        script_path = f"/tmp/{script_name}"
        try:
            with open(script_path, "w") as f:
                f.write(script_content)
            os.chmod(script_path, 0o755)
            self.command_runner.run_command(f"pkexec bash {script_path}", on_complete)
        except Exception as e:
            print(f"Error creating script {script_name}: {e}")
    
    def _is_flatpak_installed(self, flatpak_id):
        """Check if a Flatpak app is installed."""
        try:
            result = subprocess.run(['flatpak', 'info', flatpak_id],
                                    capture_output=True, text=True)
            return result.returncode == 0
        except Exception:
            return False


    def _on_scan_hardware(self, button):
        """Scan hardware and show results."""
        from utils.hardware_detector import scan_hardware

        def update_status(text):
            self.progress_label.set_text(text)

        def update_progress(fraction):
            self.progress_bar.set_fraction(fraction)

        def _make_frame(title):
            frame = Gtk.Frame(label=title)
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
            box.set_margin_left(15)
            box.set_margin_right(15)
            box.set_margin_top(10)
            box.set_margin_bottom(10)
            frame.add(box)
            return frame, box

        def _driver_action_buttons(parent_box, driver_status, missing_packages,
                                    recommended_driver, install_cb, uninstall_cb=None):
            """Add Install/Uninstall button row based on driver_status."""
            if driver_status == 'installed':
                lbl = Gtk.Label()
                lbl.set_markup(f"<span foreground='green'>✓ {_('Driver installed')}</span>")
                lbl.set_xalign(0)
                parent_box.pack_start(lbl, False, False, 0)
                if uninstall_cb:
                    btn = Gtk.Button(label=_("Uninstall"))
                    btn.connect('clicked', uninstall_cb)
                    parent_box.pack_start(btn, False, False, 2)
            elif driver_status == 'different_version':
                lbl = Gtk.Label()
                lbl.set_markup(f"<span foreground='orange'>⚠ {_('Different version installed')}</span>")
                lbl.set_xalign(0)
                parent_box.pack_start(lbl, False, False, 0)
                btn = Gtk.Button(label=f"{_('Switch to')} {recommended_driver}")
                btn.connect('clicked', install_cb)
                parent_box.pack_start(btn, False, False, 2)
            elif driver_status == 'partial':
                lbl = Gtk.Label()
                lbl.set_markup(f"<span foreground='orange'>⚠ {_('Partially installed — missing:')} {', '.join(missing_packages)}</span>")
                lbl.set_xalign(0)
                lbl.set_line_wrap(True)
                parent_box.pack_start(lbl, False, False, 0)
                btn = Gtk.Button(label=_("Complete installation"))
                btn.connect('clicked', install_cb)
                parent_box.pack_start(btn, False, False, 2)
            else:  # missing
                lbl = Gtk.Label()
                lbl.set_markup(f"<span foreground='red'>✗ {_('Not installed')}</span>")
                lbl.set_xalign(0)
                parent_box.pack_start(lbl, False, False, 0)
                btn = Gtk.Button(label=f"{_('Install')} {recommended_driver}")
                btn.connect('clicked', install_cb)
                parent_box.pack_start(btn, False, False, 2)

        def show_results(results):
            self.progress_bar.set_fraction(0.0)

            dialog = Gtk.Dialog(
                title=_("Hardware Detection"),
                parent=self.parent_window,
                flags=0
            )
            dialog.set_default_size(700, 650)

            scrolled = Gtk.ScrolledWindow()
            scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
            dialog.get_content_area().pack_start(scrolled, True, True, 0)

            main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
            main_box.set_margin_left(20)
            main_box.set_margin_right(20)
            main_box.set_margin_top(20)
            main_box.set_margin_bottom(10)
            scrolled.add(main_box)

            # ── CPU ──
            if results.get('cpu'):
                frame, box = _make_frame(_('Processor'))
                cpu = results['cpu']
                lbl = Gtk.Label()
                lbl.set_markup(
                    f"<b>{_('Model:')}</b> {cpu.get('model', 'N/A')}\n"
                    f"<b>{_('Cores:')}</b> {cpu.get('cores', 0)}  "
                    f"<b>{_('Threads:')}</b> {cpu.get('threads', 0)}"
                )
                lbl.set_xalign(0)
                lbl.set_line_wrap(True)
                box.pack_start(lbl, False, False, 0)
                main_box.pack_start(frame, False, False, 0)

            # ── RAM ──
            if results.get('memory'):
                frame, box = _make_frame(_('RAM Memory'))
                mem = results['memory']
                lbl = Gtk.Label()
                lbl.set_markup(
                    f"<b>{_('Total:')}</b> {mem.get('total', '?')}  "
                    f"<b>{_('Available:')}</b> {mem.get('available', '?')}"
                )
                lbl.set_xalign(0)
                box.pack_start(lbl, False, False, 0)
                main_box.pack_start(frame, False, False, 0)

            # ── VM ──
            vm = results.get('vm_detection', {})
            if vm.get('is_vm'):
                frame, box = _make_frame(_("Virtual Machine"))
                lbl = Gtk.Label()
                lbl.set_markup(f"<b>{_('Type:')}</b> {vm.get('type', '?')}")
                lbl.set_xalign(0)
                box.pack_start(lbl, False, False, 0)

                required = vm.get('required_packages', [])
                if required:
                    pkgs_str = ' '.join(required)
                    rec_lbl = Gtk.Label()
                    rec_lbl.set_markup(f"<b>{_('Recommended tools:')}</b> {pkgs_str}")
                    rec_lbl.set_xalign(0)
                    box.pack_start(rec_lbl, False, False, 0)

                    def _install_vm(b, p=pkgs_str):
                        dialog.destroy()
                        self._on_driver_clicked(b, p)

                    def _uninstall_vm(b, p=pkgs_str):
                        dialog.destroy()
                        self._on_remove_driver_clicked(b, p)

                    _driver_action_buttons(
                        box,
                        vm.get('driver_status', 'missing'),
                        vm.get('missing_packages', []),
                        pkgs_str,
                        _install_vm,
                        _uninstall_vm
                    )
                main_box.pack_start(frame, False, False, 0)

            # ── GPUs ──
            for gpu in results.get('gpus', []):
                title = f"{_('Graphics Card')} — {gpu.get('vendor', '?')} {gpu.get('model', '')}"
                frame, box = _make_frame(title)

                type_lbl = Gtk.Label()
                type_lbl.set_markup(f"<b>{_('Type:')}</b> {gpu.get('type', '?')}")
                type_lbl.set_xalign(0)
                box.pack_start(type_lbl, False, False, 0)

                rec = gpu.get('recommended_driver')
                if rec:
                    rec_lbl = Gtk.Label()
                    rec_lbl.set_markup(f"<b>{_('Recommended driver:')}</b> {rec}")
                    rec_lbl.set_xalign(0)
                    box.pack_start(rec_lbl, False, False, 0)

                    def _install_gpu(b, driver=rec):
                        dialog.destroy()
                        self._on_install_recommended_driver(b, driver, dialog)

                    def _uninstall_gpu(b):
                        dialog.destroy()
                        self._on_uninstall_nvidia_clicked(b)

                    _driver_action_buttons(
                        box,
                        gpu.get('driver_status', 'missing'),
                        gpu.get('missing_packages', []),
                        rec,
                        _install_gpu,
                        _uninstall_gpu if gpu.get('vendor') == 'NVIDIA' else None
                    )
                main_box.pack_start(frame, False, False, 0)

            # ── Hybrid Graphics ──
            hybrid = results.get('hybrid_gpu', {})
            if hybrid.get('is_hybrid'):
                frame, box = _make_frame(_('Hybrid Graphics'))
                lbl = Gtk.Label()
                lbl.set_markup(
                    f"<b>{_('Integrated:')}</b> {hybrid.get('integrated', '?')}\n"
                    f"<b>{_('Dedicated:')}</b> {hybrid.get('dedicated', '?')}"
                )
                lbl.set_xalign(0)
                box.pack_start(lbl, False, False, 0)

                btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
                offload_btn = Gtk.Button(label=_("PRIME Render Offload"))
                offload_btn.set_tooltip_text(_("Use NVIDIA on demand (saves battery)"))
                offload_btn.connect("clicked", self._on_hybrid_clicked, "offload")
                offload_btn.connect("clicked", lambda x: dialog.destroy())
                btn_box.pack_start(offload_btn, True, True, 0)

                primary_btn = Gtk.Button(label=_("NVIDIA Primary"))
                primary_btn.set_tooltip_text(_("Always use NVIDIA (max performance)"))
                primary_btn.connect("clicked", self._on_hybrid_clicked, "nvidia")
                primary_btn.connect("clicked", lambda x: dialog.destroy())
                btn_box.pack_start(primary_btn, True, True, 0)

                box.pack_start(btn_box, False, False, 4)
                main_box.pack_start(frame, False, False, 0)

            # ── Wi-Fi ──
            wifi_list = results.get('wifi', [])
            if wifi_list:
                frame, box = _make_frame(_('Wi-Fi'))
                for adapter in wifi_list:
                    sep_lbl = Gtk.Label()
                    sep_lbl.set_markup(
                        f"<b>{adapter.get('vendor', '?')}</b> — {adapter.get('model', '')}"
                    )
                    sep_lbl.set_xalign(0)
                    sep_lbl.set_line_wrap(True)
                    box.pack_start(sep_lbl, False, False, 0)

                    pkg = adapter.get('firmware_package')
                    if pkg:
                        def _install_wifi(b, p=pkg):
                            dialog.destroy()
                            self._on_driver_clicked(b, p)

                        def _uninstall_wifi(b, p=pkg):
                            dialog.destroy()
                            self._on_remove_driver_clicked(b, p)

                        _driver_action_buttons(
                            box,
                            adapter.get('driver_status', 'missing'),
                            adapter.get('missing_packages', []),
                            pkg,
                            _install_wifi,
                            _uninstall_wifi
                        )
                main_box.pack_start(frame, False, False, 0)

            # ── Audio ──
            audio_list = results.get('audio', [])
            if audio_list:
                frame, box = _make_frame(_('Audio'))
                for device in audio_list:
                    dev_lbl = Gtk.Label()
                    dev_lbl.set_markup(f"• {device.get('model', '?')}")
                    dev_lbl.set_xalign(0)
                    dev_lbl.set_line_wrap(True)
                    box.pack_start(dev_lbl, False, False, 0)

                    pkgs = device.get('required_packages', [])
                    if pkgs:
                        pkgs_str = ' '.join(pkgs)

                        def _install_audio(b, p=pkgs_str):
                            dialog.destroy()
                            self._on_driver_clicked(b, p)

                        def _uninstall_audio(b, p=pkgs_str):
                            dialog.destroy()
                            self._on_remove_driver_clicked(b, p)

                        _driver_action_buttons(
                            box,
                            device.get('driver_status', 'missing'),
                            device.get('missing_packages', []),
                            pkgs_str,
                            _install_audio,
                            _uninstall_audio
                        )
                main_box.pack_start(frame, False, False, 0)

            # ── Bluetooth ──
            bt = results.get('bluetooth')
            if bt:
                frame, box = _make_frame(_('Bluetooth'))
                bt_lbl = Gtk.Label()
                bt_lbl.set_markup(f"• {bt.get('model', '?')}")
                bt_lbl.set_xalign(0)
                box.pack_start(bt_lbl, False, False, 0)

                pkgs = bt.get('required_packages', [])
                if pkgs:
                    pkgs_str = ' '.join(pkgs)

                    def _install_bt(b, p=pkgs_str):
                        dialog.destroy()
                        self._on_driver_clicked(b, p)

                    def _uninstall_bt(b, p=pkgs_str):
                        dialog.destroy()
                        self._on_remove_driver_clicked(b, p)

                    _driver_action_buttons(
                        box,
                        bt.get('driver_status', 'missing'),
                        bt.get('missing_packages', []),
                        pkgs_str,
                        _install_bt,
                        _uninstall_bt
                    )
                main_box.pack_start(frame, False, False, 0)

            # ── Printers ──
            pr = results.get('printers')
            if pr:
                frame, box = _make_frame(_('Printers'))
                pr_lbl = Gtk.Label()
                pr_lbl.set_markup(f"• {pr.get('model', '?')}")
                pr_lbl.set_xalign(0)
                box.pack_start(pr_lbl, False, False, 0)

                pkgs = pr.get('required_packages', [])
                if pkgs:
                    pkgs_str = ' '.join(pkgs)

                    def _install_pr(b, p=pkgs_str):
                        dialog.destroy()
                        self._on_driver_clicked(b, p)

                    def _uninstall_pr(b, p=pkgs_str):
                        dialog.destroy()
                        self._on_remove_driver_clicked(b, p)

                    _driver_action_buttons(
                        box,
                        pr.get('driver_status', 'missing'),
                        pr.get('missing_packages', []),
                        pkgs_str,
                        _install_pr,
                        _uninstall_pr
                    )
                main_box.pack_start(frame, False, False, 0)

            # ── Storage ──
            if results.get('storage'):
                frame, box = _make_frame(_('Storage'))
                for device in results['storage']:
                    lbl = Gtk.Label()
                    lbl.set_markup(f"• <b>{device.get('name', '?')}:</b> {device.get('size', '?')}")
                    lbl.set_xalign(0)
                    box.pack_start(lbl, False, False, 0)
                main_box.pack_start(frame, False, False, 0)

            # ── Network ──
            if results.get('network'):
                frame, box = _make_frame(_('Network'))
                for iface in results['network']:
                    text = f"• <b>{iface.get('name', '?')}:</b> {iface.get('type', '?')}"
                    if iface.get('status'):
                        text += f" — {iface['status']}"
                    lbl = Gtk.Label()
                    lbl.set_markup(text)
                    lbl.set_xalign(0)
                    box.pack_start(lbl, False, False, 0)
                main_box.pack_start(frame, False, False, 0)

            # ── Close button ──
            close_btn = Gtk.Button(label=_("Close"))
            close_btn.connect("clicked", lambda x: dialog.destroy())
            btn_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            btn_row.set_halign(Gtk.Align.END)
            btn_row.set_margin_top(8)
            btn_row.set_margin_bottom(10)
            btn_row.set_margin_end(10)
            btn_row.pack_start(close_btn, False, False, 0)
            dialog.get_content_area().pack_start(btn_row, False, False, 0)

            dialog.show_all()

        scan_hardware(update_status, update_progress, show_results)
    
    def _on_install_recommended_driver(self, button, driver, dialog):
        """Install recommended driver from hardware scan."""
        button.set_sensitive(False)
        dialog.destroy()

        cuda_drivers = {"nvidia-driver-580": "580", "nvidia-driver-590": "590", "nvidia-driver-610": "610"}
        legacy_drivers = {"nvidia-tesla-470-driver", "nvidia-legacy-390xx-driver", "nvidia-legacy-340xx-driver"}

        if driver in cuda_drivers:
            self._on_nvidia_cuda_repo_clicked(button, cuda_drivers[driver])
        elif driver == "nvidia-driver":
            self._on_nvidia_repo_clicked(button, "nvidia-driver")
        elif driver in legacy_drivers:
            self._on_legacy_nvidia_clicked(button, driver)
        elif driver == "nouveau":
            self._on_driver_clicked(button, "xserver-xorg-video-nouveau")
        else:
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

    def _on_uninstall_nvidia_clicked(self, button):
        """Remove all NVIDIA drivers and related packages."""
        confirm_dialog = Gtk.MessageDialog(
            transient_for=self.parent_window,
            flags=0,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.YES_NO,
            text=_("Uninstall NVIDIA Drivers")
        )
        confirm_dialog.format_secondary_text(
            _("This will completely remove all NVIDIA and CUDA packages from your system.\n\n"
              "This includes drivers, kernel modules, DKMS entries, CUDA libraries "
              "and NVIDIA repository sources.\n\n"
              "After removal you can install a different driver version.\n\n"
              "A system restart will be required.\n\n"
              "Do you want to continue?")
        )
        response = confirm_dialog.run()
        confirm_dialog.destroy()
        if response != Gtk.ResponseType.YES:
            return

        script = """#!/bin/bash

echo "=== Removing all NVIDIA drivers ==="
echo ""

echo "[0/7] Removing NVIDIA DKMS modules from all kernels..."
for entry in $(dkms status | grep -i nvidia | awk -F'[:,]' '{print $1"/"$2}' | tr -d ' '); do
    dkms remove --force "$entry" --all 2>/dev/null || true
done
for kver in $(ls /lib/modules/); do
    rm -f /lib/modules/$kver/updates/dkms/nvidia*.ko*
    rm -f /lib/modules/$kver/updates/dkms/nvidia-*.ko*
    depmod -a "$kver" 2>/dev/null || true
done
rm -rf /var/lib/dkms/nvidia*

echo "[1/7] Fixing any interrupted dpkg state..."
dpkg --configure -a 2>/dev/null || true

echo "[2/7] Removing NVIDIA and CUDA packages..."
NVIDIA_PKGS=$(dpkg -l | grep -iE '^[a-z]+[[:space:]]+(nvidia|libnvidia|cuda)' | awk '{print $2}' | tr '\n' ' ')
if [ -n "$NVIDIA_PKGS" ]; then
    echo "Packages to remove: $NVIDIA_PKGS"
    apt purge -y $NVIDIA_PKGS 2>/dev/null || dpkg --purge --force-depends $NVIDIA_PKGS
else
    echo "No NVIDIA/CUDA packages found."
fi
apt autoremove -y 2>/dev/null || true

echo "[3/7] Removing NVIDIA CUDA repository sources..."
rm -f /etc/apt/sources.list.d/cuda-*.list
rm -f /etc/apt/sources.list.d/nvidia*.list
rm -f /usr/share/keyrings/cuda-*.gpg
rm -f /usr/share/keyrings/nvidia*.gpg
apt update -q

echo "[4/7] Removing NVIDIA modprobe/dracut configuration..."
rm -f /etc/modprobe.d/blacklist-nouveau.conf
rm -f /etc/dracut.conf.d/nvidia.conf
rm -f /etc/dracut.conf.d/blacklist-nouveau.conf
rm -f /etc/apt/apt.conf.d/99nvidia-sha1-exception

echo "[5/7] Restoring GRUB defaults..."
sed -i 's/ nvidia-drm.modeset=1//' /etc/default/grub 2>/dev/null || true
update-grub 2>/dev/null || true

echo "[6/7] Regenerating initramfs..."
if command -v dracut >/dev/null 2>&1; then
    dracut --force
elif command -v update-initramfs >/dev/null 2>&1; then
    update-initramfs -u
fi

echo ""
echo "[7/7] Done."
echo "=== NVIDIA drivers removed completely ==="
echo "Restart the system before installing a new driver version."
"""
        self._run_script_as_root(script, "uninstall-nvidia.sh", self._refresh_driver_status)

    def _on_hybrid_clicked(self, button, mode):
        """Configure hybrid graphics."""
        if mode == "offload":
            de = self.environment_detector.desktop_environment.value
            script = f"""#!/bin/bash
set -e

DESKTOP_ENV="{de}"
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

# Generate kwinoutputconfig.json for KDE Plasma to fix wallpaper/icons loss on reboot
if [ "$DESKTOP_ENV" = "kde" ]; then
    echo "KDE Plasma detected - generating kwinoutputconfig.json..."

    INTEL_CONNECTOR=$(ls /sys/class/drm/ | grep -E "^card[0-9]+-eDP" | head -1 | sed 's/card[0-9]*-//')
    if [ -z "$INTEL_CONNECTOR" ]; then
        INTEL_CONNECTOR=$(ls /sys/class/drm/ | grep -E "^card[0-9]+-LVDS" | head -1 | sed 's/card[0-9]*-//')
    fi

    if [ -n "$INTEL_CONNECTOR" ]; then
        echo "Detected connector: $INTEL_CONNECTOR"
        REAL_USER=$(getent passwd $PKEXEC_UID | cut -d: -f1)
        REAL_HOME=$(getent passwd $PKEXEC_UID | cut -d: -f6)

        KWIN_CONFIG_DIR="$REAL_HOME/.config/kdedefaults"
        mkdir -p "$KWIN_CONFIG_DIR"

        cat > "$KWIN_CONFIG_DIR/kwinoutputconfig.json" << EOF
[
    {{
        "data": [{{"connectorName": "$INTEL_CONNECTOR"}}],
        "name": "outputs"
    }},
    {{
        "data": [
            {{
                "lidClosed": false,
                "outputs": [
                    {{
                        "enabled": true,
                        "outputIndex": 0,
                        "position": {{"x": 0, "y": 0}},
                        "priority": 0
                    }}
                ]
            }}
        ],
        "name": "setups"
    }}
]
EOF
        chown -R "$REAL_USER:$REAL_USER" "$KWIN_CONFIG_DIR" 2>/dev/null
        echo "kwinoutputconfig.json created for user $REAL_USER."
    else
        echo "No eDP/LVDS connector detected, skipping kwinoutputconfig.json."
    fi
fi

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
        # SDDM supports both X11 and Wayland sessions natively
        # User can choose at login screen — no additional config needed
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

# Ensure NVIDIA modules are included in initramfs
if command -v dracut >/dev/null 2>&1; then
    mkdir -p /etc/dracut.conf.d
    echo 'omit_drivers+=" nouveau "' > /etc/dracut.conf.d/blacklist-nouveau.conf
    echo 'add_drivers+=" nvidia nvidia_modeset nvidia_uvm nvidia_drm "' > /etc/dracut.conf.d/nvidia.conf
    echo "Regenerating initramfs with NVIDIA modules..."
    dracut --force
elif command -v update-initramfs >/dev/null 2>&1; then
    echo "Regenerating initramfs..."
    update-initramfs -u
fi

echo ""
echo "=== Configuration complete ==="
echo "NVIDIA configured as primary GPU for $DESKTOP_ENV."
echo ""
if [ "$DESKTOP_ENV" = "xfce" ]; then
    echo "Xfce uses X11 only."
else
    echo "Both X11 and Wayland sessions are available."
    if [[ "$DRIVER_VERSION" =~ ^[0-9]+$ ]] && [ "$DRIVER_VERSION" -ge 555 ]; then
        echo "Wayland: fully supported (driver $DRIVER_VERSION)."
    elif [[ "$DRIVER_VERSION" =~ ^[0-9]+$ ]] && [ "$DRIVER_VERSION" -ge 550 ]; then
        echo "WARNING: Driver 550 has known freezes with KDE Wayland."
        echo "Upgrade to 580 or 590 for a stable Wayland experience."
    else
        echo "WARNING: Could not detect driver version or version below 550."
        echo "Wayland stability not guaranteed. Use X11 session if issues arise."
    fi
fi
echo ""
echo "IMPORTANT: Restart the system to apply changes."
"""
            self._run_script_as_root(script, "configure-nvidia-primary.sh")
