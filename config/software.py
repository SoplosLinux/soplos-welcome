"""
Software configuration for Soplos Welcome.
Defines available software categories and packages.
"""

import os
from pathlib import Path

# Get project root
PROJECT_ROOT = Path(__file__).parent.parent

# Software categories with their packages
SOFTWARE_CATEGORIES = {
    'browsers': {
        'title': 'Navegadores Web',
        'icon': 'browsers',
        'packages': [
            {
                'name': 'Firefox',
                'package': 'firefox',
                'flatpak': 'org.mozilla.firefox',
                'icon': 'firefox.png',
                'description': 'Navegador web libre y gratuito desarrollado por Mozilla',
                'official': True
            },
            {
                'name': 'Google Chrome',
                'package': 'google-chrome-stable',
                'icon': 'chrome.png',
                'description': 'Navegador web desarrollado por Google',
                'official': False,
                'deb_url': 'https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb'
            },
            {
                'name': 'Chromium',
                'package': 'chromium',
                'flatpak': 'org.chromium.Chromium',
                'icon': 'chromium.png',
                'description': 'Proyecto de código abierto detrás de Google Chrome',
                'official': True
            },
            {
                'name': 'Brave',
                'package': 'brave-browser',
                'flatpak': 'com.brave.Browser',
                'icon': 'brave.png',
                'description': 'Navegador centrado en la privacidad que bloquea anuncios',
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
                'description': 'Fork de Firefox centrado en privacidad, seguridad y libertad',
                'official': False
            },
            {
                'name': 'Midori',
                'package': 'midori',
                'icon': 'midori.png',
                'description': 'Navegador web ligero, rápido y seguro',
                'official': False,
                'deb_url': 'https://github.com/goastian/midori-desktop/releases/download/v11.6/midori_11.6-1_amd64.deb'
            },
        ]
    },
    
    'comunications': {
        'title': 'Comunicación',
        'icon': 'comunications',
        'packages': [
            {
                'name': 'Thunderbird',
                'package': 'thunderbird',
                'flatpak': 'org.mozilla.Thunderbird',
                'icon': 'thunderbird.png',
                'description': 'Cliente de correo electrónico libre desarrollado por Mozilla',
                'official': True
            },
            {
                'name': 'Discord',
                'package': 'discord',
                'flatpak': 'com.discordapp.Discord',
                'icon': 'discord.png',
                'description': 'Aplicación de comunicación para comunidades y gaming',
                'official': False
            },
            {
                'name': 'Telegram',
                'package': 'telegram-desktop',
                'flatpak': 'org.telegram.desktop',
                'icon': 'telegram.png',
                'description': 'Aplicación de mensajería rápida y segura',
                'official': False
            },
            {
                'name': 'Signal',
                'package': 'signal-desktop',
                'flatpak': 'org.signal.Signal',
                'icon': 'signal.png',
                'description': 'Mensajería privada con cifrado de extremo a extremo',
                'official': False
            },
            {
                'name': 'Element',
                'package': 'element-desktop',
                'flatpak': 'im.riot.Riot',
                'icon': 'element.png',
                'description': 'Cliente para Matrix, comunicación descentralizada',
                'official': False
            },
            {
                'name': 'WhatsApp',
                'package': None,
                'flatpak': 'io.github.mimbrero.WhatsAppDesktop',
                'icon': 'whatsapp.png',
                'description': 'Cliente no oficial de WhatsApp para escritorio',
                'official': False
            }
        ]
    },
    
    'developer': {
        'title': 'Desarrollo',
        'icon': 'vscode.png',
        'packages': [
            {
                'name': 'Visual Studio Code',
                'package': 'code',
                'flatpak': 'com.visualstudio.code',
                'icon': 'vscode.png',
                'description': 'Editor de código fuente desarrollado por Microsoft',
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
                'description': 'Versión libre de Visual Studio Code sin telemetría',
                'official': False
            },
            {
                'name': 'Google Antigravity',
                'package': 'antigravity',
                'icon': 'antigravity.png',
                'description': 'IDE avanzado con gravedad cero',
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
                'description': 'Editor de texto sofisticado para código y marcado',
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
                'deb_url': 'https://api2.cursor.sh/updates/download/golden/linux-x64-deb/cursor/2.1',
                'icon': 'cursor.png',
                'description': 'Editor de código con IA integrada',
                'official': False
            },
            {
                'name': 'Zed',
                'package': None,
                'flatpak': None,
                'icon': 'zed.png',
                'description': 'Editor de código colaborativo de alto rendimiento',
                'official': False,
                'install_commands': [
                    'curl -fsSL https://zed.dev/install.sh | sh'
                ]
            },
            {
                'name': 'Geany',
                'package': 'geany',
                'flatpak': 'org.geany.Geany',
                'icon': 'geany.png',
                'description': 'IDE ligero y rápido con soporte para múltiples lenguajes',
                'official': True
            },
            {
                'name': 'Bluefish',
                'package': 'bluefish',
                'icon': 'bluefish.png',
                'description': 'Editor avanzado para programadores web',
                'official': True
            },
            {
                'name': 'FileZilla',
                'package': 'filezilla',
                'icon': 'filezilla.png',
                'description': 'Cliente FTP/SFTP rápido y confiable',
                'official': True
            }
        ]
    },
    
    'graphics': {
        'title': 'Gráficos y Diseño',
        'icon': 'graphics',
        'packages': [
            {
                'name': 'GIMP',
                'package': 'gimp',
                'flatpak': 'org.gimp.GIMP',
                'icon': 'gimp.png',
                'description': 'Editor de imágenes avanzado y gratuito',
                'official': True
            },
            {
                'name': 'Inkscape',
                'package': 'inkscape',
                'flatpak': 'org.inkscape.Inkscape',
                'icon': 'inkscape.png',
                'description': 'Editor de gráficos vectoriales profesional',
                'official': True
            },
            {
                'name': 'Blender',
                'package': 'blender',
                'flatpak': 'org.blender.Blender',
                'icon': 'blender.png',
                'description': 'Suite de creación 3D completa y gratuita',
                'official': True
            },
            {
                'name': 'Krita',
                'package': 'krita',
                'flatpak': 'org.kde.krita',
                'icon': 'krita.png',
                'description': 'Programa de pintura digital profesional',
                'official': True
            },
            {
                'name': 'darktable',
                'package': 'darktable',
                'flatpak': 'org.darktable.Darktable',
                'icon': 'darktable.png',
                'description': 'Mesa de trabajo virtual para fotografía',
                'official': True
            },
            {
                'name': 'RapidRAW',
                'package': 'rapid-raw',
                'deb_url': 'https://github.com/CyberTimon/RapidRAW/releases/download/v1.4.5/03_RapidRAW_v1.4.5_ubuntu-24.04_amd64.deb',
                'icon': 'rapidraw.png',
                'description': 'Editor de fotos RAW rápido y moderno',
                'official': False
            }
        ]
    },
    
    'multimedia': {
        'title': 'Multimedia',
        'icon': 'multimedia',
        'packages': [
            {
                'name': 'VLC Media Player',
                'package': 'vlc',
                'flatpak': 'org.videolan.VLC',
                'icon': 'vlc.png',
                'description': 'Reproductor multimedia universal',
                'official': True
            },
            {
                'name': 'OBS Studio',
                'package': 'obs-studio',
                'flatpak': 'com.obsproject.Studio',
                'icon': 'obs-studio.png',
                'description': 'Software para streaming y grabación de video',
                'official': True
            },
            {
                'name': 'Kdenlive',
                'package': 'kdenlive',
                'flatpak': 'org.kde.kdenlive',
                'icon': 'kdenlive.png',
                'description': 'Editor de video no lineal profesional',
                'official': True
            },
            {
                'name': 'Audacity',
                'package': 'audacity',
                'flatpak': 'org.audacityteam.Audacity',
                'icon': 'audacity.png',
                'description': 'Editor de audio gratuito y de código abierto',
                'official': True
            },
            {
                'name': 'MPV',
                'package': 'mpv',
                'flatpak': 'io.mpv.Mpv',
                'icon': 'mpv.png',
                'description': 'Reproductor multimedia minimalista y potente',
                'official': True
            },
            {
                'name': 'LMMS',
                'package': 'lmms',
                'icon': 'lmms.png',
                'description': 'Estación de trabajo de audio digital',
                'official': True
            },
            {
                'name': 'Mixxx',
                'package': 'mixxx',
                'icon': 'mixxx.png',
                'description': 'Software profesional de DJ',
                'official': True
            },
            {
                'name': 'Kodi',
                'package': 'kodi',
                'flatpak': 'tv.kodi.Kodi',
                'icon': 'kodi.png',
                'description': 'Centro multimedia de código abierto',
                'official': True
            },
            {
                'name': 'OpenShot',
                'package': 'openshot-qt',
                'flatpak': 'org.openshot.OpenShot',
                'icon': 'openshot.png',
                'description': 'Editor de video fácil de usar',
                'official': True
            },
            {
                'name': 'DaVinci Resolve',
                'package': None,
                'flatpak': None,
                'icon': 'davinci-resolve.png',
                'description': 'Edición de video profesional (Script por Daniel Tufvesson)',
                'official': False,
                'custom_install': True
            }
        ]
    },
    
    'office': {
        'title': 'Oficina',
        'icon': 'office',
        'packages': [
            {
                'name': 'LibreOffice',
                'package': 'libreoffice',
                'flatpak': 'org.libreoffice.LibreOffice',
                'icon': 'libreoffice.png',
                'description': 'Suite ofimática completa y gratuita',
                'official': True
            },
            {
                'name': 'OnlyOffice',
                'package': 'onlyoffice-desktopeditors',
                'flatpak': 'org.onlyoffice.desktopeditors',
                'icon': 'onlyoffice.png',
                'description': 'Suite ofimática compatible con Microsoft Office',
                'official': False
            },
            {
                'name': 'WPS Office',
                'package': None,
                'flatpak': 'com.wps.Office',
                'icon': 'wpsoffice.png',
                'description': 'Suite ofimática ligera y elegante',
                'official': False
            },
            {
                'name': 'Adobe Reader',
                'package': None,
                'flatpak': 'com.adobe.Reader',
                'icon': 'reader.png',
                'description': 'Lector de PDF de Adobe',
                'official': False
            }
        ]
    },
    
    'gaming': {
        'title': 'Gaming',
        'icon': 'steam.png',
        'packages': [
            {
                'name': 'Steam',
                'package': 'steam',
                'flatpak': 'com.valvesoftware.Steam',
                'icon': 'steam.png',
                'description': 'Plataforma de distribución de juegos',
                'official': False
            },
            {
                'name': 'Lutris',
                'package': 'lutris',
                'flatpak': 'net.lutris.Lutris',
                'icon': 'lutris.png',
                'description': 'Plataforma de gaming para Linux',
                'official': True
            },
            {
                'name': 'Bottles',
                'package': 'bottles',
                'flatpak': 'com.usebottles.bottles',
                'icon': 'bottles.png',
                'description': 'Gestor de prefijos de Wine fácil de usar',
                'official': False
            },
            {
                'name': 'RetroArch',
                'package': 'retroarch',
                'flatpak': 'org.libretro.RetroArch',
                'icon': 'retroarch.png',
                'description': 'Frontend para emuladores y engines de juegos',
                'official': True
            },
            {
                'name': 'Heroic Games Launcher',
                'package': None,
                'flatpak': 'com.heroicgameslauncher.hgl',
                'icon': 'heroic.png',
                'description': 'Launcher para Epic Games Store y GOG',
                'official': False
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
        return PROJECT_ROOT / 'assets' / 'icons' / 'com.soplos.welcome.png'

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
