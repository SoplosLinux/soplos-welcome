"""
Software tab router for Soplos Welcome.
Intelligently detects desktop environment and loads appropriate software management interface.
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

from core.i18n_manager import _
from core.environment import DesktopEnvironment


class SoftwareTab(Gtk.Box):
    """
    Smart software management router that detects the desktop environment
    and loads the appropriate software management interface.
    """
    
    def __init__(self, i18n_manager, theme_manager, environment_detector, parent_window, progress_bar, progress_label):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        
        self.i18n_manager = i18n_manager
        self.theme_manager = theme_manager
        self.environment_detector = environment_detector
        self.parent_window = parent_window
        self.progress_bar = progress_bar
        self.progress_label = progress_label
        
        # Detect desktop environment
        self.desktop_environment = self._detect_desktop_environment()
        
        # Load appropriate software tab
        self._load_desktop_specific_tab()
    
    def _detect_desktop_environment(self):
        """Detect the current desktop environment."""
        try:
            env_info = self.environment_detector.detect_all()
            de_name = env_info.get('desktop_environment', 'unknown').lower()
            
            if 'gnome' in de_name:
                return DesktopEnvironment.GNOME
            elif 'kde' in de_name or 'plasma' in de_name:
                return DesktopEnvironment.KDE  
            elif 'xfce' in de_name:
                return DesktopEnvironment.XFCE
            else:
                # Default fallback to XFCE for unknown environments
                return DesktopEnvironment.XFCE
                
        except Exception as e:
            print(f"Error detecting desktop environment: {e}")
            return DesktopEnvironment.XFCE
    
    def _load_desktop_specific_tab(self):
        """Load the appropriate desktop-specific software tab."""
        try:
            if self.desktop_environment == DesktopEnvironment.GNOME:
                from .software_gnome_tab import SoftwareGnomeTab
                software_tab = SoftwareGnomeTab(
                    self.i18n_manager,
                    self.theme_manager, 
                    self.parent_window,
                    self.progress_bar,
                    self.progress_label
                )
                print("🌊 Loading GNOME software interface")
                
            elif self.desktop_environment == DesktopEnvironment.KDE:
                from .software_plasma_tab import SoftwarePlasmaTab
                software_tab = SoftwarePlasmaTab(
                    self.i18n_manager,
                    self.theme_manager,
                    self.parent_window, 
                    self.progress_bar,
                    self.progress_label
                )
                print("🔷 Loading Plasma software interface")
                
            else:  # XFCE or unknown
                from .software_xfce_tab import SoftwareXfceTab
                software_tab = SoftwareXfceTab(
                    self.i18n_manager,
                    self.theme_manager,
                    self.parent_window,
                    self.progress_bar, 
                    self.progress_label
                )
                print("🖥️ Loading XFCE software interface")
            
            # Add the desktop-specific tab to this container
            self.pack_start(software_tab, True, True, 0)
            software_tab.show_all()
            
        except ImportError as e:
            print(f"Error loading desktop-specific software tab: {e}")
            # Fallback to a basic placeholder
            self._create_fallback_tab()
    
    def _create_fallback_tab(self):
        """Create a fallback tab when desktop-specific tabs are not available."""
        fallback_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        fallback_box.set_margin_left(30)
        fallback_box.set_margin_right(30)
        fallback_box.set_margin_top(30)
        fallback_box.set_margin_bottom(30)
        
        # Header
        title = Gtk.Label()
        title.set_markup(f"<span size='20000' weight='bold'>{_('Software Management')}</span>")
        title.set_halign(Gtk.Align.START)
        fallback_box.pack_start(title, False, False, 0)
        
        # Status message
        status_msg = Gtk.Label()
        de_name = self.desktop_environment.value if self.desktop_environment else "unknown"
        status_msg.set_markup(f"<span size='12000'>{_('Loading software management for')} {de_name.upper()}...</span>")
        status_msg.set_halign(Gtk.Align.START)
        fallback_box.pack_start(status_msg, False, False, 0)
        
        # Info message
        info_msg = Gtk.Label()
        info_msg.set_markup(f"<span size='11000'>{_('Desktop-specific software interface will be available soon.')}</span>")
        info_msg.set_halign(Gtk.Align.START)
        info_msg.get_style_context().add_class('dim-label')
        fallback_box.pack_start(info_msg, False, False, 0)
        
        self.pack_start(fallback_box, True, True, 0)
        fallback_box.show_all()
