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
                'snap': 'firefox',
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
                'package': 'chromium-browser',
                'flatpak': 'org.chromium.Chromium',
                'snap': 'chromium',
                'icon': 'chromium.png',
                'description': 'Proyecto de código abierto detrás de Google Chrome',
                'official': True
            },
            {
                'name': 'Brave',
                'package': 'brave-browser',
                'flatpak': 'com.brave.Browser',
                'snap': 'brave',
                'icon': 'brave.png',
                'description': 'Navegador centrado en la privacidad que bloquea anuncios',
                'official': False
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
                'name': 'Epiphany',
                'package': 'epiphany-browser',
                'flatpak': 'org.gnome.Epiphany',
                'icon': 'epiphany.png',
                'description': 'Navegador web oficial de GNOME',
                'official': True
            }
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
                'snap': 'thunderbird',
                'icon': 'thunderbird.png',
                'description': 'Cliente de correo electrónico libre desarrollado por Mozilla',
                'official': True
            },
            {
                'name': 'Discord',
                'package': 'discord',
                'flatpak': 'com.discordapp.Discord',
                'snap': 'discord',
                'icon': 'discord.png',
                'description': 'Aplicación de comunicación para comunidades y gaming',
                'official': False
            },
            {
                'name': 'Telegram',
                'package': 'telegram-desktop',
                'flatpak': 'org.telegram.desktop',
                'snap': 'telegram-desktop',
                'icon': 'telegram.png',
                'description': 'Aplicación de mensajería rápida y segura',
                'official': True
            },
            {
                'name': 'Signal',
                'package': 'signal-desktop',
                'flatpak': 'org.signal.Signal',
                'snap': 'signal-desktop',
                'icon': 'signal.png',
                'description': 'Mensajería privada con cifrado de extremo a extremo',
                'official': False
            },
            {
                'name': 'Element',
                'package': 'element-desktop',
                'flatpak': 'im.riot.Riot',
                'snap': 'element-desktop',
                'icon': 'element.png',
                'description': 'Cliente para Matrix, comunicación descentralizada',
                'official': True
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
        'icon': 'developer',
        'packages': [
            {
                'name': 'Visual Studio Code',
                'package': 'code',
                'flatpak': 'com.visualstudio.code',
                'snap': 'code',
                'icon': 'vscode.png',
                'description': 'Editor de código fuente desarrollado por Microsoft',
                'official': False
            },
            {
                'name': 'VSCodium',
                'package': 'codium',
                'flatpak': 'com.vscodium.codium',
                'snap': 'codium',
                'icon': 'vscodium.png',
                'description': 'Versión libre de Visual Studio Code sin telemetría',
                'official': False
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
                'name': 'Sublime Text',
                'package': 'sublime-text',
                'flatpak': 'com.sublimetext.three',
                'snap': 'sublime-text',
                'icon': 'sublime-text.png',
                'description': 'Editor de texto sofisticado para código y marcado',
                'official': False
            },
            {
                'name': 'Bluefish',
                'package': 'bluefish',
                'icon': 'bluefish.png',
                'description': 'Editor avanzado para programadores web',
                'official': True
            },
            {
                'name': 'Zed',
                'package': None,
                'flatpak': None,
                'icon': 'zed.png',
                'description': 'Editor de código colaborativo de alto rendimiento',
                'official': False,
                'custom_install': True
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
                'snap': 'gimp',
                'icon': 'gimp.png',
                'description': 'Editor de imágenes avanzado y gratuito',
                'official': True
            },
            {
                'name': 'Inkscape',
                'package': 'inkscape',
                'flatpak': 'org.inkscape.Inkscape',
                'snap': 'inkscape',
                'icon': 'inkscape.png',
                'description': 'Editor de gráficos vectoriales profesional',
                'official': True
            },
            {
                'name': 'Blender',
                'package': 'blender',
                'flatpak': 'org.blender.Blender',
                'snap': 'blender',
                'icon': 'blender.png',
                'description': 'Suite de creación 3D completa y gratuita',
                'official': True
            },
            {
                'name': 'Krita',
                'package': 'krita',
                'flatpak': 'org.kde.krita',
                'snap': 'krita',
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
                'name': 'RawTherapee',
                'package': 'rawtherapee',
                'flatpak': 'com.rawtherapee.RawTherapee',
                'icon': 'rawtherapee.png',
                'description': 'Procesador de archivos RAW gratuito',
                'official': True
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
                'snap': 'vlc',
                'icon': 'vlc.png',
                'description': 'Reproductor multimedia universal',
                'official': True
            },
            {
                'name': 'OBS Studio',
                'package': 'obs-studio',
                'flatpak': 'com.obsproject.Studio',
                'snap': 'obs-studio',
                'icon': 'obs-studio.png',
                'description': 'Software para streaming y grabación de video',
                'official': True
            },
            {
                'name': 'Kdenlive',
                'package': 'kdenlive',
                'flatpak': 'org.kde.kdenlive',
                'snap': 'kdenlive',
                'icon': 'kdenlive.png',
                'description': 'Editor de video no lineal profesional',
                'official': True
            },
            {
                'name': 'Audacity',
                'package': 'audacity',
                'flatpak': 'org.audacityteam.Audacity',
                'snap': 'audacity',
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
                'name': 'OpenShot',
                'package': 'openshot-qt',
                'flatpak': 'org.openshot.OpenShot',
                'snap': 'openshot-community',
                'icon': 'openshot.png',
                'description': 'Editor de video fácil de usar',
                'official': True
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
                'snap': 'libreoffice',
                'icon': 'libreoffice.png',
                'description': 'Suite ofimática completa y gratuita',
                'official': True
            },
            {
                'name': 'OnlyOffice',
                'package': 'onlyoffice-desktopeditors',
                'flatpak': 'org.onlyoffice.desktopeditors',
                'snap': 'onlyoffice-desktopeditors',
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
            }
        ]
    },
    
    'gaming': {
        'title': 'Gaming',
        'icon': 'gaming',
        'packages': [
            {
                'name': 'Steam',
                'package': 'steam',
                'flatpak': 'com.valvesoftware.Steam',
                'snap': 'steam',
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
                'official': True
            },
            {
                'name': 'RetroArch',
                'package': 'retroarch',
                'flatpak': 'org.libretro.RetroArch',
                'snap': 'retroarch',
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
