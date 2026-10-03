#!/bin/bash
set -e



SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
PROGRAM_DIRECTORY="$(dirname "$(dirname "$SCRIPT_DIR")")"
COMPOSE_FILE="$PROGRAM_DIRECTORY/RemoteControl/docker/docker-compose.yml"
SMARTTV_APP_DIR="$PROGRAM_DIRECTORY/SmartTVApp"
SMARTTV_PYTHON="$SMARTTV_APP_DIR/.venv/bin/python"
INPUTMAPPER_APP_DIR="$PROGRAM_DIRECTORY/InputMapper"
INPUTMAPPER_PYTHON="$INPUTMAPPER_APP_DIR/.venv/bin/python"

echo "=== 1. Launching Remote Control Docker Container"
docker compose -f "$COMPOSE_FILE" start
echo "--> Remote Control Docker Container started on http://localhost:5001"

echo "=== 2. Launching Background Input Mapper"


if [ ! -f "$INPUTMAPPER_PYTHON" ]; then
    echo "Error: Virtual environment not found in $BG_APP_DIR!"
    exit 1
fi

if pgrep -f "$INPUTMAPPER_APP_DIR" > /dev/null; then
    echo "--> Input Mapper is ALREADY running. Skipping background launch."
else
    cd $INPUTMAPPER_APP_DIR
    nohup "$INPUTMAPPER_PYTHON" -m main > /dev/null 2>&1 &
    echo "--> Input Mapper Launched in Background"
fi



echo "--> Input Mapper Launched in Background "

echo " 3. Launching SmartTVApp Python Application"

if [ ! -f "$SMARTTV_PYTHON" ]; then
    echo "Error: Virtual environment not found in $BG_APP_DIR!"
    exit 1
fi
cd $SMARTTV_APP_DIR
"$SMARTTV_PYTHON" -m main

echo "--> Input Mapper Launched in Background "

echo "=== 3. Closing Python Application and Deactivating Environment"


