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
- Installation of recommended software
- Desktop customization
- Access to help and support resources
- Intuitive and user-friendly interface
- Support for multiple languages
- **Universal Desktop Support**: GNOME, KDE Plasma, XFCE
- **Advanced Architecture**: Modular design with Python and GTK3

## 📸 Screenshots

### Main Welcome Screen
![Main Welcome Screen](https://raw.githubusercontent.com/SoplosLinux/tyron/main/media/soplos-welcome/screenshots/screenshot1.png)

### Initial Setup
![Initial Setup](https://raw.githubusercontent.com/SoplosLinux/tyron/main/media/soplos-welcome/screenshots/screenshot2.png)

### Software Installation
![Software Installation](https://raw.githubusercontent.com/SoplosLinux/tyron/main/media/soplos-welcome/screenshots/screenshot3.png)

### System Configuration
![System Configuration](https://raw.githubusercontent.com/SoplosLinux/tyron/main/media/soplos-welcome/screenshots/screenshot4.png)

### Desktop Customization
![Desktop Customization](https://raw.githubusercontent.com/SoplosLinux/tyron/main/media/soplos-welcome/screenshots/screenshot5.png)

### About Soplos Linux
![About Soplos Linux](https://raw.githubusercontent.com/SoplosLinux/tyron/main/media/soplos-welcome/screenshots/screenshot6.png)

## 🔧 Installation

```bash
# Installation instructions
sudo apt install soplos-welcome
```

## 🌐 Supported Languages

- Spanish
- English
- French
- Portuguese
- German
- Italian
- Russian
- Romanian

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

### v2.0.0 (24/11/2025)
- **Complete Rewrite**: New modular architecture for better maintainability.
- **Universal Support**: Unified codebase for GNOME, KDE, and XFCE.
- **Improved UI**: Modernized interface with better theming support.
- **Enhanced Software Center**: Better integration with native package managers.
- **Driver Management**: Hardware detection and automatic driver recommendations.
- **Kernel Management**: Liquorix and XanMod kernels (4 variants: x64v3, x64v4, EDGE, LTS) with NVIDIA compatibility checks.
- **CPU Microcode**: Intel and AMD firmware security updates.
- **System Maintenance**: Tools to clean old kernels and update GRUB.
- **Fixed Welcome URLs**: Updated all links to point to soplos.org.
- **Fixed Repo Selector**: Button now launches the application instead of attempting installation.

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
