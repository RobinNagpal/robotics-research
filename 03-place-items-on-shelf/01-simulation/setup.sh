#!/usr/bin/env bash
#
# Single-line setup for the shelf-stocking simulation.
#
# Builds the Docker image: ROS 2 Jazzy + Gazebo Harmonic + Nav2/MoveIt deps,
# then compiles the ROS 2 workspace inside the image. Run this once.
#
#   ./setup.sh
#
set -euo pipefail
cd "$(dirname "$0")"

if ! command -v docker >/dev/null 2>&1; then
  echo "ERROR: docker is not installed. Install Docker Desktop / Docker Engine first." >&2
  exit 1
fi

echo ">> Building the simulation image (this takes several minutes the first time)..."
docker compose build

echo ""
echo ">> Setup complete."
echo ">> Run the full autonomous simulation with:   ./run.sh"
echo ">> Run with the Gazebo GUI (Linux + X11) with: ./run.sh --gui"
