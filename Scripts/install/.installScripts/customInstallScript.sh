#!/bin/bash
set -e

# Ensure the script is run with root privileges
if [ "$EUID" -ne 0 ]; then
  echo "Error: Please run this script with sudo."
  exit 1
fi



# Helper function to ask user confirmation for optional steps
confirm_step() {
  local prompt_message="$1"
  while true; do
    read -p "$prompt_message (y/n): " choice
    case "$choice" in
      [Yy]* ) return 0 ;;
      [Nn]* ) return 1 ;;
      * ) echo "Please answer yes (y) or no (n)." ;;
    esac
  done
}

echo "=================================================="
echo "          SmartTV Suite Installation              "
echo "=================================================="

# Prompt user for installation directory
DEFAULT_DIR="/opt"
read -p "Enter installation directory [$DEFAULT_DIR]: " USER_DIR


# Locate current script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALLATION_DIRECTORY="${USER_DIR:-$DEFAULT_DIR}"
PROGRAM_DIRECTORY="$(dirname "$(dirname "$(dirname "$SCRIPT_DIR")")")"
NAME_PROGRAM_DIRECTORY="${PROGRAM_DIRECTORY##*/}"
TARGET_DIR="$INSTALLATION_DIRECTORY/$NAME_PROGRAM_DIRECTORY"
SCRIPT_DIR_TARGHET="$TARGET_DIR/Scripts/install/.installScripts"

echo "[INFO] Script Directory:          $SCRIPT_DIR"
echo "[INFO] Program Directory:         $PROGRAM_DIRECTORY"
echo "[INFO] Installation Directory:    $INSTALLATION_DIRECTORY"
echo "[INFO] Name of Program Directory: $NAME_PROGRAM_DIRECTORY"
echo "[INFO] Target Directory:          $TARGET_DIR"
echo "[INFO] Script Directory Target:   $SCRIPT_DIR_TARGHET"

echo ""
echo "Target Directory set to: $INSTALLATION_DIRECTORY"
echo "=================================================="

# Mandatory Steps Confirmation (1, 2, 3)
echo ""
echo "Steps 1, 2, and 3 are MANDATORY for the application to function."
if ! confirm_step "Proceed with the mandatory installation steps?"; then
  echo "Installation aborted by user."
  exit 0
fi

# --- MANDATORY STEPS ---

# Step 1: Move Application
echo ""
echo "=== 1. Moving application files (Mandatory) ==="
"$SCRIPT_DIR/installationDirectory.sh" "$PROGRAM_DIRECTORY" "$INSTALLATION_DIRECTORY"
echo "--> Application moved successfully!"

# Step 2: System Packages & Docker
echo ""
echo "=== 2. Installing system packages and Docker (Mandatory) ==="
"$SCRIPT_DIR_TARGHET/installSystemPakageAndDocker.sh"
echo "--> System packages and Docker installed successfully!"

# Step 3: Application Setup
echo ""
echo "=== 3. Setting up Python environments and Docker container (Mandatory) ==="
"$SCRIPT_DIR_TARGHET/setupApplication.sh" "$TARGET_DIR"
echo "--> Application setup completed!"


# --- OPTIONAL STEPS ---

# Step 4: Third-Party Software
echo ""
echo "=== 4. Installing third-party software (Optional) ==="
if confirm_step "Do you want to install third-party applications?"; then
  "$SCRIPT_DIR_TARGHET/installThirdPartSoftware.sh"
  echo "--> All third-party software installed!"
else
  echo "--> Skipped step 4."
fi

# Step 5: Ubuntu Customization
echo ""
echo "=== 5. Customizing Ubuntu environment (Optional) ==="
if confirm_step "Do you want to apply Ubuntu desktop customizations (dark theme & dock)?"; then
  "$SCRIPT_DIR_TARGHET/customizeUbuntu.sh"
  echo "--> Ubuntu customization applied successfully!"
else
  echo "--> Skipped step 5."
fi

# Step 6: Auto-Start on Boot
echo ""
echo "=== 6. Configuring auto-start on boot (Optional) ==="
if confirm_step "Do you want the application to start automatically on system boot?"; then
  "$SCRIPT_DIR_TARGHET/autoStartOnBoot.sh" "$TARGET_DIR"
  echo "--> Auto-start configuration completed!"
else
  echo "--> Skipped step 6."
fi

echo ""
echo "=================================================="
echo "         INSTALLATION PROCESS FINISHED            "
echo "=================================================="