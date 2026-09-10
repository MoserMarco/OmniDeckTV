#!/bin/bash
set -e

# Find the directory where THIS script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Define the relative path to the docker-compose.jml file
COMPOSE_FILE="$SCRIPT_DIR/../../RemoteControl/docker/docker-compose.dev.yml"

echo "=== 1. Making the development scripts executable ==="
# Grant execution permissions (+x is safer than 700 and doesn't require sudo)
chmod +x "$SCRIPT_DIR"/*.sh
chmod +x "$SCRIPT_DIR"/.devScripts/*.sh 2>/dev/null || true
echo "--> All development scripts are now executable."

echo ""
echo "=== 2. Creating Python virtual environments ==="
"$SCRIPT_DIR/.devScripts/setupEnv.sh" "$SCRIPT_DIR/../../SmartTVApp"
"$SCRIPT_DIR/.devScripts/setupEnv.sh" "$SCRIPT_DIR/../../RemoteControl"
echo "--> All Python environments are ready."

echo ""
echo "=== 3. Building Docker image and creating container ==="
docker compose -f "$COMPOSE_FILE" build --no-cache
docker compose -f "$COMPOSE_FILE" create
echo "--> Docker container created successfully!"