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
                'name': 'Vivaldi',
                'package': None,
                'flatpak': 'com.vivaldi.Vivaldi',
                'icon': 'vivaldi.png',
                'description': _('Feature-packed web browser with built-in tools'),
                'official': False
            },
            {
                'name': 'Opera GX',
                'package': None,
                'flatpak': 'com.opera.opera-gx',
                'icon': 'opera-gx.png',
                'description': _('Gaming browser with system resource controls'),
                'official': False
            },
            {
                'name': 'Opera',
                'package': None,
                'flatpak': 'com.opera.Opera',
                'icon': 'opera.png',
                'description': _('Feature-rich browser with built-in VPN and ad blocker'),
                'official': False
            },
            {
                'name': 'Zen Browser',
                'package': 'zen-browser',
                'icon': 'zen-browser.png',
                'description': _('Privacy-focused Firefox-based browser with beautiful design'),
                'official': False,
                'install_commands': [
                    'ZEN_URL=$(curl -s https://api.github.com/repos/sh4r10/zen-browser-debian/releases/latest | grep browser_download_url | grep -v zip | grep -v tar | cut -d\\" -f4)',
                    'wget -q --show-progress -O /tmp/zen-browser.deb "$ZEN_URL"',
                    'apt install -y /tmp/zen-browser.deb',
                    'rm -f /tmp/zen-browser.deb'
                ]
            },
            {
                'name': 'Helium',
                'package': 'helium-bin',
                'icon': 'helium.png',
                'description': _('Privacy-focused browser built on Chromium with YouTube integration'),
                'official': False,
                'install_commands': [
                    'HELIUM_URL=$(curl -s https://api.github.com/repos/imputnet/helium-linux/releases/latest | grep browser_download_url | grep amd64.deb | cut -d\\" -f4)',
                    'wget -q --show-progress -O /tmp/helium.deb "$HELIUM_URL"',
                    'apt install -y /tmp/helium.deb',
                    'rm -f /tmp/helium.deb'
                ]
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
            {
                'name': 'Brave Origin',
                'package': 'brave-origin',
                'icon': 'brave-origin.png',
                'description': _('Privacy-focused browser by Brave with integrated AI assistant'),
                'official': False,
                'install_commands': [
                    'curl -fsS https://dl.brave.com/install.sh | FLAVOR=origin sh',
                    f'bash \'{os.path.join(PROJECT_ROOT, "services", "brave-origin-icon-patch.sh")}\' \'{os.path.join(PROJECT_ROOT, "assets", "icons", "browsers", "brave-origin-icons")}\'',
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
                'flatpak': None,
                'icon': 'whatsapp.png',
                'description': _('WhatsApp Web as a desktop app (Soplos WebApp Manager)'),
                'official': False,
                'webapp_id': 'whatsapp',
                'webapp_url': 'https://web.whatsapp.com/',
                'webapp_icon': os.path.join(PROJECT_ROOT, "assets", "icons", "comunications", "whatsapp.png"),
                'webapp_category': 'Network'
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
                'package': None,
                'icon': 'antigravity.png',
                # Google's own apt repo for Antigravity was discontinued, so this now
                # downloads the official tarball straight from Google's CDN and
                # extracts it to /opt, matching Welcome 3.0. The cleanup step below
                # removes the previous apt-repo-based install (package, repo file and
                # keyring) first, so upgrading from that leaves nothing behind.
                'description': _('Advanced Agentic AI Coding Assistant'),
                'official': False,
                'check_path': '/opt/antigravity/antigravity-ide',
                'install_commands': [
                    'dpkg -s antigravity >/dev/null 2>&1 && apt purge -y antigravity',
                    'rm -f /etc/apt/sources.list.d/antigravity.list /etc/apt/keyrings/antigravity-repo-key.gpg',
                    'wget -q -O /tmp/antigravity.tar.gz "https://edgedl.me.gvt1.com/edgedl/release2/j0qc3/antigravity/stable/2.5.5-4923483625488384/linux-x64/Antigravity%20IDE.tar.gz"',
                    'rm -rf /opt/antigravity',
                    'mkdir -p /opt/antigravity',
                    "tar --transform 's,^Antigravity IDE,antigravity,' -xzf /tmp/antigravity.tar.gz -C /opt",
                    'rm -f /tmp/antigravity.tar.gz',
                    'cp /opt/antigravity/resources/app/resources/linux/code.png /usr/share/pixmaps/antigravity.png',
                    "printf '[Desktop Entry]\\nName=Antigravity\\nExec=/opt/antigravity/antigravity-ide\\nIcon=/usr/share/pixmaps/antigravity.png\\nType=Application\\nCategories=Development;\\nComment=Advanced Agentic AI Coding Assistant\\n' > /usr/share/applications/antigravity.desktop",
                    'update-desktop-database /usr/share/applications 2>/dev/null || true'
                ],
                'uninstall_commands': [
                    'rm -rf /opt/antigravity',
                    'rm -f /usr/share/pixmaps/antigravity.png',
                    'rm -f /usr/share/applications/antigravity.desktop',
                    'update-desktop-database /usr/share/applications 2>/dev/null || true'
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
                'name': 'Zed',
                'package': None,
                'flatpak': 'dev.zed.Zed',
                'icon': 'zed.png',
                'description': _('High-performance, multiplayer code editor'),
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
            # Image editing
            {
                'name': 'GIMP',
                'package': 'gimp',
                'flatpak': 'org.gimp.GIMP',
                'icon': 'gimp.png',
                'description': _('Advanced and free image editor'),
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
                'name': 'Affinity Suite',
                'package': None,
                'icon': 'affinity.png',
                'description': _('Professional photo editing, design and publishing suite'),
                'official': False,
                'check_path': '~/AppImages/Affinity-3.0.2-x86_64.AppImage',
                'install_commands': [
                    'REAL_HOME=$(getent passwd $PKEXEC_UID | cut -d: -f6)',
                    'REAL_USER=$(getent passwd $PKEXEC_UID | cut -d: -f1)',
                    'sudo -u $REAL_USER mkdir -p "$REAL_HOME/AppImages/.icons"',
                    'sudo -u $REAL_USER mkdir -p "$REAL_HOME/.local/share/applications"',
                    'wget -q -O "$REAL_HOME/AppImages/Affinity-3.0.2-x86_64.AppImage" "https://github.com/ryzendew/Linux-Affinity-Installer/releases/download/3.2.0/Affinity-3.0.2-x86_64.AppImage"',
                    'chmod +x "$REAL_HOME/AppImages/Affinity-3.0.2-x86_64.AppImage"',
                    f'cp {os.path.join(PROJECT_ROOT, "assets", "icons", "graphics", "affinity.png")} "$REAL_HOME/AppImages/.icons/AffinitySuite.png"',
                    'chown -R $PKEXEC_UID:$PKEXEC_UID "$REAL_HOME/AppImages"',
                    "printf '[Desktop Entry]\\nName=Affinity Suite\\nExec=%s/AppImages/Affinity-3.0.2-x86_64.AppImage\\nIcon=%s/AppImages/.icons/AffinitySuite.png\\nType=Application\\nCategories=Graphics;\\nComment=Professional photo editing, design and publishing suite\\n' \"$REAL_HOME\" \"$REAL_HOME\" | sudo -u $REAL_USER tee \"$REAL_HOME/.local/share/applications/affinity.desktop\" > /dev/null",
                ],
                'uninstall_commands': [
                    'REAL_HOME=$(getent passwd $PKEXEC_UID | cut -d: -f6)',
                    'rm -f "$REAL_HOME/AppImages/Affinity-3.0.2-x86_64.AppImage"',
                    'rm -f "$REAL_HOME/AppImages/.icons/AffinitySuite.png"',
                    'rm -f "$REAL_HOME/.local/share/applications/affinity.desktop"'
                ]
            },
            {
                'name': 'Fog Panther',
                'package': None,
                'flatpak': 'com.fogpanther.FogPanther',
                'icon': 'pantherfog.png',
                'description': _('Professional image editor'),
                'official': False
            },
            {
                'name': 'Patchy',
                'package': None,
                'flatpak': None,
                'icon': 'patchy.png',
                'description': _('Open-source image editor focused on PSD compatibility and Photoshop-like workflows'),
                'official': False,
                'check_path': '~/.local/share/flatpak/app/com.rtsoft.patchy',
                'install_commands': [
                    'REAL_USER=$(getent passwd $PKEXEC_UID | cut -d: -f1)',
                    'sudo -u $REAL_USER flatpak remote-add --user --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo',
                    'wget -q -O /tmp/PatchyLinux.flatpak https://github.com/SethRobinson/Patchy/releases/download/v1.00/PatchyLinux.flatpak',
                    'chmod 644 /tmp/PatchyLinux.flatpak',
                    'sudo -u $REAL_USER flatpak install --user -y --noninteractive --bundle /tmp/PatchyLinux.flatpak',
                    'rm -f /tmp/PatchyLinux.flatpak'
                ],
                'uninstall_commands': [
                    'REAL_USER=$(getent passwd $PKEXEC_UID | cut -d: -f1)',
                    'sudo -u $REAL_USER flatpak uninstall --user -y com.rtsoft.patchy'
                ]
            },
            {
                'name': 'PhotoCraft',
                'package': 'photocraft',
                'flatpak': None,
                'icon': 'photocraft.png',
                'description': _('Clean-room Photoshop alternative written in Rust'),
                'official': False,
                'install_commands': [
                    'PHOTOCRAFT_URL=$(curl -s https://api.github.com/repos/storytold/photocraft/releases/latest | grep browser_download_url | grep linux-x86_64.deb | cut -d\\" -f4)',
                    'wget -q -O /tmp/photocraft.deb "$PHOTOCRAFT_URL"',
                    'apt install -y /tmp/photocraft.deb',
                    'rm -f /tmp/photocraft.deb'
                ],
                'uninstall_commands': [
                    'apt remove -y photocraft'
                ]
            },
            # Vector / Design
            {
                'name': 'Inkscape',
                'package': 'inkscape',
                'flatpak': 'org.inkscape.Inkscape',
                'icon': 'inkscape.png',
                'description': _('Professional vector graphics editor'),
                'official': True
            },
            {
                'name': 'VectorCraft',
                'package': 'vectorcraft',
                'flatpak': None,
                'icon': 'vectorcraft.png',
                'description': _('Clean-room Illustrator alternative written in Rust'),
                'official': False,
                'install_commands': [
                    'VECTORCRAFT_URL=$(curl -s https://api.github.com/repos/storytold/vectorcraft/releases/latest | grep browser_download_url | grep linux-x86_64.deb | cut -d\\" -f4)',
                    'wget -q -O /tmp/vectorcraft.deb "$VECTORCRAFT_URL"',
                    'apt install -y /tmp/vectorcraft.deb',
                    'rm -f /tmp/vectorcraft.deb'
                ],
                'uninstall_commands': [
                    'apt remove -y vectorcraft'
                ]
            },
            # 3D
            {
                'name': 'Blender',
                'package': 'blender',
                'flatpak': 'org.blender.Blender',
                'icon': 'blender.png',
                'description': _('Complete and free 3D creation suite'),
                'official': True
            },
            # Photography / RAW
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
                'package': None,
                'flatpak': 'io.github.CyberTimon.RapidRAW',
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
                'name': 'ART',
                'package': None,
                'flatpak': 'us.pixls.art.ART',
                'icon': 'art.png',
                'description': _('Advanced RAW photo editor with local adjustments'),
                'official': False
            },
            {
                'name': 'LightCraft',
                'package': 'lightcraft',
                'flatpak': None,
                'icon': 'lightcraft.png',
                'description': _('Clean-room Lightroom alternative written in Rust'),
                'official': False,
                'install_commands': [
                    'LIGHTCRAFT_URL=$(curl -s https://api.github.com/repos/storytold/lightcraft/releases/latest | grep browser_download_url | grep linux-x86_64.deb | cut -d\\" -f4)',
                    'wget -q -O /tmp/lightcraft.deb "$LIGHTCRAFT_URL"',
                    'apt install -y /tmp/lightcraft.deb',
                    'rm -f /tmp/lightcraft.deb'
                ],
                'uninstall_commands': [
                    'apt remove -y lightcraft'
                ]
            },
            {
                'name': 'Hugin',
                'package': 'hugin',
                'icon': 'hugin.png',
                'description': _('Panorama photo stitcher'),
                'official': True
            }
        ]
    },
    
    'multimedia': {
        'title': _('Multimedia'),
        'icon': 'multimedia',
        'packages': [
            # Media players
            {
                'name': 'VLC Media Player',
                'package': 'vlc',
                'flatpak': 'org.videolan.VLC',
                'icon': 'vlc.png',
                'description': _('Universal media player'),
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
                'name': 'Kodi',
                'package': 'kodi',
                'flatpak': 'tv.kodi.Kodi',
                'icon': 'kodi.png',
                'description': _('Open-source media center'),
                'official': True
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
                'name': 'Glassy Music',
                'package': 'glassy-music-nankill-mod',
                'flatpak': None,
                'icon': 'glassy-music.png',
                'description': _('Customized YouTube Music desktop client with lyrics, ad blocking and shader effects'),
                'official': False,
                'install_commands': [
                    'GLASSY_URL=$(curl -s https://api.github.com/repos/NanKillBro/glassy-music-nankill/releases/latest | grep browser_download_url | grep amd64.deb | cut -d\\" -f4)',
                    'wget -q -O /tmp/glassy-music.deb "$GLASSY_URL"',
                    'apt install -y /tmp/glassy-music.deb',
                    'rm -f /tmp/glassy-music.deb'
                ],
                'uninstall_commands': [
                    'apt remove -y glassy-music-nankill-mod'
                ]
            },
            {
                'name': 'Orchard',
                'package': None,
                'flatpak': None,
                'icon': 'orchard.png',
                # Orchard's own "stable" GitHub releases have shipped with an empty asset
                # list since v4.5.0 (their desktop build pipeline currently only publishes
                # working Linux packages under the 5.0.0 beta track), and /releases/latest
                # on this repo can resolve to an unrelated mobile-app release with no Linux
                # assets at all — so unlike the other GitHub-sourced entries here, there is
                # no reliable "always get the newest" URL to query. Pinned to the current
                # beta, needs a manual bump if Orchard ever publishes a working stable
                # release again.
                'description': _('Power-user desktop client for YouTube Music with smart crossfade, equalizer and Discord presence'),
                'official': False,
                'check_path': '~/.local/share/flatpak/app/dev.sfg.orchard',
                'install_commands': [
                    'REAL_USER=$(getent passwd $PKEXEC_UID | cut -d: -f1)',
                    'sudo -u $REAL_USER flatpak remote-add --user --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo',
                    'wget -q -O /tmp/orchard.flatpak https://github.com/SFG5453/Orchard/releases/download/v5.0.0-beta.9/orchard-packages-5.0.0-linux-x64.flatpak',
                    'chmod 644 /tmp/orchard.flatpak',
                    'sudo -u $REAL_USER flatpak install --user -y --noninteractive --bundle /tmp/orchard.flatpak',
                    'rm -f /tmp/orchard.flatpak'
                ],
                'uninstall_commands': [
                    'REAL_USER=$(getent passwd $PKEXEC_UID | cut -d: -f1)',
                    'sudo -u $REAL_USER flatpak uninstall --user -y dev.sfg.orchard'
                ]
            },
            {
                'name': 'Sonora',
                'package': None,
                'flatpak': None,
                'icon': 'sonora.png',
                # Sonora publishes its own single-app Flatpak repo instead of using
                # Flathub — installing straight from its .flatpakref URL adds that repo
                # (named "sonora") and installs the app in one step.
                'description': _('Native music streaming client for Apple Music, Spotify, YouTube Music, Deezer and local files'),
                'official': False,
                'check_path': '~/.local/share/flatpak/app/io.github.nolight132.sonora',
                'install_commands': [
                    'REAL_USER=$(getent passwd $PKEXEC_UID | cut -d: -f1)',
                    'sudo -u $REAL_USER flatpak install --user -y --noninteractive https://sonorahq.github.io/sonora/sonora.flatpakref'
                ],
                'uninstall_commands': [
                    'REAL_USER=$(getent passwd $PKEXEC_UID | cut -d: -f1)',
                    'sudo -u $REAL_USER flatpak uninstall --user -y io.github.nolight132.sonora',
                    'sudo -u $REAL_USER flatpak remote-delete --user sonora 2>/dev/null || true'
                ]
            },
            # Video
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
                'name': 'OpenShot',
                'package': 'openshot-qt',
                'flatpak': 'org.openshot.OpenShot',
                'icon': 'openshot.png',
                'description': _('Easy to use video editor'),
                'official': True
            },
            {
                'name': 'HandBrake',
                'package': 'handbrake',
                'flatpak': 'fr.handbrake.ghb',
                'icon': 'handbrake.png',
                'description': _('Open source video transcoder'),
                'official': True
            },
            {
                'name': 'Concat',
                'package': 'concat',
                'flatpak': None,
                'icon': 'concat.png',
                'description': _('Free, open-source video editor with local AI captioning and a native Rust engine'),
                'official': False,
                'install_commands': [
                    'CONCAT_URL=$(curl -s https://api.github.com/repos/jub0t/Concat/releases/latest | grep browser_download_url | grep linux-x86_64.deb | cut -d\\" -f4)',
                    'wget -q -O /tmp/concat.deb "$CONCAT_URL"',
                    'apt install -y /tmp/concat.deb',
                    'rm -f /tmp/concat.deb'
                ],
                'uninstall_commands': [
                    'apt remove -y concat'
                ]
            },
            {
                'name': 'FilmCraft',
                'package': 'filmcraft',
                'flatpak': None,
                'icon': 'filmcraft.png',
                'description': _('Clean-room Premiere Pro alternative written in Rust'),
                'official': False,
                'install_commands': [
                    'FILMCRAFT_URL=$(curl -s https://api.github.com/repos/storytold/filmcraft/releases/latest | grep browser_download_url | grep linux-x86_64.deb | cut -d\\" -f4)',
                    'wget -q -O /tmp/filmcraft.deb "$FILMCRAFT_URL"',
                    'apt install -y /tmp/filmcraft.deb',
                    'rm -f /tmp/filmcraft.deb'
                ],
                'uninstall_commands': [
                    'apt remove -y filmcraft'
                ]
            },
            {
                'name': 'EffectCraft',
                'package': 'effectcraft',
                'flatpak': None,
                'icon': 'effectcraft.png',
                'description': _('Clean-room After Effects alternative written in Rust'),
                'official': False,
                'install_commands': [
                    'EFFECTCRAFT_URL=$(curl -s https://api.github.com/repos/storytold/effectcraft/releases/latest | grep browser_download_url | grep linux-x86_64.deb | cut -d\\" -f4)',
                    'wget -q -O /tmp/effectcraft.deb "$EFFECTCRAFT_URL"',
                    'apt install -y /tmp/effectcraft.deb',
                    'rm -f /tmp/effectcraft.deb'
                ],
                'uninstall_commands': [
                    'apt remove -y effectcraft'
                ]
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
                'name': 'Drift',
                'package': None,
                'flatpak': 'org.cutwire.Drift',
                'icon': 'drift.png',
                'description': _('Edit and export videos easily'),
                'official': False
            },
            {
                'name': 'Prism',
                'package': None,
                'flatpak': 'org.cutwire.Prism',
                'icon': 'prism.png',
                'description': _('Trigger and mix live visuals'),
                'official': False
            },
            # Audio / DAW
            {
                'name': 'Audacity',
                'package': None,
                'flatpak': None,
                'icon': 'audacity.png',
                # Audacity 4 dropped its Debian package in favor of an official AppImage
                # only (confirmed on audacityteam.org/download/Linux and the GitHub
                # releases page — no .deb asset exists), so this follows the same
                # AppImage pattern as the other AppImage entries in this file instead
                # of apt. The release tag changes per version, so the asset URL is
                # resolved from the GitHub API rather than hardcoded.
                'description': _('Free and open-source audio editor'),
                'official': False,
                'check_path': '~/AppImages/audacity-linux-x86_64.AppImage',
                'install_commands': [
                    'REAL_HOME=$(getent passwd $PKEXEC_UID | cut -d: -f6)',
                    'REAL_USER=$(getent passwd $PKEXEC_UID | cut -d: -f1)',
                    'sudo -u $REAL_USER mkdir -p "$REAL_HOME/AppImages/.icons"',
                    'sudo -u $REAL_USER mkdir -p "$REAL_HOME/.local/share/applications"',
                    'AUDACITY_URL=$(curl -s https://api.github.com/repos/audacity/audacity/releases/latest | grep browser_download_url | grep linux-.*-x86_64.AppImage | cut -d\\" -f4)',
                    'wget -q -O "$REAL_HOME/AppImages/audacity-linux-x86_64.AppImage" "$AUDACITY_URL"',
                    'chmod +x "$REAL_HOME/AppImages/audacity-linux-x86_64.AppImage"',
                    f'cp {os.path.join(PROJECT_ROOT, "assets", "icons", "multimedia", "audacity.png")} "$REAL_HOME/AppImages/.icons/audacity.png"',
                    'chown -R $PKEXEC_UID:$PKEXEC_UID "$REAL_HOME/AppImages"',
                    "printf '[Desktop Entry]\\nType=Application\\nName=Audacity\\nExec=%s/AppImages/audacity-linux-x86_64.AppImage\\nIcon=%s/AppImages/.icons/audacity.png\\nCategories=AudioVideo;Audio;\\nComment=Free, open source, cross-platform audio editor\\nX-AppImage-Integrate=true\\n' \"$REAL_HOME\" \"$REAL_HOME\" | sudo -u $REAL_USER tee \"$REAL_HOME/.local/share/applications/audacity.desktop\" > /dev/null",
                ],
                'uninstall_commands': [
                    'REAL_HOME=$(getent passwd $PKEXEC_UID | cut -d: -f6)',
                    'rm -f "$REAL_HOME/AppImages/audacity-linux-x86_64.AppImage"',
                    'rm -f "$REAL_HOME/AppImages/.icons/audacity.png"',
                    'rm -f "$REAL_HOME/.local/share/applications/audacity.desktop"'
                ]
            },
            {
                'name': 'KutEditor',
                'package': 'kuteditor',
                'flatpak': None,
                'icon': 'kuteditor.png',
                'description': _('Native podcast editor: multitrack audio, AI transcription and Podcasting 2.0 chapters'),
                'official': True
            },
            {
                'name': 'LMMS',
                'package': None,
                'flatpak': 'io.lmms.LMMS',
                'icon': 'lmms.png',
                'description': _('Digital audio workstation'),
                'official': False
            },
            {
                'name': 'Mixxx',
                'package': 'mixxx',
                'icon': 'mixxx.png',
                'description': _('Professional DJ software'),
                'official': True
            },
            {
                'name': 'Bitwig Studio',
                'package': None,
                'flatpak': 'com.bitwig.BitwigStudio',
                'icon': 'bitwig-studio.png',
                'description': _('Professional digital audio workstation for music production'),
                'official': False
            },
            {
                'name': 'Reaper',
                'package': None,
                'flatpak': 'fm.reaper.Reaper',
                'icon': 'reaper.png',
                'description': _('Professional digital audio workstation and MIDI sequencer'),
                'official': False
            },
            {
                'name': 'Zrythm',
                'package': None,
                'flatpak': 'org.zrythm.Zrythm',
                'icon': 'zrythm.png',
                'description': _('Free and open-source digital audio workstation'),
                'official': False
            },
            {
                'name': 'Ardour',
                'package': None,
                'flatpak': 'org.ardour.Ardour',
                'icon': 'ardour.png',
                'description': _('Professional recording, editing and mixing DAW'),
                'official': False
            }
        ]
    },
    
    'office': {
        'title': _('Office'),
        'icon': 'office',
        'packages': [
            # Office suites
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
                'name': 'Calligra',
                'package': None,
                'flatpak': 'org.kde.calligra',
                'icon': 'calligra.png',
                'description': _('KDE office suite: word processor, spreadsheet and presentation'),
                'official': True
            },
            {
                'name': 'Collabora Office',
                'package': None,
                'flatpak': 'com.collaboraoffice.Office',
                'icon': 'collabora.png',
                'description': _('Enterprise-grade LibreOffice fork by Collabora'),
                'official': True
            },
            {
                'name': 'GenOffice',
                'package': 'genoffice',
                'flatpak': None,
                'icon': 'genoffice.png',
                'description': _('Open-source AI office suite: Docs, Sheets, Slides, PDF, HTML and Markdown'),
                'official': False,
                'install_commands': [
                    'wget -q -O /tmp/genoffice.deb https://genoffice.ai/download/linux-deb',
                    'apt install -y /tmp/genoffice.deb',
                    'rm -f /tmp/genoffice.deb'
                ]
            },
            # PDF
            {
                'name': 'Adobe Reader',
                'package': None,
                'flatpak': 'com.adobe.Reader',
                'icon': 'reader.png',
                'description': _('Adobe PDF reader'),
                'official': False
            },
            {
                'name': 'JoPDF',
                'package': 'jopdf',
                'flatpak': None,
                'icon': 'jopdf.png',
                'description': _('PDF editor: annotate, sign, fill forms and merge PDFs'),
                'official': False,
                'install_commands': [
                    'wget -q -O /tmp/jopdf.deb https://cdn.jopdf.com/download/jopdf/jopdf-linux-amd64_setup.deb',
                    'apt install -y /tmp/jopdf.deb',
                    'rm /tmp/jopdf.deb'
                ]
            },
            {
                'name': 'PrintCraft',
                'package': 'printcraft',
                'flatpak': None,
                'icon': 'printcraft.png',
                'description': _('Clean-room Acrobat alternative written in Rust'),
                'official': False,
                'install_commands': [
                    'PRINTCRAFT_URL=$(curl -s https://api.github.com/repos/storytold/pdfcraft/releases/latest | grep browser_download_url | grep linux-x86_64.deb | cut -d\\" -f4)',
                    'wget -q -O /tmp/printcraft.deb "$PRINTCRAFT_URL"',
                    'apt install -y /tmp/printcraft.deb',
                    'rm -f /tmp/printcraft.deb'
                ],
                'uninstall_commands': [
                    'apt remove -y printcraft'
                ]
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
                'name': 'GeForce NOW',
                'package': None,
                'flatpak': None,
                'icon': 'geforcenow.png',
                'description': _('NVIDIA cloud gaming — stream games from the cloud'),
                'official': False,
                'check_path': '~/.local/share/flatpak/app/com.nvidia.geforcenow',
                'install_commands': [
                    'REAL_USER=$(getent passwd $PKEXEC_UID | cut -d: -f1)',
                    'sudo -u $REAL_USER flatpak remote-add --user --if-not-exists GeForceNOW https://international.download.nvidia.com/GFNLinux/flatpak/geforcenow.flatpakrepo',
                    'sudo -u $REAL_USER flatpak install --user -y GeForceNOW com.nvidia.geforcenow'
                ],
                'uninstall_commands': [
                    'REAL_USER=$(getent passwd $PKEXEC_UID | cut -d: -f1)',
                    'sudo -u $REAL_USER flatpak uninstall --user -y com.nvidia.geforcenow'
                ]
            },
            {
                'name': 'ES-DE',
                'package': None,
                'icon': 'ES-DE.png',
                'description': _('Frontend for emulators with a modern interface'),
                'official': False,
                'check_path': '~/AppImages/ES-DE_x64.AppImage',
                'install_commands': [
                    'REAL_HOME=$(getent passwd $PKEXEC_UID | cut -d: -f6)',
                    'REAL_USER=$(getent passwd $PKEXEC_UID | cut -d: -f1)',
                    'sudo -u $REAL_USER mkdir -p "$REAL_HOME/AppImages/.icons"',
                    'wget -q -O "$REAL_HOME/AppImages/ES-DE_x64.AppImage" "https://gitlab.com/es-de/emulationstation-de/-/package_files/246875981/download"',
                    'chmod +x "$REAL_HOME/AppImages/ES-DE_x64.AppImage"',
                    f'cp {os.path.join(PROJECT_ROOT, "assets", "icons", "gaming", "ES-DE.png")} "$REAL_HOME/AppImages/.icons/ES-DE.png"',
                    'chown -R $PKEXEC_UID:$PKEXEC_UID "$REAL_HOME/AppImages"',
                    'sudo -u $REAL_USER mkdir -p "$REAL_HOME/.local/share/applications"',
                    "printf '[Desktop Entry]\\nName=ES-DE\\nExec=%s/AppImages/ES-DE_x64.AppImage\\nIcon=%s/AppImages/.icons/ES-DE.png\\nType=Application\\nCategories=Game;\\nComment=Frontend for emulators with a modern interface\\n' \"$REAL_HOME\" \"$REAL_HOME\" | sudo -u $REAL_USER tee \"$REAL_HOME/.local/share/applications/es-de.desktop\" > /dev/null"
                ],
                'uninstall_commands': [
                    'REAL_HOME=$(getent passwd $PKEXEC_UID | cut -d: -f6)',
                    'rm -f "$REAL_HOME/AppImages/ES-DE_x64.AppImage"',
                    'rm -f "$REAL_HOME/AppImages/.icons/ES-DE.png"',
                    'rm -f "$REAL_HOME/.local/share/applications/es-de.desktop"'
                ]
            },
            {
                'name': 'PPSSPP',
                'package': None,
                'flatpak': 'org.ppsspp.PPSSPP',
                'icon': 'ppsspp.png',
                'description': _('PSP emulator with high-quality rendering'),
                'official': False,
                'post_install_script': 'ppsspp-lutris-runner.sh'
            }
        ]
    },

    'app_management': {
        'title': _('App Management'),
        'icon': 'app_management',
        'packages': [
            {
                'name': 'Soplos WebApp Manager',
                'package': 'soplos-webapp-manager',
                'icon': 'soplos-webapps-manager.png',
                'description': _('Manage your web applications with ease'),
                'official': True
            },
            {
                'name': 'Soplos AppImage Manager',
                'package': 'soplos-appimage-manager',
                'icon': 'soplos-appimage-manager.png',
                'description': _('Manage and integrate AppImages on your system'),
                'official': True
            },
            {
                'name': 'Flatseal',
                'package': None,
                'flatpak': 'com.github.tchx84.Flatseal',
                'icon': 'flatseal.png',
                'description': _('Manage Flatpak permissions'),
                'official': False
            },
            {
                'name': 'Gear Lever',
                'package': None,
                'flatpak': 'it.mijorus.gearlever',
                'icon': 'gear-lever.png',
                'description': _('Manage AppImages effortlessly'),
                'official': False
            },
            {
                'name': 'Warehouse',
                'package': None,
                'flatpak': 'io.github.flattool.Warehouse',
                'icon': 'warehouse.png',
                'description': _('Manage and control your Flatpak apps and runtimes'),
                'official': False
            }
        ]
    },
    'downloads': {
        'title': _('Downloads'),
        'icon': 'downloads',
        'packages': [
            {
                'name': 'qBittorrent',
                'package': None,
                'flatpak': 'org.qbittorrent.qBittorrent',
                'icon': 'qbittorrent.png',
                'description': _('Free and open-source BitTorrent client'),
                'official': False
            },
            {
                'name': 'Transmission',
                'package': 'transmission-gtk',
                'icon': 'transmission.png',
                'description': _('Lightweight and easy-to-use BitTorrent client'),
                'official': False
            },
            {
                'name': 'JDownloader',
                'package': None,
                'flatpak': 'org.jdownloader.JDownloader',
                'icon': 'jdownloader.png',
                'description': _('Download manager for direct downloads, video sites and file hosts'),
                'official': False
            },
            {
                'name': 'Syncthing Tray',
                'package': None,
                'flatpak': 'io.github.martchus.syncthingtray',
                'icon': 'syncthing.png',
                'description': _('Tray application for Syncthing — sync files between devices'),
                'official': False
            }
        ]
    },
    'hardware': {
        'title': _('Hardware'),
        'icon': 'hardware',
        'packages': [
            {
                'name': 'Resources',
                'package': None,
                'flatpak': 'net.nokyan.Resources',
                'icon': 'resources.png',
                'description': _('Modern system monitor with detailed resource usage'),
                'official': False
            },
            {
                'name': 'LACT',
                'package': None,
                'flatpak': 'io.github.ilya_zlobintsev.LACT',
                'icon': 'lact.png',
                'description': _('GPU control center for AMD and NVIDIA on Linux'),
                'official': False
            },
            {
                'name': 'CPU Power',
                'package': 'cpupower-gui',
                'icon': 'cpupower.png',
                'description': _('Control the CPU frequency governor from a graphical interface'),
                'official': False,
                'install_commands': [
                    'apt install -y cpupower-gui linux-cpupower'
                ],
                'uninstall_commands': [
                    'apt remove -y cpupower-gui linux-cpupower'
                ]
            },
            {
                'name': 'amdgpu_top',
                'package': 'amdgpu-top',
                'icon': 'amdgpu-top.png',
                'description': _('Real-time AMD GPU usage monitor with detailed metrics'),
                'official': False,
                'install_commands': [
                    'AMDGPU_TOP_URL=$(curl -s https://api.github.com/repos/Umio-Yasuno/amdgpu_top/releases/latest | grep browser_download_url | grep amd64.deb | grep -v without_gui | cut -d\\" -f4)',
                    'wget -q --show-progress -O /tmp/amdgpu-top.deb "$AMDGPU_TOP_URL"',
                    'apt install -y /tmp/amdgpu-top.deb',
                    'rm -f /tmp/amdgpu-top.deb'
                ]
            },
            {
                'name': 'nvtop',
                'package': 'nvtop',
                'icon': 'nvtop.png',
                'description': _('GPU process monitor for NVIDIA, AMD and Intel'),
                'official': True
            },
            {
                'name': 'CoolerControl',
                'package': None,
                'flatpak': None,
                'icon': 'coolercontrol.png',
                'description': _('Fan and cooling control with a web interface'),
                'official': False,
                'check_path': '~/AppImages/CoolerControlD-x86_64.AppImage',
                'install_commands': [
                    f'bash {os.path.join(PROJECT_ROOT, "services", "coolercontrol-install.sh")} {os.path.join(PROJECT_ROOT, "assets", "icons", "hardware", "coolercontrol.png")}'
                ],
                'uninstall_commands': [
                    'REAL_HOME=$(getent passwd $PKEXEC_UID | cut -d: -f6)',
                    'rm -f "$REAL_HOME/AppImages/CoolerControlD-x86_64.AppImage"',
                    'rm -f "$REAL_HOME/AppImages/.icons/coolercontrol.png"',
                    'rm -f "$REAL_HOME/.local/share/applications/soplos-appimage-coolercontrold.desktop"',
                    'rm -f "$REAL_HOME/.local/share/applications/soplos-webapp-coolercontrol-ui-111987.desktop"',
                    'rm -rf "$REAL_HOME/.local/share/soplos-webapps/coolercontrol-ui-111987"'
                ]
            }
        ]
    },
    'files': {
        'title': _('Files'),
        'icon': 'files',
        'packages': [
            {
                'name': 'PeaZip',
                'package': None,
                'flatpak': 'io.github.peazip.PeaZip',
                'icon': 'peazip.png',
                'description': _('Free file archiver and extractor utility'),
                'official': False
            },
            {
                'name': 'FileZilla',
                'package': 'filezilla',
                'icon': 'filezilla.png',
                'description': _('Fast and reliable FTP, FTPS and SFTP client'),
                'official': False
            },
            {
                'name': 'GNOME Commander',
                'package': 'gnome-commander',
                'icon': 'gnome-commander.png',
                'description': _('Twin-panel file manager for GNOME'),
                'official': False
            },
            {
                'name': 'Double Commander',
                'package': None,
                'flatpak': None,
                'icon': 'doublecmd.png',
                'description': _('Twin-panel file manager with advanced features'),
                'official': False,
                'check_path': '~/AppImages/doublecmd-gtk-latest-x86_64.AppImage',
                'install_commands': [
                    'REAL_HOME=$(getent passwd $PKEXEC_UID | cut -d: -f6)',
                    'REAL_USER=$(getent passwd $PKEXEC_UID | cut -d: -f1)',
                    'sudo -u "$REAL_USER" mkdir -p "$REAL_HOME/AppImages/.icons"',
                    'sudo -u "$REAL_USER" mkdir -p "$REAL_HOME/.local/share/applications"',
                    'wget -q --show-progress -O "$REAL_HOME/AppImages/doublecmd-gtk-latest-x86_64.AppImage" "https://download.opensuse.org/repositories/home:/Alexx2000/AppImage/doublecmd-gtk-latest-x86_64.AppImage"',
                    'chmod +x "$REAL_HOME/AppImages/doublecmd-gtk-latest-x86_64.AppImage"',
                    f'cp {os.path.join(PROJECT_ROOT, "assets", "icons", "files", "doublecmd.png")} "$REAL_HOME/AppImages/.icons/doublecmd.png"',
                    'chown -R "$PKEXEC_UID:$PKEXEC_UID" "$REAL_HOME/AppImages"',
                    "printf '[Desktop Entry]\\nType=Application\\nName=Double Commander\\nExec=%s/AppImages/doublecmd-gtk-latest-x86_64.AppImage\\nIcon=%s/AppImages/.icons/doublecmd.png\\nCategories=FileManager;\\nComment=Twin-panel file manager with advanced features\\nX-AppImage-Integrate=true\\n' \"$REAL_HOME\" \"$REAL_HOME\" | sudo -u \"$REAL_USER\" tee \"$REAL_HOME/.local/share/applications/doublecmd.desktop\" > /dev/null",
                    'chown "$PKEXEC_UID:$PKEXEC_UID" "$REAL_HOME/.local/share/applications/doublecmd.desktop"',
                    'sudo -u "$REAL_USER" update-desktop-database "$REAL_HOME/.local/share/applications" 2>/dev/null || true'
                ],
                'uninstall_commands': [
                    'REAL_HOME=$(getent passwd $PKEXEC_UID | cut -d: -f6)',
                    'rm -f "$REAL_HOME/AppImages/doublecmd-gtk-latest-x86_64.AppImage"',
                    'rm -f "$REAL_HOME/AppImages/.icons/doublecmd.png"',
                    'rm -f "$REAL_HOME/.local/share/applications/doublecmd.desktop"'
                ]
            }
        ]
    },
    'remotes': {
        'title': _('Remote Desktops'),
        'icon': 'remotes',
        'packages': [
            {
                'name': 'Remmina',
                'package': None,
                'flatpak': 'org.remmina.Remmina',
                'icon': 'remmina.png',
                'description': _('Remote desktop client supporting RDP, VNC, SSH and more'),
                'official': True
            },
            {
                'name': 'RustDesk',
                'package': None,
                'flatpak': 'com.rustdesk.RustDesk',
                'icon': 'rustdesk.png',
                'description': _('Open-source remote desktop software, self-hostable'),
                'official': False
            },
            {
                'name': 'AnyDesk',
                'package': None,
                'flatpak': 'com.anydesk.Anydesk',
                'icon': 'anydesk.png',
                'description': _('Fast and secure remote desktop application'),
                'official': False
            },
            {
                'name': 'NoMachine',
                'package': None,
                'flatpak': 'com.nomachine.nxplayer',
                'icon': 'nomachine.png',
                'description': _('Remote desktop client for accessing NoMachine servers'),
                'official': False
            }
        ]
    },
    'virtual': {
        'title': _('Virtualization'),
        'icon': 'virtual',
        'packages': [
            {
                'name': 'VirtualBox',
                'package': 'virtualbox-7.2',
                'flatpak': None,
                'icon': 'virtualbox.png',
                'description': _('Full-featured virtual machine hypervisor by Oracle'),
                'official': False,
                'license_confirm': {
                    'title': _('This adds two repositories to your system'),
                    'body': _("Installing VirtualBox adds Oracle's own repository, plus Debian's trixie-security repository (needed because a dependency VirtualBox requires is no longer in this system's own suite). Both stay configured permanently after this — Uninstall removes them again. Continuing accepts this.")
                },
                'install_commands': [
                    'wget -qO- https://www.virtualbox.org/download/oracle_vbox_2016.asc | gpg --yes --output /usr/share/keyrings/oracle-virtualbox-2016.gpg --dearmor',
                    'CODENAME=$(apt-cache policy | grep o=Debian | grep -o "n=[a-z]*" | cut -d= -f2 | sort | uniq -c | sort -rn | head -1 | tr -dc "a-z") || true',
                    'case "$CODENAME" in bookworm|trixie|bullseye) ;; *) CODENAME="trixie" ;; esac',
                    'echo "deb [arch=amd64 signed-by=/usr/share/keyrings/oracle-virtualbox-2016.gpg] https://download.virtualbox.org/virtualbox/debian $CODENAME contrib" > /etc/apt/sources.list.d/virtualbox.list',
                    'if ! grep -rq "trixie-security" /etc/apt/sources.list.d/*.sources /etc/apt/sources.list.d/*.list 2>/dev/null; then printf \'Types: deb\\nURIs: https://security.debian.org/debian-security/\\nSuites: trixie-security\\nComponents: main\\nSigned-By: /usr/share/keyrings/debian-archive-keyring.gpg\\n\' > /etc/apt/sources.list.d/virtualbox-trixie-security.sources; fi',
                    'apt update',
                    'apt install -y virtualbox-7.2'
                ],
                'uninstall_commands': [
                    "apt purge -y 'virtualbox-*' 2>/dev/null || true",
                    'rm -f /etc/apt/sources.list.d/virtualbox.list /etc/apt/sources.list.d/virtualbox-trixie-security.sources /usr/share/keyrings/oracle-virtualbox-2016.gpg'
                ]
            },
            {
                'name': 'VirtualBox Extension Pack',
                'package': None,
                'flatpak': None,
                'icon': 'virtualbox.png',
                'description': _('USB 2.0/3.0, RDP, PXE boot and disk encryption support for VirtualBox'),
                'official': False,
                'check_path': '/usr/lib/virtualbox/ExtensionPacks/Oracle_VirtualBox_Extension_Pack',
                'license_confirm': {
                    'title': _("Accept Oracle's license"),
                    'body': _("The Extension Pack is distributed under Oracle's Personal Use and Evaluation License (PUEL), separate from VirtualBox's own open-source license. Continuing installs it and accepts that license.")
                },
                # The Extension Pack's version must match the installed VirtualBox version
                # exactly (VBoxManage refuses a mismatch), so it's detected at runtime
                # instead of pinned here. The license hash below is the real SHA-256 of
                # ExtPack-license.txt bundled inside the 7.2.18 pack (PUEL v12, 22 Jul
                # 2024), which is what VBoxManage's --accept-license expects.
                'install_commands': [
                    'VBOX_VERSION=$(VBoxManage --version 2>/dev/null | grep -oE "^[0-9]+\\.[0-9]+\\.[0-9]+")',
                    'if [ -z "$VBOX_VERSION" ]; then echo "Could not detect an installed VirtualBox version. Install VirtualBox first."; exit 1; fi',
                    'wget -q -O /tmp/vbox-extpack.vbox-extpack "https://download.virtualbox.org/virtualbox/$VBOX_VERSION/Oracle_VirtualBox_Extension_Pack-$VBOX_VERSION.vbox-extpack"',
                    'VBoxManage extpack install --replace --accept-license=eb31505e56e9b4d0fbca139104da41ac6f6b98f8e78968bdf01b1f3da3c4f9ae /tmp/vbox-extpack.vbox-extpack',
                    'rm -f /tmp/vbox-extpack.vbox-extpack'
                ],
                'uninstall_commands': [
                    'VBoxManage extpack uninstall "Oracle VirtualBox Extension Pack"'
                ]
            },
            {
                'name': 'VMware Workstation Pro',
                'package': None,
                'flatpak': None,
                'icon': 'vmware.png',
                'description': _("Broadcom's virtual machine hypervisor, with Soplos's kernel modules already integrated"),
                'official': False,
                'check_path': '/usr/bin/vmware',
                'uninstall_commands': [
                    'yes no | vmware-installer --uninstall-product vmware-workstation --console || true',
                    'apt-get remove -y soplos-vmware-modules || true'
                ]
            },
            {
                'name': 'virt-manager',
                'package': 'virt-manager',
                'icon': 'virtmanager.png',
                'description': _('Graphical tool for managing virtual machines via libvirt/QEMU'),
                'official': True
            },
            {
                'name': 'GNOME Boxes',
                'package': 'gnome-boxes',
                'icon': 'gnomeboxes.png',
                'description': _('Simple virtual machine and remote desktop viewer for GNOME'),
                'official': True
            },
            {
                'name': 'Waydroid',
                'package': 'waydroid',
                'flatpak': None,
                'icon': 'waydroid.png',
                'description': _('Android container for developing and testing Android apps'),
                'official': False,
                'install_commands': [
                    'curl -fsSL https://repo.waydro.id/waydroid.gpg -o /usr/share/keyrings/waydroid.gpg',
                    "echo 'deb [signed-by=/usr/share/keyrings/waydroid.gpg] https://repo.waydro.id/ trixie main' > /etc/apt/sources.list.d/waydroid.list",
                    'apt update',
                    'apt install -y waydroid'
                ],
                'uninstall_commands': [
                    "apt purge -y waydroid 2>/dev/null || true",
                    'rm -f /etc/apt/sources.list.d/waydroid.list /usr/share/keyrings/waydroid.gpg'
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
