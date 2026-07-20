# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/lang/en/).
 
## [2.1.0-9] - 2026-07-20

### Fixed — Translations

- **Customization Tab (GNOME) — Layout Switcher**: Three strings were missing from all 8 language files — `"Layout Switcher"`, `"Switch between GNOME Shell layout presets"` and `"Launch Soplos Layout Switcher"`. Added translations in en, es, de, fr, it, pt, ro, ru and recompiled all .mo files.

---

## [2.1.0-8] - 2026-07-19

### Added — Customization Tab (GNOME)

- **Layout Switcher**: Added to the Soplos Tools section alongside GRUB Editor and Plymouth Manager. Launches `/usr/bin/soplos-layout-switcher` to switch between GNOME Shell layout presets. Uses the existing install-if-missing flow (`pkexec apt-get install soplos-layout-switcher`) when the package is not present.

---

## [2.1.0-7] - 2026-07-10

### Added — Drivers Tab

- **NVIDIA Extras — CUDA 12 Toolkit**: Installs `cuda-toolkit-12` from the NVIDIA CUDA debian12 repository. Compatible with PyTorch and TensorFlow cu12 builds. Requires an NVIDIA driver already installed. Button reflects install state and supports uninstall with full repository cleanup.
- **NVIDIA Extras — Open Kernel Modules**: Installs `nvidia-kernel-open-dkms` (official open source NVIDIA kernel module, recommended for RTX 30 series and newer). GPU compatibility is verified via `_is_turing_plus()` before proceeding — Maxwell and Pascal GPUs receive an incompatibility error dialog. Supports switching back to the proprietary `nvidia-kernel-dkms` module.
- **NVIDIA 590/610 drivers**: `nvidia-kernel-open-dkms` is now included automatically in the install command for the 590 and 610 branches, which target Turing+ hardware exclusively.
- **Intel Extras section**: New section added between AMD Extras and Wi-Fi. Contains Intel oneAPI Base Toolkit — adds the official Intel oneAPI apt repository (GPG key from `apt.repos.intel.com`) and installs `intel-basekit` (DPC++ compiler, MKL, TBB, VTune, Advisor). Supports full uninstall including repository and keyring removal.
- **Translations**: CUDA 12 Toolkit, Open Kernel Modules and Intel oneAPI strings added to all 8 languages (en, es, de, fr, it, pt, ro, ru).

---

## [2.1.0-6] - 2026-07-08

### Fixed
- **Environment detection — Qt version**: `_detect_qt_version()` in `core/environment.py` added `FileNotFoundError` to the exception catch — previously only `subprocess.SubprocessError` and `subprocess.TimeoutExpired` were handled, so when `qmake` is not installed `subprocess.run` raised `FileNotFoundError` that propagated up through `detect_all()` and crashed the application on startup.

## [2.1.0-5] - 2026-07-07

### Changed
- Build dependency `python3-all` replaced with `python3`.

---

## [2.1.0-4] - 2026-07-06

### Added — Customization Tab

- **LucidGlyph**: New entry in the Soplos Tools section for all three DEs (XFCE, GNOME, KDE). Downloads the latest release tarball from GitHub, extracts it and runs `./lucidglyph.sh install` via pkexec. Uninstall runs `./lucidglyph.sh remove`. Detection via `/usr/local/share/lucidglyph/version` marker file.
- **LucidGlyph — DE-specific post-install**: On GNOME, `gsettings set org.gnome.desktop.interface font-antialiasing grayscale` is applied automatically after install and reset on removal. On KDE, a manual instruction dialog is shown pointing to System Settings - Text and Fonts - Sub-pixel rendering = None.

### Added — Recommended Tab

- **Hardware — amdgpu_top**: Real-time AMD GPU usage monitor. Installs via GitHub latest release `.deb` (dynamic URL via GitHub API).
- **Hardware — nvtop**: GPU process monitor for NVIDIA, AMD and Intel. Installs from official Debian repository.

### Fixed — Recommended Tab

- **FileZilla duplicate**: FileZilla was listed in both Developer and Files categories. Removed from Developer; remains only in Files.

### Translations

- Updated all 8 languages (en, es, de, fr, it, pt, ro, ru) with new strings for LucidGlyph install/uninstall flow, amdgpu_top and nvtop descriptions.

## [2.1.0-3] - 2026-06-30

### Fixed — Drivers Tab

- **Hybrid graphics — $SUDO_USER empty under pkexec**: `_on_hybrid_clicked` used `$SUDO_USER` to resolve the real user's home directory, but pkexec never sets `$SUDO_USER`. The `kwinoutputconfig.json` fix for KDE Plasma was being written to `/root/.config/kdedefaults/` instead of the actual user's home. Replaced with `$PKEXEC_UID` pattern already used by the ROCm scripts.
- **UI freeze on Wi-Fi repair**: `_on_repair_wifi_clicked` called `_detect_wifi_driver()` synchronously in the GTK main thread. On degraded hardware, `lspci -k` can block for several seconds, making the window unresponsive. Detection moved to a background thread via `threading.Thread`; result returned to GTK via `GLib.idle_add`.
- **Race condition on driver install**: Double-clicking the recommended driver install button launched multiple concurrent `pkexec apt install` processes, causing dpkg lock conflicts. Button is now disabled with `set_sensitive(False)` on first click.

### Fixed — Software Tab

- **Flatpak install missing update notifier**: Installing Flatpak pulled in `gnome-software` as a dependency of `gnome-software-plugin-flatpak`, but `package-update-indicator` was not installed. The update tray applet was missing. Added `package-update-indicator` to the Flatpak package list in all three DEs.
- **Bazaar requires system-level Flathub**: Bazaar (`io.github.kolunmi.Bazaar`) only works with Flathub enabled at the system level, but Welcome uses user-level Flathub for all other Flatpak apps. Installing Bazaar via the standard path left it broken. Now shows a warning dialog explaining the conflict and, if confirmed, adds Flathub `--system` and installs Bazaar `--system` via pkexec. Uninstalling Bazaar also removes the system Flathub remote, leaving no residue.

### Changed — Recommended Tab — Software categories reorganized

- **New category: App Management** — Soplos WebApp Manager, Soplos AppImage Manager, Flatseal, Gear Lever, Warehouse.
- **New category: Downloads** — qBittorrent, Transmission, JDownloader, Syncthing Tray.
- **New category: Hardware** — Resources, LACT, CPU Power, CoolerControl.
- **New category: Files** (replaces Utilities) — PeaZip, FileZilla, GNOME Commander, Double Commander (AppImage from OpenSUSE Build Service, latest GTK version).
- **Multimedia reordered**: grouped into Media Players (VLC, MPV, Kodi, Spotify), Video (OBS Studio, Kdenlive, OpenShot, HandBrake, DaVinci Resolve) and Audio/DAW (Audacity, LMMS, Mixxx, Bitwig Studio, Reaper, Zrythm, Ardour).
- **Graphics and Design reordered**: grouped into Image Editing (GIMP, Krita, Affinity Suite), Vector/Design (Inkscape), 3D (Blender) and Photography/RAW (darktable, RapidRAW, RawTherapee, Hugin).
- **Office reordered**: grouped into Office Suites (LibreOffice, OnlyOffice, WPS Office, Calligra, Collabora Office) and PDF (Adobe Reader, JoPDF).
- **Icon folders restructured**: icons moved from `assets/icons/utilities/` to their respective new category folders.

## [2.1.0-2] - 2026-06-29

### Fixed — Drivers Tab — NVIDIA and ROCm

- **DKMS not cleaned on uninstall**: `apt purge` leaves compiled `.ko` files in `/lib/modules/`. When reinstalling a different driver version, DKMS refused with "version not newer". Uninstall script now runs `dkms remove --force` on all NVIDIA entries and removes orphaned `.ko` files from every kernel directory before purging packages.
- **DKMS not cleaned on install**: Same stale DKMS state caused installation failures when switching driver versions. Both the CUDA-repo path (590/610) and the Debian-repo path (550) now perform the same DKMS cleanup before `apt install`.
- **Escaped quotes in 590 and 610 repo setup**: The `rm -rf "$TEMP_DIR"` line inside Python triple-quoted strings generated an extra trailing quote in the bash output (`"$TEMP_DIR""`), corrupting the cleanup command. Fixed by converting those blocks to raw strings (`r"""..."""`).
- **ROCm codename**: The `CODENAME` case statement included `bookworm` as a branch, but Soplos is based on Debian Testing/Trixie moving toward Forky — never Debian 12. Replaced with `trixie` and `forky` cases only.

## [2.1.0-1] - 2026-06-24

### Added — Drivers Tab — AMD Extras (ROCm)

- **ROCm OpenCL**: new section "AMD Extras" with OpenCL runtime for AMD GPUs (RDNA1+). Installs `rocm-opencl-runtime` from the official AMD ROCm 6.4 repository. Adds the user to `render` and `video` groups automatically. For DaVinci Resolve, Blender HIP and general GPU compute.
- **ROCm Full Suite**: full ROCm platform (`rocm`) for AI/ML development with PyTorch and TensorFlow on AMD GPU. Several GB download.
- Both buttons support install/uninstall with checkmark detection via `_driver_buttons`.

### Added — Recommended Tab — Helium browser

- **Helium**: privacy-focused browser built on Chromium with YouTube integration. Installed from the latest GitHub release `.deb` (`imputnet/helium-linux`) via dynamic URL — package `helium-bin`.

### Fixed — Drivers Tab

- **NVIDIA Extras checkmarks**: DaVinci Resolve Extras and Blender CUDA Toolkit buttons now show a checkmark when their packages (`nvidia-opencl-icd`, `nvidia-cuda-toolkit`) are installed. Previously they had no state detection.
- **LACT removed**: LACT GPU Control Center was duplicated in both Drivers and Recommended tabs. Removed from Drivers — it belongs in Recommended only.

### Changed — Drivers Tab — VirtualBox Guest Additions

- **Updated to 7.2.10**: replaced bundled `VBoxLinuxAdditions.run` with the 7.2.10 release.

### Fixed — Assets permissions

- **Normalized to 644/755**: all files under `assets/` set to 644, all directories to 755, `VBoxLinuxAdditions.run` kept at 755.

## [2.1.0] - 2026-06-20

### Added — Drivers Tab — NVIDIA 610

- **NVIDIA 610 (Latest)**: new driver button for Blackwell and newer hardware (RTX 50/60 series). Installed from the official NVIDIA CUDA repository for Debian 13 (`nvidia-driver-pinning-610` + `cuda-drivers-610`). Verified present in the CUDA debian13 repo (`nvidia-driver-pinning-610_610-2`).
- **NVIDIA 590 renamed to Stable**: the 590 button label has been updated from "Latest" to "Stable" to reflect that 610 is now the most recent branch.
- **Grid layout updated**: 610 occupies row 0 col 0, 590 moves to row 0 col 1. All other drivers shift one row down. Uninstall button now spans both columns in row 4.

### Added — Welcome Tab — Gaming Mode link

- **Gaming Mode link on home screen**: a new row below "Customize your desktop" shows the gaming controller icon and a clickable link ("Activate Gaming Mode") that triggers `_toggle_gaming_tab()` — identical to Ctrl+G. The row only renders if the Gaming tab loaded correctly.

## [2.0.9-3] - 2026-06-09

### Fixed — Recommended Tab

- **Brave Origin icon**: moved from `brave-origin-icons/48x48/apps/brave-origin.png` to `brave-origin.png` at the browsers icons root — same flat structure as all other browser icons, avoids packaging issues with nested subdirectories.
- **Affinity Suite reverted to 3.0.2**: the 3.2.0 AppImage switched to Wine 11 and fails on most systems. Reverted to the 3.0.2 AppImage (Wine 10), available at the same release tag (`3.2.0`) of the upstream repo. Updated `check_path`, wget URL, chmod target, and `.desktop` `Exec` entry accordingly.

## [2.0.9-2] - 2026-06-09

### Added — Recommended Tab — New browsers

- **Brave Origin**: privacy-focused browser by Brave with integrated AI assistant. Installed via Brave's official script (`FLAVOR=origin`). Icon patch replaces the bundled orange icon with a black version in all sizes, patching both `/usr/share/icons/hicolor/` and `/opt/brave.com/brave-origin/` (postinst source) to survive updates.
- **Opera**: feature-rich browser with built-in VPN and ad blocker. Installed as Flatpak (`com.opera.Opera`).
- **Zen Browser**: privacy-focused Firefox-based browser with beautiful design. Installed from the latest GitHub release `.deb` via dynamic URL.

### Fixed — Drivers Tab — NVIDIA false positives

- **NVIDIA 550 detection**: `check_fn` now uses `_get_nvidia_active_version() == '550'` instead of `_is_package_installed('nvidia-driver')`. Previously, having any NVIDIA driver installed (e.g. 580) also marked 550 as installed because both share the `nvidia-driver` meta-package.
- **NVIDIA false positives on AMD systems**: the dpkg fallback in `_get_nvidia_active_version()` now only runs when `lspci` detects NVIDIA hardware. On AMD-only systems, leftover NVIDIA packages in dpkg no longer trigger false-positive driver checkmarks.

## [2.0.9-1] - 2026-05-29

### Fixed — App icon in GNOME Software

- **Removed `slide1.png` from `assets/icons/`**: this file was being picked up by the repo manager and packaged as the application icon, causing GNOME Software to display the wrong image instead of the correct `org.soplos.welcome.png` icon.

## [2.0.9] - 2026-05-28

### Changed — Drivers Tab — VirtualBox Guest Additions

- **Updated to VirtualBox Guest Additions 7.2.8**: first release with official Linux 7.0 kernel support. The previous script downloaded the obsolete 7.0.20 ISO from Oracle's servers. The `VBoxLinuxAdditions.run` installer is now bundled directly in the package under `assets/vbox/` — no internet connection required at install time.
- **Compiles `vboxguest`, `vboxsf` and `vboxvideo`** for kernel 7.0.9-soplos via DKMS. The "unable to load vboxguest kernel module" message is expected when the system runs in VMware/QEMU (not in VirtualBox) — the modules load correctly when booted inside VirtualBox.

### Fixed — Pango Markup

- **"Security & System Protection" header**: the `&` character was unescaped in the `en` and `de` `.po` translations, causing a GTK warning (`Error on line 1: Entity did not end with a semicolon`) when the Security tab was created. Fixed by using `&amp;` in the `msgstr` of both locales.

## [2.0.8-9] - 2026-05-27

### Fixed — Recommended Tab

- **Affinity AppImage URL updated to 3.2.0**: the previous URL pointing to 3.0.2 returned HTTP 404, causing `wget` to exit with code 8 and aborting the entire batch install chain due to `set -e`. URL now points to the 3.2.0 release.
- **Affinity `.desktop` file ownership**: `printf '...' > file` under pkexec wrote the file as root. Replaced with `sudo -u $REAL_USER tee` so the file is owned by the real user. Also ensured the parent directory is created with `sudo -u $REAL_USER mkdir -p` before writing.
- **ES-DE `.desktop` file ownership**: same `tee` fix applied — `.desktop` file was being created as root under pkexec.
- **RapidRAW reverted to Flatpak**: a previous session had incorrectly changed RapidRAW from `flatpak install flathub io.github.CyberTimon.RapidRAW` to a Debian `.deb` install. Reverted to Flatpak.
- **Batch install chain failure with `set -e`**: the consolidated batch script used a global `set -e`, so a single failed package (e.g. Affinity 404) would abort all remaining packages in the selection. Each package is now wrapped in its own subshell with `set -e` isolated inside — a failure prints a warning and the script continues with the next package.

### Changed — Kernels Tab

- **Removed NVIDIA/Liquorix warning**: the notice advising against using Liquorix with NVIDIA has been removed from the tab.
- **Soplos Kernel Installer repositioned**: moved from after XanMod to between Microcodes and the Available Kernels section (below Liquorix was before).
- **Soplos Kernel Installer icon added**: the section now displays the application icon (`org.soplos.kernel-installer.png`) with the same layout as packages in the Recommended tab — icon on the left, bold name and description stacked to the right, action buttons at the end of the row.

## [2.0.8-8] - 2026-05-26

### Fixed — DaVinci GPU Patch

- **Fixed permission error in `davinci-gpu-patch.sh`**: the `mkdir -p ~/.local/share/applications/` call was running as root (via pkexec), causing that directory to be owned by root. Subsequent writes from Soplos WebApp Manager and Soplos AppImage Manager failed with `PermissionError: [Errno 13]`. The command now uses `sudo -u "$REAL_USER"` to create the directory with the correct ownership.

### Fixed — Lutris Vulkan Patch

- **Fixed Lutris Vulkan fix targeting wrong deployment**: `lutris-vulkan-patch.sh` used a plain `find` that could pick up `gpu.py` from an old Flatpak deployment instead of the active one. After a Flatpak update, the new deployment had the unpatched file and Lutris kept sending a GPU/vulkaninfo error notification repeatedly. The script now searches under the `active` symlink (`x86_64/stable/active`) with `-L` to follow symlinks, with a fallback that searches any `*/active/*` path for non-standard architectures or branches.

## [2.0.8-7] - 2026-05-25

### 🎬 Recommended Tab — DaVinci Resolve

- **Updated MakeResolveDeb to 1.10.0** (release 2026-05-15 by Daniel Tufvesson): adds split `-data` package for DaVinci Resolve 21+ (plugins folder separated into `davinci-resolve-data` package). Drops slow `xz -9` compression in favour of default gzip — significantly faster build.
- **Install step now handles two `.deb` files**: for Resolve 21+ MakeResolveDeb generates a main package and a `-data` package; both are now installed in sequence automatically.

### 🎨 Recommended Tab — Icons

- **Calligra**: updated icon.

## [2.0.8-6] - 2026-05-24

### 🔧 Drivers Tab — Wi-Fi Repair Detection Improved

- **Triple detection strategy**: (1) sysfs `/sys/class/net/*/wireless` — works when interface is active; (2) `iw dev` — works when interface is down but module is loaded; (3) `lspci -k` — works when the module is not loaded at all, which is the exact case of broken WiFi after reboot (module loads but fails to find firmware → circular dependency). Now the button can always identify the driver and repair WiFi regardless of the system state.

## [2.0.8-5] - 2026-05-23

### 🔧 Drivers Tab — Wi-Fi Repair

- **Added "Repair Wi-Fi" button**: Automatically detects the active Wi-Fi driver by reading `/sys/class/net/*/wireless` (no external commands needed). Shows a confirmation dialog with the detected driver and interface name. On confirmation runs `modprobe -r <driver>`, waits 1 second, `modprobe <driver>` and `systemctl restart NetworkManager`. Works with any brand — Intel (`iwlwifi`), Realtek, Atheros, MediaTek, Broadcom, etc. If no Wi-Fi interface is found, shows a warning dialog instead.

### 🌍 Translations

- Added Wi-Fi Repair strings (button label, tooltip, dialogs) in all 8 languages.

## [2.0.8-4] - 2026-05-22

### 🖥️ Drivers Tab — Detection Fixes

- **Fixed false "installed" state on Nouveau button**: now checks `/etc/modprobe.d/*.conf` for `blacklist nouveau` — if blacklisted the button correctly shows as not active, even though the package is present on the system.
- **Fixed false "installed" state on AMD button**: now requires all three packages (`firmware-amd-graphics`, `mesa-vulkan-drivers`, `xserver-xorg-video-all`) to be installed simultaneously, instead of just one.
- **Fixed false "installed" state on Wi-Fi Intel/Realtek buttons**: now combines package presence with `lsmod` module check, so the button only shows as installed when the firmware package is present AND the corresponding kernel module is actually loaded.

### 📦 Recommended Tab — Utilities

- **Added Syncthing Tray** (`io.github.martchus.syncthingtray`): tray application for Syncthing — sync files between devices. Available as Flatpak from Flathub.

### 🌍 Translations

- Added Syncthing Tray description string in all 8 languages.

## [2.0.8-3] - 2026-05-18

### 🎮 Gaming Tab — Optimizations

- **Added RyzenAdj** to the Optimizations section: compiles from source, installs the binary and shared library, and creates a systemd service that applies AMD thermal limits (`--tctl-temp=85`, `--stapm-limit=35000`, `--fast-limit=35000`, `--slow-limit=35000`) at boot. Ideal for AMD mini PCs with proprietary EC firmware that blocks NBFC-based tools.
- **Added Lutris Vulkan Fix** button to the Optimizations section: patches `gpu.py` inside the Lutris Flatpak sandbox to use `/app/bin/vulkaninfo` instead of the broken `/usr/bin/vulkaninfo` path. Replaces the unreliable automatic post-install hook — must be run manually after Lutris has been launched at least once.
- **Removed Ryzen Master Commander**: eliminated from the Optimizations section as it requires NBFC for fan control, which is incompatible with the proprietary EC firmware on AMD mini PCs.
- **Removed Lutris Vulkan patch from post_install_script**: the automatic patch after Lutris install was unreliable (Flatpak sandbox not yet initialised at that point); replaced by the manual button above.

### 🔧 Fixes

- **Ctrl+Shift+Tab**: backward tab navigation was silently ignored because GTK sends `KEY_ISO_Left_Tab` for that combination, not `KEY_Tab`. The key handler now checks for `KEY_ISO_Left_Tab` explicitly and navigates to the previous tab correctly.

### 🌍 Translations

- Added strings for RyzenAdj (install/uninstall labels, description, confirmation dialogs) in all 8 languages.
- Added strings for Lutris Vulkan Fix (label, description, warning dialog) in all 8 languages.

## [2.0.8-2] - 2026-04-30

### 🛍️ Software Tab — Snap Store & Bazaar

- **Added Snap Store and Bazaar to all three DEs** (XFCE, GNOME, KDE/Plasma): The software grid is now 4 columns × 2 rows. Snap Store (`snap:snap-store`) and Bazaar (`flatpak:io.github.kolunmi.Bazaar`) occupy the new column.
- **Dependency check dialog**: If the user clicks Snap Store without `snapd` installed, or Bazaar without `flatpak` installed, a warning dialog offers to install the missing runtime first.
- **Fixed: buttons now correctly show "Uninstall" state** for Snap and Flatpak apps: `snap install/remove` now uses `pkexec` (was failing silently as a regular user, leaving the button stuck on "Install"). The post-operation callback no longer leaks a `GLib.idle_add` loop by returning the timer source ID.
- **Fixed: program no longer hangs after installing Bazaar**: `flatpak install` now uses `--user --noninteractive` flags, which avoids prompting for interactive confirmation and eliminates the need for `pkexec`.

### 🔒 Security Tab — VPN

- **Added Surfshark** (`com.surfshark.Surfshark`) and **Mozilla VPN** (`org.mozilla.vpn`) to the VPN section as Flatpak apps. Both include Install/Uninstall/Open buttons with state detection.

### 🎮 Gaming Tab — Optimizations

- **Added CPU Power** tool to the Optimizations section: installs `linux-cpupower` and `cpupower-gui` via `pkexec apt`, allowing control of the CPU frequency governor (powersave, performance, etc.) from a graphical interface.

### 📦 Recommended Tab — Office

- **Added Calligra** (`org.kde.calligra`) and **Collabora Office** (`org.collaboraoffice.CollaboraOffice`) as Flatpak entries in the Office section. Both support multi-selection batch install.

### 🖥️ Footer

- **Removed "Ready/Listo" status text**: The footer now shows only the desktop environment and display protocol, without the translated "Ready" prefix.

### 🎨 Customization Tab

- **Docklike removed from XFCE**: The Docklike launcher has been removed from the XFCE tools since its functionality is now completely integrated into Soplos Theme Manager.

## [2.0.8-1] - 2026-04-04

### 🎮 Hybrid Graphics — Fixes

- **Fixed NVIDIA Primary mode not booting**: The "NVIDIA Primary" script was regenerating the initramfs without first creating the dracut configuration files (`/etc/dracut.conf.d/nvidia.conf`, `blacklist-nouveau.conf`). This caused the system to boot without NVIDIA modules loaded, resulting in a black screen or failed boot on laptops. Now creates the dracut configs before calling `dracut --force`, consistent with the repository install script.
- **PRIME Render Offload — KDE Plasma fix**: On KDE Plasma systems with Optimus hybrid graphics, KWin could lose the wallpaper and desktop icons after each reboot due to not correctly identifying the laptop screen connector. The PRIME Offload script now detects the Intel display connector dynamically from `/sys/class/drm/` (`eDP` or `LVDS`) and generates `~/.config/kdedefaults/kwinoutputconfig.json` with the correct output priority, leaving resolution, refresh rate and scale for KWin to fill in. Only runs on KDE Plasma (detected via `EnvironmentDetector` at launch, not by scanning binaries at runtime).



### 🎬 DaVinci Resolve — Script Update & Optional Patches

- **MakeResolveDeb updated to 1.9.0** (by Daniel Tufvesson, 2026-04-14): Adds full support for DaVinci Resolve 21 with its own `process_21()` function. In version 21, the `Apple Immersive` folder is copied from the installer if present instead of always being created empty. Package compression changed from gzip level 1 to xz level 9 for smaller output.
- **Virtual microphone patch**: New optional post-install patch that creates a PipeWire virtual microphone so DaVinci Resolve can start on systems without a physical audio capture device. The patch auto-detects whether a real capture device is present and skips itself if one is found.
- **Integrated GPU patch (AMD / Intel iGPU)**: New optional post-install patch for mini PCs and systems with integrated graphics. Installs the appropriate OpenCL stack (Mesa Rusticl for AMD, Intel NEO for Intel), downloads i915 firmware for ADL-N/N-series chips if missing, injects a libProResRAW stub to prevent Signal 11 crashes, patches the `.desktop` launcher with the correct environment variables, and adds the user to the `render` and `video` groups.
- **Post-install patches dialog**: After successfully installing DaVinci Resolve, a new dialog offers both patches as optional checkboxes ("Skip" / "Apply Selected"). Selecting none goes straight to cleanup. When both are selected, the mic patch runs first, then the GPU patch, then cleanup.

### 🔧 Drivers Tab — Fixes & Full Rework

- **Fixed crash on startup**: `self._driver_buttons` dict was never initialized and `subprocess` was not imported at module level, causing `AttributeError` and `NameError` on load.
- **Install/Uninstall toggle**: All 15 driver buttons (NVIDIA 590/580/550/470/390/340, Nouveau, AMD, Wi-Fi Intel/Realtek/Broadcom, Printers, Bluetooth, VMware/QEMU/VirtualBox) now show `✓ name` when the driver is installed and act as uninstall on click, or as install when not present — consistent with the Gaming and Recommended tabs.
- **NVIDIA 590 and 580 buttons**: Were created but never stored in `_driver_buttons`, so their state was never reflected. Now fully registered.
- **Auto-refresh after operations**: `_refresh_driver_status` is called on startup and as a callback after every install/uninstall, keeping all buttons in sync.

### 🔍 Hardware Scanner — Fixes & Full Rework

- **Fixed broken GPU section**: Dialog was using `results['gpu']` (old single-GPU key) instead of `results['gpus']` (list). On systems with no GPU entry under that key the section was silently skipped.
- **All hardware sections now shown**: GPU(s), Hybrid Graphics, Wi-Fi adapters, Audio, Bluetooth, Printers, VM Tools — each with their detected model, driver status (✓ installed / ✗ missing / ⚠ partial) and Install/Uninstall button.
- **VM Tools detection**: If running inside VMware, VirtualBox or QEMU/KVM, the scanner now detects it, shows whether the guest tools are installed, and offers to install or uninstall them directly.

### ➕ New Applications
- **ProtonVPN** (`com.protonvpn.www`): Added to Security tab in a new VPN section, with Install/Uninstall toggle.
- **ClamUI** (`io.github.linx_systems.ClamUI`): Added to Security tab in the antivirus section alongside ClamTk.
- **LACT** (`io.github.ilya_zlobintsev.LACT`): Added to Drivers tab in the AMD section for GPU overclocking and monitoring.
- **Resources** (`net.nokyan.Resources`): Added to Recommended tab in the utilities section as a modern system monitor.
- **Soplos Kernel Installer** (`soplos-kernel-installer`): Added to Kernels tab with Install/Uninstall toggle and Open button.
- **Portmaster**: Added to Security tab (Firewall section) as a privacy-focused packet filter. Downloads the official `portmaster-installer.deb` with no hardcoded version.
- **JoPDF**: Added to Recommended tab (Ofimática section) as a PDF editor. Downloads `jopdf-linux-amd64_setup.deb` directly from the official site.
- **qBittorrent** (`org.qbittorrent.qBittorrent`): Added to Recommended tab (Utilities section) via Flatpak.
- **JDownloader** (`org.jdownloader.JDownloader`): Added to Recommended tab (Utilities section) via Flatpak.
- **PPSSPP** (`org.ppsspp.PPSSPP`): Added to Recommended (Gaming section) and Gaming tab launchers via Flatpak. Includes a post-install script that creates a symlink to the Flatpak binary as the Lutris runner, making PSP games playable directly from Lutris.
- **LACT** (`io.github.ilya_zlobintsev.LACT`): Also added to Recommended tab (Utilities section) via Flatpak.
- **CoolerControl**: Added to Recommended tab (Utilities section) as an AppImage that runs as root (fan/cooling daemon) plus a WebApp shortcut pointing to `http://localhost:11987/`.

### 🎮 Gaming Tab — MangoHud Rework
- **MangoHud** now installs via Flatpak instead of system packages. Six packages are installed: `MangoHud`, `GOverlay`, `VulkanInfo`, `vkBasalt`, `gamescope`, and `DXVK`.

### 🔧 Post-Install Script System
- **Lutris Vulkan patch**: After installing Lutris (Flatpak) from Recommended or Gaming tab, `lutris-vulkan-patch.sh` runs automatically and patches `gpu.py` inside the Flatpak to use `/app/bin/vulkaninfo` instead of the broken `/usr/bin/vulkaninfo` path.
- **PPSSPP Lutris runner**: After installing PPSSPP Flatpak, `ppsspp-lutris-runner.sh` runs automatically. It backs up any existing `PPSSPPSDL` binary in Lutris' runner directory and creates a symlink to the PPSSPP Flatpak binary.
- **General post-install hook**: Both `recommended_tab.py` and `gaming_tab.py` now support a `post_install_script` key in any package dict. After a successful install, the named script (from `services/`) is executed as the current user.

### 🛡️ Security Tab — Icons & Layout
- **Icons added to all 14 tools**: Timeshift, Grub BTRFS, Deja Dup, BTRFS Assistant, GUFW, Portmaster, Proton VPN, BleachBit, Stacer, Sweeper, Soplos Sys Cleaner, ClamTk, ClamUI and rkhunter now show a 48 px icon from `assets/icons/security/`.
- **Same row layout as Gaming/Recommended**: Each tool's icon is now centred vertically next to both the name and the description, matching the visual style of the other tabs.
- **Open Portmaster button**: When Portmaster is installed an "Open Portmaster" button launches the app via `gtk-launch portmaster` with a `/opt/safing/portmaster/portmaster` fallback.
- **UFW conflict warning**: When Portmaster is installed and UFW is active, an orange warning label recommends disabling UFW to avoid rule conflicts.

### 🎮 Gaming Tab — GeForce NOW, Badges & Tooltips
- **GeForce NOW WebApp launcher**: New launcher that installs a Soplos WebApp Manager `.desktop` entry pointing to `https://play.geforcenow.com/` using the system's Chromium/Brave/Firefox (auto-detected).
- **Flatpak / AppImage / WebApp badges**: All launcher widgets now display a small badge indicating the installation method.
- **Optimization button tooltips**: All 7 optimization buttons in the Gaming tab now show a tooltip on hover explaining what each option does.
- **MangoHud Flatpak package IDs corrected**: Fixed to the exact IDs required — `io.github.benjamimgois.goverlay`, `org.freedesktop.Platform.VulkanLayer.MangoHud`, `org.freedesktop.Platform.VulkanInfo`, `org.freedesktop.Platform.VulkanLayer.gamescope`, `org.winehq.Wine.DLLs.dxvk`, `org.freedesktop.Platform.VulkanLayer.vkBasalt`.

### 💻 Software Tab (XFCE)
- **GNOME Software**: Now also installs `gnome-packagekit` so that the XFCE panel update indicator can actually apply updates when clicked.

### 🌍 Translations
- Added `"Complete installation"` string in all 8 languages (ES, EN, FR, DE, PT, IT, RO, RU).
- Added translations for new apps (ProtonVPN, ClamUI, LACT, Resources) in all 8 languages.
- Added translations for PPSSPP, LACT (utilities), CoolerControl, and updated Drivers tab subtitle in all 8 languages.
- Added missing translations for all Security tab tool descriptions, driver status labels (Audio, Not installed, Driver installed, Hybrid Graphics, Partially installed, Different version installed), kernel AVX2 description, and app descriptions (JDownloader, qBittorrent, JoPDF) in all 8 languages.

## [2.0.8] - 2026-03-31

### ✨ Customization Tab
- **Install dialog for Soplos tools**: Buttons for Soplos tools (Soplos Theme Manager, Soplos Docklike, etc.) now detect whether the tool is installed. If not, they show a confirmation dialog inviting the user to install it via `pkexec apt-get install`, and auto-launch the tool on success.

### ⭐ Recommended Tab
- Added 6 new Flatpak applications: **Bitwig Studio**, **Reaper**, **Zrythm**, **Ardour** (Multimedia), **Warehouse** (Flatpak manager), **PeaZip** (archive manager).

### ⌨️ Keyboard Navigation
- **Ctrl+Shift+Tab**: Navigate to previous tab (backward navigation now works).
- **F1**: Opens the About dialog, consistent with all other Soplos applications.

### 🎨 UI Fixes
- **About dialog**: Fixed dark strip between content and action area in both dark and light themes.
- **Welcome tab**: Added Security to the features list (was missing). Fixed icon order to match tab order. Updated tab icons to match the feature list icons.
- **Drivers tab**: Removed emojis from Frame labels (Processor, Graphics Card, Hybrid Graphics, RAM Memory, Virtual Machine) for better font compatibility.

### 🔧 Code Audit
- Removed unused demo code (`_add_software_demo_buttons`, `_on_demo_install`, `_on_demo_uninstall` and related methods) from `main_window.py`.
- Fixed deprecated `get_action_area()` call in `drivers_tab.py` (replaced with manual button box in `get_content_area()`).
- Fixed duplicate imports in `welcome_tab.py`.
- Removed "coming soon" placeholder text from tab fallback view.
- Unified version string to 2.0.8 across all modules.

### 🌍 Translations
- Added `• Manage system security` string in all 8 languages (ES, EN, FR, DE, PT, IT, RO, RU).
- Added install flow strings for Soplos tools dialog in all 8 languages.
- Added descriptions for 6 new Recommended apps in all 8 languages.

## [2.0.7-3] - 2026-03-24

### 🚀 NVIDIA 580 Driver Fix
- **SHA1/sqv workaround**: Replaced cuda-keyring with `[trusted=yes]` in sources.list for the debian12 CUDA repo, bypassing `sqv` rejection of SHA1 key binding signatures on Debian 13.
- **Version pinning**: Added `nvidia-driver-pinning-580` installation step to force apt to resolve the 580 branch instead of the latest (595+).
- **Downgrade support**: Added `--allow-downgrades` flag to handle packages already at a newer version (e.g. `firmware-nvidia-gsp`, `libxnvctrl0`).
- **Uninstall cleanup**: `_on_uninstall_nvidia_clicked` now also removes `99nvidia-sha1-exception` leftover file.

### 🔧 Hardware Detection Improvements
- **GTX 16xx / MX550/MX450**: Correctly mapped to `nvidia-driver-590` (CUDA repo, debian13).
- **Maxwell GPUs** (GTX 9xx, 8xx, 9xxM): Correctly mapped to `nvidia-driver-580` (CUDA repo, debian12).
- **lspci caching**: Added `_get_lspci_output()` helper; `scan_hardware` now calls lspci once and passes the result to both `detect_gpu` and `detect_hybrid_gpu`.

### 🛡️ Security Tab
- **Soplos Sys Cleaner**: Added to the Cleaning section with install/uninstall and "Open" button.

### ⭐ Recommended Tab
- **Soplos AppImage Manager**: Added to the Utilities category.
- **OBS Studio** and **HandBrake**: Switched to Flatpak installation (apt versions cause dependency issues on Debian 13).
- **Lutris**: Switched to Flatpak in both Recommended and Gaming tabs.
- **AppImage badge**: Packages installed as AppImage now display an AppImage badge alongside their name.
- **Official badge**: Now only shown when the install method is APT (not Flatpak or AppImage).

### 🌍 Translations
- Updated all 8 languages (ES, EN, FR, DE, PT, IT, RO, RU) with 4 new strings: Soplos AppImage Manager description, AppImage badge, Soplos Sys Cleaner description, and "Open Soplos Sys Cleaner" button.

## [2.0.7-2] - 2026-03-13

### 🚀 NVIDIA Driver Fixes
- **Hardware Detection**: Corrected mapping for GeForce 650M/750M (Kepler MacBooks) to use driver 470 instead of nouveau.
- **MX/GT Series**: Improved detection patterns for MX and legacy GT series GPUs.
- **Installation Workflow**:
  - Added mandatory confirmation dialogs before starting driver installation.
  - Implemented automatic `apt purge` of existing NVIDIA drivers to prevent conflicts.
  - Ensured explicit installation of `nvidia-smi`, `nvidia-settings`, `nvidia-modprobe`, and `libglu1-mesa`.
  - Added fallback support for `update-initramfs` when `dracut` is not available.

### 🌍 Translations
- Updated all 8 supported languages (ES, EN, FR, DE, PT, IT, RO, RU) with new confirmation dialog strings.

## [2.0.7-1] - 2026-03-12


### 🚀 NVIDIA Driver Improvements
- **Official Repository Logic**: Refactored official NVIDIA repository installation logic to follow official documentation.
- **Keyring Handling**: Uses the official `cuda-keyring` package to manage repositories and GPG keys, resolving issues with empty GPG files.
- **Robustness**: Improved the installation script for Debian 12 (driver 580) and 13 (driver 590) with better fallback logic and error handling.

## [2.0.7] - 2026-03-11

### 🔧 NVIDIA Legacy Drivers Overhaul
- **APT-based Legacy Installation**: Legacy NVIDIA drivers (340, 390, 470) are now installed via APT from Debian Sid instead of `.run` files, for cleaner integration and fewer dependency conflicts.
- **Debian Sid Workflow**: New two-step dialog guides users to temporarily enable Debian Sid (Unstable) via **Soplos Repo Selector** before installing legacy drivers, with clear warnings to disable Sid afterwards.
- **Automatic Repo Selector Launch**: Clicking a legacy driver button now opens Soplos Repo Selector automatically and waits for the user to finish before proceeding with the installation.
- **Correct APT Package Names**: Updated hardware detector to use `nvidia-legacy-340xx-driver`, `nvidia-legacy-390xx-driver`, and `nvidia-tesla-470-driver` from Debian Sid.

### 🌍 Translations
- Added 4 new translation strings for the legacy driver dialogs in all 8 languages (ES, EN, FR, DE, PT, IT, RO, RU).

## [2.0.6-3] - 2026-03-08

### 🛠️ Bug Fixes
- **AppImages**: Fixed `Errno 13 Permission denied` when creating web apps by installing all AppImages (Affinity Suite, ES-DE, Stacer) to `~/AppImage` instead of `/opt`, and removing the use of `pkexec` to prevent root ownership of user directories.

## [2.0.6-2] - 2026-03-07

### 🛠️ Bug Fixes
- **Gaming Tab**: Fixed an issue where installing gaming wallpapers on GNOME (Boro) would duplicate existing Soplos wallpapers in the background settings.

## [2.0.6] - 2026-03-04
 
### 🆕 Added
- **Recommended Tab**: New "Utilities" section featuring Soplos WebApp Manager, Flatseal, and Gear Lever.
- **Gaming Tab**: Added ProtonUp-Qt to the launchers list for managing GE-Proton and Wine versions.
 
### 🔧 Kernels Tab Fixes
- **Clean Old Kernels**: Fixed critical logic bug where older kernels were sometimes kept instead of newer ones due to lexicographical sorting.
  - Implemented version-aware sorting (`sort -V`) for accurate identification of the latest kernels.
  - Enhanced preservation logic: now keeps the running kernel PLUS the latest version of each branch (Main, Liquorix, XanMod).
  - Deep cleaning: Switched to `apt purge` to remove configuration files and stale modules.
  - Automatic header cleanup: Matching `linux-headers-*` packages are now purged alongside images.
 
## [2.0.5] - 2026-03-02

### 🛠️ Bug Fixes
- **Recommended Tab**: Fixed logic bug in batch installation mode ("Selección Múltiple") that caused custom script applications (like ES-DE and Affinity Suite) to collide and fail during selection or removal.

## [2.0.4] - 2026-02-24

### 🎮 Gaming Tab Enhancements
- **Sober (Roblox)**: Added Sober launcher to Gaming tab (successor to Vinegar)
- **EmulationStation-DE**: Added as AppImage in both Gaming tab and Recommended tab
- **Internationalized Launchers**: All 14 launcher descriptions now use `_()` instead of hardcoded Spanish strings, with translations in all 8 languages
- **Launcher Alignment Fix**: Fixed visual alignment of launcher entries with uniform height (60px), centered icons, and consistent description wrapping

### 🔧 Kernels Tab Improvements
- **"Kernels" tab name**: Changed to "Kernels" in all 8 languages (was translated as "Núcleos", "Noyaux", "Ядра", etc.)
- **Clean Old Kernels**: Completely rewritten kernel cleanup with Python-based logic:
  - Smart classification: keeps running kernel + latest base + latest Liquorix + latest XanMod
  - Confirmation dialog showing ✓ kernels to keep and ✗ packages to remove (including headers)
  - Single `pkexec` execution with `apt autoremove` and `update-grub`
  - Proper "System is clean" message when nothing to remove

### 🛡️ Security Tab Changes
- **Stacer AppImage**: Converted from broken `.deb` installation to stable AppImage (`/opt/stacer/Stacer.AppImage`)
  - Survives `apt upgrade` without breaking
  - Creates `.desktop` file for system integration
  - Clean uninstall removes AppImage and desktop entry

### 🌍 Internationalization
- Added 8 new gaming launcher translations (R2ModMan, Vinegar, Prism Launcher, Itch.io, Minigalaxy, Moonlight, Chiaki, Discord)
- Added EmulationStation-DE description translations for all 8 languages
- Added 7 new kernel cleanup dialog translations (confirmation, keep/remove labels)
- Changed "Kernels" to remain untranslated as a universal technical term

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

---

## Tyson Branch

## [1.1.5] - 2025-09-08

### 🆕 Changed / Fixed
- Updated all welcome tab link buttons to soplos.org: website (`https://soplos.org`), forum (`https://soplos.org/forums/`) and wiki (`https://soplos.org/wiki/`).
- Removed deprecated `on_website_clicked` and `on_wiki_clicked` method handlers — buttons now use inline lambdas consistently.
- Updated Blender icon to the new design.

## [1.1.4] - 2025-09-08

### 🆕 Added / Fixed
- Updated Blender icon to the requested image.
- Fixed welcome tab link buttons (website, forums, wiki).

## [1.1.3] - 2025-08-02

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

## [1.1.0] - 2025-07-24

### 🛠️ Fixed
- Fixed Flatpak/Flathub installation bug: Now Flatpak applications can be installed from Flathub without requiring administrator privileges. The Software Center correctly adds Flathub for the current user.

## [1.0.9] - 2025-07-18

### 🛠️ Fixed
- Fixed install buttons in the Software Center (now work correctly).

## [1.0.8] - 2025-07-15

### 🆕 Added / Improved
- Improvements in QEMU/KVM integration and operation for virtual machines.
- Enhanced management and installation of NVIDIA drivers (detection, recommendation, and a more robust installation process).
- **Translation dictionary fragmentation completed:** Interface texts are now organized by language in separate files for Spanish, English, French, Portuguese, German, Italian, Russian, and Romanian.
- **Internationalization:** The program has been fully internationalized to facilitate global collaboration and translation contributions.
- **Recommended Tab:** Improved logic for install/uninstall buttons, now updates state and action dynamically after each operation.
- **LibreWolf:** Installation now uses Flatpak (Flathub) instead of APT or external repositories, avoiding conflicts and simplifying maintenance.

## [1.0.7] - 2025-07-13

### 🛠️ Improved - Metainfo and AppStream/DEP-11 compatibility
- Metainfo updated to comply with AppStream/DEP-11.
- Minor improvements in integration and documentation.
- No functional changes in the application.

## [1.0.6] - 2025-06-24

### 🆕 Added
- Improvements to the Software Center and browser updates.
- Software Center now detects if programs are installed.
- Midori replaced with Epiphany (GNOME Web) as lightweight browser.
- DaVinci Resolve replaced with Shotcut for video editing.
- Driver Center improved with optimized hardware detection.
- Enhanced hardware scanning functionality.

## [1.0.5] - 2025-06-14

### 🔧 Fixed
- Reverted App ID to `com.soplos.welcome` (dot notation restored after 1.0.2 change).
- Soplos Packager injection block removed from `main.py` (reverted to clean entry point).
- Assets renamed back to `com.soplos.welcome` convention (desktop file, icons, metainfo, pixmaps).

## [1.0.4] - 2025-06-09

### 🔧 Fixed
- Autostart updated: now copies `com.soploswelcome.desktop` from `/usr/share/applications/` instead of writing inline content, ensuring the autostart entry always matches the installed desktop file.
- Desktop file references updated (`X-GNOME-Application-ID`, `X-AppStream-Metadata`, `Icon`, `StartupWMClass`) to use `com.soploswelcome`.

## [1.0.3] - 2025-06-05

### 🔧 Fixed
- Soplos Packager App ID initialization block injected into `main.py`: sets `GLib.set_prgname`, `GLib.set_application_name` and `Gtk.Window.set_default_icon_name` to `com.soploswelcome` for correct window manager integration.

## [1.0.2] - 2025-06-04

### 🔄 Changed
- Renamed all assets from `com.soplos.welcome` to `com.soploswelcome` (dot removed) for Soplos Packager compatibility: desktop file, icons (all sizes), metainfo and pixmaps.
- App ID changed from `com.soplos.welcome` to `com.soploswelcome`.

## [1.0.1] - 2025-05-28

### 🔧 Fixed
- Welcome tab: corrected website button URL from `soploslinux.com/distro` to the distro-specific URL (`soploslinux.com/tyson`).

## [1.0.0] - 2025-05-20

### 🎉 Initial Release
- Port of Tyron 1.0.0 to Soplos Tyson. Initial release of Soplos Welcome for Tyson.
- Welcome screen for Soplos Linux.
- Initial system setup.
- Installation of recommended software.
- Desktop customization.
- Access to help and support resources.
- Intuitive and user-friendly interface.
- Support for multiple languages.

---

## Tyron Branch

## [1.1.4] - 2025-09-08

### 🆕 Added / Fixed
- Updated Blender icon to the requested image.
- Fixed welcome tab link buttons (website, forums, wiki).

## [1.1.3] - 2025-08-03

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

## [1.0.8] - 2025-07-24

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

## [1.0.5] - 2025-05-08

### 🔧 Fixed
- Reverted App ID to `com.soplos.welcome` (dot notation restored after 1.0.2 change).
- Soplos Packager injection block removed from `main.py` (reverted to clean entry point).
- Assets renamed back to `com.soplos.welcome` convention (desktop file, icons, metainfo, pixmaps).

## [1.0.4] - 2025-05-07

### 🔧 Fixed
- Autostart updated: now copies `com.soploswelcome.desktop` from `/usr/share/applications/` instead of writing inline content, ensuring the autostart entry always matches the installed desktop file.
- Desktop file references updated (`X-GNOME-Application-ID`, `X-AppStream-Metadata`, `Icon`, `StartupWMClass`) to use `com.soploswelcome`.

## [1.0.3] - 2025-05-06

### 🔧 Fixed
- Soplos Packager App ID initialization block injected into `main.py`: sets `GLib.set_prgname`, `GLib.set_application_name` and `Gtk.Window.set_default_icon_name` to `com.soploswelcome` for correct window manager integration.

## [1.0.2] - 2025-05-05

### 🔄 Changed
- Renamed all assets from `com.soplos.welcome` to `com.soploswelcome` (dot removed) for Soplos Packager compatibility: desktop file, icons (all sizes), metainfo and pixmaps.
- App ID changed from `com.soplos.welcome` to `com.soploswelcome`.

## [1.0.1] - 2025-04-25

### 🔧 Fixed
- Welcome tab: corrected website button URL from `soploslinux.com/distro` to the distro-specific URL (`soploslinux.com/tyron`).

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
