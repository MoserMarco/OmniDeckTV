#!/bin/bash
INSTALLATION_DIRECTORY=$1

if [ -n "$SUDO_USER" ]; then
    USER_HOME=$(getent passwd "$SUDO_USER" | cut -d: -f6)
else
    USER_HOME="$HOME"
fi

SERVICE_FILE="$USER_HOME/.config/autostart/omnidecktv.desktop"
DESKTOP_ICON="$USER_HOME/Desktop/omnidecktv.desktop"
DESKTOP_ICON_IMAGE="$INSTALLATION_DIRECTORY/SmartTVApp/images/Icon.png"


ln -sf "$INSTALLATION_DIRECTORY/Scripts/install/run_all.sh" /usr/local/bin/omnidecktv

echo "--> Configuring automatic startup at boot..."

mkdir -p "$USER_HOME/.config/autostart"


cat << EOL > "$SERVICE_FILE"
[Desktop Entry]
Type=Application
Name=OmniDeckTV
Exec=/usr/local/bin/omnidecktv
Terminal=false
X-GNOME-Autostart-enabled=true
EOL


echo "[SUCCESS] The omnidecktv service is configured and started!"

echo "--> Creating icon in the desktop"
# Create the .desktop file with absolute paths
cat << EOL > "$DESKTOP_ICON"
[Desktop Entry]
Version=1.0
Type=Application
Name=OmniDeckTV
Exec=/usr/local/bin/omnidecktv
Icon=$DESKTOP_ICON_IMAGE
Terminal=false
EOL


# Set standard execution permissions
chmod 755 "$DESKTOP_ICON"



echo "[SUCCESS] Desktop shortcut successfully created at: $DESKTOP_ICON"

