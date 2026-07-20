# Soplos Welcome

[![License: GPL-3.0+](https://img.shields.io/badge/License-GPL--3.0%2B-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Version](https://img.shields.io/badge/version-2.1.0--9-green.svg)]()

A welcome application for Soplos Linux that helps new users get started with their system.

*A welcome application for Soplos Linux that helps new users get started with their system.*

## 📝 Description

Soplos Welcome is a welcome application that guides new users through the initial setup and customization of their Soplos Linux system, providing an easy and friendly experience.

## ✨ Features

- Initial system setup
- **Complete Hardware Detection**: Automatic CPU, GPU, RAM, storage, network, VM, and hybrid graphics detection
- **Advanced Driver Management**: NVIDIA (590/580/550/470/390/340), AMD, Wi-Fi, VM Tools with one-click installation
- **Hybrid Graphics Support**: PRIME Render Offload (battery saving) and NVIDIA Primary (max performance) for laptops
- **Two-Phase NVIDIA Installation**: Systemd-based installation for .run files prevents black screen issues
- **NVIDIA Extras**: DaVinci Resolve OpenCL/CUDA libraries, Blender CUDA Toolkit
- **Kernel Management**: Liquorix, XanMod (x64v3, x64v4, EDGE, LTS) with NVIDIA compatibility checks
- **CPU Microcode Updates**: Intel and AMD firmware security updates
- **System Maintenance**: Clean old kernels, Update GRUB
- **Security Center**: Backups (Timeshift/Deja Dup), Firewall (GUFW), Antivirus (ClamTk), and Filesystem tools
- **Desktop Customization**: Native tools for XFCE, GNOME, and Plasma + Soplos exclusive tools
- Installation of recommended software
- Access to help and support resources
- Intuitive and user-friendly interface
- Support for multiple languages
- **Universal Desktop Support**: XFCE/Tyron (LightDM), KDE Plasma/Tyson (SDDM), GNOME/Boro (GDM3)
- **Display Protocol Support**: Full X11 and Wayland compatibility with automatic detection
- **Environment Detection**: Automatic DE, display manager, and display protocol detection
- **Advanced Architecture**: Modular design with Python and GTK3

## 📸 Screenshots

### Welcome Tab
![Welcome Tab](https://raw.githubusercontent.com/SoplosLinux/soplos-welcome/main/assets/screenshots/screenshot01.png)

### Software Tab - Install Software Centers
![Software Tab](https://raw.githubusercontent.com/SoplosLinux/soplos-welcome/main/assets/screenshots/screenshot02.png)

### Drivers Tab - Hardware Scan and NVIDIA/AMD (Part 1)
![Drivers Tab Part 1](https://raw.githubusercontent.com/SoplosLinux/soplos-welcome/main/assets/screenshots/screenshot03.png)

### Drivers Tab - Wi-Fi, Other Drivers, and VM Tools (Part 2)
![Drivers Tab Part 2](https://raw.githubusercontent.com/SoplosLinux/soplos-welcome/main/assets/screenshots/screenshot04.png)

### Kernels Tab - CPU Microcode and System Information (Part 1)
![Kernels Tab Part 1](https://raw.githubusercontent.com/SoplosLinux/soplos-welcome/main/assets/screenshots/screenshot05.png)

### Kernels Tab - Liquorix and XanMod Kernel Variants (Part 2)
![Kernels Tab Part 2](https://raw.githubusercontent.com/SoplosLinux/soplos-welcome/main/assets/screenshots/screenshot06.png)

### Security Tab - System Backups and Firewall (Part 1)
![Security Tab Part 1](https://raw.githubusercontent.com/SoplosLinux/soplos-welcome/main/assets/screenshots/screenshot07.png)

### Security Tab - Filesystem Tools and Antivirus (Part 2)
![Security Tab Part 2](https://raw.githubusercontent.com/SoplosLinux/soplos-welcome/main/assets/screenshots/screenshot08.png)

### Recommended Tab - Install Recommended Software
![Recommended Tab](https://raw.githubusercontent.com/SoplosLinux/soplos-welcome/main/assets/screenshots/screenshot09.png)

### Customization Tab - Personalize Your System
![Customization Tab](https://raw.githubusercontent.com/SoplosLinux/soplos-welcome/main/assets/screenshots/screenshot10.png)

### Gaming Tab - System Optimizations (Part 1)
![Gaming Tab Part 1](https://raw.githubusercontent.com/SoplosLinux/soplos-welcome/main/assets/screenshots/screenshot11.png)

### Gaming Tab - Game Launchers (Part 2)
![Gaming Tab Part 2](https://raw.githubusercontent.com/SoplosLinux/soplos-welcome/main/assets/screenshots/screenshot12.png)

### Gaming Tab - RGB Theme Activated
![Gaming RGB Theme](https://raw.githubusercontent.com/SoplosLinux/soplos-welcome/main/assets/screenshots/screenshot13.png)

## 🔧 Installation

```bash
# Installation instructions
sudo apt install soplos-welcome
```

## 🌐 Supported Languages (100% Complete)

- 🇪🇸 Spanish (Español)
- 🇬🇧 English
- 🇫🇷 French (Français)
- 🇵🇹 Portuguese (Português)
- 🇩🇪 German (Deutsch)
- 🇮🇹 Italian (Italiano)
- 🇷🇺 Russian (Русский)
- 🇷🇴 Romanian (Română)

## 📄 License

This project is licensed under [GPL-3.0+](https://www.gnu.org/licenses/gpl-3.0.html) (GNU General Public License version 3 or later).

This license guarantees the following freedoms:
- The freedom to use the program for any purpose
- The freedom to study how the program works and modify it
- The freedom to distribute copies of the program
- The freedom to improve the program and publish those improvements

Any derivative work must be distributed under the same license (GPL-3.0+).

For more details, see the LICENSE file or visit [gnu.org/licenses/gpl-3.0](https://www.gnu.org/licenses/gpl-3.0.html).


## 👤 Developer

Developed by Sergi Perich  
Website: https://soplos.org  
Contact: info@soploslinux.com

## 🔗 Links

- [Website](https://soplos.org)
- [Report issues](https://github.com/SoplosLinux/soplos-welcome/issues)
- [Help](https://soplos.org)

## 📦 Versions

### v2.1.0-2 (2026-06-29)
- **Fixed — Drivers Tab (NVIDIA uninstall)**: `apt purge` leaves compiled `.ko` files in `/lib/modules/`. Reinstalling a different driver version caused DKMS to refuse with "version not newer". Uninstall script now runs `dkms remove --force` on all NVIDIA entries and removes orphaned `.ko` files from every kernel directory before purging.
- **Fixed — Drivers Tab (NVIDIA install)**: Same stale DKMS state affected the install path when switching versions. Both the CUDA-repo path (590/610) and the Debian-repo path (550) now perform full DKMS cleanup before `apt install`.
- **Fixed — Drivers Tab (590/610 repo setup)**: The `rm -rf "$TEMP_DIR"` line inside Python triple-quoted strings generated a trailing extra quote in the bash output (`"$TEMP_DIR""`). Fixed by converting those blocks to raw strings (`r"""..."""`).
- **Fixed — Drivers Tab (ROCm codename)**: The `CODENAME` case statement included `bookworm` as a branch. Soplos is based on Debian Testing/Trixie moving toward Forky, never Debian 12. Replaced with `trixie` and `forky` cases only.

### v2.1.0-1 (2026-06-24)
- **Drivers Tab — AMD Extras**: new section with ROCm OpenCL (`rocm-opencl-runtime`) and ROCm Full Suite (`rocm`) from AMD's official repo. Adds user to `render` and `video` groups. For RDNA1+ GPUs (RX 5000+, Radeon 600M/700M series).
- **Drivers Tab — NVIDIA Extras checkmarks**: DaVinci Resolve Extras and Blender CUDA Toolkit now show a checkmark when installed.
- **Drivers Tab — LACT removed**: duplicated in Recommended tab, removed from Drivers.
- **Drivers Tab — VirtualBox Guest Additions 7.2.10**: updated bundled installer.
- **Recommended Tab — Helium**: added privacy-focused Chromium-based browser with YouTube integration, installed from latest GitHub release `.deb`.
- **Assets permissions**: normalized to 644 (files) / 755 (dirs) across the entire assets folder.

### v2.1.0 (2026-06-20)
- **Drivers Tab — NVIDIA 610 (Latest)**: new driver button for Blackwell and newer hardware (RTX 50/60 series). Installed via NVIDIA CUDA repo for Debian 13 (`nvidia-driver-pinning-610` + `cuda-drivers-610`).
- **Drivers Tab — NVIDIA 590 renamed to Stable**: label updated from "Latest" to "Stable" now that 610 is the most recent branch.
- **Welcome Tab — Gaming Mode link**: new row below "Customize your desktop" with a clickable link that activates the Gaming tab (same as Ctrl+G).

### v2.0.9-3 (2026-06-09)
- **Fixed — Recommended Tab (Brave Origin icon)**: moved to `brave-origin.png` at the browsers icons root — same flat structure as all other browser icons.
- **Fixed — Recommended Tab (Affinity Suite)**: reverted to 3.0.2 AppImage — the 3.2.0 build switched to Wine 11 and fails on most systems. The 3.0.2 AppImage (Wine 10) is hosted at the same upstream release tag.

### v2.0.9-2 (2026-06-09)
- **Recommended Tab — Brave Origin**: privacy-focused browser by Brave with integrated AI assistant. Installed via official Brave script. Black icon patch applied at install time (patches both hicolor and `/opt` to survive updates).
- **Recommended Tab — Opera**: feature-rich browser with built-in VPN and ad blocker. Installed as Flatpak.
- **Recommended Tab — Zen Browser**: Firefox-based privacy browser. Installed from latest GitHub release `.deb` with dynamic URL.
- **Fixed — Drivers Tab (NVIDIA 550)**: `check_fn` changed from package check to `_get_nvidia_active_version() == '550'` — having the 580 driver installed no longer also marks 550.
- **Fixed — Drivers Tab (NVIDIA false positives on AMD)**: dpkg fallback in `_get_nvidia_active_version()` now gated by `lspci` hardware check — leftover NVIDIA packages no longer trigger false positives on AMD systems.

### v2.0.9-1 (2026-05-29)
- **Fixed — App icon in GNOME Software**: `slide1.png` was being packaged as the application icon, causing GNOME Software to display the wrong image. Removed `slide1.png` from `assets/icons/` — the correct icon (`org.soplos.welcome.png`) is now the only icon file in the repository.

### v2.0.9 (2026-05-28)
- **Drivers Tab — VirtualBox Guest Additions**: Updated to 7.2.8 (first version with Linux 7.0 kernel support). The `.run` installer is now bundled directly in the package (`assets/vbox/`) — no download required. Compiles `vboxguest`, `vboxsf` and `vboxvideo` modules via DKMS.
- **Fixed — Pango markup**: "Security & System Protection" header caused a GTK warning on English and German locales due to unescaped `&` inside a `set_markup()` call. Fixed in the `.po` files for `en` and `de`.

### v2.0.8-9 (2026-05-27)
- **Fixed — Recommended Tab (Affinity)**: Updated AppImage URL to 3.2.0 (3.0.2 was returning HTTP 404). Fixed `printf >` writing `.desktop` file as root under pkexec — now uses `sudo -u $REAL_USER tee` to keep correct ownership.
- **Fixed — Recommended Tab (ES-DE)**: Same `tee` fix applied to the ES-DE `.desktop` file creation under pkexec.
- **Fixed — Recommended Tab (RapidRAW)**: Reverted to Flatpak (`io.github.CyberTimon.RapidRAW`) — a previous session had incorrectly switched it to a Debian `.deb`.
- **Fixed — Recommended Tab (Batch Install)**: `set -e` in the consolidated batch script caused the entire installation chain to abort when one package failed. Each package is now isolated in its own subshell — a failure is reported as a warning and the next package continues normally.
- **Kernels Tab**: Removed the NVIDIA/Liquorix warning notice.
- **Kernels Tab**: Moved Soplos Kernel Installer above Liquorix (below Microcodes).
- **Kernels Tab**: Added Soplos Kernel Installer icon to its section.

### v2.0.8-8 (2026-05-26)
- **Fixed — DaVinci GPU Patch**: `davinci-gpu-patch.sh` created `~/.local/share/applications/` as root (via pkexec), causing Soplos WebApp Manager and Soplos AppImage Manager to fail with `PermissionError: [Errno 13]` when writing `.desktop` files. Fixed by using `sudo -u "$REAL_USER"` for the directory creation.
- **Fixed — Lutris Vulkan Patch**: `lutris-vulkan-patch.sh` could patch an outdated `gpu.py` from a stale Flatpak deployment. After a Flatpak update the new deployment had the unpatched file, causing Lutris to send a repeated vulkaninfo error notification. The script now targets the `active` deployment symlink only.

### v2.0.8-7 (2026-05-25)
- **Recommended Tab — DaVinci Resolve**: Updated MakeResolveDeb to 1.10.0 — adds split `-data` package for Resolve 21+ (plugins folder in a separate `.deb`), drops slow xz compression in favour of default gzip. Install step now handles both `.deb` files automatically.
- **Recommended Tab — Icons**: Updated Calligra icon.

### v2.0.8-6 (2026-05-24)
- **Drivers Tab — Wi-Fi Repair detection improved**: Triple detection strategy — (1) sysfs `/sys/class/net/*/wireless`, (2) `iw dev` when interface is down, (3) `lspci -k` when module is not loaded at all (the exact broken-WiFi-after-reboot case). Now repairs WiFi even when the kernel module failed to initialize at boot.

### v2.0.8-5 (2026-05-23)
- **Drivers Tab — Wi-Fi Repair**: New "Repair Wi-Fi" button automatically detects the active Wi-Fi driver (reads `/sys/class/net/*/wireless`) and reloads it via `modprobe -r` + `modprobe` + `systemctl restart NetworkManager`. Works with any brand (Intel, Realtek, Atheros, MediaTek, etc.).
- **Translations**: Added Wi-Fi Repair strings in all 8 languages.

### v2.1.0-9 (2026-07-20)
- **Translations — Customization Tab (GNOME)**: Added Layout Switcher strings in all 8 languages (en, es, de, fr, it, pt, ro, ru) — "Layout Switcher", "Switch between GNOME Shell layout presets" and "Launch Soplos Layout Switcher" were missing from all .po/.mo files.

### v2.1.0-8 (2026-07-19)
- **Customization Tab (GNOME)**: Added Layout Switcher to the Soplos Tools section — launches `soplos-layout-switcher` to switch between GNOME Shell layout presets. Follows the existing install-if-missing pattern (pkexec apt-get) shared with GRUB Editor and Plymouth Manager.

### v2.1.0-7 (2026-07-10)
- **Added — Drivers Tab (NVIDIA Extras)**: CUDA 12 Toolkit — installs `cuda-toolkit-12` from the NVIDIA CUDA debian12 repository (compatible with PyTorch and TensorFlow cu12 builds). Requires an NVIDIA driver already installed. Button reflects install state and supports uninstall.
- **Added — Drivers Tab (NVIDIA Extras)**: Open Kernel Modules — installs `nvidia-kernel-open-dkms` (official open source NVIDIA kernel module). Requires Turing or newer GPU (RTX 20 series, GTX 1650/1660 or newer). GPU compatibility check via `_is_turing_plus()` before proceeding; incompatible GPUs (Maxwell/Pascal) receive an error dialog. Supports switching back to the proprietary module.
- **Added — Drivers Tab (NVIDIA 590/610)**: `nvidia-kernel-open-dkms` included automatically in the install command for the 590 and 610 driver branches, which target Turing+ hardware exclusively.
- **Added — Drivers Tab (Intel Extras)**: New section between AMD Extras and Wi-Fi. Intel oneAPI Base Toolkit — adds the official Intel oneAPI apt repository (GPG key from Intel), installs `intel-basekit` (DPC++ compiler, MKL, TBB, VTune, Advisor). Supports uninstall including full repository cleanup.
- **Translations**: Added CUDA 12, Intel oneAPI and Open Kernel Modules strings in all 8 languages (en, es, de, fr, it, pt, ro, ru).

### v2.1.0-6 (2026-07-08)
- **Fixed — Environment detection**: `_detect_qt_version()` added `FileNotFoundError` to the exception catch — previously only `subprocess.SubprocessError` and `subprocess.TimeoutExpired` were handled, so when `qmake` is not installed `subprocess.run` raised `FileNotFoundError` that propagated up through `detect_all()` and crashed the application on startup.

### v2.1.0-5 (2026-07-07)
- **Build**: Build dependency `python3-all` replaced with `python3`.

### v2.1.0-4 (2026-07-06)
- **Customization Tab**: Added LucidGlyph font rendering enhancement — install/uninstall from the Soplos Tools section. Uses GitHub latest release via pkexec. On GNOME applies `gsettings font-antialiasing grayscale` automatically. On KDE shows manual instruction for Sub-pixel rendering.
- **Recommended Tab — Hardware**: Added amdgpu_top (AMD GPU monitor, GitHub .deb) and nvtop (GPU process monitor, official repo).
- **Recommended Tab**: Removed FileZilla duplicate from Developer category (now only in Files).
- **Translations**: Updated all 8 languages with LucidGlyph, amdgpu_top and nvtop strings.

### v2.1.0-3 (2026-06-30)
- **Drivers Tab**: Fixed `$SUDO_USER` empty under pkexec in hybrid graphics — `kwinoutputconfig.json` was written to `/root` instead of the user's home. Replaced with `$PKEXEC_UID` pattern.
- **Drivers Tab**: Fixed UI freeze on Wi-Fi repair — `lspci` detection moved to background thread via `threading.Thread` + `GLib.idle_add`.
- **Drivers Tab**: Fixed race condition on recommended driver install — button disabled on first click to prevent multiple concurrent pkexec processes.
- **Software Tab**: Fixed Flatpak install missing `package-update-indicator` (update tray applet) in all three DEs.
- **Software Tab**: Bazaar now shows a warning about system-level Flathub conflict before installing. Install/uninstall use `--system` scope and clean up the system remote on removal.
- **Recommended Tab**: New categories — App Management, Downloads, Hardware, Files (replaces Utilities). Added Transmission, FileZilla, GNOME Commander, Double Commander (AppImage).
- **Recommended Tab**: Multimedia, Graphics and Design, and Office sections reordered by type (players/video/audio, image/vector/3D/photo, suites/PDF).
- **Translations**: All new strings added and compiled in 8 languages (en, es, de, fr, it, pt, ro, ru).

### v2.0.8-4 (2026-05-22)
- **Drivers Tab**: Fixed false "installed" state on Nouveau button — now checks `/etc/modprobe.d/` for `blacklist nouveau`.
- **Drivers Tab**: Fixed false "installed" state on AMD button — now requires all three packages (`firmware-amd-graphics`, `mesa-vulkan-drivers`, `xserver-xorg-video-all`).
- **Drivers Tab**: Fixed false "installed" state on Wi-Fi Intel/Realtek buttons — now combines package presence with `lsmod` module check.
- **Recommended Tab — Utilities**: Added Syncthing Tray (`io.github.martchus.syncthingtray`) — tray application for Syncthing, sync files between devices.
- **Translations**: Added Syncthing Tray description string in all 8 languages.

### v2.0.8-3 (2026-05-18)
- **Gaming Tab**: Added RyzenAdj to Optimizations — compiles from source, installs binary + shared library + systemd service with AMD thermal limits. Ideal for AMD mini PCs with proprietary EC firmware.
- **Gaming Tab**: Added Lutris Vulkan Fix button — manual patch for `gpu.py` inside the Lutris Flatpak to fix broken `vulkaninfo` path. Replaces unreliable post-install auto-hook.
- **Gaming Tab**: Removed Ryzen Master Commander (incompatible with proprietary EC firmware on AMD mini PCs — requires NBFC).
- **Fixed**: Ctrl+Shift+Tab backward tab navigation (GTK sends `KEY_ISO_Left_Tab`, now handled correctly).
- **Translations**: Added RyzenAdj and Lutris Vulkan Fix strings in all 8 languages.

### v2.0.8-2 (2026-04-30)
- **Software Tab — Snap Store & Bazaar**: Added to all three DEs (XFCE, GNOME, KDE/Plasma) in a 4-column × 2-row grid layout. Snap Store installs via `snap:snap-store`; Bazaar installs via `flatpak:io.github.kolunmi.Bazaar`.
- **Security Tab — VPN**: Added Surfshark (`com.surfshark.Surfshark`) and Mozilla VPN (`org.mozilla.vpn`) as Flatpak entries in the VPN section, with Install/Uninstall/Open buttons and state detection.
- **Gaming Tab — Optimizations**: Added CPU Power tool (installs `linux-cpupower` + `cpupower-gui`) to control the CPU frequency governor from a graphical interface.
- **Recommended Tab — Office**: Added Calligra (`org.kde.calligra`) and Collabora Office (`org.collaboraoffice.CollaboraOffice`) as Flatpak entries in the Office section.
- **Footer**: Removed "Ready/Listo" status prefix; now shows only the DE and display protocol.
- **Customization Tab**: Docklike launcher removed from XFCE tools (functionality now integrated into Soplos Theme Manager).
- **Dependency check dialog**: Clicking Snap Store without `snapd`, or Bazaar without `flatpak`, shows a warning dialog that offers to install the missing runtime first.
- **Fixed: Snap Store/Bazaar buttons now show "Uninstall" when already installed**: `snap install/remove` was missing `pkexec` and failing silently as a regular user, leaving buttons stuck on "Install". Fixed. Also fixed a GLib.idle_add callback loop caused by the on_complete lambda returning the timer source ID.
- **Fixed: program no longer hangs after installing Bazaar**: `flatpak install` now uses `--user --noninteractive` to avoid interactive prompts.
- **Translations**: Added new strings for all new features in all 8 languages.

### v2.0.8-1 (2026-04-04)
- **DaVinci Resolve**: Updated MakeResolveDeb script to 1.9.0 (adds DaVinci Resolve 21 support, xz compression).
- **DaVinci Resolve**: New optional post-install patches dialog with virtual microphone patch (for systems without audio capture device) and integrated GPU patch for AMD/Intel iGPU (OpenCL stack, i915 firmware, libProResRAW stub, launcher patching, render group membership).
- **Drivers Tab**: Fixed crash on startup (uninitialized button registry and missing subprocess import).
- **Drivers Tab**: All 15 driver buttons now show install/uninstall state and refresh automatically after each operation. NVIDIA 590 and 580 buttons were missing from the registry.
- **Hardware Scanner**: Fixed broken GPU section (old single-GPU API). Now shows all hardware sections (GPU, Wi-Fi, Audio, Bluetooth, Printers, VM Tools) with Install/Uninstall buttons and driver status.
- **New Apps**: Added ProtonVPN (Security → VPN), ClamUI (Security → Antivirus), LACT (Drivers → AMD), Resources (Recommended → Utilities), Soplos Kernel Installer (Kernels tab).
- **Portmaster**: Added to Security tab (Firewall section); installs via official `portmaster-installer.deb` with no hardcoded version number.
- **JoPDF**: Added to Recommended tab (Ofimática/Office section) as a PDF editor.
- **qBittorrent & JDownloader**: Added to Recommended tab (Utilities section) via Flatpak.
- **PPSSPP**: Added to Recommended (Gaming section) and Gaming tab launchers via Flatpak. Post-install script auto-links the Flatpak binary as the Lutris PSP runner.
- **LACT (utilities) & CoolerControl**: Added to Recommended tab (Utilities section). CoolerControl installs as a root AppImage daemon with a WebApp shortcut for the web UI.
- **MangoHud**: Reworked to install via Flatpak with 6 packages: MangoHud, GOverlay, VulkanInfo, vkBasalt, gamescope, DXVK.
- **Post-install script system**: Recommended and Gaming tabs now support a `post_install_script` hook in any package entry; runs automatically after a successful install.
- **Lutris Vulkan patch**: Auto-applied after Lutris install — patches `gpu.py` inside the Flatpak to fix `vulkaninfo` path.
- **Translations**: Added `"Complete installation"` string and translations for all new apps in all 8 languages.
- **Security Tab — Icons**: 48 px icons added to all 14 tools (Timeshift, Grub BTRFS, Deja Dup, BTRFS Assistant, GUFW, Portmaster, Proton VPN, BleachBit, Stacer, Sweeper, Soplos Sys Cleaner, ClamTk, ClamUI, rkhunter) with the same centred icon+name+description row layout as Gaming and Recommended tabs.
- **Security Tab — Portmaster**: Open Portmaster button (gtk-launch with path fallback) and UFW conflict warning label when both Portmaster and UFW are active simultaneously.
- **Gaming Tab — GeForce NOW**: New WebApp launcher that creates a Soplos WebApp Manager `.desktop` entry for `https://play.geforcenow.com/` with automatic browser detection.
- **Gaming Tab — Badges & Tooltips**: All launcher widgets now show Flatpak/AppImage/WebApp badges; all 7 optimization buttons show tooltip descriptions on hover.
- **Gaming Tab — MangoHud**: Corrected Flatpak package IDs to the exact required values (`io.github.benjamimgois.goverlay`, `org.freedesktop.Platform.VulkanLayer.MangoHud`, `org.winehq.Wine.DLLs.dxvk`, etc.).
- **Software Tab (XFCE)**: GNOME Software now also installs `gnome-packagekit` so the panel update indicator can apply updates.
- **Translations**: Added missing translation strings for Security tab tool descriptions, driver status labels, kernel AVX2 description, and app descriptions (JDownloader, qBittorrent, JoPDF) in all 8 languages.
- **Hybrid Graphics — NVIDIA Primary fix**: Dracut config files were not created before initramfs regeneration, causing the system to boot without NVIDIA modules loaded. Now creates `/etc/dracut.conf.d/nvidia.conf` and `blacklist-nouveau.conf` before calling `dracut --force`.
- **Hybrid Graphics — PRIME Offload KDE fix**: Script now generates `~/.config/kdedefaults/kwinoutputconfig.json` with the Intel display connector detected dynamically from `/sys/class/drm/` (eDP or LVDS), setting output priority without hardcoding resolution, refresh rate or scale. Only runs on KDE Plasma (detected via EnvironmentDetector at launch).

### v2.0.8 (2026-03-31)
- **Customization Tab**: Soplos tool buttons now detect if the tool is installed and offer an install dialog with auto-launch on success.
- **Recommended Tab**: Added 6 new Flatpak apps: Bitwig Studio, Reaper, Zrythm, Ardour, Warehouse, PeaZip.
- **Keyboard Navigation**: Ctrl+Shift+Tab for backward tab navigation; F1 opens the About dialog.
- **UI Fixes**: Fixed dark strip in About dialog (dark and light themes). Welcome tab now includes Security in the features list with correct icons and tab order. Removed emojis from Drivers tab Frame labels.
- **Code Audit**: Removed demo code, fixed deprecated get_action_area(), fixed duplicate imports, removed "coming soon" placeholder text.
- **Translations**: Updated all 8 languages with new strings for install flow, 6 new apps, and Security feature.

### v2.0.7-3 (2026-03-24)
- **NVIDIA 580 Fix**: Resolved SHA1/sqv rejection on Debian 13 using `[trusted=yes]` repo entry, version pinning with `nvidia-driver-pinning-580`, and `--allow-downgrades` to handle newer package versions.
- **Hardware Detection**: GTX 16xx/MX550/MX450 correctly mapped to driver 590; Maxwell GPUs (GTX 9xx/8xx, 9xxM) correctly mapped to driver 580. Added lspci caching to avoid duplicate system calls.
- **Security Tab**: Added Soplos Sys Cleaner to the Cleaning section with install/uninstall and launch button.
- **Recommended Tab**: Added Soplos AppImage Manager to Utilities. OBS Studio and HandBrake switched to Flatpak. New AppImage badge for AppImage-based packages. Official badge now only shown for APT-installed packages.
- **Gaming Tab**: Lutris switched to Flatpak installation in both Recommended and Gaming tabs.
- **Translations**: Updated all 8 languages with 4 new strings (AppImage Manager description, AppImage badge, Sys Cleaner description, Open Sys Cleaner button).

### v2.0.7-2 (2026-03-13)
- **NVIDIA Driver Logic Fixes**: Corrected mapping for MacBook Kepler GPUs (650M/750M) and improved driver detection for MX/GT series.
- **Improved Installation Workflow**: Added confirmation dialogs for all NVIDIA installation paths, explicit installation of auxiliary tools (nvidia-smi, settings, modprobe), and pre-installation driver cleanup.
- **Translations**: Updated all 8 supported languages with 4 new confirmation dialog strings.

### v2.0.7-1 (2026-03-12)
- **NVIDIA Driver Improvements**: Improved official repository installation logic for Debian 12/13.
- **Keyring Management**: Switched to official `cuda-keyring` package for more robust GPG handling.

### v2.0.7 (2026-03-11)
- **NVIDIA Legacy Drivers**: Legacy drivers (340, 390, 470) now install via APT from Debian Sid instead of `.run` files.
- **Debian Sid Workflow**: Two-step dialog guides users to enable Sid via Soplos Repo Selector before installing legacy drivers.
- **Automatic Repo Selector Launch**: Legacy driver buttons now automatically open Soplos Repo Selector and wait for the user to finish.
- **Correct APT Packages**: Updated to `nvidia-legacy-340xx-driver`, `nvidia-legacy-390xx-driver`, `nvidia-tesla-470-driver`.
- **Translations**: Added 4 new legacy driver dialog strings in all 8 languages.

### v2.0.6-3 (2026-03-08)
- **AppImages**: Fixed `Errno 13 Permission denied` when creating web apps by installing all AppImages (Affinity Suite, ES-DE, Stacer) to `~/AppImage` instead of `/opt` or `~/.local`, and removing the use of `pkexec` for their installation to prevent root ownership of user directories.

### v2.0.6-2 (2026-03-07)
- **Gaming Tab**: Fixed an issue where installing gaming wallpapers on GNOME (Boro) would duplicate existing Soplos wallpapers in the background settings.

### v2.0.5 (2026-03-02)
- **Recommended Tab**: Fixed batch installation collision logic with custom script applications (e.g., ES-DE and Affinity Suite).

### v2.0.4 (2026-02-24)
- **Gaming Tab**: Added Sober (Roblox) and EmulationStation-DE (AppImage) launchers.
- **Gaming Tab**: Internationalized all 14 launcher descriptions with `_()` and 8-language translations.
- **Gaming Tab**: Fixed launcher alignment with uniform height (60px) and consistent layout.
- **Kernels Tab**: "Kernels" name kept untranslated as universal technical term.
- **Kernels Tab**: Rewritten Clean Old Kernels with smart classification (keeps latest base + Liquorix + XanMod + running), confirmation dialog, and single `pkexec`.
- **Security Tab**: Stacer converted from broken `.deb` to stable AppImage (`/opt/stacer/`).
- **Translations**: Added 15+ new translation strings across all 8 languages.

### v2.0.3 (2026-01-09)
- **Documentation**: Added manual page and copyright file.

### v2.0.2 (2026-01-04)
- **Security Tab**: Added **Grub BTRFS** management (Automatically add BTRFS snapshots to GRUB menu).
- **Security Tab**: Fixed TimeShift integration to work seamlessly with grub-btrfs.
- **Languages**: Updated all translation dictionaries with new strings.

### v2.0.1 (2025-12-27)
- **NVIDIA Driver Improvements**: Added NVIDIA 580 Production driver (580.119.02) for RTX 40/50 series
- **RTX 50/40 Detection**: Proper GPU detection for Blackwell and Ada Lovelace architectures
- **GTX 10xx Fix**: Pascal GPUs now correctly use latest driver instead of legacy 470
- **UI Updates**: Clearer driver version labels ("NVIDIA 550 Repo" and "NVIDIA 580 Production")
- **Fixed GPU detection bug**: No longer always recommends driver 580 for all GPUs
- **Legacy GPU support**: GeForce 8000/9000 and MacBook GPUs (GT 320M, 330M, 650M, 750M) now recommend `nouveau`
- **Quadro/Tesla cards**: Professional GPUs now properly detected and recommended repo driver
- **Safer fallback**: Unknown GPUs now default to `nvidia-driver` (repo) instead of 580

### v2.0.0 (2025-12-06)
- **Complete Rewrite**: New modular architecture for better maintainability.
- **Universal Support**: Unified codebase for GNOME, KDE, and XFCE.
- **Improved UI**: Modernized interface with better theming support.
- **Enhanced Software Center**: Better integration with native package managers.
- **Driver Management**: Hardware detection and automatic driver recommendations.
- **Kernel Management**: Liquorix and XanMod kernels (4 variants: x64v3, x64v4, EDGE, LTS) with NVIDIA compatibility checks.
- **CPU Microcode**: Intel and AMD firmware security updates.
- **System Maintenance**: Tools to clean old kernels and update GRUB.
- **Recommended Tab Enhancements**:
  - **Search and Filter**: Real-time search to quickly find applications by name or description, with persistent state across mode switches
  - **Batch Installation Mode**: "Selección Múltiple" mode for installing multiple packages at once (APT consolidated, Flatpak/deb/custom scripts sequential, only DaVinci excluded)
  - **Batch Selection Controls**: "Seleccionar Todos" and "Deseleccionar Todos" buttons that respect active search filter
  - **Custom Script Support**: Complex installation workflows (repository setup, GPG keys, multi-step installations).
  - **Global Progress Bar Integration**: All operations now use the unified progress bar system.
  - **Improved Error Handling**: Better feedback and UI recovery on installation failures.
  - **UI Stability Fixes**: Resolved freezing and deformation issues during package operations.
- **Software Updates**:
  - **DaVinci Resolve**: Added professional video editor with optimized custom installation workflow:
    - Sequential installation process (dependencies → extraction → conversion → installation)
    - Performance optimization: Reduced package build time from ~45 minutes to ~5-10 minutes using faster gzip compression
    - Fixed .deb installation using `dpkg -i` with automatic dependency resolution
    - Enhanced error handling and comprehensive debug logging
    - Script by Daniel Tufvesson with Soplos optimizations
  - **RapidRAW**: Replaced RawTherapee with RapidRAW (modern RAW photo editor via .deb).
  - **Google Antigravity**: Replaced Geany with Google Antigravity IDE (custom repository installation).
  - **Midori**: Replaced Epiphany with Midori lightweight browser (.deb installation).
  - **Snap Removal**: Removed Snap support from Recommended software to prioritize native and Flatpak packages.
- **Gaming Features**:
  - **System Optimizations**: GameMode installation, CPU performance script with power-profiles-daemon, gaming kernel parameters (sysctl).
  - **Performance Mode**: Fully implemented with automatic power-profiles-daemon installation and configuration.
  - **GPU Optimization**: Automatic GPU vendor detection (NVIDIA/AMD/Intel) with driver environment configuration for optimal gaming performance.
  - **Disk I/O Optimization**: Udev rules for optimal disk schedulers (mq-deadline for SSD, none for NVMe, BFQ for HDD).
  - **Performance Tools**: MangoHud + Goverlay for FPS monitoring and overlay customization.
  - **Game Launchers**: Full installation support for 13 gaming platforms:
    - Steam (Flatpak) - Digital game distribution platform
    - Lutris (APT/Flatpak) - Unified game manager for Linux
    - Heroic Games Launcher (Flatpak) - Epic Games, GOG, and Amazon Games
    - Bottles (Flatpak) - Run Windows applications using Wine
    - Vinegar (Flatpak) - Modern Roblox Launcher
    - R2ModMan (Flatpak) - Mod manager for Lethal Company, Valheim, etc.
    - Prism Launcher (Flatpak) - Custom Minecraft launcher
    - Itch.io (Flatpak) - Indie game marketplace
    - Minigalaxy (APT/Flatpak) - Simple GOG.com client
    - RetroArch (APT/Flatpak) - Multi-emulator frontend
    - Moonlight (Flatpak) - NVIDIA GameStream/Sunshine client
    - Chiaki (Flatpak) - PlayStation Remote Play (HDR support)
    - Discord (Flatpak) - Gaming community communication
  - **Installation Method Badges**: Visual indicators showing APT or Flatpak installation methods.
  - **Official Package Badges**: Security indicators for official repository packages.
  - **RGB Gaming Theme**: Toggle-able black theme with red neon accents, applies instantly without restart.
  - **Gaming Wallpapers**: Automatic installation of gaming-themed wallpapers with GNOME XML registry support.
  - **Revert Functionality**: Easy rollback of gaming optimizations.
- **UI Improvements**:
  - **Category Icons**: Updated Development category icon to VS Code, Gaming category icon to Steam.
  - **Installation Methods**: Full support for APT, Flatpak, .deb URLs, and custom installation scripts.
- **System Integration**:
  - **Icon Fixes**: Corrected application icon visibility by renaming assets to match App ID (`org.soplos.welcome`).
  - **Desktop Entry**: Added proper `.desktop` file for system integration.
- **Fixed Welcome URLs**: Updated all links to point to soplos.org.
- **Fixed Repo Selector**: Button now launches the application instead of attempting installation.
- **Fixed KDE Icon**: Resolved application icon display issue in KDE Plasma with proper WM_CLASS configuration.
- **Fixed Welcome Tab Autostart**: Corrected .desktop file creation and path resolution for autostart functionality.
- **Fixed Flatpak Installation**: Corrected Flathub repository setup and package installation in Tyson variant.
- **Recommends Tab UI**: Improved button alignment consistency with minimum height enforcement for description labels.
- **Fixed Gaming Tab**: Dialog messages now display line breaks correctly, GPU detection avoids false AMD positives in VMs, removed 32-bit package dependencies, all optimizations use single password prompt, complete Revert All functionality.
- **Fixed UFW Firewall**: Status detection and activation (single password prompt, no interactive prompts), periodic status updates to detect external changes.
- **Fixed BTRFS Detection**: Filesystem detection for Calamares subvolumes (@, @home).
- **Fixed Window Deformation**: Progress label stretching during downloads.
- **Improved Gaming Tab**: Fixed wallpaper installation progress bar, added Performance Mode toggle, updated Revert All dialog, removed wallpaper uninstallation for safety.
- **Fixed Batch Installation**: Improved reliability for Chrome, RapidRAW, Midori, and Cursor installations.
- **Fixed Clean System**: Optimized to require only a single password prompt.
- **Fixed Recommended Tab UI**: Resolved scrollbar overlap issue.
- **Updated Google Antigravity**: Description updated to "Advanced Agentic AI Coding Assistant".
- **Fixed Translations**: Comprehensive cleanup of Spanish dictionary and missing wallpaper messages.
- **Fixed ClamAV**: Resolved password prompt and translation issues.
- **Fixed Progress Bar**: Corrected percentage overflow (>100%) in batch mode.
- **Fixed Recommended Tab Scrollbar**: Resolved vertical scrollbar overlapping content boxes.
- **Complete French Dictionary**: Full revision and 100% translation (565 messages), fixed corrupted syntax, added 35+ new translations.
- **Complete German Dictionary**: Full revision, fixed typo "Dunkle" (Dark theme), 100% translation (565 messages).
- **Complete Italian Dictionary**: Full revision and 100% translation (565 messages), 35 missing translations added, 23 fuzzy flags corrected.
- **Complete Portuguese Dictionary**: Full revision and 100% translation (565 messages), fixed typo "PROPÓSITIO", improved "Upgrade" localization.
- **Complete Romanian Dictionary**: Full revision and 100% translation (565 messages), added missing help texts.
- **Complete Russian Dictionary**: Full revision and 100% translation (565 messages), 14 missing translations added, 23 fuzzy fixed, typo "интерфейфейс" corrected.
- **Translation Quality**: All 8 languages (EN, ES, DE, FR, IT, PT, RO, RU) now at 100% with 565 messages each.

### Tyson (v1.0.0 – v1.1.5)

#### v1.1.5 (2025-09-08)
- Updated website, forum and wiki URL buttons to soplos.org.
- Removed deprecated `on_website_clicked` and `on_wiki_clicked` handlers (replaced by inline lambdas).
- Updated Blender icon.

#### v1.1.4 (2025-09-08)
- Updated Blender icon and fixed link buttons in the welcome tab.

#### v1.1.3 (2025-08-02)
- Updated all translation dictionaries.
- Fixed several functions in the hardware detector.
- Updated all program icons.

#### v1.1.2 (2025-07-27)
- Changed program icon to a new design.

#### v1.1.1 (2025-07-27)
- Fixed office install/uninstall button logic in the Recommended tab.
- Fixed hardware detector.

#### v1.1.0 (2025-07-24)
- Fixed Flatpak/Flathub installation bug.

#### v1.0.9 (2025-07-18)
- Fixed install buttons in the Software Center.

#### v1.0.8 (2025-07-15)
- Improvements in QEMU/KVM integration.
- Enhanced management and installation of NVIDIA drivers.
- Translation dictionary fragmentation completed.
- Full internationalization.

#### v1.0.7 (2025-07-13)
- Metainfo update to comply with AppStream/DEP-11.

#### v1.0.6 (2025-06-24)
- Internationalization improvements.
- Minor bug fixes.

#### v1.0.5 (2025-06-14)
- Reverted App ID to `com.soplos.welcome` (dot notation restored).
- Soplos Packager block removed from `main.py`.
- Assets renamed back to `com.soplos.welcome` convention.

#### v1.0.4 (2025-06-09)
- Autostart updated: copies system `.desktop` file instead of writing inline content.
- Desktop file references updated to `com.soploswelcome` (ID, icon, StartupWMClass).

#### v1.0.3 (2025-06-05)
- Soplos Packager App ID block injected into `main.py` for correct window manager integration.

#### v1.0.2 (2025-06-04)
- Renamed all assets from `com.soplos.welcome` to `com.soploswelcome` (dot removed).

#### v1.0.1 (2025-05-28)
- Fixed welcome tab website URL to use distro-specific link.

#### v1.0.0 (2025-05-20)
- Port of Tyron 1.0.0 to Soplos Tyson. Initial release of Soplos Welcome for Tyson.

### Tyron (v1.0.0 – v1.1.4)

#### v1.1.4 (2025-09-08)
- Updated Blender icon and fixed link buttons in the welcome tab.

#### v1.1.3 (2025-08-03)
- Updated all translation dictionaries.
- Fixed several functions in the hardware detector.
- Updated all program icons.

#### v1.1.2 (2025-07-27)
- Changed program icon to a new design.

#### v1.1.1 (2025-07-27)
- Fixed office install/uninstall button logic in the Recommended tab.
- Fixed hardware detector.

#### v1.1.0 (2025-07-25)
- Fixed Flatpak/Flathub installation bug.

#### v1.0.9 (2025-07-24)
- Fixed install buttons in the Software Center.

#### v1.0.8 (2025-07-24)
- Improvements in QEMU/KVM integration.
- Enhanced management and installation of NVIDIA drivers.
- Translation dictionary fragmentation completed.
- Full internationalization.

#### v1.0.7 (2025-07-18)
- Metainfo update to comply with AppStream/DEP-11.

#### v1.0.6 (2025-05-20)
- Internationalization improvements.
- Minor bug fixes.

#### v1.0.5 (2025-05-08)
- Reverted App ID to `com.soplos.welcome` (dot notation restored).
- Soplos Packager block removed from `main.py`.
- Assets renamed back to `com.soplos.welcome` convention.

#### v1.0.4 (2025-05-07)
- Autostart updated: copies system `.desktop` file instead of writing inline content.
- Desktop file references updated to `com.soploswelcome` (ID, icon, StartupWMClass).

#### v1.0.3 (2025-05-06)
- Soplos Packager App ID block injected into `main.py` for correct window manager integration.

#### v1.0.2 (2025-05-05)
- Renamed all assets from `com.soplos.welcome` to `com.soploswelcome` (dot removed).

#### v1.0.1 (2025-04-25)
- Fixed welcome tab website URL to use distro-specific link.

#### v1.0.0 (2025-04-08)
- Initial release.
