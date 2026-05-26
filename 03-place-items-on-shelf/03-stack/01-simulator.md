# Stack layer: Simulator

> **Job:** model the store, the shelves, the products, and the robot
> under one physics engine, with sensors, so the pick-drive-place loop
> can be proven before any hardware exists. The two things that matter
> most here are **contact physics** (will a grasp/place behave like
> reality?) and **rendering realism + domain randomization** (will the
> perception model survive the sim-to-real gap?).

## Comparison

| Framework | Rendering realism | Contact / physics fidelity | Sensor + ROS 2 integration | Synthetic-data / domain randomization | Compute need | License | Bottom line |
|-----------|-------------------|----------------------------|----------------------------|----------------------------------------|--------------|---------|-------------|
| **NVIDIA Isaac Sim** | Excellent (RTX path tracing) | High (PhysX 5, GPU) | RGB-D/lidar built in; maintained ROS 2 bridge | Best in class (Replicator) | High — needs RTX GPU | Proprietary EULA, free | Strongest for *perception + mobile manipulation*; heavy and GPU-bound |
| **Gazebo (Harmonic)** | Moderate (OGRE2) | Good (DART/Bullet/ODE) | Native, first-class (`ros_gz`), rich sensor plugins | Limited (manual / plugins) | Low–moderate (CPU OK) | Apache-2.0 (open) | The open, ROS-native default to prove *mechanics* cheaply; weak realism |
| **MuJoCo** | Low–moderate | Excellent (fast, accurate contacts) | Sensors basic; ROS 2 via third-party | Via MJX/code, no built-in scene DR | Low (CPU); GPU via MJX | Apache-2.0 (open) | Best contact dynamics for tuning the grasp/place in isolation; not a whole navigable store |
| **Genesis** | Good (ray-traced) | High, very fast (GPU) | Nascent ROS support | Generative scene tooling, immature | Moderate–high (GPU) | Open (permissive) | Promising 2024 speed/physics; ecosystem too young to bet a delivery on |
| **PyBullet** | Low | Moderate | DIY; community ROS bridges | Code-only | Very low | Open (zlib) | Easy Python prototyping/RL; too low-fidelity for the perception half |
| **Webots** | Moderate | Good (ODE-based) | Good ROS 2 support | Limited | Low | Apache-2.0 (open) | Friendly for mobile-robot basics; less suited to photoreal perception or heavy manipulation |

## Top choice

**Two-stage: Gazebo Harmonic → NVIDIA Isaac Sim.**

- Start in **Gazebo Harmonic** to wire up ROS 2 + Nav2 + MoveIt 2 and
  prove the *mechanics* of drive-pick-place with known poses. It is
  open, cheap on hardware, and the most painless ROS-native sim.
- Move to **Isaac Sim** for the *perception* half: RTX realism plus
  **Replicator** domain randomization (lighting, texture, product pose)
  is exactly what keeps a product/slot detector from overfitting one
  clean scene — the single biggest sim-to-real risk for this project.

Keep **MuJoCo** in your back pocket as a focused rig if the contact
dynamics of the set-down need careful tuning. Skip Genesis/PyBullet for
delivery work — prototyping only.
