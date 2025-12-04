"""
Main window for Soplos Welcome.
Central GUI component that manages all tabs and overall application interface.
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, GdkPixbuf, Pango

from core.i18n_manager import _
from core import __version__
from ui import DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT, MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT, CSS_CLASSES


class MainWindow(Gtk.ApplicationWindow):
    """
    Main application window for Soplos Welcome.
    Manages the tab notebook, status bar, and overall window layout.
    """
    
    def __init__(self, application, environment_detector, theme_manager, i18n_manager):
        """
        Initialize the main window.
        
        Args:
            application: The parent GTK application
            environment_detector: Environment detection instance
            theme_manager: Theme management instance  
            i18n_manager: Internationalization manager instance
        """
        super().__init__(application=application)
        
        # Store references to managers
        self.application = application
        self.environment_detector = environment_detector
        self.theme_manager = theme_manager
        self.i18n_manager = i18n_manager
        
        # Window properties
        self.set_title(_("Soplos Welcome"))
        self.set_default_size(DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)
        self.set_size_request(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        # Apply CSS class
        self.get_style_context().add_class(CSS_CLASSES['window'])
        
        # Window icon
        self._set_window_icon()
        
        # Create UI
        self._create_ui()
        
        # Connect signals
        self.connect('delete-event', self._on_delete_event)
        self.connect('key-press-event', self._on_key_press)
        
        print("Main window created successfully")
    
    def _set_window_icon(self):
        """Set the window icon."""
        try:
            icon_path = self.application.assets_path / 'icons' / 'org.soplos.welcome.png'
            if icon_path.exists():
                self.set_icon_from_file(str(icon_path))
            else:
                # Fallback to system icon
                self.set_icon_name('system-software-install')
        except Exception as e:
            print(f"Error setting window icon: {e}")
    
    def _create_ui(self):
        """Create the main user interface."""
        # Main vertical box - simple and clean
        main_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        main_vbox.get_style_context().add_class(CSS_CLASSES['content'])
        self.add(main_vbox)
        
        # Main content area with visible tabs
        self._create_content_area(main_vbox)
        
        # Status bar at bottom
        self._create_status_bar(main_vbox)
        
        # Show all widgets
        main_vbox.show_all()
        
        # Set Welcome tab as the initial active tab (must be after show_all)
        GLib.idle_add(lambda: self.notebook.set_current_page(0))
    
    def _create_header_bar_with_fallback(self):
        """Siempre crear HeaderBar moderna, sin fallback a controles clásicos."""
        return self._create_modern_header_bar()
    
    def _create_modern_header_bar(self):
        """Create modern HeaderBar for GNOME-like environments."""
        header = Gtk.HeaderBar()
        header.set_show_close_button(True)
        header.set_title(_("Soplos Welcome"))
        header.set_has_subtitle(True)
        header.set_subtitle(f"v{__version__}")
        
        self._add_header_buttons(header)
        self.set_titlebar(header)
        self.header = header
        return True
    
    def _create_simple_header_bar_fallback(self):
        """Create HeaderBar but keep traditional decorations as backup."""
        try:
            header = Gtk.HeaderBar()
            header.set_show_close_button(True)
            header.set_title(_("Soplos Welcome"))
            header.set_has_subtitle(True)
            header.set_subtitle(f"v{__version__}")
            
            # Force decoration layout for XFCE
            header.set_decoration_layout("menu:minimize,maximize,close")
            
            self._add_header_buttons(header)
            
            # Try to set as titlebar
            self.set_titlebar(header)
            self.header = header
            
            # For XFCE, ensure we have window controls
            if not header.get_show_close_button():
                print("HeaderBar controls not working, falling back to traditional titlebar")
                return False
            
            return True
            
        except Exception as e:
            print(f"Simple HeaderBar failed: {e}")
            return False
    
    def _add_header_buttons(self, header):
        """Add buttons to the header bar."""
        # Left side buttons
        # Language selector button
        lang_button = Gtk.MenuButton()
        lang_button.set_image(Gtk.Image.new_from_icon_name('preferences-desktop-locale', Gtk.IconSize.BUTTON))
        lang_button.set_tooltip_text(_("Change Language"))
        
        # Create language menu
        lang_menu = self._create_language_menu()
        lang_button.set_popup(lang_menu)
        header.pack_start(lang_button)
        
        # Theme toggle button
        theme_button = Gtk.Button()
        theme_icon = 'weather-clear-night' if self.environment_detector.is_dark_theme else 'weather-clear'
        theme_button.set_image(Gtk.Image.new_from_icon_name(theme_icon, Gtk.IconSize.BUTTON))
        theme_button.set_tooltip_text(_("Toggle Theme"))
        theme_button.connect('clicked', self._on_theme_toggle)
        header.pack_start(theme_button)
        
        # Right side buttons  
        # Info button
        info_button = Gtk.Button()
        info_button.set_image(Gtk.Image.new_from_icon_name('dialog-information', Gtk.IconSize.BUTTON))
        info_button.set_tooltip_text(_("About Soplos Welcome"))
        info_button.connect('clicked', self._on_about_clicked)
        header.pack_end(info_button)
    
    def _create_traditional_titlebar(self, main_vbox):
        """Deshabilitado: no crear barra de título tradicional ni controles clásicos."""
        pass
    
    def _create_language_menu(self):
        """Create language selection menu."""
        menu = Gtk.Menu()
        
        available_languages = self.i18n_manager.get_available_languages()
        current_lang = self.i18n_manager.get_current_language()
        
        for lang_code, lang_name in available_languages.items():
            item = Gtk.CheckMenuItem(label=f"{lang_name} ({lang_code.upper()})")
            item.set_active(lang_code == current_lang)
            item.connect('activate', self._on_language_changed, lang_code)
            menu.append(item)
        
        menu.show_all()
        return menu
    
    def _create_content_area(self, main_vbox):
        """Create the main content area with tabs."""
        # Create notebook for tabs with visible tabs
        self.notebook = Gtk.Notebook()
        self.notebook.set_tab_pos(Gtk.PositionType.TOP)
        self.notebook.set_scrollable(True)
        self.notebook.set_show_tabs(True)  # Always show tabs
        self.notebook.set_show_border(False)  # Cleaner look
        
        # Add custom CSS to make the tab bar thicker
        self._apply_notebook_custom_css()
        
        # Add the notebook directly (no overlay controls needed with native decorations)
        notebook_container = self.notebook
        
        # Progress area (initially hidden) - CREATE BEFORE TABS
        self.progress_revealer = Gtk.Revealer()
        self.progress_revealer.set_transition_type(Gtk.RevealerTransitionType.SLIDE_DOWN)
        
        progress_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        progress_box.set_margin_left(20)
        progress_box.set_margin_right(20)
        progress_box.set_margin_top(10)
        progress_box.set_margin_bottom(10)
        
        # Progress bar
        self.progress_bar = Gtk.ProgressBar()
        self.progress_bar.get_style_context().add_class(CSS_CLASSES['progress_bar'])
        self.progress_bar.set_show_text(True)
        progress_box.pack_start(self.progress_bar, False, False, 0)
        
        # Progress label
        self.progress_label = Gtk.Label()
        self.progress_label.get_style_context().add_class(CSS_CLASSES['status_label'])
        self.progress_label.set_text(_("Ready"))
        self.progress_label.set_ellipsize(Pango.EllipsizeMode.MIDDLE)  # Truncate long text
        self.progress_label.set_max_width_chars(80)  # Limit width
        progress_box.pack_start(self.progress_label, False, False, 0)
        
        self.progress_revealer.add(progress_box)
        
        # Add tabs AFTER progress widgets exist
        self._create_tabs()
        
        # Pack everything
        main_vbox.pack_start(self.progress_revealer, False, False, 0)
        main_vbox.pack_start(notebook_container, True, True, 0)
    
    def _create_tabs(self):
        """Create all application tabs."""
        # Tab definitions (name, class_name, icon_name) - CORRECT ORDER
        tab_definitions = [
            (_("Welcome"), "WelcomeTab", "user-home"),
            (_("Software"), "SoftwareTab", "system-software-install"), 
            (_("Drivers"), "DriversTab", "preferences-system"),
            (_("Kernels"), "KernelsTab", "applications-system"),
            (_("Security"), "SecurityTab", "security-high"),
            (_("Recommended"), "RecommendedTab", "starred"),
            (_("Customization"), "CustomizationTab", "preferences-desktop-theme")
        ]
        
        for tab_name, tab_class, icon_name in tab_definitions:
            try:
                # Create appropriate tab content
                if tab_class == "WelcomeTab":
                    from .tabs.welcome_tab import WelcomeTab
                    tab_content = WelcomeTab(self.i18n_manager, self.theme_manager, self.application.assets_path)
                elif tab_class == "SoftwareTab":
                    from .tabs.software_tab import SoftwareTab
                    tab_content = SoftwareTab(
                        self.i18n_manager, 
                        self.theme_manager, 
                        self.environment_detector,
                        self,  # parent_window for progress access
                        self.progress_bar,
                        self.progress_label
                    )
                elif tab_class == "RecommendedTab":
                    from .tabs.recommended_tab import RecommendedTab
                    tab_content = RecommendedTab(
                        self.i18n_manager, 
                        self.theme_manager,
                        self,  # parent_window
                        self.progress_bar,
                        self.progress_label
                    )
                elif tab_class == "DriversTab":
                    from .tabs.drivers_tab import DriversTab
                    tab_content = DriversTab(
                        self.i18n_manager,
                        self.theme_manager,
                        self,  # parent_window
                        self.progress_bar,
                        self.progress_label
                    )
                elif tab_class == "KernelsTab":
                    from .tabs.kernels_tab import KernelsTab
                    tab_content = KernelsTab(
                        self.i18n_manager,
                        self.theme_manager,
                        self,  # parent_window
                        self.progress_bar,
                        self.progress_label
                    )
                elif tab_class == "SecurityTab":
                    from .tabs.security_tab import SecurityTab
                    tab_content = SecurityTab(
                        self.i18n_manager,
                        self.theme_manager,
                        self,  # parent_window
                        self.progress_bar,
                        self.progress_label
                    )
                elif tab_class == "CustomizationTab":
                    from .tabs.customization_tab import CustomizationTab
                    tab_content = CustomizationTab(
                        self.i18n_manager, 
                        self.theme_manager,
                        self.environment_detector
                    )
                else:
                    # Create placeholder tab for others
                    tab_content = self._create_placeholder_tab(tab_name, tab_class, icon_name)
                
                # Create tab label with icon
                tab_label_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
                
                # Tab icon
                tab_icon = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.MENU)
                tab_label_box.pack_start(tab_icon, False, False, 0)
                
                # Tab text
                tab_text = Gtk.Label(label=tab_name)
                tab_label_box.pack_start(tab_text, False, False, 0)
                tab_label_box.show_all()
                
                # Add tab to notebook
                page_num = self.notebook.append_page(tab_content, tab_label_box)
                self.notebook.set_tab_reorderable(tab_content, True)
                
                print(f"Created tab: {tab_name}")
                
            except Exception as e:
                print(f"Error creating tab {tab_name}: {e}")
        
        # Initialize hidden Gaming Tab (Easter Egg)
        try:
            from .tabs.gaming_tab import GamingTab
            self.gaming_tab = GamingTab(
                self.i18n_manager,
                self.theme_manager,
                self,
                self.progress_bar,
                self.progress_label
            )
            self.gaming_tab_label = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
            icon = Gtk.Image.new_from_icon_name("input-gaming", Gtk.IconSize.MENU)
            label = Gtk.Label(label="Gaming")
            self.gaming_tab_label.pack_start(icon, False, False, 0)
            self.gaming_tab_label.pack_start(label, False, False, 0)
            self.gaming_tab_label.show_all()
            self.gaming_tab_added = False
        except Exception as e:
            print(f"Error creating GamingTab: {e}")
            self.gaming_tab = None
            self.gaming_tab_label = None
            self.gaming_tab_added = False
        
        print("✅ All tabs created successfully")
    
    def _create_notebook_controls_overlay(self, overlay_container):
        """Create window control buttons as overlay on the notebook."""
        # Control buttons container - positioned at top right
        controls_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        controls_box.set_margin_right(12)
        controls_box.set_margin_top(6)
        controls_box.set_halign(Gtk.Align.END)
        controls_box.set_valign(Gtk.Align.START)
        
        # Style the container to look like window controls
        controls_box.get_style_context().add_class("window-controls")
        
        # Minimize button
        minimize_button = Gtk.Button()
        minimize_button.set_image(Gtk.Image.new_from_icon_name('window-minimize', Gtk.IconSize.SMALL_TOOLBAR))
        minimize_button.set_tooltip_text(_("Minimize"))
        minimize_button.connect('clicked', self._on_minimize_window)
        minimize_button.get_style_context().add_class("window-control-button")
        minimize_button.set_size_request(24, 24)
        minimize_button.set_relief(Gtk.ReliefStyle.NONE)  # Botón plano
        controls_box.pack_start(minimize_button, False, False, 0)
        
        # Maximize/Restore button
        self.maximize_button = Gtk.Button()
        if self.is_maximized():
            self.maximize_button.set_image(Gtk.Image.new_from_icon_name('window-restore', Gtk.IconSize.SMALL_TOOLBAR))
            self.maximize_button.set_tooltip_text(_("Restore"))
        else:
            self.maximize_button.set_image(Gtk.Image.new_from_icon_name('window-maximize', Gtk.IconSize.SMALL_TOOLBAR))
            self.maximize_button.set_tooltip_text(_("Maximize"))
        self.maximize_button.connect('clicked', self._on_maximize_toggle)
        self.maximize_button.get_style_context().add_class("window-control-button")
        self.maximize_button.set_size_request(24, 24)
        self.maximize_button.set_relief(Gtk.ReliefStyle.NONE)  # Botón plano
        controls_box.pack_start(self.maximize_button, False, False, 0)
        
        # Close button
        close_button = Gtk.Button()
        close_button.set_image(Gtk.Image.new_from_icon_name('window-close', Gtk.IconSize.SMALL_TOOLBAR))
        close_button.set_tooltip_text(_("Close"))
        close_button.connect('clicked', self._on_close_window)
        close_button.get_style_context().add_class("window-control-button")
        close_button.get_style_context().add_class("close-button")
        close_button.set_size_request(24, 24)
        close_button.set_relief(Gtk.ReliefStyle.NONE)  # Botón plano
        controls_box.pack_start(close_button, False, False, 0)
        
        # Connect to window state changes to update maximize button
        self.connect('window-state-event', self._on_window_state_changed)
        
        # Add controls as overlay
        overlay_container.add_overlay(controls_box)
    
    def _apply_notebook_custom_css(self):
        """Apply custom CSS to make the notebook tab bar thicker."""
        css_provider = Gtk.CssProvider()
        css_data = """
        notebook > header {
            min-height: 20px;
            padding: 0px 0;
        }
        
        notebook > header > tabs > tab {
            min-height: 20px;
            padding: 8px 12px;
        }
        
        notebook > header > tabs > tab label {
            padding: 4px 8px;
        }
        """
        
        try:
            css_provider.load_from_data(css_data.encode('utf-8'))
            screen = Gdk.Screen.get_default()
            style_context = Gtk.StyleContext()
            style_context.add_provider_for_screen(
                screen, 
                css_provider, 
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )
            print("✅ Custom notebook CSS applied successfully")
        except Exception as e:
            print(f"⚠️ Error applying custom CSS: {e}")
    
    def _create_placeholder_tab(self, tab_name, tab_class, icon_name):
        """Create a placeholder tab while real tabs are being developed."""
        # Main container
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_kinetic_scrolling(True)
        
        # Content box
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        content_box.set_margin_left(30)
        content_box.set_margin_right(30)
        content_box.set_margin_top(30)
        content_box.set_margin_bottom(30)
        
        # Large icon
        large_icon = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.DIALOG)
        large_icon.get_style_context().add_class(CSS_CLASSES['icon_large'])
        content_box.pack_start(large_icon, False, False, 0)
        
        # Title
        title_label = Gtk.Label()
        title_label.set_markup(f"<span size='x-large' weight='bold'>{tab_name}</span>")
        title_label.get_style_context().add_class(CSS_CLASSES['welcome_title'])
        content_box.pack_start(title_label, False, False, 0)
        
        # Description
        descriptions = {
            "Welcome": _("Welcome to Soplos Linux! Get started with your new system."),
            "Software": _("Install and manage software packages, repositories, and software centers."),
            "Drivers": _("Detect and install optimal hardware drivers for your system."),
            "Customization": _("Customize your desktop environment, themes, and appearance."),
            "Kernels": _("Manage system kernels and performance optimizations."),
            "Recommended": _("Discover recommended applications for your workflow.")
        }
        
        desc_label = Gtk.Label()
        desc_label.set_text(descriptions.get(tab_name.replace(_(""), ""), _("Tab content coming soon...")))
        desc_label.get_style_context().add_class(CSS_CLASSES['welcome_subtitle'])
        desc_label.set_line_wrap(True)
        desc_label.set_justify(Gtk.Justification.CENTER)
        content_box.pack_start(desc_label, False, False, 0)
        
        # Environment info card
        if tab_name == _("Welcome"):
            self._add_environment_info_card(content_box)
        
        # Demo buttons for software tab
        if tab_name == _("Software"):
            self._add_software_demo_buttons(content_box)
        
        # Coming soon message
        coming_soon = Gtk.Label()
        coming_soon.set_markup(f"<span style='italic'>{_('Full implementation coming soon...')}</span>")
        coming_soon.get_style_context().add_class('dim-label')
        content_box.pack_start(coming_soon, False, False, 0)
        
        scrolled.add(content_box)
        scrolled.show_all()
        
        return scrolled
    
    def _add_environment_info_card(self, content_box):
        """Add environment information card to welcome tab."""
        # Environment info card
        info_card = Gtk.Frame()
        info_card.get_style_context().add_class(CSS_CLASSES['card'])
        info_card.set_label(_("System Information"))
        
        info_grid = Gtk.Grid()
        info_grid.set_column_spacing(20)
        info_grid.set_row_spacing(10)
        info_grid.set_margin_left(15)
        info_grid.set_margin_right(15)
        info_grid.set_margin_top(15)
        info_grid.set_margin_bottom(15)
        
        # Get environment info
        env_info = self.environment_detector.detect_all()
        
        # Add environment details
        details = [
            (_("Desktop Environment"), env_info['desktop_environment'].title()),
            (_("Display Protocol"), env_info['display_protocol'].title()),
            (_("Theme Type"), env_info['theme_type'].title()),
            (_("Current Language"), self.i18n_manager.get_current_language_name()),
            (_("Current Theme"), self.theme_manager.current_theme or _("Default"))
        ]
        
        for i, (label_text, value_text) in enumerate(details):
            # Label
            label = Gtk.Label()
            label.set_markup(f"<b>{label_text}:</b>")
            label.set_halign(Gtk.Align.START)
            info_grid.attach(label, 0, i, 1, 1)
            
            # Value
            value = Gtk.Label(label=value_text)
            value.set_halign(Gtk.Align.START)
            info_grid.attach(value, 1, i, 1, 1)
        
        info_card.add(info_grid)
        content_box.pack_start(info_card, False, False, 0)
    
    def _add_software_demo_buttons(self, content_box):
        """Add demo buttons to software tab."""
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        button_box.set_halign(Gtk.Align.CENTER)
        
        # Demo install button
        install_btn = Gtk.Button(label=_("Install Demo Package"))
        install_btn.get_style_context().add_class(CSS_CLASSES['button_install'])
        install_btn.connect('clicked', self._on_demo_install)
        button_box.pack_start(install_btn, False, False, 0)
        
        # Demo uninstall button
        uninstall_btn = Gtk.Button(label=_("Uninstall Demo Package"))
        uninstall_btn.get_style_context().add_class(CSS_CLASSES['button_uninstall'])
        uninstall_btn.connect('clicked', self._on_demo_uninstall)
        button_box.pack_start(uninstall_btn, False, False, 0)
        
        content_box.pack_start(button_box, False, False, 0)
    
    def _create_status_bar(self, main_vbox):
        """Create a clean status bar with system info and version."""
        # Create simple horizontal box for status bar
        status_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        status_box.set_margin_left(15)
        status_box.set_margin_right(15)
        status_box.set_margin_top(8)
        status_box.set_margin_bottom(8)
        
        # Left side: System info
        env_info = self.environment_detector.detect_all()
        desktop_name = self._translate_desktop_name(env_info['desktop_environment'])
        protocol_name = self._translate_protocol_name(env_info['display_protocol'])
        
        status_text = _("Ready - {desktop} on {protocol}").format(
            desktop=desktop_name,
            protocol=protocol_name
        )
        
        self.status_label = Gtk.Label(label=status_text)
        self.status_label.set_halign(Gtk.Align.START)
        self.status_label.set_name("status-system")  # For consistent styling
        status_box.pack_start(self.status_label, False, False, 0)
        
        # Right side: Version info
        version_text = f"Soplos Welcome v{__version__}"
        version_label = Gtk.Label(label=version_text)
        version_label.set_halign(Gtk.Align.END)
        version_label.set_name("status-version")  # For consistent styling
        version_label.get_style_context().add_class('dim-label')
        status_box.pack_end(version_label, False, False, 0)
        
        main_vbox.pack_start(status_box, False, False, 0)
    
    def _translate_desktop_name(self, desktop_env):
        """Translate desktop environment name."""
        desktop_map = {
            'gnome': _("GNOME"),
            'kde': _("KDE Plasma"),
            'plasma': _("KDE Plasma"),
            'xfce': _("XFCE"),
            'unknown': _("Unknown")
        }
        return desktop_map.get(desktop_env.lower(), _("Unknown"))
    
    def _translate_protocol_name(self, protocol):
        """Translate display protocol name."""
        protocol_map = {
            'x11': _("X11"),
            'wayland': _("Wayland"),
            'unknown': _("Unknown")
        }
        return protocol_map.get(protocol.lower(), _("Unknown"))
    
    def show_progress(self, message, fraction=None):
        """
        Show progress bar with message.
        
        Args:
            message: Progress message to display
            fraction: Progress fraction (0.0-1.0), None for pulse mode
        """
        self.progress_label.set_text(message)
        
        if fraction is not None:
            self.progress_bar.set_fraction(fraction)
            self.progress_bar.set_text(f"{int(fraction * 100)}%")
        else:
            self.progress_bar.pulse()
            self.progress_bar.set_text(_("Working..."))
        
        self.progress_revealer.set_reveal_child(True)
        
        # Process pending events to update UI
        while Gtk.events_pending():
            Gtk.main_iteration()
    
    def hide_progress(self):
        """Hide progress bar."""
        self.progress_revealer.set_reveal_child(False)
        self.progress_label.set_text(_("Ready"))
        self.progress_bar.set_fraction(0.0)
        self.progress_bar.set_text("")
    
    def show_about_dialog(self):
        """Show about dialog."""
        dialog = Gtk.AboutDialog()
        dialog.set_transient_for(self)
        dialog.set_modal(True)
        
        dialog.set_program_name(_("Soplos Welcome"))
        dialog.set_version("2.0.0")
        dialog.set_comments(_("The world's most advanced welcome application for Linux"))
        dialog.set_copyright("Copyright © 2025 Sergi Perich")
        dialog.set_license_type(Gtk.License.GPL_3_0)
        dialog.set_website("https://soplos.org")
        dialog.set_website_label(_("Soplos Linux Website"))
        dialog.set_authors(["Sergi Perich"])
        
        # Set logo if available
        try:
            logo_path = self.application.assets_path / 'icons' / 'org.soplos.welcome.png'
            if logo_path.exists():
                logo_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(str(logo_path), 128, 128, True)
                dialog.set_logo(logo_pixbuf)
        except Exception:
            pass
        
        dialog.run()
        dialog.destroy()
    
    # Event handlers
    def _on_delete_event(self, window, event):
        """Handle window close event."""
        print("Main window closing...")
        return False  # Allow window to close
    
    def _on_key_press(self, widget, event):
        """Handle key press events."""
        keyval = event.keyval
        state = event.state
        
        # Check for Ctrl+Q to quit
        if state & Gdk.ModifierType.CONTROL_MASK:
            if keyval == Gdk.KEY_q:
                self.close()
                return True
            
            # Ctrl+Tab to switch tabs
            elif keyval == Gdk.KEY_Tab:
                current_page = self.notebook.get_current_page()
                total_pages = self.notebook.get_n_pages()
                next_page = (current_page + 1) % total_pages
                self.notebook.set_current_page(next_page)
                return True
                
            # Easter Egg: Ctrl+G for Gaming Tab
            elif keyval == Gdk.KEY_g:
                self._toggle_gaming_tab()
                return True
            
        return False

    def _toggle_gaming_tab(self):
        """Toggle the visibility of the hidden Gaming Tab."""
        if not hasattr(self, 'gaming_tab') or self.gaming_tab is None:
            return
            
        if self.gaming_tab_added:
            # Remove tab
            page_num = self.notebook.page_num(self.gaming_tab)
            if page_num != -1:
                self.notebook.remove_page(page_num)
                self.gaming_tab_added = False
                print("Gaming Mode Deactivated")
        else:
            # Add tab
            self.gaming_tab.show_all()  # Ensure content is visible
            self.notebook.append_page(self.gaming_tab, self.gaming_tab_label)
            self.gaming_tab_added = True
            
            # Switch to it
            page_num = self.notebook.page_num(self.gaming_tab)
            self.notebook.set_current_page(page_num)
            
            # Show notification/effect
            print("Gaming Mode Activated!")
            # Use progress bar to show notification
            if hasattr(self, 'progress_revealer'):
                self.progress_revealer.set_reveal_child(True)
                self.progress_label.set_text(_("🎮 Gaming Mode Activated!"))
                self.progress_bar.set_fraction(1.0)
                
                # Hide after 2 seconds
                GLib.timeout_add(2000, lambda: self.progress_revealer.set_reveal_child(False))
    
    def _on_language_changed(self, menu_item, lang_code):
        """Handle language change."""
        if menu_item.get_active():
            if self.i18n_manager.set_language(lang_code):
                # Show restart recommendation
                dialog = Gtk.MessageDialog(
                    transient_for=self,
                    flags=0,
                    message_type=Gtk.MessageType.INFO,
                    buttons=Gtk.ButtonsType.OK,
                    text=_("Language Changed")
                )
                dialog.format_secondary_text(
                    _("Language has been changed to {language}. "
                      "Please restart the application for full effect.").format(
                        language=self.i18n_manager.get_current_language_name()
                    )
                )
                dialog.run()
                dialog.destroy()
    
    def _on_theme_toggle(self, button):
        """Handle theme toggle."""
        current_theme = self.theme_manager.current_theme
        
        if current_theme == 'dark':
            new_theme = 'light'
        elif current_theme == 'light':
            new_theme = 'dark'
        else:
            # Toggle based on system preference
            new_theme = 'dark' if not self.environment_detector.is_dark_theme else 'light'
        
        if self.theme_manager.load_theme(new_theme):
            # Update button icon
            icon_name = 'weather-clear-night' if new_theme == 'light' else 'weather-clear'
            button.set_image(Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.BUTTON))
    
    def _on_about_clicked(self, button):
        """Handle about button click."""
        self.show_about_dialog()
    
    def _on_demo_install(self, button):
        """Demo install operation with realistic progress."""
        # Disable button during installation
        button.set_sensitive(False)
        
        # Simulate realistic installation progress
        self.show_progress(_("Preparando instalación..."), 0.0)
        
        def update_progress():
            steps = [
                (_("Descargando paquete..."), 0.2),
                (_("Verificando dependencias..."), 0.4),
                (_("Instalando archivos..."), 0.6),
                (_("Configurando aplicación..."), 0.8),
                (_("Finalizando instalación..."), 0.9),
                (_("¡Instalación completada!"), 1.0)
            ]
            
            def run_step(step_index):
                if step_index < len(steps):
                    message, fraction = steps[step_index]
                    self.show_progress(message, fraction)
                    
                    # Schedule next step
                    if step_index < len(steps) - 1:
                        GLib.timeout_add(800, lambda: run_step(step_index + 1))
                    else:
                        # Installation complete
                        GLib.timeout_add(1500, lambda: self._finish_demo_install(button))
                
                return False
            
            run_step(0)
            return False
        
        GLib.timeout_add(500, update_progress)
    
    def _finish_demo_install(self, button):
        """Finish demo installation."""
        self.hide_progress()
        button.set_sensitive(True)
        
        # Show success notification
        self.show_progress(_("✅ Instalación exitosa"), 1.0)
        GLib.timeout_add(2000, self.hide_progress)
        
        return False
    
    def _on_demo_uninstall(self, button):
        """Demo uninstall operation with progress."""
        button.set_sensitive(False)
        
        self.show_progress(_("Desinstalando paquete..."), 0.0)
        
        def update_uninstall_progress():
            steps = [
                (_("Deteniendo servicios..."), 0.3),
                (_("Eliminando archivos..."), 0.7),
                (_("Limpiando configuración..."), 0.9),
                (_("¡Desinstalación completada!"), 1.0)
            ]
            
            def run_step(step_index):
                if step_index < len(steps):
                    message, fraction = steps[step_index]
                    self.show_progress(message, fraction)
                    
                    if step_index < len(steps) - 1:
                        GLib.timeout_add(600, lambda: run_step(step_index + 1))
                    else:
                        GLib.timeout_add(1000, lambda: self._finish_demo_uninstall(button))
                
                return False
            
            run_step(0)
            return False
        
        GLib.timeout_add(300, update_uninstall_progress)
    
    def _finish_demo_uninstall(self, button):
        """Finish demo uninstallation."""
        self.hide_progress()
        button.set_sensitive(True)
        
        self.show_progress(_("✅ Desinstalación exitosa"), 1.0)
        GLib.timeout_add(2000, self.hide_progress)
        
        return False
    
    # Window control button callbacks
    def _on_minimize_window(self, button):
        """Minimize the window."""
        self.iconify()
    
    def _on_maximize_toggle(self, button):
        """Toggle between maximize and restore."""
        if self.is_maximized():
            self.unmaximize()
        else:
            self.maximize()
    
    def _on_close_window(self, button):
        """Close the window."""
        self.close()
    
    def _on_window_state_changed(self, window, event):
        """Update maximize button when window state changes."""
        if hasattr(self, 'maximize_button'):
            if event.new_window_state & Gdk.WindowState.MAXIMIZED:
                self.maximize_button.set_image(Gtk.Image.new_from_icon_name('window-restore', Gtk.IconSize.MENU))
                self.maximize_button.set_tooltip_text(_("Restore"))
            else:
                self.maximize_button.set_image(Gtk.Image.new_from_icon_name('window-maximize', Gtk.IconSize.MENU))
                self.maximize_button.set_tooltip_text(_("Maximize"))
        return False
