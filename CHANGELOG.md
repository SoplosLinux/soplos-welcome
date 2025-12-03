# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/lang/en/).

## [2.0.0] - 2025-11-30

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
  - **Game Launchers**: Quick installation for Steam, Lutris, Heroic, Bottles, Prism Launcher, RetroArch, Discord
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
- **KDE Plasma Icon**: Resolved application icon display issue in KDE Plasma with proper WM_CLASS and .desktop file association.
- **Welcome Tab Autostart**: Fixed .desktop file creation and dynamic path resolution for autostart functionality.
- **Flatpak Installation**: Corrected Flathub repository setup and package installation in Tyson variant, ensuring user-level installations work without password prompts.
- **Recommends Tab UI**: Improved button alignment consistency by enforcing minimum height for description labels, eliminating visual inconsistencies.
- Fixed DriversTab initialization
- Fixed Repo Selector button to launch application
- Updated Welcome tab URLs to soplos.org

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
