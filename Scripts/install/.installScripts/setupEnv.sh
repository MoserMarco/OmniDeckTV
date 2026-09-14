#!/bin/bash
set -e


if [ -z "$1" ]; then
    echo "Error: No project directory provided."
    echo "Usage: $0 <path_to_project_folder>"
    exit 1
fi

PROJECT_DIR="$1"
VENV_DIR="$PROJECT_DIR/.venv"
REQ_FILE="$PROJECT_DIR/requirements.txt"


echo "=== 1. Checking environment for: $PROJECT_DIR"



if [ -d "$VENV_DIR" ]; then
    echo "--> Virtual environment already exists."
else
    echo "--> Virtual environment not found. Creating .venv..."
    python3 -m venv "$VENV_DIR"
    echo "--> Virtual environment created."
fi


source "$VENV_DIR/bin/activate"


pip install --upgrade pip -q


if [ -f "$REQ_FILE" ]; then
    echo "=== 2. Checking dependencies from requirements.txt..."


    MISSING=$(pip install -r "$REQ_FILE" --dry-run 2>&1 | grep -E "Would install|Would update" || true)

    if [ -n "$MISSING" ]; then
        echo "--> Missing dependencies found. Installing..."
        pip install -r "$REQ_FILE"
        echo "--> All dependencies installed successfully."
    else
        echo "--> All dependencies are already installed and up to date."
    fi
else
    echo "--> Warning: requirements.txt not found in $PROJECT_DIR"
fi

deactivate
