#!/bin/bash
# Exit immediately if a command exits with a non-zero status
set -e

echo "--------------------------------------------------"
echo " Starting uninstallation of TVControlHub..."
echo "--------------------------------------------------"




# Remove binary from /usr/local/bin
BINARY_FILE="/usr/local/bin/tvcontrolhub"
if [ -f "$BINARY_FILE" ]; then
    echo "Removing executable from /usr/local/bin..."
    rm -f "$BINARY_FILE"
else
    echo "Executable not found in /usr/local/bin. Skipping."
fi

# Remove Desktop Icon from $HOME/Desktop/tvcontrolhub.desktop
DESKTOP_ICON="$HOME/Desktop/tvcontrolhub.desktop"
if [ -f "$DESKTOP_ICON" ]; then
    echo "Removing executable from $DESKTOP_ICON..."
    rm -f "$DESKTOP_ICON"
else
    echo "Executable not found in $DESKTOP_ICON. Skipping."
fi

# Remove Autoboot Service from  $HOME/.config/autostart/tvcontrolhub.desktop
AUTOBOOT_SERVICE="$HOME/.config/autostart/tvcontrolhub.desktop"
if [ -f "$AUTOBOOT_SERVICE" ]; then
    echo "Removing executable from $AUTOBOOT_SERVICE..."
    rm -f "$AUTOBOOT_SERVICE"
else
    echo "Executable not found in $AUTOBOOT_SERVICE. Skipping."
fi

# Determine the program directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROGRAM_DIRECTORY="$(dirname "$(dirname "$(dirname "$SCRIPT_DIR")")")"

# Remove application directory without interactive prompts
if [ -d "$PROGRAM_DIRECTORY" ]; then
    echo "Removing application directory at: $PROGRAM_DIRECTORY"
    # Note: Using -rf instead of -ri to avoid prompt spam, -f avoids errors if already gone
    rm -rf "$PROGRAM_DIRECTORY"
else
    echo "Application directory not found. Skipping."
fi


echo "--------------------------------------------------"
echo " TVControlHub has been successfully uninstalled."
echo "--------------------------------------------------"