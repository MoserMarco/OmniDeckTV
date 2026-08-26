#!/bin/bash

# Save current directory as default target
cd ../../
target=$(pwd)
cd TVControlHub/RemoteControl

# --- Argument check ---
if [ $# -gt 1 ]; then
    echo "Error: too many arguments. Usage: $0 [optional_absolute_path]"
    exit 1
fi

if [ $# -eq 1 ]; then
    if [[ $1 != /* ]]; then
        echo "Error: the argument must be an absolute path (must start with /)"
        exit 1
    fi
    target="$1"
    # --- Check if TVControlHub already exists ---
    if [ -d "$target/TVControlHub" ]; then
	echo "A directory named 'TVControlHub' already exists in $target"
	read -p "Do you want to replace it? (Y/N): " response
	if [[ "$response" == "N" || "$response" == "n" ]]; then
            echo "Operation cancelled."
	    exit 1
	fi
	echo "Removing old TVControlHub directory..."
	rm -rf "$target/TVControlHub"
    fi
    # --- Move project ---
    echo "Moving TVControlHub to $target"
    mv ../../TVControlHub "$target"
    # --- Setup environment ---
    cd "$target/TVControlHub/RemoteControl" || { echo "❌ Error: directory not found"; exit 1; }

fi


rm -R ../SoftwareLauncher/
rm -R ../README.md
rm -R ../CommandListener/

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# --- Handle existing systemd service file ---
SERVICE_PATH="/etc/systemd/system/TVControlHub.service"

if [ -f "$SERVICE_PATH" ]; then
    echo "Service file already exists at $SERVICE_PATH"
    read -p "Do you want to replace it? (Y/N): " response
    if [[ "$response" == "N" || "$response" == "n" ]]; then
        echo "Operation cancelled."
        exit 1
    fi
    echo "Removing old service file..."
    sudo rm -f "$SERVICE_PATH"
fi

# --- Create new systemd service file from scratch ---
echo "Creating new systemd service file with target path $target..."

sudo tee "$SERVICE_PATH" > /dev/null <<EOF
[Unit]
Description=TVControlHub
After=network.target

[Service]
WorkingDirectory=$target/TVControlHub/RemoteControl
Environment="PATH=$target/TVControlHub/RemoteControl/venv/bin"
ExecStart=$target/TVControlHub/RemoteControl/venv/bin/python $target/TVControlHub/RemoteControl/app.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF


# --- Configure systemd service ---
sudo systemctl daemon-reload
sudo systemctl enable TVControlHub
sudo systemctl start TVControlHub
sudo systemctl status TVControlHub