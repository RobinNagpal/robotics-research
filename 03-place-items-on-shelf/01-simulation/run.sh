#!/usr/bin/env bash
#
# Single-line run for the shelf-stocking simulation.
#
#   ./run.sh           # headless autonomous mission (works anywhere, prints the success log)
#   ./run.sh --gui     # open the Gazebo GUI (Linux + X11; run `xhost +local:docker` first)
#
set -euo pipefail
cd "$(dirname "$0")"

HEADLESS=true
if [[ "${1:-}" == "--gui" ]]; then
  HEADLESS=false
  # Best-effort: allow the container to reach the local X server on Linux.
  command -v xhost >/dev/null 2>&1 && xhost +local:docker >/dev/null 2>&1 || true
fi

echo ">> Launching simulation (headless=${HEADLESS}). Ctrl-C to stop."
docker compose run --rm sim \
  ros2 launch shelf_bringup sim.launch.py headless:=${HEADLESS}
