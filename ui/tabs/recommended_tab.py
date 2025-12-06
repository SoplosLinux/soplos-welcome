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
from core.i18n_manager import _

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
        
        # Batch mode state
        self.batch_mode = False
        self.selected_apt = []
        self.selected_flatpak = []
        self.selected_deb_urls = []  # List of (url, package_name) tuples
        self.selected_custom = []  # List of (commands_list, package_name) tuples
        
        # Search state
        self.search_query = ""
        
        self.set_margin_left(20)
        self.set_margin_right(20)
        self.set_margin_top(20)
        self.set_margin_bottom(20)
        
        self._init_ui()

    def _init_ui(self):
        """Initialize the UI."""
        # Header
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        
        # Left side: titles
        titles_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        
        title = Gtk.Label()
        title.set_markup(f'<span size="18000" weight="bold">{self.i18n_manager._("Recommended for You")}</span>')
        title.set_halign(Gtk.Align.START)
        titles_box.pack_start(title, False, False, 0)
        
        subtitle = Gtk.Label(self.i18n_manager._("Curated applications based on your desktop environment"))
        subtitle.set_halign(Gtk.Align.START)
        subtitle.get_style_context().add_class('dim-label')
        titles_box.pack_start(subtitle, False, False, 0)
        
        header_box.pack_start(titles_box, True, True, 0)
        
        # Right side: batch mode toggle button
        self.batch_toggle_button = Gtk.Button.new_with_label(_("Multiple Selection"))
        self.batch_toggle_button.set_valign(Gtk.Align.CENTER)
        self.batch_toggle_button.connect('clicked', self._on_toggle_batch_mode)
        header_box.pack_end(self.batch_toggle_button, False, False, 0)
        
        # Search entry (to the left of batch button)
        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_placeholder_text(_("Search programs..."))
        self.search_entry.set_max_width_chars(30)
        self.search_entry.set_valign(Gtk.Align.CENTER)
        self.search_entry.connect('search-changed', self._on_search_changed)
        header_box.pack_end(self.search_entry, False, False, 0)
        
        self.pack_start(header_box, False, False, 0)
        
        # Scrolled window for content
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_min_content_height(400)
        
        # Main content box
        self.content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.content_box.set_margin_right(10) # Prevent scrollbar overlap
        scrolled.add(self.content_box)
        
        self.pack_start(scrolled, True, True, 0)
        
        # Bottom batch action bar (initially hidden)
        self.batch_bar = Gtk.ActionBar()
        
        batch_bar_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        
        # Left side: Select/Deselect all buttons
        select_all_button = Gtk.Button.new_with_label(_("Select All"))
        select_all_button.connect('clicked', self._on_select_all)
        batch_bar_box.pack_start(select_all_button, False, False, 0)
        
        deselect_all_button = Gtk.Button.new_with_label(_("Deselect All"))
        deselect_all_button.connect('clicked', self._on_deselect_all)
        batch_bar_box.pack_start(deselect_all_button, False, False, 0)
        
        # Center: Counter
        self.batch_label = Gtk.Label(_("0 programs selected"))
        self.batch_label.get_style_context().add_class('dim-label')
        batch_bar_box.pack_start(self.batch_label, True, True, 0)
        
        # Right side: Install button
        batch_install_button = Gtk.Button.new_with_label(_("Install Selected"))
        batch_install_button.get_style_context().add_class('suggested-action')
        batch_install_button.connect('clicked', self._on_install_batch)
        batch_bar_box.pack_end(batch_install_button, False, False, 0)
        
        self.batch_bar.set_center_widget(batch_bar_box)
        batch_bar_box.show_all()  # Show all internal widgets
        self.pack_end(self.batch_bar, False, False, 0)
        self.batch_bar.set_no_show_all(True)  # Prevent showing with parent's show_all
        self.batch_bar.hide()  # Hide initially
        
        # Load content
        self._load_recommended_software()
    
    def _load_recommended_software(self):
        """Load recommended software categories."""
        categories = get_all_categories()
        
        # Show only selected categories with featured apps
        recommended_categories = ['browsers', 'comunications', 'office', 'multimedia', 'graphics', 'developer', 'gaming']
        
        has_results = False
        for category_id in recommended_categories:
            if category_id in categories:
                category_data = categories[category_id]
                if self._create_category_section(category_id, category_data, featured_only=False):
                    has_results = True
        
        # Show "no results" message if search query is active but nothing matches
        if self.search_query and not has_results:
            no_results_label = Gtk.Label()
            no_results_label.set_markup(f'<span size="12000">{_("No results found for")} "{self.search_query}"</span>')
            no_results_label.get_style_context().add_class('dim-label')
            no_results_label.set_margin_top(50)
            self.content_box.pack_start(no_results_label, True, True, 0)
    
    def _create_category_section(self, category_id: str, category_data: dict, featured_only: bool = False) -> bool:
        """Create a section for a recommended software category.
        
        Returns:
            bool: True if any packages were shown, False otherwise
        """
        # Filter packages based on search query
        packages = category_data.get('packages', [])
        if self.search_query:
            query_lower = self.search_query.lower()
            packages = [
                pkg for pkg in packages
                if query_lower in pkg['name'].lower() or query_lower in pkg.get('description', '').lower()
            ]
        
        # Skip category if no packages match
        if not packages:
            return False
        
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
        
        # Add packages to grid (already filtered)
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
        return True
    
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
            flatpak_badge.set_markup(f'<span size="small" foreground="#888888" background="#333333"> {_("Flatpak")} </span>')
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
        
        # Check if this package should be excluded from batch mode (only DaVinci Resolve)
        install_method = self._get_install_method(package)
        exclude_from_batch = install_method == 'davinci_resolve'
        
        # BATCH MODE: Show checkbox for compatible packages
        if self.batch_mode and not exclude_from_batch and not is_processing:
            is_installed = self._is_package_installed(package)
            
            if not is_installed:
                # Show checkbox
                checkbox = Gtk.CheckButton()
                checkbox.set_valign(Gtk.Align.CENTER)
                
                # Pre-check if already selected
                if self._is_package_selected(package):
                    checkbox.set_active(True)
                
                checkbox.connect('toggled', self._on_checkbox_toggled, package, category_id)
                button_box.pack_start(checkbox, False, False, 0)
            else:
                # Already installed - show label
                installed_label = Gtk.Label(_("Installed"))
                installed_label.get_style_context().add_class('dim-label')
                button_box.pack_start(installed_label, False, False, 0)
        
        # NORMAL MODE or EXCLUDED PACKAGES: Show buttons
        elif is_processing:
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
                uninstall_button = Gtk.Button.new_with_label(_("Uninstall"))
                uninstall_button.get_style_context().add_class('destructive-action')
                uninstall_button.set_size_request(110, -1)
                uninstall_button.connect('clicked', self._on_uninstall_package, category_id, package)
                button_box.pack_start(uninstall_button, False, False, 0)
            else:
                # Not installed state
                install_button = Gtk.Button.new_with_label(_("Install"))
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
            command = f"""wget -q --show-progress -O /tmp/{pkg_name}.deb "{deb_url}"
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
                f.write(f"\necho '{_('Operation completed successfully')}'\n")
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
    
    def _on_toggle_batch_mode(self, button):
        """Toggle between normal and batch installation mode."""
        self.batch_mode = not self.batch_mode
        
        # Update button label
        if self.batch_mode:
            self.batch_toggle_button.set_label(_("Normal Mode"))
        else:
            self.batch_toggle_button.set_label(_("Multiple Selection"))
            # Clear selections when exiting batch mode
            self.selected_apt.clear()
            self.selected_flatpak.clear()
            self.selected_deb_urls.clear()
            self.selected_custom.clear()
            self.batch_bar.hide()
        
        # Rebuild content with new mode
        self._refresh_content()
    
    def _on_checkbox_toggled(self, checkbox, package, category_id):
        """Handle checkbox toggle in batch mode."""
        install_method = self._get_install_method(package)
        
        if checkbox.get_active():
            # Add to appropriate list
            if install_method == 'apt' and package.get('package'):
                if package['package'] not in self.selected_apt:
                    self.selected_apt.append(package['package'])
            elif install_method == 'flatpak' and package.get('flatpak'):
                if package['flatpak'] not in self.selected_flatpak:
                    self.selected_flatpak.append(package['flatpak'])
            elif install_method == 'deb' and package.get('deb_url'):
                deb_info = (package['deb_url'], package['package'])
                if deb_info not in self.selected_deb_urls:
                    self.selected_deb_urls.append(deb_info)
            elif install_method == 'custom' and package.get('install_commands'):
                custom_info = (package['install_commands'], package['package'])
                if custom_info not in self.selected_custom:
                    self.selected_custom.append(custom_info)
        else:
            # Remove from appropriate list
            if install_method == 'apt' and package['package'] in self.selected_apt:
                self.selected_apt.remove(package['package'])
            elif install_method == 'flatpak' and package['flatpak'] in self.selected_flatpak:
                self.selected_flatpak.remove(package['flatpak'])
            elif install_method == 'deb':
                deb_info = (package['deb_url'], package['package'])
                if deb_info in self.selected_deb_urls:
                    self.selected_deb_urls.remove(deb_info)
            elif install_method == 'custom':
                # Find and remove custom script
                custom_to_remove = None
                for custom_info in self.selected_custom:
                    if custom_info[1] == package['package']:
                        custom_to_remove = custom_info
                        break
                if custom_to_remove:
                    self.selected_custom.remove(custom_to_remove)
        
        self._update_batch_bar()
    
    def _is_package_selected(self, package: dict) -> bool:
        """Check if a package is currently selected in batch mode."""
        install_method = self._get_install_method(package)
        
        if install_method == 'apt' and package.get('package'):
            return package['package'] in self.selected_apt
        elif install_method == 'flatpak' and package.get('flatpak'):
            return package['flatpak'] in self.selected_flatpak
        elif install_method == 'deb' and package.get('deb_url'):
            deb_info = (package['deb_url'], package['package'])
            return deb_info in self.selected_deb_urls
        elif install_method == 'custom' and package.get('install_commands'):
            for custom_info in self.selected_custom:
                if custom_info[1] == package['package']:
                    return True
        return False
    
    def _on_search_changed(self, search_entry):
        """Handle search query changes."""
        self.search_query = search_entry.get_text().strip()
        self._refresh_content()
    
    def _on_select_all(self, button):
        """Select all visible uninstalled packages."""
        categories = get_all_categories()
        recommended_categories = ['browsers', 'comunications', 'office', 'multimedia', 'graphics', 'developer', 'gaming']
        
        for category_id in recommended_categories:
            if category_id not in categories:
                continue
                
            category_data = categories[category_id]
            packages = category_data.get('packages', [])
            
            # Apply search filter
            if self.search_query:
                query_lower = self.search_query.lower()
                packages = [
                    pkg for pkg in packages
                    if query_lower in pkg['name'].lower() or query_lower in pkg.get('description', '').lower()
                ]
            
            # Select each uninstalled package
            for package in packages:
                install_method = self._get_install_method(package)
                
                # Skip if excluded from batch or already installed
                if install_method == 'davinci_resolve' or self._is_package_installed(package):
                    continue
                
                # Add to appropriate list if not already selected
                if install_method == 'apt' and package.get('package'):
                    if package['package'] not in self.selected_apt:
                        self.selected_apt.append(package['package'])
                elif install_method == 'flatpak' and package.get('flatpak'):
                    if package['flatpak'] not in self.selected_flatpak:
                        self.selected_flatpak.append(package['flatpak'])
                elif install_method == 'deb' and package.get('deb_url'):
                    deb_info = (package['deb_url'], package['package'])
                    if deb_info not in self.selected_deb_urls:
                        self.selected_deb_urls.append(deb_info)
                elif install_method == 'custom' and package.get('install_commands'):
                    custom_info = (package['install_commands'], package['package'])
                    if custom_info not in self.selected_custom:
                        self.selected_custom.append(custom_info)
        
        self._update_batch_bar()
        self._refresh_content()
    
    def _on_deselect_all(self, button):
        """Deselect all packages."""
        self.selected_apt.clear()
        self.selected_flatpak.clear()
        self.selected_deb_urls.clear()
        self.selected_custom.clear()
        
        self._update_batch_bar()
        self._refresh_content()
    
    def _update_batch_bar(self):
        """Update the batch action bar with selection count."""
        total = len(self.selected_apt) + len(self.selected_flatpak) + len(self.selected_deb_urls) + len(self.selected_custom)
        
        if total > 0:
            self.batch_label.set_text(_("{} programs selected").format(total) if total != 1 else _("1 program selected"))
            self.batch_bar.show()
        else:
            self.batch_bar.hide()
    
    def _on_install_batch(self, button):
        """Install all selected packages."""
        total = len(self.selected_apt) + len(self.selected_flatpak) + len(self.selected_deb_urls) + len(self.selected_custom)
        
        if total == 0:
            return
        
        # Show confirmation dialog
        dialog = Gtk.MessageDialog(
            transient_for=self.parent_window,
            flags=0,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text=_("Install {} selected programs?").format(total)
        )
        
        details = []
        if self.selected_apt:
            details.append(f"APT: {', '.join(self.selected_apt)}")
        if self.selected_flatpak:
            flatpak_names = [fp.split('.')[-1] for fp in self.selected_flatpak]
            details.append(f"Flatpak: {', '.join(flatpak_names)}")
        if self.selected_deb_urls:
            deb_names = [name for _, name in self.selected_deb_urls]
            details.append(f".deb: {', '.join(deb_names)}")
        if self.selected_custom:
            custom_names = [name for _, name in self.selected_custom]
            details.append(f"Custom: {', '.join(custom_names)}")
        
        dialog.format_secondary_text("\n".join(details))
        
        response = dialog.run()
        dialog.destroy()
        
        if response != Gtk.ResponseType.YES:
            return
        
        # Disable batch mode during installation
        self.batch_toggle_button.set_sensitive(False)
        self.batch_bar.hide()
        
        # Start batch installation
        self._install_batch_step_1_apt()
    
    def _install_batch_step_1_apt(self):
        """Step 1: Install all APT packages in single command."""
        if self.selected_apt:
            packages = ' '.join(self.selected_apt)
            cmd = f"pkexec apt install -y {packages}"
            self.command_runner.run_command(cmd, self._install_batch_step_2_flatpak)
        else:
            self._install_batch_step_2_flatpak()
    
    def _install_batch_step_2_flatpak(self):
        """Step 2: Install Flatpak packages sequentially."""
        if self.selected_flatpak:
            self._install_next_flatpak(0)
        else:
            self._install_batch_step_3_deb()
    
    def _install_next_flatpak(self, index):
        """Install next Flatpak package."""
        if index >= len(self.selected_flatpak):
            self._install_batch_step_3_deb()
            return
        
        flatpak_id = self.selected_flatpak[index]
        cmd = f"flatpak install -y flathub {flatpak_id}"
        self.command_runner.run_command(cmd, lambda: self._install_next_flatpak(index + 1))
    
    def _install_batch_step_3_deb(self):
        """Step 3: Install all .deb packages in single consolidated script."""
        if not self.selected_deb_urls:
            self._install_batch_step_4_custom()
            return
        
        # Create a single script that downloads and installs ALL .deb packages
        script_path = "/tmp/batch-install-deb-all.sh"
        
        try:
            with open(script_path, "w") as f:
                f.write("#!/bin/bash\n")
                f.write("# Batch download and installation of .deb packages\n\n")
                
                f.write("set -e  # Exit on error\n\n")
                
                # First, download all .deb files (no root needed)
                for deb_url, pkg_name in self.selected_deb_urls:
                    f.write(f"echo '{_('Downloading')} {pkg_name}...'\n")
                    f.write(f'wget -q --show-progress -O /tmp/{pkg_name}.deb "{deb_url}" || {{ echo "{_("Download failed for")} {pkg_name}"; exit 1; }}\n')
                    f.write(f'chmod 644 /tmp/{pkg_name}.deb\n')
                
                f.write(f"\necho '{_('Installing all .deb packages...')}'\n")
                
                # Then install all at once (running as root)
                deb_files = " ".join([f"/tmp/{pkg_name}.deb" for _, pkg_name in self.selected_deb_urls])
                f.write(f"dpkg -i {deb_files} || apt-get install -f -y || {{ echo '{_("Installation failed")}'; exit 1; }}\n")
                
                # Cleanup
                for _, pkg_name in self.selected_deb_urls:
                    f.write(f"rm -f /tmp/{pkg_name}.deb\n")
                
                f.write(f"echo '{_('All .deb packages installed successfully')}'\n")
            
            os.chmod(script_path, 0o755)
            
            # Execute entire script with pkexec (single password prompt, root permissions for download & install)
            cmd = f"pkexec {script_path}"
            self.command_runner.run_command(cmd, self._install_batch_step_4_custom)
            
        except Exception as e:
            print(f"Error creating consolidated .deb script: {e}")
            self._install_batch_step_4_custom()
    
    def _install_batch_step_4_custom(self):
        """Step 4: Install custom script packages in single consolidated script."""
        if not self.selected_custom:
            self._install_batch_complete()
            return
        
        # Consolidate ALL custom scripts into ONE script file to avoid multiple password prompts
        script_path = "/tmp/batch-install-custom-all.sh"
        
        try:
            with open(script_path, "w") as f:
                f.write("#!/bin/bash\n")
                f.write("# Batch installation of custom script packages\n")
                f.write("set -e  # Exit on error\n\n")
                
                for commands_list, pkg_name in self.selected_custom:
                    f.write(f"# Installing {pkg_name}\n")
                    f.write(f"echo 'Installing {pkg_name}...'\n")
                    f.write("\n".join(commands_list))
                    f.write("\n\n")
                
                f.write("echo 'All custom scripts completed successfully'\n")
            
            os.chmod(script_path, 0o755)
            
            # Single pkexec call for ALL custom scripts
            cmd = f"pkexec {script_path}"
            self.command_runner.run_command(cmd, self._install_batch_complete)
            
        except Exception as e:
            print(f"Error creating consolidated custom script: {e}")
            self._install_batch_complete()
    
    def _install_batch_complete(self):
        """Complete batch installation."""
        # Clear selections
        self.selected_apt.clear()
        self.selected_flatpak.clear()
        self.selected_deb_urls.clear()
        self.selected_custom.clear()
        
        # Clear cache
        self.package_status_cache.clear()
        
        # Re-enable batch mode toggle
        self.batch_toggle_button.set_sensitive(True)
        
        # Refresh UI
        self._refresh_content()
        
        # Show completion dialog
        dialog = Gtk.MessageDialog(
            transient_for=self.parent_window,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=_("Batch Installation Complete")
        )
        dialog.format_secondary_text(_("All selected programs have been installed."))
        dialog.run()
        dialog.destroy()
    
    def _clear_status(self):
        """Clear the status message."""
        self.status_label.set_text(_("Ready"))
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
        
        # 1. Show dialog explaining manual download
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

        # 2. File Chooser
        file_filter = Gtk.FileFilter()
        file_filter.set_name(_("DaVinci Resolve Installer"))
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


        # Start installation process
        package_id = "multimedia:DaVinci Resolve"
        self.installing_packages.add(package_id)
        self._refresh_content()
        
        # Step 1: Install dependencies
        self._davinci_step_1_deps(filename, package_data)

    def _davinci_step_1_deps(self, filename, package_data):
        """Step 1: Install dependencies (requires root)."""
        cmd = "pkexec apt-get install -y fakeroot xorriso unzip"
        self.command_runner.run_command(cmd, lambda: self._davinci_step_2_extract(filename, package_data))

    def _davinci_step_2_extract(self, filename, package_data):
        """Step 2: Extract installer to local work directory."""
        
        installer_dir = os.path.dirname(filename)
        work_dir = os.path.join(installer_dir, "soplos-davinci-work")
        
        # Clean previous work dir
        if os.path.exists(work_dir):
            import shutil
            shutil.rmtree(work_dir, ignore_errors=True)
        os.makedirs(work_dir, exist_ok=True)
        
        if filename.lower().endswith(".zip"):
            # Unzip to work dir
            cmd = f"unzip -o '{filename}' -d '{work_dir}'"
            self.command_runner.run_command(cmd, lambda: self._davinci_step_3_convert(work_dir, package_data))
        else:
            # Copy .run file
            cmd = f"cp '{filename}' '{work_dir}/'"
            self.command_runner.run_command(cmd, lambda: self._davinci_step_3_convert(work_dir, package_data))

    def _davinci_step_3_convert(self, work_dir, package_data):
        """Step 3: Run makeresolvedeb (as user)."""
        
        # Find .run file
        run_file = None
        for f in os.listdir(work_dir):
            if f.endswith(".run"):
                run_file = f
                break
        
        if not run_file:
            self._on_package_operation_complete(package_data, False)
            return


        # Find makeresolvedeb script using dynamic path resolution
        # Get the directory where this Python file is located
        current_file = os.path.abspath(__file__)
        # Go up to the main application directory (ui/tabs -> ui -> root)
        app_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
        src_script = os.path.join(app_root, "services", "makeresolvedeb_1.8.3_multi.sh")
        
        if not os.path.exists(src_script):
            self._on_package_operation_complete(package_data, False)
            return
        
        dst_script = os.path.join(work_dir, "makeresolvedeb.sh")
        
        import shutil
        try:
            shutil.copy(src_script, dst_script)
            os.chmod(dst_script, 0o755)
            os.chmod(os.path.join(work_dir, run_file), 0o755)
        except Exception as e:
            self._on_package_operation_complete(package_data, False)
            return

        # Run conversion
        # IMPORTANT: Run as current user, NOT root. CommandRunner runs as user by default.
        # We chain commands: cd to dir, then run script
        cmd = f"cd '{work_dir}' && ./makeresolvedeb.sh '{run_file}'"
        self.command_runner.run_command(cmd, lambda: self._davinci_step_4_install(work_dir, package_data))

    def _davinci_step_4_install(self, work_dir, package_data):
        """Step 4: Install generated .deb (requires root)."""
        
        # Find .deb file
        deb_file = None
        for f in os.listdir(work_dir):
            if f.endswith(".deb"):
                deb_file = f
                break
        
        if not deb_file:
            self._on_package_operation_complete(package_data, False)
            return

        full_deb_path = os.path.join(work_dir, deb_file)
        
        # Install
        cmd = f"pkexec apt-get install -y '{full_deb_path}'"
        self.command_runner.run_command(cmd, lambda: self._davinci_cleanup(work_dir, package_data))

    def _davinci_cleanup(self, work_dir, package_data):
        """Step 5: Cleanup."""
        import shutil
        shutil.rmtree(work_dir, ignore_errors=True)
        
        # Mark as complete
        # We need to manually trigger the completion logic
        # Since we added it to installing_packages manually
        package_id = "multimedia:DaVinci Resolve"
        if package_id in self.installing_packages:
            self.installing_packages.remove(package_id)
        
        self._refresh_content()
        
        
        # Show success dialog
        dialog = Gtk.MessageDialog(
            transient_for=self.parent_window,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=_("Installation Complete")
        )
        dialog.format_secondary_text(_("DaVinci Resolve has been installed successfully."))
        dialog.run()
        dialog.destroy()
