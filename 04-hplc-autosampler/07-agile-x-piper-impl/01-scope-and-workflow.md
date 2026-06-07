# Part 01 — Scope & workflow (AgileX PiPER simulation)

> **Sim goal:** Stand up the whole HPLC sample-prep cell as a Gazebo
> Harmonic world — an AgileX PiPER arm fixed to a bench, ringed by
> static station models at known locations — and prove the per-vial
> loop is reachable and plannable before any hardware is bought.

This document is the foundation the other nine sim docs build on.
Everything downstream (gripping, decapping, dispensing, tray loading,
perception, orchestration) assumes a working **digital twin** of the
cell already exists. A digital twin here just means a simulated copy
of the bench — accurate enough in **layout and geometry** to test
software against, not a perfect physics replica.

The PiPER is a lightweight 6-DoF (six-degrees-of-freedom, i.e. six
independent joints) arm: roughly ~1.5 kg payload, ~600 mm reach, and
~4.2 kg arm weight (`~` — verify against the current datasheet). A
2 mL vial weighs only a few grams, so payload is never the constraint
here, and unlike a tiny desktop arm, **reach is not the gating
worry either**. The ~600 mm working radius comfortably serves several
spread-out stations, so we can lay the cell out on a normal bench
rather than packing everything into a cramped bubble. This part is
where we confirm that comfortable layout actually closes.

## What we can prove in simulation

Entirely before buying anything, the open-source sim lets us prove:

- **Cell layout works.** Arm, bench, and all stations fit together
  on a normal-size bench and do not collide at rest.
- **Reachability with margin.** Every station's working point sits
  inside the arm's reachable workspace (the set of poses the arm can
  physically achieve), with room to spare for approach and retreat.
  With ~600 mm of reach this is expected to pass easily — the
  interesting question becomes *good* poses (well-conditioned arm
  configurations), not merely *any* pose.
- **The end-to-end loop is expressible.** The full per-vial sequence
  can be scripted and stepped through as motion-planning goals.
- **Layout freedom.** Because reach is generous, sim is where we pick
  a *convenient* station arrangement (ergonomic spacing, room for
  cabling and fixtures) rather than fighting a reach limit. Contrast
  the myCobot 280 (~280 mm), where the same nine stations must huddle
  tightly or lean on a rail/turntable just to be touchable.
- **Cycle-time first estimate.** Once motions plan, summing planned
  trajectory durations gives an early throughput figure (hedge it —
  sim timing ignores real settling and station dwell).

What sim **cannot** prove here: that the real bench is rigid enough,
that the PiPER's real repeatability lands the gripper on a 2 mL vial,
or that station fixtures align in millimetres on the physical bench.
Those are hardware-acceptance items (see
`10-hardware-platform-and-capital-model.md`). Sim proves the plan is
*geometrically and logically sound*, not that the metal behaves.

## Open-source tools

| Tool | Role | Bottom line |
|------|------|-------------|
| Gazebo Harmonic (gz-sim) | Physics + 3D world holding bench and stations | Primary simulator; fully open, good ROS 2 bridge. |
| `piper_ros` | AgileX ROS/ROS 2 packages with the PiPER URDF | Ships robot description; we adapt its assets, not author from scratch. |
| PiPER URDF | Robot description (links, joints, meshes) | Single source of arm geometry; comes from `piper_ros`. |
| MoveIt 2 config | Planning groups + IK for the PiPER | Generate from the URDF if the vendor config is not ready. |
| `gz_ros2_control` | Drives the URDF's joints inside Gazebo | Lets ROS 2 controllers command the simulated arm. |
| ROS 2 (Humble/Jazzy) | Middleware tying nodes together | Standard; everything speaks ROS 2 topics/actions. |
| RViz2 / Foxglove | Visualisation + interactive goal poses | See the cell, drag goals, confirm reach by eye. |
| Pinocchio / MeshCat | Fast kinematics + lightweight viewer | Scriptable reachability sweeps outside Gazebo. |

Note: `piper_sdk` is AgileX's low-level CAN-bus SDK for the **real**
arm. We do **not** use it in sim — in simulation we drive the URDF
through `gz_ros2_control` and MoveIt 2 so the same higher-level code
targets sim now and hardware later. (The PiPER is also Hugging Face
**LeRobot**-compatible, which matters only if we add learned policies
in a much later milestone — out of scope for v1.)

## How to simulate it now

`piper_ros` (GitHub `agilexrobotics`) ships the PiPER URDF and ROS 2
packages. If a ready-made MoveIt config is not yet included, we
generate one from the URDF with the MoveIt Setup Assistant — a one-time
step that defines the arm's planning group, joint limits, and IK
solver.

**1. Bring up the arm from `piper_ros`.** Clone the package into a
ROS 2 workspace. Confirm the URDF loads, then either launch the
vendor MoveIt config or generate one with the Setup Assistant. Verify
the simulated arm exposes `/joint_states` and answers a
`FollowJointTrajectory` action through a `joint_trajectory_controller`,
and that `move_group` plans against it. This is sim/hardware parity:
the same action interface the real driver would later present.

**2. Build the world SDF (the cell).** Author a Gazebo `world.sdf`
describing the static cell:

- a **bench** model (a box) at the world origin;
- the PiPER **base mount** frame on the bench top;
- one static model per station, each at a fixed, named transform
  (**tf frame** — a named coordinate frame ROS 2 tracks):
  - `vial_supply` — a nested rack of empty/incoming 2 mL vials;
  - `decap_station` — the decapping/capping fixture (Part 03);
  - `dispense_station` — the diluent/standard dispenser (Part 04);
  - `balance_station` — the optional weighing fixture (Part 04);
  - `scan_station` — the barcode/label reader pose (Part 06);
  - `autosampler_tray` — the destination tray (Part 05).

  Publish these as static transforms with a
  `static_transform_publisher` per frame, or bake them into a single
  bench Xacro so every node shares one map of where things are. With
  ~600 mm of reach we can space these out comfortably around the arm
  rather than crowding them.

**3. Spawn the arm into the cell.** Ensure the URDF carries a
`<ros2_control>` block referencing the `gz_ros2_control` plugin, then
spawn it with `ros_gz_sim create -topic robot_description`. Bring up a
`joint_state_broadcaster` and the `joint_trajectory_controller`.

**4. Reachability check.** Confirm the comfortable layout closes:

- In RViz2, set the planning frame to the bench base, then send a
  goal pose at each station's tf frame (plus a short approach offset
  along the tool axis). A successful plan = reachable.
- Automate it: a small node loops over the station frames, calls
  MoveIt's `plan`, and records success/failure plus the IK
  (inverse-kinematics — solving joint angles for a desired hand pose)
  solution. A Pinocchio script can sweep a grid of approach poses per
  station for a fuller reachability map and a *manipulability* score
  (how well-conditioned, i.e. far from awkward singular poses, each
  reach is).
- Because reach is generous, the likely finding is not "does it
  reach?" but "which arrangement gives the cleanest, most repeatable
  arm poses?" Iterating layout in the SDF is free; iterating on a real
  bench is not — which is the entire point of proving it in the twin
  first.

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

Beyond the PiPER and its gripper, the real cell needs a rigid
**bench**, **fixtures/jigs** that hold each station in a repeatable
spot, and the **autosampler** itself (the instrument front-end that
draws from the tray). In this part *none of these are bought* — each
is a **static model** in the Gazebo world:

- bench, jigs, racks → simple box/mesh models at fixed tf frames;
- autosampler tray → a model with addressable slot frames;
- stations → static models now, upgraded to **mock-station service
  nodes** (ROS 2 nodes that fake a station's behaviour at its tf
  frame) in their respective parts.

Notably, the PiPER's reach means we do **not** expect to need a rail
or turntable to extend the workspace, simplifying the bill of
materials versus a smaller arm. The fidelity claim is deliberately
modest: geometry and placement are real enough to test reach and
motion; physical rigidity, vibration, and mounting tolerance are
deferred to hardware bring-up.

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
- `10-hardware-platform-and-capital-model.md` — carries the reach,
  payload, and cost figures into the buy case.
- High-level companion: `../03-high-level-solution/01-scope-and-workflow.md`.
- Folder overview: `README.md`.
