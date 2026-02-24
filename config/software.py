"""
Software configuration for Soplos Welcome.
Defines available software categories and packages.
"""

import os
from pathlib import Path
from core.i18n_manager import _

# Get project root
PROJECT_ROOT = Path(__file__).parent.parent

# Software categories with their packages
SOFTWARE_CATEGORIES = {
    'browsers': {
        'title': _('Web Browsers'),
        'icon': 'browsers',
        'packages': [
            {
                'name': 'Firefox',
                'package': 'firefox',
                'flatpak': 'org.mozilla.firefox',
                'icon': 'firefox.png',
                'description': _('Free and open-source web browser developed by Mozilla'),
                'official': True
            },
            {
                'name': 'Google Chrome',
                'package': 'google-chrome-stable',
                'icon': 'chrome.png',
                'description': _('Web browser developed by Google'),
                'official': False,
                'install_commands': [
                    'wget -q -O /tmp/google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb',
                    'apt install -y /tmp/google-chrome.deb',
                    'rm /tmp/google-chrome.deb'
                ]
            },
            {
                'name': 'Chromium',
                'package': 'chromium',
                'flatpak': 'org.chromium.Chromium',
                'icon': 'chromium.png',
                'description': _('Open-source project behind Google Chrome'),
                'official': True
            },
            {
                'name': 'Brave',
                'package': 'brave-browser',
                'flatpak': 'com.brave.Browser',
                'icon': 'brave.png',
                'description': _('Privacy-focused browser that blocks ads'),
                'official': False,
                'install_commands': [
                    'apt install -y curl',
                    'curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg',
                    'curl -fsSLo /etc/apt/sources.list.d/brave-browser-release.sources https://brave-browser-apt-release.s3.brave.com/brave-browser.sources',
                    'apt update',
                    'apt install -y brave-browser'
                ]
            },
            {
                'name': 'LibreWolf',
                'package': 'librewolf',
                'flatpak': 'io.gitlab.librewolf-community',
                'icon': 'librewolf.png',
                'description': _('Firefox fork focused on privacy, security and freedom'),
                'official': False
            },
            {
                'name': 'Midori',
                'package': 'midori',
                'icon': 'midori.png',
                'description': _('Lightweight, fast and secure web browser'),
                'official': False,
                'install_commands': [
                    'wget -q -O /tmp/midori.deb https://github.com/goastian/midori-desktop/releases/download/v11.6/midori_11.6-1_amd64.deb',
                    'apt install -y /tmp/midori.deb',
                    'rm /tmp/midori.deb'
                ]
            },
        ]
    },
    
    'comunications': {
        'title': _('Communication'),
        'icon': 'comunications',
        'packages': [
            {
                'name': 'Thunderbird',
                'package': 'thunderbird',
                'flatpak': 'org.mozilla.Thunderbird',
                'icon': 'thunderbird.png',
                'description': _('Free email client developed by Mozilla'),
                'official': True
            },
            {
                'name': 'Discord',
                'package': 'discord',
                'flatpak': 'com.discordapp.Discord',
                'icon': 'discord.png',
                'description': _('Communication app for communities and gaming'),
                'official': False
            },
            {
                'name': 'Telegram',
                'package': 'telegram-desktop',
                'flatpak': 'org.telegram.desktop',
                'icon': 'telegram.png',
                'description': _('Fast and secure messaging app'),
                'official': False
            },
            {
                'name': 'Signal',
                'package': 'signal-desktop',
                'flatpak': 'org.signal.Signal',
                'icon': 'signal.png',
                'description': _('Private messaging with end-to-end encryption'),
                'official': False
            },
            {
                'name': 'Element',
                'package': 'element-desktop',
                'flatpak': 'im.riot.Riot',
                'icon': 'element.png',
                'description': _('Matrix client for decentralized communication'),
                'official': False
            },
            {
                'name': 'WhatsApp',
                'package': None,
                'flatpak': 'io.github.mimbrero.WhatsAppDesktop',
                'icon': 'whatsapp.png',
                'description': _('Unofficial WhatsApp desktop client'),
                'official': False
            },
            {
                'name': 'Slack',
                'package': None,
                'flatpak': 'com.slack.Slack',
                'icon': 'slack.png',
                'description': _('Team collaboration and communication platform'),
                'official': False
            },
            {
                'name': 'Zoom',
                'package': None,
                'flatpak': 'us.zoom.Zoom',
                'icon': 'zoom.png',
                'description': _('Video conferencing and meetings'),
                'official': False
            }
        ]
    },
    
    'developer': {
        'title': _('Development'),
        'icon': 'vscode.png',
        'packages': [
            {
                'name': 'Visual Studio Code',
                'package': 'code',
                'flatpak': 'com.visualstudio.code',
                'icon': 'vscode.png',
                'description': _('Source code editor developed by Microsoft'),
                'official': False,
                'install_commands': [
                    'apt install -y wget gpg apt-transport-https',
                    'wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor --yes > /usr/share/keyrings/packages.microsoft.gpg',
                    'echo "deb [arch=amd64 signed-by=/usr/share/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" | tee /etc/apt/sources.list.d/vscode.list > /dev/null',
                    'apt update',
                    'apt install -y code'
                ]
            },
            {
                'name': 'VSCodium',
                'package': 'codium',
                'flatpak': 'com.vscodium.codium',
                'icon': 'vscodium.png',
                'description': _('Free version of Visual Studio Code without telemetry'),
                'official': False
            },
            {
                'name': 'Google Antigravity',
                'package': 'antigravity',
                'icon': 'antigravity.png',
                'description': _('Advanced Agentic AI Coding Assistant'),
                'official': False,
                'install_commands': [
                    'mkdir -p /etc/apt/keyrings',
                    'curl -fsSL https://us-central1-apt.pkg.dev/doc/repo-signing-key.gpg | gpg --dearmor --yes -o /etc/apt/keyrings/antigravity-repo-key.gpg',
                    'echo "deb [signed-by=/etc/apt/keyrings/antigravity-repo-key.gpg] https://us-central1-apt.pkg.dev/projects/antigravity-auto-updater-dev/ antigravity-debian main" | tee /etc/apt/sources.list.d/antigravity.list > /dev/null',
                    'apt update',
                    'apt install -y antigravity'
                ]
            },
            {
                'name': 'Sublime Text',
                'package': 'sublime-text',
                'flatpak': 'com.sublimetext.three',
                'icon': 'sublime-text.png',
                'description': _('Sophisticated text editor for code and markup'),
                'official': False,
                'install_commands': [
                    'apt install -y wget gpg apt-transport-https',
                    'mkdir -p /etc/apt/keyrings',
                    'wget -qO /etc/apt/keyrings/sublimehq-pub.asc https://download.sublimetext.com/sublimehq-pub.gpg',
                    'echo -e "Types: deb\\nURIs: https://download.sublimetext.com/\\nSuites: apt/stable/\\nSigned-By: /etc/apt/keyrings/sublimehq-pub.asc" | tee /etc/apt/sources.list.d/sublime-text.sources > /dev/null',
                    'apt update',
                    'apt install -y sublime-text'
                ]
            },
            {
                'name': 'Cursor',
                'package': 'cursor',
                'install_commands': [
                    'wget -q -O /tmp/cursor.deb "https://api2.cursor.sh/updates/download/golden/linux-x64-deb/cursor/0.43.3"',
                    'apt install -y /tmp/cursor.deb',
                    'rm /tmp/cursor.deb'
                ],
                'icon': 'cursor.png',
                'description': _('Code editor with integrated AI'),
                'official': False
            },
            {
                'name': 'Pulsar',
                'package': None,
                'flatpak': 'dev.pulsar_edit.Pulsar',
                'icon': 'pulsar.png',
                'description': _('A community-led, hyper-hackable text editor'),
                'official': False
            },
            {
                'name': 'Geany',
                'package': 'geany',
                'flatpak': 'org.geany.Geany',
                'icon': 'geany.png',
                'description': _('Lightweight and fast IDE with multi-language support'),
                'official': True
            },
            {
                'name': 'Bluefish',
                'package': 'bluefish',
                'icon': 'bluefish.png',
                'description': _('Advanced editor for web programmers'),
                'official': True
            },
            {
                'name': 'FileZilla',
                'package': 'filezilla',
                'icon': 'filezilla.png',
                'description': _('Fast and reliable FTP/SFTP client'),
                'official': True
            },
            {
                'name': 'Postman',
                'package': None,
                'flatpak': 'com.getpostman.Postman',
                'icon': 'postman.png',
                'description': _('API development and testing platform'),
                'official': False
            }
        ]
    },
    
    'graphics': {
        'title': _('Graphics and Design'),
        'icon': 'graphics',
        'packages': [
            {
                'name': 'GIMP',
                'package': 'gimp',
                'flatpak': 'org.gimp.GIMP',
                'icon': 'gimp.png',
                'description': _('Advanced and free image editor'),
                'official': True
            },
            {
                'name': 'Inkscape',
                'package': 'inkscape',
                'flatpak': 'org.inkscape.Inkscape',
                'icon': 'inkscape.png',
                'description': _('Professional vector graphics editor'),
                'official': True
            },
            {
                'name': 'Blender',
                'package': 'blender',
                'flatpak': 'org.blender.Blender',
                'icon': 'blender.png',
                'description': _('Complete and free 3D creation suite'),
                'official': True
            },
            {
                'name': 'Krita',
                'package': 'krita',
                'flatpak': 'org.kde.krita',
                'icon': 'krita.png',
                'description': _('Professional digital painting program'),
                'official': True
            },
            {
                'name': 'darktable',
                'package': 'darktable',
                'flatpak': 'org.darktable.Darktable',
                'icon': 'darktable.png',
                'description': _('Virtual lighttable for photography'),
                'official': True
            },
            {
                'name': 'RapidRAW',
                'package': 'rapid-raw',
                'install_commands': [
                    'wget -q -O /tmp/rapidraw.deb https://github.com/CyberTimon/RapidRAW/releases/download/v1.4.6/03_RapidRAW_v1.4.6_ubuntu-24.04_amd64.deb',
                    'apt install -y /tmp/rapidraw.deb',
                    'rm /tmp/rapidraw.deb'
                ],
                'icon': 'rapidraw.png',
                'description': _('Fast and modern RAW photo editor'),
                'official': False
            },
            {
                'name': 'RawTherapee',
                'package': 'rawtherapee',
                'flatpak': 'com.rawtherapee.RawTherapee',
                'icon': 'rawtherapee.png',
                'description': _('Advanced RAW photo processing program'),
                'official': True
            },
            {
                'name': 'Hugin',
                'package': 'hugin',
                'icon': 'hugin.png',
                'description': _('Panorama photo stitcher'),
                'official': True
            },
            {
                'name': 'Affinity Suite',
                'package': None,
                'icon': 'affinity.png',
                'description': _('Professional photo editing, design and publishing suite'),
                'official': False,
                'check_path': '/opt/affinity/Affinity.AppImage',
                'install_commands': [
                    'mkdir -p /opt/affinity',
                    'wget -q -O /opt/affinity/Affinity.AppImage "https://github.com/ryzendew/Linux-Affinity-Installer/releases/download/3.0.2/Affinity-3.0.2-x86_64.AppImage"',
                    'chmod +x /opt/affinity/Affinity.AppImage',
                    'mkdir -p /usr/share/icons/hicolor/256x256/apps/',
                    'cp /usr/local/bin/soplos-welcome/assets/icons/graphics/affinity.png /usr/share/icons/hicolor/256x256/apps/affinity.png',
                    'gtk-update-icon-cache /usr/share/icons/hicolor/ 2>/dev/null || true',
                    "printf '[Desktop Entry]\\nName=Affinity Suite\\nExec=/opt/affinity/Affinity.AppImage\\nIcon=affinity\\nType=Application\\nCategories=Graphics;\\nComment=Professional photo editing, design and publishing suite\\n' > /usr/share/applications/affinity.desktop"
                ],
                'uninstall_commands': [
                    'rm -rf /opt/affinity/',
                    'rm -f /usr/share/applications/affinity.desktop',
                    'rm -f /usr/share/icons/hicolor/256x256/apps/affinity.png',
                    'gtk-update-icon-cache /usr/share/icons/hicolor/ 2>/dev/null || true'
                ]
            }
        ]
    },
    
    'multimedia': {
        'title': _('Multimedia'),
        'icon': 'multimedia',
        'packages': [
            {
                'name': 'VLC Media Player',
                'package': 'vlc',
                'flatpak': 'org.videolan.VLC',
                'icon': 'vlc.png',
                'description': _('Universal media player'),
                'official': True
            },
            {
                'name': 'OBS Studio',
                'package': 'obs-studio',
                'flatpak': 'com.obsproject.Studio',
                'icon': 'obs-studio.png',
                'description': _('Software for streaming and video recording'),
                'official': True
            },
            {
                'name': 'Kdenlive',
                'package': 'kdenlive',
                'flatpak': 'org.kde.kdenlive',
                'icon': 'kdenlive.png',
                'description': _('Professional non-linear video editor'),
                'official': True
            },
            {
                'name': 'Audacity',
                'package': 'audacity',
                'flatpak': 'org.audacityteam.Audacity',
                'icon': 'audacity.png',
                'description': _('Free and open-source audio editor'),
                'official': True
            },
            {
                'name': 'MPV',
                'package': 'mpv',
                'flatpak': 'io.mpv.Mpv',
                'icon': 'mpv.png',
                'description': _('Minimalist and powerful media player'),
                'official': True
            },
            {
                'name': 'LMMS',
                'package': 'lmms',
                'icon': 'lmms.png',
                'description': _('Digital audio workstation'),
                'official': True
            },
            {
                'name': 'Mixxx',
                'package': 'mixxx',
                'icon': 'mixxx.png',
                'description': _('Professional DJ software'),
                'official': True
            },
            {
                'name': 'Kodi',
                'package': 'kodi',
                'flatpak': 'tv.kodi.Kodi',
                'icon': 'kodi.png',
                'description': _('Open-source media center'),
                'official': True
            },
            {
                'name': 'OpenShot',
                'package': 'openshot-qt',
                'flatpak': 'org.openshot.OpenShot',
                'icon': 'openshot.png',
                'description': _('Easy to use video editor'),
                'official': True
            },
            {
                'name': 'DaVinci Resolve',
                'package': None,
                'flatpak': None,
                'icon': 'davinci-resolve.png',
                'description': _('Professional video editing (Script by Daniel Tufvesson)'),
                'official': False,
                'custom_install': True
            },
            {
                'name': 'Spotify',
                'package': None,
                'flatpak': 'com.spotify.Client',
                'icon': 'spotify.png',
                'description': _('Digital music streaming service'),
                'official': False
            },
            {
                'name': 'HandBrake',
                'package': 'handbrake',
                'flatpak': 'fr.handbrake.ghb',
                'icon': 'handbrake.png',
                'description': _('Open source video transcoder'),
                'official': True
            }
        ]
    },
    
    'office': {
        'title': _('Office'),
        'icon': 'office',
        'packages': [
            {
                'name': 'LibreOffice',
                'package': 'libreoffice',
                'flatpak': 'org.libreoffice.LibreOffice',
                'icon': 'libreoffice.png',
                'description': _('Complete and free office suite'),
                'official': True
            },
            {
                'name': 'OnlyOffice',
                'package': 'onlyoffice-desktopeditors',
                'flatpak': 'org.onlyoffice.desktopeditors',
                'icon': 'onlyoffice.png',
                'description': _('Office suite compatible with Microsoft Office'),
                'official': False
            },
            {
                'name': 'WPS Office',
                'package': None,
                'flatpak': 'com.wps.Office',
                'icon': 'wpsoffice.png',
                'description': _('Lightweight and elegant office suite'),
                'official': False
            },
            {
                'name': 'Adobe Reader',
                'package': None,
                'flatpak': 'com.adobe.Reader',
                'icon': 'reader.png',
                'description': _('Adobe PDF reader'),
                'official': False
            }
        ]
    },
    
    'gaming': {
        'title': _('Gaming'),
        'icon': 'steam.png',
        'packages': [
            {
                'name': 'Steam',
                'package': None,
                'flatpak': 'com.valvesoftware.Steam',
                'icon': 'steam.png',
                'description': _('Digital distribution platform for video games'),
                'official': False
            },
            {
                'name': 'Lutris',
                'package': 'lutris',
                'flatpak': 'net.lutris.Lutris',
                'icon': 'lutris.png',
                'description': _('Unified platform for managing games on Linux'),
                'official': True
            },
            {
                'name': 'Bottles',
                'package': None,
                'flatpak': 'com.usebottles.bottles',
                'icon': 'bottles.png',
                'description': _('Run Windows applications on Linux using Wine'),
                'official': False
            },
            {
                'name': 'RetroArch',
                'package': 'retroarch',
                'flatpak': 'org.libretro.RetroArch',
                'icon': 'retroarch.png',
                'description': _('Frontend for emulators and game engines'),
                'official': True
            },
            {
                'name': 'Heroic Games Launcher',
                'package': None,
                'flatpak': 'com.heroicgameslauncher.hgl',
                'icon': 'heroic.png',
                'description': _('Launcher for Epic, GOG and Amazon Games'),
                'official': False
            },
            {
                'name': 'EmulationStation-DE',
                'package': None,
                'icon': 'ES-DE.png',
                'description': _('Frontend for emulators with a modern interface'),
                'official': False,
                'check_path': '/opt/es-de/EmulationStation-DE.AppImage',
                'install_commands': [
                    'mkdir -p /opt/es-de',
                    'wget -q -O /opt/es-de/EmulationStation-DE.AppImage "https://gitlab.com/es-de/emulationstation-de/-/package_files/246875981/download"',
                    'chmod +x /opt/es-de/EmulationStation-DE.AppImage',
                    'cp /usr/local/bin/soplos-welcome/assets/icons/gaming/ES-DE.png /usr/share/icons/hicolor/256x256/apps/es-de.png',
                    'gtk-update-icon-cache /usr/share/icons/hicolor/ 2>/dev/null || true',
                    "bash -c 'cat > /usr/share/applications/es-de.desktop << EOF\\n[Desktop Entry]\\nName=EmulationStation-DE\\nExec=/opt/es-de/EmulationStation-DE.AppImage\\nIcon=es-de\\nType=Application\\nCategories=Game;\\nComment=Frontend for emulators with a modern interface\\nEOF'"
                ],
                'uninstall_commands': [
                    'rm -rf /opt/es-de/',
                    'rm -f /usr/share/applications/es-de.desktop',
                    'rm -f /usr/share/icons/hicolor/256x256/apps/es-de.png',
                    'gtk-update-icon-cache /usr/share/icons/hicolor/ 2>/dev/null || true'
                ]
            }
        ]
    }
}

def get_icon_path(category: str, icon_name: str) -> Path:
    """Get the full path to an icon file."""
    if category and icon_name:
        return PROJECT_ROOT / 'assets' / 'icons' / category / icon_name
    elif icon_name:
        return PROJECT_ROOT / 'assets' / 'icons' / icon_name
    else:
        return PROJECT_ROOT / 'assets' / 'icons' / 'org.soplos.welcome.png'

def get_category_icon_path(category: str) -> Path:
    """Get the path to a category icon."""
    return PROJECT_ROOT / 'assets' / 'icons' / category

def get_all_categories():
    """Get all software categories."""
    return SOFTWARE_CATEGORIES

def get_category(category_name: str):
    """Get a specific category."""
    return SOFTWARE_CATEGORIES.get(category_name, {})

def get_package_info(category_name: str, package_name: str):
    """Get information about a specific package."""
    category = get_category(category_name)
    if not category:
        return None
    
    for package in category.get('packages', []):
        if package['name'].lower() == package_name.lower():
            return package
    return None
