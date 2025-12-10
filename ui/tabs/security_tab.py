"""
Security tab for Soplos Welcome.
Manages security tools, backups, firewall, and antivirus.
"""

import gi
import os
import subprocess
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

from core.i18n_manager import _
from utils.command_runner import CommandRunner


class SecurityTab(Gtk.ScrolledWindow):
    """
    Security management tab.
    Provides tools for backups, firewall, filesystem tools, and antivirus.
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
        self.timeshift_row = None
        self.dejaduprow = None
        self.gufw_row = None
        self.ufw_status_label = None
        self.btrfs_row = None
        self.clamtk_row = None
        self.rkhunter_row = None
        self.bleachbit_row = None
        
        # Timer for periodic UFW status updates
        self.ufw_timer_id = None
        
        self._create_ui()
        
        # Start periodic UFW status check (every 3 seconds)
        self._start_ufw_status_timer()
    
    def _create_ui(self):
        """Create the security tab interface."""
        # Header
        header = Gtk.Label()
        header.set_markup(f'<span size="20000" weight="bold">{_("Security &amp; System Protection")}</span>')
        header.set_halign(Gtk.Align.START)
        self.main_box.pack_start(header, False, False, 0)
        
        subtitle = Gtk.Label(_("Protect your system with backups, firewall, and security tools"))
        subtitle.set_halign(Gtk.Align.START)
        subtitle.get_style_context().add_class('dim-label')
        self.main_box.pack_start(subtitle, False, False, 0)
        
        # Separator
        self.main_box.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 10)
        
        # System Backups section
        self._create_backups_section()
        
        # Separator
        self.main_box.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 10)
        
        # Firewall section
        self._create_firewall_section()
        
        # Separator
        self.main_box.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 10)
        
        # Filesystem tools section
        self._create_filesystem_section()
        
        # Separator
        self.main_box.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 10)
        
        # System Cleaning section
        self._create_cleaning_section()
        
        # Separator
        self.main_box.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 10)
        
        # Antivirus section
        self._create_antivirus_section()
        
        # Update button states
        self._update_all_buttons()
        
        self.show_all()
    
    def _create_backups_section(self):
        """Create system backups section."""
        backups_frame = Gtk.Frame()
        backups_frame.set_label(_("System Backups"))
        backups_frame.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        self.main_box.pack_start(backups_frame, False, False, 5)
        
        backups_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        backups_container.set_border_width(10)
        backups_frame.add(backups_container)
        
        # Timeshift
        timeshift_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        backups_container.pack_start(timeshift_box, False, False, 5)
        
        timeshift_header = Gtk.Label()
        timeshift_header.set_markup(f"<b>Timeshift</b> <span color='#50fa7b'>({_('Recommended')})</span>")
        timeshift_header.set_xalign(0)
        timeshift_box.pack_start(timeshift_header, False, False, 0)
        
        timeshift_desc = Gtk.Label()
        timeshift_desc.set_markup(f"<small>{_('Creates automatic system snapshots. Protects your configuration and allows easy restoration.')}</small>")
        timeshift_desc.set_line_wrap(True)
        timeshift_desc.set_xalign(0)
        timeshift_box.pack_start(timeshift_desc, False, False, 0)
        
        self.timeshift_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        timeshift_box.pack_start(self.timeshift_row, False, False, 2)
        
        # Deja Dup
        dejadup_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        backups_container.pack_start(dejadup_box, False, False, 5)
        
        dejadup_header = Gtk.Label()
        dejadup_header.set_markup(f"<b>Deja Dup</b>")
        dejadup_header.set_xalign(0)
        dejadup_box.pack_start(dejadup_header, False, False, 0)
        
        dejadup_desc = Gtk.Label()
        dejadup_desc.set_markup(f"<small>{_('Simple backups of personal files with encryption support.')}</small>")
        dejadup_desc.set_line_wrap(True)
        dejadup_desc.set_xalign(0)
        dejadup_box.pack_start(dejadup_desc, False, False, 0)
        
        self.dejadup_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        dejadup_box.pack_start(self.dejadup_row, False, False, 2)
    
    def _create_firewall_section(self):
        """Create firewall protection section."""
        firewall_frame = Gtk.Frame()
        firewall_frame.set_label(_("Firewall Protection"))
        firewall_frame.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        self.main_box.pack_start(firewall_frame, False, False, 5)
        
        firewall_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        firewall_container.set_border_width(10)
        firewall_frame.add(firewall_container)
        
        # GUFW
        gufw_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        firewall_container.pack_start(gufw_box, False, False, 5)
        
        gufw_header = Gtk.Label()
        gufw_header.set_markup(f"<b>GUFW</b> <span color='#50fa7b'>({_('Recommended for Desktop')})</span>")
        gufw_header.set_xalign(0)
        gufw_box.pack_start(gufw_header, False, False, 0)
        
        gufw_desc = Gtk.Label()
        gufw_desc.set_markup(f"<small>{_('Simple graphical interface for UFW firewall. Control network traffic easily.')}</small>")
        gufw_desc.set_line_wrap(True)
        gufw_desc.set_xalign(0)
        gufw_box.pack_start(gufw_desc, False, False, 0)
        
        self.gufw_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        gufw_box.pack_start(self.gufw_row, False, False, 2)
        
        # UFW Status
        ufw_status_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        firewall_container.pack_start(ufw_status_box, False, False, 5)
        
        ufw_status_title = Gtk.Label()
        ufw_status_title.set_markup(f"<b>{_('Firewall Status')}:</b>")
        ufw_status_box.pack_start(ufw_status_title, False, False, 0)
        
        self.ufw_status_label = Gtk.Label()
        ufw_status_box.pack_start(self.ufw_status_label, False, False, 0)
        
        # Activate/Deactivate button
        self.ufw_toggle_button = Gtk.Button()
        self.ufw_toggle_button.connect('clicked', self._on_toggle_ufw_clicked)
        ufw_status_box.pack_start(self.ufw_toggle_button, False, False, 0)
    
    def _create_filesystem_section(self):
        """Create filesystem tools section."""
        fs_frame = Gtk.Frame()
        fs_frame.set_label(_("Filesystem Tools"))
        fs_frame.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        self.main_box.pack_start(fs_frame, False, False, 5)
        
        fs_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        fs_container.set_border_width(10)
        fs_frame.add(fs_container)
        
        # Detect filesystem
        current_fs = self._detect_filesystem()
        
        # BTRFS Assistant
        btrfs_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        fs_container.pack_start(btrfs_box, False, False, 5)
        
        btrfs_header = Gtk.Label()
        if current_fs == 'btrfs':
            btrfs_header.set_markup(f"<b>BTRFS Assistant</b>")
        else:
            btrfs_header.set_markup(f"<b>BTRFS Assistant</b> <span color='#888888'>({_('Only for BTRFS')})</span>")
        btrfs_header.set_xalign(0)
        btrfs_box.pack_start(btrfs_header, False, False, 0)
        
        btrfs_desc = Gtk.Label()
        if current_fs == 'btrfs':
            btrfs_desc.set_markup(f"<small>{_('Advanced management of BTRFS subvolumes and snapshots.')}</small>")
        else:
            btrfs_desc.set_markup(f"<small>{_('Advanced management of BTRFS subvolumes and snapshots.')}\n<i>{_('Current system')}: {current_fs.upper()}. {_('BTRFS Assistant is not compatible.')}</i></small>")
        btrfs_desc.set_line_wrap(True)
        btrfs_desc.set_xalign(0)
        btrfs_box.pack_start(btrfs_desc, False, False, 0)
        
        self.btrfs_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        btrfs_box.pack_start(self.btrfs_row, False, False, 2)
    
    def _create_cleaning_section(self):
        """Create system cleaning section."""
        clean_frame = Gtk.Frame()
        clean_frame.set_label(_("System Cleaning"))
        clean_frame.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        self.main_box.pack_start(clean_frame, False, False, 5)
        
        clean_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        clean_container.set_border_width(10)
        clean_frame.add(clean_container)
        
        # BleachBit
        bleachbit_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        clean_container.pack_start(bleachbit_box, False, False, 5)
        
        bleachbit_header = Gtk.Label()
        bleachbit_header.set_markup(f"<b>BleachBit</b> <span color='#50fa7b'>({_('Recommended')})</span>")
        bleachbit_header.set_xalign(0)
        bleachbit_box.pack_start(bleachbit_header, False, False, 0)
        
        bleachbit_desc = Gtk.Label()
        bleachbit_desc.set_markup(f"<small>{_('Free disk space and maintain privacy. Cleans cache, cookies, and temporary files.')}</small>")
        bleachbit_desc.set_line_wrap(True)
        bleachbit_desc.set_xalign(0)
        bleachbit_box.pack_start(bleachbit_desc, False, False, 0)
        
        self.bleachbit_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        bleachbit_box.pack_start(self.bleachbit_row, False, False, 2)
    
    def _create_antivirus_section(self):
        """Create antivirus and malware section."""
        av_frame = Gtk.Frame()
        av_frame.set_label(_("Antivirus & Malware"))
        av_frame.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        self.main_box.pack_start(av_frame, False, False, 5)
        
        av_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        av_container.set_border_width(10)
        av_frame.add(av_container)
        
        # ClamTk
        clamtk_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        av_container.pack_start(clamtk_box, False, False, 5)
        
        clamtk_header = Gtk.Label()
        clamtk_header.set_markup(f"<b>ClamTk</b> <span color='#50fa7b'>({_('Recommended')})</span>")
        clamtk_header.set_xalign(0)
        clamtk_box.pack_start(clamtk_header, False, False, 0)
        
        clamtk_desc = Gtk.Label()
        clamtk_desc.set_markup(f"<small>{_('Graphical interface for ClamAV. Scan your system against viruses and malware.')}</small>")
        clamtk_desc.set_line_wrap(True)
        clamtk_desc.set_xalign(0)
        clamtk_box.pack_start(clamtk_desc, False, False, 0)
        
        self.clamtk_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        clamtk_box.pack_start(self.clamtk_row, False, False, 2)
        
        # rkhunter
        rkhunter_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        av_container.pack_start(rkhunter_box, False, False, 5)
        
        rkhunter_header = Gtk.Label()
        rkhunter_header.set_markup(f"<b>rkhunter</b> <span color='#ffb86c'>({_('Advanced')})</span>")
        rkhunter_header.set_xalign(0)
        rkhunter_box.pack_start(rkhunter_header, False, False, 0)
        
        rkhunter_desc = Gtk.Label()
        rkhunter_desc.set_markup(f"<small>{_('Command-line tool to detect rootkits and system threats.')}</small>")
        rkhunter_desc.set_line_wrap(True)
        rkhunter_desc.set_xalign(0)
        rkhunter_box.pack_start(rkhunter_desc, False, False, 0)
        
        self.rkhunter_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        rkhunter_box.pack_start(self.rkhunter_row, False, False, 2)
    
    def _detect_filesystem(self):
        """Detect root filesystem type."""
        try:
            # Use findmnt which correctly detects BTRFS even with subvolumes (@, @home, etc.)
            result = subprocess.run(
                ["findmnt", "-n", "-o", "FSTYPE", "/"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                return result.stdout.strip().lower()
        except:
            pass
        return "unknown"
    
    def _is_ufw_active(self):
        """Check if UFW firewall is active."""
        try:
            # Read UFW config file (no password needed)
            with open('/etc/ufw/ufw.conf', 'r') as f:
                for line in f:
                    if line.strip().startswith('ENABLED='):
                        return 'yes' in line.lower()
        except:
            pass
        return False
    
    def _is_package_installed(self, package_name):
        """Check if a package is installed."""
        try:
            result = subprocess.run(
                ["dpkg-query", "-W", "-f=${Status}", package_name],
                capture_output=True, text=True
            )
            return "install ok installed" in result.stdout
        except:
            return False
    
    def _update_all_buttons(self):
        """Update all buttons based on installation status."""
        self._clear_container(self.timeshift_row)
        self._clear_container(self.dejadup_row)
        self._clear_container(self.gufw_row)
        self._clear_container(self.btrfs_row)
        self._clear_container(self.clamtk_row)
        self._clear_container(self.rkhunter_row)
        self._clear_container(self.bleachbit_row)
        
        # Timeshift
        self._update_package_button('timeshift', self.timeshift_row, with_configure=True)
        
        # Deja Dup
        self._update_package_button('deja-dup', self.dejadup_row)
        
        # GUFW
        self._update_package_button('gufw', self.gufw_row, with_configure=True, configure_label=_("Open GUFW"))
        
        # BTRFS Assistant (only if btrfs)
        current_fs = self._detect_filesystem()
        if current_fs == 'btrfs':
            self._update_package_button('btrfs-assistant', self.btrfs_row, with_configure=True)
        else:
            not_available = Gtk.Label()
            not_available.set_markup(f"<i>{_('Not available on')} {current_fs.upper()}</i>")
            self.btrfs_row.pack_start(not_available, False, False, 0)
        
        # BleachBit
        self._update_package_button('bleachbit', self.bleachbit_row, with_configure=True, configure_label=_("Open BleachBit"))
        
        # ClamTk (install both clamav and clamtk)
        self._update_clamtk_button()
        
        # rkhunter
        self._update_package_button('rkhunter', self.rkhunter_row, with_scan=True)
        
        # UFW Status
        self._update_ufw_status()
        
        # Show buttons
        self.timeshift_row.show_all()
        self.dejadup_row.show_all()
        self.gufw_row.show_all()
        self.btrfs_row.show_all()
        self.clamtk_row.show_all()
        self.rkhunter_row.show_all()
        self.bleachbit_row.show_all()
    
    def _update_package_button(self, package, row, with_configure=False, configure_label=None, with_scan=False):
        """Update button for a package."""
        is_installed = self._is_package_installed(package)
        
        if is_installed:
            uninstall_btn = Gtk.Button(label=_("Uninstall"))
            uninstall_btn.get_style_context().add_class("destructive-action")
            uninstall_btn.connect('clicked', lambda w: self._on_uninstall_package(package))
            row.pack_start(uninstall_btn, False, False, 0)
            
            installed_label = Gtk.Label(label=_("Installed"))
            installed_label.get_style_context().add_class("success")
            row.pack_start(installed_label, False, False, 10)
            
            # Configure button if requested
            if with_configure:
                label = configure_label if configure_label else _("Configure")
                configure_btn = Gtk.Button(label=label)
                configure_btn.get_style_context().add_class("suggested-action")
                configure_btn.connect('clicked', lambda w: self._on_configure_package(package))
                row.pack_start(configure_btn, False, False, 0)
            
            # Scan button for rkhunter
            if with_scan:
                scan_btn = Gtk.Button(label=_("Scan System"))
                scan_btn.connect('clicked', lambda w: self._on_scan_rkhunter())
                row.pack_start(scan_btn, False, False, 0)
        else:
            install_btn = Gtk.Button(label=_("Install"))
            install_btn.get_style_context().add_class("suggested-action")
            install_btn.connect('clicked', lambda w: self._on_install_package(package))
            row.pack_start(install_btn, False, False, 0)
    
    def _update_clamtk_button(self):
        """Update ClamTk button (installs both clamav and clamtk)."""
        is_installed = self._is_package_installed('clamtk')
        
        if is_installed:
            uninstall_btn = Gtk.Button(label=_("Uninstall"))
            uninstall_btn.get_style_context().add_class("destructive-action")
            uninstall_btn.connect('clicked', lambda w: self._on_uninstall_package('clamav clamtk'))
            self.clamtk_row.pack_start(uninstall_btn, False, False, 0)
            
            installed_label = Gtk.Label(label=_("Installed"))
            installed_label.get_style_context().add_class("success")
            self.clamtk_row.pack_start(installed_label, False, False, 10)
            
            # Update definitions button
            update_btn = Gtk.Button(label=_("Update Definitions"))
            update_btn.connect('clicked', self._on_update_clamav)
            self.clamtk_row.pack_start(update_btn, False, False, 0)
        else:
            install_btn = Gtk.Button(label=_("Install"))
            install_btn.get_style_context().add_class("suggested-action")
            install_btn.connect('clicked', lambda w: self._on_install_package('clamav clamtk'))
            self.clamtk_row.pack_start(install_btn, False, False, 0)
    
    def _update_ufw_status(self):
        """Update UFW status display."""
        is_active = self._is_ufw_active()
        
        if is_active:
            self.ufw_status_label.set_markup(f"<span color='#50fa7b'><b>{_('Active')}</b></span>")
            self.ufw_toggle_button.set_label(_("Deactivate"))
            self.ufw_toggle_button.get_style_context().add_class("destructive-action")
        else:
            self.ufw_status_label.set_markup(f"<span color='#ff5555'><b>{_('Inactive')}</b></span>")
            self.ufw_toggle_button.set_label(_("Activate"))
            self.ufw_toggle_button.get_style_context().add_class("suggested-action")
    
    def _clear_container(self, container):
        """Clear all widgets from a container."""
        if container:
            for child in container.get_children():
                container.remove(child)
    
    def _on_operation_complete(self, success=True):
        """Callback after operation completes."""
        GLib.timeout_add(1000, self._update_all_buttons)
        GLib.timeout_add(1000, self._update_ufw_status)
    
    # Event handlers
    def _on_install_package(self, packages):
        """Install package(s)."""
        script_content = f"""#!/bin/bash
echo "Installing {packages}..."
pkexec apt install -y {packages}
echo "{_('Installation complete.')}"
"""
        script_path = f"/tmp/install-{packages.split()[0]}.sh"
        with open(script_path, "w") as f:
            f.write(script_content)
        os.chmod(script_path, 0o755)
        self.command_runner.run_command(script_path, self._on_operation_complete)
    
    def _on_uninstall_package(self, packages):
        """Uninstall package(s)."""
        script_content = f"""#!/bin/bash
echo "Uninstalling {packages}..."
pkexec apt remove -y {packages}
echo "{_('Uninstallation complete.')}"
"""
        script_path = f"/tmp/uninstall-{packages.split()[0]}.sh"
        with open(script_path, "w") as f:
            f.write(script_content)
        os.chmod(script_path, 0o755)
        self.command_runner.run_command(script_path, self._on_operation_complete)
    
    def _on_configure_package(self, package):
        """Open configuration GUI for package."""
        try:
            if package == 'timeshift':
                subprocess.Popen(['pkexec', 'timeshift-gtk'])
            elif package == 'gufw':
                subprocess.Popen(['gufw'])
            elif package == 'btrfs-assistant':
                subprocess.Popen(['pkexec', 'btrfs-assistant'])
            elif package == 'bleachbit':
                subprocess.Popen(['bleachbit'])
        except Exception as e:
            print(f"Error launching {package}: {e}")
    
    def _on_toggle_ufw_clicked(self, widget):
        """Toggle UFW firewall on/off."""
        is_active = self._is_ufw_active()
        
        if is_active:
            # Single pkexec call for disable
            command = "pkexec bash -c 'ufw disable'"
        else:
            # Single pkexec call for enable (all commands run as root)
            command = "pkexec bash -c 'ufw --force enable && systemctl enable ufw && systemctl start ufw'"
        
        self.command_runner.run_command(command, self._on_operation_complete)
    
    def _on_update_clamav(self, widget):
        """Update ClamAV virus definitions."""
        # Create the inner script that will run with root privileges
        inner_script = "/tmp/freshclam-update.sh"
        with open(inner_script, "w") as f:
            f.write("#!/bin/bash\n")
            f.write("systemctl stop clamav-freshclam 2>/dev/null || true\n")
            f.write("freshclam 2>&1\n")
            f.write("systemctl start clamav-freshclam 2>/dev/null || true\n")
        os.chmod(inner_script, 0o755)
        
        # Create the outer script that calls pkexec
        script_path = "/tmp/update-clamav.sh"
        with open(script_path, "w") as f:
            f.write("#!/bin/bash\n")
            f.write(f"echo '{_('Updating virus definitions...')}'\n")
            f.write(f"pkexec {inner_script}\n")
            f.write(f"echo '{_('Definitions updated successfully!')}'\n")
            f.write("sleep 2\n")
        os.chmod(script_path, 0o755)
        self.command_runner.run_command(script_path)
    
    def _on_scan_rkhunter(self):
        """Run rkhunter system scan."""
        script_path = "/tmp/scan-rkhunter.sh"
        with open(script_path, "w") as f:
            f.write("#!/bin/bash\n")
            f.write(f"echo '{_('Scanning system for rootkits...')}'\n")
            f.write("pkexec rkhunter --check --skip-keypress --nocolors 2>&1 | grep -v '^$'\n")
            f.write(f"echo '{_('Scan complete.')}'\n")
            f.write("sleep 3\n")
        os.chmod(script_path, 0o755)
        self.command_runner.run_command(script_path)
    
    def _start_ufw_status_timer(self):
        """Start periodic UFW status check."""
        # Check every 3 seconds
        self.ufw_timer_id = GLib.timeout_add_seconds(3, self._periodic_ufw_check)
    
    def _stop_ufw_status_timer(self):
        """Stop periodic UFW status check."""
        if self.ufw_timer_id:
            GLib.source_remove(self.ufw_timer_id)
            self.ufw_timer_id = None
    
    def _periodic_ufw_check(self):
        """Periodic check of UFW status (called by timer)."""
        self._update_ufw_status()
        return True  # Keep timer running

