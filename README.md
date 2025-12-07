# Soplos Welcome

[![License: GPL-3.0+](https://img.shields.io/badge/License-GPL--3.0%2B-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Version](https://img.shields.io/badge/version-2.0.0-green.svg)]()

A welcome application for Soplos Linux that helps new users get started with their system.

*A welcome application for Soplos Linux that helps new users get started with their system.*

## 📝 Description

Soplos Welcome is a welcome application that guides new users through the initial setup and customization of their Soplos Linux system, providing an easy and friendly experience.

## ✨ Features

- Initial system setup
- **Complete Hardware Detection**: Automatic CPU, GPU, RAM, storage, network, and VM detection
- **Advanced Driver Management**: NVIDIA (Latest + Legacy), AMD, Wi-Fi, VM Tools with one-click installation
- **Kernel Management**: Liquorix, XanMod (x64v3, x64v4, EDGE, LTS) with NVIDIA compatibility checks
- **CPU Microcode Updates**: Intel and AMD firmware security updates
- **System Maintenance**: Clean old kernels, Update GRUB
- **Security Center**: Backups (Timeshift/Deja Dup), Firewall (GUFW), Antivirus (ClamTk), and Filesystem tools
- **Desktop Customization**: Native tools for XFCE, GNOME, and Plasma + Soplos exclusive tools
- Installation of recommended software
- Access to help and support resources
- Intuitive and user-friendly interface
- Support for multiple languages
- **Universal Desktop Support**: GNOME, KDE Plasma, XFCE
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

### v2.0.0 (06/12/2025)
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

### v1.1.4 (08/09/2025)
- Updated Blender icon and fixed link buttons in the welcome tab.

### v1.1.3 (28/07/2025)
- Updated all translation dictionaries.
- Fixed several functions in the hardware detector.
- Updated all program icons.

### v1.1.2 (27/07/2025)
- Changed program icon to a new design.

### v1.1.1 (27/07/2025)
- Fixed office install/uninstall button logic in the Recommended tab.
- Fixed hardware detector.

### v1.1.0 (25/07/2025)
- Fixed Flatpak/Flathub installation bug.

### v1.0.9 (24/07/2025)
- Fixed install buttons in the Software Center.

### v1.0.8 (21/07/2025)
- Improvements in QEMU/KVM integration.
- Enhanced management and installation of NVIDIA drivers.
- Translation dictionary fragmentation completed.
- Full internationalization.

### v1.0.7 (18/07/2025)
- Metainfo update to comply with AppStream/DEP-11.

### v1.0.6 (20/05/2025)
- Internationalization improvements.
- Minor bug fixes.

### v1.0.0 (08/04/2025)
- Initial release.
