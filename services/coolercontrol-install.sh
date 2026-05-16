#!/bin/bash
# Soplos Linux - CoolerControl installer
# Creates AppImage entry (Soplos AppImage Manager) + WebApp entry (Soplos WebApp Manager)

REAL_HOME=$(getent passwd "$PKEXEC_UID" | cut -d: -f6)
REAL_USER=$(getent passwd "$PKEXEC_UID" | cut -d: -f1)
ICON_SRC="$1"
WEBAPP_ID="coolercontrol-ui-111987"
WEBAPP_PROFILE="$REAL_HOME/.local/share/soplos-webapps/$WEBAPP_ID"
APPIMAGE_URL="https://gitlab.com/coolercontrol/coolercontrol/-/releases/4.1.0/downloads/packages/CoolerControlD-x86_64.AppImage"

# ── Directories ────────────────────────────────────────────────
sudo -u "$REAL_USER" mkdir -p "$REAL_HOME/AppImages/.icons"
sudo -u "$REAL_USER" mkdir -p "$REAL_HOME/.local/share/applications"
sudo -u "$REAL_USER" mkdir -p "$WEBAPP_PROFILE"

# ── Download AppImage ──────────────────────────────────────────
wget -q --show-progress -O "$REAL_HOME/AppImages/CoolerControlD-x86_64.AppImage" "$APPIMAGE_URL"
chmod +x "$REAL_HOME/AppImages/CoolerControlD-x86_64.AppImage"
cp "$ICON_SRC" "$REAL_HOME/AppImages/.icons/coolercontrol.png"
chown -R "$PKEXEC_UID:$PKEXEC_UID" "$REAL_HOME/AppImages"

# ── AppImage .desktop (Soplos AppImage Manager format) ─────────
cat > "$REAL_HOME/.local/share/applications/soplos-appimage-coolercontrold.desktop" << DESKTOP
[Desktop Entry]
Type=Application
Name=CoolerControl
Exec=pkexec $REAL_HOME/AppImages/CoolerControlD-x86_64.AppImage
TryExec=$REAL_HOME/AppImages/CoolerControlD-x86_64.AppImage
Icon=$REAL_HOME/AppImages/.icons/coolercontrol.png
Categories=System;
Comment=Fan and cooling control daemon
X-AppImage-RunAsRoot=true
X-AppImage-Integrate=true
DESKTOP
chown "$PKEXEC_UID:$PKEXEC_UID" "$REAL_HOME/.local/share/applications/soplos-appimage-coolercontrold.desktop"

# ── Detect browser ─────────────────────────────────────────────
BROWSER_CMD=""
BROWSER_EXEC_LINE=""
STARTUP_CLASS="soplos-webapp-$WEBAPP_ID"

# System browsers (Chromium-based preferred for --app= mode)
for b in chromium chromium-browser brave-browser google-chrome vivaldi; do
    if command -v "$b" &>/dev/null; then
        BROWSER_CMD="$b"
        break
    fi
done

if [ -n "$BROWSER_CMD" ]; then
    BROWSER_EXEC_LINE="env CHROME_DESKTOP=soplos-webapp-$WEBAPP_ID.desktop $BROWSER_CMD --ozone-platform-hint=auto --wayland-app-id=soplos-webapp-$WEBAPP_ID --class=soplos-webapp-$WEBAPP_ID --name=soplos-webapp-$WEBAPP_ID --wm-class=soplos-webapp-$WEBAPP_ID --user-data-dir=$WEBAPP_PROFILE --app=http://localhost:11987/"
    STARTUP_CLASS="chrome-localhost__-Default"
else
    # Flatpak Chromium
    if sudo -u "$REAL_USER" flatpak info org.chromium.Chromium &>/dev/null; then
        BROWSER_EXEC_LINE="env CHROME_DESKTOP=soplos-webapp-$WEBAPP_ID.desktop flatpak run org.chromium.Chromium --ozone-platform-hint=auto --wayland-app-id=soplos-webapp-$WEBAPP_ID --class=soplos-webapp-$WEBAPP_ID --name=soplos-webapp-$WEBAPP_ID --wm-class=soplos-webapp-$WEBAPP_ID --user-data-dir=$WEBAPP_PROFILE --app=http://localhost:11987/"
        STARTUP_CLASS="chrome-localhost__-Default"
    # Firefox
    elif command -v firefox &>/dev/null; then
        BROWSER_EXEC_LINE="env MOZ_APP_REMOTINGNAME=soplos-webapp-$WEBAPP_ID firefox -no-remote -new-instance -profile $WEBAPP_PROFILE -class soplos-webapp-$WEBAPP_ID -name soplos-webapp-$WEBAPP_ID http://localhost:11987/"
    # Flatpak Firefox
    elif sudo -u "$REAL_USER" flatpak info org.mozilla.firefox &>/dev/null; then
        BROWSER_EXEC_LINE="env MOZ_APP_REMOTINGNAME=soplos-webapp-$WEBAPP_ID flatpak run org.mozilla.firefox -no-remote -new-instance -profile $WEBAPP_PROFILE -class soplos-webapp-$WEBAPP_ID -name soplos-webapp-$WEBAPP_ID http://localhost:11987/"
    else
        # Fallback: xdg-open
        BROWSER_EXEC_LINE="xdg-open http://localhost:11987/"
    fi
fi

# ── WebApp .desktop (Soplos WebApp Manager format) ─────────────
cat > "$REAL_HOME/.local/share/applications/soplos-webapp-$WEBAPP_ID.desktop" << DESKTOP
[Desktop Entry]
Version=1.0
Name=CoolerControl UI
Comment=Soplos WebApp for CoolerControl UI
Exec=$BROWSER_EXEC_LINE
Terminal=false
X-MultipleArgs=false
Type=Application
Icon=$REAL_HOME/AppImages/.icons/coolercontrol.png
Categories=System;
StartupWMClass=$STARTUP_CLASS
StartupNotify=true
X-Soplos-Navbar=false
X-Soplos-ExtraParams=
X-Soplos-Incognito=false
DESKTOP
chown "$PKEXEC_UID:$PKEXEC_UID" "$REAL_HOME/.local/share/applications/soplos-webapp-$WEBAPP_ID.desktop"
chown -R "$PKEXEC_UID:$PKEXEC_UID" "$WEBAPP_PROFILE"

sudo -u "$REAL_USER" update-desktop-database "$REAL_HOME/.local/share/applications" 2>/dev/null || true

echo "[OK] CoolerControl installed. AppImage and WebApp entries created."
