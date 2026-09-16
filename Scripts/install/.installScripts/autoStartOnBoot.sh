#!/bin/bash
INSTALLATION_DIRECTORY=$1

if [ -n "$SUDO_USER" ]; then
    USER_HOME=$(getent passwd "$SUDO_USER" | cut -d: -f6)
else
    USER_HOME="$HOME"
fi

SERVICE_FILE="$USER_HOME/.config/autostart/tvcontrolhub.desktop"
DESKTOP_ICON="$USER_HOME/Desktop/tvcontrolhub.desktop"
DESKTOP_ICON_IMAGE="$INSTALLATION_DIRECTORY/SmartTVApp/images/Icon.png"
echo "$SERVICE_FILE"
echo "$DESKTOP_ICON"
echo "$DESKTOP_ICON_IMAGE"

ln -sf "$INSTALLATION_DIRECTORY/Scripts/install/run_all.sh" /usr/local/bin/tvcontrolhub

echo "--> Configuring automatic startup at boot..."

mkdir -p "$HOME/.config/autostart"


cat << EOL > "$SERVICE_FILE"
[Desktop Entry]
Type=Application
Name=TV Control Hub
Exec=/usr/local/bin/tvcontrolhub
Terminal=false
X-GNOME-Autostart-enabled=true
EOL


echo "[SUCCESS] The tvcontrolhub service is configured and started!"

echo "--> Creating icon in the desktop"
# Create the .desktop file with absolute paths
cat << EOL > "$DESKTOP_ICON"
[Desktop Entry]
Version=1.0
Type=Application
Name=TV Control Hub
Exec=/usr/local/bin/tvcontrolhub
Icon=$DESKTOP_ICON_IMAGE
Terminal=false
EOL

# Set proper security permissions (resolves "Invalid Permissions")
chmod 755 "$DESKTOP_ICON"

# Authorize the shortcut (bypasses "Allow Launching" right-click step)
if [ -n "$SUDO_USER" ]; then
    chown "$SUDO_USER:$SUDO_USER" "$DESKTOP_ICON"


    sudo -u "$SUDO_USER" DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/$(id -u "$SUDO_USER")/bus" gio trust "$DESKTOP_ICON" 2>/dev/null || true
else
    gio trust "$DESKTOP_ICON" 2>/dev/null || true
fi

echo "[SUCCESS] Desktop shortcut successfully created at: $DESKTOP_ICON"

