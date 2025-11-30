"""
Recommended tab implementation for Soplos Welcome.
Shows curated applications based on desktop environment and user needs.
"""

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gtk, GdkPixbuf, GLib
import threading
import subprocess
import os
from pathlib import Path

from config.software import get_all_categories


from config.paths import ICONS_DIR

class RecommendedTab(Gtk.Box):
    """Recommended applications tab with curated software selections."""
    
    def __init__(self, i18n_manager, theme_manager):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.i18n_manager = i18n_manager
        self.theme_manager = theme_manager
        self.installing_packages = set()  # Track packages being installed
        
        self.set_margin_left(20)
        self.set_margin_right(20)
        self.set_margin_top(20)
        self.set_margin_bottom(20)
        
        self._setup_ui()
        self._load_recommended_software()
    
    def _setup_ui(self):
        """Setup the recommended applications tab user interface."""
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
        
        # Status bar
        self.status_label = Gtk.Label("Listo")
        self.status_label.set_halign(Gtk.Align.START)
        self.status_label.get_style_context().add_class('dim-label')
        self.pack_start(self.status_label, False, False, 0)
    
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
        category_icon = self._load_category_icon(category_id)
        if category_icon:
            header_box.pack_start(category_icon, False, False, 0)
        
        # Category title
        title_label = Gtk.Label()
        title_label.set_markup(f'<span size="14000" weight="bold">{category_data["title"]}</span>')
        title_label.set_halign(Gtk.Align.START)
        header_box.pack_start(title_label, False, False, 0)
        
        frame.set_label_widget(header_box)
        
        # Packages grid
        grid = Gtk.Grid()
        grid.set_column_spacing(15)
        grid.set_row_spacing(10)
        grid.set_margin_left(15)
        grid.set_margin_right(15)
        grid.set_margin_top(10)
        grid.set_margin_bottom(15)
        
        # Add featured packages to grid
        packages = category_data.get('packages', [])
        if featured_only:
            # Show only the first 4 most popular apps per category
            packages = packages[:4]
        
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
        if package.get('official', False):
            name_text += ' <span size="small" foreground="#28a745">●</span>'
        name_label.set_markup(name_text)
        name_label.set_halign(Gtk.Align.START)
        name_box.pack_start(name_label, False, False, 0)
        
        info_box.pack_start(name_box, False, False, 0)
        
        # Package description
        desc_label = Gtk.Label(package.get('description', ''))
        desc_label.set_halign(Gtk.Align.START)
        desc_label.set_line_wrap(True)
        desc_label.set_max_width_chars(45)
        desc_label.get_style_context().add_class('dim-label')
        info_box.pack_start(desc_label, False, False, 0)
        
        box.pack_start(info_box, True, True, 0)
        
        # Action button
        button_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        button_box.set_valign(Gtk.Align.CENTER)
        
        # Check if package is installed
        is_installed = self._is_package_installed(package)
        package_id = f"{category_id}:{package['name']}"
        
        if package_id in self.installing_packages:
            # Installing state
            spinner = Gtk.Spinner()
            spinner.start()
            button_box.pack_start(spinner, False, False, 0)
            
            installing_label = Gtk.Label("Instalando...")
            installing_label.get_style_context().add_class('dim-label')
            button_box.pack_start(installing_label, False, False, 0)
        elif is_installed:
            # Installed state
            installed_label = Gtk.Label("✓ Instalado")
            installed_label.get_style_context().add_class('success-label')
            button_box.pack_start(installed_label, False, False, 0)
        else:
            # Not installed state
            install_button = Gtk.Button.new_with_label("Instalar")
            install_button.get_style_context().add_class('suggested-action')
            install_button.set_size_request(80, -1)
            install_button.connect('clicked', self._on_install_package, category_id, package)
            button_box.pack_start(install_button, False, False, 0)
        
        box.pack_start(button_box, False, False, 0)
        
        return box
    
    def _load_category_icon(self, category_id: str) -> Gtk.Widget:
        """Load and return a category icon."""
        try:
            # Try to find a representative icon in the category folder
            icon_dir = Path(os.path.join(ICONS_DIR, category_id))
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
    
    def _is_package_installed(self, package: dict) -> bool:
        """Check if a package is installed."""
        try:
            # Check APT package
            if package.get('package'):
                result = subprocess.run(
                    ['dpkg', '-l', package['package']],
                    capture_output=True, text=True
                )
                if result.returncode == 0 and 'ii' in result.stdout:
                    return True
            
            # Check Flatpak
            if package.get('flatpak'):
                result = subprocess.run(
                    ['flatpak', 'list', '--app', package['flatpak']],
                    capture_output=True, text=True
                )
                if result.returncode == 0 and package['flatpak'] in result.stdout:
                    return True
            
            # Check Snap
            if package.get('snap'):
                result = subprocess.run(
                    ['snap', 'list', package['snap']],
                    capture_output=True, text=True
                )
                if result.returncode == 0:
                    return True
        
        except Exception:
            pass
        
        return False
    
    def _on_install_package(self, button, category_id: str, package: dict):
        """Handle package installation."""
        package_id = f"{category_id}:{package['name']}"
        
        if package_id in self.installing_packages:
            return  # Already installing
        
        self.installing_packages.add(package_id)
        self.status_label.set_text(f"Instalando {package['name']}...")
        
        # Refresh the UI to show installing state
        self._refresh_content()
        
        # Install in background thread
        thread = threading.Thread(
            target=self._install_package_thread,
            args=(category_id, package)
        )
        thread.daemon = True
        thread.start()
    
    def _install_package_thread(self, category_id: str, package: dict):
        """Install package in background thread."""
        package_id = f"{category_id}:{package['name']}"
        success = False
        
        try:
            # Try Flatpak first if available
            if package.get('flatpak'):
                result = subprocess.run(
                    ['flatpak', 'install', '-y', 'flathub', package['flatpak']],
                    capture_output=True, text=True
                )
                if result.returncode == 0:
                    success = True
            
            # Try APT if Flatpak failed or not available
            elif package.get('package') and not success:
                result = subprocess.run(
                    ['pkexec', 'apt', 'install', '-y', package['package']],
                    capture_output=True, text=True
                )
                if result.returncode == 0:
                    success = True
            
            # Try Snap as last resort
            elif package.get('snap') and not success:
                result = subprocess.run(
                    ['snap', 'install', package['snap']],
                    capture_output=True, text=True
                )
                if result.returncode == 0:
                    success = True
        
        except Exception as e:
            print(f"Error installing {package['name']}: {e}")
        
        # Update UI in main thread
        GLib.idle_add(self._on_package_operation_complete, 
                     category_id, package, success)
    
    def _on_package_operation_complete(self, category_id: str, package: dict, success: bool):
        """Handle completion of package operation."""
        package_id = f"{category_id}:{package['name']}"
        
        # Remove from installing set
        self.installing_packages.discard(package_id)
        
        # Update status
        if success:
            self.status_label.set_text(f"{package['name']} instalado exitosamente")
        else:
            self.status_label.set_text(f"Error al instalar {package['name']}")
        
        # Refresh the content
        self._refresh_content()
        
        # Clear status after 3 seconds
        GLib.timeout_add_seconds(3, self._clear_status)
    
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
