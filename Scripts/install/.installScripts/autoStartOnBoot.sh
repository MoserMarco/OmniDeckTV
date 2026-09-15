#!/bin/bash
INSTALLATION_DIRECTORY=$1
SERVICE_FILE="/etc/systemd/system/tvcontrolhub.service"
CURRENT_USER="$USER"
TARGET_DIR="${TARGET_DIR:-/usr/local/bin}"

ln -sf "$INSTALLATION_DIRECTORY/Scripts/install/run_all.sh" /usr/local/bin/tvcontrolhub

echo "--> Configuring automatic startup at boot..."

sudo tee "$SERVICE_FILE" > /dev/null <<EOF
[Unit]
Description=TVControlHub Service
After=network.target

[Service]
Type=simple
User=$CURRENT_USER
WorkingDirectory=$TARGET_DIR
ExecStart=/usr/local/bin/tvcontrolhub
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now tvcontrolhub.service

echo "[SUCCESS] The tvcontrolhub service is configured and started!"