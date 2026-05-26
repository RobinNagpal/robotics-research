#!/usr/bin/env bash
#
# Single-line run for the shelf-stocking simulation.
#
#   ./run.sh                       # headless autonomous mission (prints the log)
#   ./run.sh --gui                 # open the Gazebo GUI (Linux + X11)
#   ./run.sh arm_backend:=direct   # skip MoveIt, use the ikpy direct backend
#
# Any extra args are forwarded to the launch file.
#
set -euo pipefail
cd "$(dirname "$0")"

HEADLESS=true
PASS=()
for a in "$@"; do
  if [[ "$a" == "--gui" ]]; then
    HEADLESS=false
    command -v xhost >/dev/null 2>&1 && xhost +local:docker >/dev/null 2>&1 || true
  else
    PASS+=("$a")
  fi
done

echo ">> Launching simulation (headless=${HEADLESS}). Ctrl-C to stop."
docker compose run --rm sim \
  ros2 launch shelf_bringup sim.launch.py headless:=${HEADLESS} "${PASS[@]}"
