"""
Environment detection module for Soplos Welcome.
Handles desktop environment detection, display protocol identification,
and system environment configuration.
"""

import os
import subprocess
import configparser
from pathlib import Path
from typing import Dict, Optional, Tuple
from enum import Enum


class DesktopEnvironment(Enum):
    """Supported desktop environments."""
    GNOME = "gnome"
    KDE = "kde"
    XFCE = "xfce"
    UNKNOWN = "unknown"


class DisplayProtocol(Enum):
    """Display server protocols."""
    X11 = "x11"
    WAYLAND = "wayland"
    UNKNOWN = "unknown"


class ThemeType(Enum):
    """System theme types."""
    LIGHT = "light"
    DARK = "dark"
    UNKNOWN = "unknown"


class EnvironmentDetector:
    """
    Detects and analyzes the current desktop environment, display protocol,
    and system theme preferences.
    """
    
    def __init__(self):
        self._desktop_env = None
        self._display_protocol = None
        self._theme_type = None
        self._environment_info = {}
        
    def detect_all(self) -> Dict[str, str]:
        """
        Performs complete environment detection.
        
        Returns:
            Dictionary with all detected environment information
        """
        self._detect_desktop_environment()
        self._detect_display_protocol()
        self._detect_theme_type()
        self._detect_additional_info()
        
        return {
            'desktop_environment': self._desktop_env.value,
            'display_protocol': self._display_protocol.value,
            'theme_type': self._theme_type.value,
            'environment_info': self._environment_info
        }
    
    def _detect_desktop_environment(self) -> DesktopEnvironment:
        """Detects the current desktop environment."""
        # Check XDG_CURRENT_DESKTOP first (most reliable)
        current_desktop = os.environ.get('XDG_CURRENT_DESKTOP', '').lower()
        
        if 'gnome' in current_desktop:
            self._desktop_env = DesktopEnvironment.GNOME
        elif 'kde' in current_desktop or 'plasma' in current_desktop:
            self._desktop_env = DesktopEnvironment.KDE
        elif 'xfce' in current_desktop:
            self._desktop_env = DesktopEnvironment.XFCE
        else:
            # Fallback detection methods
            self._desktop_env = self._fallback_desktop_detection()
        
        return self._desktop_env
    
    def _fallback_desktop_detection(self) -> DesktopEnvironment:
        """Fallback method for desktop environment detection."""
        # Check for specific processes
        try:
            result = subprocess.run(['pgrep', '-f'], 
                                   input='gnome-shell|kwin|xfwm4', 
                                   text=True, 
                                   capture_output=True)
            
            if 'gnome-shell' in result.stdout:
                return DesktopEnvironment.GNOME
            elif 'kwin' in result.stdout:
                return DesktopEnvironment.KDE
            elif 'xfwm4' in result.stdout:
                return DesktopEnvironment.XFCE
        except subprocess.SubprocessError:
            pass
        
        # Check for environment variables
        if os.environ.get('GNOME_DESKTOP_SESSION_ID'):
            return DesktopEnvironment.GNOME
        elif os.environ.get('KDE_SESSION_VERSION'):
            return DesktopEnvironment.KDE
        elif os.environ.get('XFCE_PANEL_MIGRATE_DEFAULT'):
            return DesktopEnvironment.XFCE
        
        return DesktopEnvironment.UNKNOWN
    
    def _detect_display_protocol(self) -> DisplayProtocol:
        """Detects the display server protocol (X11 or Wayland)."""
        session_type = os.environ.get('XDG_SESSION_TYPE', '').lower()
        
        if session_type == 'wayland':
            self._display_protocol = DisplayProtocol.WAYLAND
        elif session_type == 'x11' or os.environ.get('DISPLAY'):
            self._display_protocol = DisplayProtocol.X11
        else:
            self._display_protocol = DisplayProtocol.UNKNOWN
            
        return self._display_protocol
    
    def _detect_theme_type(self) -> ThemeType:
        """Detects system theme preference (dark/light)."""
        try:
            if self._desktop_env == DesktopEnvironment.GNOME:
                self._theme_type = self._detect_gnome_theme()
            elif self._desktop_env == DesktopEnvironment.KDE:
                self._theme_type = self._detect_kde_theme()
            elif self._desktop_env == DesktopEnvironment.XFCE:
                self._theme_type = self._detect_xfce_theme()
            else:
                self._theme_type = ThemeType.UNKNOWN
        except Exception:
            self._theme_type = ThemeType.UNKNOWN
            
        return self._theme_type
    
    def _detect_gnome_theme(self) -> ThemeType:
        """Detects GNOME theme preference."""
        try:
            result = subprocess.run([
                'gsettings', 'get', 'org.gnome.desktop.interface', 'color-scheme'
            ], capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0:
                if 'dark' in result.stdout.lower():
                    return ThemeType.DARK
                elif 'light' in result.stdout.lower():
                    return ThemeType.LIGHT
        except (subprocess.SubprocessError, subprocess.TimeoutExpired):
            pass
        
        # Fallback: check GTK theme
        try:
            result = subprocess.run([
                'gsettings', 'get', 'org.gnome.desktop.interface', 'gtk-theme'
            ], capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0 and 'dark' in result.stdout.lower():
                return ThemeType.DARK
        except (subprocess.SubprocessError, subprocess.TimeoutExpired):
            pass
            
        return ThemeType.LIGHT  # Default to light
    
    def _detect_kde_theme(self) -> ThemeType:
        """Detects KDE theme preference."""
        # 1. Check kdeglobals (standard KDE config)
        try:
            kde_config = Path.home() / '.config' / 'kdeglobals'
            if kde_config.exists():
                config = configparser.ConfigParser()
                config.read(kde_config)
                
                # Check color scheme
                if 'General' in config:
                    color_scheme = config['General'].get('ColorScheme', '').lower()
                    if 'dark' in color_scheme or 'black' in color_scheme:
                        return ThemeType.DARK
                
                # Check background color
                if 'Colors:Window' in config:
                    bg_color = config['Colors:Window'].get('BackgroundNormal', '')
                    if bg_color:
                        try:
                            r, g, b = map(int, bg_color.split(','))
                            if (r + g + b) / 3 < 128:
                                return ThemeType.DARK
                        except ValueError:
                            pass
        except Exception:
            pass

        # 2. Check GTK3 settings (KDE syncs to this)
        try:
            gtk_config = Path.home() / '.config' / 'gtk-3.0' / 'settings.ini'
            if gtk_config.exists():
                config = configparser.ConfigParser()
                config.read(gtk_config)
                if 'Settings' in config:
                    # Check prefer-dark-theme
                    prefer_dark = config['Settings'].get('gtk-application-prefer-dark-theme', '').lower()
                    if prefer_dark in ['1', 'true', 'yes']:
                        return ThemeType.DARK
                    
                    # Check theme name
                    theme_name = config['Settings'].get('gtk-theme-name', '').lower()
                    if 'dark' in theme_name:
                        return ThemeType.DARK
        except Exception:
            pass
            
        return ThemeType.LIGHT  # Default to light

    def _detect_xfce_theme(self) -> ThemeType:
        """Detects XFCE theme preference."""
        try:
            # Check XFCE4 settings
            result = subprocess.run([
                'xfconf-query', '-c', 'xsettings', '-p', '/Net/ThemeName'
            ], capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0 and 'dark' in result.stdout.lower():
                return ThemeType.DARK
                
        except (subprocess.SubprocessError, subprocess.TimeoutExpired):
            pass
        
        return ThemeType.LIGHT  # Default to light
    
    def _detect_additional_info(self):
        """Collects additional environment information."""
        self._environment_info = {
            'desktop_session': os.environ.get('DESKTOP_SESSION', ''),
            'gdm_session': os.environ.get('GDMSESSION', ''),
            'window_manager': self._detect_window_manager(),
            'gtk_version': self._detect_gtk_version(),
            'qt_version': self._detect_qt_version(),
        }
    
    def _detect_window_manager(self) -> str:
        """Detects the current window manager."""
        try:
            # Try wmctrl first
            result = subprocess.run(['wmctrl', '-m'], 
                                   capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if line.startswith('Name:'):
                        return line.split(':', 1)[1].strip()
        except (subprocess.SubprocessError, subprocess.TimeoutExpired):
            pass
        
        # Fallback: check common window managers
        wm_processes = ['kwin', 'gnome-shell', 'xfwm4', 'openbox', 'i3', 'awesome']
        try:
            for wm in wm_processes:
                result = subprocess.run(['pgrep', wm], 
                                       capture_output=True, timeout=2)
                if result.returncode == 0:
                    return wm
        except (subprocess.SubprocessError, subprocess.TimeoutExpired):
            pass
            
        return 'unknown'
    
    def _detect_gtk_version(self) -> str:
        """Detects GTK version."""
        try:
            import gi
            gi.require_version('Gtk', '3.0')
            from gi.repository import Gtk
            return f"{Gtk.get_major_version()}.{Gtk.get_minor_version()}.{Gtk.get_micro_version()}"
        except ImportError:
            return 'unknown'
    
    def _detect_qt_version(self) -> str:
        """Detects Qt version if available."""
        try:
            result = subprocess.run(['qmake', '--version'], 
                                   capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'Qt version' in line:
                        return line.split()[-1]
        except (subprocess.SubprocessError, subprocess.TimeoutExpired):
            pass
        
        return 'unknown'
    
    # Public properties for easy access
    @property
    def desktop_environment(self) -> DesktopEnvironment:
        """Current desktop environment."""
        if self._desktop_env is None:
            self._detect_desktop_environment()
        return self._desktop_env
    
    @property
    def display_protocol(self) -> DisplayProtocol:
        """Current display protocol."""
        if self._display_protocol is None:
            self._detect_display_protocol()
        return self._display_protocol
    
    @property
    def theme_type(self) -> ThemeType:
        """Current theme type."""
        if self._theme_type is None:
            self._detect_theme_type()
        return self._theme_type
    
    @property
    def is_wayland(self) -> bool:
        """True if running on Wayland."""
        return self.display_protocol == DisplayProtocol.WAYLAND
    
    @property
    def is_dark_theme(self) -> bool:
        """True if using dark theme."""
        return self.theme_type == ThemeType.DARK
    
    def configure_environment_variables(self):
        """
        Configures environment variables for optimal GTK integration
        based on the detected environment.
        """
        if self.is_wayland:
            # Wayland-specific optimizations
            os.environ['GTK_USE_PORTAL'] = '1'
            os.environ['GDK_BACKEND'] = 'wayland'
            
        if self.desktop_environment == DesktopEnvironment.KDE:
            # KDE-specific optimizations
            if self.theme_type != ThemeType.UNKNOWN:
                # Only set if not already set by user/system
                if 'GTK_THEME' not in os.environ:
                    theme_name = self._get_kde_gtk_theme()
                    if theme_name:
                        os.environ['GTK_THEME'] = theme_name
        
        # Disable accessibility bus if not needed (reduces startup time)
        if not os.environ.get('ENABLE_ACCESSIBILITY'):
            os.environ['NO_AT_BRIDGE'] = '1'
            os.environ['AT_SPI_BUS'] = '0'
    
    def _get_kde_gtk_theme(self) -> Optional[str]:
        """Gets the appropriate GTK theme for KDE integration."""
        try:
            if self.theme_type == ThemeType.DARK:
                return 'Breeze-Dark'
            else:
                return 'Breeze'
        except Exception:
            return None


# Global instance for easy access
_environment_detector = None

def get_environment_detector() -> EnvironmentDetector:
    """
    Returns the global environment detector instance.
    Creates it if it doesn't exist.
    """
    global _environment_detector
    if _environment_detector is None:
        _environment_detector = EnvironmentDetector()
    return _environment_detector

def detect_environment() -> Dict[str, str]:
    """
    Convenience function to detect all environment information.
    
    Returns:
        Dictionary with complete environment detection results
    """
    detector = get_environment_detector()
    return detector.detect_all()
