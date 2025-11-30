"""
Gaming tab implementation for Soplos Welcome.
Hidden easter egg tab with gaming optimizations and tools.
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

from config.paths import ICONS_DIR

class GamingTab(Gtk.Box):
    """Hidden gaming tab with optimizations and tools."""
    
    def __init__(self, i18n_manager, theme_manager, parent_window, progress_bar, progress_label):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        
        self.i18n_manager = i18n_manager
        self.theme_manager = theme_manager
        self.parent_window = parent_window
        self.progress_bar = progress_bar
        self.progress_label = progress_label
        
        # Set margins
        self.set_margin_top(20)
        self.set_margin_bottom(20)
        self.set_margin_left(20)
        self.set_margin_right(20)
        
        # Create UI
        self._create_ui()
        
    def _create_ui(self):
        """Create the user interface."""
        # Scrollable area
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.pack_start(scrolled, True, True, 0)
        
        # Content box
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        scrolled.add(content_box)
        
        # Header
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        header_box.set_halign(Gtk.Align.CENTER)
        
        icon = Gtk.Image.new_from_icon_name("input-gaming", Gtk.IconSize.DIALOG)
        header_box.pack_start(icon, False, False, 0)
        
        title = Gtk.Label()
        title.set_markup("<span size='x-large' weight='bold'>Gaming Center</span>")
        header_box.pack_start(title, False, False, 0)
        
        content_box.pack_start(header_box, False, False, 10)
        
        # 1. Optimizations Section
        self._create_section(content_box, "Optimizations", [
            ("GameMode", "Enable Feral GameMode", "gamemode"),
            ("High Performance", "Set CPU Governor to Performance", "cpu-performance"),
            ("Sysctl Tweaks", "Apply gaming kernel parameters", "preferences-system")
        ])
        
        # 2. Launchers Section
        self._create_section(content_box, "Launchers", [
            ("Steam", "Install Steam", "steam"),
            ("Lutris", "Install Lutris", "lutris"),
            ("Heroic", "Install Heroic Games Launcher", "heroic"),
            ("Bottles", "Install Bottles", "bottles")
        ])
        
        # 3. Wallpapers Section
        self._create_section(content_box, "Customization", [
            ("Gaming Wallpapers", "Install exclusive gaming wallpapers", "preferences-desktop-wallpaper"),
            ("RGB Theme", "Enable RGB accent colors", "preferences-desktop-theme")
        ])
        
    def _create_section(self, parent, title_text, items):
        """Create a section with a title and a grid of buttons."""
        # Section Frame
        frame = Gtk.Frame()
        frame.get_style_context().add_class("card")
        parent.pack_start(frame, False, False, 0)
        
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_margin_top(15)
        vbox.set_margin_bottom(15)
        vbox.set_margin_left(15)
        vbox.set_margin_right(15)
        frame.add(vbox)
        
        # Title
        label = Gtk.Label()
        label.set_markup(f"<span size='large' weight='bold'>{title_text}</span>")
        label.set_halign(Gtk.Align.START)
        vbox.pack_start(label, False, False, 0)
        
        # Grid for items
        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        grid.set_column_homogeneous(True)
        vbox.pack_start(grid, False, False, 0)
        
        # Add items
        col = 0
        row = 0
        for name, desc, icon_name in items:
            button = self._create_item_button(name, desc, icon_name)
            grid.attach(button, col, row, 1, 1)
            
            col += 1
            if col > 1:  # 2 columns
                col = 0
                row += 1
                
    def _create_item_button(self, name, desc, icon_name):
        """Create a button for an item."""
        button = Gtk.Button()
        button.set_relief(Gtk.ReliefStyle.NONE)
        button.get_style_context().add_class("flat")
        
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox.set_margin_top(10)
        hbox.set_margin_bottom(10)
        hbox.set_margin_left(10)
        hbox.set_margin_right(10)
        
        # Icon
        try:
            # Try loading from assets first if it's a custom icon
            # For now just use icon name
            icon = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.DND)
        except:
            icon = Gtk.Image.new_from_icon_name("image-missing", Gtk.IconSize.DND)
            
        hbox.pack_start(icon, False, False, 0)
        
        # Text
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        vbox.set_valign(Gtk.Align.CENTER)
        
        name_label = Gtk.Label()
        name_label.set_markup(f"<b>{name}</b>")
        name_label.set_halign(Gtk.Align.START)
        vbox.pack_start(name_label, False, False, 0)
        
        desc_label = Gtk.Label(label=desc)
        desc_label.set_halign(Gtk.Align.START)
        desc_label.get_style_context().add_class("dim-label")
        desc_label.set_line_wrap(True)
        desc_label.set_max_width_chars(30)
        vbox.pack_start(desc_label, False, False, 0)
        
        hbox.pack_start(vbox, True, True, 0)
        
        button.add(hbox)
        
        # Connect click (placeholder)
        button.connect("clicked", self._on_item_clicked, name)
        
        return button
        
    def _on_item_clicked(self, button, name):
        """Handle item clicks."""
        print(f"Clicked: {name}")
        # Placeholder for future implementation
        dialog = Gtk.MessageDialog(
            transient_for=self.parent_window,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=f"Gaming Feature: {name}"
        )
        dialog.format_secondary_text("This feature is coming soon!")
        dialog.run()
        dialog.destroy()
