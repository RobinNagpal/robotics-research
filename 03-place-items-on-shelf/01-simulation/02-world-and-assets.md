# Phase 1 — The store world & assets

> **Goal:** a static Gazebo Harmonic world holding the aisle, one
> shelving unit, the floor, and lighting — plus the three physics assets
> the task needs: the **SKU**, the **shelf**, and the **tray**. Build the
> *smallest* asset set and randomize from there (`../01-requirements.md`
> §scope, `../03-stack/01-simulator.md`).
>
> **Checkpoint:** the world loads; a can dropped on the shelf and tray
> settles and stays put (stable contacts, no jitter or sink-through).

---

## 1.1 The world file

`shelf_worlds/worlds/store_aisle.sdf` — an SDF world with:

- the **physics** system, **sensors** system, **scene broadcaster**, and
  **user commands** systems (the standard `gz-sim` plugin set so sensors
  and spawning work);
- a **ground plane** and a couple of **directional/area lights** giving
  roughly uniform illumination (v1 assumes good lighting —
  `../01-requirements.md` §3);
- an **aisle**: two facing shelving units or one shelf + a back wall, at
  standard grocery spacing so the base has a realistic stand-off.

Keep gravity at `-9.81`, a small fixed timestep (e.g. `0.001 s`) for
stable contacts, and a real-time factor of 1.0 to start.

## 1.2 The shelf model

`shelf_worlds/models/grocery_shelf/` as an SDF model:

- **Static** (`<static>true</static>`) — it never moves, so it is pure
  collision + visual geometry, cheap to simulate.
- Modeled to **standard grocery dimensions**: shelf height(s) in the
  arm's reach envelope, a flat open-faced shelf board for a **single
  layer, side-by-side** placement (no stacking — §scope).
- Give the shelf board realistic **friction** so a placed can doesn't
  slide off.
- Define a **slot origin** convention (a known frame/offset on the shelf
  board) that the planogram will reference in Phase 5.

## 1.3 The SKU (the product)

`shelf_worlds/models/can_sku/` — one rigid SKU, e.g. a 400 g can:

- A single link with **realistic mass (~0.4 kg)**, a cylinder collision,
  and a center of mass roughly central.
- **Friction (`mu`, `mu2`)** tuned so a parallel-jaw grasp can hold it —
  too low and it squirts out, too high and contacts jitter. This is the
  number you will tune most.
- Inertia computed from the cylinder (don't leave default unit inertia —
  it causes instability).
- Known outer dimensions and a **preferred grasp** (side pinch for a can)
  recorded in the model's metadata / a sidecar YAML for the grasp layer.

> Start with **one** SKU. A second SKU is a later milestone, not now.

## 1.4 The tray

`shelf_worlds/models/tray/`:

- A shallow tray with **fixed, known cell positions** (the "known tray
  layout" from `../01-requirements.md` §5) so the first pick needs no bin
  perception.
- Mounted to the robot in Phase 2 at a known pose; for now model it
  standalone and verify cans sit in their cells stably.

## 1.5 Spawning & a smoke test

- Add the shelf and tray to the world directly; spawn the SKU(s) via
  `ros_gz_sim create` (service spawn) so the orchestration layer can
  re-spawn a fresh tray each run.
- **Smoke test:** drop a can onto the shelf board and into a tray cell.
  It should settle within a few timesteps and **stay put** for 30 s with
  no drift. If it jitters, sinks, or slides, fix mass/inertia/friction
  and timestep **now** — every later phase inherits these contacts.

## 1.6 A note on randomization

Gazebo gives geometric randomization cheaply: jitter the **tray cell
offsets**, the **SKU spawn pose**, and the **robot start pose** between
runs (Phase 5 uses this for the success-rate log). Save photoreal visual
randomization (textures, lighting sweeps) for the **Isaac Sim** stage —
Gazebo is the wrong tool for it (`../03-stack/01-simulator.md`).

## Deliverables

- `store_aisle.sdf` loads in `gz sim` with shelf, tray, floor, lighting.
- `can_sku`, `grocery_shelf`, `tray` models with tuned mass/friction.
- A documented **slot-origin** frame and **tray-cell** layout for later
  phases.

## Checkpoint

The world loads and a can rests stably on both the shelf and a tray cell.
Stable contacts proven — move to Phase 2 (the robot).
