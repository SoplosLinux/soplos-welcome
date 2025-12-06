"""
Main application class for Soplos Welcome.
Handles application lifecycle, initialization, and coordination between modules.
"""

import sys
import os
import signal
from pathlib import Path
from typing import Optional

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, Gio

from .environment import get_environment_detector
from .theme_manager import get_theme_manager, initialize_theming
from .i18n_manager import get_i18n_manager, initialize_i18n, _


class SoplosWelcomeApplication(Gtk.Application):
    """
    Main application class for Soplos Welcome.
    Manages the application lifecycle and coordinates between all components.
    """
    
    def __init__(self):
        """Initialize the Soplos Welcome application."""
        super().__init__(
            application_id='org.soplos.welcome',
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE
        )
        
        # Application state
        self.main_window = None
        self.environment_detector = None
        self.theme_manager = None
        self.i18n_manager = None
        
        # Application paths
        self.app_path = Path(__file__).parent.parent
        self.assets_path = self.app_path / 'assets'
        self.locale_path = self.app_path / 'locale'
        
        # Connect signals
        self.connect('startup', self.on_startup)
        self.connect('activate', self.on_activate)
        self.connect('command-line', self.on_command_line)
        self.connect('shutdown', self.on_shutdown)
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._handle_signal)
        signal.signal(signal.SIGTERM, self._handle_signal)
        
    def on_shutdown(self, app):
        """Called when the application shuts down."""
        print("Shutting down Soplos Welcome...")
        self._cleanup_garbage()

    def _cleanup_garbage(self):
        """Remove __pycache__ and other temporary files."""
        try:
            import shutil
            root_path = self.app_path
            print(f"Cleaning runtimes from: {root_path}")
            
            # Clean __pycache__
            for root, dirs, files in os.walk(root_path):
                if '__pycache__' in dirs:
                    pycache_path = os.path.join(root, '__pycache__')
                    try:
                        shutil.rmtree(pycache_path, ignore_errors=True)
                    except Exception:
                        pass
                        
            # Clean any rogue .deb files in root/bin that might have slipped (strict policy)
            # This addresses the user's specific complaint about r2modman.deb
            for file in os.listdir(root_path):
                if file.endswith(".deb") or (file.endswith(".sh") and "makeresolve" not in file):
                   try:
                       os.remove(os.path.join(root_path, file))
                       print(f"Removed rogue file: {file}")
                   except Exception:
                       pass
                       
        except Exception as e:
            print(f"Cleanup warning: {e}")
    
    def on_startup(self, app):
        """Called when the application starts up."""
        print("Starting Soplos Welcome 2.0...")
        
        # Initialize core systems
        self._initialize_environment()
        self._initialize_internationalization()
        self._initialize_theming()
        self._setup_application_properties()
        
        print("Application initialization completed")
    
    def on_activate(self, app):
        """Called when the application is activated."""
        if self.main_window is None:
            self._create_main_window()
        
        # Present the window
        self.main_window.present()
    
    def on_command_line(self, app, command_line):
        """Handle command line arguments."""
        args = command_line.get_arguments()
        
        # Parse command line options
        if len(args) > 1:
            for arg in args[1:]:  # Skip program name
                if arg in ['--help', '-h']:
                    self._print_help()
                    return 0
                elif arg in ['--version', '-v']:
                    self._print_version()
                    return 0
                elif arg.startswith('--lang='):
                    lang_code = arg.split('=', 1)[1]
                    if self.i18n_manager.set_language(lang_code):
                        print(f"Language set to: {lang_code}")
                    else:
                        print(f"Invalid language code: {lang_code}")
                elif arg.startswith('--theme='):
                    theme_name = arg.split('=', 1)[1]
                    if self.theme_manager.load_theme(theme_name):
                        print(f"Theme set to: {theme_name}")
                    else:
                        print(f"Invalid theme: {theme_name}")
                elif arg in ['--debug']:
                    self._enable_debug_mode()
                else:
                    print(f"Unknown argument: {arg}")
        
        # Activate the application
        self.activate()
        return 0
    
    def _initialize_environment(self):
        """Initialize environment detection."""
        try:
            self.environment_detector = get_environment_detector()
            env_info = self.environment_detector.detect_all()
            
            print(f"Desktop Environment: {env_info['desktop_environment']}")
            print(f"Display Protocol: {env_info['display_protocol']}")
            print(f"Theme Type: {env_info['theme_type']}")
            
            # Configure environment variables for optimal integration
            self.environment_detector.configure_environment_variables()
            
        except Exception as e:
            print(f"Error initializing environment detection: {e}")
            # Continue with defaults
    
    def _initialize_internationalization(self):
        """Initialize the internationalization system."""
        try:
            current_lang = initialize_i18n(str(self.locale_path))
            self.i18n_manager = get_i18n_manager()
            
            print(f"Language initialized: {current_lang}")
            
            # Set up gettext for the entire application
            import gettext
            gettext.bindtextdomain('soplos-welcome', str(self.locale_path))
            gettext.textdomain('soplos-welcome')
            
        except Exception as e:
            print(f"Error initializing internationalization: {e}")
            # Continue with English defaults
    
    def _initialize_theming(self):
        """Initialize the theming system."""
        try:
            loaded_theme = initialize_theming(str(self.assets_path))
            self.theme_manager = get_theme_manager()
            
            print(f"Theme loaded: {loaded_theme}")
            
        except Exception as e:
            print(f"Error initializing theming: {e}")
            # Continue with default GTK theme
    
    def _setup_application_properties(self):
        """Setup application-wide properties."""
        # Set application name and icon
        GLib.set_prgname('org.soplos.welcome')
        GLib.set_application_name(_('Soplos Welcome'))
        
        # Set WM_CLASS for better integration
        if hasattr(Gdk, 'set_program_class'):
            Gdk.set_program_class('org.soplos.welcome')
        
        # Set default window icon
        icon_path = self.assets_path / 'icons' / 'org.soplos.welcome.png'
        if icon_path.exists():
            try:
                Gtk.Window.set_default_icon_from_file(str(icon_path))
            except Exception as e:
                print(f"Error setting application icon: {e}")
        
        # Set up application menu (if needed)
        self._setup_application_menu()
    
    def _setup_application_menu(self):
        """Setup application menu for GNOME integration."""
        if self.environment_detector and self.environment_detector.desktop_environment.value == 'gnome':
            # Create application menu for GNOME
            menu = Gio.Menu()
            
            # Preferences action
            preferences_action = Gio.SimpleAction.new('preferences', None)
            preferences_action.connect('activate', self._on_preferences)
            self.add_action(preferences_action)
            menu.append(_('Preferences'), 'app.preferences')
            
            # About action
            about_action = Gio.SimpleAction.new('about', None)
            about_action.connect('activate', self._on_about)
            self.add_action(about_action)
            menu.append(_('About'), 'app.about')
            
            # Quit action
            quit_action = Gio.SimpleAction.new('quit', None)
            quit_action.connect('activate', self._on_quit)
            self.add_action(quit_action)
            menu.append(_('Quit'), 'app.quit')
            
            self.set_app_menu(menu)
    
    def _create_main_window(self):
        """Create the main application window."""
        try:
            # Import here to avoid circular imports
            from ui.main_window import MainWindow
            
            self.main_window = MainWindow(
                application=self,
                environment_detector=self.environment_detector,
                theme_manager=self.theme_manager,
                i18n_manager=self.i18n_manager
            )
            
            # Connect window destroy signal
            self.main_window.connect('destroy', self._on_window_destroy)
            
        except Exception as e:
            print(f"Error creating main window: {e}")
            self.quit()
    
    def _on_preferences(self, action, parameter):
        """Handle preferences action."""
        # TODO: Implement preferences dialog
        print("Preferences dialog not yet implemented")
    
    def _on_about(self, action, parameter):
        """Handle about action."""
        if self.main_window:
            self.main_window.show_about_dialog()
    
    def _on_quit(self, action, parameter):
        """Handle quit action."""
        self.quit()
    
    def _on_window_destroy(self, window):
        """Handle main window destruction."""
        self.main_window = None
        self.quit()
    
    def _handle_signal(self, signum, frame):
        """Handle system signals for graceful shutdown."""
        print(f"Received signal {signum}, shutting down...")
        GLib.idle_add(self.quit)
    
    def _print_help(self):
        """Print command line help."""
        help_text = _("""
Soplos Welcome 2.0 - The world's most advanced welcome application

Usage: soplos-welcome [OPTIONS]

Options:
  -h, --help              Show this help message
  -v, --version           Show version information
  --lang=LANG             Set language (es, en, fr, de, pt, it, ro, ru)
  --theme=THEME           Set theme (base, light, dark, gnome, kde, xfce)
  --debug                 Enable debug mode

Examples:
  soplos-welcome                    # Start with auto-detected settings
  soplos-welcome --lang=es          # Start in Spanish
  soplos-welcome --theme=dark       # Start with dark theme
  soplos-welcome --debug            # Start in debug mode

For more information, visit: https://soplos.org
""")
        print(help_text)
    
    def _print_version(self):
        """Print version information."""
        from core import __version__
        
        version_text = _("""
Soplos Welcome {version}

Copyright (C) 2025 Sergi Perich
This is free software; see the source for copying conditions.
There is NO warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

Desktop Environment: {desktop_env}
Display Protocol: {display_protocol}
Theme: {theme}
Language: {language}
""").format(
            version=__version__,
            desktop_env=self.environment_detector.desktop_environment.value if self.environment_detector else 'unknown',
            display_protocol=self.environment_detector.display_protocol.value if self.environment_detector else 'unknown',
            theme=self.theme_manager.current_theme if self.theme_manager else 'unknown',
            language=self.i18n_manager.get_current_language() if self.i18n_manager else 'unknown'
        )
        print(version_text)
    
    def _enable_debug_mode(self):
        """Enable debug mode with verbose output."""
        os.environ['SOPLOS_DEBUG'] = '1'
        print("Debug mode enabled")
        
        # Enable GTK debug if available
        os.environ['GTK_DEBUG'] = 'all'
        os.environ['G_MESSAGES_DEBUG'] = 'all'
    
    def get_application_info(self) -> dict:
        """
        Get comprehensive application information.
        
        Returns:
            Dictionary with application state information
        """
        return {
            'version': getattr(__import__('core'), '__version__', '2.0.0'),
            'app_path': str(self.app_path),
            'assets_path': str(self.assets_path),
            'locale_path': str(self.locale_path),
            'current_language': self.i18n_manager.get_current_language() if self.i18n_manager else 'unknown',
            'current_theme': self.theme_manager.current_theme if self.theme_manager else 'unknown',
            'environment_info': self.environment_detector.detect_all() if self.environment_detector else {},
            'window_active': self.main_window is not None
        }


def create_application() -> SoplosWelcomeApplication:
    """
    Create and return a new Soplos Welcome application instance.
    
    Returns:
        New SoplosWelcomeApplication instance
    """
    return SoplosWelcomeApplication()

def run_application(argv: list = None) -> int:
    """
    Run the Soplos Welcome application.
    
    Args:
        argv: Command line arguments (uses sys.argv if None)
        
    Returns:
        Application exit code
    """
    if argv is None:
        argv = sys.argv
    
    app = create_application()
    
    try:
        exit_code = app.run(argv)
        return exit_code
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        return 130
    except Exception as e:
        print(f"Application error: {e}")
        return 1
