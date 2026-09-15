#!/bin/bash
set -e

echo "=== Setup of TVControlHub ==="
INSTALLATION_DIRECTORY=$1
COMPOSE_FILE="INSTALLATION_DIRECTORY/RemoteControl/docker/docker-compose.yml"
echo "--> Creating Python virtual environments ==="
"$INSTALLATION_DIRECTORY/Scripts/install/.installScripts/setupEnv.sh" "$INSTALLATION_DIRECTORY/SmartTVApp"

echo "-> All Python environments are ready."

echo ""
echo "--> Building Docker image and creating container ==="
docker compose -f "$COMPOSE_FILE" build --no-cache
docker compose -f "$COMPOSE_FILE" create
echo "--> Docker container created successfully!"