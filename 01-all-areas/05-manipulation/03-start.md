# How to Get Started

## Week 1-2: Classical grasping

- Run AnyGrasp or Contact-GraspNet on the GraspNet-1Billion dataset.
- Implement antipodal grasp sampling from a point cloud in Open3D.
- Read Dex-Net 2/3/4 papers.

## Week 3-4: Sim manipulation

- Set up Robosuite or ManiSkill 3 with a Franka arm.
- Train a Diffusion Policy on a pick-and-place task.
- Try RoboCasa kitchen tasks.

## Week 5: Imitation learning on real hardware

- If you have access: collect 50 teleop demos on an Aloha or SO-100,
  train ACT or Diffusion Policy with LeRobot.
- If sim-only: collect demos via MimicGen and fine-tune OpenVLA on
  LIBERO.

## Week 6: Sim-to-real RL

- Reproduce a small DextrAH-style result in Isaac Lab: train in
  parallel envs with domain randomization, evaluate transfer.

## Week 7-8: Bin-picking pipeline

- Combine FoundationPose (or AnyGrasp) + a MoveIt 2 plan + a hardware
  arm (or its sim twin) to do reliable singulation from a bin.

## Cheap hardware to own

- **SO-100** (~$300) — perfect for ACT / VLA experiments.
- **Aloha kit** (~$5k) — bimanual + base.
- **xArm 6 / xArm 7** ($5-10k) — pro-grade, ROS2 compatible.
- **LEAP Hand** (~$2k DIY) — open-source dexterous hand.

## Datasets and benchmarks

GraspNet-1Billion, BOP, LIBERO, RoboCasa, Meta-World, Robosuite, DROID,
BridgeData V2, Open X-Embodiment.

## Communities

CoRL, RSS, ICRA, IROS; LeRobot Discord; NVIDIA Isaac Slack; r/robotics;
Ken Goldberg / Berkeley AUTOLAB papers; Stanford ALOHA team.
