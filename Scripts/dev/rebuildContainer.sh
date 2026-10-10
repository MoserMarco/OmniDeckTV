#!/bin/bash
set -e



SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="$SCRIPT_DIR/../../RemoteControl/docker/docker-compose.dev.yml"

echo "=== 1. Removing existing containers ==="
docker compose -f "$COMPOSE_FILE" down --remove-orphans

echo "=== 2. Rebuilding the image ==="
docker compose -f "$COMPOSE_FILE" build --no-cache

echo "=== 3. Pushing image to Docker Hub (overwrite) ==="
docker compose -f "$COMPOSE_FILE" push

echo "=== 4. Creating new container (without starting) ==="
docker compose -f "$COMPOSE_FILE" create

echo "=== Completed successfully using: $COMPOSE_FILE ==="