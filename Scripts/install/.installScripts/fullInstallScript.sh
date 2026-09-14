#!/bin/bash
set -e

# Ensure the script is run with root privileges
if [ "$EUID" -ne 0 ]; then
  echo "Error: Please run this script with sudo."
  exit 1
fi

# Locate current script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALLATION_DIRECTORY="/opt"
PROGRAM_DIRECTORY="$(dirname "$(dirname "$(dirname "$SCRIPT_DIR")")")"
NAME_PROGRAM_DIRECTORY="${PROGRAM_DIRECTORY##*/}"
TARGET_DIR="$INSTALLATION_DIRECTORY/$NAME_PROGRAM_DIRECTORY"
SCRIPT_DIR_TARGHET="$TARGET_DIR/Scripts/install/.installScripts"

echo "[INFO] Script Directory:          $SCRIPT_DIR"
echo "[INFO] Program Directory:         $PROGRAM_DIRECTORY"
echo "[INFO] Installation Directory:    $INSTALLATION_DIRECTORY"
echo "[INFO] Name of Program Directory: $NAME_PROGRAM_DIRECTORY"
echo "[INFO] Target Directory:          $TARGET_DIR"

echo "=================================================="
echo " Starting Full Automatic Installation"
echo " Target Directory: $INSTALLATION_DIRECTORY"
echo "=================================================="

echo ""
echo "=== 1. Moving the application to the installation directory ==="
"$SCRIPT_DIR/installationDirectory.sh" "$PROGRAM_DIRECTORY" "$INSTALLATION_DIRECTORY"
echo "--> Application moved successfully!"

echo ""
echo "=== 2. Installing system packages and Docker ==="
"$SCRIPT_DIR_TARGHET/installSystemPakageAndDocker.sh"
echo "--> System packages and Docker installed successfully!"

echo ""
echo "=== 3. Setting up Python environments and Docker container ==="
"$SCRIPT_DIR_TARGHET/setupApplication.sh" "$TARGET_DIR"
echo "--> Application setup completed!"

echo ""
echo "=== 4. Installing third-party software ==="
"$SCRIPT_DIR_TARGHET/installThirdPartSoftware.sh"
echo "--> All third-party software installed!"

echo ""
echo "=== 5. Customizing Ubuntu environment ==="
"$SCRIPT_DIR_TARGHET/customizeUbuntu.sh"
echo "--> Ubuntu customization applied successfully!"

echo ""
echo "=== 6. Configuring auto-start on boot ==="
"$SCRIPT_DIR_TARGHET/autoStartOnBoot.sh" "$TARGET_DIR"
echo "--> Auto-start configuration completed!"

echo ""
echo "=================================================="
echo " AUTOMATIC INSTALLATION COMPLETED SUCCESSFULLY!"
echo "=================================================="