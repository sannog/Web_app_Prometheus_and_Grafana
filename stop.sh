#!/bin/bash

# Stop the monitoring stack using docker-compose or docker compose

set -e

if command -v docker-compose >/dev/null 2>&1; then
  COMPOSE_CMD="docker-compose"
else
  COMPOSE_CMD="docker compose"
fi

echo "🛑 Stopping Monitoring Stack..."
echo "Using: $COMPOSE_CMD"

$COMPOSE_CMD down

echo "✅ Monitoring stack stopped"


