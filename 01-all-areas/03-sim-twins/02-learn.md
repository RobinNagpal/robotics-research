# Important Things to Learn

If you're coming from web dev, the gap is **a small amount of physics
intuition** plus **NVIDIA's USD / Omniverse stack** plus **enough RL
to drive a sim training loop**. The Python tooling is the same as
everywhere else.

## Layer 0: Python and PyTorch

Same baseline as every ML field. Spend a week if you haven't:

- Python type hints, dataclasses, NumPy, pathlib, uv / venv.
- PyTorch tensors and autograd. A tensor is a multi-dimensional
  array; `requires_grad=True` is like reactive state — PyTorch
  tracks every operation so it can auto-compute gradients later.
  Karpathy's "neural networks zero-to-hero" series is the best free
  intro.
- **JAX** (optional but useful) — DeepMind's alternative to PyTorch,
  used by MJX, Brax, MuJoCo Playground. Same mental model with
  more explicit pure-functional style.

## Layer 1: Physics simulation foundations

You do not need a graduate degree in mechanics; you need the
following 5 concepts to "click."

- **Rigid-body dynamics.** A rigid body has position, orientation,
  linear velocity, angular velocity. Newton-Euler equations evolve
  them under forces and torques.
- **Contact mechanics.** Two bodies touching: normal force, friction
  (Coulomb model), constraint solvers (LCP, PGS, ADMM). This is
  where simulators get hard — contact-rich tasks (grasping, walking)
  push solver edge cases.
- **Time stepping.** Explicit (RK4, semi-implicit Euler) vs.
  implicit. Sub-stepping. Stiff vs. non-stiff. Most robotics sims
  run a 1-10 ms step.
- **Constraints.** Joint constraints (revolute, prismatic, ball),
  contact constraints, friction cones.
- **Soft bodies, cloth, fluids.** Mostly out-of-scope for robotics
  training, but Genesis and NVIDIA Warp are pushing into this
  territory.

## Layer 2: Differentiable physics (the interesting modern bit)

A differentiable simulator lets you backprop gradients through
contacts. That means you can train a policy with **gradient descent
through physics** instead of RL — orders of magnitude more sample-
efficient when it works.

- **MJX** (DeepMind, JAX-based MuJoCo) — most mature.
- **Brax** (DeepMind) — JAX-based, lighter; great for fast research
  iteration.
- **NVIDIA Warp** — Python -> CUDA kernel JIT; differentiable
  rigid + soft body.
- **Genesis** — 2024+ entrant, differentiable across many physics
  modes.
- **Drake autodiff** — symbolic / automatic differentiation for
  model-based work.

## Layer 3: Rendering and assets

The rendering side is where digital-twin / sim2real lives.

- **USD (Universal Scene Description).** The format. Read the Pixar
  tutorials. Understand "stages, layers, composition arcs, prims."
  This is the JSON of the sim world.
- **PBR (physically-based rendering) materials.** Roughness,
  metallic, normal, albedo — the same 4-5 textures you've seen in
  Blender / Three.js.
- **Ray tracing basics.** NVIDIA RTX path tracing is what makes
  Isaac Sim photoreal. Slow but high quality. Faster
  rasterization-only modes exist.
- **Procedural generation.** USD composition arcs let you build
  layouts programmatically. Combined with BlenderProc / NVIDIA
  Replicator, this is how you generate 100k+ scenes from a few
  templates.
- **3D Gaussian Splatting, NeRF, neural reconstruction.** For
  building digital twins from real captures. Polycam / Luma /
  Matterport are the consumer-side capture tools.

## Layer 4: Reinforcement learning (enough to drive sim)

You don't need PhD-level RL; you need to be able to train and tune
a PPO baseline.

- **Algorithms to know by name:** PPO (the workhorse for sim
  training), SAC (off-policy, sample-efficient), TD3, A2C.
- **On-policy vs off-policy.** PPO collects fresh data each
  iteration; SAC reuses a replay buffer. PPO + thousands of parallel
  envs is the dominant sim-training pattern.
- **Reward shaping.** The art of designing reward functions that
  produce the behavior you want without exploits. Frequently
  underestimated in difficulty.
- **Curriculum learning.** Start easy, get harder. The classic way
  to train policies that wouldn't converge from random init.
- **Offline RL** (CQL, IQL, TD3+BC) — RL that learns from a fixed
  dataset. Useful when sim is expensive.

Knowing RL adds **+33% to salary** per the 2025 Robotics Salary
Guide. This is the single best ROI training topic in the field.

## Layer 5: Sim-to-real techniques

The art of crossing the reality gap. Five techniques you'll see
everywhere:

- **Domain randomization** (textures, lighting, friction, masses,
  sensor noise). The original sim2real workhorse.
- **System identification.** Measure the real robot's properties
  (friction, inertia, motor delay) and plug them back into sim.
- **Privileged-teacher / DR-student** (RMA recipe). Train a teacher
  policy in sim with full state access, then distill into a student
  that only sees realistic sensors.
- **Real-to-sim asset capture.** Scan the real environment with a
  phone (Polycam, Luma, Matterport), import into the sim.
- **Cosmos / world models for video-level augmentation.** Use a
  generative world model to "imagine" alternate futures from the
  same starting state, training on a much larger effective dataset.

## Layer 6: Synthetic data pipelines

A big slice of "sim work" is just generating labeled data.

- **NVIDIA Replicator** — Isaac Sim's randomization + annotation
  framework. Generates labeled images at scale (2D / 3D boxes,
  segmentation masks, depth, normals, optical flow).
- **BlenderProc** — open-source procedural Blender data pipeline.
- **NVISII** — Python ray tracer for synthetic data.
- **NVIDIA Omniverse Kit extensions** — custom Python extensions
  inside Omniverse. The way to build serious customer-facing tools.

## Layer 7: Tools and platforms

- **Isaac Sim + Isaac Lab** for high-fidelity GPU-parallel training.
  Free to download; closed source but Python-scriptable.
- **MuJoCo + MJX** for fast research iteration. JAX-based.
- **Genesis** for unified fast differentiable sim (2024+).
- **Gazebo Garden** for ROS2-native sim. The standard if your
  product also talks ROS2.
- **Drake** for model-based, contact-rich research.
- **CARLA, NVIDIA DRIVE Sim** for autonomous-vehicle research.
- **Weights & Biases / MLflow** for experiment tracking.
- **Hydra / OmegaConf** for hierarchical YAML configs (you'll have
  many).
- **Docker, CUDA, NVIDIA Container Toolkit** — yes, again. Versions
  matter.

## Layer 8: Mathematical comfort

Same as VLA / perception:

- linear algebra (matrices, eigenvectors, SVD),
- multivariable calculus (gradients, chain rule),
- probability (distributions, KL divergence),
- basic optimization (SGD, Adam, schedules),
- some classical mechanics (Newton's laws is enough).

3Blue1Brown's "Essence of linear algebra" and "Essence of calculus"
playlists are sufficient as a refresher.

## Must-read papers (in this order)

1. **Domain Randomization** (Tobin et al., IROS 2017).
2. **OpenAI Rubik's Cube** (2019).
3. **ANYmal sim-to-real RL** (Hwangbo et al., Science Robotics 2019).
4. **Rapid Motor Adaptation** (Kumar et al., RSS 2021).
5. **Isaac Lab / Orbit** (Mittal et al., 2023).
6. **MimicGen** (Mandlekar et al., CoRL 2023).
7. **RoboCasa** (NVIDIA, 2024).
8. **DextrAH** (NVIDIA, 2024).
9. **Cosmos** (NVIDIA, 2025).

Write a 1-page summary of each in your own words.

## Communities and people to follow

- Conferences: **CoRL**, **RSS**, **ICRA**, **IROS**, **NeurIPS**
  robotics workshops.
- NVIDIA Isaac Sim forum and Discord (the most active sim-specific
  community).
- MuJoCo forum on the DeepMind side.
- OpenUSD community at openusd.org.
- X/Twitter: @YukezhuYuke (RoboCasa), @drjimfan (NVIDIA GEAR),
  @DieterFox, @hjones (Isaac), @AnimeshGarg.
