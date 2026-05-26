#!/usr/bin/env bash
# Sources ROS 2 + the built workspace and points Gazebo at our worlds/models.
set -e

source /opt/ros/jazzy/setup.bash
if [ -f /ws/install/setup.bash ]; then
  source /ws/install/setup.bash
fi

# Let `gz sim` resolve our custom worlds and models by name.
SHARE=/ws/install/shelf_bringup/share/shelf_bringup
export GZ_SIM_RESOURCE_PATH="${SHARE}/models:${SHARE}/worlds:${GZ_SIM_RESOURCE_PATH:-}"

mkdir -p /ws/logs
exec "$@"
