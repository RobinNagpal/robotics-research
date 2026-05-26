# Phase 3 — Navigation (map, localize, drive to the shelf)

> **Goal:** the robot autonomously drives from a start pose to a stable
> picking/placing pose in front of the target shelf, then holds it. In
> v1 the goal is a **fixed picking pose** and any dynamic obstacle
> triggers a **safe-stop**, not a re-route (`../01-requirements.md` §6–7,
> `../03-stack/03-mobile-base-navigation.md`).
>
> **Checkpoint:** send one goal pose; the robot plans and drives to the
> shelf stand-off pose and stops cleanly.

---

## 3.1 Build the map (SLAM)

Use **`slam_toolbox`** in async mode against the bridged `/scan` + tf:

1. Launch the world + robot, drive the base around the aisle with teleop.
2. Run `slam_toolbox` to build a 2D occupancy grid of the aisle.
3. Save it (`slam_toolbox` serialize, or `nav2_map_server` `map_saver`)
   to `shelf_navigation/maps/aisle.yaml` + `.pgm`.

The aisle is small and flat, so a single slow pass gives a clean map.

## 3.2 Localize on the saved map (production runs)

Once the map is stable, switch from live SLAM to **AMCL** (in
`nav2_bringup`) localizing against `aisle.yaml`. This is the repeatable
configuration the success-rate runs use — SLAM is for map-building,
AMCL for the actual stocking runs.

## 3.3 Nav2 bring-up

`shelf_navigation/launch/nav2.launch.py` starting `nav2_bringup` with
`shelf_navigation/config/nav2_params.yaml`. Key params for this robot:

- **Robot footprint / radius** matching the base.
- **Costmaps:** static layer (the map) + obstacle layer (live `/scan`) +
  inflation. The obstacle layer is what makes a shopper show up.
- **Planner / controller:** the Nav2 defaults (NavFn/Smac + DWB/MPPI) are
  fine for point-to-point in a small aisle.
- **`use_sim_time: true`** everywhere.

## 3.4 The picking pose

- The job (Phase 5) names a target shelf; the picking pose is a **fixed
  stand-off pose** in front of that shelf, stored with the shelf in the
  map / a small config.
- Send it as a Nav2 `NavigateToPose` goal. When Nav2 reports success the
  base is roughly in place.
- **Precise alignment:** a fixed stand-off is not accurate enough for
  manipulation, so add a short **vision-based nudge** — read the shelf
  face from the wrist RGB-D (a planar fit, Phase 5), compute the small
  base/arm offset, and refine. In Phase 3 you can stub this as "good
  enough" and tighten it in Phase 5.

## 3.5 Safe-stop, not re-route

v1 never plans *through* a dynamic obstacle. Wire the costmap so that an
unexpected obstacle in the path causes Nav2 to **stop** (and the
orchestrator, Phase 5, to hold), rather than enabling clever recovery
re-routing. Keep recoveries minimal — spin/back-up off, stop on.

## 3.6 Expose navigation as an action

Wrap "drive to the picking pose for shelf X" as the **`NavigateToShelf`**
ROS 2 action the Behavior Tree calls in Phase 5 (thin wrapper over Nav2's
`NavigateToPose`). This keeps the orchestrator clean.

## Deliverables

- `aisle.yaml` map of the store.
- `nav2_params.yaml` tuned for the base + a working `nav2.launch.py`.
- AMCL localization on the saved map.
- A `NavigateToShelf` action (or a documented stub) returning success at
  the picking pose.

## Checkpoint

From a random start pose, one goal sends the robot to a stable stand-off
pose in front of the shelf, and an obstacle in the path makes it
safe-stop. Navigation proven — move to Phase 4 (the arm).
