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

mkdir -p "$USER_HOME/.config/autostart"


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


# Set standard execution permissions
chmod 755 "$DESKTOP_ICON"

# Mark the file as trusted on modern desktop environments
if command -v gio &> /dev/null; then
    # Attempt trust marking via gio custom metadata
    gio set "$DESKTOP_ICON" custom::trusted true 2>/dev/null || true
    # Enable trusted launch for GNOME
    gio set "$DESKTOP_ICON" metadata::trusted true 2>/dev/null || true
fi

# If the file exists on the user's Desktop, remove the launch restrictions
if [ -f "$DESKTOP_ICON" ]; then
    gio set "$DESKTOP_ICON" metadata::trusted yes 2>/dev/null || true
fi

echo "[SUCCESS] Desktop shortcut successfully created at: $DESKTOP_ICON"

