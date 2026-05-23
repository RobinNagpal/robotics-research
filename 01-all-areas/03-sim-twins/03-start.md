# How to Get Started

A concrete 8-week plan. The goal isn't to read everything — it's to
ship a working sim demo end-to-end by the end: a custom environment,
a trained policy, and a video.

## Prerequisites (1 week, can overlap with Week 1)

- Comfortable Python.
- NumPy + basic PyTorch (Karpathy's "neural networks zero-to-hero"
  if not).
- **GPU strongly recommended.** Three options:
  - **Local NVIDIA GPU** (RTX 4070 / 3080 / 4090 with 16-24 GB
    VRAM) — by far the easiest for Isaac Sim, which is finicky on
    cloud. If you can buy/borrow one, do.
  - **Rent**: Lambda Labs, RunPod, Modal, Vast.ai. ~$0.40-$2/hr
    for an A100/H100. Confirm the image has NVIDIA drivers + a
    desktop / VNC; Isaac Sim needs OpenGL / Vulkan, not just CUDA.
  - **Colab Pro** ($10/mo) — works for MuJoCo / MJX / Brax (which
    are pure CUDA), not Isaac Sim (needs a display server).
- **Ubuntu 22.04** is the most-supported OS. Windows works for Isaac
  Sim but is bumpier; macOS only works for MuJoCo / pure-Python sims.

## Week 1: MuJoCo first (the easy start)

Goal: get used to loading a robot, applying forces, and watching it
move.

- Install **MuJoCo** (free since 2021; just `pip install mujoco`).
  Run the bundled `mjpython simulate` viewer on a few of the
  shipped XML models — humanoid, ant, cartpole.
- Build a custom **MJCF** scene: a UR5 or Panda arm + a box on a
  table. Apply joint torques and watch.
- Install **MuJoCo Playground** (DeepMind, 2024) — the official
  curated env collection with JAX/MJX training. Run a Brax / MJX PPO
  reach task — should converge in minutes on a single GPU.

## Week 2: Isaac Sim / Isaac Lab

Goal: train your first GPU-parallel policy.

- Install **Isaac Sim 4.x**. Use the local installer; the
  containerized version is harder to make interactive.
- Install **Isaac Lab** (the RL training layer; formerly Orbit).
  Run the quickstart on the **Cartpole** task, then **Ant**, then
  the **ANYmal quadruped locomotion** task with 4096 parallel envs.
- Read the Isaac Lab docs cover-to-cover. The framework's
  abstractions (Env, AssetCfg, ManagerBased vs Direct workflow) are
  where most newcomers get stuck.
- Walk through the **NVIDIA Replicator** tutorials for
  synthetic-data generation.

## Week 3: USD and assets

Goal: stop being scared of USD files.

- Read Pixar's USD tutorials (the first 5 of the official Universal
  Scene Description tutorials are enough).
- Build a custom scene via composition arcs: a base environment
  layer + a robot layer + a randomized objects layer.
- Convert a glTF model to USD with `usd-from-gltf` or NVIDIA's
  Asset Converter inside Omniverse. Add **SimReady metadata**
  (mass, friction, collider) so the asset is physics-ready.
- Tip: a lot of free 3D assets exist (Sketchfab, Polyhaven,
  NVIDIA's Omniverse asset library, Objaverse). Use them.

## Week 4: Sim-to-real basics

Goal: train one policy with proper domain randomization.

- Reproduce a small **ANYmal-style** RL locomotion result in Isaac
  Lab. Sweep over the DR ranges (friction, mass, motor delay).
- Read the **RMA** paper (Kumar et al., RSS 2021). Try the
  privileged-teacher / DR-student recipe on the same env — train a
  teacher with full state observation, then distill to a student
  with only realistic sensor observations.
- Compare the no-DR policy vs. DR-trained policy via stress tests
  in sim (mass / friction perturbations way outside training range).

## Week 5: Digital twin from a real scan

Goal: bring a real environment into sim.

- Scan a room of your apartment with **Polycam** or **Luma AI** on
  your phone (or use **RealityCapture** if you have a Windows
  workstation). Export to OBJ / glTF.
- Convert the mesh to USD; attach physics colliders (Open3D for
  decimation, then USD's collision API). Add lights and PBR
  materials.
- Drop in a moving Franka arm or a Carter mobile robot. Render a
  walk-through video in Isaac Sim with RTX path tracing.

## Week 6: Differentiable physics

Goal: train without RL.

- Try **MJX** or **Genesis** with a differentiable contact task
  (cloth push, cartpole swing-up, a small reach task).
- Compare gradient-descent through physics vs. PPO on the same
  task. When it works, gradient descent should be far more
  sample-efficient — when it doesn't, contact non-smoothness is the
  reason.
- Read **DiffMimic** / Brax differentiable-control examples.

## Week 7-8: Build one substantial portfolio project

Pick something you'd put on your resume. Some ideas:

- **A procedural warehouse generator.** Python tool that takes a
  CAD floor plan and emits 100s of randomized USD scenes
  (lighting, shelving, clutter). Pure Replicator + USD.
- **A Sim2Real toolkit for a single Franka task.** One full
  pipeline: env definition, DR config, PPO training, sim eval,
  policy export to ONNX. Clean repo + demo video.
- **A synthetic dataset (100k frames) for a specific vision
  benchmark.** Document your DR config, run a baseline detector on
  it, compare to real-data training.
- **An Isaac Lab task as an open-source repo + W&B run.** Pick
  something not in Isaac Lab's stock examples (e.g., bimanual
  insertion, peg-hole). This is the most-requested portfolio
  artifact by NVIDIA recruiters.

## Datasets / benchmarks worth knowing

- **RoboCasa Kitchen** — NVIDIA's 2024 large-scale kitchen sim
  suite.
- **MetaWorld MT-50** — 50 tabletop tasks; classic RL benchmark.
- **DMC (DeepMind Control Suite)** — the MuJoCo-based RL
  benchmark.
- **LIBERO** — 130 manipulation tasks, four suites.
- **CALVIN** — long-horizon language-conditioned tasks.
- **Habitat-Matterport (HM3D)** — large indoor scan dataset for
  embodied AI.
- **Objaverse / Objaverse-XL** — 10M+ 3D objects on Sketchfab,
  free for research.
- **BOP** — 6-DoF pose benchmark (useful for synthetic-data
  validation).

## Communities

- **NVIDIA Isaac Sim Discord and forum** — the most active sim-
  specific community by far.
- **MuJoCo forum** at the DeepMind GitHub discussions.
- **OpenUSD community** at openusd.org.
- **CoRL, RSS, ICRA, IROS** workshops on sim-to-real, photoreal
  simulation, world models.
- X/Twitter: @YukezhuYuke (RoboCasa), @drjimfan (NVIDIA GEAR),
  @DieterFox, @AnimeshGarg, @hjones.
