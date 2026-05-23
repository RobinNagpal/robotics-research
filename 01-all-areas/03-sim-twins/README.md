# Simulation & Digital Twins

> Written for a web developer who has never touched a robot. We'll
> define every term and lean on analogies from web development.

## What is this subfield, in one paragraph?

Robots are expensive, fragile, and slow to iterate on. A single
real-world training run might mean a $30k arm, a human operator, and a
day of work — for one data point. **Simulation** sidesteps that: you
build a virtual robot inside a physics engine and run thousands of
copies in parallel on a GPU. **Digital twins** are the same idea
applied to a *specific* real environment (one warehouse, one factory
floor, one hospital): a high-fidelity virtual replica that you can
test policies against before deploying to the real building.

If you've ever set up a staging environment that mirrors production
exactly, that's the web-dev analogue. A simulator is staging for
robots — except it also runs your unit tests at 10,000x real-time and
generates training data for free.

## Why is this called "digital twin," and how is it different from "simulation"?

- **Simulator** = a generic virtual world. ("a kitchen," "a tabletop,"
  "a sidewalk.") Used for training and benchmarking.
- **Digital twin** = a virtual replica of *a specific real asset* (a
  particular Amazon fulfillment center, a particular surgical robot
  arm with its measured friction values). Used for predictive
  maintenance, fleet validation, and pre-deployment testing.

You'll see both terms used interchangeably in marketing. Underneath,
they share 90% of the same tech stack (USD assets, MuJoCo / Isaac Sim
/ PhysX physics, GPU rendering).

## Why is this one of the top-3 picks?

- **Pure software.** Zero robots required, ever. You can do all of
  this from a single workstation with a decent NVIDIA GPU, or from
  rented cloud GPUs.
- **Fastest-growing market segment in robotics by CAGR.** The
  Physical-AI simulation + digital-twin market is projected to grow
  from **$3.8B in 2025 to $34.6B by 2034 (~28.5% CAGR)** — the
  highest of any segment in this analysis. Source: market reports
  cited in the 2025 Robotics Salary Guide.
- **Customer demand is acute right now.** Every humanoid startup
  (Figure, 1X, Apptronik, Skild, Physical Intelligence) is burning
  cash on data collection. Anything that 10x's data via sim is
  immediately useful.
- **NVIDIA is investing hard.** Isaac Sim, Isaac Lab, Omniverse,
  Cosmos — NVIDIA has put unprecedented dollars into this stack
  since 2023. That has both pulled the field forward and created
  a hiring surge.
- **Pulls from web-dev skills.** Most sim work is Python + Python +
  Python, with USD assets in JSON-ish files, web dashboards (W&B,
  Streamlit) for tracking, and Docker for reproducible
  environments. The transferable surface is huge.

## Files in this folder

- [01-examples-of-work.md](01-examples-of-work.md) — production
  simulators, digital-twin platforms, landmark research.
- [02-important-to-learn.md](02-important-to-learn.md) — layered
  curriculum from physics basics to differentiable rendering.
- [03-how-to-start.md](03-how-to-start.md) — concrete 8-week plan.
- [04-major-new-employers.md](04-major-new-employers.md) — who hires
  sim engineers, with comp bands.
- [05-projects-to-sell.md](05-projects-to-sell.md) — five projects
  you can ship and bill for.

## Glossary (read this once before the other files)

- **Simulator** — a program that models physics + rendering so a
  virtual robot can interact with virtual objects. Examples: MuJoCo,
  Isaac Sim, PyBullet, Drake.
- **Physics engine** — the math that resolves "what happens when
  these objects touch." Rigid-body dynamics, collisions, friction,
  constraints.
- **Rendering** — turning the 3D scene into images for the virtual
  camera. Either rasterization (fast, game-style) or ray tracing
  (slow, photoreal).
- **Domain randomization** (DR) — during training, randomly vary
  textures, lighting, friction, masses, sensor noise. Forces the
  policy to be robust so it survives the messier real world.
- **Sim-to-real (Sim2Real)** — the act of training a policy in sim
  and deploying it on a real robot. The "reality gap" is the
  performance drop when you cross over.
- **USD (Universal Scene Description)** — Pixar's open file format
  for 3D scenes; the JSON of modern simulation. NVIDIA standardized
  on it across Isaac and Omniverse.
- **URDF / SDF / MJCF / Onshape XML** — older robot-description
  formats (XML files describing joints + links + collision meshes).
  You'll convert between these and USD constantly.
- **Differentiable simulation** — a simulator where you can backprop
  gradients through the physics. Lets you train policies with
  gradient descent instead of RL. Examples: MJX, Brax, Genesis,
  Drake autodiff.
- **Parallel envs** — run thousands of copies of the same simulation
  on a single GPU. Standard for modern RL training. Isaac Lab
  ships with 4096+ parallel envs per GPU as a default.
- **Replicator** — Isaac Sim's domain-randomization + synthetic-data
  framework. Generates labeled images at scale.
- **Reality gap** — the residual difference between sim and real
  that makes policies fail when deployed. The whole sim-to-real
  field exists to shrink this gap.
- **World model** — a learned simulator (a neural net that predicts
  "next frame given current frame + action"). Examples: NVIDIA
  Cosmos, 1X's NEO world model, DreamerV3.
