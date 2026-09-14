#!/bin/bash
set -e

echo "=== Customizing Ubuntu Desktop Settings ==="

# 1. Enable Dark Mode
echo "--> Enabling Dark Mode..."
gsettings set org.gnome.desktop.interface color-scheme 'prefer-dark'
# Legacy support for GTK3/4 applications
gsettings set org.gnome.desktop.interface gtk-theme 'Yaru-dark'

# 2. Configure Dash (Dock) Favorites
echo "--> Configuring Dash applications..."

# Ordered list of .desktop launchers:
# 1. Google Chrome
# 2. Terminal
# 3. Files (Nautilus)
# 4. Settings
FAVORITES="['google-chrome.desktop', 'org.gnome.Terminal.desktop', 'org.gnome.Nautilus.desktop', 'org.gnome.Settings.desktop']"

gsettings set org.gnome.shell favorite-apps "$FAVORITES"

echo "=== Desktop setup completed successfully! ==="