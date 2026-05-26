# Stack layer: Simulator

> **Job:** model the store, the shelves, the products, and the robot
> under one physics engine, with sensors, so the pick-drive-place loop
> can be proven before any hardware exists. The two things that matter
> most here are **contact physics** (will a grasp/place behave like
> reality?) and **rendering realism + domain randomization** (will the
> perception model survive the sim-to-real gap?).

## How this layer fits into the architecture

The simulator is not a part of the robot — it is the **practice world**
the robot lives in before (and alongside) the real store. Picture a
video-game copy of the grocery aisle, the shelves, the products, and the
robot itself, all obeying real physics: gravity, friction, and
collisions.

It sits at the **bottom of the stack** because every other layer needs
something to act on. Before a real store, a real robot, and real cans
exist, the simulator supplies all three. It feeds fake-but-realistic
sensor data *into* the system — camera images to the perception layer,
lidar scans to the navigation layer — and it receives the motor commands
the system sends *back*, then moves the simulated robot accordingly.
Because it exchanges those messages through the same ROS 2 interface the
real hardware will use (see `02-middleware.md`), the code you write
against the simulator is the same code that later runs on real metal.

Concretely, during one rehearsal of the pick-place cycle: the simulator
renders what the wrist camera "sees" of the tray → the perception layer
reads it; the arm-motion layer sends joint commands → the simulator
moves the simulated arm and reports back whether the gripper actually
touched the can. This is where you measure the success rate from the
requirements (`../01-requirements.md`) before risking real hardware.

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

## Cost, hardware & where it runs

| Tier | Pick | Where it runs | Machine requirements | Cost |
|------|------|---------------|----------------------|------|
| **Best in class** | NVIDIA Isaac Sim | Local RTX workstation, or a cloud GPU VM | RTX GPU (RTX 4080/4090, or A6000/L40), ≥16 GB VRAM, 32–64 GB RAM, Ubuntu or Windows | Software free (proprietary EULA); needs a ~$3–6k RTX workstation, or rent a cloud GPU (AWS g5/g6, ~$1–2/hr) |
| **Good enough & cheapest** | Gazebo Harmonic | Any modern CPU laptop or desktop | 4+ core CPU, 16 GB RAM, integrated GPU is fine; Ubuntu 24.04 | Free / open source — runs on hardware you already own |
| **Best cost-for-performance** | Gazebo for the mechanics + Isaac Sim rented by the hour for the perception/DR phase | Gazebo local; Isaac on a cloud RTX VM only during photoreal + domain-randomization sessions | As above for each stage | Free for the bulk of the work; cloud GPU billed only in bursts (~$1–2/hr) when you actually need realism |

Isaac Sim is the only layer that genuinely *demands* an RTX GPU — the
RTX path tracer and Replicator are the whole reason to pay for it. Gazebo
asks for nothing you don't already have, which is why the recommended
path proves mechanics there first and only buys GPU time once perception
needs photorealism.
