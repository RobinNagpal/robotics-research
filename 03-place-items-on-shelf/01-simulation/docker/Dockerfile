# Shelf-stocking simulation — ROS 2 Jazzy + Gazebo Harmonic.
# Works on amd64 and arm64 (Apple Silicon) Docker hosts. CPU-only; no GPU.
FROM ros:jazzy-ros-base

SHELL ["/bin/bash", "-c"]
ENV DEBIAN_FRONTEND=noninteractive

# --- Gazebo Harmonic apt repository -----------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
      curl gnupg lsb-release ca-certificates \
 && curl -sSL https://packages.osrfoundation.org/gazebo.gpg \
      -o /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg \
 && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" \
      > /etc/apt/sources.list.d/gazebo-stable.list \
 && rm -rf /var/lib/apt/lists/*

# --- ROS 2 + Gazebo + control + tooling -------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
      gz-harmonic \
      ros-jazzy-ros-gz \
      ros-jazzy-ros2-control \
      ros-jazzy-ros2-controllers \
      ros-jazzy-gz-ros2-control \
      ros-jazzy-xacro \
      ros-jazzy-robot-state-publisher \
      ros-jazzy-joint-state-publisher \
      ros-jazzy-controller-manager \
      ros-jazzy-teleop-twist-keyboard \
      ros-jazzy-rviz2 \
      python3-pip python3-colcon-common-extensions \
 && rm -rf /var/lib/apt/lists/*

# --- Python libs for inverse kinematics + math ------------------------------
# PEP 668: allow installing into the system interpreter inside the container.
RUN pip3 install --no-cache-dir --break-system-packages \
      ikpy numpy scipy

# --- Build the ROS 2 workspace ----------------------------------------------
WORKDIR /ws
COPY shelf_ws/src /ws/src
RUN source /opt/ros/jazzy/setup.bash \
 && colcon build --symlink-install \
 && rm -rf /ws/build /ws/log

COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]
