"""
Gaming tab implementation for Soplos Welcome.
Hidden easter egg tab with gaming optimizations and tools.
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Pango

from config.paths import ICONS_DIR
from utils.command_runner import CommandRunner
import subprocess
import os

class GamingTab(Gtk.Box):
    """Hidden gaming tab with optimizations and tools."""
    
    def __init__(self, i18n_manager, theme_manager, parent_window, progress_bar, progress_label):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        
        self.i18n_manager = i18n_manager
        self.theme_manager = theme_manager
        self.parent_window = parent_window
        self.progress_bar = progress_bar
        self.progress_label = progress_label
        
        # Create CommandRunner for launcher installations
        self.command_runner = CommandRunner(self.progress_bar, self.progress_label, self.parent_window)
        
        # Cache for launcher installation status
        self.launcher_status_cache = {}
        
        # RGB Theme state
        self.rgb_theme_active = False
        self.rgb_css_provider = None
        
        # Set margins
        self.set_margin_left(20)
        self.set_margin_right(20)
        self.set_margin_top(20)
        self.set_margin_bottom(20)
        
        # Create UI
        self._create_ui()
        self.show_all()
        
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
            ("GameMode", "Install Feral GameMode", "gaming/gamemode.png"),
            ("Performance Mode",  "Install CPU performance script", "gaming/performance.png"),
            ("Gaming Sysctl", "Apply kernel gaming tweaks", "preferences-system"),
            ("Optimize GPU", "Configure GPU drivers for gaming", "display"),
            ("Disk I/O", "Optimize disk schedulers", "drive-harddisk"),
            ("MangoHud", "Install FPS overlay + Goverlay", "utilities-system-monitor"),
            ("Revert All", "Undo all gaming optimizations", "edit-undo")
        ])
        
        # 2. Launchers Section (dynamic from config)
        self._create_launchers_section(content_box)
        
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
        elif name == "Gaming Wallpapers":
            self._install_gaming_wallpapers()
        elif name == "RGB Theme":
            self._toggle_rgb_theme()
        elif name == "Revert All":
            self._revert_all_optimizations()
        else:
            # Placeholder for other launchers
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
        import subprocess
        import os
        from config.paths import BASE_DIR
        
        # Detect GPU using lspci
        try:
            lspci_output = subprocess.check_output(['lspci'], universal_newlines=True)
        except subprocess.CalledProcessError:
            error_dialog = Gtk.MessageDialog(
                transient_for=self.parent_window,
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text="GPU Detection Failed"
            )
            error_dialog.format_secondary_text("Could not detect GPU. Please install 'pciutils' package.")
            error_dialog.run()
            error_dialog.destroy()
            return
        
        # Determine GPU vendor(s) - detect ALL GPUs for hybrid detection
        gpus = []
        
        for line in lspci_output.lower().split('\n'):
            if 'vga' in line or '3d' in line or 'display' in line:
                if 'nvidia' in line:
                    gpus.append(('nvidia', line.split(':')[-1].strip().title()))
                elif 'amd' in line or 'ati' in line or 'radeon' in line:
                    gpus.append(('amd', line.split(':')[-1].strip().title()))
                elif 'intel' in line:
                    gpus.append(('intel', line.split(':')[-1].strip().title()))
        
        if not gpus:
            error_dialog = Gtk.MessageDialog(
                transient_for=self.parent_window,
                flags=0,
                message_type=Gtk.MessageType.WARNING,
                buttons=Gtk.ButtonsType.OK,
                text="Unsupported GPU"
            )
            error_dialog.format_secondary_text(
                "Could not detect a supported GPU (NVIDIA, AMD, or Intel).\\n\\n"
                "GPU optimizations are only available for these vendors."
            )
            error_dialog.run()
            error_dialog.destroy()
            return
        
        # Check if hybrid graphics (multiple GPUs)
        is_hybrid = len(gpus) > 1
        has_nvidia = any(vendor == 'nvidia' for vendor, _ in gpus)
        
        # Determine primary GPU (NVIDIA > AMD > Intel)
        gpu_vendor = None
        gpu_model = "Unknown"
        
        for vendor, model in gpus:
            if vendor == 'nvidia':
                gpu_vendor = 'nvidia'
                gpu_model = model
                break
        
        if not gpu_vendor:
            for vendor, model in gpus:
                if vendor == 'amd':
                    gpu_vendor = 'amd'
                    gpu_model = model
                    break
        
        if not gpu_vendor:
            gpu_vendor, gpu_model = gpus[0]
        
        # Confirm with user
        optimizations_text = {
            'nvidia': (
                "• Shader disk cache enabled\\n"
                "• Threaded optimization enabled\\n"
                "• VSync disabled (lower input lag)\\n"
                "• NVAPI enabled for Proton"
            ),
            'amd': (
                "• GPL shader pipeline enabled\\n"
                "• RADV driver forced\\n"
                "• OpenGL threading enabled\\n"
                "• Radeonsi driver optimization"
            ),
            'intel': (
                "• OpenGL threading enabled\\n"
                "• Iris driver optimization (Gen9+)"
            )
        }
        
        dialog = Gtk.MessageDialog(
            transient_for=self.parent_window,
            flags=0,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text=f"Optimize {gpu_vendor.upper()} GPU for Gaming?"
        )
        dialog.format_secondary_text(
            f"Detected GPU: {gpu_model}\\n\\n"
            f"Optimizations to apply:\\n{optimizations_text[gpu_vendor]}\\n\\n"
            "These settings will be applied system-wide via environment variables.\\n\\n"
            "Continue?"
        )
        
        response = dialog.run()
        dialog.destroy()
        
        if response != Gtk.ResponseType.YES:
            return
        
        # Copy appropriate config file
        source_file = os.path.join(BASE_DIR, "services", "gaming", f"{gpu_vendor}-env.conf")
        dest_file = f"/etc/environment.d/50-soplos-{gpu_vendor}-gaming.conf"
        
        try:
            # Copy config file
            subprocess.run([
                "pkexec", "cp", source_file, dest_file
            ], check=True)
            
            # Install prime-run if hybrid NVIDIA system
            prime_run_installed = False
            if is_hybrid and has_nvidia:
                try:
                    prime_run_source = os.path.join(BASE_DIR, "services", "gaming", "prime-run")
                    prime_run_dest = "/usr/local/bin/prime-run"
                    
                    # Copy prime-run script
                    subprocess.run([
                        "pkexec", "cp", prime_run_source, prime_run_dest
                    ], check=True)
                    
                    # Make executable
                    subprocess.run([
                        "pkexec", "chmod", "+x", prime_run_dest
                    ], check=True)
                    
                    prime_run_installed = True
                except subprocess.CalledProcessError:
                    # Non-critical error, continue
                    pass
            
            # Build success message
            if is_hybrid and has_nvidia:
                # Hybrid graphics message
                integrated_gpu = next((m for v, m in gpus if v in ['intel', 'amd']), "Unknown")
                
                success_msg = (
                    f"✅ Hybrid Graphics Optimized!\\n\\n"
                    f"GPU Dedicada: {gpu_model}\\n"
                    f"GPU Integrada: {integrated_gpu}\\n\\n"
                )
                
                if prime_run_installed:
                    success_msg += (
                        f"✅ prime-run script installed to /usr/local/bin/prime-run\\n\\n"
                        f"Usage for hybrid graphics:\\n"
                        f"• Steam: Add 'prime-run %command%' to game launch options\\n"
                        f"• Lutris: Add 'prime-run' as a prefix\\n"
                        f"• Terminal: prime-run <application>\\n\\n"
                        f"This forces games to use your NVIDIA GPU.\\n\\n"
                    )
                
                success_msg += (
                    f"⚠️  IMPORTANT: You must LOG OUT and log back in for changes to take effect.\\n\\n"
                    f"Configuration saved to: {dest_file}"
                )
            else:
                # Single GPU message
                success_msg = (
                    f"Gaming optimizations applied for {gpu_model}.\\n\\n"
                    f"⚠️  IMPORTANT: You must LOG OUT and log back in for changes to take effect.\\n\\n"
                    f"Configuration saved to:\\n{dest_file}"
                )
            
            # Show success
            success_dialog = Gtk.MessageDialog(
                transient_for=self.parent_window,
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text=f"{gpu_vendor.upper()} GPU Optimized!"
            )
            success_dialog.format_secondary_text(success_msg)
            success_dialog.run()
            success_dialog.destroy()
            
        except subprocess.CalledProcessError as e:
            error_dialog = Gtk.MessageDialog(
                transient_for=self.parent_window,
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text="Optimization Failed"
            )
            error_dialog.format_secondary_text(str(e))
            error_dialog.run()
            error_dialog.destroy()

    
    def _optimize_disk_io(self):
        """Optimize disk I/O schedulers."""
        import subprocess
        import os
        from config.paths import BASE_DIR
        
        source_file = os.path.join(BASE_DIR, "services", "gaming", "ioschedulers.rules")
        dest_file = "/etc/udev/rules.d/60-soplos-ioschedulers.rules"
        
        # Check if already applied
        is_applied = os.path.exists(dest_file)
        
        if is_applied:
            # Revert
            dialog = Gtk.MessageDialog(
                transient_for=self.parent_window,
                flags=0,
                message_type=Gtk.MessageType.QUESTION,
                buttons=Gtk.ButtonsType.YES_NO,
                text="Revert Disk I/O Optimizations?"
            )
            dialog.format_secondary_text("This will remove the custom I/O scheduler rules.")
            
            response = dialog.run()
            dialog.destroy()
            
            if response != Gtk.ResponseType.YES:
                return
            
            try:
                subprocess.run(["pkexec", "rm", dest_file], check=True)
                subprocess.run(["pkexec", "udevadm", "control", "--reload-rules"], check=True)
                subprocess.run(["pkexec", "udevadm", "trigger"], check=True)
                
                success_dialog = Gtk.MessageDialog(
                    transient_for=self.parent_window,
                    flags=0,
                    message_type=Gtk.MessageType.INFO,
                    buttons=Gtk.ButtonsType.OK,
                    text="Disk I/O optimizations reverted!"
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
                text="Optimize Disk I/O Schedulers?"
            )
            dialog.format_secondary_text(
                "This will configure optimal I/O schedulers for gaming:\\n\\n"
                "• HDD: BFQ scheduler (best latency)\\n"
                "• SSD (SATA): mq-deadline\\n"
                "• NVMe: none (maximum performance)\\n\\n"
                "Changes take effect immediately without reboot.\\n\\n"
                "Continue?"
            )
            
            response = dialog.run()
            dialog.destroy()
            
            if response != Gtk.ResponseType.YES:
                return
            
            try:
                # Copy udev rules
                subprocess.run(["pkexec", "cp", source_file, dest_file], check=True)
                
                # Reload udev rules
                subprocess.run(["pkexec", "udevadm", "control", "--reload-rules"], check=True)
                
                # Trigger udev to apply rules
                subprocess.run(["pkexec", "udevadm", "trigger"], check=True)
                
                success_dialog = Gtk.MessageDialog(
                    transient_for=self.parent_window,
                    flags=0,
                    message_type=Gtk.MessageType.INFO,
                    buttons=Gtk.ButtonsType.OK,
                    text="Disk I/O Optimized!"
                )
                success_dialog.format_secondary_text(
                    "I/O schedulers have been optimized for gaming.\\n\\n"
                    "Changes are active immediately.\\n\\n"
                    f"Configuration saved to:\\n{dest_file}"
                )
                success_dialog.run()
                success_dialog.destroy()
                
            except subprocess.CalledProcessError as e:
                error_dialog = Gtk.MessageDialog(
                    transient_for=self.parent_window,
                    flags=0,
                    message_type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.OK,
                    text="Optimization failed"
                )
                error_dialog.format_secondary_text(str(e))
                error_dialog.run()
                error_dialog.destroy()
    
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
    
    def _install_gaming_wallpapers(self):
        """Install gaming wallpapers to the appropriate directory based on DE."""
        import subprocess
        import os
        import tempfile
        import shutil
        from config.paths import BASE_DIR
        
        # Detect current DE
        session = os.environ.get('XDG_CURRENT_DESKTOP', '').lower()
        
        # Determine destination directory based on DE
        is_gnome = False
        if 'kde' in session or 'plasma' in session:
            dest_dir = "/usr/share/wallpapers/soplos"
            de_name = "KDE Plasma"
        elif 'xfce' in session:
            dest_dir = "/usr/share/backgrounds/soplos"
            de_name = "XFCE"
        elif 'gnome' in session:
            # GNOME uses backgrounds
            dest_dir = "/usr/share/backgrounds/soplos"
            de_name = "GNOME"
            is_gnome = True
        else:
            # Default to backgrounds for unknown DEs
            dest_dir = "/usr/share/backgrounds/soplos"
            de_name = "your desktop environment"
        
        # Confirmation dialog
        dialog = Gtk.MessageDialog(
            transient_for=self.parent_window,
            flags=0,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text="Install Gaming Wallpapers?"
        )
        dialog.format_secondary_text(
            f"This will install exclusive gaming wallpapers for {de_name}.\\n\\n"
            f"Destination: {dest_dir}\\n\\n"
            "Continue?"
        )
        
        response = dialog.run()
        dialog.destroy()
        
        if response != Gtk.ResponseType.YES:
            return
        
        try:
            # Path to compressed wallpapers
            wallpapers_archive = os.path.join(BASE_DIR, "assets", "wallpapers", "wallpapers.tar.xz")
            
            if not os.path.exists(wallpapers_archive):
                raise FileNotFoundError(f"Wallpapers archive not found: {wallpapers_archive}")
            
            # Create temporary directory for extraction
            with tempfile.TemporaryDirectory() as temp_dir:
                # Extract archive
                subprocess.run([
                    "tar", "-xf", wallpapers_archive, "-C", temp_dir
                ], check=True)
                
                # Copy wallpapers to destination (with pkexec for system directory)
                # Find extracted wallpapers
                extracted_files = []
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                            extracted_files.append(os.path.join(root, file))
                
                if not extracted_files:
                    raise FileNotFoundError("No wallpaper files found in archive")
                
                # Copy each file with pkexec
                installed_filenames = []
                for wallpaper in extracted_files:
                    filename = os.path.basename(wallpaper)
                    subprocess.run([
                        "pkexec", "cp", wallpaper, dest_dir
                    ], check=True)
                    installed_filenames.append(filename)
                
                # Generate GNOME XML if needed
                if is_gnome:
                    self._generate_gnome_wallpaper_xml(installed_filenames, dest_dir, temp_dir)
            
            # Success dialog
            success_dialog = Gtk.MessageDialog(
                transient_for=self.parent_window,
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text="Gaming wallpapers installed successfully!"
            )
            success_dialog.format_secondary_text(
                f"Wallpapers have been installed to:\\n{dest_dir}\\n\\n"
                f"You can now select them from your {de_name} wallpaper settings."
            )
            success_dialog.run()
            success_dialog.destroy()
            
        except FileNotFoundError as e:
            error_dialog = Gtk.MessageDialog(
                transient_for=self.parent_window,
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text="Archive not found"
            )
            error_dialog.format_secondary_text(str(e))
            error_dialog.run()
            error_dialog.destroy()
            
        except subprocess.CalledProcessError as e:
            error_dialog = Gtk.MessageDialog(
                transient_for=self.parent_window,
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text="Installation failed"
            )
            error_dialog.format_secondary_text(
                f"Failed to install wallpapers: {str(e)}\\n\\n"
                "Make sure you have proper permissions."
            )
            error_dialog.run()
            error_dialog.destroy()
            
        except Exception as e:
            error_dialog = Gtk.MessageDialog(
                transient_for=self.parent_window,
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text="Unexpected error"
            )
            error_dialog.format_secondary_text(str(e))
            error_dialog.run()
            error_dialog.destroy()
    
    def _generate_gnome_wallpaper_xml(self, filenames, dest_dir, temp_dir):
        """Generate GNOME wallpaper XML file based on installed files."""
        import subprocess
        import os
        
        # Sort files by name for consistent ordering
        filenames.sort()
        
        # Generate XML content
        xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml_content += '<!DOCTYPE wallpapers SYSTEM "gnome-wp-list.dtd">\n'
        xml_content += '<wallpapers>\n'
        
        for filename in filenames:
            # Remove extension for the name
            name_without_ext = os.path.splitext(filename)[0]
            
            xml_content += '  <wallpaper deleted="false">\n'
            xml_content += f'    <name>Soplos Gaming {name_without_ext}</name>\n'
            xml_content += f'    <filename>{dest_dir}/{filename}</filename>\n'
            xml_content += '    <options>zoom</options>\n'
            xml_content += '  </wallpaper>\n'
        
        xml_content += '</wallpapers>\n'
        
        # Write XML to temp file
        temp_xml = os.path.join(temp_dir, "soplos-gaming-wallpapers.xml")
        with open(temp_xml, 'w') as f:
            f.write(xml_content)
        
        # Copy XML to system directory with pkexec
        xml_dest = "/usr/share/gnome-background-properties/soplos-gaming-wallpapers.xml"
        subprocess.run([
            "pkexec", "cp", temp_xml, xml_dest
        ], check=True)

    def _create_launchers_section(self, parent):
        """Create launchers section with install buttons and badges."""
        # Define launchers locally (NOT from config/software.py to avoid duplicates in recommended tab)
        launchers = [
            {
                'name': 'Steam',
                'package': None,
                'flatpak': 'com.valvesoftware.Steam',
                'icon': 'steam.png',
                'description': 'Plataforma de distribución digital de videojuegos',
                'official': False
            },
            {
                'name': 'Lutris',
                'package': 'lutris',
                'flatpak': 'net.lutris.Lutris',
                'icon': 'lutris.png',
                'description': 'Plataforma unificada para gestionar juegos en Linux',
                'official': True
            },
            {
                'name': 'Heroic Games Launcher',
                'package': None,
                'flatpak': 'com.heroicgameslauncher.hgl',
                'icon': 'heroic.png',
                'description': 'Launcher para juegos de Epic, GOG y Amazon Games',
                'official': False
            },
            {
                'name': 'Bottles',
                'package': None,
                'flatpak': 'com.usebottles.bottles',
                'icon': 'bottles.png',
                'description': 'Ejecuta aplicaciones Windows en Linux usando Wine',
                'official': False
            },
            {
                'name': 'Prism Launcher',
                'package': None,
                'flatpak': 'org.prismlauncher.PrismLauncher',
                'icon': 'prism.png',
                'description': 'Launcher personalizado para Minecraft',
                'official': False
            },
            {
                'name': 'Itch.io',
                'package': None,
                'flatpak': 'io.itch.itch',
                'icon': 'itch-io.png',
                'description': 'Plataforma de distribución de juegos indie',
                'official': False
            },
            {
                'name': 'Minigalaxy',
                'package': 'minigalaxy',
                'flatpak': 'io.github.sharkwouter.Minigalaxy',
                'icon': 'gog.png',
                'description': 'Cliente simple para GOG.com',
                'official': True
            },
            {
                'name': 'RetroArch',
                'package': 'retroarch',
                'flatpak': 'org.libretro.RetroArch',
                'icon': 'retroarch.png',
                'description': 'Frontend para emuladores y motores de juegos',
                'official': True
            },
            {
                'name': 'Discord',
                'package': None,
                'flatpak': 'com.discordapp.Discord',
                'icon': 'discord.png',
                'description': 'Plataforma de comunicación para comunidades gaming',
                'official': False
            }
        ]
        
        if not launchers:
            return
        
        # Section Frame
        section_frame = Gtk.Frame()
        section_frame.set_label_align(0.02, 0.5)
        section_frame.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        parent.pack_start(section_frame, False, False, 0)
        
        # Section title
        title = Gtk.Label()
        title.set_markup('<span size="large" weight="bold">Launchers</span>')
        section_frame.set_label_widget(title)
        
        # Grid for launchers
        grid = Gtk.Grid()
        grid.set_row_spacing(10)
        grid.set_column_spacing(15)
        grid.set_margin_left(20)
        grid.set_margin_right(20)
        grid.set_margin_top(15)
        grid.set_margin_bottom(15)
        grid.set_column_homogeneous(True)
        
        # Add launcher widgets (2 columns)
        row = 0
        col = 0
        max_cols = 2
        
        for launcher in launchers:
            launcher_widget = self._create_launcher_widget(launcher)
            grid.attach(launcher_widget, col, row, 1, 1)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        section_frame.add(grid)
    
    def _create_launcher_widget(self, launcher):
        """Create a widget for a single launcher with badges."""
        # Main container
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        box.set_margin_top(8)
        box.set_margin_bottom(8)
        
        # Icon
        icon = self._load_launcher_icon(launcher.get('icon', ''))
        if icon:
            box.pack_start(icon, False, False, 0)
        
        # Info box
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        
        # Name + Badges
        name_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        
        name_label = Gtk.Label()
        name_text = f"<b>{launcher['name']}</b>"
        name_label.set_markup(name_text)
        name_label.set_halign(Gtk.Align.START)
        name_box.pack_start(name_label, False, False, 0)
        
        # Add Flatpak badge ONLY when using flatpak (same style as recommended tab)
        install_method = self._get_install_method(launcher)
        if install_method == 'flatpak':
            flatpak_badge = Gtk.Label()
            flatpak_badge.set_markup('<span size="small" foreground="#888888" background="#333333"> Flatpak </span>')
            flatpak_badge.set_valign(Gtk.Align.CENTER)
            name_box.pack_start(flatpak_badge, False, False, 0)
        
        # Official badge
        if launcher.get('official', False):
            official_badge = Gtk.Image.new_from_icon_name("security-high-symbolic", Gtk.IconSize.MENU)
            official_badge.get_style_context().add_class('success-color')
            official_badge.set_tooltip_text("Official Package")
            name_box.pack_start(official_badge, False, False, 0)
        
        info_box.pack_start(name_box, False, False, 0)
        
        # Description
        desc_label = Gtk.Label(launcher.get('description', ''))
        desc_label.set_halign(Gtk.Align.START)
        desc_label.set_line_wrap(True)
        desc_label.set_max_width_chars(45)
        desc_label.set_lines(2)
        desc_label.set_ellipsize(Pango.EllipsizeMode.END)
        desc_label.set_size_request(-1, 40)
        desc_label.get_style_context().add_class('dim-label')
        info_box.pack_start(desc_label, False, False, 0)
        
        box.pack_start(info_box, True, True, 0)
        
        # Button
        button_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        button_box.set_valign(Gtk.Align.CENTER)
        
        if self._is_launcher_installed(launcher):
            button = Gtk.Button.new_with_label("Desinstalar")
            button.get_style_context().add_class('destructive-action')
            button.set_size_request(110, -1)
            button.connect('clicked', self._on_uninstall_launcher, launcher)
        else:
            button = Gtk.Button.new_with_label("Instalar")
            button.get_style_context().add_class('suggested-action')
            button.set_size_request(110, -1)
            button.connect('clicked', self._on_install_launcher, launcher)
        
        button_box.pack_start(button, False, False, 0)
        box.pack_start(button_box, False, False, 0)
        
        return box
    
    def _load_launcher_icon(self, icon_name):
        """Load launcher icon."""
        if not icon_name:
            return None
        
        try:
            # Discord icon is in comunications folder
            if icon_name == 'discord.png':
                icon_path = os.path.join(ICONS_DIR, 'comunications', icon_name)
            else:
                icon_path = os.path.join(ICONS_DIR, 'gaming', icon_name)
            
            if os.path.exists(icon_path):
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    icon_path, 48, 48, True
                )
                return Gtk.Image.new_from_pixbuf(pixbuf)
        except Exception as e:
            print(f"Error loading launcher icon {icon_name}: {e}")
        
        return None
    
    def _get_install_method(self, launcher):
        """Get preferred install method for launcher."""
        # Prefer Flatpak for certain launchers (like recommended tab)
        prefer_flatpak = ['Steam', 'Heroic Games Launcher', 'Bottles', 'Discord', 
                         'Prism Launcher', 'Itch.io']
        
        if launcher['name'] in prefer_flatpak and launcher.get('flatpak'):
            return 'flatpak'
        
        # APT first if available
        if launcher.get('package'):
            return 'apt'
        elif launcher.get('flatpak'):
            return 'flatpak'
        
        return 'unknown'
    
    def _is_launcher_installed(self, launcher):
        """Check if launcher is installed."""
        name = launcher['name']
        
        # Check cache
        if name in self.launcher_status_cache:
            return self.launcher_status_cache[name]
        
        method = self._get_install_method(launcher)
        is_installed = False
        
        try:
            if method == 'apt' and launcher.get('package'):
                result = subprocess.run(
                    ['dpkg', '-s', launcher['package']],
                    capture_output=True, text=True
                )
                is_installed = 'Status: install ok installed' in result.stdout
            elif method == 'flatpak' and launcher.get('flatpak'):
                result = subprocess.run(
                    ['flatpak', 'info', launcher['flatpak']],
                    capture_output=True, text=True
                )
                is_installed = result.returncode == 0
        except:
            pass
        
        self.launcher_status_cache[name] = is_installed
        return is_installed
    
    def _on_install_launcher(self, button, launcher):
        """Install launcher."""
        method = self._get_install_method(launcher)
        command = ""
        script_name = ""
        
        if method == 'apt' and launcher.get('package'):
            command = f"pkexec apt install -y {launcher['package']}"
            script_name = f"install-{launcher['package']}.sh"
        elif method == 'flatpak' and launcher.get('flatpak'):
            command = f"flatpak install -y flathub {launcher['flatpak']}"
            script_name = f"install-{launcher['flatpak'].replace('.', '-')}.sh"
        
        if command:
            self._run_launcher_script(command, script_name, launcher)
    
    def _on_uninstall_launcher(self, button, launcher):
        """Uninstall launcher."""
        method = self._get_install_method(launcher)
        command = ""
        script_name = ""
        
        if method == 'apt' and launcher.get('package'):
            command = f"pkexec apt remove -y {launcher['package']}"
            script_name = f"uninstall-{launcher['package']}.sh"
        elif method == 'flatpak' and launcher.get('flatpak'):
            command = f"flatpak uninstall -y {launcher['flatpak']}"
            script_name = f"uninstall-{launcher['flatpak'].replace('.', '-')}.sh"
        
        if command:
            self._run_launcher_script(command, script_name, launcher)
    
    def _run_launcher_script(self, command, script_name, launcher):
        """Create and run installation script."""
        script_path = f"/tmp/{script_name}"
        try:
            with open(script_path, "w") as f:
                f.write("#!/bin/bash\n")
                f.write("set -e\n")
                f.write(command + "\n")
                f.write("echo 'Operation completed successfully'\n")
            os.chmod(script_path, 0o755)
            
            # Run and refresh on complete
            self.command_runner.run_command(
                script_path,
                lambda: self._on_launcher_operation_complete(launcher)
            )
        except Exception as e:
            print(f"Error running launcher script: {e}")
    
    def _on_launcher_operation_complete(self, launcher):
        """Handle launcher operation completion."""
        # Clear cache
        if launcher['name'] in self.launcher_status_cache:
            del self.launcher_status_cache[launcher['name']]
        
        # Recreate the launchers section (refresh UI)
        print(f"Launcher operation completed for {launcher['name']}")
        # Note: Full UI refresh would require rebuilding the entire content_box
        # For now, cache invalidation ensures next check is accurate
    
    def _toggle_rgb_theme(self):
        """Toggle RGB Gaming theme (black with red neon accents)."""
        from gi.repository import Gdk
        
        if self.rgb_theme_active:
            # Deactivate RGB theme
            if self.rgb_css_provider:
                screen = Gdk.Screen.get_default()
                Gtk.StyleContext.remove_provider_for_screen(
                    screen,
                    self.rgb_css_provider
                )
                self.rgb_css_provider = None
            
            self.rgb_theme_active = False
            
            # Show confirmation
            dialog = Gtk.MessageDialog(
                transient_for=self.parent_window,
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text="RGB Theme Deactivated"
            )
            dialog.format_secondary_text("The RGB gaming theme has been disabled.")
            dialog.run()
            dialog.destroy()
        else:
            # Activate RGB theme
            try:
                # Load gaming RGB CSS
                rgb_css_path = os.path.join(
                    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                    'assets', 'themes', 'gaming-rgb.css'
                )
                
                if not os.path.exists(rgb_css_path):
                    dialog = Gtk.MessageDialog(
                        transient_for=self.parent_window,
                        flags=0,
                        message_type=Gtk.MessageType.ERROR,
                        buttons=Gtk.ButtonsType.OK,
                        text="Error"
                    )
                    dialog.format_secondary_text(f"RGB theme file not found:\n{rgb_css_path}")
                    dialog.run()
                    dialog.destroy()
                    return
                
                # Create and apply CSS provider
                self.rgb_css_provider = Gtk.CssProvider()
                self.rgb_css_provider.load_from_path(rgb_css_path)
                
                screen = Gdk.Screen.get_default()
                Gtk.StyleContext.add_provider_for_screen(
                    screen,
                    self.rgb_css_provider,
                    Gtk.STYLE_PROVIDER_PRIORITY_USER  # High priority to override
                )
                
                self.rgb_theme_active = True
                
                # Show confirmation
                dialog = Gtk.MessageDialog(
                    transient_for=self.parent_window,
                    flags=0,
                    message_type=Gtk.MessageType.INFO,
                    buttons=Gtk.ButtonsType.OK,
                    text="RGB Theme Activated! 🎮"
                )
                dialog.format_secondary_text(
                    "Gaming RGB theme applied!\n\n"
                    "• Black background with red neon accents\n"
                    "• Click 'RGB Theme' again to deactivate"
                )
                dialog.run()
                dialog.destroy()
                
            except Exception as e:
                dialog = Gtk.MessageDialog(
                    transient_for=self.parent_window,
                    flags=0,
                    message_type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.OK,
                    text="Error Activating RGB Theme"
                )
                dialog.format_secondary_text(f"Failed to load RGB theme:\n{str(e)}")
                dialog.run()
                dialog.destroy()
