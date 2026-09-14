#!/bin/bash
set -e

# Ensure the script is run with root privileges
if [ "$EUID" -ne 0 ]; then
  echo "Error: Please run this script with sudo."
  exit 1
fi

# Find the directory where THIS script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"


echo "=== 1. Making the development scripts executable ==="
# Grant execution permissions (+x is safer than 700 and doesn't require sudo)
chmod +x "$SCRIPT_DIR"/*.sh
chmod +x "$SCRIPT_DIR"/.installScripts/*.sh 2>/dev/null || true
echo "--> All development scripts are now executable."

show_menu() {
    clear
    echo "=================================================="
    echo "        TVControlHub Installation Menu            "
    echo "=================================================="
    echo " 1) Automatic Installation (Recommended)"
    echo "    - Full setup: apps, Docker, theme & autostart"
    echo ""
    echo " 2) Custom Installation"
    echo "    - Choose step-by-step what to install"
    echo ""
    echo " 3) Exit"
    echo "=================================================="
    read -p "Select an option [1-3]: " choice
}

show_menu

case $choice in
    1)
        echo ""
        echo "Starting Automatic Full Installation..."
        "$SCRIPT_DIR/.installScripts/fullInstallScript.sh" --full
        ;;
    2)
        echo ""
        echo "Starting Custom Installation..."
        "$SCRIPT_DIR/.installScripts/customInstallScript.sh" --full
        ;;
    3)
        echo "Installation canceled."
        exit 0
        ;;
    *)
        echo "Invalid option. Exiting."
        exit 1
        ;;
esac