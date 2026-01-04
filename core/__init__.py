"""
Core module for Soplos Welcome.
Contains the main application logic, environment detection, and system management.
"""

__version__ = "2.0.2"
__author__ = "Sergi Perich"
__email__ = "info@soploslinux.com"
__license__ = "GPL-3.0+"

# Core module exports
from .application import SoplosWelcomeApplication, create_application, run_application
from .environment import (
    EnvironmentDetector, 
    DesktopEnvironment, 
    DisplayProtocol, 
    ThemeType,
    get_environment_detector,
    detect_environment
)
from .theme_manager import ThemeManager, get_theme_manager, initialize_theming
from .i18n_manager import I18nManager, get_i18n_manager, initialize_i18n, _, ngettext

__all__ = [
    # Application
    'SoplosWelcomeApplication',
    'create_application', 
    'run_application',
    
    # Environment Detection
    'EnvironmentDetector',
    'DesktopEnvironment',
    'DisplayProtocol', 
    'ThemeType',
    'get_environment_detector',
    'detect_environment',
    
    # Theme Management
    'ThemeManager',
    'get_theme_manager',
    'initialize_theming',
    
    # Internationalization
    'I18nManager',
    'get_i18n_manager', 
    'initialize_i18n',
    '_',
    'ngettext'
]
