"""
Kernels tab for Soplos Welcome.
Handles kernel management and updates.
"""

import gi
import os
import subprocess
import logging
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

from core.i18n_manager import _
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
        
        # NVIDIA compatibility warning
        compat_label = Gtk.Label()
        compat_label.set_markup(f"<span color='#ff5555' weight='bold'>{_('Warning: Liquorix kernel is NOT compatible with proprietary NVIDIA drivers.')}</span>")
        compat_label.set_line_wrap(True)
        compat_label.set_xalign(0)
        self.main_box.pack_start(compat_label, False, False, 5)

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
        
        # Separator
        xanmod_container.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 5)
        
        # Variant 1: x64v3 (Standard - Recommended)
        xanmod_v3_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        xanmod_container.pack_start(xanmod_v3_box, False, False, 5)
        
        xanmod_v3_header = Gtk.Label()
        xanmod_v3_header.set_markup(f"<b>{_('x64v3 - Standard')} <span color='#50fa7b'>({_('Recommended')})</span></b>")
        xanmod_v3_header.set_xalign(0)
        xanmod_v3_box.pack_start(xanmod_v3_header, False, False, 0)
        
        xanmod_v3_desc = Gtk.Label()
        xanmod_v3_desc.set_markup(f"<small>{_('For CPUs from 2015+ (Intel Haswell, AMD Zen and newer). AVX2 optimizations.')}</small>")
        xanmod_v3_desc.set_line_wrap(True)
        xanmod_v3_desc.set_xalign(0)
        xanmod_v3_box.pack_start(xanmod_v3_desc, False, False, 0)
        
        self.xanmod_v3_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        xanmod_v3_box.pack_start(self.xanmod_v3_row, False, False, 2)
        
        # Variant 2: x64v4 (Advanced)
        xanmod_v4_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        xanmod_container.pack_start(xanmod_v4_box, False, False, 5)
        
        xanmod_v4_header = Gtk.Label()
        xanmod_v4_header.set_markup(f"<b>{_('x64v4 - Advanced')}</b>")
        xanmod_v4_header.set_xalign(0)
        xanmod_v4_box.pack_start(xanmod_v4_header, False, False, 0)
        
        xanmod_v4_desc = Gtk.Label()
        xanmod_v4_desc.set_markup(f"<small>{_('For very recent CPUs (Intel 12th gen+, AMD Zen 4+). AVX-512 support.')}</small>")
        xanmod_v4_desc.set_line_wrap(True)
        xanmod_v4_desc.set_xalign(0)
        xanmod_v4_box.pack_start(xanmod_v4_desc, False, False, 0)
        
        self.xanmod_v4_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        xanmod_v4_box.pack_start(self.xanmod_v4_row, False, False, 2)
        
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
            elif kernel_type == "xanmod-v3":
                result = subprocess.run(['dpkg', '-l', 'linux-xanmod-x64v3'], 
                                      capture_output=True, text=True)
                return result.returncode == 0
            elif kernel_type == "xanmod-v4":
                result = subprocess.run(['dpkg', '-l', 'linux-xanmod-x64v4'], 
                                      capture_output=True, text=True)
                return result.returncode == 0
            elif kernel_type == "xanmod-edge":
                result = subprocess.run(['dpkg', '-l', 'linux-xanmod-edge-x64v3'], 
                                      capture_output=True, text=True)
                return result.returncode == 0
            elif kernel_type == "xanmod-lts":
                result = subprocess.run(['dpkg', '-l', 'linux-xanmod-lts-x64v3'], 
                                      capture_output=True, text=True)
                return result.returncode == 0
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
        self._clear_container(self.xanmod_v3_row)
        self._clear_container(self.xanmod_v4_row)
        self._clear_container(self.xanmod_edge_row)
        self._clear_container(self.xanmod_lts_row)
        
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
        
        # Update XanMod v3 button
        self._update_xanmod_variant_button("xanmod-v3", self.xanmod_v3_row, "x64v3")
        
        # Update XanMod v4 button
        self._update_xanmod_variant_button("xanmod-v4", self.xanmod_v4_row, "x64v4")
        
        # Update XanMod EDGE button
        self._update_xanmod_variant_button("xanmod-edge", self.xanmod_edge_row, "EDGE")
        
        # Update XanMod LTS button
        self._update_xanmod_variant_button("xanmod-lts", self.xanmod_lts_row, "LTS")
        
        # Show new buttons
        self.microcode_row.show_all()
        self.liquorix_row.show_all()
        self.xanmod_v3_row.show_all()
        self.xanmod_v4_row.show_all()
        self.xanmod_edge_row.show_all()
        self.xanmod_lts_row.show_all()

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

    def _update_xanmod_variant_button(self, kernel_type, row, label_suffix):
        """Update button for a specific XanMod variant"""
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
            install_button.connect("clicked", lambda w: self.on_install_xanmod_clicked(w, kernel_type))
            row.pack_start(install_button, False, False, 0)

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
        script_content = f"""#!/bin/bash
echo "{_('Installing Liquorix Kernel...')}"
curl -s 'https://liquorix.net/install-liquorix.sh' | pkexec bash
echo "{_('Installation complete.')}"
"""
        script_path = "/tmp/install-liquorix.sh"
        with open(script_path, "w") as f:
            f.write(script_content)
        os.chmod(script_path, 0o755)
        self.command_runner.run_command(script_path, self._on_operation_complete)

    def on_install_xanmod_clicked(self, widget, kernel_type):
        """Install specific XanMod variant"""
        # Map kernel types to package names
        package_map = {
            "xanmod-v3": "linux-xanmod-x64v3",
            "xanmod-v4": "linux-xanmod-x64v4",
            "xanmod-edge": "linux-xanmod-edge-x64v3",
            "xanmod-lts": "linux-xanmod-lts-x64v3"
        }
        
        package = package_map.get(kernel_type, "linux-xanmod-x64v3")
        variant_name = kernel_type.replace("xanmod-", "").upper()
        
        script_content = f"""#!/bin/bash
echo "{_('Installing XanMod')} {variant_name}..."
pkexec bash -c '
wget -qO - https://dl.xanmod.org/archive.key | gpg --dearmor -o /etc/apt/keyrings/xanmod-archive-keyring.gpg 2>/dev/null || true
echo "deb [signed-by=/etc/apt/keyrings/xanmod-archive-keyring.gpg] http://deb.xanmod.org releases main" > /etc/apt/sources.list.d/xanmod-release.list
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
pkexec apt remove -y linux-image-liquorix-amd64 linux-headers-liquorix-amd64
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
        
        # Map kernel types to package names
        package_map = {
            "xanmod-v3": "linux-xanmod-x64v3",
            "xanmod-v4": "linux-xanmod-x64v4",
            "xanmod-edge": "linux-xanmod-edge-x64v3",
            "xanmod-lts": "linux-xanmod-lts-x64v3"
        }
        
        package = package_map.get(kernel_type, "linux-xanmod-x64v3")
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
        """Clean old kernels, keeping the running kernel and the latest of each type."""
        try:
            # Get current running kernel
            current_kernel = subprocess.check_output(['uname', '-r']).decode().strip()
            
            # Get all installed kernel image packages
            result = subprocess.run(
                ['dpkg', '-l', 'linux-image-*'],
                capture_output=True, text=True
            )
            
            # Parse installed kernels (only real kernel packages, not meta-packages)
            meta_packages = {
                'linux-image-amd64', 'linux-image-liquorix-amd64',
                'linux-image-686', 'linux-image-686-pae'
            }
            installed = []
            for line in result.stdout.splitlines():
                if line.startswith('ii') and 'linux-image-' in line:
                    pkg = line.split()[1]
                    if pkg in meta_packages:
                        continue
                    installed.append(pkg)
            
            if not installed:
                self._show_info_dialog(_("No kernels found"), _("Could not find any installed kernel packages."))
                return
            
            # Classify kernels by type
            base_kernels = []
            liquorix_kernels = []
            xanmod_kernels = []
            
            for pkg in installed:
                if 'liquorix' in pkg:
                    liquorix_kernels.append(pkg)
                elif 'xanmod' in pkg:
                    xanmod_kernels.append(pkg)
                else:
                    base_kernels.append(pkg)
            
            # Sort each group (dpkg version order)
            base_kernels.sort()
            liquorix_kernels.sort()
            xanmod_kernels.sort()
            
            # Determine which to keep
            keep = set()
            
            # Always keep the running kernel's package
            for pkg in installed:
                if current_kernel in pkg:
                    keep.add(pkg)
            
            # Keep the latest base kernel
            if base_kernels:
                keep.add(base_kernels[-1])
            
            # Keep the latest liquorix kernel (if any)
            if liquorix_kernels:
                keep.add(liquorix_kernels[-1])
            
            # Keep the latest xanmod kernel (if any)
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
            
            # Also find matching headers packages
            headers_to_remove = []
            for pkg in to_remove:
                header_pkg = pkg.replace('linux-image-', 'linux-headers-')
                check = subprocess.run(['dpkg', '-s', header_pkg], capture_output=True, text=True)
                if check.returncode == 0:
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
                f"{_('Packages to remove')} ({len(all_to_remove)}):\n{remove_text}\n\n"
                f"{_('Continue?')}"
            )
            
            response = dialog.run()
            dialog.destroy()
            
            if response != Gtk.ResponseType.YES:
                return
            
            # Build removal script (single pkexec execution)
            packages_str = " ".join(all_to_remove)
            script_content = (
                "#!/bin/bash\n"
                "set -e\n"
                f"echo \"{_('Removing old kernels...')}\"\n"
                f"apt remove -y {packages_str}\n"
                "apt autoremove -y\n"
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

