# Part 01 — Scope & workflow (simulation)

> **Sim goal:** Stand up the entire HPLC sample-prep cell as a
> Gazebo Harmonic world — the reBot arm bolted to a bench surrounded
> by every station at a known location — and prove the arm can reach
> all of them before any other part is built.

This document is the foundation the other nine sim docs build on.
Everything downstream (gripping, decapping, dispensing, tray loading,
perception, orchestration) assumes a working **digital twin** of the
cell already exists. A digital twin here just means a simulated copy
of the bench, accurate enough in **layout and geometry** to test
software against. This part creates that copy and answers the first
gating question: *with the arm fixed where we plan to fix it, can it
physically reach every place it needs to touch?*

## What we can prove in simulation

In open-source sim, entirely before buying anything, we can prove:

- **Cell layout works.** The arm, bench, and all stations fit
  together and do not collide at rest.
- **Reachability.** Every station's working point sits inside the
  arm's reachable workspace (the set of poses the arm can actually
  achieve), with margin for approach and retreat.
- **The end-to-end loop is expressible.** The full per-vial sequence
  can be scripted and stepped through as motion-planning goals.
- **Cycle-time first estimate.** Once motions plan, summing planned
  trajectory durations gives an early throughput figure (hedge it —
  sim timing ignores real settling and station dwell).

What sim **cannot** prove here: that the real bench is rigid enough,
that the arm's real repeatability lands the gripper on a 2 mL vial,
or that station fixtures align in millimetres on the physical bench.
Those are hardware-acceptance items (see
`10-hardware-platform-and-capital-model.md`). Sim proves the plan is
*geometrically and logically sound*, not that the metal behaves.

## Open-source tools

| Tool | Role | Bottom line |
|------|------|-------------|
| Gazebo Harmonic (gz-sim) | Physics + 3D world holding bench and stations | Primary simulator; fully open, good ROS 2 bridge. |
| reBot URDF | Robot description (links, joints, meshes) | Ships with reBot; the single source of arm geometry. |
| `gz_ros2_control` | Drives the URDF's joints inside Gazebo | Lets ROS 2 controllers command the simulated arm. |
| ROS 2 (Humble/Jazzy) | Middleware tying nodes together | Standard; everything speaks ROS 2 topics/actions. |
| MoveIt 2 | Motion planning + reachability checks | Plans collision-free arm motions to each station. |
| MoveIt Setup Assistant | Generates a MoveIt config from the URDF | One-time step since official reBot config is pending. |
| RViz2 / Foxglove | Visualisation + interactive goal poses | See the cell, drag goals, confirm reach by eye. |
| Pinocchio / MeshCat | Fast kinematics + lightweight viewer | Scriptable reachability sweeps outside Gazebo. |

## How to simulate it now

The reBot Arm B601-DM ships an open URDF and a ROS 2 workspace
(`rebotarm_ros2`) exposing `/joint_states`, `FollowJointTrajectory`,
`GripperCommand`, and `MoveToPose` (assets:
`Seeed-Projects/reBot-DevArm`). As of early 2026 the official MoveIt 2
config and Isaac Sim USD import were still "in development", so for a
fully open stack we drive the URDF ourselves. We do **not** need the
hardware driver for sim.

**1. Build the world SDF.** Author a Gazebo `world.sdf` describing the
static cell:

- a **bench** model (a box) at the world origin;
- the reBot **base mount** frame on the bench top;
- one static model per station, each placed at a fixed, named
  transform (**tf frame** — a named coordinate frame ROS 2 tracks):
  - `vial_supply` — a nested rack of empty/incoming 2 mL vials;
  - `decap_station` — the decapping/capping fixture (Part 03);
  - `dispense_station` — the diluent/standard dispenser (Part 04);
  - `scan_station` — the barcode/label reader pose (Part 06);
  - `autosampler_tray` — the destination tray (Part 05).

  Publish these as static transforms with a
  `static_transform_publisher` per frame, or bake them into a single
  `tf` URDF/Xacro for the bench so every node shares one map of where
  things are.

**2. Spawn the arm.** Add `gz_ros2_control` to the reBot URDF as the
`<ros2_control>` hardware plugin, then spawn the robot into the world
with `ros_gz_sim create -topic robot_description`. Bring up a
`joint_state_broadcaster` and a `joint_trajectory_controller` so the
arm answers `FollowJointTrajectory`, mirroring the real driver's
interface — meaning the same higher-level code works on sim and (later)
hardware.

**3. Generate the MoveIt config.** Run the **MoveIt Setup Assistant**
on the reBot URDF once: define the arm planning group, the gripper
group, the self-collision matrix, and named poses (`home`, `ready`).
Save the generated config package and launch `move_group` against the
simulated controllers. RViz2's MotionPlanning panel now plans for the
sim arm.

**4. Reachability check (the gate for this part).** Before anything
else, confirm the arm reaches each station:

- In RViz2, set the planning frame to the bench base, then send a
  goal pose at each station's tf frame (plus a short approach offset
  along the tool axis). A successful plan = reachable.
- Automate it: a small node loops over the five station frames,
  calls MoveIt's `plan` (or `MoveToPose`), and records
  success/failure and IK (inverse-kinematics — solving joint angles
  for a desired hand pose) solutions. A Pinocchio script can sweep a
  grid of approach poses per station for a fuller reachability map.
- If a station is unreachable, move it in the SDF (or relocate the
  arm mount) and re-run. Iterating here is free; iterating on a real
  bench is not.

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

Beyond the reBot arm and its gripper, the real cell needs a rigid
**bench**, **fixtures/jigs** that hold each station in a repeatable
spot, and the **autosampler** itself (the instrument front-end that
draws from the tray). In this part *none of these are bought* — each
is a **static model** in the Gazebo world:

- bench, jigs, racks → simple box/mesh models at fixed tf frames;
- autosampler tray → a model with addressable slot frames;
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
- High-level companion: `../03-high-level-solution/01-scope-and-workflow.md`.
- Folder overview: `README.md`.
