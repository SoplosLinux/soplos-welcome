"""
Customization tab for Soplos Welcome.
Handles desktop customization using Soplos tools.
"""

import gi
import os
import subprocess
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, GLib

from core.i18n_manager import _


class CustomizationTab(Gtk.ScrolledWindow):
    """
    Desktop customization tab.
    Launches Soplos customization tools based on desktop environment.
    """
    
    def __init__(self, i18n_manager, theme_manager, environment_detector):
        super().__init__()
        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        
        self.i18n_manager = i18n_manager
        self.theme_manager = theme_manager
        self.environment_detector = environment_detector
        
        # Get base path for assets
        self.base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.icons_path = os.path.join(self.base_path, 'assets', 'icons', 'soplos')
        
        # Main container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        main_box.set_margin_left(30)
        main_box.set_margin_right(30)
        main_box.set_margin_top(30)
        main_box.set_margin_bottom(30)
        
        self.add(main_box)
        
        # Create UI based on desktop environment
        self._create_ui(main_box)
        
        self.show_all()
    
    def _create_ui(self, container):
        """Create the customization tab interface."""
        # Header
        header_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        
        title = Gtk.Label()
        title.set_markup(f"<span size='20000' weight='bold'>{_('Desktop Customization')}</span>")
        title.set_halign(Gtk.Align.START)
        header_box.pack_start(title, False, False, 0)
        
        subtitle = Gtk.Label()
        subtitle.set_markup(f"<span size='12000'>{_('Customize your desktop environment and themes')}</span>")
        subtitle.set_halign(Gtk.Align.START)
        subtitle.get_style_context().add_class('dim-label')
        header_box.pack_start(subtitle, False, False, 0)
        
        container.pack_start(header_box, False, False, 0)
        
        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        container.pack_start(separator, False, False, 0)
        
        # Content based on desktop environment
        de = self.environment_detector.desktop_environment.value
        if de == 'xfce':
            self._create_xfce_ui(container)
        elif de == 'gnome':
            self._create_gnome_ui(container)
        elif de == 'plasma':
            self._create_plasma_ui(container)
        else:
            self._create_placeholder_ui(container)
    
    def _create_xfce_ui(self, container):
        """Create XFCE customization interface with Soplos tools."""
        # === SECTION 1: Soplos Tools ===
        soplos_label = Gtk.Label()
        soplos_label.set_markup(f"<span size='13000' weight='bold'>{_('Soplos Tools')}</span>")
        soplos_label.set_halign(Gtk.Align.START)
        soplos_label.set_margin_top(10)
        container.pack_start(soplos_label, False, False, 5)
        
        # FlowBox for Soplos tool buttons (2x2 grid)
        flowbox_soplos = Gtk.FlowBox()
        flowbox_soplos.set_valign(Gtk.Align.START)
        flowbox_soplos.set_max_children_per_line(2)
        flowbox_soplos.set_min_children_per_line(2)
        flowbox_soplos.set_selection_mode(Gtk.SelectionMode.NONE)
        flowbox_soplos.set_row_spacing(15)
        flowbox_soplos.set_column_spacing(15)
        flowbox_soplos.set_homogeneous(True)
        container.pack_start(flowbox_soplos, False, False, 5)
        
        # Soplos tools configuration
        soplos_tools = [
            {
                'icon': 'soplos-theme-manager.png',
                'label': _('Theme Manager'),
                'description': _('Customize GTK themes, icons, cursors and XFCE panel'),
                'tooltip': _('Launch Soplos Theme Manager'),
                'command': '/usr/bin/soplos-theme-manager'
            },
            {
                'icon': 'soplos-docklike.png',
                'label': _('Docklike'),
                'description': _('Configure dock and panel plugins'),
                'tooltip': _('Launch Soplos Docklike'),
                'command': '/usr/bin/soplos-docklike'
            },
            {
                'icon': 'soplos-grub-editor.png',
                'label': _('GRUB Editor'),
                'description': _('Edit boot menu (GRUB configuration)'),
                'tooltip': _('Launch Soplos GRUB Editor'),
                'command': '/usr/bin/soplos-grub-editor'
            },
            {
                'icon': 'soplos-plymouth-manager.png',
                'label': _('Plymouth Manager'),
                'description': _('Customize boot splash screen'),
                'tooltip': _('Launch Soplos Plymouth Manager'),
                'command': '/usr/bin/soplos-plymouth-manager'
            }
        ]
        
        # Create buttons for Soplos tools
        for tool in soplos_tools:
            button = self._create_tool_button(
                tool['icon'],
                tool['label'],
                tool['description'],
                tool['tooltip'],
                tool['command']
            )
            flowbox_soplos.add(button)
        
        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(15)
        separator.set_margin_bottom(15)
        container.pack_start(separator, False, False, 0)
        
        # === SECTION 2: XFCE Settings ===
        xfce_label = Gtk.Label()
        xfce_label.set_markup(f"<span size='13000' weight='bold'>{_('XFCE Settings')}</span>")
        xfce_label.set_halign(Gtk.Align.START)
        container.pack_start(xfce_label, False, False, 5)
        
        # FlowBox for XFCE settings (3 columns)
        flowbox_xfce = Gtk.FlowBox()
        flowbox_xfce.set_valign(Gtk.Align.START)
        flowbox_xfce.set_max_children_per_line(3)
        flowbox_xfce.set_min_children_per_line(2)
        flowbox_xfce.set_selection_mode(Gtk.SelectionMode.NONE)
        flowbox_xfce.set_row_spacing(15)
        flowbox_xfce.set_column_spacing(15)
        flowbox_xfce.set_homogeneous(True)
        container.pack_start(flowbox_xfce, True, True, 5)
        
        # XFCE native tools configuration
        xfce_tools = [
            {
                'icon_name': 'preferences-desktop-theme',
                'label': _('Appearance'),
                'description': _('Themes, icons, fonts'),
                'tooltip': _('XFCE Appearance Settings'),
                'command': '/usr/bin/xfce4-appearance-settings'
            },
            {
                'icon_name': 'preferences-desktop-wallpaper',
                'label': _('Desktop'),
                'description': _('Wallpapers and desktop'),
                'tooltip': _('XFCE Desktop Settings'),
                'command': '/usr/bin/xfdesktop-settings'
            },
            {
                'icon_name': 'preferences-system-windows',
                'label': _('Window Manager'),
                'description': _('Window decorations'),
                'tooltip': _('XFCE Window Manager Settings'),
                'command': '/usr/bin/xfwm4-settings'
            },
            {
                'icon_name': 'input-keyboard',
                'label': _('Keyboard'),
                'description': _('Keyboard and shortcuts'),
                'tooltip': _('XFCE Keyboard Settings'),
                'command': '/usr/bin/xfce4-keyboard-settings'
            },
            {
                'icon_name': 'input-mouse',
                'label': _('Mouse'),
                'description': _('Mouse and touchpad'),
                'tooltip': _('XFCE Mouse Settings'),
                'command': '/usr/bin/xfce4-mouse-settings'
            },
            {
                'icon_name': 'preferences-system-notifications',
                'label': _('Notifications'),
                'description': _('Notification settings'),
                'tooltip': _('XFCE Notification Settings'),
                'command': '/usr/bin/xfce4-notifyd-config'
            },
            {
                'icon_name': 'preferences-system',
                'label': _('Settings Editor'),
                'description': _('Advanced settings'),
                'tooltip': _('XFCE Settings Editor'),
                'command': '/usr/bin/xfce4-settings-editor'
            }
        ]
        
        # Create buttons for XFCE settings
        for tool in xfce_tools:
            button = self._create_xfce_button(
                tool['icon_name'],
                tool['label'],
                tool['description'],
                tool['tooltip'],
                tool['command']
            )
            flowbox_xfce.add(button)
    
    def _create_gnome_ui(self, container):
        """Create GNOME customization interface."""
        # === SECTION 1: Soplos Tools ===
        soplos_label = Gtk.Label()
        soplos_label.set_markup(f"<span size='13000' weight='bold'>{_('Soplos Tools')}</span>")
        soplos_label.set_halign(Gtk.Align.START)
        soplos_label.set_margin_top(10)
        container.pack_start(soplos_label, False, False, 5)
        
        # FlowBox for Soplos tools (2 columns)
        flowbox_soplos = Gtk.FlowBox()
        flowbox_soplos.set_valign(Gtk.Align.START)
        flowbox_soplos.set_max_children_per_line(2)
        flowbox_soplos.set_min_children_per_line(2)
        flowbox_soplos.set_selection_mode(Gtk.SelectionMode.NONE)
        flowbox_soplos.set_row_spacing(15)
        flowbox_soplos.set_column_spacing(15)
        flowbox_soplos.set_homogeneous(True)
        container.pack_start(flowbox_soplos, False, False, 5)
        
        # Universal Soplos tools (no Theme Manager, no Docklike)
        soplos_tools = [
            {
                'icon': 'soplos-grub-editor.png',
                'label': _('GRUB Editor'),
                'description': _('Edit boot menu (GRUB configuration)'),
                'tooltip': _('Launch Soplos GRUB Editor'),
                'command': '/usr/bin/soplos-grub-editor'
            },
            {
                'icon': 'soplos-plymouth-manager.png',
                'label': _('Plymouth Manager'),
                'description': _('Customize boot splash screen'),
                'tooltip': _('Launch Soplos Plymouth Manager'),
                'command': '/usr/bin/soplos-plymouth-manager'
            }
        ]
        
        for tool in soplos_tools:
            button = self._create_tool_button(
                tool['icon'], tool['label'], tool['description'],
                tool['tooltip'], tool['command']
            )
            flowbox_soplos.add(button)
        
        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(15)
        separator.set_margin_bottom(15)
        container.pack_start(separator, False, False, 0)
        
        # === SECTION 2: GNOME Settings ===
        gnome_label = Gtk.Label()
        gnome_label.set_markup(f"<span size='13000' weight='bold'>{_('GNOME Settings')}</span>")
        gnome_label.set_halign(Gtk.Align.START)
        container.pack_start(gnome_label, False, False, 5)
        
        # FlowBox for GNOME settings
        flowbox_gnome = Gtk.FlowBox()
        flowbox_gnome.set_valign(Gtk.Align.START)
        flowbox_gnome.set_max_children_per_line(3)
        flowbox_gnome.set_min_children_per_line(2)
        flowbox_gnome.set_selection_mode(Gtk.SelectionMode.NONE)
        flowbox_gnome.set_row_spacing(15)
        flowbox_gnome.set_column_spacing(15)
        flowbox_gnome.set_homogeneous(True)
        container.pack_start(flowbox_gnome, True, True, 5)
        
        # GNOME tools
        gnome_tools = [
            {
                'icon_name': 'gnome-control-center',
                'label': _('Settings'),
                'description': _('System settings'),
                'tooltip': _('GNOME Control Center'),
                'command': 'gnome-control-center'
            },
            {
                'icon_name': 'gnome-tweaks',
                'label': _('Tweaks'),
                'description': _('Advanced tweaks'),
                'tooltip': _('GNOME Tweaks'),
                'command': 'gnome-tweaks'
            },
            {
                'icon_name': 'org.gnome.Extensions',
                'label': _('Extensions'),
                'description': _('Manage extensions'),
                'tooltip': _('GNOME Extensions'),
                'command': 'gnome-extensions-app'
            },
            {
                'icon_name': 'dconf-editor',
                'label': _('dconf Editor'),
                'description': _('Advanced configuration'),
                'tooltip': _('dconf Editor'),
                'command': 'dconf-editor'
            }
        ]
        
        for tool in gnome_tools:
            button = self._create_xfce_button(
                tool['icon_name'], tool['label'], tool['description'],
                tool['tooltip'], tool['command']
            )
            flowbox_gnome.add(button)
    
    def _create_plasma_ui(self, container):
        """Create KDE Plasma customization interface."""
        # === SECTION 1: Soplos Tools ===
        soplos_label = Gtk.Label()
        soplos_label.set_markup(f"<span size='13000' weight='bold'>{_('Soplos Tools')}</span>")
        soplos_label.set_halign(Gtk.Align.START)
        soplos_label.set_margin_top(10)
        container.pack_start(soplos_label, False, False, 5)
        
        # FlowBox for Soplos tools (2 columns)
        flowbox_soplos = Gtk.FlowBox()
        flowbox_soplos.set_valign(Gtk.Align.START)
        flowbox_soplos.set_max_children_per_line(2)
        flowbox_soplos.set_min_children_per_line(2)
        flowbox_soplos.set_selection_mode(Gtk.SelectionMode.NONE)
        flowbox_soplos.set_row_spacing(15)
        flowbox_soplos.set_column_spacing(15)
        flowbox_soplos.set_homogeneous(True)
        container.pack_start(flowbox_soplos, False, False, 5)
        
        # Universal Soplos tools (no Theme Manager, no Docklike)
        soplos_tools = [
            {
                'icon': 'soplos-grub-editor.png',
                'label': _('GRUB Editor'),
                'description': _('Edit boot menu (GRUB configuration)'),
                'tooltip': _('Launch Soplos GRUB Editor'),
                'command': '/usr/bin/soplos-grub-editor'
            },
            {
                'icon': 'soplos-plymouth-manager.png',
                'label': _('Plymouth Manager'),
                'description': _('Customize boot splash screen'),
                'tooltip': _('Launch Soplos Plymouth Manager'),
                'command': '/usr/bin/soplos-plymouth-manager'
            }
        ]
        
        for tool in soplos_tools:
            button = self._create_tool_button(
                tool['icon'], tool['label'], tool['description'],
                tool['tooltip'], tool['command']
            )
            flowbox_soplos.add(button)
        
        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(15)
        separator.set_margin_bottom(15)
        container.pack_start(separator, False, False, 0)
        
        # === SECTION 2: KDE Settings ===
        kde_label = Gtk.Label()
        kde_label.set_markup(f"<span size='13000' weight='bold'>{_('KDE Settings')}</span>")
        kde_label.set_halign(Gtk.Align.START)
        container.pack_start(kde_label, False, False, 5)
        
        # FlowBox for KDE settings
        flowbox_kde = Gtk.FlowBox()
        flowbox_kde.set_valign(Gtk.Align.START)
        flowbox_kde.set_max_children_per_line(3)
        flowbox_kde.set_min_children_per_line(2)
        flowbox_kde.set_selection_mode(Gtk.SelectionMode.NONE)
        flowbox_kde.set_row_spacing(15)
        flowbox_kde.set_column_spacing(15)
        flowbox_kde.set_homogeneous(True)
        container.pack_start(flowbox_kde, True, True, 5)
        
        # KDE tools (using .desktop files like Tyson)
        kde_tools = [
            {
                'icon_name': 'preferences-desktop-theme-global',
                'label': _('Look and Feel'),
                'description': _('Themes and appearance'),
                'tooltip': _('KDE Look and Feel Settings'),
                'desktop_file': 'kcm_lookandfeel.desktop'
            },
            {
                'icon_name': 'preferences-system-login',
                'label': _('Login Screen'),
                'description': _('SDDM login manager'),
                'tooltip': _('KDE SDDM Settings'),
                'desktop_file': 'kcm_sddm.desktop'
            },
            {
                'icon_name': 'preferences-desktop-display',
                'label': _('Plymouth'),
                'description': _('Boot splash configuration'),
                'tooltip': _('KDE Plymouth Settings'),
                'desktop_file': 'kcm_plymouth.desktop'
            },
            {
                'icon_name': 'systemsettings',
                'label': _('System Settings'),
                'description': _('All system settings'),
                'tooltip': _('KDE System Settings'),
                'command': 'systemsettings'
            }
        ]
        
        for tool in kde_tools:
            if 'desktop_file' in tool:
                button = self._create_kde_button(
                    tool['icon_name'], tool['label'], tool['description'],
                    tool['tooltip'], tool['desktop_file']
                )
            else:
                button = self._create_xfce_button(
                    tool['icon_name'], tool['label'], tool['description'],
                    tool['tooltip'], tool['command']
                )
            flowbox_kde.add(button)
    
    
    def _create_tool_button(self, icon_filename, label_text, description_text, tooltip_text, command):
        """Create a button with icon, label and description for a customization tool."""
        # Container for the button content
        tool_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        tool_box.set_homogeneous(False)
        tool_box.set_margin_start(10)
        tool_box.set_margin_end(10)
        tool_box.set_margin_top(10)
        tool_box.set_margin_bottom(10)
        
        # Load icon
        icon_path = os.path.join(self.icons_path, icon_filename)
        try:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                filename=icon_path,
                width=64,
                height=64,
                preserve_aspect_ratio=True
            )
            icon = Gtk.Image.new_from_pixbuf(pixbuf)
            tool_box.pack_start(icon, False, False, 5)
        except Exception as e:
            print(f"Error loading icon {icon_path}: {e}")
            # Fallback to generic icon
            icon = Gtk.Image.new_from_icon_name("preferences-desktop", Gtk.IconSize.DIALOG)
            tool_box.pack_start(icon, False, False, 5)
        
        # Add title label (bold)
        title_label = Gtk.Label()
        title_label.set_markup(f"<b>{label_text}</b>")
        tool_box.pack_start(title_label, False, False, 0)
        
        # Add description label (dim, smaller, wrapped)
        desc_label = Gtk.Label(label=description_text)
        desc_label.set_line_wrap(True)
        desc_label.set_max_width_chars(30)
        desc_label.set_xalign(0.5)
        desc_label.get_style_context().add_class('dim-label')
        tool_box.pack_start(desc_label, False, False, 0)
        
        # Create button
        button = Gtk.Button()
        button.add(tool_box)
        button.set_tooltip_text(tooltip_text)
        button.connect('clicked', self._on_tool_clicked, command)
        
        return button
    
    def _create_xfce_button(self, icon_name, label_text, description_text, tooltip_text, command):
        """Create a button with system icon for XFCE settings."""
        # Container for the button content
        tool_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        tool_box.set_homogeneous(False)
        tool_box.set_margin_start(10)
        tool_box.set_margin_end(10)
        tool_box.set_margin_top(10)
        tool_box.set_margin_bottom(10)
        
        # Load system icon (smaller, 48px for XFCE tools)
        icon = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.DIALOG)
        tool_box.pack_start(icon, False, False, 5)
        
        # Add title label (bold)
        title_label = Gtk.Label()
        title_label.set_markup(f"<b>{label_text}</b>")
        tool_box.pack_start(title_label, False, False, 0)
        
        # Add description label (dim, smaller, wrapped)
        desc_label = Gtk.Label(label=description_text)
        desc_label.set_line_wrap(True)
        desc_label.set_max_width_chars(25)
        desc_label.set_xalign(0.5)
        desc_label.get_style_context().add_class('dim-label')
        tool_box.pack_start(desc_label, False, False, 0)
        
        # Create button
        button = Gtk.Button()
        button.add(tool_box)
        button.set_tooltip_text(tooltip_text)
        button.connect('clicked', self._on_tool_clicked, command)
        
        return button
    
    def _create_kde_button(self, icon_name, label_text, description_text, tooltip_text, desktop_file):
        """Create a button for KDE settings using .desktop files."""
        # Container for the button content
        tool_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        tool_box.set_homogeneous(False)
        tool_box.set_margin_start(10)
        tool_box.set_margin_end(10)
        tool_box.set_margin_top(10)
        tool_box.set_margin_bottom(10)
        
        # Load system icon
        icon = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.DIALOG)
        tool_box.pack_start(icon, False, False, 5)
        
        # Add title label (bold)
        title_label = Gtk.Label()
        title_label.set_markup(f"<b>{label_text}</b>")
        tool_box.pack_start(title_label, False, False, 0)
        
        # Add description label (dim, smaller, wrapped)
        desc_label = Gtk.Label(label=description_text)
        desc_label.set_line_wrap(True)
        desc_label.set_max_width_chars(25)
        desc_label.set_xalign(0.5)
        desc_label.get_style_context().add_class('dim-label')
        tool_box.pack_start(desc_label, False, False, 0)
        
        # Create button
        button = Gtk.Button()
        button.add(tool_box)
        button.set_tooltip_text(tooltip_text)
        button.connect('clicked', self._on_kde_desktop_clicked, desktop_file)
        
        return button
    
    def _on_kde_desktop_clicked(self, button, desktop_file):
        """Launch KDE application using .desktop file."""
        # Generate debounce flag
        flag_name = f"_kde_{desktop_file.replace('.', '_')}_running"
        
        # Debounce check
        if getattr(self, flag_name, False):
            return
        
        setattr(self, flag_name, True)
        
        # Launch using gtk-launch
        try:
            subprocess.Popen(['gtk-launch', desktop_file])
        except Exception as e:
            print(f"Error launching {desktop_file}: {e}")
        
        # Reset flag after 2 seconds
        GLib.timeout_add_seconds(2, lambda: setattr(self, flag_name, False) or False)
    
    
    def _create_placeholder_ui(self, container):
        """Create placeholder for non-XFCE environments."""
        content_area = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        
        # Info message
        info_label = Gtk.Label()
        de_name = self.environment_detector.desktop_environment.value.upper()
        info_label.set_markup(
            f"<span size='14000'>{_('Customization tools for')} {de_name} "
            f"{_('coming in future versions...')}</span>"
        )
        info_label.set_halign(Gtk.Align.CENTER)
        info_label.set_valign(Gtk.Align.CENTER)
        info_label.get_style_context().add_class('dim-label')
        info_label.set_line_wrap(True)
        
        content_area.pack_start(info_label, True, True, 0)
        
        # XFCE notice
        notice = Gtk.Label()
        notice.set_markup(
            f"<i>{_('Note: Soplos customization tools are currently available for XFCE.')}</i>"
        )
        notice.set_halign(Gtk.Align.CENTER)
        notice.get_style_context().add_class('dim-label')
        
        content_area.pack_start(notice, False, False, 0)
        
        container.pack_start(content_area, True, True, 0)
    
    def _on_tool_clicked(self, button, command):
        """Launch a Soplos customization tool with debounce."""
        # Generate debounce flag name from command
        tool_name = os.path.basename(command).replace('-', '_')
        flag_name = f"_{tool_name}_running"
        
        # Debounce check
        if getattr(self, flag_name, False):
            return
        
        # Set flag
        setattr(self, flag_name, True)
        
        # Launch tool
        try:
            if os.path.exists(command):
                subprocess.Popen([command])
            else:
                print(f"Tool not found: {command}")
        except Exception as e:
            print(f"Error launching {command}: {e}")
        
        # Reset flag after 2 seconds
        GLib.timeout_add_seconds(2, lambda: setattr(self, flag_name, False) or False)
