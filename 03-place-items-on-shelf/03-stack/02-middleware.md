# Stack layer: Middleware

> **Job:** the communication and tooling backbone that connects every
> other layer — navigation, motion planning, perception, orchestration —
> and lets the *same* nodes run in simulation and on hardware. This is a
> near-foregone choice in modern robotics, but it is worth seeing why,
> and what the alternatives give up.

## Comparison

| Framework | Maintenance / longevity | Real-time / QoS (DDS) | Nav2 + MoveIt 2 ecosystem | Tooling (rviz, tf2, bags) | Multi-language | Learning resources | Bottom line |
|-----------|-------------------------|-----------------------|---------------------------|---------------------------|----------------|--------------------|-------------|
| **ROS 2** (Jazzy / Humble) | Active, the field standard | Yes — DDS, configurable QoS | First-class; both built on ROS 2 | Full (rviz2, tf2, rosbag2) | C++, Python (+ Rust, C# community) | Vast | The default; everything this project needs runs here out of the box |
| **ROS 1** (Noetic) | **EOL May 2025** | No (TCPROS, no QoS) | Legacy Nav (`move_base`), MoveIt 1 | Mature but frozen | C++, Python | Vast but aging | Do not start new work here — dead end |
| **YARP** | Active (niche, humanoids) | Limited | No Nav2/MoveIt | Own toolset | C++, Python | Small | Strong in its niche (iCub); off-ecosystem for this build |
| **LCM** | Low activity | Low-latency UDP, no QoS layer | None | Minimal | C++, Java, Python | Small | A lean message bus, not a robotics framework — too little |
| **microROS** | Active (companion to ROS 2) | Yes (on MCUs) | Bridges into ROS 2 | Via the ROS 2 host | C | Growing | For microcontrollers only; complements, not replaces, ROS 2 |
| **Custom DDS** (Cyclone/Fast-DDS direct) | N/A (you maintain it) | Full control | You reimplement everything | None | C++/C | DDS docs only | Maximum control, maximum cost — reinventing ROS 2 |

## Top choice

**ROS 2 (Jazzy Jalisco on Ubuntu 24.04, or Humble on 22.04).**

It is the only option where Nav2 and MoveIt 2 — the two layers the robot
absolutely needs — are first-class citizens, where rviz2/tf2/rosbag2
make debugging tractable, and where the sim (Gazebo `ros_gz`, Isaac Sim
bridge) speaks the same interface as hardware, so transfer is a driver
swap rather than a rewrite. ROS 1 is end-of-life; everything else
sacrifices the ecosystem this project is built on. Add **microROS** only
if a microcontroller (e.g. a gripper or sensor MCU) needs to join the
graph.
