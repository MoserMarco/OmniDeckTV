#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
PROGRAM_DIRECTORY="$(dirname  "$(dirname  "$SCRIPT_DIR")")"
INPUTMAPPER_APP_DIR="$PROGRAM_DIRECTORY/InputMapper"
INPUTMAPPER_PYTHON="$INPUTMAPPER_APP_DIR/.venv/bin/python"
echo $INPUTMAPPER_APP_DIR
pkill -f "InputMapper"

flatpak run org.libretro.RetroArch
if pgrep -f "$INPUTMAPPER_APP_DIR" > /dev/null; then
    echo "--> Input Mapper is ALREADY running. Skipping background launch."
else
    cd $INPUTMAPPER_APP_DIR
    nohup "$INPUTMAPPER_PYTHON" -m main > /dev/null 2>&1 &
    echo "--> Input Mapper Launched in Background"
fi