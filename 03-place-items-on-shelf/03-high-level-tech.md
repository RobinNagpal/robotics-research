# High-level tech — simulating the store, the robot, and the task

> The frameworks to build the shelf-stocking robot from
> `01-requirements.md`. This is a **simulation-first** project: stand up
> the store and the mobile manipulator in a simulator, prove the
> pick-drive-place loop there, then transfer. Everything below is glued
> together with **ROS 2** so the same nodes run in sim and on hardware.
>
> **New to the jargon?** Every technical term used below (ROS, USD,
> URDF, RGB-D, SLAM, AMCL, and the rest) is explained in one or two
> plain sentences in `02-glossary.md` — read that first.

---

## Stack at a glance

| Layer | Job | Recommended | Alternatives |
|-------|-----|-------------|--------------|
| Simulator | The store, shelves, products, physics | **NVIDIA Isaac Sim** | Gazebo (Harmonic), MuJoCo, Genesis |
| Middleware | Connect everything, sim↔real parity | **ROS 2** (Jazzy/Humble) | — |
| Mobile base | Map, localize, drive to shelf | **Nav2** | — |
| Arm motion | Collision-free pick/place trajectories | **MoveIt 2** | cuMotion, Pinocchio + custom |
| Perception | Find shelf face, slot, product pose | RealSense-style RGB-D + **FoundationPose** / planar fits | YOLO-World, Grounding DINO, SAM 2 |
| Grasping | Where/how to grab the SKU | **AnyGrasp / Contact-GraspNet** | analytical antipodal (rigid SKU) |
| Orchestration | Sequence the task, handle failures | **Behavior Trees** (BehaviorTree.CPP / Nav2 BT) | state machine (SMACH/YASMIN) |

Each row has a dedicated deep-dive in `03-stack/` — a side-by-side
comparison of the candidate frameworks on 5-7 parameters with a top
pick: `01-simulator.md`, `02-middleware.md`,
`03-mobile-base-navigation.md`, `04-arm-motion-planning.md`,
`05-perception.md`, `06-grasping.md`, `07-orchestration.md`.

---

## 1. Simulating the store

The simulator must model three things: the **store environment**
(aisle, shelves, floor), the **products** (rigid bodies with mass and
friction), and the **robot** (mobile base + arm) — all under one physics
engine so contacts and grasps behave.

- **NVIDIA Isaac Sim (recommended).** Best fit for a *mobile
  manipulator* in a photorealistic store. USD-based scene composition
  makes it easy to lay out an aisle, drop in shelf and product assets
  (Isaac/SimReady or imported USD/CAD), and randomize lighting, texture,
  and product pose via **Replicator** — which is exactly what you need
  to train/validate perception and not overfit to one clean scene. Has
  a maintained **ROS 2 bridge**, and pairs with **Isaac Lab** if you
  later want RL/learned policies.
- **Gazebo (Harmonic).** The lighter, fully open, ROS-native option.
  Excellent Nav2 + MoveIt 2 integration and far cheaper on hardware.
  Less photorealism, so weaker for the *perception* half — fine if you
  start with geometric/known-pose placement and add learned perception
  later.
- **MuJoCo / Genesis.** Strong, fast contact physics for the
  grasp/place dynamics in isolation; less suited to a whole navigable
  store. Useful as a focused rig for tuning the place motion.

**Assets:** model the aisle and shelving to standard grocery
dimensions; represent the SKU as a rigid body with realistic mass,
friction, and (for suction) a flat graspable face. Build a **small
asset set first** (one shelf, one SKU, one tray) and randomize from
there.

---

## 2. The robot model (mobile base + arm)

- Describe the robot as a single **URDF** (Gazebo/MoveIt) or **USD**
  (Isaac Sim) **mobile manipulator** — base, arm joints, gripper, and
  the wrist camera frame in one kinematic tree, so base + arm are
  reasoned about together (the whole-body reach problem in the
  requirements).
- Sensors to model: 2D lidar + wheel odometry on the base (for Nav2),
  and one wrist-mounted RGB-D camera (for slot/product perception).
- Keep joint limits, link masses, and gripper geometry realistic from
  the start — these drive both motion planning and the sim-to-real gap.

---

## 3. Navigation — drive to the shelf (Nav2)

- **Nav2** handles the mobile half: SLAM or a pre-built map,
  localization (AMCL), global + local planning, and recovery behaviors.
- For v1 the goal is a fixed **picking pose** in front of the target
  shelf; Nav2 drives there, then a short vision-based alignment step
  refines the pose relative to the shelf face before manipulation.
- Dynamic obstacles (a shopper) trigger Nav2's costmap → in v1 this maps
  to a **safe-stop**, not a clever re-route (per requirements §7).

---

## 4. Arm motion — pick and place (MoveIt 2)

- **MoveIt 2** plans collision-free trajectories for the pick (tray →
  grasp) and place (grasp → slot) using the scene as a collision world
  (shelf, neighbors, base).
- Model the shelf and already-placed products as collision objects so
  the arm doesn't clip a neighbor — knocking over a neighbor is a
  defined failure.
- **cuMotion** (GPU motion planning, ships with Isaac) is a drop-in
  upgrade if planning latency dominates cycle time later.
- The place is a **guarded/compliant set-down**: approach, light contact
  with the shelf, release — not a free-space drop.

---

## 5. Perception — find the slot and the product

This is the part that ties back to the perception-cv area, and it scales
with how much "known" you allow yourself:

- **v1 (mostly known):** product comes from a known tray layout and the
  slot is computed from the planogram + a **planar fit of the shelf
  face** from the RGB-D point cloud. Minimal learning — geometry plus a
  known SKU model.
- **Product pose:** for the known rigid SKU, **FoundationPose** (6-DoF
  pose from RGB-D + the CAD/mesh) gives a robust pick pose and a
  natural step up from "fixed tray position."
- **Slot/empty-space detection:** segment the shelf and find the empty
  region for the next facing — start geometric, move to **SAM 2** /
  open-vocab detection (**YOLO-World**, **Grounding DINO**) when you
  relax the "known layout" assumption.
- **Grasp synthesis:** for the rigid SKU an analytical antipodal/suction
  grasp is enough; **AnyGrasp** or **Contact-GraspNet** generalize it
  once SKUs vary.
- **Train/validate on randomized sim** (Isaac Replicator: lighting,
  texture, pose) so perception survives the sim-to-real gap.

---

## 6. Orchestration — sequencing the task

- Drive the pick-drive-place loop (requirements §6) with a **Behavior
  Tree** (BehaviorTree.CPP, or the Nav2 BT engine you're already
  running). BTs make the failure/skip/safe-stop logic explicit and
  reusable.
- Each leaf is a ROS 2 action: `NavigateToShelf`, `PickProduct`,
  `LocateSlot`, `PlaceProduct`, `VerifyPlacement`. Per-unit
  success/failure logging lives here.
- A simple state machine (SMACH/YASMIN) is an acceptable lighter-weight
  alternative for v1.

---

## 7. Recommended path for v1

1. **Gazebo + ROS 2 + Nav2 + MoveIt 2** to get the *mechanics* working
   end to end with known tray and planogram (no learned perception):
   drive to shelf, pick from a known pose, place by geometry. Cheapest
   way to prove the loop.
2. **Move to Isaac Sim** (or add it alongside) for **photorealistic,
   randomized perception** — FoundationPose for product pose, shelf/slot
   detection — so the vision half is trained and validated against
   domain randomization, not a single clean scene.
3. **Harden + measure:** randomize start poses, tray positions, and
   lighting; collect the per-unit success-rate log from requirements §9.
4. **Then** consider a hardware pilot, reusing the same ROS 2 nodes.

Keep the ROS 2 interface identical across sim and hardware so the
transfer is a swap of drivers, not a rewrite.
