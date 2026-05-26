# Phase 4 — Manipulation (pick, grasp, place)

> **Goal:** with the base parked at the shelf, plan a collision-free arm
> trajectory to pick a can from the known tray pose, hold it through a
> reliable simulated grasp, and set it down on the shelf slot with a
> light, guarded contact. Knocking a neighbor or clipping the shelf is a
> defined failure (`../01-requirements.md` §6–7,
> `../03-stack/04-arm-motion-planning.md`).
>
> **Checkpoint:** the arm picks a can from the tray and places it upright
> on the shelf, collision-free, repeatably.

---

## 4.1 MoveIt 2 configuration

Generate `shelf_moveit_config/` with the **MoveIt Setup Assistant** from
`robot.urdf.xacro`:

- Define **planning groups:** `arm` (the 6 joints) and `gripper`.
- Auto-generate the **self-collision** matrix.
- Set the **end-effector** (gripper) and a few named poses (`home`,
  `pre-pick`, `pre-place`).
- Use the **`joint_trajectory_controller`** from Phase 2 as the MoveIt
  controller (the `moveit_controllers.yaml` must match the spawned
  controller names).
- Default planner: **OMPL** (RRTConnect) is plenty for v1; cuRobo is the
  later GPU upgrade (`../03-stack/04-arm-motion-planning.md`), not now.

## 4.2 The collision world

MoveIt must plan *around* the shelf and already-placed cans:

- Add the **shelf** as a static collision object (from its known pose /
  mesh).
- Add **each placed can** as a collision object after a successful place
  (the orchestrator updates the planning scene in Phase 5).
- This is what stops the arm clipping the shelf board or a neighbor.

## 4.3 The pick

A known-pose pick (no perception yet — that is Phase 5's geometric pose):

1. Read the **next tray cell** pose (known layout) → the grasp pose comes
   from the SKU's preferred grasp (side pinch for a can).
2. Plan to a **pre-pick** pose above/beside the cell.
3. Cartesian **approach** to the grasp pose.
4. **Close the gripper** and attach (see §4.5).
5. Cartesian **retreat** lifting the can clear of the tray.

## 4.4 The place (guarded set-down)

The place is a controlled set-down, **not a free-space drop**
(`../03-stack/04-arm-motion-planning.md`):

1. Plan to a **pre-place** pose above the target slot (slot origin +
   offset by how many already placed — from the planogram, Phase 5).
2. Cartesian **descend** until light contact with the shelf board (cap
   downward force / stop on a small contact, so it is "guarded").
3. **Open the gripper** and detach.
4. Cartesian **retreat** clear of the placed can.
5. Add the placed can to the collision scene.

## 4.5 Grasping in Gazebo — the DetachableJoint trick

**This is the part that bites people.** Pure friction grasping of a
rigid body in Gazebo is unreliable — the can slips or jitters. The
pragmatic, widely-used approach:

- Use the **`DetachableJoint`** system: when the gripper closes *and* a
  **contact sensor** on the gripper pads reports contact with the SKU,
  create a fixed joint between the gripper link and the can. On gripper
  open, **detach** it.
- This gives a rock-solid "grasp" without fighting friction, and it maps
  cleanly to a real gripper's open/close + a grasp-success check.
- Expose it behind a small **`shelf_grasp`** node so the rest of the
  stack just sees "grasp succeeded / released" — the analytical grasp
  decision (`../03-stack/06-grasping.md`) and the sim attach mechanism
  stay separate, so the learned grasp model can drop in later untouched.

> Alternative: a suction model via a fixed joint on a single contact
> point (good for flat-topped boxes / `Dex-Net`-style suction). For a can
> SKU, the pinch + DetachableJoint is simplest.

## 4.6 Grasp confirmation

Confirm the grasp the way hardware would: gripper joint state (did it
close to the expected width?) plus the DetachableJoint attach event, and
optionally a weight/contact check. A failed grasp is **logged and
skipped**, not retried forever (`../01-requirements.md` §7).

## 4.7 Expose pick & place as actions

Wrap the two motions as **`PickProduct`** and **`PlaceProduct`** ROS 2
actions for the Behavior Tree (Phase 5), each returning success/failure
and a reason.

## Deliverables

- `shelf_moveit_config/` planning for `arm` + `gripper`, controllers
  matched.
- Collision-world updates for shelf + placed cans.
- A reliable sim grasp via DetachableJoint behind `shelf_grasp`.
- `PickProduct` / `PlaceProduct` actions.

## Checkpoint

The arm repeatedly picks a can from the tray and places it upright on the
shelf with a guarded set-down, no collisions. Manipulation proven — move
to Phase 5 (the full loop).
