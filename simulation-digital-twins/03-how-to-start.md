# How to Get Started

## Week 1: MuJoCo first

- Install MuJoCo (free since 2021). Run the MJX tutorials end to end.
- Build a custom XML scene with a UR5 or Panda + a few objects.
- Train PPO on a simple reach task with Brax or MJX.

## Week 2: Isaac Sim / Isaac Lab

- Install Isaac Sim 4.x. Run the Isaac Lab quickstart on a quadruped
  locomotion task with 4096 parallel envs.
- Walk through the Replicator tutorials for synthetic-data generation.

## Week 3: USD and assets

- Learn USD basics with Pixar's tutorials.
- Build a custom factory or kitchen scene via composition arcs.
- Convert a glTF model to USD; tag it with SimReady metadata.

## Week 4: Sim-to-real

- Reproduce a small ANYmal-style RL locomotion result and run domain
  randomization sweeps in Isaac Lab.
- Read the RMA paper and try the privileged-teacher / DR-student
  recipe.

## Week 5: Digital twin from scan

- Scan a real room with Polycam or RealityCapture; convert to USD via
  Omniverse.
- Add physics colliders, lights, and a moving robot.

## Week 6: Differentiable physics

- Try MJX or Genesis with a differentiable contact task (cloth, push).
- Read DiffMimic / Brax differentiable-control examples.

## Week 7-8: A buildable showcase

Pick one and ship it:

- A procedural warehouse generator that emits randomized USD scenes.
- A Sim2Real toolkit for a Franka arm with one trained policy.
- A synthetic dataset (100k frames) for a specific vision benchmark.

## Communities

NVIDIA Isaac Sim forum and Discord; MuJoCo forum; CoRL / RSS workshops
on sim-to-real; OpenUSD community; X/Twitter: @YukezhuYuke, @hjones,
@DieterFox.
