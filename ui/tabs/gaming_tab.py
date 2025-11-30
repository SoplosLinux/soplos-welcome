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
            ("GameMode", "Install Feral GameMode", "gamemode"),
            ("Performance Mode",  "Install CPU performance script", "cpu-performance"),
            ("Gaming Sysctl", "Apply kernel gaming tweaks", "preferences-system"),
            ("Optimize GPU", "Configure GPU drivers for gaming", "display"),
            ("Disk I/O", "Optimize disk schedulers", "drive-harddisk"),
            ("MangoHud", "Install FPS overlay + Goverlay", "utilities-system-monitor"),
            ("Revert All", "Undo all gaming optimizations", "edit-undo")
        ])
        
        # 2. Launchers Section
        # 2. Launchers Section
        self._create_section(content_box, "Launchers", [
            ("Steam", "Install Steam", "gaming/steam.png"),
            ("Lutris", "Install Lutris", "gaming/lutris.png"),
            ("Heroic", "Install Heroic Games Launcher", "gaming/heroic.png"),
            ("Bottles", "Install Bottles", "gaming/bottles.png"),
            ("Prism Launcher", "Minecraft Launcher with mod support", "gaming/prism.png"),
            ("Itch.io", "Indie games marketplace", "gaming/itch-io.png"),
            ("Minigalaxy", "Simple GOG client", "gaming/gog.png"),
            ("RetroArch", "All-in-one emulation frontend", "gaming/retroarch.png"),
            ("Discord", "Chat for gamers", "comunications/discord.png")
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
        import os
        icon = None
        
        if icon_name.endswith('.png'):
            try:
                icon_path = os.path.join(ICONS_DIR, icon_name)
                if os.path.exists(icon_path):
                    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(icon_path, 32, 32, True)
                    icon = Gtk.Image.new_from_pixbuf(pixbuf)
            except Exception as e:
                print(f"Error loading icon {icon_name}: {e}")
        
        if icon is None:
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
        
        # Router for different features
        if name == "GameMode":
            self._install_gamemode()
        elif name == "Performance Mode":
            self._install_performance_mode()
        elif name == "Gaming Sysctl":
            self._toggle_gaming_sysctl()
        elif name == "Optimize GPU":
            self._optimize_gpu()
        elif name == "Disk I/O":
            self._optimize_disk_io()
        elif name == "MangoHud":
            self._install_mangohud()
        elif name == "Revert All":
            self._revert_all_optimizations()
        else:
            # Placeholder for launchers and wallpapers
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
    
    # === OPTIMIZATION IMPLEMENTATIONS ===
    
    def _install_gamemode(self):
        """Install GameMode."""
        import subprocess
        import os
        
        dialog = Gtk.MessageDialog(
            transient_for=self.parent_window,
            flags=0,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text="Install GameMode?"
        )
        dialog.format_secondary_text(
            "GameMode optimizes system performance when running games.\n\n"
            "Packages to install:\n"
            "- gamemode\n"
            "- libgamemode0\n"
            "- libgamemode0:i386 (for 32-bit games)\n\n"
            "Continue?"
        )
        
        response = dialog.run()
        dialog.destroy()
        
        if response != Gtk.ResponseType.YES:
            return
        
        # Install via pkexec
        try:
            subprocess.run([
                "pkexec", "apt", "install", "-y",
                "gamemode", "libgamemode0", "libgamemode0:i386"
            ], check=True)
            
            # Show success
            success_dialog = Gtk.MessageDialog(
                transient_for=self.parent_window,
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text="GameMode installed successfully!"
            )
            success_dialog.format_secondary_text(
                "Usage:\n"
                "• Steam: Add 'gamemoderun %command%' to game launch options\n"
                "• Lutris: Enable 'Feral GameMode' in game settings"
            )
            success_dialog.run()
            success_dialog.destroy()
            
        except subprocess.CalledProcessError as e:
            error_dialog = Gtk.MessageDialog(
                transient_for=self.parent_window,
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text="Installation failed"
            )
            error_dialog.format_secondary_text(str(e))
            error_dialog.run()
            error_dialog.destroy()
    
    def _install_performance_mode(self):
        """Install Performance Mode script."""
        import subprocess
        import os
        from config.paths import BASE_DIR
        
        script_source = os.path.join(BASE_DIR, "services", "gaming", "game-performance.sh")
        script_dest = "/usr/local/bin/soplos-game-performance"
        
        dialog = Gtk.MessageDialog(
            transient_for=self.parent_window,
            flags=0,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text="Install Performance Mode Script?"
        )
        dialog.format_secondary_text(
            "This script temporarily sets CPU to 'performance' mode when launching games.\n\n"
            "Requirements:\n"
            "- power-profiles-daemon\n\n"
            "The script will be installed to /usr/local/bin/soplos-game-performance\n\n"
            "Continue?"
        )
        
        response = dialog.run()
        dialog.destroy()
        
        if response != Gtk.ResponseType.YES:
            return
        
        try:
            # Install power-profiles-daemon if not present
            subprocess.run([
                "pkexec", "apt", "install", "-y", "power-profiles-daemon"
            ], check=True)
            
            # Copy script
            subprocess.run([
                "pkexec", "cp", script_source, script_dest
            ], check=True)
            
            # Make executable
            subprocess.run([
                "pkexec", "chmod", "+x", script_dest
            ], check=True)
            
            # Show success
            success_dialog = Gtk.MessageDialog(
                transient_for=self.parent_window,
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text="Performance Mode script installed!"
            )
            success_dialog.format_secondary_text(
                "Usage:\n"
                "• Steam: Add 'soplos-game-performance %command%' to game launch options\n"
                "• Lutris: Add 'soplos-game-performance' as a prefix in Lutris settings\n\n"
                "Your CPU will automatically switch to performance mode when games are running."
            )
            success_dialog.run()
            success_dialog.destroy()
            
        except subprocess.CalledProcessError as e:
            error_dialog = Gtk.MessageDialog(
                transient_for=self.parent_window,
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text="Installation failed"
            )
            error_dialog.format_secondary_text(str(e))
            error_dialog.run()
            error_dialog.destroy()
    
    def _toggle_gaming_sysctl(self):
        """Apply or revert gaming sysctl tweaks."""
        import subprocess
        import os
        from config.paths import BASE_DIR
        
        sysctl_file = "/etc/sysctl.d/99-soplos-gaming.conf"
        sysctl_source = os.path.join(BASE_DIR, "services", "gaming", "sysctl-gaming.conf")
        
        # Check if already applied
        is_applied = os.path.exists(sysctl_file)
        
        if is_applied:
            # Revert
            dialog = Gtk.MessageDialog(
                transient_for=self.parent_window,
                flags=0,
                message_type=Gtk.MessageType.QUESTION,
                buttons=Gtk.ButtonsType.YES_NO,
                text="Revert Gaming Sysctl Tweaks?"
            )
            dialog.format_secondary_text("This will remove the gaming kernel optimizations.")
            
            response = dialog.run()
            dialog.destroy()
            
            if response != Gtk.ResponseType.YES:
                return
            
            try:
                subprocess.run(["pkexec", "rm", sysctl_file], check=True)
                subprocess.run(["pkexec", "sysctl", "--system"], check=True)
                
                success_dialog = Gtk.MessageDialog(
                    transient_for=self.parent_window,
                    flags=0,
                    message_type=Gtk.MessageType.INFO,
                    buttons=Gtk.ButtonsType.OK,
                    text="Gaming sysctl tweaks reverted!"
                )
                success_dialog.run()
                success_dialog.destroy()
                
            except subprocess.CalledProcessError as e:
                error_dialog = Gtk.MessageDialog(
                    transient_for=self.parent_window,
                    flags=0,
                    message_type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.OK,
                    text="Revert failed"
                )
                error_dialog.format_secondary_text(str(e))
                error_dialog.run()
                error_dialog.destroy()
        else:
            # Apply
            dialog = Gtk.MessageDialog(
                transient_for=self.parent_window,
                flags=0,
                message_type=Gtk.MessageType.QUESTION,
                buttons=Gtk.ButtonsType.YES_NO,
                text="Apply Gaming Sysctl Tweaks?"
            )
            dialog.format_secondary_text(
                "This will optimize kernel parameters for gaming:\n\n"
                "• vm.max_map_count = 2147483642 (essential for Proton/Steam)\n"
                "• vm.swappiness = 10 (prefer RAM over swap)\n"
                "• Network optimizations for online gaming\n"
                "• Reduced system latency\n\n"
                "⚠️  WARNING: Disables some security features (split_lock_mitigate)\n\n"
                "Continue?"
            )
            
            response = dialog.run()
            dialog.destroy()
            
            if response != Gtk.ResponseType.YES:
                return
            
            try:
                subprocess.run(["pkexec", "cp", sysctl_source, sysctl_file], check=True)
                subprocess.run(["pkexec", "sysctl", "--system"], check=True)
                
                success_dialog = Gtk.MessageDialog(
                    transient_for=self.parent_window,
                    flags=0,
                    message_type=Gtk.MessageType.INFO,
                    buttons=Gtk.ButtonsType.OK,
                    text="Gaming sysctl tweaks applied!"
                )
                success_dialog.format_secondary_text("Kernel parameters optimized for gaming.")
                success_dialog.run()
                success_dialog.destroy()
                
            except subprocess.CalledProcessError as e:
                error_dialog = Gtk.MessageDialog(
                    transient_for=self.parent_window,
                    flags=0,
                    message_type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.OK,
                    text="Apply failed"
                )
                error_dialog.format_secondary_text(str(e))
                error_dialog.run()
                error_dialog.destroy()
    
    def _optimize_gpu(self):
        """Optimize GPU drivers for gaming."""
        # This is a complex function, will be implemented in next iteration
        dialog = Gtk.MessageDialog(
            transient_for=self.parent_window,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="GPU Optimization"
        )
        dialog.format_secondary_text(
            "GPU optimization coming in next update!\n\n"
            "This will detect your GPU and apply:\n"
            "• AMD: RADV/Mesa optimizations\n"
            "• NVIDIA: Threading + shader cache\n"
            "• Intel: Mesa optimizations"
        )
        dialog.run()
        dialog.destroy()
    
    def _optimize_disk_io(self):
        """Optimize disk I/O schedulers."""
        # Similar to sysctl, will be implemented
        dialog = Gtk.MessageDialog(
            transient_for=self.parent_window,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="Disk I/O Optimization"
        )
        dialog.format_secondary_text(
            "Disk I/O optimization coming in next update!\n\n"
            "This will assign optimal schedulers:\n"
            "• HDD: BFQ (best latency)\n"
            "• SSD: mq-deadline\n"
            "• NVMe: none (maximum performance)"
        )
        dialog.run()
        dialog.destroy()
    
    def _install_mangohud(self):
        """Install MangoHud + Goverlay."""
        import subprocess
        
        dialog = Gtk.MessageDialog(
            transient_for=self.parent_window,
            flags=0,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text="Install MangoHud + Goverlay?"
        )
        dialog.format_secondary_text(
            "MangoHud provides an FPS and system monitoring overlay for games.\n"
            "Goverlay is a GUI configurator for MangoHud.\n\n"
            "Packages to install:\n"
            "- mangohud\n"
            "- mangohud:i386 (for 32-bit games)\n"
            "- goverlay\n\n"
            "Continue?"
        )
        
        response = dialog.run()
        dialog.destroy()
        
        if response != Gtk.ResponseType.YES:
            return
        
        try:
            subprocess.run([
                "pkexec", "apt", "install", "-y",
                "mangohud", "mangohud:i386", "goverlay"
            ], check=True)
            
            success_dialog = Gtk.MessageDialog(
                transient_for=self.parent_window,
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text="MangoHud + Goverlay installed!"
            )
            success_dialog.format_secondary_text(
                "Usage:\n"
                "• Steam: Add 'mangohud %command%' to game launch options\n"
                "• Configure via Goverlay application\n"
                "• Toggle in-game with Shift+F12"
            )
            success_dialog.run()
            success_dialog.destroy()
            
        except subprocess.CalledProcessError as e:
            error_dialog = Gtk.MessageDialog(
                transient_for=self.parent_window,
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text="Installation failed"
            )
            error_dialog.format_secondary_text(str(e))
            error_dialog.run()
            error_dialog.destroy()
    
    def _revert_all_optimizations(self):
        """Revert all gaming optimizations."""
        import subprocess
        import os
        
        dialog = Gtk.MessageDialog(
            transient_for=self.parent_window,
            flags=0,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.YES_NO,
            text="Revert ALL Gaming Optimizations?"
        )
        dialog.format_secondary_text(
            "This will remove:\n"
            "• Gaming sysctl tweaks\n"
            "• GPU optimizations (future)\n"
            "• Disk I/O optimizations (future)\n\n"
            "GameMode, MangoHud, and scripts will remain installed.\n\n"
            "Continue?"
        )
        
        response = dialog.run()
        dialog.destroy()
        
        if response != Gtk.ResponseType.YES:
            return
        
        try:
            # Remove sysctl if exists
            if os.path.exists("/etc/sysctl.d/99-soplos-gaming.conf"):
                subprocess.run(["pkexec", "rm", "/etc/sysctl.d/99-soplos-gaming.conf"], check=True)
                subprocess.run(["pkexec", "sysctl", "--system"], check=True)
            
            success_dialog = Gtk.MessageDialog(
                transient_for=self.parent_window,
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text="Optimizations reverted!"
            )
            success_dialog.format_secondary_text("All gaming tweaks have been removed.")
            success_dialog.run()
            success_dialog.destroy()
            
        except subprocess.CalledProcessError as e:
            error_dialog = Gtk.MessageDialog(
                transient_for=self.parent_window,
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text="Revert failed"
            )
            error_dialog.format_secondary_text(str(e))
            error_dialog.run()
            error_dialog.destroy()

