#!/bin/bash
set -e


SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="$SCRIPT_DIR/../../RemoteControl/docker/docker-compose.dev.yml"
SMARTTV_APP_DIR="$SCRIPT_DIR/../../SmartTVApp"


echo "=== 1. Starting Remote Control Docker Container"
docker compose -f "$COMPOSE_FILE" start
echo "--> Docker Container started on http://localhost:5001"



echo " 2. Launching SmartTVApp Python Application"

if [ ! -d "$SMARTTV_APP_DIR/.venv" ]; then
    echo "Error: Virtual environment not found in $SMARTTV_APP_DIR!"
    echo "Please run setup.sh first."
    exit 1
fi

# Attiva il venv ed esegue l'applicazione Python
source "$SMARTTV_APP_DIR/.venv/bin/activate"


cd "$SMARTTV_APP_DIR"
python3 -m src.main




echo "=== 3. Closing Python Application and Deactivating Environment"

deactivate
echo "--> Application closed and environment deactivated"

echo "=== 4. Stopping Remote Control Docker Container"

docker compose -f "$COMPOSE_FILE" stop
echo "--> Docker Container stopped successfully"