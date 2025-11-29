"""
Theme management system for Soplos Welcome.
Handles CSS theme loading, application, and dynamic theme switching.
"""

import os
from pathlib import Path
from typing import Dict, Optional, List
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from .environment import get_environment_detector, DesktopEnvironment, ThemeType


class ThemeManager:
    """
    Manages CSS themes for the application with automatic detection
    and desktop environment integration.
    """
    
    def __init__(self, assets_path: str):
        """
        Initialize the theme manager.
        
        Args:
            assets_path: Path to the assets directory containing themes
        """
        self.assets_path = Path(assets_path)
        self.themes_path = self.assets_path / 'themes'
        self.css_provider = None
        self.current_theme = None
        self.environment_detector = get_environment_detector()
        
        # Ensure themes directory exists
        self.themes_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize CSS provider
        self._init_css_provider()
    
    def _init_css_provider(self):
        """Initialize the GTK CSS provider."""
        self.css_provider = Gtk.CssProvider()
        
        # Add to default screen
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(
            screen, 
            self.css_provider, 
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
    
    def get_available_themes(self) -> List[str]:
        """
        Get list of available theme names.
        
        Returns:
            List of theme names (without .css extension)
        """
        if not self.themes_path.exists():
            return []
        
        themes = []
        for theme_file in self.themes_path.glob('*.css'):
            themes.append(theme_file.stem)
        
        return sorted(themes)
    
    def detect_optimal_theme(self) -> str:
        """
        Detects the optimal theme based on the current environment.
        
        Returns:
            Theme name that best matches the current environment
        """
        env_info = self.environment_detector.detect_all()
        desktop_env = env_info['desktop_environment']
        theme_type = env_info['theme_type']
        
        # Priority order for theme selection
        theme_candidates = []
        
        # 1. Desktop-specific theme with light/dark variant
        if desktop_env != 'unknown':
            theme_candidates.append(f"{desktop_env}-{theme_type}")
            theme_candidates.append(f"{desktop_env}")
        
        # 2. Generic light/dark theme
        theme_candidates.append(theme_type)
        
        # 3. Base theme
        theme_candidates.append('base')
        
        # 4. Fallback themes
        theme_candidates.extend(['light', 'default'])
        
        # Find the first available theme
        available_themes = self.get_available_themes()
        for candidate in theme_candidates:
            if candidate in available_themes:
                return candidate
        
        # Ultimate fallback
        if available_themes:
            return available_themes[0]
        
        return 'base'  # Will create if doesn't exist
    
    def load_theme(self, theme_name: str) -> bool:
        """
        Load and apply a specific theme.
        
        Args:
            theme_name: Name of the theme to load
            
        Returns:
            True if theme was loaded successfully, False otherwise
        """
        theme_path = self.themes_path / f"{theme_name}.css"
        
        if not theme_path.exists():
            # Try to create a basic theme if it doesn't exist
            if theme_name == 'base':
                self._create_base_theme()
            else:
                print(f"Theme '{theme_name}' not found at {theme_path}")
                return False
        
        try:
            self.css_provider.load_from_path(str(theme_path))
            self.current_theme = theme_name
            print(f"Successfully loaded theme: {theme_name}")
            return True
        except Exception as e:
            print(f"Error loading theme '{theme_name}': {e}")
            return False
    
    def load_optimal_theme(self) -> str:
        """
        Automatically detects and loads the optimal theme.
        
        Returns:
            Name of the loaded theme
        """
        optimal_theme = self.detect_optimal_theme()
        
        if self.load_theme(optimal_theme):
            return optimal_theme
        
        # Fallback to base theme
        if optimal_theme != 'base':
            if self.load_theme('base'):
                return 'base'
        
        print("Warning: No theme could be loaded")
        return 'none'
    
    def reload_current_theme(self):
        """Reload the currently active theme."""
        if self.current_theme:
            self.load_theme(self.current_theme)
    
    def add_custom_css(self, css_content: str):
        """
        Add custom CSS content to the current theme.
        
        Args:
            css_content: CSS content to add
        """
        try:
            self.css_provider.load_from_data(css_content.encode('utf-8'))
        except Exception as e:
            print(f"Error adding custom CSS: {e}")
    
    def _create_base_theme(self):
        """Create a basic base theme if it doesn't exist."""
        base_theme_content = """
/* Base Theme for Soplos Welcome */

/* Application Window */
.soplos-welcome-window {
    background-color: @theme_bg_color;
    color: @theme_fg_color;
}

/* Main Content Area */
.soplos-content {
    padding: 20px;
    background-color: @theme_base_color;
    border-radius: 8px;
}

/* Tabs */
.soplos-tab {
    padding: 10px 20px;
    border-radius: 6px 6px 0 0;
    background-color: @theme_bg_color;
    border: 1px solid @borders;
    border-bottom: none;
}

.soplos-tab:checked {
    background-color: @theme_base_color;
    color: @theme_selected_fg_color;
}

/* Buttons */
.soplos-button-install {
    background-color: @theme_selected_bg_color;
    color: @theme_selected_fg_color;
    border-radius: 6px;
    padding: 8px 16px;
    border: 1px solid @borders;
}

.soplos-button-uninstall {
    background-color: @error_color;
    color: white;
    border-radius: 6px;
    padding: 8px 16px;
    border: 1px solid @borders;
}

.soplos-button-primary {
    background-color: @theme_selected_bg_color;
    color: @theme_selected_fg_color;
    border-radius: 6px;
    padding: 10px 20px;
    border: 1px solid @borders;
    font-weight: bold;
}

/* Cards and Containers */
.soplos-card {
    background-color: @theme_base_color;
    border: 1px solid @borders;
    border-radius: 8px;
    padding: 16px;
    margin: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Status and Progress */
.soplos-status-label {
    color: @theme_fg_color;
    font-size: 14px;
}

.soplos-progress-bar {
    border-radius: 4px;
}

/* Icons */
.soplos-icon-large {
    -gtk-icon-size: 48px;
}

.soplos-icon-medium {
    -gtk-icon-size: 32px;
}

.soplos-icon-small {
    -gtk-icon-size: 16px;
}

/* Separators */
.soplos-separator {
    background-color: @borders;
    margin: 10px 0;
}

/* Welcome Screen Specific */
.soplos-welcome-title {
    font-size: 24px;
    font-weight: bold;
    color: @theme_selected_bg_color;
    margin-bottom: 10px;
}

.soplos-welcome-subtitle {
    font-size: 16px;
    color: @theme_fg_color;
    margin-bottom: 20px;
}

/* Software Tab Specific */
.soplos-software-grid {
    padding: 10px;
}

.soplos-software-item {
    padding: 10px;
    border-radius: 6px;
    background-color: @theme_base_color;
    border: 1px solid @borders;
    margin: 4px;
}

.soplos-software-item:hover {
    background-color: @theme_selected_bg_color;
    color: @theme_selected_fg_color;
}

/* Hardware Tab Specific */
.soplos-hardware-info {
    font-family: monospace;
    background-color: @theme_base_color;
    border: 1px solid @borders;
    border-radius: 4px;
    padding: 10px;
}

/* Responsive Design */
@media (max-width: 800px) {
    .soplos-content {
        padding: 10px;
    }
    
    .soplos-card {
        margin: 4px;
        padding: 12px;
    }
}
"""
        
        base_theme_path = self.themes_path / 'base.css'
        try:
            with open(base_theme_path, 'w', encoding='utf-8') as f:
                f.write(base_theme_content)
            print(f"Created base theme at {base_theme_path}")
        except Exception as e:
            print(f"Error creating base theme: {e}")
    
    def create_dark_theme(self):
        """Create a dark theme variant."""
        dark_theme_content = """
/* Dark Theme for Soplos Welcome */
@import url('base.css');

/* Override colors for dark theme */
@define-color theme_bg_color #2b2b2b;
@define-color theme_fg_color #ffffff;
@define-color theme_base_color #3c3c3c;
@define-color theme_selected_bg_color #4a90e2;
@define-color theme_selected_fg_color #ffffff;
@define-color borders #555555;
@define-color error_color #e74c3c;

/* Dark-specific adjustments */
.soplos-welcome-window {
    background-color: #2b2b2b;
    color: #ffffff;
}

.soplos-card {
    background-color: #3c3c3c;
    border-color: #555555;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.soplos-hardware-info {
    background-color: #1e1e1e;
    color: #00ff00;
    border-color: #555555;
}
"""
        
        dark_theme_path = self.themes_path / 'dark.css'
        try:
            with open(dark_theme_path, 'w', encoding='utf-8') as f:
                f.write(dark_theme_content)
            print(f"Created dark theme at {dark_theme_path}")
        except Exception as e:
            print(f"Error creating dark theme: {e}")
    
    def create_light_theme(self):
        """Create a light theme variant."""
        light_theme_content = """
/* Light Theme for Soplos Welcome */
@import url('base.css');

/* Override colors for light theme */
@define-color theme_bg_color #f5f5f5;
@define-color theme_fg_color #2c3e50;
@define-color theme_base_color #ffffff;
@define-color theme_selected_bg_color #3498db;
@define-color theme_selected_fg_color #ffffff;
@define-color borders #e0e0e0;
@define-color error_color #e74c3c;

/* Light-specific adjustments */
.soplos-welcome-window {
    background-color: #f5f5f5;
    color: #2c3e50;
}

.soplos-card {
    background-color: #ffffff;
    border-color: #e0e0e0;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.soplos-hardware-info {
    background-color: #f8f9fa;
    color: #2c3e50;
    border-color: #e0e0e0;
}
"""
        
        light_theme_path = self.themes_path / 'light.css'
        try:
            with open(light_theme_path, 'w', encoding='utf-8') as f:
                f.write(light_theme_content)
            print(f"Created light theme at {light_theme_path}")
        except Exception as e:
            print(f"Error creating light theme: {e}")
    
    def initialize_default_themes(self):
        """Create default themes if they don't exist."""
        if not (self.themes_path / 'base.css').exists():
            self._create_base_theme()
        
        if not (self.themes_path / 'dark.css').exists():
            self.create_dark_theme()
        
        if not (self.themes_path / 'light.css').exists():
            self.create_light_theme()


# Global theme manager instance
_theme_manager = None

def get_theme_manager(assets_path: str = None) -> ThemeManager:
    """
    Returns the global theme manager instance.
    
    Args:
        assets_path: Path to assets directory (only used on first call)
        
    Returns:
        Global ThemeManager instance
    """
    global _theme_manager
    if _theme_manager is None:
        if assets_path is None:
            # Default path relative to this file
            current_dir = Path(__file__).parent.parent
            assets_path = current_dir / 'assets'
        _theme_manager = ThemeManager(str(assets_path))
    return _theme_manager

def initialize_theming(assets_path: str = None) -> str:
    """
    Initialize the theming system and load the optimal theme.
    
    Args:
        assets_path: Path to assets directory
        
    Returns:
        Name of the loaded theme
    """
    theme_manager = get_theme_manager(assets_path)
    theme_manager.initialize_default_themes()
    return theme_manager.load_optimal_theme()
