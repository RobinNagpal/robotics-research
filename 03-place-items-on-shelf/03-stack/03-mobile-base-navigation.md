# Stack layer: Mobile-base navigation

> **Job:** map the aisle, localize the base in it, and drive to a stable
> picking/placing pose in front of the target shelf — then hold that
> pose for manipulation. In v1 the goal is a fixed pose and any dynamic
> obstacle triggers a **safe-stop** (not a clever re-route), so the bar
> is "reliable point-to-point navigation with good localization," not
> "crowd-navigating AV."

## How this layer fits into the architecture

Navigation is the robot's **legs and sense of place**. Its single job in
the architecture is to get the whole robot body to a precise standing
spot in front of the correct shelf, and hold it steady there, so the arm
can reach the slot.

Where it sits in the flow: the orchestration layer (the "supervisor,"
see `07-orchestration.md`) hands navigation a goal — "go to the picking
pose in front of shelf #4." Navigation then takes over the **mobile
base**. It reads the lidar and wheel odometry, compares them against the
stored map of the aisle to work out where it currently is
(localization), plans a path, and drives the wheels there, stopping at
the goal. A short vision-based nudge lines it up exactly with the shelf
face. Only once navigation reports "arrived" does the supervisor move on
to picking.

It deliberately owns *only base movement*. It never touches the arm, the
product camera, or the grasp — those are other layers. If a person steps
into the aisle, navigation is the layer that notices (through its
costmap) and triggers the **safe-stop** the requirements call for.
Everything it does flows over ROS 2 (`02-middleware.md`), and during
development the "world" it drives through is the simulator
(`01-simulator.md`).

## Navigation stacks

| Framework | ROS 2 native | Completeness (plan + control + recovery) | SLAM / localization included | Dynamic-obstacle handling | Maturity / community | Customizability | Bottom line |
|-----------|--------------|------------------------------------------|------------------------------|---------------------------|----------------------|-----------------|-------------|
| **Nav2** | Yes | Full: planners, controllers, BT navigator, recoveries | Pairs with slam_toolbox / AMCL | Costmap + configurable behaviors | High, very active | High (Behavior-Tree driven, pluginable) | The complete, modular ROS 2 answer — built for exactly this |
| **move_base** (ROS 1) | No | Full but monolithic | gmapping / AMCL | Costmap recovery | Mature but **EOL** | Lower (plugin but ROS 1) | Legacy predecessor to Nav2 — don't start here |
| **Autoware.Universe** | Yes | Full, AV-grade (lanes, prediction) | LiDAR SLAM + NDT | Strong (built for traffic) | High but AV-focused | High but heavyweight | Massive overkill for an indoor AMR; huge integration cost |
| **Isaac ROS (nvblox + nav)** | Yes (GPU) | Adds GPU 3D mapping into Nav2 | nvblox 3D reconstruction | 3D-aware costmaps | Growing | Moderate | A GPU accelerator *for* Nav2, not a replacement — add later if needed |
| **Vendor AMR SDK** | Varies | Turnkey for that base | Proprietary | Vendor-defined | Varies, closed | Low (black box) | Fast if you buy that base; locks you in, weak for sim-first dev |

### SLAM / localization backend (used with Nav2)

| Backend | Map type | Loop closure | Lifelong / re-localization | ROS 2 support | Bottom line |
|---------|----------|--------------|----------------------------|---------------|-------------|
| **slam_toolbox** | 2D occupancy | Yes | Yes (serialize + continue) | First-class | Best default for a 2D indoor aisle |
| **Cartographer** | 2D/3D | Yes | Limited | Maintained | Accurate but heavier to tune |
| **RTAB-Map** | 3D RGB-D/lidar | Yes | Yes | Good | Use if you want a 3D map of the store |
| **AMCL** | Localization only | N/A | Needs a prior map | Built into Nav2 | Pair with a pre-built map for production runs |

## Top choice

**Nav2 + slam_toolbox** (with **AMCL** on a saved map for production).

Nav2 is the only stack that is ROS 2 native, feature-complete
(global/local planning, control, recoveries), and customizable through
the same Behavior-Tree philosophy used at the orchestration layer.
`slam_toolbox` builds and maintains the 2D map of the aisle cleanly; once
the map is stable, switch to AMCL localization against it for repeatable
runs. Reserve **Isaac ROS / nvblox** as a GPU upgrade for 3D-aware
costmaps if the flat-floor 2D assumption later breaks. Avoid Autoware
(AV-scale overkill) and vendor SDKs (lock-in, poor sim-first fit).
