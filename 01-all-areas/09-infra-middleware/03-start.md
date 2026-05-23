# How to Get Started

## Week 1-2: ROS2 fluency

- Work through the official ROS2 Humble or Jazzy tutorials end to end.
- Build a small custom node in both rclpy and rclcpp; understand the
  executor models.
- Write a complex launch file with composable nodes.

## Week 3: QoS and DDS

- Read the ROS2 QoS docs and the Cyclone DDS deployment guide.
- Run two machines with ROS2; tune for low-latency video over Wi-Fi vs
  reliable telemetry over wired.
- Try Zenoh with the zenoh-bridge-ros2 across two networks.

## Week 4: Data plumbing

- Record a robot session as MCAP using rosbag2.
- Open it in Foxglove Studio; build a custom panel.
- Try Rerun.io for a multimodal log (images + transforms + scalars).

## Week 5: Real-time + embedded

- Boot PREEMPT_RT on a Jetson Orin or RPi 5; measure latency with
  cyclictest.
- Cross-compile a ROS2 workspace for ARM with colcon.
- Flash micro-ROS to an STM32 / ESP32 and pub-sub with the main host.

## Week 6: CI and OTA

- Set up GitHub Actions running ROS2 + Gazebo in Docker; run regression
  tests on a recorded MCAP.
- Set up Mender or RAUC OTA on a test Jetson; demonstrate an A/B
  rollback.

## Week 7-8: Build a small fleet platform

Pick one:

- A Foxglove-clone observability dashboard for 3 sim robots.
- A "ROS2 in a single Docker compose" template that any startup can
  adopt.
- A CI runner that replays a directory of MCAPs through a candidate
  perception node and posts regression deltas.

## Communities

ROS Discourse, ROS Discord, Foxglove Slack, Zenoh Discord, NVIDIA Isaac
ROS forum, Apex.AI talks at ROSCon.
