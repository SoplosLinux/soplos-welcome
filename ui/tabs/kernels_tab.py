"""
Kernels tab for Soplos Welcome.
Handles kernel management and updates.
"""

import gi
import os
import subprocess
import logging
gi.require_version('Gtk', '3.0')
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gtk, GLib, GdkPixbuf

from core.i18n_manager import _
from config.paths import ICONS_DIR
from utils.command_runner import CommandRunner
from utils.hardware_detector import detect_gpu


class KernelsTab(Gtk.ScrolledWindow):
    """
    Kernel management tab.
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
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.main_box.set_margin_left(20)
        self.main_box.set_margin_right(20)
        self.main_box.set_margin_top(20)
        self.main_box.set_margin_bottom(20)
        
        self.add(self.main_box)
        
        # Containers for dynamic buttons
        self.liquorix_row = None
        self.xanmod_row = None
        self.current_kernel_info = None
        self.kernel_installer_row = None
        
        self._create_ui()
    
    def _create_ui(self):
        """Create the kernels tab interface."""
        # Header
        header = Gtk.Label()
        header.set_markup(f'<span size="20000" weight="bold">{_("Kernel Management")}</span>')
        header.set_halign(Gtk.Align.START)
        self.main_box.pack_start(header, False, False, 0)
        
        # Current kernel information
        current_kernel_frame = Gtk.Frame()
        current_kernel_frame.set_label(_("System Information"))
        current_kernel_frame.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        self.main_box.pack_start(current_kernel_frame, False, False, 5)
        
        current_kernel_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        current_kernel_box.set_border_width(10)
        current_kernel_frame.add(current_kernel_box)
        
        self.current_kernel_info = Gtk.Label()
        self.current_kernel_info.set_xalign(0)
        self.current_kernel_info.set_line_wrap(True)
        current_kernel_box.pack_start(self.current_kernel_info, False, False, 0)
        
        # Update kernel info
        self._update_kernel_info()
        
        # Separator
        self.main_box.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 10)

        # Broken repository notice (only visible when leftovers are found)
        self._create_repo_repair_section()

        # CPU Microcode section
        microcode_frame = Gtk.Frame()
        microcode_frame.set_label(_("CPU Microcode Updates"))
        microcode_frame.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        self.main_box.pack_start(microcode_frame, False, False, 5)
        
        microcode_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        microcode_container.set_border_width(10)
        microcode_frame.add(microcode_container)
        
        microcode_desc = Gtk.Label()
        microcode_desc.set_markup(f"<small>{_('Security and performance firmware updates for your CPU.')}</small>")
        microcode_desc.set_line_wrap(True)
        microcode_desc.set_xalign(0)
        microcode_container.pack_start(microcode_desc, False, False, 0)
        
        # Detect CPU vendor and show appropriate microcode
        self.microcode_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        microcode_container.pack_start(self.microcode_row, False, False, 5)

        # Separator
        self.main_box.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 5)

        # Frame for Soplos Kernel Installer
        ski_frame = Gtk.Frame()
        ski_frame.set_label(_("Soplos Kernel Installer"))
        ski_frame.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        self.main_box.pack_start(ski_frame, False, False, 5)

        ski_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        ski_row.set_border_width(10)
        ski_frame.add(ski_row)

        ski_icon_path = os.path.join(ICONS_DIR, "kernels", "org.soplos.kernel-installer.png")
        if os.path.exists(ski_icon_path):
            try:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(ski_icon_path, 48, 48, True)
                ski_icon = Gtk.Image.new_from_pixbuf(pixbuf)
                ski_row.pack_start(ski_icon, False, False, 0)
            except Exception:
                pass

        ski_info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        ski_row.pack_start(ski_info_box, True, True, 0)

        ski_name = Gtk.Label()
        ski_name.set_markup('<span weight="bold">Soplos Kernel Installer</span>')
        ski_name.set_halign(Gtk.Align.START)
        ski_info_box.pack_start(ski_name, False, False, 0)

        ski_desc = Gtk.Label(label=_("Graphical tool to manage and install kernels from the Soplos repository."))
        ski_desc.set_line_wrap(True)
        ski_desc.set_xalign(0)
        ski_info_box.pack_start(ski_desc, False, False, 0)

        self.kernel_installer_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        ski_row.pack_start(self.kernel_installer_row, False, False, 0)

        # Separator
        self.main_box.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 5)

        # Section for kernels
        kernel_label = Gtk.Label()
        kernel_label.set_markup(f"<b>{_('Available Kernels')}</b>")
        kernel_label.set_halign(Gtk.Align.START)
        self.main_box.pack_start(kernel_label, False, False, 5)

        kernel_desc_label = Gtk.Label(
            label=_("Manage your system kernels. You can install optimized kernels for better performance or latency.")
        )
        kernel_desc_label.set_line_wrap(True)
        kernel_desc_label.set_xalign(0)
        self.main_box.pack_start(kernel_desc_label, False, False, 5)

        # Frame for Liquorix
        liquorix_frame = Gtk.Frame()
        liquorix_frame.set_label(_("Liquorix Kernel"))
        liquorix_frame.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        self.main_box.pack_start(liquorix_frame, False, False, 5)
        
        liquorix_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        liquorix_container.set_border_width(10)
        liquorix_frame.add(liquorix_container)
        
        # Description of Liquorix
        liquorix_desc = Gtk.Label(label=_("Optimized for interactive systems and gaming. High responsiveness and low latency."))
        liquorix_desc.set_line_wrap(True)
        liquorix_desc.set_xalign(0)
        liquorix_container.pack_start(liquorix_desc, False, False, 0)
        
        # Row for Liquorix (dynamic)
        self.liquorix_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        liquorix_container.pack_start(self.liquorix_row, False, False, 5)
        
        # Frame for XanMod Kernels
        xanmod_frame = Gtk.Frame()
        xanmod_frame.set_label(_("XanMod Kernel Variants"))
        xanmod_frame.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        self.main_box.pack_start(xanmod_frame, False, False, 5)
        
        xanmod_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        xanmod_container.set_border_width(10)
        xanmod_frame.add(xanmod_container)
        
        # General description
        xanmod_general_desc = Gtk.Label()
        xanmod_general_desc.set_markup(f"<b>{_('High performance kernel with advanced optimizations.')}</b>\n{_('Choose the variant that matches your hardware:')}")
        xanmod_general_desc.set_line_wrap(True)
        xanmod_general_desc.set_xalign(0)
        xanmod_container.pack_start(xanmod_general_desc, False, False, 5)
        
        # Report which build this CPU can actually run
        psabi_level = self._get_cpu_psabi_level()
        if psabi_level >= 3:
            arch_text = _('Your CPU supports x86-64-v3 builds.')
        elif psabi_level == 2:
            arch_text = _('Your CPU supports x86-64-v2 only, so the v2 builds will be installed.')
        else:
            arch_text = _('Your CPU is below x86-64-v2. Only the LTS variant can run on it.')

        xanmod_arch_desc = Gtk.Label()
        xanmod_arch_desc.set_markup(f"<small>{arch_text}</small>")
        xanmod_arch_desc.set_line_wrap(True)
        xanmod_arch_desc.set_xalign(0)
        xanmod_container.pack_start(xanmod_arch_desc, False, False, 0)

        # Separator
        xanmod_container.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 5)

        # Variant 1: Standard (Recommended)
        xanmod_main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        xanmod_container.pack_start(xanmod_main_box, False, False, 5)

        xanmod_main_header = Gtk.Label()
        xanmod_main_header.set_markup(f"<b>{_('Standard')} <span color='#50fa7b'>({_('Recommended')})</span></b>")
        xanmod_main_header.set_xalign(0)
        xanmod_main_box.pack_start(xanmod_main_header, False, False, 0)

        xanmod_main_desc = Gtk.Label()
        xanmod_main_desc.set_markup(f"<small>{_('General purpose build. Balanced performance for everyday use.')}</small>")
        xanmod_main_desc.set_line_wrap(True)
        xanmod_main_desc.set_xalign(0)
        xanmod_main_box.pack_start(xanmod_main_desc, False, False, 0)

        self.xanmod_main_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        xanmod_main_box.pack_start(self.xanmod_main_row, False, False, 2)

        # Variant 2: RT (Real Time)
        xanmod_rt_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        xanmod_container.pack_start(xanmod_rt_box, False, False, 5)

        xanmod_rt_header = Gtk.Label()
        xanmod_rt_header.set_markup(f"<b>{_('RT - Real Time')}</b>")
        xanmod_rt_header.set_xalign(0)
        xanmod_rt_box.pack_start(xanmod_rt_header, False, False, 0)

        xanmod_rt_desc = Gtk.Label()
        xanmod_rt_desc.set_markup(f"<small>{_('PREEMPT_RT build. Minimal latency for audio production, streaming and competitive gaming.')}</small>")
        xanmod_rt_desc.set_line_wrap(True)
        xanmod_rt_desc.set_xalign(0)
        xanmod_rt_box.pack_start(xanmod_rt_desc, False, False, 0)

        self.xanmod_rt_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        xanmod_rt_box.pack_start(self.xanmod_rt_row, False, False, 2)

        # Variant 3: EDGE (Experimental)
        xanmod_edge_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        xanmod_container.pack_start(xanmod_edge_box, False, False, 5)
        
        xanmod_edge_header = Gtk.Label()
        xanmod_edge_header.set_markup(f"<b>{_('EDGE - Experimental')} <span color='#ffb86c'>({_('Not recommended for production')})</span></b>")
        xanmod_edge_header.set_xalign(0)
        xanmod_edge_box.pack_start(xanmod_edge_header, False, False, 0)
        
        xanmod_edge_desc = Gtk.Label()
        xanmod_edge_desc.set_markup(f"<small>{_('Latest experimental features. May be unstable. For testing only.')}</small>")
        xanmod_edge_desc.set_line_wrap(True)
        xanmod_edge_desc.set_xalign(0)
        xanmod_edge_box.pack_start(xanmod_edge_desc, False, False, 0)
        
        self.xanmod_edge_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        xanmod_edge_box.pack_start(self.xanmod_edge_row, False, False, 2)
        
        # Variant 4: LTS (Long Term Support)
        xanmod_lts_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        xanmod_container.pack_start(xanmod_lts_box, False, False, 5)
        
        xanmod_lts_header = Gtk.Label()
        xanmod_lts_header.set_markup(f"<b>{_('LTS - Long Term Support')} <span color='#50fa7b'>({_('Most stable')})</span></b>")
        xanmod_lts_header.set_xalign(0)
        xanmod_lts_box.pack_start(xanmod_lts_header, False, False, 0)
        
        xanmod_lts_desc = Gtk.Label()
        xanmod_lts_desc.set_markup(f"<small>{_('Long-term support, conservative updates. Best for stability.')}</small>")
        xanmod_lts_desc.set_line_wrap(True)
        xanmod_lts_desc.set_xalign(0)
        xanmod_lts_box.pack_start(xanmod_lts_desc, False, False, 0)
        
        self.xanmod_lts_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        xanmod_lts_box.pack_start(self.xanmod_lts_row, False, False, 2)
        
        # Separator
        self.main_box.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 10)

        # Frame for maintenance
        maintenance_frame = Gtk.Frame()
        maintenance_frame.set_label(_("System Maintenance"))
        maintenance_frame.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        self.main_box.pack_start(maintenance_frame, False, False, 5)
        
        maintenance_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        maintenance_container.set_border_width(10)
        maintenance_frame.add(maintenance_container)
        
        # Description of cleanup
        clean_desc = Gtk.Label(label=_("Tools to keep your system clean and updated."))
        clean_desc.set_line_wrap(True)
        clean_desc.set_xalign(0)
        maintenance_container.pack_start(clean_desc, False, False, 0)
        
        # Maintenance buttons
        maintenance_buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        maintenance_container.pack_start(maintenance_buttons, False, False, 5)
        
        # Button to clean old kernels
        clean_button = Gtk.Button(label=_("Clean Old Kernels"))
        clean_button.set_tooltip_text(_("Remove old unused kernels to free up space"))
        clean_button.connect("clicked", self.on_clean_kernels_clicked)
        maintenance_buttons.pack_start(clean_button, False, False, 0)
        
        # Button to update GRUB
        grub_button = Gtk.Button(label=_("Update GRUB"))
        grub_button.set_tooltip_text(_("Regenerate GRUB configuration file"))
        grub_button.connect("clicked", self.on_update_grub_clicked)
        maintenance_buttons.pack_start(grub_button, False, False, 0)
        
        # Update initial states
        self._update_kernel_buttons()
        
        self.show_all()

    def _has_broken_xanmod_repo(self):
        """Check for a XanMod repository still pointing at the retired suite."""
        try:
            with open('/etc/apt/sources.list.d/xanmod-release.list', 'r') as f:
                content = f.read()
        except Exception:
            return False

        for line in content.splitlines():
            if 'deb.xanmod.org' in line and 'releases' in line.split():
                return True
        return False

    def _create_repo_repair_section(self):
        """Create the container for the broken repository notice."""
        self._repo_repair_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.main_box.pack_start(self._repo_repair_box, False, False, 5)
        self._refresh_repo_repair_section()

    def _refresh_repo_repair_section(self):
        """Show the repair notice only while a broken repository is present."""
        for child in self._repo_repair_box.get_children():
            self._repo_repair_box.remove(child)

        if not self._has_broken_xanmod_repo():
            # set_no_show_all survives the show_all() call of the parent container
            self._repo_repair_box.set_no_show_all(True)
            self._repo_repair_box.hide()
            return

        self._repo_repair_box.set_no_show_all(False)

        warning = Gtk.Label()
        warning.set_markup(
            f"<span color='#ffb86c' weight='bold'>{_('Broken XanMod repository detected')}</span>\n"
            f"<small>{_('A previous version added a XanMod repository that no longer exists, and it makes every system update fail. Repairing removes it, and you can install XanMod again afterwards.')}</small>"
        )
        warning.set_line_wrap(True)
        warning.set_xalign(0)
        self._repo_repair_box.pack_start(warning, False, False, 0)

        repair_btn = Gtk.Button(label=_("Repair repository"))
        repair_btn.get_style_context().add_class("suggested-action")
        repair_btn.set_halign(Gtk.Align.START)
        repair_btn.connect("clicked", self._on_repair_xanmod_repo_clicked)
        self._repo_repair_box.pack_start(repair_btn, False, False, 0)

        self._repo_repair_box.show_all()

    def _on_repair_xanmod_repo_clicked(self, widget):
        """Remove the broken XanMod repository left behind by earlier versions."""
        script_content = """#!/bin/bash
echo "=== Repairing XanMod repository ==="
pkexec bash -c '
rm -f /etc/apt/sources.list.d/xanmod-release.list
rm -f /etc/apt/keyrings/xanmod-archive-keyring.gpg
apt update -q || true
'
echo "[+] Broken repository removed."
"""
        script_path = "/tmp/repair-xanmod-repo.sh"
        with open(script_path, "w") as f:
            f.write(script_content)
        os.chmod(script_path, 0o755)
        self.command_runner.run_command(script_path, self._on_repo_repair_complete)

    def _on_repo_repair_complete(self, success=True):
        """Refresh the notice once the repair finished."""
        GLib.timeout_add(1000, self._refresh_repo_repair_section)

    def _get_current_kernel_info(self):
        """Obtain detailed information about the current kernel"""
        try:
            # Current kernel
            current_kernel = subprocess.check_output(['uname', '-r']).decode().strip()
            
            # Kernel type
            kernel_type = _("Standard Kernel")
            if 'liquorix' in current_kernel:
                kernel_type = _("Liquorix Kernel")
            elif 'xanmod' in current_kernel:
                kernel_type = _("XanMod Kernel")
            
            # Architecture
            arch = subprocess.check_output(['uname', '-m']).decode().strip()
            
            # Uptime
            try:
                uptime_output = subprocess.check_output(['uptime', '-p']).decode().strip()
                uptime = uptime_output.replace('up ', '')
            except:
                uptime = _("Unknown")
            
            return {
                'kernel': current_kernel,
                'type': kernel_type,
                'arch': arch,
                'uptime': self._format_uptime_localized(uptime)
            }
        except Exception as e:
            logging.error(f"Error obtaining kernel information: {e}")
            return {
                'kernel': _("Not detected"),
                'type': _("Unknown"),
                'arch': _("Not detected"),
                'uptime': _("Unknown")
            }

    def _format_uptime_localized(self, uptime_str):
        """Format uptime string to be localized"""
        # uptime -p returns strings like "up 2 hours, 30 minutes"
        # We need to parse numbers and translate text
        try:
            # Remove "up " prefix
            clean_str = uptime_str.replace("up ", "").strip()
            parts = clean_str.split(", ")
            localized_parts = []
            
            for part in parts:
                if "week" in part:
                    num = part.split()[0]
                    localized_parts.append(f"{num} {_('weeks')}")
                elif "day" in part:
                    num = part.split()[0]
                    localized_parts.append(f"{num} {_('days')}")
                elif "hour" in part:
                    num = part.split()[0]
                    localized_parts.append(f"{num} {_('hours')}")
                elif "minute" in part:
                    num = part.split()[0]
                    localized_parts.append(f"{num} {_('minutes')}")
            
            return ", ".join(localized_parts)
        except Exception:
            return uptime_str

    def _update_kernel_info(self):
        """Update the information of the current kernel"""
        info = self._get_current_kernel_info()
        info_text = (
            f"<b>{_('Current Kernel')}:</b> {info['kernel']}\n"
            f"<b>{_('Type')}:</b> {info['type']}\n"
            f"<b>{_('Architecture')}:</b> {info['arch']}\n"
            f"<b>{_('Uptime')}:</b> {info['uptime']}"
        )
        self.current_kernel_info.set_markup(info_text)

    def _detect_cpu_vendor(self):
        """Detect CPU vendor (Intel or AMD)"""
        try:
            with open('/proc/cpuinfo', 'r') as f:
                cpuinfo = f.read()
            
            if 'GenuineIntel' in cpuinfo:
                return 'intel'
            elif 'AuthenticAMD' in cpuinfo:
                return 'amd'
            else:
                return None
        except Exception as e:
            logging.error(f"Error detecting CPU vendor: {e}")
            return None

    def _get_cpu_psabi_level(self):
        """Return the highest x86-64 psABI level this CPU supports (1 to 4)."""
        try:
            flags = set()
            with open('/proc/cpuinfo', 'r') as f:
                for line in f:
                    if line.startswith('flags'):
                        flags = set(line.split(':', 1)[1].split())
                        break
        except Exception as e:
            logging.error(f"Error detecting CPU psABI level: {e}")
            return 1

        if not flags:
            return 1

        v2 = {'cx16', 'lahf_lm', 'popcnt', 'sse4_1', 'sse4_2', 'ssse3'}
        v3 = {'avx', 'avx2', 'bmi1', 'bmi2', 'f16c', 'fma', 'abm', 'movbe', 'xsave'}
        v4 = {'avx512f', 'avx512bw', 'avx512cd', 'avx512dq', 'avx512vl'}

        if not v2.issubset(flags):
            return 1
        if not v3.issubset(flags):
            return 2
        if not v4.issubset(flags):
            return 3
        return 4

    def _get_xanmod_package(self, kernel_type):
        """Resolve the XanMod package for a variant, honouring the CPU psABI level.

        XanMod publishes x64v2 and x64v3 for every branch, plus x64v1 for LTS.
        The x64v4 builds were dropped upstream, so v3 is the ceiling.
        Returns None when the CPU cannot run any build of that variant.
        """
        tier = min(self._get_cpu_psabi_level(), 3)

        if kernel_type == "xanmod-lts":
            return f"linux-xanmod-lts-x64v{tier}"

        if tier < 2:
            # Only the LTS branch ships a v1 build
            return None

        prefixes = {
            "xanmod-main": "linux-xanmod",
            "xanmod-rt": "linux-xanmod-rt",
            "xanmod-edge": "linux-xanmod-edge",
        }
        prefix = prefixes.get(kernel_type)
        if not prefix:
            return None
        return f"{prefix}-x64v{tier}"

    def _is_microcode_installed(self, vendor):
        """Check if microcode is installed"""
        try:
            if vendor == 'intel':
                result = subprocess.run(['dpkg', '-l', 'intel-microcode'], 
                                      capture_output=True, text=True)
                return result.returncode == 0
            elif vendor == 'amd':
                result = subprocess.run(['dpkg', '-l', 'amd64-microcode'], 
                                      capture_output=True, text=True)
                return result.returncode == 0
        except Exception as e:
            logging.error(f"Error checking microcode: {e}")
            return False
        return False

    def _is_kernel_installed(self, kernel_type):
        """Check if a specific kernel is installed"""
        try:
            if kernel_type == "liquorix":
                result = subprocess.run(['dpkg', '-l', 'linux-image-liquorix-amd64'],
                                      capture_output=True, text=True)
                return result.returncode == 0

            # XanMod package names depend on the psABI level of this CPU
            package = self._get_xanmod_package(kernel_type)
            if not package:
                return False
            return self._is_package_installed(package)
        except Exception as e:
            logging.error(f"Error checking kernel {kernel_type}: {e}")
            return False
        return False

    def _is_kernel_in_use(self, kernel_type):
        """Check if a kernel is currently in use"""
        try:
            current_kernel = subprocess.check_output(['uname', '-r']).decode().strip()
            if kernel_type == "liquorix":
                return 'liquorix' in current_kernel
            elif kernel_type.startswith("xanmod"):
                return 'xanmod' in current_kernel
        except:
            return False
        return False

    def _update_kernel_buttons(self):
        """Update the buttons according to the installation status of the kernels"""
        # Clear existing rows
        self._clear_container(self.microcode_row)
        self._clear_container(self.liquorix_row)
        self._clear_container(self.xanmod_main_row)
        self._clear_container(self.xanmod_rt_row)
        self._clear_container(self.xanmod_edge_row)
        self._clear_container(self.xanmod_lts_row)
        self._clear_container(self.kernel_installer_row)
        
        # Check for NVIDIA GPU
        gpu_info = detect_gpu()
        is_nvidia = gpu_info.get('vendor') == 'NVIDIA'
        
        # Update Microcode button
        self._update_microcode_button()
        
        # Update Liquorix button
        if self._is_kernel_installed("liquorix"):
            uninstall_button = Gtk.Button(label=_("Uninstall Liquorix"))
            uninstall_button.get_style_context().add_class("destructive-action")
            uninstall_button.connect("clicked", self.on_uninstall_liquorix_clicked)
            self.liquorix_row.pack_start(uninstall_button, False, False, 0)
            # Status label
            if self._is_kernel_in_use("liquorix"):
                status_label = Gtk.Label(label=_("In Use"))
                status_label.get_style_context().add_class("success")
            else:
                status_label = Gtk.Label(label=_("Installed"))
            self.liquorix_row.pack_start(status_label, False, False, 10)
        else:
            install_button = Gtk.Button(label=_("Install Liquorix"))
            install_button.get_style_context().add_class("suggested-action")
            
            if is_nvidia:
                install_button.set_sensitive(False)
                install_button.set_tooltip_text(_("Liquorix is not compatible with NVIDIA drivers"))
                
                warning_label = Gtk.Label()
                warning_label.set_markup(f"<span color='#ff5555' size='small'>{_('Incompatible with NVIDIA')}</span>")
                self.liquorix_row.pack_start(install_button, False, False, 0)
                self.liquorix_row.pack_start(warning_label, False, False, 10)
            else:
                install_button.connect("clicked", self.on_install_liquorix_clicked)
                self.liquorix_row.pack_start(install_button, False, False, 0)
        
        # Update XanMod Standard button
        self._update_xanmod_variant_button("xanmod-main", self.xanmod_main_row)

        # Update XanMod RT button
        self._update_xanmod_variant_button("xanmod-rt", self.xanmod_rt_row)

        # Update XanMod EDGE button
        self._update_xanmod_variant_button("xanmod-edge", self.xanmod_edge_row)

        # Update XanMod LTS button
        self._update_xanmod_variant_button("xanmod-lts", self.xanmod_lts_row)

        # Update Soplos Kernel Installer button
        self._update_kernel_installer_button()

        # Show new buttons
        self.microcode_row.show_all()
        self.liquorix_row.show_all()
        self.xanmod_main_row.show_all()
        self.xanmod_rt_row.show_all()
        self.xanmod_edge_row.show_all()
        self.xanmod_lts_row.show_all()
        self.kernel_installer_row.show_all()

    def _update_microcode_button(self):
        """Update microcode button based on CPU vendor"""
        cpu_vendor = self._detect_cpu_vendor()
        
        if not cpu_vendor:
            # Unknown CPU, show message
            no_cpu_label = Gtk.Label()
            no_cpu_label.set_markup(f"<i>{_('CPU vendor not detected')}</i>")
            self.microcode_row.pack_start(no_cpu_label, False, False, 0)
            return
        
        vendor_name = "Intel" if cpu_vendor == "intel" else "AMD"
        
        if self._is_microcode_installed(cpu_vendor):
            status_label = Gtk.Label()
            status_label.set_markup(f"<b>{vendor_name} Microcode</b>")
            status_label.set_xalign(0)
            self.microcode_row.pack_start(status_label, False, False, 0)
            
            installed_label = Gtk.Label(label=_("Installed"))
            installed_label.get_style_context().add_class("success")
            self.microcode_row.pack_start(installed_label, False, False, 10)
            
            uninstall_button = Gtk.Button(label=_("Uninstall"))
            uninstall_button.get_style_context().add_class("destructive-action")
            uninstall_button.connect("clicked", lambda w: self.on_uninstall_microcode_clicked(w, cpu_vendor))
            self.microcode_row.pack_start(uninstall_button, False, False, 0)
        else:
            status_label = Gtk.Label()
            status_label.set_markup(f"<b>{vendor_name} Microcode</b>")
            status_label.set_xalign(0)
            self.microcode_row.pack_start(status_label, False, False, 0)
            
            install_button = Gtk.Button(label=_("Install"))
            install_button.get_style_context().add_class("suggested-action")
            install_button.connect("clicked", lambda w: self.on_install_microcode_clicked(w, cpu_vendor))
            self.microcode_row.pack_start(install_button, False, False, 0)

    def _update_xanmod_variant_button(self, kernel_type, row):
        """Update button for a specific XanMod variant"""
        package = self._get_xanmod_package(kernel_type)

        if not package:
            # Installing a build the CPU cannot execute leaves an unbootable system,
            # so the option is blocked instead of merely warned about
            blocked_button = Gtk.Button(label=_("Install"))
            blocked_button.set_sensitive(False)
            blocked_button.set_tooltip_text(_("This variant requires x86-64-v2 or higher"))
            row.pack_start(blocked_button, False, False, 0)

            reason_label = Gtk.Label()
            reason_label.set_markup(f"<span color='#ff5555' size='small'>{_('Not compatible with your CPU')}</span>")
            row.pack_start(reason_label, False, False, 10)
            return

        if self._is_kernel_installed(kernel_type):
            uninstall_button = Gtk.Button(label=_("Uninstall"))
            uninstall_button.get_style_context().add_class("destructive-action")
            uninstall_button.connect("clicked", lambda w: self.on_uninstall_xanmod_clicked(w, kernel_type))
            row.pack_start(uninstall_button, False, False, 0)
            
            # Status label
            if self._is_kernel_in_use(kernel_type):
                status_label = Gtk.Label(label=_("In Use"))
                status_label.get_style_context().add_class("success")
            else:
                status_label = Gtk.Label(label=_("Installed"))
            row.pack_start(status_label, False, False, 10)
        else:
            install_button = Gtk.Button(label=_("Install"))
            install_button.get_style_context().add_class("suggested-action")
            install_button.set_tooltip_text(package)
            install_button.connect("clicked", lambda w: self.on_install_xanmod_clicked(w, kernel_type))
            row.pack_start(install_button, False, False, 0)

    def _is_package_installed(self, package):
        """Check if a dpkg package is installed"""
        try:
            result = subprocess.run(['dpkg', '-s', package], capture_output=True, text=True)
            return result.returncode == 0 and 'Status: install ok installed' in result.stdout
        except Exception:
            return False

    def _update_kernel_installer_button(self):
        """Update Soplos Kernel Installer button based on installation status"""
        if self._is_package_installed('soplos-kernel-installer'):
            uninstall_btn = Gtk.Button(label=_("Uninstall"))
            uninstall_btn.connect('clicked', lambda w: self._on_uninstall_kernel_installer())
            self.kernel_installer_row.pack_start(uninstall_btn, False, False, 0)

            installed_label = Gtk.Label(label=_("Installed"))
            installed_label.get_style_context().add_class("success")
            self.kernel_installer_row.pack_start(installed_label, False, False, 10)

            open_btn = Gtk.Button(label=_("Open Soplos Kernel Installer"))
            open_btn.connect('clicked', lambda w: self._on_open_kernel_installer())
            self.kernel_installer_row.pack_start(open_btn, False, False, 0)
        else:
            install_btn = Gtk.Button(label=_("Install"))
            install_btn.connect('clicked', lambda w: self._on_install_kernel_installer())
            self.kernel_installer_row.pack_start(install_btn, False, False, 0)

    def _on_install_kernel_installer(self):
        """Install soplos-kernel-installer via apt"""
        script_content = f"""#!/bin/bash
echo "{_('Installing Soplos Kernel Installer...')}"
pkexec apt install -y soplos-kernel-installer
echo "{_('Installation complete.')}"
"""
        script_path = "/tmp/install-soplos-kernel-installer.sh"
        with open(script_path, "w") as f:
            f.write(script_content)
        import os
        os.chmod(script_path, 0o755)
        self.command_runner.run_command(
            f"bash {script_path}",
            on_complete=self._on_operation_complete
        )

    def _on_uninstall_kernel_installer(self):
        """Uninstall soplos-kernel-installer via apt"""
        script_content = f"""#!/bin/bash
echo "{_('Uninstalling Soplos Kernel Installer...')}"
pkexec apt remove -y soplos-kernel-installer
echo "{_('Uninstallation complete.')}"
"""
        script_path = "/tmp/uninstall-soplos-kernel-installer.sh"
        with open(script_path, "w") as f:
            f.write(script_content)
        import os
        os.chmod(script_path, 0o755)
        self.command_runner.run_command(
            f"bash {script_path}",
            on_complete=self._on_operation_complete
        )

    def _on_open_kernel_installer(self):
        """Launch Soplos Kernel Installer"""
        try:
            subprocess.Popen(['soplos-kernel-installer'])
        except Exception as e:
            print(f"Error launching soplos-kernel-installer: {e}")

    def _clear_container(self, container):
        """Clear all widgets from a container"""
        for child in container.get_children():
            container.remove(child)

    def _on_operation_complete(self, success=True):
        """Callback that is executed after an installation/uninstallation operation"""
        # Update kernel information and buttons
        self._update_kernel_info()
        GLib.timeout_add(1000, self._update_kernel_buttons)

    def on_install_liquorix_clicked(self, widget):
        # The installer is downloaded first: piping curl straight into a root shell
        # feeds an HTTP error page to bash and still reports success
        script_content = f"""#!/bin/bash
echo "{_('Installing Liquorix Kernel...')}"
INSTALLER=$(mktemp /tmp/liquorix-upstream.XXXXXX.sh)
if ! curl -fsSL https://liquorix.net/install-liquorix.sh -o "$INSTALLER"; then
    rm -f "$INSTALLER"
    echo "{_('Could not download the Liquorix installer. Check your internet connection.')}"
    exit 1
fi
pkexec bash "$INSTALLER"
STATUS=$?
rm -f "$INSTALLER"
if [ $STATUS -ne 0 ]; then
    echo "{_('Installation failed.')}"
    exit $STATUS
fi
echo "{_('Installation complete.')}"
"""
        script_path = "/tmp/install-liquorix.sh"
        with open(script_path, "w") as f:
            f.write(script_content)
        os.chmod(script_path, 0o755)
        self.command_runner.run_command(script_path, self._on_operation_complete)

    def on_install_xanmod_clicked(self, widget, kernel_type):
        """Install specific XanMod variant"""
        package = self._get_xanmod_package(kernel_type)
        if not package:
            self._show_info_dialog(
                _("Not compatible"),
                _("Your CPU does not meet the requirements of this XanMod variant.")
            )
            return

        variant_name = kernel_type.replace("xanmod-", "").upper()

        script_content = f"""#!/bin/bash
echo "{_('Installing XanMod')} {variant_name}..."
pkexec bash -c '
set -eo pipefail
mkdir -p /etc/apt/keyrings
# Earlier versions wrote the retired "releases" suite, which fails on every
# apt update. Reinstalling must repair that state.
rm -f /etc/apt/sources.list.d/xanmod-release.list
wget -qO - https://dl.xanmod.org/archive.key | gpg --batch --yes --dearmor -o /etc/apt/keyrings/xanmod-archive-keyring.gpg
# XanMod publishes one suite per Debian codename. Soplos declares its own
# VERSION_CODENAME in /etc/os-release, so the codename is taken from the
# Debian repositories actually configured on the system.
CODENAME=$(apt-cache policy | grep o=Debian | grep -o "n=[a-z]*" | cut -d= -f2 | sort | uniq -c | sort -rn | head -1 | tr -dc "a-z") || true
case "$CODENAME" in
    bookworm|trixie|forky|sid) ;;
    *)
        echo "Could not determine the Debian codename of this system."
        echo "XanMod publishes one suite per Debian codename, so the repository cannot be configured."
        exit 1
        ;;
esac
echo "deb [signed-by=/etc/apt/keyrings/xanmod-archive-keyring.gpg] http://deb.xanmod.org $CODENAME main" > /etc/apt/sources.list.d/xanmod-release.list
apt update
apt install -y {package}
'
echo "{_('Installation complete.')}"
"""
        script_path = f"/tmp/install-xanmod-{kernel_type}.sh"
        with open(script_path, "w") as f:
            f.write(script_content)
        os.chmod(script_path, 0o755)
        self.command_runner.run_command(script_path, self._on_operation_complete)

    def on_uninstall_liquorix_clicked(self, widget):
        if self._is_kernel_in_use("liquorix"):
            self._show_in_use_warning("Liquorix")
            return
        
        script_content = f"""#!/bin/bash
echo "{_('Uninstalling Liquorix Kernel...')}"
pkexec bash -c '
apt remove -y linux-image-liquorix-amd64 linux-headers-liquorix-amd64
rm -f /etc/apt/sources.list.d/liquorix.list
rm -f /etc/apt/keyrings/liquorix-keyring.gpg
apt update -q || true
'
echo "{_('Uninstallation complete.')}"
"""
        script_path = "/tmp/uninstall-liquorix.sh"
        with open(script_path, "w") as f:
            f.write(script_content)
        os.chmod(script_path, 0o755)
        self.command_runner.run_command(script_path, self._on_operation_complete)

    def on_uninstall_xanmod_clicked(self, widget, kernel_type):
        """Uninstall specific XanMod variant"""
        if self._is_kernel_in_use(kernel_type):
            variant_name = kernel_type.replace("xanmod-", "").upper()
            self._show_in_use_warning(f"XanMod {variant_name}")
            return
        
        package = self._get_xanmod_package(kernel_type)
        if not package:
            return

        variant_name = kernel_type.replace("xanmod-", "").upper()

        script_content = f"""#!/bin/bash
echo "{_('Uninstalling XanMod')} {variant_name}..."
pkexec apt remove -y {package}
echo "{_('Uninstallation complete.')}"
"""
        script_path = f"/tmp/uninstall-xanmod-{kernel_type}.sh"
        with open(script_path, "w") as f:
            f.write(script_content)
        os.chmod(script_path, 0o755)
        self.command_runner.run_command(script_path, self._on_operation_complete)

    def _show_in_use_warning(self, kernel_name):
        dialog = Gtk.MessageDialog(
            transient_for=self.parent_window,
            flags=0,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.OK,
            text=_("Kernel in Use")
        )
        dialog.format_secondary_text(
            _("Cannot uninstall {0} because it is currently running. Please boot into another kernel first.").format(kernel_name)
        )
        dialog.run()
        dialog.destroy()

    def on_clean_kernels_clicked(self, widget):
        """Clean old kernels, keeping the running kernel and the latest of each type (Debian, Soplos, Liquorix, XanMod)."""
        try:
            # Get current running kernel
            current_kernel = subprocess.check_output(['uname', '-r']).decode().strip()
            
            # Get all installed kernel image packages
            result = subprocess.run(
                ['dpkg', '-l', 'linux-image-*'],
                capture_output=True, text=True
            )
            
            # Parse installed kernels (ignore meta-packages)
            meta_patterns = ['linux-image-amd64', 'linux-image-liquorix-amd64', 'linux-image-xanmod', 'linux-image-686']
            installed = []
            for line in result.stdout.splitlines():
                if line.startswith('ii') and 'linux-image-' in line:
                    pkg = line.split()[1]
                    if any(pattern in pkg for pattern in meta_patterns) and not any(char.isdigit() for char in pkg):
                        continue
                    installed.append(pkg)
            
            if not installed:
                self._show_info_dialog(_("No kernels found"), _("Could not find any installed kernel packages."))
                return
            
            # Helper for version sorting (Debian standard)
            def version_sort(pkgs):
                if not pkgs:
                    return []
                try:
                    res = subprocess.run(['sort', '-V'], input="\n".join(pkgs), capture_output=True, text=True)
                    return res.stdout.splitlines()
                except:
                    return sorted(pkgs)
            
            # Classify and sort kernels by type. Soplos kernels are their own family:
            # lumping them with Debian's keeps only the highest version of the two
            # and silently removes the other branch as a fallback.
            def _family(pkg, *tags):
                return any(tag in pkg for tag in tags)

            base_kernels = version_sort([p for p in installed if not _family(p, 'liquorix', 'xanmod', 'soplos')])
            soplos_kernels = version_sort([p for p in installed if 'soplos' in p])
            liquorix_kernels = version_sort([p for p in installed if 'liquorix' in p])
            xanmod_kernels = version_sort([p for p in installed if 'xanmod' in p])
            
            # Determine which to keep
            keep = set()
            
            # 1. Always keep the running kernel
            for pkg in installed:
                if current_kernel in pkg:
                    keep.add(pkg)
            
            # 2. Keep the latest of each branch
            if base_kernels:
                keep.add(base_kernels[-1])
            if soplos_kernels:
                keep.add(soplos_kernels[-1])
            if liquorix_kernels:
                keep.add(liquorix_kernels[-1])
            if xanmod_kernels:
                keep.add(xanmod_kernels[-1])
            
            # Determine which to remove
            to_remove = [pkg for pkg in installed if pkg not in keep]
            
            if not to_remove:
                self._show_info_dialog(
                    _("System is clean"),
                    _("No old kernels to remove. Your system is already clean.")
                )
                return
            
            # Find matching headers packages to purge them as well
            headers_to_remove = []
            for pkg in to_remove:
                header_pkg = pkg.replace('linux-image-', 'linux-headers-')
                check = subprocess.run(['dpkg', '-l', header_pkg], capture_output=True, text=True)
                if check.returncode == 0 and 'ii' in check.stdout:
                    headers_to_remove.append(header_pkg)
            
            all_to_remove = to_remove + headers_to_remove
            
            # Show confirmation dialog
            dialog = Gtk.MessageDialog(
                transient_for=self.parent_window,
                flags=0,
                message_type=Gtk.MessageType.QUESTION,
                buttons=Gtk.ButtonsType.YES_NO,
                text=_("Clean Old Kernels")
            )
            
            keep_text = "\n".join(f"  \u2713 {pkg}" for pkg in sorted(keep))
            remove_text = "\n".join(f"  \u2717 {pkg}" for pkg in sorted(all_to_remove))
            
            dialog.format_secondary_text(
                f"{_('Current kernel')}: {current_kernel}\n\n"
                f"{_('Kernels to keep')}:\n{keep_text}\n\n"
                f"{_('Packages to purge')} ({len(all_to_remove)}):\n{remove_text}\n\n"
                f"{_('This will remove binaries, headers and configuration files.')}\n"
                f"{_('Continue?')}"
            )
            
            response = dialog.run()
            dialog.destroy()
            
            if response != Gtk.ResponseType.YES:
                return
            
            # Build removal script (Purge + Autoremove + Update GRUB)
            packages_str = " ".join(all_to_remove)
            script_content = (
                "#!/bin/bash\n"
                "set -e\n"
                f"echo \"{_('Purging old kernels and headers...')}\"\n"
                f"apt purge -y {packages_str}\n"
                "apt autoremove --purge -y\n"
                f"echo \"{_('Updating GRUB...')}\"\n"
                "update-grub\n"
                f"echo \"{_('Cleanup complete.')}\"\n"
            )
            script_path = "/tmp/clean-kernels.sh"
            with open(script_path, "w") as f:
                f.write(script_content)
            os.chmod(script_path, 0o755)
            self.command_runner.run_command(f"pkexec bash {script_path}", self._on_operation_complete)
            
        except Exception as e:
            self._show_info_dialog(_("Error"), str(e))
    
    def _show_info_dialog(self, title, message):
        """Show a simple info dialog."""
        dialog = Gtk.MessageDialog(
            transient_for=self.parent_window,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=title
        )
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()

    def on_update_grub_clicked(self, widget):
        script_content = f"""#!/bin/bash
echo "{_('Updating GRUB...')}"
if [ -x /usr/sbin/update-grub ]; then
    pkexec /usr/sbin/update-grub
else
    pkexec update-grub
fi
echo "{_('GRUB update complete.')}"
"""
        script_path = "/tmp/update-grub.sh"
        with open(script_path, "w") as f:
            f.write(script_content)
        os.chmod(script_path, 0o755)
        self.command_runner.run_command(script_path)

    def on_install_microcode_clicked(self, widget, vendor):
        """Install CPU microcode"""
        package = "intel-microcode" if vendor == "intel" else "amd64-microcode"
        vendor_name = "Intel" if vendor == "intel" else "AMD"
        
        script_content = f"""#!/bin/bash
echo "{_('Installing')} {vendor_name} Microcode..."
pkexec apt update
pkexec apt install -y {package}
echo "{_('Installation complete.')}"
echo "{_('A system reboot is recommended to apply microcode updates.')}"
"""
        script_path = f"/tmp/install-microcode-{vendor}.sh"
        with open(script_path, "w") as f:
            f.write(script_content)
        os.chmod(script_path, 0o755)
        self.command_runner.run_command(script_path, self._on_operation_complete)

    def on_uninstall_microcode_clicked(self, widget, vendor):
        """Uninstall CPU microcode"""
        package = "intel-microcode" if vendor == "intel" else "amd64-microcode"
        vendor_name = "Intel" if vendor == "intel" else "AMD"
        
        script_content = f"""#!/bin/bash
echo "{_('Uninstalling')} {vendor_name} Microcode..."
pkexec apt remove -y {package}
echo "{_('Uninstallation complete.')}"
"""
        script_path = f"/tmp/uninstall-microcode-{vendor}.sh"
        with open(script_path, "w") as f:
            f.write(script_content)
        os.chmod(script_path, 0o755)
        self.command_runner.run_command(script_path, self._on_operation_complete)

