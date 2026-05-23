# Examples of Work

A tour of "what simulation looks like in industry." Skim this — the
goal is name recognition, not depth.

## Production simulators (the headline tools the industry uses)

These are the equivalent of "the major cloud providers" in web terms.
Most production training happens in one of these.

- **NVIDIA Isaac Sim / Isaac Lab** — Omniverse-based, USD-native,
  GPU-parallel envs. The de-facto industry sim. Isaac Lab (the RL
  training layer, formerly Orbit) ships thousands of parallel envs
  per GPU and is the default for new humanoid training pipelines.
- **NVIDIA Cosmos** (Jan 2025) — open-weights world-foundation-model
  platform for synthetic robotics video / data generation. NVIDIA's
  bet on "world models as data factories."
- **MuJoCo / MJX** (DeepMind) — fast, accurate contact physics; MJX
  is JAX-based and GPU-vectorized. Free, MIT-licensed since 2021
  (when Google open-sourced it). The research-community favorite.
- **Genesis** (CMU + collaborators, late 2024) — open universal
  physics platform. GPU-accelerated, differentiable, claims
  43,000,000 FPS (across parallel envs). Newest entrant, lots of
  hype.
- **Gazebo / Ignition / Gazebo Garden** — the long-running ROS-native
  sim. Older, slower, but tightly integrated with ROS2.
- **Drake** (Toyota Research / MIT) — model-based, contact-rich. The
  "engineering correctness" simulator. Used by TRI and many academic
  manipulation groups.
- **PyBullet** — the lightweight Python sim. Easy to start, less
  common in production. Still common in academic baselines.
- **CARLA, NVIDIA DRIVE Sim, AWS Wayve Infinity** — autonomous-
  vehicle sims.
- **AirSim** (Microsoft, archived 2022 but still used) and
  **Flightmare** — drone sims.
- **Habitat 3.0** (Meta, 2023) — embodied AI / social nav.
- **AI2-THOR, iGibson 2.0, RoboCasa** — indoor manipulation /
  navigation sims. RoboCasa (NVIDIA, 2024) is the latest, kitchen-
  focused, built on Robosuite + MuJoCo.

## Digital-twin platforms (sim's industrial cousin)

These target factories, warehouses, and cities — not robot training
specifically.

- **NVIDIA Omniverse + USD** — collaborative 3D / simulation
  platform. Hub product around which Isaac orbits.
- **Siemens Process Simulate, ABB RobotStudio, FANUC ROBOGUIDE** —
  industrial robot offline programming + twin. The boring incumbents
  that still run actual factory floors.
- **Microsoft Azure Digital Twins** — generic IoT / factory twin.
- **Unity Industrial Collection, Unreal Twinmotion** —
  game-engine-based twins.
- **Cesium / Google 3D Tiles** — large-scale geospatial twins. Cities
  and outdoor environments.
- **Matterport, Polycam, Luma AI, Scaniverse** — 3D scan -> twin
  pipelines. Consumer-side capture into industrial workflows.

## Landmark research (read these eventually, in this order)

The papers that built the modern sim2real stack.

- **Domain randomization** (Tobin et al., IROS 2017) — the founding
  paper of sim2real for vision. "Randomize textures + lighting
  during training and your policy generalizes to the real world."
- **OpenAI Rubik's Cube** (2019) — dexterous manipulation,
  sim-to-real via automatic domain randomization. Showed sim2real
  could solve real-world dexterous tasks.
- **ANYmal sim-to-real RL** (Hwangbo et al., Science Robotics 2019)
  — quadruped locomotion learned entirely in sim, deployed to ANYmal
  on day one. The locomotion analogue of the Rubik's Cube paper.
- **Rapid Motor Adaptation (RMA)** (Kumar et al., RSS 2021) — the
  "privileged teacher + DR student" recipe that powers most modern
  legged-robot training.
- **Isaac Lab / Orbit** (Mittal et al., 2023) — NVIDIA's massively-
  parallel RL training framework. The reference implementation for
  "4000 envs on one GPU."
- **MimicGen** (Mandlekar et al., NVIDIA, CoRL 2023) — synthetic
  demonstration generation. Given one human demo, generate 1000
  variations by replaying the trajectory in new scenes.
- **DextrAH-G / DextrAH-RGB** (NVIDIA, 2024) — large-scale sim-to-
  real for dexterous hand manipulation. Sim trained, real-world
  deployed.
- **RoboCasa** (NVIDIA, 2024) — large-scale kitchen sim with
  thousands of procedurally generated layouts.
- **Cosmos Foundation Models** (NVIDIA, Jan 2025) — world-foundation-
  models for synthetic robotics data.
- **3D Gaussian Splatting** + sim2real bridge work (2024-25) — using
  scan-derived splats as rendering backends inside the simulator.

## Open-source pillars (the equivalent of "npm packages you'll actually use")

- **Isaac Sim + Isaac Lab** — NVIDIA's stack. Free to use; closed
  source but heavily extensible via Python.
- **MuJoCo, MJX** — Apache 2.0, hands-down the most-used research
  sim.
- **Genesis** — Apache 2.0, fast-iterating.
- **Brax** (Google DeepMind) — JAX-based, differentiable physics.
- **PyBullet** — simple, MIT.
- **Drake** — BSD; Pythonic and C++.
- **Robosuite** — RL-focused wrapper on top of MuJoCo.
- **BlenderProc** — procedural photoreal data generation in
  Blender. Apache 2.0.
- **NVISII** — Python ray-tracer for synthetic data.
- **gz_ros2_control, isaac_ros, ros_gz_bridge** — the ROS2 bridges
  for the various sims.

## Standards and asset formats

- **OpenUSD** (Pixar, then open-sourced) — the lingua franca of
  modern simulation. JSON-ish file format; if you only learn one
  format, learn this one.
- **URDF** — old ROS robot-description XML. Still in use everywhere.
- **MJCF** — MuJoCo's XML. Cleaner than URDF; widely used in
  research.
- **glTF, OBJ, FBX** — mesh interchange formats; you'll convert to
  USD constantly.
- **NVIDIA SimReady** — metadata standard for "ready-to-simulate"
  assets (mass properties, materials, collision meshes pre-attached).
