"""
User interface module for Soplos Welcome.
Contains all GTK-based UI components, windows, tabs, widgets, and dialogs.
"""

# UI module information
__version__ = "2.0.1"
__author__ = "Sergi Perich"

# Re-export main components when they're available
# Note: Imports are conditional to avoid circular dependencies

try:
    from .main_window import MainWindow
    __all__ = ['MainWindow']
except ImportError:
    # MainWindow not yet available
    __all__ = []

# UI Constants
DEFAULT_WINDOW_WIDTH = 1000
DEFAULT_WINDOW_HEIGHT = 700
MIN_WINDOW_WIDTH = 800
MIN_WINDOW_HEIGHT = 600

# CSS Classes
CSS_CLASSES = {
    'window': 'soplos-welcome-window',
    'content': 'soplos-content', 
    'tab': 'soplos-tab',
    'card': 'soplos-card',
    'button_install': 'soplos-button-install',
    'button_uninstall': 'soplos-button-uninstall',
    'button_primary': 'soplos-button-primary',
    'status_label': 'soplos-status-label',
    'progress_bar': 'soplos-progress-bar',
    'icon_large': 'soplos-icon-large',
    'icon_medium': 'soplos-icon-medium',
    'icon_small': 'soplos-icon-small',
    'separator': 'soplos-separator',
    'welcome_title': 'soplos-welcome-title',
    'welcome_subtitle': 'soplos-welcome-subtitle',
    'software_grid': 'soplos-software-grid',
    'software_item': 'soplos-software-item',
    'hardware_info': 'soplos-hardware-info'
}
