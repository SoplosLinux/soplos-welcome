"""
Recommended tab implementation for Soplos Welcome.
Shows curated applications based on desktop environment and user needs.
"""

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gtk, GdkPixbuf, GLib, Pango
import threading
import subprocess
import os
import urllib.request
from pathlib import Path

from config.software import get_all_categories


from config.paths import ICONS_DIR

class RecommendedTab(Gtk.Box):
    """Recommended applications tab with curated software selections."""
    
    def __init__(self, i18n_manager, theme_manager, parent_window, progress_bar, progress_label):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        
        self.i18n_manager = i18n_manager
        self.theme_manager = theme_manager
        self.parent_window = parent_window
        self.progress_bar = progress_bar
        self.progress_label = progress_label
        
        # Create CommandRunner
        from utils.command_runner import CommandRunner
        self.command_runner = CommandRunner(self.progress_bar, self.progress_label, self.parent_window)
        
        self.installing_packages = set()  # Track packages being installed
        self.package_status_cache = {}    # Cache for package installation status
        
        self.set_margin_left(20)
        self.set_margin_right(20)
        self.set_margin_top(20)
        self.set_margin_bottom(20)
        
        self._init_ui()

    def _init_ui(self):
        """Initialize the UI."""
        # Header
        header_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        
        title = Gtk.Label()
        title.set_markup(f'<span size="18000" weight="bold">{self.i18n_manager._("Recommended for You")}</span>')
        title.set_halign(Gtk.Align.START)
        header_box.pack_start(title, False, False, 0)
        
        subtitle = Gtk.Label(self.i18n_manager._("Curated applications based on your desktop environment"))
        subtitle.set_halign(Gtk.Align.START)
        subtitle.get_style_context().add_class('dim-label')
        header_box.pack_start(subtitle, False, False, 0)
        
        self.pack_start(header_box, False, False, 0)
        
        # Scrolled window for content
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_min_content_height(400)
        
        # Main content box
        self.content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        scrolled.add(self.content_box)
        
        self.pack_start(scrolled, True, True, 0)
        
        # Load content
        self._load_recommended_software()
    
    def _load_recommended_software(self):
        """Load recommended software categories."""
        categories = get_all_categories()
        
        # Show only selected categories with featured apps
        recommended_categories = ['browsers', 'comunications', 'office', 'multimedia', 'graphics', 'developer', 'gaming']
        
        for category_id in recommended_categories:
            if category_id in categories:
                category_data = categories[category_id]
                self._create_category_section(category_id, category_data, featured_only=False)
    
    def _create_category_section(self, category_id: str, category_data: dict, featured_only: bool = False):
        """Create a section for a recommended software category."""
        # Category frame
        frame = Gtk.Frame()
        frame.set_label_align(0.0, 0.5)
        frame.set_margin_bottom(10)
        
        # Category header
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        header_box.set_margin_left(10)
        header_box.set_margin_right(10)
        header_box.set_margin_top(5)
        header_box.set_margin_bottom(5)
        
        # Category icon
        category_icon = self._load_category_icon(category_id, category_data.get('icon'))
        if category_icon:
            header_box.pack_start(category_icon, False, False, 0)
        
        # Category title
        title_label = Gtk.Label()
        title_label.set_markup(f'<span size="14000" weight="bold">{category_data["title"]}</span>')
        title_label.set_halign(Gtk.Align.START)
        header_box.pack_start(title_label, False, False, 0)
        
        frame.set_label_widget(header_box)
        
        # Create SizeGroups for alignment
        if not hasattr(self, 'name_group'):
            self.name_group = Gtk.SizeGroup(mode=Gtk.SizeGroupMode.VERTICAL)
            self.desc_group = Gtk.SizeGroup(mode=Gtk.SizeGroupMode.VERTICAL)
            self.button_group = Gtk.SizeGroup(mode=Gtk.SizeGroupMode.VERTICAL)
        
        # Packages grid
        grid = Gtk.Grid()
        grid.set_column_spacing(15)
        grid.set_row_spacing(10)
        grid.set_column_homogeneous(True)  # Make all columns same width for alignment
        grid.set_margin_left(15)
        grid.set_margin_right(15)
        grid.set_margin_top(10)
        grid.set_margin_bottom(15)
        
        # Add packages to grid
        packages = category_data.get('packages', [])
        
        row = 0
        col = 0
        max_cols = 2
        
        for package in packages:
            package_widget = self._create_package_widget(category_id, package)
            grid.attach(package_widget, col, row, 1, 1)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        frame.add(grid)
        frame.show_all()
        self.content_box.pack_start(frame, False, False, 0)
    
    def _create_package_widget(self, category_id: str, package: dict) -> Gtk.Widget:
        """Create a widget for a single recommended package."""
        # Main container
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        box.set_margin_left(10)
        box.set_margin_right(10)
        box.set_margin_top(8)
        box.set_margin_bottom(8)
        
        # Package icon
        icon = self._load_package_icon(category_id, package.get('icon', ''))
        if icon:
            box.pack_start(icon, False, False, 0)
        
        # Package info
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        
        # Package name with official badge
        name_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        
        name_label = Gtk.Label()
        name_text = f'<span weight="bold">{package["name"]}</span>'
        name_label.set_markup(name_text)
        name_label.set_halign(Gtk.Align.START)
        name_box.pack_start(name_label, False, False, 0)
        
        # Add Flatpak badge ONLY when using flatpak
        install_method = self._get_install_method(package)
        if install_method == 'flatpak':
            flatpak_badge = Gtk.Label()
            flatpak_badge.set_markup('<span size="small" foreground="#888888" background="#333333"> Flatpak </span>')
            flatpak_badge.set_valign(Gtk.Align.CENTER)
            name_box.pack_start(flatpak_badge, False, False, 0)
        
        # Official badge
        if package.get('official', False):
            official_badge = Gtk.Image.new_from_icon_name("security-high-symbolic", Gtk.IconSize.MENU)
            official_badge.get_style_context().add_class('success-color')
            official_badge.set_tooltip_text(self.i18n_manager._("Official Package"))
            name_box.pack_start(official_badge, False, False, 0)
            
        # Add to SizeGroup for alignment
        if self.name_group:
            self.name_group.add_widget(name_box)
        
        info_box.pack_start(name_box, False, False, 0)
        
        # Package description
        desc_label = Gtk.Label(package.get('description', ''))
        desc_label.set_halign(Gtk.Align.START)
        desc_label.set_line_wrap(True)
        desc_label.set_max_width_chars(45)
        desc_label.set_lines(2)  # Always reserve space for 2 lines
        desc_label.set_ellipsize(Pango.EllipsizeMode.END)
        desc_label.set_size_request(-1, 40)  # Fixed height for alignment
        desc_label.get_style_context().add_class('dim-label')
        
        # Add to SizeGroup for alignment
        if self.desc_group:
            self.desc_group.add_widget(desc_label)
        
        info_box.pack_start(desc_label, False, False, 0)
        
        box.pack_start(info_box, True, True, 0)
        
        # Action button
        button_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        button_box.set_valign(Gtk.Align.CENTER)
        
        # Add to button SizeGroup for alignment
        if self.button_group:
            self.button_group.add_widget(button_box)
        
        # Check if package is being processed (installing/uninstalling)
        package_id = f"{category_id}:{package['name']}"
        is_processing = package_id in self.installing_packages
        
        if is_processing:
            # Processing state - Button disabled or showing status
            # Since we use global progress bar, we just show a disabled button or label
            processing_label = Gtk.Label(self.i18n_manager._("Processing..."))
            processing_label.get_style_context().add_class('dim-label')
            button_box.pack_start(processing_label, False, False, 0)
        else:
            # Check if package is installed (only if not processing)
            is_installed = self._is_package_installed(package)
            
            if is_installed:
                # Installed state - show uninstall button
                uninstall_button = Gtk.Button.new_with_label("Desinstalar")
                uninstall_button.get_style_context().add_class('destructive-action')
                uninstall_button.set_size_request(110, -1)
                uninstall_button.connect('clicked', self._on_uninstall_package, category_id, package)
                button_box.pack_start(uninstall_button, False, False, 0)
            else:
                # Not installed state
                install_button = Gtk.Button.new_with_label("Instalar")
                install_button.get_style_context().add_class('suggested-action')
                install_button.set_size_request(110, -1)
                install_button.connect('clicked', self._on_install_package, category_id, package)
                button_box.pack_start(install_button, False, False, 0)
        
        box.pack_start(button_box, False, False, 0)
        
        return box
    
    def _load_category_icon(self, category_id: str, specific_icon: str = None) -> Gtk.Widget:
        """Load and return a category icon."""
        try:
            icon_dir = Path(os.path.join(ICONS_DIR, category_id))
            
            # If specific icon is provided, try to load it first
            if specific_icon and icon_dir.exists():
                icon_path = icon_dir / specific_icon
                if icon_path.exists():
                    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                        str(icon_path), 24, 24, True
                    )
                    return Gtk.Image.new_from_pixbuf(pixbuf)

            # Fallback: Try to find a representative icon in the category folder
            if icon_dir.exists():
                # Use the first available icon as category icon
                for icon_file in icon_dir.glob("*.png"):
                    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                        str(icon_file), 24, 24, True
                    )
                    image = Gtk.Image.new_from_pixbuf(pixbuf)
                    return image
        except Exception as e:
            print(f"Error loading category icon for {category_id}: {e}")
        
        return None
    
    def _load_package_icon(self, category_id: str, icon_name: str) -> Gtk.Widget:
        """Load and return a package icon."""
        if not icon_name:
            return None
        
        try:
            icon_path = os.path.join(ICONS_DIR, category_id, icon_name)
            if os.path.exists(icon_path):
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    icon_path, 48, 48, True
                )
                image = Gtk.Image.new_from_pixbuf(pixbuf)
                return image
        except Exception as e:
            print(f"Error loading package icon {icon_name}: {e}")
        
        return None
    
    def _get_install_method(self, package: dict) -> str:
        """Determine the preferred installation method for a package."""
        # List of packages that MUST use Flatpak even if APT is available
        # This matches the behavior of previous versions (Tyron/Tyson)
        prefer_flatpak = [
            'Telegram', 'Discord', 'Signal', 'Element', 'WhatsApp',
            'LibreWolf', 'LibreOffice', 'OnlyOffice', 'WPS Office',
            'OpenShot', 'Kdenlive', 'Shotcut',
            'VSCodium', 'Zed',
            'Steam', 'Heroic Games Launcher', 'Bottles'
        ]
        
        if package['name'] in prefer_flatpak and package.get('flatpak'):
            return 'flatpak'
            
        # Check for custom installation handlers
        if package.get('name') == 'DaVinci Resolve':
            return 'davinci_resolve'

        # Check for custom installation commands
        if 'install_commands' in package:
            return 'custom'
            
        # Check for .deb URL installation
        if package.get('deb_url'):
            return 'deb'
            
        # Default Priority: APT > Flatpak
        if package.get('package'): # APT package
            return 'apt'
        elif package.get('flatpak'):
            return 'flatpak'
        
        return 'unknown'
    
    def _is_package_installed(self, package: dict) -> bool:
        """Check if a package is installed using the preferred method."""
        package_name = package['name']
        
        # Return cached result if available
        if package_name in self.package_status_cache:
            return self.package_status_cache[package_name]
            
        install_method = self._get_install_method(package)
        is_installed = False
        
        try:
            if (install_method == 'apt' or install_method == 'deb' or install_method == 'custom') and package.get('package'):
                result = subprocess.run(
                    ['dpkg', '-s', package['package']],
                    capture_output=True, text=True
                )
                is_installed = 'Status: install ok installed' in result.stdout
            
            elif install_method == 'flatpak' and package.get('flatpak'):
                result = subprocess.run(
                    ['flatpak', 'info', package['flatpak']],
                    capture_output=True, text=True
                )
                is_installed = result.returncode == 0
        
        except Exception:
            pass
            
        # Update cache
        self.package_status_cache[package_name] = is_installed
        return is_installed
    
    def _on_install_package(self, button, category_id: str, package: dict):
        """Handle package installation."""
        package_id = f"{category_id}:{package['name']}"
        
        if package_id in self.installing_packages:
            return  # Already installing
        
        self.installing_packages.add(package_id)
        
        install_method = self._get_install_method(package)
        command = ""
        script_name = ""
        
        if install_method == 'davinci_resolve':
            self._install_davinci_resolve(package)
            return

        if install_method == 'apt' and package.get('package'):
            command = f"pkexec apt install -y {package['package']}"
            script_name = f"install-{package['package']}.sh"
            
        elif install_method == 'flatpak' and package.get('flatpak'):
            command = f"flatpak install -y flathub {package['flatpak']}"
            script_name = f"install-{package['flatpak']}.sh"
            
        elif install_method == 'deb' and package.get('deb_url'):
            # Create a script for downloading and installing .deb
            deb_url = package['deb_url']
            pkg_name = package['package']
            command = f"""wget -O /tmp/{pkg_name}.deb "{deb_url}"
pkexec apt install -y /tmp/{pkg_name}.deb
rm -f /tmp/{pkg_name}.deb"""
            script_name = f"install-{pkg_name}.sh"
            
        elif install_method == 'custom' and package.get('install_commands'):
            # Custom installation commands
            pkg_name = package['package']
            # Join commands with newlines
            cmds = "\n".join(package['install_commands'])
            command = cmds
            script_name = f"install-{pkg_name}.sh"
        
        if command:
            self._create_and_run_script(command, script_name, package, is_install=True)

    def _on_uninstall_package(self, button, category_id: str, package: dict):
        """Handle package uninstallation."""
        package_id = f"{category_id}:{package['name']}"
        
        if package_id in self.installing_packages:
            return  # Already processing
        
        self.installing_packages.add(package_id)
        
        install_method = self._get_install_method(package)
        command = ""
        script_name = ""
        
        if (install_method == 'apt' or install_method == 'deb' or install_method == 'custom') and package.get('package'):
            command = f"pkexec apt remove -y {package['package']}"
            script_name = f"uninstall-{package['package']}.sh"
            
        elif install_method == 'flatpak' and package.get('flatpak'):
            command = f"flatpak uninstall -y {package['flatpak']}"
            script_name = f"uninstall-{package['flatpak']}.sh"
            
        if command:
            self._create_and_run_script(command, script_name, package, is_install=False)

    def _create_and_run_script(self, script_content, script_name, package, is_install):
        """Create and execute installation/removal scripts."""
        script_path = f"/tmp/{script_name}"
        try:
            with open(script_path, "w") as f:
                f.write("#!/bin/bash\n")
                f.write(script_content)
                f.write("\necho 'Operation completed successfully'\n")
            os.chmod(script_path, 0o755)
            
            # Run with CommandRunner - use pkexec to run entire script with privileges
            # For flatpak, run directly; for apt/deb, use pkexec
            if 'flatpak' in script_content:
                os.chmod(script_path, 0o755)
            
            # Run with CommandRunner
            # For flatpak, run directly
            # For apt/deb (inside script), run directly (pkexec is inside)
            # For custom scripts (install), run with pkexec (entire script as root)
            if package.get('install_commands') and is_install:
                final_command = f"pkexec {script_path}"
            else:
                final_command = script_path
            
            self.command_runner.run_command(
                final_command, 
                lambda: self._on_package_operation_complete(package, is_install)
            )
                
        except Exception as e:
            print(f"Error creating script {script_name}: {e}")
            # Cleanup on error
            package_id = f"recommended:{package['name']}" # Approximate ID reconstruction
            # We need the category_id but don't have it easily here. 
            # Let's just clear it from the set by name if possible or iterate
            # Ideally we pass category_id through, but for now let's just refresh
            self.installing_packages.clear() # Brute force cleanup
            self._refresh_content()

    def _on_package_operation_complete(self, package: dict, is_install: bool):
        """Handle completion of package operation."""
        # Invalidate cache
        if package['name'] in self.package_status_cache:
            del self.package_status_cache[package['name']]
            
        # Clear installing set - we need to remove by ID. 
        # Since we don't have category_id here easily, we'll iterate and remove matching names
        to_remove = set()
        for pid in self.installing_packages:
            if pid.endswith(f":{package['name']}"):
                to_remove.add(pid)
        
        for pid in to_remove:
            self.installing_packages.discard(pid)
            
        # Refresh UI
        GLib.idle_add(self._refresh_content)
    
    def _clear_status(self):
        """Clear the status message."""
        self.status_label.set_text("Listo")
        return False  # Don't repeat
    
    def _refresh_content(self):
        """Refresh the entire content area."""
        # Remove all children
        for child in self.content_box.get_children():
            child.destroy()
        
        # Reload content
        self._load_recommended_software()
        self.content_box.show_all()

    def _pulse_progress(self, progress_bar):
        """Pulse the progress bar."""
        # Stop pulsing if widget is destroyed or not mapped
        try:
            if progress_bar.get_mapped():
                progress_bar.pulse()
                return True
        except Exception:
            pass
        return False
    def _install_davinci_resolve(self, package_data):
        """Handle complex DaVinci Resolve installation."""
        # 1. Check dependencies
        deps_script = "pkexec apt install -y fakeroot xorriso"
        
        # 2. Show dialog explaining manual download
        dialog = Gtk.MessageDialog(
            transient_for=self.parent_window,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK_CANCEL,
            text=_("DaVinci Resolve Installation")
        )
        dialog.format_secondary_text(
            _("DaVinci Resolve requires manual download due to licensing.\n\n"
              "1. Go to blackmagicdesign.com and download the Linux version (ZIP).\n"
              "2. Click OK to select the downloaded file.\n"
              "3. We will convert it to a Debian package and install it.")
        )
        response = dialog.run()
        dialog.destroy()
        
        if response != Gtk.ResponseType.OK:
            return

        # 3. File Chooser
        file_filter = Gtk.FileFilter()
        file_filter.set_name("DaVinci Resolve Installer")
        file_filter.add_pattern("*.zip")
        file_filter.add_pattern("*.run")
        
        chooser = Gtk.FileChooserDialog(
            title=_("Select DaVinci Resolve Installer"),
            parent=self.parent_window,
            action=Gtk.FileChooserAction.OPEN
        )
        chooser.add_buttons(
            _("Cancel"), Gtk.ResponseType.CANCEL,
            _("Select"), Gtk.ResponseType.OK
        )
        chooser.add_filter(file_filter)
        
        response = chooser.run()
        filename = chooser.get_filename()
        chooser.destroy()
        
        if response != Gtk.ResponseType.OK or not filename:
            return

        # 4. Create installation script
        # We use a comprehensive script to handle extraction, conversion and installation
        script_content = f"""
# Install dependencies
{deps_script}

# Create temp dir
WORK_DIR=$(mktemp -d)
cd "$WORK_DIR"

echo "Working in $WORK_DIR"

# Copy installer
echo "Copying installer..."
cp "{filename}" .

# Extract if zip
if [[ "{filename}" == *.zip ]]; then
    echo "Extracting ZIP..."
    unzip -o "$(basename "{filename}")"
    RUN_FILE=$(ls *.run | head -n 1)
else
    RUN_FILE="$(basename "{filename}")"
fi

# Copy local MakeResolveDeb
echo "Copying local MakeResolveDeb..."
cp "/usr/local/bin/soplos-welcome/services/makeresolvedeb_1.8.3_multi.sh" .
MRD_SCRIPT="makeresolvedeb_1.8.3_multi.sh"
chmod +x "$MRD_SCRIPT"

# Run conversion
echo "Converting package (this may take a while)..."
./"$MRD_SCRIPT" "$RUN_FILE"

# Install generated DEB
DEB_FILE=$(ls *_amd64.deb | head -n 1)
if [ -f "$DEB_FILE" ]; then
    echo "Installing $DEB_FILE..."
    pkexec apt install -y "./$DEB_FILE"
else
    echo "Error: DEB file not generated"
    exit 1
fi

# Cleanup
cd ..
rm -rf "$WORK_DIR"
"""
        # We need to manually add to installing packages because _create_and_run_script expects it
        package_id = f"multimedia:DaVinci Resolve"
        self.installing_packages.add(package_id)
        self._refresh_content()
        
        # Run script
        self._create_and_run_script(script_content, "install-davinci.sh", package_data, is_install=True)
