"""
GNOME Software Management Tab for Soplos Welcome.
Optimized software management interface for GNOME desktop environment.
"""

import gi
import os
import subprocess
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, GLib

from core.i18n_manager import _
from utils.command_runner import CommandRunner
from config.paths import BASE_DIR


class SoftwareGnomeTab(Gtk.Box):
    """
    GNOME-optimized software management tab.
    Features modern GNOME software managers and Flatpak integration.
    """
    
    def __init__(self, i18n_manager, theme_manager, parent_window, progress_bar, progress_label):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        
        self.i18n_manager = i18n_manager
        self.theme_manager = theme_manager
        self.parent_window = parent_window
        self.progress_bar = progress_bar
        self.progress_label = progress_label
        
        # Create CommandRunner
        self.command_runner = CommandRunner(self.progress_bar, self.progress_label, self.parent_window)
        
        # Software tracking for button updates
        self.software_buttons = {}
        
        self.set_border_width(10)
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the GNOME software interface."""
        # Main container - centered (Standardized with XFCE)
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        main_box.set_halign(Gtk.Align.CENTER)
        self.pack_start(main_box, True, True, 0)
        
        # Top buttons - Modern repository management
        self._create_repo_buttons(main_box)
        
        # Software grid
        self._create_software_grid(main_box)
        
        # Bottom buttons - GNOME-specific configurations
        self._create_config_buttons(main_box)
        
        self.show_all()
    
    def _create_repo_buttons(self, parent):
        """Create repository management buttons for GNOME."""
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        parent.pack_start(button_box, False, False, 5)
        

        
        # Update
        update_button = Gtk.Button(label=_("Update"))
        update_button.connect("clicked", self._on_update_clicked)
        button_box.pack_start(update_button, True, True, 0)
        
        # Upgrade
        upgrade_button = Gtk.Button(label=_("Upgrade"))
        upgrade_button.connect("clicked", self._on_upgrade_clicked)
        button_box.pack_start(upgrade_button, True, True, 0)
    
    def _create_software_grid(self, parent):
        """Create the software applications grid optimized for GNOME."""
        # Grid for software options
        software_grid = Gtk.Grid()
        software_grid.set_row_spacing(15)
        software_grid.set_column_spacing(15)
        software_grid.set_halign(Gtk.Align.CENTER)
        parent.pack_start(software_grid, False, False, 15)
        
        # Path to software icons
        icons_path = os.path.join(BASE_DIR, "assets/icons/software")
        
        # Software options optimized for GNOME
        software_options = [
            (_("Synaptic"), "synaptic", "synaptic.png"),
            (_("Gdebi"), "gdebi gdebi-core", "gdebi.png"),
            (_("GNOME Software"), "gnome-software package-update-indicator", "gnome-software.png"),
            (_("Flatpak"), "flatpak gnome-software-plugin-flatpak", "flatpak.png"),
            (_("Snap"), "snapd gnome-software-plugin-snap", "snap.png"),
            (_("Repo Selector"), "soplos-repo-selector", "reposelector.png")
        ]
        
        # Create software buttons
        row = 0
        col = 0
        for name, packages, icon_name in software_options:
            # Container for each software
            app_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
            app_container.set_size_request(140, 140)
            
            # Icon
            icon_path = os.path.join(icons_path, icon_name)
            icon = self._load_icon(icon_path, 48)
            app_container.pack_start(icon, False, False, 0)
            
            # Label
            label = Gtk.Label(label=name)
            label.set_line_wrap(True)
            label.set_justify(Gtk.Justification.CENTER)
            app_container.pack_start(label, False, False, 0)
            
            # Button - special handling for Repo Selector
            main_package = packages.split()[0]
            if main_package == "soplos-repo-selector":
                # Create Launch button for Repo Selector
                button = Gtk.Button(label=_("Open"))
                button.get_style_context().add_class("suggested-action")
                button.connect("clicked", self._on_repo_selector_clicked)
            else:
                # Normal install/uninstall button
                button = self._create_software_button(main_package, packages)
            
            app_container.pack_start(button, False, False, 0)
            
            # Store reference for updates (only for installable packages)
            if main_package != "soplos-repo-selector":
                self.software_buttons[main_package] = {
                    'container': app_container,
                    'packages': packages
                }
            
            software_grid.attach(app_container, col, row, 1, 1)
            
            col += 1
            if col >= 3:  # 3 columns
                col = 0
                row += 1
    
    def _create_config_buttons(self, parent):
        """Create GNOME-specific configuration buttons."""
        config_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        parent.pack_start(config_box, False, False, 5)
        
        # Add Flathub (prioritized for GNOME)
        flathub_button = Gtk.Button(label=_("Add Flathub"))
        flathub_button.get_style_context().add_class("suggested-action")
        flathub_button.connect("clicked", self._on_flathub_clicked)
        config_box.pack_start(flathub_button, True, True, 0)
        

        
        # Clean system
        clean_button = Gtk.Button(label=_("Clean System"))
        clean_button.connect("clicked", self._on_clean_clicked)
        config_box.pack_start(clean_button, True, True, 0)
    
    def _create_repo_selector_column(self, parent):
        """Create the Soplos Repo Selector promotion column."""
        right_column = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        right_column.set_size_request(250, -1)
        parent.pack_start(right_column, False, False, 0)
        
        # Large icon
        repo_icon_path = os.path.join(BASE_DIR, "assets/icons/software/reposelector.png")
        try:
            repo_icon = self._load_icon(repo_icon_path, 80)
        except:
            repo_icon = Gtk.Image.new_from_icon_name("system-software-install", Gtk.IconSize.DIALOG)
        right_column.pack_start(repo_icon, False, False, 0)
        
        # Title
        title = Gtk.Label()
        title.set_markup(f"<span size='large' weight='bold'>{_('Soplos Repository Manager')}</span>")
        title.set_justify(Gtk.Justification.CENTER)
        title.set_line_wrap(True)
        right_column.pack_start(title, False, False, 0)
        
        # Description
        description = Gtk.Label(label=_("Manage repositories and modern software sources integrated with GNOME Software."))
        description.set_justify(Gtk.Justification.CENTER)
        description.set_line_wrap(True)
        right_column.pack_start(description, False, False, 0)
        
        # Launch button
        launch_button = Gtk.Button(label=_("Launch Repository Manager"))
        launch_button.get_style_context().add_class("suggested-action")
        launch_button.connect("clicked", self._on_repo_selector_clicked)
        right_column.pack_start(launch_button, False, False, 0)
    
    def _load_icon(self, icon_path, size=48):
        """Load icon with fallback support."""
        try:
            if os.path.exists(icon_path):
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    icon_path, size, size, True
                )
                return Gtk.Image.new_from_pixbuf(pixbuf)
        except Exception as e:
            print(f"Error loading icon {icon_path}: {e}")
        
        # Fallback to system icon
        return Gtk.Image.new_from_icon_name("application-x-executable", Gtk.IconSize.DIALOG)
    
    def _is_package_installed(self, package_name):
        """Check if a package is installed."""
        try:
            result = subprocess.run(
                ["dpkg-query", "-W", "-f=${Status}", package_name],
                capture_output=True, text=True
            )
            return "install ok installed" in result.stdout
        except Exception as e:
            print(f"Error checking package {package_name}: {e}")
            return False
    
    def _create_software_button(self, package_name, packages):
        """Create install/uninstall button based on package status."""
        is_installed = self._is_package_installed(package_name)
        
        if is_installed:
            button = Gtk.Button(label=_("Uninstall"))
            button.get_style_context().add_class("destructive-action")
            button.connect("clicked", self._on_uninstall_clicked, packages, package_name)
        else:
            button = Gtk.Button(label=_("Install"))
            button.get_style_context().add_class("suggested-action")
            button.connect("clicked", self._on_install_clicked, packages, package_name)
        
        button.set_use_underline(True)
        return button
    
    def _update_software_button(self, package_name):
        """Update button state after installation/removal."""
        if package_name not in self.software_buttons:
            return
            
        container = self.software_buttons[package_name]['container']
        packages = self.software_buttons[package_name]['packages']
        
        # Find current button (last child)
        children = container.get_children()
        if len(children) < 3:
            return
            
        old_button = children[-1]
        
        # Create new button
        new_button = self._create_software_button(package_name, packages)
        
        # Replace button
        container.remove(old_button)
        container.pack_start(new_button, False, False, 0)
        new_button.show()
        
        print(f"✅ Button updated for {package_name}")
    
    def _create_and_run_script(self, script_content, script_name, package_to_update=None, on_complete=None):
        """Create and execute installation/removal scripts."""
        script_path = f"/tmp/{script_name}"
        try:
            with open(script_path, "w") as f:
                f.write("#!/bin/bash\n")
                f.write("set -e\n")
                f.write(script_content)
                f.write(f"\necho '{_('Operation completed successfully')}'\n")
                f.write("sleep 2\n")
            os.chmod(script_path, 0o755)
            
            # Run with progress tracking
            if package_to_update:
                self.command_runner.run_command(
                    script_path, 
                    lambda: self._on_operation_complete(True, package_to_update)
                )
            else:
                self.command_runner.run_command(script_path, on_complete)
                
        except Exception as e:
            print(f"Error creating script {script_name}: {e}")
    
    def _on_operation_complete(self, success, package_to_update):
        """Callback after installation/removal operation."""
        if package_to_update:
            print(f"Operation completed for {package_to_update}, success: {success}")
            # Update button after a delay
            GLib.timeout_add(3000, lambda: self._update_software_button(package_to_update))
    
    # Event handlers
    def _on_repo_selector_clicked(self, widget):
        """Launch Soplos Repository Selector."""
        try:
            subprocess.Popen(["soplos-repo-selector"])
        except Exception as e:
            print(f"Error launching repository selector: {e}")
    
    def _on_update_clicked(self, widget):
        """Update package repositories with GNOME integration and check for upgrades."""
        script_content = """
# Update package lists
pkexec apt update
# Also update Flatpak
flatpak update --appstream
"""
        self._create_and_run_script(
            script_content, 
            "update-repos-gnome.sh",
            on_complete=self._check_updates
        )
    
    def _check_updates(self):
        """Check for upgradable packages after update."""
        try:
            # Run apt list --upgradable
            # We do NOT force locale here, we parse the structure
            result = subprocess.run(
                ["apt", "list", "--upgradable"],
                capture_output=True,
                text=True
            )
            
            output = result.stdout
            lines = output.split('\n')
            
            # Filter relevant lines
            packages = []
            for line in lines:
                # apt list output format is typically: package/suite version arch [status]
                # We look for lines containing '/' which separates package and suite
                if '/' in line and ('Listing...' not in line and 'Listando...' not in line):
                    try:
                        parts = line.split('/')
                        if len(parts) > 1:
                            pkg_name = parts[0]
                            # Try to get version info
                            rest = parts[1]
                            version_parts = rest.split()
                            version_info = version_parts[1] if len(version_parts) > 1 else ""
                            packages.append(f"{pkg_name} ({version_info})")
                    except Exception:
                        continue
            
            self._show_update_dialog(packages)
            
        except Exception as e:
            print(f"Error checking updates: {e}")
            self._show_update_dialog([])

    def _show_update_dialog(self, packages):
        """Show dialog with available updates."""
        if not packages:
            dialog = Gtk.MessageDialog(
                transient_for=self.parent_window,
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text=_("System Up to Date")
            )
            dialog.format_secondary_text(_("No packages available to update at this time."))
            dialog.run()
            dialog.destroy()
            return

        # Create custom dialog for updates
        dialog = Gtk.Dialog(title=_("Available Updates"), transient_for=self.parent_window, flags=0)
        dialog.add_buttons(
            _("Cancel"), Gtk.ResponseType.CANCEL,
            _("Update All"), Gtk.ResponseType.OK
        )
        
        # Content area
        box = dialog.get_content_area()
        box.set_spacing(10)
        box.set_margin_top(10)
        box.set_margin_bottom(10)
        box.set_margin_left(10)
        box.set_margin_right(10)
        
        # Header
        header = Gtk.Label()
        header.set_markup(f"<b>{len(packages)} {_('updates available')}</b>")
        box.pack_start(header, False, False, 0)
        
        # Scrolled window for package list
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_min_content_height(200)
        scrolled.set_min_content_width(350)
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        
        # Package list
        list_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        for pkg in packages:
            label = Gtk.Label(label=pkg)
            label.set_halign(Gtk.Align.START)
            list_box.pack_start(label, False, False, 0)
        
        scrolled.add(list_box)
        box.pack_start(scrolled, True, True, 0)
        
        dialog.show_all()
        response = dialog.run()
        dialog.destroy()
        
        if response == Gtk.ResponseType.OK:
            self._on_upgrade_clicked(None)

    def _on_upgrade_clicked(self, widget):
        """Upgrade system packages with GNOME integration."""
        script_content = """
# System upgrade
pkexec apt upgrade -y
# Update Flatpak apps
flatpak update -y
"""
        self._create_and_run_script(script_content, "upgrade-system-gnome.sh")
    
    def _on_install_clicked(self, widget, packages, main_package):
        """Install software packages."""
        script_content = f"pkexec apt install -y {packages}"
        self._create_and_run_script(script_content, f"install-{main_package}.sh", main_package)
    
    def _on_uninstall_clicked(self, widget, packages, main_package):
        """Uninstall software packages."""
        script_content = f"pkexec apt remove -y {packages}"
        self._create_and_run_script(script_content, f"uninstall-{main_package}.sh", main_package)
    
    def _on_flathub_clicked(self, widget):
        """Add Flathub repository."""
        script_content = "flatpak remote-add --if-not-exists --user flathub https://dl.flathub.org/repo/flathub.flatpakrepo"
        self._create_and_run_script(script_content, "add-flathub-gnome.sh")
    
    def _on_extensions_clicked(self, widget):
        """Configure GNOME Extensions."""
        try:
            # Try to launch GNOME Extensions Manager
            subprocess.Popen(["gnome-shell-extension-prefs"])
        except FileNotFoundError:
            try:
                # Fallback to Extensions app if available
                subprocess.Popen(["gnome-extensions"])
            except FileNotFoundError:
                # Open extensions website
                subprocess.Popen(["xdg-open", "https://extensions.gnome.org/"])
    
    def _on_clean_clicked(self, widget):
        """Clean system packages with GNOME integration."""
        script_content = """
# Clean APT packages
pkexec sh -c "apt autoremove -y && apt clean"
# Clean Flatpak
flatpak uninstall --unused -y
"""
        self._create_and_run_script(script_content, "clean-system-gnome.sh")
