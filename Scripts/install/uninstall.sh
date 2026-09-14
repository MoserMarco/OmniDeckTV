#!/bin/bash
# Exit immediately if a command exits with a non-zero status
set -e

echo "--------------------------------------------------"
echo " Starting uninstallation of TVControlHub..."
echo "--------------------------------------------------"

# Stop and disable the systemd service if it is running
if systemctl is-active --quiet tvcontrolhub.service 2>/dev/null; then
    echo "Stopping tvcontrolhub systemd service..."
    systemctl stop tvcontrolhub.service || true
    systemctl disable tvcontrolhub.service || true
fi

# Remove systemd service file
SERVICE_FILE="/etc/systemd/system/tvcontrolhub.service"
if [ -f "$SERVICE_FILE" ]; then
    echo "Removing systemd service file..."
    rm -f "$SERVICE_FILE"
    echo "Reloading systemd manager configuration..."
    systemctl daemon-reload
else
    echo "Systemd service file not found. Skipping."
fi

# Remove binary from /usr/local/bin
BINARY_FILE="/usr/local/bin/tvcontrolhub"
if [ -f "$BINARY_FILE" ]; then
    echo "Removing executable from /usr/local/bin..."
    rm -f "$BINARY_FILE"
else
    echo "Executable not found in /usr/local/bin. Skipping."
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