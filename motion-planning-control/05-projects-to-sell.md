# Four Projects You Can Build and Sell

## 1. Real-time MPC library for small drones (~4 weeks)

Embedded NMPC (ACADOS-generated C code) for sub-250g quadrotors, with
a ROS2 + PX4 integration layer. Handles aggressive maneuvers and
obstacle avoidance from a depth camera.

- **Stack:** ACADOS, CasADi, PX4 uORB bridge, RealSense or OAK-D depth.
- **Buyers:** inspection-drone startups, racing-drone teams, university
  labs.
- **Pricing:** $5-20k integration + open-source core + commercial
  support.

## 2. Quadruped locomotion-as-a-service (~3-4 weeks)

For owners of Unitree Go2 / A1 (large hobbyist + small-company market):
deliver a trained RL locomotion policy tuned to their payload and
terrain, plus a teleoperation app and safety bumpers.

- **Stack:** Isaac Lab training, ONNX export, ROS2 bridge, mobile app
  over WebRTC.
- **Buyers:** Go2 owners doing inspection / security / research.
- **Pricing:** $2-10k per robot tuning; subscription for updates.

## 3. Pick-and-place planning as an API (~3 weeks)

REST endpoint: send a scene (point cloud + objects), get back a
time-optimal, collision-free trajectory for a UR / Franka / xArm. Wraps
MoveIt 2 + TrajOpt with sane defaults and post-processing.

- **Stack:** MoveIt 2, OMPL, TrajOpt, FastAPI, gRPC.
- **Buyers:** integrators and contract manufacturers that have arms but
  no motion-planning engineer.
- **Pricing:** $0.01-0.10 per plan + $500-5k/mo SaaS.

## 4. Safety-shield layer for learned policies (~4 weeks)

A drop-in safety filter that wraps any learned policy (RL or VLA),
verifies each action against control-barrier-function constraints in
real time, and falls back to a safe default if violated.

- **Stack:** CBF library (compose with Pinocchio dynamics), JAX/Numba
  for speed, ROS2 + Foxglove monitoring.
- **Buyers:** humanoid and AMR companies needing certification-ready
  safety stories.
- **Pricing:** $25-100k per platform integration; recurring license.
