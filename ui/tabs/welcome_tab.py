"""
Welcome tab implementation for Soplos Welcome.
Displays welcome information and quick actions.
"""

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gtk, GdkPixbuf
import webbrowser
from pathlib import Path

from core.i18n_manager import _

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gtk, GdkPixbuf
import webbrowser
import subprocess
import os
from pathlib import Path


class WelcomeTab(Gtk.Box):
    """Welcome tab with system information and quick actions."""
    
    def __init__(self, i18n_manager, theme_manager, assets_path=None):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.i18n_manager = i18n_manager
        self.theme_manager = theme_manager
        self.assets_path = assets_path
        
        self.set_margin_left(25)
        self.set_margin_right(25)
        self.set_margin_top(15)
        self.set_margin_bottom(15)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the welcome tab user interface."""
        # Main container with centered content
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        main_box.set_halign(Gtk.Align.CENTER)
        main_box.set_valign(Gtk.Align.CENTER)
        
        # Logo section
        logo_section = self._create_logo_section()
        main_box.pack_start(logo_section, False, False, 0)
        
        # Welcome text section
        text_section = self._create_text_section()
        main_box.pack_start(text_section, False, False, 0)
        
        # Features section
        features_section = self._create_features_section()
        main_box.pack_start(features_section, False, False, 0)
        
        # Action buttons section
        actions_section = self._create_actions_section()
        main_box.pack_start(actions_section, False, False, 0)
        
        # Center everything
        self.pack_start(main_box, True, False, 0)
    
    def _create_logo_section(self) -> Gtk.Widget:
        """Create the logo section."""
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        box.set_halign(Gtk.Align.CENTER)
        
        # Determine assets path
        if self.assets_path:
            assets_base = self.assets_path
        else:
            # Fallback: calculate from current file location
            assets_base = Path(__file__).parent.parent.parent / 'assets'
        
        # Soplos logo
        try:
            logo_path = assets_base / 'icons' / 'soplos-logo.png'
            if logo_path.exists():
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    str(logo_path), 128, 128, True
                )
                logo_image = Gtk.Image.new_from_pixbuf(pixbuf)
                box.pack_start(logo_image, False, False, 0)
        except Exception as e:
            print(f"Error loading logo: {e}")
            # Fallback to welcome icon
            try:
                fallback_path = assets_base / 'icons' / 'org.soplos.welcome.png'
                if fallback_path.exists():
                    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                        str(fallback_path), 128, 128, True
                    )
                    logo_image = Gtk.Image.new_from_pixbuf(pixbuf)
                    box.pack_start(logo_image, False, False, 0)
            except:
                pass  # No logo, continue without it
        
        return box
    
    def _create_text_section(self) -> Gtk.Widget:
        """Create the welcome text section."""
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box.set_halign(Gtk.Align.CENTER)
        
        # Main title
        title = Gtk.Label()
        title.set_markup(f'<span size="20000" weight="bold">{_("Welcome to Soplos Linux")}</span>')
        title.set_halign(Gtk.Align.CENTER)
        title.set_margin_bottom(1)
        title.get_style_context().add_class('soplos-welcome-title')
        box.pack_start(title, False, False, 0)
        
        # Subtitle
        subtitle = Gtk.Label()
        subtitle.set_markup('<span size="12000">Tu puerta de entrada al ecosistema Soplos</span>')
        subtitle.set_halign(Gtk.Align.CENTER)
        subtitle.get_style_context().add_class('dim-label')
        subtitle.set_margin_bottom(1)
        box.pack_start(subtitle, False, False, 0)
        
        # Description
        description = Gtk.Label()
        description.set_markup(
            f'<span size="10000">{_("Thank you for choosing Soplos Linux! This application will help you get started with your new system.")}</span>'
        )
        description.set_halign(Gtk.Align.CENTER)
        description.set_justify(Gtk.Justification.CENTER)
        description.set_line_wrap(True)
        description.set_max_width_chars(80)
        description.set_margin_top(2)
        description.get_style_context().add_class('dim-label')
        box.pack_start(description, False, False, 0)
        
        return box
    
    def _create_features_section(self) -> Gtk.Widget:
        """Create the features section."""
        frame = Gtk.Frame()
        frame.set_label(_("Use the tabs above to:"))
        frame.set_label_align(0.5, 0.5)
        frame.set_margin_left(15)
        frame.set_margin_right(15)
        
        # Features grid
        grid = Gtk.Grid()
        grid.set_column_spacing(30)
        grid.set_row_spacing(8)
        grid.set_margin_left(25)
        grid.set_margin_right(25)
        grid.set_margin_top(10)
        grid.set_margin_bottom(10)
        grid.set_halign(Gtk.Align.CENTER)
        
        features = [
            (_("• Install essential software"), "package-x-generic"),
            (_("• Configure system drivers"), "preferences-desktop-peripherals"), 
            (_("• Customize your desktop"), "preferences-desktop-theme"),
            (_("• Manage system kernels"), "utilities-system-monitor"),
            (_("• View recommended applications"), "gnome-software")
        ]
        
        for i, feature_data in enumerate(features):
            text = feature_data[0]
            icon_name = feature_data[1]
            
            # Create system icon
            try:
                icon = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.LARGE_TOOLBAR)
            except Exception as e:
                print(f"Error loading icon {icon_name}: {e}")
                # Ultimate fallback
                icon = Gtk.Image.new_from_icon_name("preferences-system", Gtk.IconSize.LARGE_TOOLBAR)
            
            # Set consistent icon properties
            icon.set_halign(Gtk.Align.CENTER)
            icon.set_valign(Gtk.Align.CENTER)
            grid.attach(icon, 0, i, 1, 1)
            
            # Text label
            label = Gtk.Label(text)
            label.set_halign(Gtk.Align.START)
            label.set_valign(Gtk.Align.CENTER)
            label.set_margin_left(10)
            grid.attach(label, 1, i, 1, 1)
        
        frame.add(grid)
        return frame
    
    def _create_actions_section(self) -> Gtk.Widget:
        """Create the action buttons section."""
        # Main container for buttons
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        main_box.set_halign(Gtk.Align.CENTER)
        main_box.set_margin_top(8)
        
        # Single row with all buttons aligned
        buttons_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        buttons_row.set_halign(Gtk.Align.CENTER)
        
        # Get Started button (switches to Software tab)
        get_started_btn = Gtk.Button()
        get_started_btn.get_style_context().add_class('soplos-button-primary')
        get_started_btn.set_size_request(120, 45)
        
        # Create button content with icon and text
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        start_icon = Gtk.Image.new_from_icon_name("media-playback-start", Gtk.IconSize.BUTTON)
        start_label = Gtk.Label(_("Comenzar"))
        btn_box.pack_start(start_icon, False, False, 0)
        btn_box.pack_start(start_label, False, False, 0)
        btn_box.set_halign(Gtk.Align.CENTER)
        get_started_btn.add(btn_box)
        get_started_btn.connect('clicked', self._on_get_started_clicked)
        buttons_row.pack_start(get_started_btn, False, False, 8)
        
        # Website button
        website_btn = Gtk.Button()
        website_btn.get_style_context().add_class('soplos-button-secondary')
        website_btn.set_size_request(100, 45)
        website_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        website_icon = Gtk.Image.new_from_icon_name("web-browser", Gtk.IconSize.BUTTON)
        website_label = Gtk.Label(_("Web"))
        website_box.pack_start(website_icon, False, False, 0)
        website_box.pack_start(website_label, False, False, 0)
        website_box.set_halign(Gtk.Align.CENTER)
        website_btn.add(website_box)
        website_btn.connect('clicked', self._on_website_clicked)
        buttons_row.pack_start(website_btn, False, False, 8)
        
        # Forum button  
        forum_btn = Gtk.Button()
        forum_btn.get_style_context().add_class('soplos-button-secondary')
        forum_btn.set_size_request(100, 45)
        forum_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        forum_icon = Gtk.Image.new_from_icon_name("system-users", Gtk.IconSize.BUTTON)
        forum_label = Gtk.Label(_("Foros"))
        forum_box.pack_start(forum_icon, False, False, 0)
        forum_box.pack_start(forum_label, False, False, 0)
        forum_box.set_halign(Gtk.Align.CENTER)
        forum_btn.add(forum_box)
        forum_btn.connect('clicked', self._on_forum_clicked)
        buttons_row.pack_start(forum_btn, False, False, 8)
        
        # Wiki button
        wiki_btn = Gtk.Button()
        wiki_btn.get_style_context().add_class('soplos-button-secondary')
        wiki_btn.set_size_request(100, 45)
        wiki_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        wiki_icon = Gtk.Image.new_from_icon_name("help-contents", Gtk.IconSize.BUTTON)
        wiki_label = Gtk.Label(_("Wiki"))
        wiki_box.pack_start(wiki_icon, False, False, 0)
        wiki_box.pack_start(wiki_label, False, False, 0)
        wiki_box.set_halign(Gtk.Align.CENTER)
        wiki_btn.add(wiki_box)
        wiki_btn.connect('clicked', self._on_wiki_clicked)
        buttons_row.pack_start(wiki_btn, False, False, 8)
        
        # Donate button
        donate_btn = Gtk.Button()
        donate_btn.set_size_request(100, 45)
        donate_btn.get_style_context().add_class('soplos-button-accent')
        donate_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        donate_icon = Gtk.Image.new_from_icon_name("emblem-favorite", Gtk.IconSize.BUTTON)
        donate_label = Gtk.Label(_("Donar"))
        donate_box.pack_start(donate_icon, False, False, 0)
        donate_box.pack_start(donate_label, False, False, 0)
        donate_box.set_halign(Gtk.Align.CENTER)
        donate_btn.add(donate_box)
        donate_btn.connect('clicked', self._on_donate_clicked)
        buttons_row.pack_start(donate_btn, False, False, 8)
        
        main_box.pack_start(buttons_row, False, False, 0)
        
        # Autostart toggle section
        autostart_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        autostart_box.set_halign(Gtk.Align.CENTER)
        autostart_box.set_margin_top(8)
        
        # Autostart switch
        self.autostart_switch = Gtk.Switch()
        self.autostart_switch.set_active(self._check_autostart_enabled())
        self.autostart_switch.connect('notify::active', self._on_autostart_toggled)
        
        # Autostart label
        autostart_label = Gtk.Label(_("Show this application on startup"))
        autostart_label.get_style_context().add_class('dim-label')
        
        autostart_box.pack_start(autostart_label, False, False, 0)
        autostart_box.pack_start(self.autostart_switch, False, False, 0)
        
        main_box.pack_start(autostart_box, False, False, 0)
        
        return main_box
    
    def _on_get_started_clicked(self, button):
        """Handle Get Started button click."""
        # Switch to Software tab (tab index 1)
        notebook = self._find_notebook_parent()
        if notebook:
            notebook.set_current_page(1)
    
    def _on_website_clicked(self, button):
        """Handle Website button click."""
        try:
            webbrowser.open("https://soplos.org")
        except Exception as e:
            print(f"Error opening website: {e}")
            self._show_error_dialog(_("No se pudo abrir el sitio web"), 
                                   _("Verifica tu conexión a internet e inténtalo de nuevo."))
    
    def _on_forum_clicked(self, button):
        """Handle Forum button click."""
        try:
            webbrowser.open("https://soplos.org/forums")
        except Exception as e:
            print(f"Error opening forum: {e}")
            self._show_error_dialog(_("No se pudo abrir el foro"), 
                                   _("Verifica tu conexión a internet e inténtalo de nuevo."))
    
    def _on_wiki_clicked(self, button):
        """Handle Wiki button click."""
        try:
            webbrowser.open("https://soplos.org/wiki")
        except Exception as e:
            print(f"Error opening wiki: {e}")
            self._show_error_dialog(_("No se pudo abrir la wiki"), 
                                   _("Verifica tu conexión a internet e inténtalo de nuevo."))
    
    def _on_donate_clicked(self, button):
        """Handle Donate button click."""
        try:
            webbrowser.open("https://www.paypal.com/paypalme/isubdes")
        except Exception as e:
            print(f"Error opening donation page: {e}")
            self._show_error_dialog(_("No se pudo abrir la página de donaciones"), 
                                   _("Verifica tu conexión a internet e inténtalo de nuevo."))
    
    def _show_error_dialog(self, primary_text, secondary_text):
        """Show error dialog."""
        dialog = Gtk.MessageDialog(
            transient_for=self.get_toplevel(),
            modal=True,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=primary_text
        )
        dialog.format_secondary_text(secondary_text)
        dialog.run()
        dialog.destroy()
    
    def _check_autostart_enabled(self):
        """Check if autostart is enabled."""
        import os
        from pathlib import Path
        
        autostart_dir = Path.home() / ".config" / "autostart"
        autostart_file = autostart_dir / "org.soplos.welcome.desktop"
        
        return autostart_file.exists()
    
    def _on_autostart_toggled(self, switch, gparam):
        """Handle autostart toggle."""
        import os
        from pathlib import Path
        
        autostart_dir = Path.home() / ".config" / "autostart"
        autostart_file = autostart_dir / "org.soplos.welcome.desktop"
        
        if switch.get_active():
            # Enable autostart
            try:
                # Create autostart directory if it doesn't exist
                autostart_dir.mkdir(parents=True, exist_ok=True)
                
                # Create desktop file content with all 8 language translations
                desktop_content = """[Desktop Entry]
Name=Soplos Welcome
Name[es]=Bienvenida a Soplos
Name[en]=Soplos Welcome
Name[fr]=Bienvenue à Soplos
Name[de]=Soplos Willkommen
Name[pt]=Bem-vindo ao Soplos
Name[it]=Benvenuto in Soplos
Name[ro]=Bun venit la Soplos
Name[ru]=Добро пожаловать в Soplos
Comment=Soplos Linux Welcome Application
Comment[es]=Aplicación de Bienvenida de Soplos Linux
Comment[en]=Soplos Linux Welcome Application
Comment[fr]=Application de bienvenue de Soplos Linux
Comment[de]=Soplos Linux Willkommensanwendung
Comment[pt]=Aplicação de Boas-vindas do Soplos Linux
Comment[it]=Applicazione di benvenuto di Soplos Linux
Comment[ro]=Aplicația de bun venit Soplos Linux
Comment[ru]=Приложение приветствия Soplos Linux
Exec=soplos-welcome
Icon=org.soplos.welcome
Terminal=false
Type=Application
Categories=System;
StartupNotify=true
X-GNOME-Autostart-enabled=true
"""
                
                # Write the desktop file
                with open(autostart_file, 'w') as f:
                    f.write(desktop_content)
                
                print(f"Autostart enabled: {autostart_file}")
                
            except Exception as e:
                print(f"Error enabling autostart: {e}")
                switch.set_active(False)  # Revert the switch
                self._show_error_dialog(
                    _("Error enabling autostart"),
                    _("Could not create autostart file.")
                )
        else:
            # Disable autostart
            try:
                if autostart_file.exists():
                    autostart_file.unlink()
                    print(f"Autostart disabled: {autostart_file}")
            except Exception as e:
                print(f"Error disabling autostart: {e}")
                switch.set_active(True)  # Revert the switch
                self._show_error_dialog(
                    _("Error disabling autostart"),
                    _("Could not remove autostart file.")
                )
    
    def _find_notebook_parent(self):
        """Find the notebook widget in the parent hierarchy."""
        parent = self.get_parent()
        while parent:
            if isinstance(parent, Gtk.Notebook):
                return parent
            parent = parent.get_parent()
        return None
