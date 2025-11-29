import subprocess
import threading
import time
import re
import os
from gi.repository import GLib
from core.i18n_manager import _

class CommandRunner:
    def __init__(self, progress_bar=None, status_label=None, parent_window=None):
        self.progress_bar = progress_bar
        self.status_label = status_label
        self.parent_window = parent_window  # Add reference to parent window
        self.current_process = None
        self.command_running = False
    
    def run_command(self, command, on_complete=None):
        """
        Runs a command with optional callback on completion
        """
        if self.command_running:
            return
            
        self.command_running = True
        
        def execute_command():
            try:
                # Determine the type of installer/command
                is_flatpak = 'flatpak' in command
                is_apt = 'apt' in command
                is_wget = 'wget' in command
                is_unzip = 'unzip' in command
                is_dpkg = 'dpkg' in command
                
                total_packages = 0
                current_package = 0
                
                process = subprocess.Popen(
                    command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                    bufsize=1
                )
                
                self.current_process = process
                
                # Update the progress bar at the start
                if self.parent_window and hasattr(self.parent_window, 'show_progress'):
                    GLib.idle_add(self.parent_window.show_progress, _("Starting..."), 0.0)
                elif self.progress_bar:
                    GLib.idle_add(self.progress_bar.set_fraction, 0.0)

                for line in iter(process.stdout.readline, ''):
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Update status label/progress message
                    if self.parent_window and hasattr(self.parent_window, 'show_progress'):
                        # We update the message but keep current fraction until calculated
                        pass 
                    elif self.status_label:
                        GLib.idle_add(self.status_label.set_text, line)
                    
                    progress = None
                    
                    # Detect progress depending on command type
                    if is_wget:
                        # Parse wget progress format
                        if '%' in line:
                            try:
                                percent = int(line[line.find(' ')+1:line.find('%')])
                                progress = percent / 100.0
                            except:
                                pass
                    
                    elif is_unzip:
                        # Estimate progress based on extracted files
                        if 'extracting:' in line.lower():
                            progress = 0.5  # Halfway through
                        elif 'inflating:' in line.lower():
                            progress = 0.75  # 75% done
                    
                    elif is_dpkg:
                        # Progress for .deb installation
                        if 'Preparing' in line:
                            progress = 0.2
                        elif 'Unpacking' in line:
                            progress = 0.5
                        elif 'Setting up' in line:
                            progress = 0.8
                    
                    elif is_apt:
                        # Support for English and Spanish (and potentially others via generic keywords)
                        # 'Get:' (En), 'Des:' (Es), 'Obt:' (Es var), 'Atin:' (Fr), 'Holen:' (De)
                        if 'Get:' in line or 'Des:' in line or 'Obt:' in line or 'Holen:' in line:
                            if total_packages == 0:
                                # Try to estimate total packages from Get lines or previous output
                                # This is a heuristic
                                if 'upgraded,' in line or 'actualizados,' in line:
                                    try:
                                        parts = line.split(',')
                                        upgraded = int([s for s in parts[0].split() if s.isdigit()][0])
                                        new_install = int([s for s in parts[1].split() if s.isdigit()][0])
                                        total_packages = upgraded + new_install
                                    except:
                                        pass
                                if total_packages == 0:
                                     total_packages = line.count('Get:') + line.count('Des:') # Fallback
                                     
                            current_package += 1
                            progress = min(current_package / max(total_packages, 1), 0.5)
                            
                        # 'Unpacking' (En), 'Desempaquetando' (Es), 'Dépaquetage' (Fr), 'Entpacken' (De)
                        elif 'Unpacking' in line or 'Desempaquetando' in line or 'Dépaquetage' in line or 'Entpacken' in line:
                            # Extract package name for better status
                            pkg_name = ""
                            try:
                                parts = line.split()
                                # Find the keyword index
                                keywords = ['Unpacking', 'Desempaquetando', 'Dépaquetage', 'Entpacken']
                                idx = -1
                                for kw in keywords:
                                    if kw in parts:
                                        idx = parts.index(kw)
                                        break
                                
                                if idx != -1 and idx + 1 < len(parts):
                                    pkg_name = parts[idx+1]
                            except:
                                pass
                                
                            if pkg_name:
                                if self.parent_window and hasattr(self.parent_window, 'show_progress'):
                                     GLib.idle_add(self.parent_window.show_progress, f"{_('Unpacking')} {pkg_name}...", None)
                            
                            progress = 0.5 + (current_package / max(total_packages, 1) * 0.25)
                            
                        # 'Setting up' (En), 'Configurando' (Es), 'Paramétrage' (Fr), 'Richte' (De)
                        elif 'Setting up' in line or 'Configurando' in line or 'Paramétrage' in line or 'Richte' in line:
                            # Extract package name
                            pkg_name = ""
                            try:
                                parts = line.split()
                                # Find the keyword index
                                keywords = ['Setting', 'Configurando', 'Paramétrage', 'Richte']
                                idx = -1
                                for kw in keywords:
                                    if kw in parts:
                                        idx = parts.index(kw)
                                        break
                                
                                if idx != -1:
                                    if parts[idx] == 'Setting' and idx + 2 < len(parts) and parts[idx+1] == 'up':
                                         pkg_name = parts[idx+2]
                                    elif idx + 1 < len(parts):
                                         pkg_name = parts[idx+1]
                            except:
                                pass

                            if pkg_name:
                                if self.parent_window and hasattr(self.parent_window, 'show_progress'):
                                     GLib.idle_add(self.parent_window.show_progress, f"{_('Configuring')} {pkg_name}...", None)

                            progress = 0.75 + (current_package / max(total_packages, 1) * 0.25)
                    
                    elif is_flatpak:
                        # Keep existing code for flatpak
                        if 'Descargando' in line or 'Downloading' in line:
                            if match := re.search(r'(\d+)%', line):
                                progress = float(match.group(1)) / 100.0
                    
                    # Update progress bar if we have a value
                    if progress is not None:
                        if self.parent_window and hasattr(self.parent_window, 'show_progress'):
                            # Only update fraction, keep text if we set it specifically above
                            GLib.idle_add(self.parent_window.show_progress, None, progress)
                        elif self.progress_bar:
                            GLib.idle_add(self.progress_bar.set_fraction, progress)
                    else:
                        # Just update text if no progress value
                        if self.parent_window and hasattr(self.parent_window, 'show_progress'):
                            GLib.idle_add(self.parent_window.show_progress, line, None)
                
                process.wait()
                
                # Complete the progress bar and status
                if self.parent_window and hasattr(self.parent_window, 'show_progress'):
                    GLib.idle_add(self.parent_window.show_progress, _('Installation complete'), 1.0)
                elif self.progress_bar:
                    GLib.idle_add(self.progress_bar.set_fraction, 1.0)
                
                if self.status_label and not self.parent_window:
                     GLib.idle_add(self.status_label.set_text, _('Installation complete'))
                
                # Wait a moment and clear
                time.sleep(1)
                
                if self.parent_window and hasattr(self.parent_window, 'hide_progress'):
                    GLib.idle_add(self.parent_window.hide_progress)
                else:
                    if self.progress_bar:
                        GLib.idle_add(self.progress_bar.set_fraction, 0.0)
                    if self.status_label:
                        GLib.idle_add(self.status_label.set_text, "")
                
                self.current_process = None
                self.command_running = False
                
                # Run callback if provided
                if on_complete:
                    GLib.idle_add(on_complete)
                
            except Exception as e:
                error_msg = f"{_('Error')}: {str(e)}"
                if self.parent_window and hasattr(self.parent_window, 'show_progress'):
                     GLib.idle_add(self.parent_window.show_progress, error_msg, 0.0)
                elif self.status_label:
                    GLib.idle_add(self.status_label.set_text, error_msg)
                
                if self.progress_bar and not self.parent_window:
                    GLib.idle_add(self.progress_bar.set_fraction, 0.0)
                    
                self.current_process = None
                self.command_running = False
        
        threading.Thread(target=execute_command, daemon=True).start()

# Convenience function for scripts that don't need the full class
def run_command(command, progress_bar=None, status_label=None, on_complete=None):
    runner = CommandRunner(progress_bar, status_label)
    runner.run_command(command, on_complete)
