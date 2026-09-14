#!/bin/bash
set -e

echo "=== Installing Third-party Software ==="

# Update package lists
sudo apt update


# Install Google Chrome
echo "--> Installing Chrome..."
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O /tmp/google-chrome-stable_current_amd64.deb
sudo apt install -y /tmp/google-chrome-stable_current_amd64.deb
rm -f /tmp/google-chrome-stable_current_amd64.deb

# Setup Flathub repository
echo "--> Adding Flathub repository..."
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo

# Install Flatpak apps
echo "--> Installing RetroArch..."
flatpak install -y flathub org.libretro.RetroArch

echo "--> Installing Kodi..."
flatpak install -y flathub tv.kodi.Kodi

echo "=== Installation Completed Successfully! ==="