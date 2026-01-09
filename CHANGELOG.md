# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/lang/en/).

## [2.0.3] - 2026-01-09

### 📚 Documentation
- **Man Page**: Added complete manual page (`docs/soplos-welcome.1`) with standard sections (NAME, SYNOPSIS, DESCRIPTION, OPTIONS, FILES, AUTHOR, COPYRIGHT, SEE ALSO).
- **Debian Copyright**: Added machine-readable copyright file (`debian/copyright`) following Debian 1.0 format with full GPL-3.0+ license block.

## [2.0.2] - 2026-01-04

### 🛡️ Security Tab Enhancements
- **New Feature: Grub BTRFS Integration** - Added one-click installation for `grub-btrfs` to automatically add snapshots to GRUB boot menu.
- **Intelligent Detection** - Only shows Grub BTRFS option if BTRFS filesystem is detected (same as BTRFS Assistant).
- **Streamlined Installation** - Uses `pkexec` for secure installation from official Soplos repositories.
- **Complementary Tool** - Positioned next to TimeShift in System Backups section as a companion tool.

### 🌍 Internationalization
- **Updated Translations** - Added translations for Grub BTRFS feature in all 8 languages (ES, EN, FR, DE, PT, IT, RO, RU).
- **Dictionary Updates** - Verified and synchronized translation keys.

## [2.0.1] - 2025-12-27

### 🚀 Hybrid Graphics Support (NEW)
- **Hybrid GPU Detection**: Automatic detection of Intel/AMD + NVIDIA configurations on laptops
- **PRIME Render Offload**: On-demand NVIDIA usage for battery saving (recommended for most users)
- **NVIDIA Primary Mode**: Always use dedicated GPU for maximum performance
- **Multi-DE Configuration**: Automatic configuration for GNOME (GDM3), KDE Plasma (SDDM), and XFCE (LightDM)
- **X11 and Wayland Support**: Proper configuration for both display protocols
- **Environment Detection Integration**: Uses `EnvironmentDetector` for smart DE/DM/protocol detection

### 🔧 Two-Phase NVIDIA Installation (NEW)
- **Systemd-based .run Installation**: Prevents black screen issues after driver installation
- **Phase 1 - Preparation**: Creates systemd service, blacklists nouveau, configures GRUB, reboots to multi-user.target
- **Phase 2 - Installation**: Installs driver without X running, regenerates initramfs, restores graphical boot
- **Fully Automatic**: User only needs to wait for two automatic reboots
- **Display Manager Support**: Automatic detection and restart of GDM3, SDDM, or LightDM

### 🎮 NVIDIA Driver Improvements
- Added **NVIDIA 590 driver** (590.48.01) - Latest driver for RTX 50/40/30 series
- Added **NVIDIA 580 Production driver** (580.119.02) for RTX 40/50 series
- **RTX 50 series (Blackwell)** now properly detected and recommended driver 590
- **RTX 40 series (Ada Lovelace)** now properly detected and recommended driver 580
- **GTX 10xx series (Pascal)** moved to latest driver support (was incorrectly recommending legacy 470)
- Drivers now ordered by version (590 → 580 → 550 → 470 → 390 → 340)
- **New "NVIDIA Extras" section** - Separated DaVinci Resolve and Blender CUDA tools from drivers
- Updated driver version labels in UI: "NVIDIA 590 (Latest)", "NVIDIA 580 (Production)", "NVIDIA 550 (Repo)"
- Improved hardware detection logic for modern NVIDIA GPUs

### � New Recommended Software
- **Multimedia**: Spotify (streaming service), HandBrake (video transcoder)
- **Communications**: Slack (team collaboration), Zoom (video conferencing)
- **Developer**: Postman (API testing)
- **Graphics**: RawTherapee (RAW processing), Hugin (panorama stitcher)

### �🛠️ Fixed
- **Single pkexec authentication** - All driver installation scripts now use single `pkexec bash` call instead of multiple `pkexec` commands (one password prompt instead of many)
- **Fixed `echo | pkexec tee` pattern** - Replaced with direct file writes since scripts run as root
- Corrected driver recommendation mapping for RTX 40/50 to use nvidia-driver-580/590
- Updated driver installation version map for automated driver selection
- **Fixed GPU detection always recommending driver 580** - Now correctly maps GPU series to appropriate drivers
- **Legacy GPU detection** (GeForce 8000/9000, MacBook GPUs) now recommends `nouveau` instead of proprietary drivers
- **Quadro/Tesla professional cards** now properly detected and recommended `nvidia-driver` (repo)
- **Changed default fallback** from `nvidia-driver-580` to `nvidia-driver` (repo) for safer unknown GPU handling

## [2.0.0] - 2025-12-06

### 🏗️ Architecture Rewrite
- Complete rewrite with modern, modular architecture.
- Separation of concerns: Core, UI, Services, Utils layers.
- Professional project structure with focused, maintainable modules.

### 🔧 Universal Desktop Compatibility
- Smart desktop environment detection.
- GNOME 48+ full integration.
- KDE Plasma 6 native support.
- XFCE 4.20 optimization.
- Complete X11 and Wayland compatibility.

### 🌍 Internationalization Overhaul
- Migrated to GNU Gettext standard with .mo files.
- Support for 8 languages: ES, EN, FR, DE, PT, IT, RO, RU.

### 🎨 Advanced Theming System
- CSS-based theming engine.
- Automatic dark/light theme detection.


### 🖥️ Complete Drivers Tab Implementation
- Hardware detection (CPU, GPU, RAM, storage, network, VM)
- NVIDIA drivers (Latest + Legacy 470/390/340 via .run files)
- DaVinci Resolve extras (OpenCL/CUDA libraries)
- Blender CUDA toolkit
- Full Dracut configuration (blacklist nouveau, NVIDIA modules, initramfs regeneration)
- AMD drivers (firmware-amd-graphics + Mesa + Vulkan)
- Wi-Fi drivers (Intel/Realtek/Broadcom)
- VM Tools (VMware/QEMU/VirtualBox)
- One-click installation from hardware scan results

### 🔧 Complete Kernels Tab Implementation
- Liquorix kernel with NVIDIA incompatibility detection and blocking
- XanMod kernel variants (x64v3 Standard, x64v4 Advanced, EDGE Experimental, LTS Long-term)
- CPU Microcode updates (Intel and AMD with automatic vendor detection)
- System maintenance tools (Clean old kernels, Update GRUB)
- Clear variant descriptions with CPU compatibility information
- NVIDIA compatibility warnings and safety checks

### ✨ Recommended Tab Complete Overhaul
- **Search and Filter**: Real-time search functionality to quickly find applications
  - Search bar positioned in header for instant access
  - Filters applications by name and description as you type
  - Displays "No results found" message when search yields no matches
  - Search state persists across mode switches (normal ↔ batch)
- **Batch Installation Mode**: New "Selección Múltiple" mode allows selecting and installing multiple packages simultaneously
  - Toggle between normal (individual buttons) and batch (checkboxes) modes
  - "Seleccionar Todos" button selects all visible uninstalled packages (respects search filter)
  - "Deseleccionar Todos" button clears all selections instantly
  - Smart grouping: APT packages installed in single command, Flatpak/deb/custom scripts sequential
  - Bottom action bar with selection counter and batch install button
  - Selection state persists during UI refresh operations
  - Full support for custom scripts (Google Antigravity, Brave, Zed, Sublime Text, etc.)
  - Only DaVinci Resolve excluded due to complex multi-step installation
- **Custom Script Support**: Complex installation workflows with repository setup, GPG keys, and multi-step installations
- **Global Progress Bar Integration**: Unified progress reporting across all installation methods
- **Enhanced Error Handling**: Robust error recovery with proper UI state management
- **Installation Methods**: Full support for APT, Flatpak, .deb URLs, and custom installation scripts
- **UI Stability Fixes**: 
  - Resolved UI freezing during package operations
  - Fixed deformation issues during installation
  - Improved cache invalidation and status updates
- **Software Ecosystem Updates**:
  - **DaVinci Resolve**: Added professional video editor with optimized custom installation workflow:
    - Sequential installation process (dependencies → extraction → conversion → installation)
    - Performance optimization: Reduced package build time from ~45 minutes to ~5-10 minutes using faster gzip compression (level 1)
    - Fixed .deb installation using `dpkg -i` instead of `apt-get install` for local packages
    - Added automatic dependency resolution with `apt-get install -f`
    - Enhanced error handling in CommandRunner to prevent UI crashes during progress updates
    - Comprehensive file-based debug logging (`~/soplos_davinci_debug.log`)
    - Script by Daniel Tufvesson with Soplos optimizations
  - **RapidRAW**: Replaced RawTherapee with modern RAW photo editor (via .deb from GitHub releases)
  - **Google Antigravity**: Replaced Geany with advanced IDE (custom repository + GPG key installation)
  - **Midori**: Replaced Epiphany with lightweight browser (.deb installation)
  - **Snap Removal**: Removed Snap support from Recommended software to prioritize native and Flatpak packages
  - **Gaming Features**:
  - **System Optimizations**: GameMode installation, CPU performance mode script with power-profiles-daemon, gaming sysctl profile
  - **Performance Mode**: Fully implemented with automatic power-profiles-daemon installation and configuration
  - **GPU Optimization**: Automatic GPU vendor detection (NVIDIA/AMD/Intel) with environment configuration files for optimal gaming drivers
  - **Disk I/O Optimization**: Udev rules implementation for optimal disk schedulers (mq-deadline for SSD, none for NVMe, BFQ for HDD)
  - **Performance Monitoring**: MangoHud + Goverlay integration for FPS overlay
  - **Game Launchers**: Full installation/uninstallation support for 13 gaming platforms:
    - **Steam (Flatpak)**: Digital game distribution platform
    - **Lutris (APT/Flatpak)**: Unified game manager for Linux with official repository package badge
    - **Heroic Games Launcher (Flatpak)**: Launcher for Epic Games, GOG, and Amazon Games
    - **Bottles (Flatpak)**: Run Windows applications using Wine with intuitive prefix management
    - **Vinegar (Flatpak)**: Modern Roblox launcher for Linux
    - **R2ModMan (Flatpak)**: Mod manager for games like Lethal Company, Valheim, Risk of Rain 2
    - **Prism Launcher (Flatpak)**: Custom Minecraft launcher with mod support
    - **Itch.io (Flatpak)**: Indie game marketplace and distribution platform
    - **Minigalaxy (APT/Flatpak)**: Simple GOG.com client with official repository package badge
    - **RetroArch (APT/Flatpak)**: Multi-system emulator frontend with official repository package badge
    - **Moonlight (Flatpak)**: NVIDIA GameStream and Sunshine streaming client
    - **Chiaki (Flatpak)**: PlayStation Remote Play client with PS4/PS5 HDR support
    - **Discord (Flatpak)**: Gaming community communication platform
  - **Installation Method Badges**: Visual indicators (Flatpak badge) to show package installation source
  - **Official Package Badges**: Security shield icon for packages from official Debian repositories
  - **RGB Gaming Theme**: Toggle-able gaming theme with black background and red neon accents:
    - Applies instantly without requiring application restart
    - Modern gaming aesthetic with glowing effects
    - One-click activation/deactivation from Gaming tab
  - **Gaming Wallpapers**: Automatic installation with GNOME XML registry support for seamless integration
  - **Revert Functionality**: One-click rollback of all gaming optimizations
  - **Custom Icons**: Vibrant gaming-themed icons for better visual identity
- **UI Enhancements**:
  - **Category Icons**: Updated Development category icon to VS Code, Gaming category icon to Steam
  - Improved category icon loading with configurable support
- **System Integration**:
  - **Icon Fixes**: Corrected application icon visibility by renaming assets to match App ID (`org.soplos.welcome`)
  - **Desktop Entry**: Added proper `.desktop` file for system integration

### 🔒 Security Tab Implementation
- **System Backups**: Integration with Timeshift and Deja Dup.
- **Firewall Management**: GUFW integration and real-time UFW status monitoring.
- **Filesystem Tools**: BTRFS Assistant detection and management.
- **Antivirus & Security**: ClamTk and rkhunter integration.
- **One-Click Actions**: Configure, Activate, Update, and Scan buttons.

### 🎨 Customization Tab Implementation
- **Universal Desktop Support**: Native customization for XFCE, GNOME, and Plasma.
- **XFCE Integration**: 
  - 4 Soplos Tools: Theme Manager, Docklike, GRUB Editor, Plymouth Manager.
  - 7 Native Settings: Appearance, Desktop, Window Manager, Keyboard, Mouse, Notifications, Settings Editor.
- **GNOME Integration**:
  - Soplos Tools: GRUB Editor, Plymouth Manager.
  - Native Settings: Control Center, Tweaks, Extensions, dconf Editor.
- **Plasma Integration**:
  - Soplos Tools: GRUB Editor, Plymouth Manager.
  - Native Settings: Look and Feel, Login Screen, Plymouth, System Settings (via .desktop files).
- **Smart Features**: Automatic DE detection, visual descriptions, debounce protection.

### 🛠️ Fixed
- **CRITICAL: GPU Detection Fix**: Resolved false positive AMD detection caused by 'compatible' string matching. Now correctly identifies NVIDIA, Intel, and VMware SVGA adapters using regex word boundaries.
- **Gaming Tab Dialog Messages**: Fixed dialog messages showing literal `\n` instead of line breaks by correcting double-escaped newlines (`\\n` → `\n`) in 8 locations
- **Gaming Tab GPU Detection**: Improved GPU detection to avoid false AMD detection in VMs (Red Hat VirtIO), now uses word-boundary checks for ATI matching
- **Gaming Tab 32-bit Packages**: Removed `:i386` package dependencies (GameMode and MangoHud) to support 64-bit only systems
- **Gaming Tab Single Password**: All optimization operations now use single `pkexec bash -c` call (Performance Mode, Gaming Sysctl, Disk I/O, GPU, Revert All)
- **Gaming Tab Revert All**: Complete revert functionality now removes sysctl, GPU environment vars, Disk I/O rules, and Performance Mode script
- **KDE Plasma Icon**: Resolved application icon display issue in KDE Plasma with proper WM_CLASS and .desktop file association.
- **Welcome Tab Autostart**: Fixed .desktop file creation and dynamic path resolution for autostart functionality.
- **Flatpak Installation**: Corrected Flathub repository setup and package installation in Tyson variant, ensuring user-level installations work without password prompts.
- **Recommends Tab UI**: Improved button alignment consistency by enforcing minimum height for description labels, eliminating visual inconsistencies.
- **Security Tab - UFW Firewall**: Fixed status detection by reading `/etc/ufw/ufw.conf` directly, simplified activation to single `pkexec` call, added `--force` flag to prevent interactive prompts, enabled systemd service persistence, added periodic status check (every 3s) to detect external changes from GUFW
- **Security Tab - BTRFS Detection**: Fixed filesystem detection using `findmnt` instead of incompatible `df` flags, now correctly detects BTRFS with Calamares subvolumes (@, @home)
- **Window Deformation**: Fixed progress label stretching during downloads by adding text ellipsization and width limits
- **Gaming Tab**: Fixed wallpaper installation progress bar (now shows progress during extraction)
- **Gaming Tab**: Added toggle functionality for Performance Mode (install/uninstall)
- **Gaming Tab**: Safety update - Removed wallpaper uninstallation to protect system files
- **Gaming Tab**: Updated "Revert All" dialog to accurately reflect implemented optimizations (GPU/Disk I/O)
- **Gaming Tab**: Added support for 4 new Flatpak launchers: R2ModMan (Mods), Moonlight (Streaming), Chiaki4deck (PS4/PS5), Vinegar (Roblox)
- **Gaming Tab**: Reordered launchers list for better organization
- Fixed DriversTab initialization
- Fixed Repo Selector button to launch application
- Updated Welcome tab URLs to soplos.org
- **Fixed Batch Installation**: Improved reliability for Chrome, RapidRAW, Midori, and Cursor installations (now use sequential logic with `dpkg -i`).
- **Fixed Clean System**: Consolidated cleanup commands into a single administrator password prompt (GNOME, Plasma, XFCE).
- **Fixed Recommended Tab UI**: Resolved vertical scrollbar overlapping content boxes.
- **Updated Google Antigravity**: Description updated to "Advanced Agentic AI Coding Assistant".
- **Fixed Translations**: Comprehensive cleanup of Spanish dictionary (removed duplicates, fixed fuzzy entries) and added missing gaming wallpaper confirmations.
- **Fixed ClamAV**: Resolved single password prompt issue and added missing translations for update process.
- **Fixed Progress Bar**: Corrected calculation logic to prevent percentage overflow (>100%) during batch installations.
- **Fixed Recommended Tab Scrollbar**: Resolved vertical scrollbar overlapping content boxes by adding right margin (20px) to FlowBox.
- **Complete French Dictionary**: Full revision and completion of French translations (565/565 messages):
  - Synchronized with latest .pot template using msgmerge
  - Added 35+ new translations (GNOME/KDE Settings, Gaming, Security, Recommended sections)
  - Fixed 23 fuzzy translations with incorrect inherited values
  - Corrected syntax error (corrupted X11 msgstr with mixed translation text)
  - Updated header with correct translator info (Sergi Perich)
- **Complete German Dictionary**: Full revision of German translations (565/565 messages):
  - Fixed typo "Dukle" → "Dunkle" (Dark theme)
  - Updated header with correct translator info
- **Complete Italian Dictionary**: Full revision of Italian translations (565/565 messages):
  - Synchronized with latest .pot template using msgmerge
  - Added 35 missing translations (GNOME/KDE Settings, Gaming, Security sections)
  - Removed 23 fuzzy flags with corrected translations
  - Updated header with translator info (Sergi Perich)
- **Complete Portuguese Dictionary**: Full revision of Portuguese translations (565/565 messages):
  - Fixed missing translation ("Symlinks created in:")
  - Fixed typo "PROPÓSITIO" → "PROPÓSITO"
  - Changed "Upgrade" to "Atualizar Sistema" for better localization
  - Updated header with translator info
- **Complete Romanian Dictionary**: Full revision of Romanian translations (565/565 messages):
  - Added 2 missing help text translations
  - Changed "Upgrade" to "Actualizare Sistem"
  - Updated header with translator info
- **Complete Russian Dictionary**: Full revision of Russian translations (565/565 messages):
  - Added 14 missing translations (AI Assistant, GNOME/KDE settings, Gaming messages)
  - Fixed 23 fuzzy translations with correct Russian text
  - Fixed typo "интерфейфейс" → "интерфейс"
  - Changed "Модернизировать" to "Обновить систему" for better localization
  - Updated header with translator info
- **Updated English/Spanish Dictionary Headers**: Corrected Last-Translator and Language-Team metadata.
- **Translation Quality**: All 8 languages (EN, ES, DE, FR, IT, PT, RO, RU) now at 100% with 565 messages each.

## [1.1.4] - 2025-09-08

### 🆕 Added / Fixed
- Updated Blender icon to the requested image.
- Fixed welcome tab link buttons (website, forums, wiki).

## [1.1.3] - 2025-07-28

### 🆕 Added / Improved
- Updated all translation dictionaries.
- Fixed several functions in the hardware detector.
- Updated all program icons.

## [1.1.2] - 2025-07-27

### 🆕 Changed
- Changed program icon to a new design.

## [1.1.1] - 2025-07-27

### 🛠️ Fixed
- Fixed office install/uninstall button logic in the Recommended tab (now works like other categories).
- Fixed hardware detector: now always returns the correct recommended driver for NVIDIA and other hardware.

## [1.1.0] - 2025-07-25

### 🛠️ Fixed
- Fixed Flatpak/Flathub installation bug: Now Flatpak applications can be installed from Flathub without requiring administrator privileges. The Software Center correctly adds Flathub for the current user.

## [1.0.9] - 2025-07-24

### 🛠️ Fixed
- Fixed install buttons in the Software Center (now work correctly).

## [1.0.8] - 2025-07-21

### 🆕 Added / Improved
- Improvements in QEMU/KVM integration and operation for virtual machines.
- Enhanced management and installation of NVIDIA drivers (detection, recommendation, and a more robust installation process).
- **Translation dictionary fragmentation completed:** Interface texts are now organized by language in separate files for Spanish, English, French, Portuguese, German, Italian, Russian, and Romanian.
- **Internationalization:** The program has been fully internationalized to facilitate global collaboration and translation contributions.
- **Recommended Tab:** Improved logic for install/uninstall buttons, now updates state and action dynamically after each operation.
- **LibreWolf:** Installation now uses Flatpak (Flathub) instead of APT or external repositories, avoiding conflicts and simplifying maintenance.

## [1.0.7] - 2025-07-18

### 🛠️ Improved - Metainfo and AppStream/DEP-11 compatibility
- Metainfo updated to comply with AppStream/DEP-11.
- Minor improvements in integration and documentation.
- No functional changes in the application.

## [1.0.6] - 2025-05-20

### 🆕 Added
- Improvements to the Software Center and browser updates.
- Software Center now detects if programs are installed.
- Midori replaced with Epiphany (GNOME Web) as lightweight browser.
- DaVinci Resolve replaced with Shotcut for video editing.
- Driver Center improved with optimized hardware detection.
- Enhanced hardware scanning functionality.

## [1.0.0] - 2025-04-08

### 🎉 Initial Release
- Welcome screen for Soplos Linux.
- Initial system setup.
- Installation of recommended software.
- Desktop customization.
- Access to help and support resources.
- Intuitive and user-friendly interface.
- Support for multiple languages.

---

## Types of Changes

- **Added** for new features
- **Improved** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for removed features
- **Fixed** for bug fixes
- **Security** for vulnerabilities


## Author

Developed and maintained by Sergi Perich  
Website: https://soplos.org  
Contact: info@soploslinux.com

## Contributing

To report bugs or request features:
- **Issues**: https://github.com/SoplosLinux/soplos-welcome/issues
- **Email**: info@soploslinux.com

## Support

- **Documentation**: https://soplos.org
- **Community**: https://soplos.org/forums/
- **Support**: info@soploslinux.com
