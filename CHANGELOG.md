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

### 🛠️ Fixed
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
