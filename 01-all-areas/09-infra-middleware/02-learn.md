# Important Things to Learn

## ROS2 fundamentals

- Nodes, topics, services, actions, parameters, lifecycle nodes.
- QoS profiles (reliability, durability, deadline) — the topic most
  people skip and most production bugs come from.
- Composition and component containers for zero-copy intra-process
  messaging.
- tf2 transform tree.
- Launch system (Python launch files), Bringup patterns.
- rclcpp vs rclpy trade-offs; executor models.

## DDS / Zenoh / messaging internals

- DDS discovery, RTPS wire protocol, multicast vs unicast.
- Cyclone DDS vs Fast DDS vs RTI tuning.
- Zenoh: routers, peers, queries vs subscriptions.
- Network bridging: zenoh-bridge-ros2, rosbridge, MQTT.

## Real-time and embedded

- PREEMPT_RT Linux kernel, isolcpus, IRQ affinity, cgroups.
- Cross-compilation for ARM (Jetson, RPi, NVIDIA Orin).
- Yocto / Buildroot / Ubuntu Core / Balena.
- micro-ROS on STM32 / ESP32.

## Data plumbing

- MCAP file format; rosbag2 internals.
- Time-series databases (TimescaleDB, InfluxDB) for fleet telemetry.
- Parquet + DuckDB for analytics on robot data.
- Foxglove and Rerun.io workflows.

## DevOps for robots

- Docker / Podman, multi-arch builds (buildx).
- Robot CI patterns: simulation-in-CI, regression testing on recorded
  bags, hardware-in-the-loop runners.
- OTA updates: Mender, RAUC, swupdate, A/B partitions.
- Fleet observability: Prometheus, OpenTelemetry, Grafana.
- SBOM and supply-chain hygiene.

## Tools

ROS2 Humble/Iron/Jazzy, Cyclone DDS, Zenoh, MCAP, Foxglove, Rerun.io,
NVIDIA Isaac ROS, micro-ROS, PREEMPT_RT, Mender / RAUC.

## Must-read

ROS2 Design (design.ros2.org), MCAP spec, REP-2014 (real-time
considerations), Foxglove engineering blog, Zenoh docs, Apex.AI
"ROS2 in production" talks.
