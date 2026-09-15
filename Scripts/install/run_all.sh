#!/bin/bash
set -e



# Locate current script directory
SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
PROGRAM_DIRECTORY="$(dirname "$(dirname "$SCRIPT_DIR")")"
COMPOSE_FILE="$PROGRAM_DIRECTORY/RemoteControl/docker/docker-compose.yml"
SMARTTV_APP_DIR="$PROGRAM_DIRECTORY/SmartTVApp"



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