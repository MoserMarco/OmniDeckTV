#!/bin/bash
set -e

# Get information about the user who initiated sudo
USER_ID=$(id -u "$SUDO_USER")

# Define the necessary graphical environment variables for gsettings
export XDG_RUNTIME_DIR="/run/user/$USER_ID"
export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/$USER_ID/bus"
export DISPLAY=":0"

echo "=== Customizing Ubuntu Desktop Settings ==="

# 1. Enable Dark Mode
echo "--> Enabling Dark Mode..."
sudo -u "$SUDO_USER" env XDG_RUNTIME_DIR="$XDG_RUNTIME_DIR" DBUS_SESSION_BUS_ADDRESS="$DBUS_SESSION_BUS_ADDRESS" DISPLAY="$DISPLAY" gsettings set org.gnome.desktop.interface color-scheme 'prefer-dark'
# Legacy support for GTK3/4 applications
sudo -u "$SUDO_USER" env XDG_RUNTIME_DIR="$XDG_RUNTIME_DIR" DBUS_SESSION_BUS_ADDRESS="$DBUS_SESSION_BUS_ADDRESS" DISPLAY="$DISPLAY" gsettings set org.gnome.desktop.interface gtk-theme 'Yaru-dark'

# 2. Configure Dash (Dock) Favorites
echo "--> Configuring Dash applications..."
FAVORITES="['google-chrome.desktop', 'org.gnome.Ptyxis.desktop', 'org.gnome.Nautilus.desktop', 'org.gnome.Settings.desktop']"

sudo -u "$SUDO_USER" env XDG_RUNTIME_DIR="$XDG_RUNTIME_DIR" DBUS_SESSION_BUS_ADDRESS="$DBUS_SESSION_BUS_ADDRESS" DISPLAY="$DISPLAY" gsettings set org.gnome.shell favorite-apps "$FAVORITES"

echo "=== Desktop setup completed successfully! ==="