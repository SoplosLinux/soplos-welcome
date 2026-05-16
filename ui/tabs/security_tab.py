"""
Security tab for Soplos Welcome.
Manages security tools, backups, firewall, and antivirus.
"""

import gi
import os
import subprocess
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, GdkPixbuf

ICONS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'assets', 'icons', 'security')

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
        self.grub_btrfs_row = None
        self.dejaduprow = None
        self.gufw_row = None
        self.portmaster_row = None
        self.ufw_status_label = None
        self.btrfs_row = None
        self.protonvpn_row = None
        self.surfshark_row = None
        self.mozilla_vpn_row = None
        self.clamtk_row = None
        self.clamui_row = None
        self.rkhunter_row = None
        self.bleachbit_row = None
        self.stacer_row = None
        self.sweeper_row = None
        self.soplos_sys_cleaner_row = None
        
        # Timer for periodic UFW status updates
        self.ufw_timer_id = None
        
        self._create_ui()

        # Start periodic UFW status check (every 3 seconds)
        self._start_ufw_status_timer()

    def _create_tool_info_block(self, icon_file, header_markup, desc_markup):
        """Return an HBox with a 48px icon centred next to name + description (same layout as Gaming tab)."""
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        hbox.set_margin_top(4)
        hbox.set_margin_bottom(4)

        icon_path = os.path.join(ICONS_DIR, icon_file)
        if os.path.exists(icon_path):
            try:
                pb = GdkPixbuf.Pixbuf.new_from_file_at_scale(icon_path, 48, 48, True)
                img = Gtk.Image.new_from_pixbuf(pb)
                img.set_valign(Gtk.Align.CENTER)
                hbox.pack_start(img, False, False, 0)
            except Exception:
                pass

        info_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        info_vbox.set_valign(Gtk.Align.CENTER)

        header_lbl = Gtk.Label()
        header_lbl.set_markup(header_markup)
        header_lbl.set_xalign(0)
        info_vbox.pack_start(header_lbl, False, False, 0)

        desc_lbl = Gtk.Label()
        desc_lbl.set_markup(desc_markup)
        desc_lbl.set_line_wrap(True)
        desc_lbl.set_xalign(0)
        info_vbox.pack_start(desc_lbl, False, False, 0)

        hbox.pack_start(info_vbox, True, True, 0)
        return hbox

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

        # VPN section
        self._create_vpn_section()

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
        
        timeshift_info = self._create_tool_info_block(
            'timeshift.png',
            f"<b>Timeshift</b> <span color='#50fa7b'>({_('Recommended')})</span>",
            f"<small>{_('Creates automatic system snapshots. Protects your configuration and allows easy restoration.')}</small>"
        )
        self.timeshift_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.timeshift_row.set_valign(Gtk.Align.CENTER)
        timeshift_info.pack_end(self.timeshift_row, False, False, 0)
        timeshift_box.pack_start(timeshift_info, False, False, 0)
        
        # Grub BTRFS (only if BTRFS)
        # Grub BTRFS
        current_fs = self._detect_filesystem()
        
        grub_btrfs_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        backups_container.pack_start(grub_btrfs_box, False, False, 5)
        
        grub_btrfs_header_markup = (
            f"<b>Grub BTRFS</b> <span color='#50fa7b'>({_('Complementary')})</span>"
            if current_fs == 'btrfs' else
            f"<b>Grub BTRFS</b> <span color='#888888'>({_('Only for BTRFS')})</span>"
        )
        grub_btrfs_desc_markup = (
            f"<small>{_('Automatically add BTRFS snapshots to GRUB menu. Allows booting from snapshots.')}</small>"
            if current_fs == 'btrfs' else
            f"<small>{_('Automatically add BTRFS snapshots to GRUB menu.')}\n<i>{_('Current system')}: {current_fs.upper()}. {_('Grub BTRFS is not compatible.')}</i></small>"
        )
        grub_btrfs_info = self._create_tool_info_block('grub-btrfs.png', grub_btrfs_header_markup, grub_btrfs_desc_markup)
        self.grub_btrfs_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.grub_btrfs_row.set_valign(Gtk.Align.CENTER)
        grub_btrfs_info.pack_end(self.grub_btrfs_row, False, False, 0)
        grub_btrfs_box.pack_start(grub_btrfs_info, False, False, 0)
        
        # Deja Dup
        dejadup_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        backups_container.pack_start(dejadup_box, False, False, 5)
        
        dejadup_info = self._create_tool_info_block(
            'dejadup.png',
            f"<b>Deja Dup</b>",
            f"<small>{_('Simple backups of personal files with encryption support.')}</small>"
        )
        self.dejadup_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.dejadup_row.set_valign(Gtk.Align.CENTER)
        dejadup_info.pack_end(self.dejadup_row, False, False, 0)
        dejadup_box.pack_start(dejadup_info, False, False, 0)
        
        # BTRFS Assistant
        btrfs_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        backups_container.pack_start(btrfs_box, False, False, 5)
        
        btrfs_header_markup = (
            f"<b>BTRFS Assistant</b>"
            if current_fs == 'btrfs' else
            f"<b>BTRFS Assistant</b> <span color='#888888'>({_('Only for BTRFS')})</span>"
        )
        btrfs_desc_markup = (
            f"<small>{_('Advanced management of BTRFS subvolumes and snapshots.')}</small>"
            if current_fs == 'btrfs' else
            f"<small>{_('Advanced management of BTRFS subvolumes and snapshots.')}\n<i>{_('Current system')}: {current_fs.upper()}. {_('BTRFS Assistant is not compatible.')}</i></small>"
        )
        btrfs_info = self._create_tool_info_block('btrfs-assistant.png', btrfs_header_markup, btrfs_desc_markup)
        self.btrfs_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.btrfs_row.set_valign(Gtk.Align.CENTER)
        btrfs_info.pack_end(self.btrfs_row, False, False, 0)
        btrfs_box.pack_start(btrfs_info, False, False, 0)
    
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
        
        gufw_info = self._create_tool_info_block(
            'gufw.png',
            f"<b>GUFW</b> <span color='#50fa7b'>({_('Recommended for Desktop')})</span>",
            f"<small>{_('Simple graphical interface for UFW firewall. Control network traffic easily.')}</small>"
        )

        # Botones + estado UFW en el lado derecho del mismo hbox
        controls_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        controls_box.set_valign(Gtk.Align.CENTER)

        self.gufw_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        controls_box.pack_start(self.gufw_row, False, False, 0)

        # Separador vertical
        separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        controls_box.pack_start(separator, False, False, 0)
        
        # UFW Status box
        ufw_status_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        controls_box.pack_start(ufw_status_box, False, False, 0)
        
        ufw_status_title = Gtk.Label()
        ufw_status_title.set_markup(f"<b>{_('Firewall Status')}:</b>")
        ufw_status_box.pack_start(ufw_status_title, False, False, 0)
        
        self.ufw_status_label = Gtk.Label()
        ufw_status_box.pack_start(self.ufw_status_label, False, False, 0)
        
        self.ufw_toggle_button = Gtk.Button()
        self.ufw_toggle_button.connect('clicked', self._on_toggle_ufw_clicked)
        ufw_status_box.pack_start(self.ufw_toggle_button, False, False, 0)

        gufw_info.pack_end(controls_box, False, False, 0)
        gufw_box.pack_start(gufw_info, False, False, 0)

        # Portmaster
        portmaster_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        firewall_container.pack_start(portmaster_box, False, False, 5)

        portmaster_info = self._create_tool_info_block(
            'portmaster.png',
            f"<b>Portmaster</b> <span color='#8be9fd'>({_('Advanced')})</span>",
            f"<small>{_('Application-level firewall. Monitor and control network connections per application.')}</small>"
        )
        self.portmaster_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.portmaster_row.set_valign(Gtk.Align.CENTER)
        portmaster_info.pack_end(self.portmaster_row, False, False, 0)
        portmaster_box.pack_start(portmaster_info, False, False, 0)

    def _create_vpn_section(self):
        """Create VPN section."""
        vpn_frame = Gtk.Frame()
        vpn_frame.set_label(_("VPN"))
        vpn_frame.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        self.main_box.pack_start(vpn_frame, False, False, 5)

        vpn_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        vpn_container.set_border_width(10)
        vpn_frame.add(vpn_container)

        protonvpn_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        vpn_container.pack_start(protonvpn_box, False, False, 5)

        protonvpn_info = self._create_tool_info_block(
            'proton-vpn.png',
            f"<b>Proton VPN</b>",
            f"<small>{_('Secure and private VPN service from Proton.')}</small>"
        )
        self.protonvpn_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.protonvpn_row.set_valign(Gtk.Align.CENTER)
        protonvpn_info.pack_end(self.protonvpn_row, False, False, 0)
        protonvpn_box.pack_start(protonvpn_info, False, False, 0)

        # Surfshark
        surfshark_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        vpn_container.pack_start(surfshark_box, False, False, 5)

        surfshark_info = self._create_tool_info_block(
            'surfshark.png',
            f"<b>Surfshark</b>",
            f"<small>{_('Fast and affordable VPN with unlimited devices.')}</small>"
        )
        self.surfshark_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.surfshark_row.set_valign(Gtk.Align.CENTER)
        surfshark_info.pack_end(self.surfshark_row, False, False, 0)
        surfshark_box.pack_start(surfshark_info, False, False, 0)

        # Mozilla VPN
        mozilla_vpn_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        vpn_container.pack_start(mozilla_vpn_box, False, False, 5)

        mozilla_vpn_info = self._create_tool_info_block(
            'mozilla-vpn.png',
            f"<b>Mozilla VPN</b>",
            f"<small>{_('VPN from Mozilla. Simple, fast and focused on privacy.')}</small>"
        )
        self.mozilla_vpn_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.mozilla_vpn_row.set_valign(Gtk.Align.CENTER)
        mozilla_vpn_info.pack_end(self.mozilla_vpn_row, False, False, 0)
        mozilla_vpn_box.pack_start(mozilla_vpn_info, False, False, 0)

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
        
        bleachbit_info = self._create_tool_info_block(
            'bleachbit.png',
            f"<b>BleachBit</b> <span color='#50fa7b'>({_('Recommended')})</span>",
            f"<small>{_('Free disk space and maintain privacy. Cleans cache, cookies, and temporary files.')}</small>"
        )
        self.bleachbit_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.bleachbit_row.set_valign(Gtk.Align.CENTER)
        bleachbit_info.pack_end(self.bleachbit_row, False, False, 0)
        bleachbit_box.pack_start(bleachbit_info, False, False, 0)
        
        # Stacer
        stacer_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        clean_container.pack_start(stacer_box, False, False, 5)
        
        stacer_info = self._create_tool_info_block(
            'stacer.png',
            f"<b>Stacer</b> <span color='#8be9fd'>({_('Alternative')})</span>",
            f"<small>{_('Modern system optimizer with resource monitoring, startup apps, and cache cleaner.')}</small>"
        )
        self.stacer_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.stacer_row.set_valign(Gtk.Align.CENTER)
        stacer_info.pack_end(self.stacer_row, False, False, 0)
        stacer_box.pack_start(stacer_info, False, False, 0)
        
        # Sweeper
        sweeper_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        clean_container.pack_start(sweeper_box, False, False, 5)
        
        sweeper_info = self._create_tool_info_block(
            'sweeper.png',
            f"<b>Sweeper</b> <span color='#8be9fd'>({_('KDE')})</span>",
            f"<small>{_('KDE system cleaner. Simple tool to clean temporary files and browsing history.')}</small>"
        )
        self.sweeper_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.sweeper_row.set_valign(Gtk.Align.CENTER)
        sweeper_info.pack_end(self.sweeper_row, False, False, 0)
        sweeper_box.pack_start(sweeper_info, False, False, 0)

        # Soplos Sys Cleaner
        soplos_cleaner_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        clean_container.pack_start(soplos_cleaner_box, False, False, 5)

        soplos_cleaner_info = self._create_tool_info_block(
            'soplos-sys-cleaner.png',
            f"<b>Soplos Sys Cleaner</b> <span color='#50fa7b'>({_('Recommended')})</span>",
            f"<small>{_('Soplos system cleaner. Clean package cache, orphan packages, logs and temporary files.')}</small>"
        )
        self.soplos_sys_cleaner_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.soplos_sys_cleaner_row.set_valign(Gtk.Align.CENTER)
        soplos_cleaner_info.pack_end(self.soplos_sys_cleaner_row, False, False, 0)
        soplos_cleaner_box.pack_start(soplos_cleaner_info, False, False, 0)

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
        
        clamtk_info = self._create_tool_info_block(
            'clamtk.png',
            f"<b>ClamTk</b> <span color='#50fa7b'>({_('Recommended')})</span>",
            f"<small>{_('Graphical interface for ClamAV. Scan your system against viruses and malware.')}</small>"
        )
        self.clamtk_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.clamtk_row.set_valign(Gtk.Align.CENTER)
        clamtk_info.pack_end(self.clamtk_row, False, False, 0)
        clamtk_box.pack_start(clamtk_info, False, False, 0)

        # ClamUI
        clamui_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        av_container.pack_start(clamui_box, False, False, 5)

        clamui_info = self._create_tool_info_block(
            'clamui.png',
            f"<b>ClamUI</b>",
            f"<small>{_('Modern Flatpak interface for ClamAV antivirus.')}</small>"
        )
        self.clamui_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.clamui_row.set_valign(Gtk.Align.CENTER)
        clamui_info.pack_end(self.clamui_row, False, False, 0)
        clamui_box.pack_start(clamui_info, False, False, 0)

        # rkhunter
        rkhunter_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        av_container.pack_start(rkhunter_box, False, False, 5)
        
        rkhunter_info = self._create_tool_info_block(
            'rkhunter.png',
            f"<b>rkhunter</b> <span color='#ffb86c'>({_('Advanced')})</span>",
            f"<small>{_('Command-line tool to detect rootkits and system threats.')}</small>"
        )
        self.rkhunter_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.rkhunter_row.set_valign(Gtk.Align.CENTER)
        rkhunter_info.pack_end(self.rkhunter_row, False, False, 0)
        rkhunter_box.pack_start(rkhunter_info, False, False, 0)
    
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
        self._clear_container(self.portmaster_row)
        self._clear_container(self.btrfs_row)
        self._clear_container(self.protonvpn_row)
        self._clear_container(self.surfshark_row)
        self._clear_container(self.mozilla_vpn_row)
        self._clear_container(self.clamtk_row)
        self._clear_container(self.clamui_row)
        self._clear_container(self.rkhunter_row)
        self._clear_container(self.bleachbit_row)
        self._clear_container(self.stacer_row)
        self._clear_container(self.sweeper_row)
        self._clear_container(self.soplos_sys_cleaner_row)
        
        # Timeshift
        self._update_package_button('timeshift', self.timeshift_row, with_configure=True)
        
        # Grub BTRFS
        self._clear_container(self.grub_btrfs_row)
        current_fs = self._detect_filesystem()
        if current_fs == 'btrfs':
            self._update_package_button('grub-btrfs', self.grub_btrfs_row)
        else:
            not_available = Gtk.Label()
            not_available.set_markup(f"<i>{_('Not available on')} {current_fs.upper()}</i>")
            self.grub_btrfs_row.pack_start(not_available, False, False, 0)
        
        # Deja Dup
        self._update_package_button('deja-dup', self.dejadup_row)
        
        # GUFW
        self._update_package_button('gufw', self.gufw_row, with_configure=True, configure_label=_("Open GUFW"))

        # Portmaster
        self._update_portmaster_button()
        
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
        
        # Stacer (AppImage from GitHub)
        self._update_stacer_button()
        
        # Sweeper
        self._update_package_button('sweeper', self.sweeper_row, with_configure=True, configure_label=_("Open Sweeper"))

        # Soplos Sys Cleaner
        self._update_package_button('soplos-sys-cleaner', self.soplos_sys_cleaner_row, with_configure=True, configure_label=_("Open Soplos Sys Cleaner"))
        
        # ProtonVPN
        self._update_protonvpn_button()

        # Surfshark
        self._update_surfshark_button()

        # Mozilla VPN
        self._update_mozilla_vpn_button()

        # ClamTk (install both clamav and clamtk)
        self._update_clamtk_button()

        # ClamUI
        self._update_clamui_button()

        # rkhunter
        self._update_package_button('rkhunter', self.rkhunter_row, with_scan=True)
        
        # UFW Status
        self._update_ufw_status()
        
        # Show buttons
        self.timeshift_row.show_all()
        self.grub_btrfs_row.show_all()
        self.dejadup_row.show_all()
        self.btrfs_row.show_all()
        self.gufw_row.show_all()
        self.portmaster_row.show_all()
        self.protonvpn_row.show_all()
        self.surfshark_row.show_all()
        self.mozilla_vpn_row.show_all()
        self.clamtk_row.show_all()
        self.clamui_row.show_all()
        self.rkhunter_row.show_all()
        self.bleachbit_row.show_all()
        self.stacer_row.show_all()
        self.sweeper_row.show_all()
        self.soplos_sys_cleaner_row.show_all()
    
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
    
    def _update_stacer_button(self):
        """Update Stacer button (AppImage from GitHub)."""
        stacer_path = os.path.expanduser('~/AppImages/Stacer.AppImage')
        is_installed = os.path.exists(stacer_path)
        
        if is_installed:
            uninstall_btn = Gtk.Button(label=_("Uninstall"))
            uninstall_btn.get_style_context().add_class("destructive-action")
            uninstall_btn.connect('clicked', lambda w: self._on_uninstall_stacer())
            self.stacer_row.pack_start(uninstall_btn, False, False, 0)
            
            installed_label = Gtk.Label(label=_("Installed"))
            installed_label.get_style_context().add_class("success")
            self.stacer_row.pack_start(installed_label, False, False, 10)
            
            configure_btn = Gtk.Button(label=_("Open Stacer"))
            configure_btn.get_style_context().add_class("suggested-action")
            configure_btn.connect('clicked', lambda w: self._on_configure_package('stacer'))
            self.stacer_row.pack_start(configure_btn, False, False, 0)
        else:
            install_btn = Gtk.Button(label=_("Install"))
            install_btn.get_style_context().add_class("suggested-action")
            install_btn.connect('clicked', lambda w: self._on_install_stacer())
            self.stacer_row.pack_start(install_btn, False, False, 0)
    
    def _on_install_stacer(self):
        """Install Stacer as AppImage."""
        script_content = (
            "#!/bin/bash\n"
            "set -e\n"
            "mkdir -p \"$HOME/AppImages/.icons\"\n"
            'wget -q -O "$HOME/AppImages/Stacer.AppImage" "https://github.com/oguzhaninan/Stacer/releases/download/v1.1.0/Stacer-1.1.0-x64.AppImage"\n'
            "chmod +x \"$HOME/AppImages/Stacer.AppImage\"\n"
            "mkdir -p \"$HOME/.local/share/applications\"\n"
            # Getting an icon to put in .icons
            'wget -q -O "$HOME/AppImages/.icons/stacer.png" "https://raw.githubusercontent.com/oguzhaninan/Stacer/master/stacer/images/stacer.png" || true\n'
            "cat > \"$HOME/.local/share/applications/stacer.desktop\" << EOF\n"
            "[Desktop Entry]\n"
            "Name=Stacer\n"
            "Exec=$HOME/AppImages/Stacer.AppImage\n"
            "Icon=$HOME/AppImages/.icons/stacer.png\n"
            "Type=Application\n"
            "Categories=System;\n"
            "Comment=Modern system optimizer with resource monitoring\n"
            "EOF\n"
            f"echo \"{_('Installation complete.')}\"\n"
        )
        script_path = "/tmp/install-stacer.sh"
        with open(script_path, "w") as f:
            f.write(script_content)
        os.chmod(script_path, 0o755)
        # Run normally without pkexec as it's in the user's home
        self.command_runner.run_command(f"bash {script_path}", self._on_operation_complete)
    
    def _on_uninstall_stacer(self):
        """Uninstall Stacer AppImage."""
        script_content = (
            "#!/bin/bash\n"
            "set -e\n"
            "rm -f \"$HOME/AppImages/Stacer.AppImage\"\n"
            "rm -f \"$HOME/AppImages/.icons/stacer.png\"\n"
            "rm -f \"$HOME/.local/share/applications/stacer.desktop\"\n"
            f"echo \"{_('Uninstallation complete.')}\"\n"
        )
        script_path = "/tmp/uninstall-stacer.sh"
        with open(script_path, "w") as f:
            f.write(script_content)
        os.chmod(script_path, 0o755)
        self.command_runner.run_command(f"bash {script_path}", self._on_operation_complete)
    
    def _is_flatpak_installed(self, flatpak_id):
        """Check if a Flatpak app is installed."""
        try:
            result = subprocess.run(
                ['flatpak', 'info', flatpak_id],
                capture_output=True, text=True
            )
            return result.returncode == 0
        except Exception:
            return False

    def _is_portmaster_installed(self):
        """Detect Portmaster via dpkg status OR presence of installation directory."""
        if self._is_package_installed('portmaster'):
            return True
        return os.path.isdir('/opt/safing/portmaster')

    def _update_portmaster_button(self):
        """Update Portmaster button (.deb installer)."""
        is_installed = self._is_portmaster_installed()

        if is_installed:
            uninstall_btn = Gtk.Button(label=_("Uninstall"))
            uninstall_btn.get_style_context().add_class("destructive-action")
            uninstall_btn.connect('clicked', lambda w: self._on_uninstall_portmaster())
            self.portmaster_row.pack_start(uninstall_btn, False, False, 0)

            installed_label = Gtk.Label(label=_("Installed"))
            installed_label.get_style_context().add_class("success")
            self.portmaster_row.pack_start(installed_label, False, False, 10)

            open_btn = Gtk.Button(label=_("Open Portmaster"))
            open_btn.get_style_context().add_class("suggested-action")
            open_btn.connect('clicked', lambda w: self._on_open_portmaster())
            self.portmaster_row.pack_start(open_btn, False, False, 0)

            if self._is_ufw_active():
                warning_lbl = Gtk.Label()
                warning_lbl.set_markup(f"<span color='#ffb86c'>⚠ {_('UFW is active — consider disabling it to avoid conflicts with Portmaster')}</span>")
                warning_lbl.set_line_wrap(True)
                self.portmaster_row.pack_start(warning_lbl, False, False, 10)
        else:
            install_btn = Gtk.Button(label=_("Install"))
            install_btn.get_style_context().add_class("suggested-action")
            install_btn.connect('clicked', lambda w: self._on_install_portmaster())
            self.portmaster_row.pack_start(install_btn, False, False, 0)

    def _on_uninstall_portmaster(self):
        """Uninstall Portmaster completely (purge + remove leftover files)."""
        script = "/tmp/uninstall-portmaster.sh"
        with open(script, "w") as f:
            f.write("#!/bin/bash\n")
            f.write("pkexec apt purge -y portmaster 2>/dev/null || true\n")
            f.write("rm -rf /opt/safing\n")
            f.write("rm -f /usr/share/applications/portmaster.desktop\n")
            f.write(f"echo '{_('Uninstallation complete.')}'\n")
        os.chmod(script, 0o755)
        self.command_runner.run_command(f"bash {script}", self._on_operation_complete)

    def _on_open_portmaster(self):
        """Launch Portmaster UI."""
        try:
            subprocess.Popen(['portmaster'])
        except Exception as e:
            print(f"Error launching Portmaster: {e}")

    def _on_install_portmaster(self):
        """Install Portmaster full package using version from Safing update index."""
        script = "/tmp/install-portmaster.sh"
        with open(script, "w") as f:
            f.write("#!/bin/bash\n")
            f.write("set -e\n")
            f.write("VERSION=$(curl -s https://updates.safing.io/stable.v3.json | python3 -c \"import json,sys; print(json.load(sys.stdin)['Version'])\")\n")
            f.write("if [ -z \"$VERSION\" ]; then echo 'Error: could not get Portmaster version'; exit 1; fi\n")
            f.write("echo \"Downloading Portmaster $VERSION...\"\n")
            f.write("wget -q --show-progress -O /tmp/portmaster-installer.deb \"https://updates.safing.io/latest/linux_amd64/packages/Portmaster_${VERSION}_amd64.deb\"\n")
            f.write("pkexec apt install -y /tmp/portmaster-installer.deb\n")
            f.write("rm -f /tmp/portmaster-installer.deb\n")
            f.write(f"echo '{_('Installation complete.')}'\n")
        os.chmod(script, 0o755)
        self.command_runner.run_command(f"bash {script}", self._on_operation_complete)

    def _update_protonvpn_button(self):
        """Update Proton VPN button (Flatpak)."""
        flatpak_id = 'com.protonvpn.www'
        is_installed = self._is_flatpak_installed(flatpak_id)

        if is_installed:
            uninstall_btn = Gtk.Button(label=_("Uninstall"))
            uninstall_btn.get_style_context().add_class("destructive-action")
            uninstall_btn.connect('clicked', lambda w: self._on_uninstall_flatpak(flatpak_id))
            self.protonvpn_row.pack_start(uninstall_btn, False, False, 0)

            installed_label = Gtk.Label(label=_("Installed"))
            installed_label.get_style_context().add_class("success")
            self.protonvpn_row.pack_start(installed_label, False, False, 10)

            open_btn = Gtk.Button(label=_("Open Proton VPN"))
            open_btn.get_style_context().add_class("suggested-action")
            open_btn.connect('clicked', lambda w: subprocess.Popen(['flatpak', 'run', flatpak_id]))
            self.protonvpn_row.pack_start(open_btn, False, False, 0)
        else:
            install_btn = Gtk.Button(label=_("Install"))
            install_btn.get_style_context().add_class("suggested-action")
            install_btn.connect('clicked', lambda w: self._on_install_flatpak(flatpak_id))
            self.protonvpn_row.pack_start(install_btn, False, False, 0)

    def _update_surfshark_button(self):
        """Update Surfshark button (Flatpak)."""
        flatpak_id = 'com.surfshark.Surfshark'
        is_installed = self._is_flatpak_installed(flatpak_id)

        if is_installed:
            uninstall_btn = Gtk.Button(label=_("Uninstall"))
            uninstall_btn.get_style_context().add_class("destructive-action")
            uninstall_btn.connect('clicked', lambda w: self._on_uninstall_flatpak(flatpak_id))
            self.surfshark_row.pack_start(uninstall_btn, False, False, 0)

            installed_label = Gtk.Label(label=_("Installed"))
            installed_label.get_style_context().add_class("success")
            self.surfshark_row.pack_start(installed_label, False, False, 10)

            open_btn = Gtk.Button(label=_("Open Surfshark"))
            open_btn.get_style_context().add_class("suggested-action")
            open_btn.connect('clicked', lambda w: subprocess.Popen(['flatpak', 'run', flatpak_id]))
            self.surfshark_row.pack_start(open_btn, False, False, 0)
        else:
            install_btn = Gtk.Button(label=_("Install"))
            install_btn.get_style_context().add_class("suggested-action")
            install_btn.connect('clicked', lambda w: self._on_install_flatpak(flatpak_id))
            self.surfshark_row.pack_start(install_btn, False, False, 0)

    def _update_mozilla_vpn_button(self):
        """Update Mozilla VPN button (Flatpak)."""
        flatpak_id = 'org.mozilla.vpn'
        is_installed = self._is_flatpak_installed(flatpak_id)

        if is_installed:
            uninstall_btn = Gtk.Button(label=_("Uninstall"))
            uninstall_btn.get_style_context().add_class("destructive-action")
            uninstall_btn.connect('clicked', lambda w: self._on_uninstall_flatpak(flatpak_id))
            self.mozilla_vpn_row.pack_start(uninstall_btn, False, False, 0)

            installed_label = Gtk.Label(label=_("Installed"))
            installed_label.get_style_context().add_class("success")
            self.mozilla_vpn_row.pack_start(installed_label, False, False, 10)

            open_btn = Gtk.Button(label=_("Open Mozilla VPN"))
            open_btn.get_style_context().add_class("suggested-action")
            open_btn.connect('clicked', lambda w: subprocess.Popen(['flatpak', 'run', flatpak_id]))
            self.mozilla_vpn_row.pack_start(open_btn, False, False, 0)
        else:
            install_btn = Gtk.Button(label=_("Install"))
            install_btn.get_style_context().add_class("suggested-action")
            install_btn.connect('clicked', lambda w: self._on_install_flatpak(flatpak_id))
            self.mozilla_vpn_row.pack_start(install_btn, False, False, 0)

    def _update_clamui_button(self):
        """Update ClamUI button (Flatpak)."""
        flatpak_id = 'io.github.linx_systems.ClamUI'
        is_installed = self._is_flatpak_installed(flatpak_id)

        if is_installed:
            uninstall_btn = Gtk.Button(label=_("Uninstall"))
            uninstall_btn.get_style_context().add_class("destructive-action")
            uninstall_btn.connect('clicked', lambda w: self._on_uninstall_flatpak(flatpak_id))
            self.clamui_row.pack_start(uninstall_btn, False, False, 0)

            installed_label = Gtk.Label(label=_("Installed"))
            installed_label.get_style_context().add_class("success")
            self.clamui_row.pack_start(installed_label, False, False, 10)

            open_btn = Gtk.Button(label=_("Open ClamUI"))
            open_btn.get_style_context().add_class("suggested-action")
            open_btn.connect('clicked', lambda w: subprocess.Popen(['flatpak', 'run', flatpak_id]))
            self.clamui_row.pack_start(open_btn, False, False, 0)
        else:
            install_btn = Gtk.Button(label=_("Install"))
            install_btn.get_style_context().add_class("suggested-action")
            install_btn.connect('clicked', lambda w: self._on_install_flatpak(flatpak_id))
            self.clamui_row.pack_start(install_btn, False, False, 0)

    def _on_install_flatpak(self, flatpak_id):
        """Install a Flatpak application."""
        script_path = f"/tmp/install-{flatpak_id.split('.')[-1].lower()}.sh"
        with open(script_path, "w") as f:
            f.write(f"#!/bin/bash\nflatpak install -y flathub {flatpak_id}\necho \"{_('Installation complete.')}\"\n")
        os.chmod(script_path, 0o755)
        self.command_runner.run_command(f"bash {script_path}", self._on_operation_complete)

    def _on_uninstall_flatpak(self, flatpak_id):
        """Uninstall a Flatpak application."""
        script_path = f"/tmp/uninstall-{flatpak_id.split('.')[-1].lower()}.sh"
        with open(script_path, "w") as f:
            f.write(f"#!/bin/bash\nflatpak uninstall -y {flatpak_id}\necho \"{_('Uninstallation complete.')}\"\n")
        os.chmod(script_path, 0o755)
        self.command_runner.run_command(f"bash {script_path}", self._on_operation_complete)

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
            elif package == 'stacer':
                stacer_path = os.path.expanduser('~/AppImages/Stacer.AppImage')
                subprocess.Popen([stacer_path])
            elif package == 'sweeper':
                subprocess.Popen(['sweeper'])
            elif package == 'soplos-sys-cleaner':
                subprocess.Popen(['soplos-sys-cleaner'])
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

