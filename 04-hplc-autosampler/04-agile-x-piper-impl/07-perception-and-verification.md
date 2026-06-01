# Part 07 — Perception & verification (AgileX PiPER simulation)

> **Sim goal:** Add simulated cameras to the Gazebo Harmonic cell — a
> wrist RGB-D camera on the PiPER plus a few fixed station cameras —
> and run the *same* perception pipeline you would run on hardware
> (AprilTags, OpenCV, point-cloud checks). Then wire each check up as a
> **verification gate** the Behavior Tree must pass before the next
> step, and confirm every detection against Gazebo's ground-truth.

This part gives the simulated cell *eyes*. It assumes the world, arm,
and station frames from `01-scope-and-workflow.md` already run, and the
station behaviours from Parts 02–05 are in place to be verified. The
big idea, carried straight from the high-level companion
`../01-high-level-solution/07-perception-and-verification.md`, is that
perception's main job in this system is not clever search — the world
is mostly where it was taught — but **cheap, reliable confirmation**
plus the discipline to stop when confirmation fails.

Two camera types matter here:

- **RGB camera** — an ordinary colour camera. A flat picture
  (red/green/blue pixels). Good for barcodes, reading a printed marker,
  spotting a colour change (foam, a spill), and 2-D position. It does
  not by itself know how far away anything is.
- **RGB-D camera** ("D" = depth) — a colour camera plus a depth sensor,
  so every pixel also carries a distance. This gives 3-D shape: how
  tall a liquid column is, whether a tray slot is empty, how far a vial
  rim is from the gripper.

An **AprilTag** is a fiducial — a small high-contrast black-and-white
square sticker designed to be found fast by a camera and turned into an
exact position and orientation (a **pose**) plus a unique ID number.
Sticking AprilTags on the rack, tray, and stations gives the arm a
precise, self-checking reference frame almost for free.

## What we can prove in simulation

Entirely before buying any camera, the sim lets us prove:

- **The perception *pipeline* runs end to end.** Camera sensors publish
  ROS 2 image/depth/point-cloud topics; `apriltag_ros`, an OpenCV
  detection node, and an Open3D/PCL level-and-seating node consume them
  and emit detections — exactly the graph that will run on hardware.
- **Verification gates work.** Each check is a ROS 2 service the
  Behavior Tree calls; we prove PASS lets the loop proceed and FAIL/
  UNSURE halts it (the gate logic of
  `08-orchestration-error-handling-and-safety.md`).
- **The detections are *correct*.** Because Gazebo knows the true pose
  and state of every object, we cross-check each detection against
  **ground truth** (the simulator's known answer) — e.g. AprilTag pose
  vs the model's real pose, "decapped" vs the cap-link state. This
  validates the *algorithm and the wiring*, which is the honest thing
  sim can validate.
- **Two-viewpoint cross-checking.** Wrist camera and a fixed camera can
  each witness the same event (vial in gripper, slot occupancy) so one
  confirms the other.

Honest limits — what sim **cannot** prove:

- **Real sensor noise.** Gazebo depth is far cleaner than a real RGB-D
  sensor; speckle, fly-through pixels, and range dropouts are absent or
  faked.
- **Glass and liquid optics.** Reflections, refraction through a clear
  2 mL vial, and a hard-to-see meniscus are exactly where real
  perception struggles and where the sim model is weakest.
- **Lighting.** Glare, shadows, and changing room light — the usual
  cause of a barcode or AprilTag that *won't* read — are not faithfully
  modelled. Robustness to lighting is a hardware-bring-up item (see
  `10-hardware-platform-and-capital-model.md`).

So: sim proves the **pipeline, the gate logic, and the sequencing are
sound**; it does not prove the camera can see through glass on a real
bench.

## Open-source tools

| Tool | Role | Bottom line |
|------|------|-------------|
| Gazebo Harmonic camera sensor | Simulated RGB camera publishing an image stream | Built-in `<sensor type="camera">`; bridges to ROS 2. |
| Gazebo Harmonic depth/RGB-D sensor | Simulated depth + colour → point cloud | `<sensor type="depth_camera"/"rgbd_camera">`; the wrist/fixed RGB-D. |
| `ros_gz_bridge` / `ros_gz_image` | Bridge Gazebo sensor topics to ROS 2 | Turns sim sensors into normal ROS 2 image/depth topics. |
| `apriltag_ros` | Detect AprilTags → pose + ID | Same package used on hardware; known-pose alignment. |
| OpenCV (`cv_bridge`) | 2-D detection: rim find, barcode region, spill colour | The general-purpose vision toolbox; runs on the RGB stream. |
| Open3D / PCL | Point-cloud level + seating checks | Liquid-column height, empty-vs-filled slot by depth. |
| `image_pipeline` | Camera info, rectification | Keeps sim camera intrinsics consistent with the pipeline. |
| RViz2 / Foxglove | View images, clouds, tag frames | Confirm detections and gate results by eye. |

## How to simulate it now

Assumes the cell from `01-scope-and-workflow.md` is running.

**1. Add camera sensors to the SDF/URDF.** Two vantage points, matching
the high-level design:

- **Wrist RGB-D.** Add a `<sensor type="rgbd_camera">` to a small
  `wrist_cam_link` fixed near the PiPER tool flange in the URDF, on its
  own tf frame `wrist_cam_optical`. It moves with the arm, so it can
  look straight down a vial, read a held barcode, or inspect a slot
  from directly above.
- **Fixed station cameras.** Place static models carrying camera or
  depth sensors at named frames — e.g. `dispense_cam` (side-on RGB-D of
  the dispense station for liquid level) and `tray_cam` (top-down RGB-D
  of the `autosampler_tray` for whole-tray slot occupancy).

Give every sensor a `<gz_frame_id>` so its data carries the right tf
frame.

**2. Publish to ROS 2.** Run `ros_gz_bridge` (or include the bridge in
the launch file) to expose each sensor as standard ROS 2 topics:
`.../image_raw`, `.../depth/image`, `.../points` (a `PointCloud2`), and
`.../camera_info`. From here, no node can tell sim from hardware — the
topic types are identical.

**3. Stick AprilTags in the world.** Apply tag textures to small plates
on the supply rack, tray corners, decap and dispense stations. Run
`apriltag_ros` against the wrist and fixed RGB streams; it publishes
each tag's pose and ID. Use these to refine the taught station frames
(drift correction) and to read which fixture is which.

**4. Run the detection / level node.** A small ROS 2 node subscribes to
the bridged topics and provides, per the table in the high-level doc:

- **rim find** (OpenCV circle/edge) on the wrist RGB-D to confirm a
  vial is present and centred before a grip;
- **presence check** (wrist + fixed) to confirm the vial is in the
  gripper after a pick;
- **cap profile** (depth/edge) to tell capped from open before fill and
  to confirm a re-cap is seated;
- **liquid level** (Open3D/PCL meniscus height on the `dispense_cam`
  cloud) — an *approximate* fill check, not metrology; accurate volume
  is the dispenser's job in
  `04-liquid-handling-and-sample-prep.md`;
- **spill / foam** (RGB colour/texture anomaly) — flag, don't proceed;
- **slot occupancy + seated** (top-down depth per cell on `tray_cam`).

**5. Wire verification gates as services.** Expose each check as a ROS 2
service returning `PASS / FAIL / UNSURE` plus the supporting image or
measurement. The Behavior Tree in
`08-orchestration-error-handling-and-safety.md` calls these between
steps:

```
pick vial ──▶ [GATE: in gripper?] ──▶ decap ──▶ [GATE: open rim?]
  ──▶ dispense ──▶ [GATE: right level? no spill?] ──▶ cap
  ──▶ [GATE: cap seated?] ──▶ read barcode ──▶ [GATE: matches worklist?]
  ──▶ place in slot ──▶ [GATE: seated in correct slot?] ──▶ next vial
```

**6. Cross-check against ground truth.** For each gate, also query the
Gazebo model's true state (pose, cap-link state, dispenser fill scalar)
and compare it to the perception result. Log mismatches. This is the
sim-only superpower: a fast, objective measure of *whether the
perception was right*, which on hardware you can only approximate. A
gate that disagrees with ground truth is a pipeline bug to fix before
hardware, not after.

## Additional hardware needed

Beyond the PiPER and gripper, the real cell needs **RGB-D cameras** (a
wrist unit and one or more fixed station units) and **controlled
lighting** (steady, glare-free illumination, possibly polarisers or
backlighting to fight glass reflections). In this part none of these is
bought:

- **RGB-D cameras → Gazebo depth-camera / rgbd sensors** publishing the
  same ROS 2 topic types the real driver would.
- **Lighting → not faithfully modelled.** Sim light is too kind; real
  glare, reflections off curved glass, shadow, and sensor noise are the
  hardest part of this layer and must be validated on hardware. Treat
  read-rate and level-accuracy numbers from sim as optimistic.

The fidelity claim is deliberately modest: sim proves the perception
*logic and plumbing*; the *optics* are a hardware-acceptance item
carried into `10-hardware-platform-and-capital-model.md`.

## How it connects

- **`02-vial-handling-and-gripping.md`** — locates the vial to pick and
  confirms it is in the gripper after the grip (presence gate).
- **`03-decapping-and-capping.md`** — gates confirm the vial is open
  before fill and the cap is seated afterwards (reads the cap-link
  state set by the decap station service).
- **`04-liquid-handling-and-sample-prep.md`** — the approximate level /
  spill / foam checks verify the dispense visibly happened; the
  dispenser's fill scalar is the ground-truth cross-check.
- **`05-tray-loading-and-positioning.md`** — slot-occupancy and seated
  checks confirm the right slot is empty and the vial is fully down.
- **`08-orchestration-error-handling-and-safety.md`** — a failed gate is
  the trigger for retry, stop, or quarantine.
- High-level companion:
  `../01-high-level-solution/07-perception-and-verification.md`.
- Back to the index: [`README.md`](README.md).
