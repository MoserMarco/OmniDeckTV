#!/bin/bash
# Exit immediately if a command exits with a non-zero status
set -e

# Ensure the script is run with root privileges
if [ "$EUID" -ne 0 ]; then
  echo "Error: Please run this script with sudo."
  exit 1
fi

echo "--------------------------------------------------"
echo " Starting uninstallation of TVControlHub..."
echo "--------------------------------------------------"

if [ -n "$SUDO_USER" ]; then
    USER_HOME=$(getent passwd "$SUDO_USER" | cut -d: -f6)
else
    USER_HOME="$HOME"
fi


# Remove binary from /usr/local/bin
BINARY_FILE="/usr/local/bin/tvcontrolhub"
if [ -f "$BINARY_FILE" ]; then
    echo "Removing executable from /usr/local/bin..."
    rm -f "$BINARY_FILE"
else
    echo "Executable not found in /usr/local/bin. Skipping."
fi

# Remove Desktop Icon from $HOME/Desktop/tvcontrolhub.desktop
DESKTOP_ICON="$USER_HOME/Desktop/tvcontrolhub.desktop"
if [ -f "$DESKTOP_ICON" ]; then
    echo "Removing executable from $DESKTOP_ICON..."
    rm -f "$DESKTOP_ICON"
else
    echo "Executable not found in $DESKTOP_ICON. Skipping."
fi

# Remove Autoboot Service from  $HOME/.config/autostart/tvcontrolhub.desktop
AUTOBOOT_SERVICE="$USER_HOME/.config/autostart/tvcontrolhub.desktop"
if [ -f "$AUTOBOOT_SERVICE" ]; then
    echo "Removing executable from $AUTOBOOT_SERVICE..."
    rm -f "$AUTOBOOT_SERVICE"
else
    echo "Executable not found in $AUTOBOOT_SERVICE. Skipping."
fi

#Remove Docker container and image
CONTAINER_NAME="remotecontrol"
IMAGE_NAME="marcomoser/remotecontrol:latest"

docker rm -f "$CONTAINER_NAME" 2>/dev/null || true

docker rmi -f "$IMAGE_NAME" 2>/dev/null || true


# Determine the program directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROGRAM_DIRECTORY="$(dirname "$(dirname "$SCRIPT_DIR")")"

# Remove application directory without interactive prompts
if [ -d "$PROGRAM_DIRECTORY" ]; then
    echo "Removing application directory at: $PROGRAM_DIRECTORY"
    # Note: Using -rf instead of -ri to avoid prompt spam, -f avoids errors if already gone
    rm -rf "$PROGRAM_DIRECTORY"
else
    echo "Application directory not found. Skipping."
fi

#Uninstall third-party software
echo "During the installation phase, you may have installed some third-party software."
echo "Mandatory software installed: Docker"
echo "Optional applications installed: Chrome, Kodi, RetroArch"
echo "In this phase, you can choose whether you want to uninstall this third-party software or keep it on your system."

uninstall_program() {
    local program="$1"

    # Converte il nome in minuscolo per rendere la ricerca case-insensitive
    local prog_lower=$(echo "$program" | tr '[:upper:]' '[:lower:]')

    case "$prog_lower" in
        "docker")
            echo "[+] Removing Docker..."
            # 1. Stop Docker and Containerd services
            sudo systemctl stop docker 2>/dev/null || true
            sudo systemctl stop containerd 2>/dev/null || true

            # 2. Purge installed packages and their configuration files
            sudo apt-get purge -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin 2>/dev/null || true

            # 3. Remove the APT repository source file and GPG key added during installation
            sudo rm -f /etc/apt/sources.list.d/docker.sources
            sudo rm -f /etc/apt/keyrings/docker.asc

            # 4. Delete Docker data directories (images, containers, volumes, and configurations)
            sudo rm -rf /var/lib/docker
            sudo rm -rf /var/lib/containerd
            sudo rm -rf /etc/docker

            # 5. Remove unused dependencies and update the package index
            sudo apt-get autoremove -y 2>/dev/null || true
            sudo apt-get update 2>/dev/null || true
            ;;

        "chrome"|"google-chrome")
            echo "[+] Removing Google Chrome..."

            # 1. Purge the Chrome package and its configurations
            sudo apt-get purge -y google-chrome-stable 2>/dev/null || true

            # 2. Remove the APT repository list and GPG key automatically added by Google
            sudo rm -f /etc/apt/sources.list.d/google-chrome.list
            sudo rm -f /etc/apt/trusted.gpg.d/google-chrome.gpg 2>/dev/null || true

            # 3. Clean up leftover dependencies and refresh apt index
            sudo apt-get autoremove -y 2>/dev/null || true
            sudo apt-get update 2>/dev/null || true
            ;;

        "kodi")
            echo "[+] Removing Kodi (Flatpak)..."
            flatpak uninstall --delete-data -y tv.kodi.Kodi 2>/dev/null || true
            ;;

        "retroarch")
            echo "[+] Removing RetroArch (Flatpak)..."
            flatpak uninstall --delete-data -y org.libretro.RetroArch 2>/dev/null || true
            ;;

        *)
            echo "[-] Error: Program '$program' is not recognized by the uninstaller."
            return 1
            ;;
    esac

    echo "[✓] $program successfully processed."
}


APP_LIST="Docker Chrome Kodi RetroArch"

# Loop through each installed application
for APP in $APP_LIST; do
    echo ""
    # Prompt the user for confirmation
    read -p "Do you want to uninstall '$APP'? [Y/N]: " CHOICE

    # Convert response to lowercase
    CHOICE=$(echo "$CHOICE" | tr '[:upper:]' '[:lower:]')

    if [ "$CHOICE" = "y" ] || [ "$CHOICE" = "yes" ]; then
        echo "Uninstalling $APP..."
        # Uninstall the app and delete associated user data
        uninstall_program "$APP"
        echo "[✓] $APP removed successfully."
    else
        echo "Keeping: $APP"
    fi
done

echo ""
echo "=========================================="
# Clean up leftover unused runtimes and dependencies
echo "Cleaning up unused dependencies and runtimes..."
flatpak uninstall --unused -y

apt update -y
apt upgrade -y
echo "--------------------------------------------------"
echo " TVControlHub has been successfully uninstalled."
echo "--------------------------------------------------"