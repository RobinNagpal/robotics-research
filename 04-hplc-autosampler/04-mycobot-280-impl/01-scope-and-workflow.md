# Part 01 — Scope & workflow (myCobot 280 simulation)

> **Sim goal:** Stand up the whole HPLC sample-prep cell as a Gazebo
> Harmonic world — an Elephant Robotics myCobot 280 fixed to a bench,
> ringed by static station models at known locations — and answer the
> one gating question this small arm raises first: with only ~280 mm
> of reach, can it actually touch every station?

This document is the foundation the other nine sim docs build on.
Everything downstream (gripping, decapping, dispensing, tray loading,
perception, orchestration) assumes a working **digital twin** of the
cell already exists. A digital twin here just means a simulated copy
of the bench — accurate enough in **layout and geometry** to test
software against, not a perfect physics replica.

The myCobot 280 is a compact 6-DoF (six-degrees-of-freedom, i.e.
six independent joints) desktop cobot: roughly ~250 g payload and a
~280 mm working radius (`~` — verify against the current datasheet).
A 2 mL vial weighs only a few grams, so payload is never the
constraint here. **Reach is.** This part is where we find out whether
the loop even fits inside that small bubble.

## What we can prove in simulation

Entirely before buying anything, the open-source sim lets us prove:

- **Cell layout works.** Arm, bench, and all stations fit together
  and do not collide at rest.
- **Reachability (the headline for the 280).** Every station's
  working point sits inside the arm's reachable workspace (the set of
  poses the arm can physically achieve), with margin for approach and
  retreat. Given ~280 mm, this is the make-or-break check.
- **The end-to-end loop is expressible.** The full per-vial sequence
  can be scripted and stepped through as motion-planning goals.
- **Layout decision.** If stations do not all fit the reach bubble,
  sim is where we choose the fix: **cluster** them tighter, add a
  small **rail or turntable** to extend effective reach, or step up
  to a **myCobot 320** (~500 mm reach, ~1 kg payload).
- **Cycle-time first estimate.** Once motions plan, summing planned
  trajectory durations gives an early throughput figure (hedge it —
  sim timing ignores real settling and station dwell).

What sim **cannot** prove here: that the real bench is rigid enough,
that the 280's real repeatability (the small desktop arms are less
precise than industrial ones) lands the gripper on a 2 mL vial, or
that station fixtures align in millimetres on the physical bench.
Those are hardware-acceptance items (see
`10-hardware-platform-and-capital-model.md`). Sim proves the plan is
*geometrically and logically sound*, not that the metal behaves.

## Open-source tools

| Tool | Role | Bottom line |
|------|------|-------------|
| Gazebo Harmonic (gz-sim) | Physics + 3D world holding bench and stations | Primary simulator; fully open, good ROS 2 bridge. |
| `mycobot_ros` | Ships the 280 URDF, a Gazebo sim, and a MoveIt config | Big head start — assets exist today; we adapt, not author. |
| myCobot 280 URDF | Robot description (links, joints, meshes) | Single source of arm geometry; comes from `mycobot_ros`. |
| `gz_ros2_control` | Drives the URDF's joints inside Gazebo | Lets ROS 2 controllers command the simulated arm. |
| ROS 2 (Humble/Jazzy) | Middleware tying nodes together | Standard; everything speaks ROS 2 topics/actions. |
| MoveIt 2 | Motion planning + reachability checks | Plans collision-free arm motions to each station. |
| RViz2 / Foxglove | Visualisation + interactive goal poses | See the cell, drag goals, confirm reach by eye. |
| Pinocchio / MeshCat | Fast kinematics + lightweight viewer | Scriptable reachability sweeps outside Gazebo. |

Note: `pymycobot` is Elephant's Python API for the **real** arm. We do
**not** use it in sim — in simulation we drive the URDF through
`gz_ros2_control` and MoveIt 2 so the same higher-level code targets
sim now and hardware later.

## How to simulate it now

`mycobot_ros` (GitHub `elephantrobotics/mycobot_ros`) already ships a
280 URDF, a Gazebo simulation, and a ready-made MoveIt config. So
unlike a from-scratch arm, our starting point is mostly assembling
existing assets rather than authoring them.

**1. Bring up the arm from `mycobot_ros`.** Clone the package into a
ROS 2 workspace and launch its Gazebo + MoveIt setup as the baseline.
Confirm the simulated arm exposes `/joint_states` and answers a
`FollowJointTrajectory` action through a `joint_trajectory_controller`,
and that `move_group` plans against it. This is sim/hardware parity:
the same action interface the real driver would present.

**2. Build the world SDF (the cell).** Extend the stock world into our
static cell. Author a Gazebo `world.sdf` describing:

- a **bench** model (a box) at the world origin;
- the myCobot 280 **base mount** frame on the bench top;
- one static model per station, each at a fixed, named transform
  (**tf frame** — a named coordinate frame ROS 2 tracks):
  - `vial_supply` — a nested rack of empty/incoming 2 mL vials;
  - `decap_station` — the decapping/capping fixture (Part 03);
  - `dispense_station` — the diluent/standard dispenser (Part 04);
  - `scan_station` — the barcode/label reader pose (Part 06);
  - `autosampler_tray` — the destination tray (Part 05).

  Publish these as static transforms with a
  `static_transform_publisher` per frame, or bake them into a single
  bench Xacro so every node shares one map of where things are.

**3. Spawn the arm into the cell.** Ensure the URDF carries a
`<ros2_control>` block with the `gz_ros2_control` plugin, then spawn
it with `ros_gz_sim create -topic robot_description`. Bring up a
`joint_state_broadcaster` and the `joint_trajectory_controller`.

**4. Reachability check (the gate for this part).** This is the step
the 280's short reach makes essential:

- In RViz2, set the planning frame to the bench base, then send a
  goal pose at each station's tf frame (plus a short approach offset
  along the tool axis). A successful plan = reachable.
- Automate it: a small node loops over the five station frames,
  calls MoveIt's `plan`, and records success/failure and IK
  (inverse-kinematics — solving joint angles for a desired hand pose)
  solutions. A Pinocchio script can sweep a grid of approach poses per
  station for a fuller reachability map.
- **If a station falls outside ~280 mm**, this is the decision point.
  In order of least to most cost: (a) **cluster** the stations tighter
  around the base; (b) add a short **linear rail** under the arm or a
  small **turntable** that re-presents stations into reach; (c)
  re-mount the arm; (d) conclude the 280 is too small and re-run the
  whole study on a **myCobot 320**. Iterating in the SDF is free;
  iterating on a real bench is not — which is the entire point of
  proving it in the twin first.

**5. Express the loop.** With every station reachable, encode the
per-vial loop as an ordered list of goals the twin must execute:

```
pick (vial_supply)
  -> scan (scan_station)
    -> decap (decap_station)
      -> dispense (dispense_station)
        -> cap (decap_station)
          -> place (autosampler_tray slot N)
```

This document only proves each step is *reachable and plannable*. The
station behaviours themselves (grasp-fix, cap toggle, fill-volume
mutation) arrive in Parts 02–07; orchestration of the whole loop is
Part 08.

## Additional hardware needed

Beyond the myCobot 280 and its gripper, the real cell needs a rigid
**bench**, **fixtures/jigs** that hold each station in a repeatable
spot, the **autosampler** itself (the instrument front-end that draws
from the tray), and — quite possibly for the 280 specifically — a
small **rail or turntable** to buy back reach. In this part *none of
these are bought* — each is a **static model** in the Gazebo world:

- bench, jigs, racks → simple box/mesh models at fixed tf frames;
- autosampler tray → a model with addressable slot frames;
- rail/turntable (if the reachability check demands it) → a modelled
  prismatic or revolute joint we can plan with;
- stations → static models now, upgraded to **mock-station service
  nodes** (ROS 2 nodes that fake a station's behaviour at its tf
  frame) in their respective parts.

The fidelity claim is deliberately modest: geometry and placement are
real enough to test reach and motion; physical rigidity, vibration,
and mounting tolerance are deferred to hardware bring-up.

## How it connects

- **This is the base layer.** Every other sim doc assumes the world,
  arm spawn, and MoveIt config from here already run.
- `02-vial-handling-and-gripping.md` — adds the vial models and grasp
  behaviour at the `vial_supply` rack defined here.
- `03-decapping-and-capping.md`, `04-liquid-handling-and-sample-prep.md`,
  `05-tray-loading-and-positioning.md` — turn the static
  `decap_station`, `dispense_station`, and `autosampler_tray` models
  into active mock stations.
- `08-orchestration-error-handling-and-safety.md` — drives the
  pick→scan→decap→dispense→cap→place loop expressed here.
- `10-hardware-platform-and-capital-model.md` — carries the
  280-vs-320 reach decision into the buy/cost case.
- High-level companion: `../01-high-level-solution/01-scope-and-workflow.md`.
- Folder overview: `README.md`.
