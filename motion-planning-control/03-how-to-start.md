# How to Get Started

## Week 1-2: Classical foundations

- Read first 6 chapters of Tedrake's **"Underactuated Robotics"** (free
  online + edX videos).
- Implement LQR for a cart-pole; then iLQR.
- Implement a simple QP-based inverse kinematics solver with Pinocchio.

## Week 3-4: Motion planning

- Read selected chapters of LaValle's **"Planning Algorithms"**.
- Implement A*, RRT, and RRT* from scratch in Python.
- Set up MoveIt 2 in ROS2 with a UR5 sim; plan and execute a
  pick-and-place.

## Week 5-6: MPC and trajectory optimization

- Pick ACADOS or CasADi; implement linear MPC for a quadrotor.
- Implement NMPC for a car-like robot with obstacle avoidance.
- Run MIT's open-source convex-MPC code on a quadruped in MuJoCo.

## Week 7-8: Learned control

- Train PPO/SAC in Isaac Lab on a quadruped or arm.
- Reproduce the "Walk These Ways" or ANYmal-style locomotion result in
  sim.
- Try DreamerV3 on a continuous-control task.

## Simulators / sandboxes

MuJoCo (free, fast), MJX (GPU-vectorized MuJoCo), Isaac Lab (high
fidelity + parallel), DRAKE (model-based gold standard), Brax (JAX
diff-physics), Genesis (2024 newcomer, very fast).

## Hardware to consider

- Bipedal Robotics Cassie / Digit (industry standard).
- Unitree A1 / Go1 / Go2 (~$3-5k entry quadruped).
- ANYmal (research-grade quadruped).
- Franka Emika Panda, UR5 (research arms).

## Communities

ICRA, IROS, CoRL, RSS, L4DC; DRAKE Slack; Boston Dynamics blog; Hutter
group / ETH videos.
