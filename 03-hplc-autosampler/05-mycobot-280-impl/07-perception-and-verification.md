# Part 07 — Perception & verification (myCobot 280 simulation)

> **Sim goal:** Give the simulated cell *eyes* — drop simulated
> cameras into the Gazebo Harmonic world, publish the same ROS 2
> image, depth, and point-cloud topics a real camera would, and run
> the *exact* perception pipeline (AprilTags, OpenCV, Open3D/PCL) that
> would run on hardware. Then wire that pipeline into **verification
> gates** the Behavior Tree must pass before each step, and validate
> every detection against Gazebo's known ground truth.

Parts 02–05 each move something; this part proves we can *see whether
the move worked* before the workflow is allowed to continue. The whole
value of doing it in sim is that the simulator already knows the true
answer (where every object actually is), so we can grade our perception
code against that truth — something we can never do on a real bench.

Two camera types are referenced throughout, defined once here:

- **RGB camera** — an ordinary colour camera. Flat picture of
  red/green/blue pixels. Good for barcodes, reading a printed fiducial,
  spotting a colour change (foam, a spill), and 2-D position. It does
  **not** directly know distance.
- **RGB-D camera** ("D" for depth) — colour plus a depth sensor, so
  every pixel also carries a distance. Gives 3-D shape: liquid-column
  height, whether a tray slot is empty, how far a vial rim is. This is
  the workhorse when "is it there, and how full / how seated" matters.

An **AprilTag** is a small high-contrast black-and-white square sticker
(a *fiducial* — a printed pattern made to be found and measured by a
camera). Each tag has a unique ID and, once detected, yields an exact
position and orientation (a **pose**). Tags on the rack, tray, and
stations give the arm a precise, self-checking reference frame.

> **The cameras are three of twelve sensors.** This part covers the
> three cameras in detail — wrist RGB (#3), tray top-down RGB-D (#1),
> and dispense side-on RGB/RGB-D (#2) — but they are part of one
> **unified sensor suite** defined in [`sensor-suite.md`](sensor-suite.md).
> The verification gates here do not rely on cameras alone: every
> camera check has **non-camera co-witnesses** the gates fuse with it
> (the *two-witness* habit). "Vial held" = wrist glance (#3) **and**
> gripper servo feedback (#4, jaw width + motor current); "cap off /
> seated" = station cam (#2) **and** decapper load-cell torque (#5);
> "right fill" = level / meniscus (#2/#8) **and** the analytical
> balance (#6, gravimetric); "vial staged / seated in slot" = camera
> **and** station presence/proximity (#7); and the base IMU (#12)
> watches that the bench stays level under all of it. So a gate that
> returns PASS is typically agreeing across an *image* and a *physical*
> measurement, not trusting either alone.

## What we can prove in simulation

Entirely before buying a single camera, the sim lets us prove:

- **The perception *pipeline* runs end to end.** Camera sensor →
  ROS 2 topic → apriltag_ros / OpenCV / Open3D node → PASS/FAIL gate
  result. Every link in that chain is real ROS 2 code; only the photons
  are synthetic.
- **Verification gates gate the workflow.** A gate that returns FAIL
  actually stops the per-vial loop in Part 08, rather than the loop
  charging ahead. This is the discipline we most need to rehearse.
- **Detection is correct, graded against truth.** Gazebo publishes the
  *true* pose of every model. We compare our AprilTag/OpenCV pose
  estimate to that ground truth and measure the error — a free, exact
  accuracy check no real lab gets.
- **Camera placement trade-offs.** The 280 is a *small* arm (~280 mm
  reach, `~` verify); a heavy wrist camera eats payload and can foul on
  its own short links. Sim lets us test how much work a fixed
  overhead/station camera can carry instead, and where to mount each.
- **Two-witness logic.** When a wrist view and a fixed view disagree,
  the gate returns UNSURE. We can rehearse that branch by placing the
  two simulated cameras at deliberately different angles.

Honest limits — what sim **cannot** prove here:

- **Real optics.** Glass-on-glass reflections, meniscus glare, clear
  liquid that is nearly invisible, label glare, motion blur, depth-sensor
  noise on shiny/transparent surfaces — Gazebo's synthetic images are
  too clean. Liquid level on a transparent vial is *especially*
  optimistic in sim.
- **Lighting.** Real benches have changing, uneven light; sim lighting
  is uniform unless we work hard to make it ugly.
- **True calibration.** Camera intrinsics and the hand-eye transform
  (where the wrist camera sits relative to the gripper) are exact in
  sim and only approximate after a real calibration.

So sim proves the *logic and the pipeline*; it does not prove the
sensor will survive contact with real glass and real light. Those are
hardware-acceptance items (see
`10-hardware-platform-and-capital-model.md`).

## Open-source tools

| Tool | Role | Bottom line |
|------|------|-------------|
| Gazebo Harmonic camera/depth sensor plugins | Render synthetic RGB, depth, and point-cloud streams | Built-in `camera` / `depth_camera` sensors; no extra cost. |
| `ros_gz_bridge` / `ros_gz_image` | Bridge Gazebo sensor data onto ROS 2 image/depth/points topics | Makes sim cameras look exactly like real ROS 2 cameras. |
| apriltag_ros | Detect AprilTag fiducials → pose + ID | Mature, fast; the backbone of known-pose alignment. |
| OpenCV | 2-D vision: rim/circle find, edges, colour anomaly | Same library used on hardware; runs unchanged on sim images. |
| Open3D / PCL | Point-cloud work: seating, level, slot occupancy | Depth-based geometric checks (level/seated) from RGB-D. |
| ZBar / pyzbar | Decode barcodes/QR off RGB frames | Hands off to identification (Part 06). |
| RViz2 / Foxglove | Visualise images, depth, clouds, tf frames | Eyeball the pipeline; confirm a tag's pose lands on the model. |
| Gazebo ground-truth pose topic | True model poses for grading detections | The sim-only "answer key" we validate detections against. |

## How to simulate it now

This part assumes the world, arm, and station frames from
`01-scope-and-workflow.md` are already running.

**1. Add camera sensors to the world SDF.** In the Gazebo `world.sdf`
(or the station/robot models), attach `<sensor type="camera">` and
`<sensor type="depth_camera">` (or an RGB-D combined sensor) where they
are needed:

- a **wrist RGB-D camera** as a small fixed joint near the gripper on
  the 280's last link — kept light, and used for close, on-demand,
  correctly-aligned views;
- one or more **fixed station cameras**, e.g. a top-down RGB-D over the
  `autosampler_tray` (slot occupancy, seating across the whole rack at
  once) and a side-on RGB-D at the `dispense_station` (liquid level).

Because the 280 is small, lean on the **fixed** cameras for the
whole-scene work and use the wrist camera only where a close aligned
view genuinely helps.

**2. Publish to ROS 2.** Bridge each sensor with `ros_gz_bridge` /
`ros_gz_image` so it appears on standard topics, e.g.:

```
/wrist_cam/image_raw        (RGB)
/wrist_cam/depth/image      (depth)
/wrist_cam/points           (point cloud)
/tray_cam/image_raw
/tray_cam/points
/dispense_cam/image_raw
/dispense_cam/depth/image
```

Each camera has its own **tf frame** (a named coordinate frame ROS 2
tracks) so detections can be transformed into the bench/base frame
shared by every node.

**3. Run apriltag_ros.** Feed it `/wrist_cam/image_raw` (and the
fixed-camera streams) plus the camera info. Place AprilTag models on the
`vial_supply` rack, the `autosampler_tray`, and each station model in
the SDF. apriltag_ros publishes each tag's pose; a small node transforms
those into the base frame and offers them as the **known-pose
alignment** other parts consume.

**4. Run a detection / level node.** One ROS 2 node subscribes to the
relevant streams and exposes the geometric checks:

- **rim / presence** (OpenCV circle/edge on the wrist RGB-D) — is a vial
  in the cell, is it in the gripper;
- **cap profile** (OpenCV + depth) — is a cap on / seated / square;
- **liquid level** (Open3D/PCL on the dispense side view) — height of
  the liquid column, *approximate* fill only (the dispenser's
  fill-volume scalar in Part 04 is the real number; the camera is the
  independent sanity check);
- **slot occupancy & seated** (Open3D/PCL on the tray top-down) —
  empty-vs-filled per cell, and vial fully down.

**5. Wire verification gates as services the BT calls.** Expose each
gate as a ROS 2 service (or action) that returns PASS / FAIL / UNSURE
plus the measurement and a timestamp, so the Behavior Tree in
`08-orchestration-error-handling-and-safety.md` ticks it as a node:

```
pick vial ──▶ [GATE: in gripper?] ──▶ decap ──▶ [GATE: open rim?]
   ──▶ dispense ──▶ [GATE: right level? no spill?] ──▶ cap
   ──▶ [GATE: cap seated?] ──▶ read barcode ──▶ [GATE: matches worklist?]
   ──▶ place in slot ──▶ [GATE: seated in correct slot?] ──▶ next vial
```

**6. Validate against ground truth (the sim-only superpower).** Subscribe
to Gazebo's true model-pose topic and, for each detection, log the error
between estimate and truth. This both *proves the pipeline is wired
correctly* and *calibrates how much to trust each gate* — and it lets us
deliberately move a model (e.g. shift a vial 5 mm) and confirm the gate
catches it. Every gate result is logged for the audit trail in
`09-software-compliance-and-integration.md`.

## Additional hardware needed

Beyond the arm and gripper, the real cell needs **RGB-D cameras** (a
wrist unit plus one or more fixed station cameras), their mounts, and
**controlled lighting** (often a simple LED panel and a matte, low-glare
backdrop to fight glass reflections). In this part *none of that is
bought*:

- cameras → Gazebo `camera` / `depth_camera` sensor plugins publishing
  to ROS 2 image/depth/point-cloud topics;
- lighting → Gazebo scene lights (clean and even — which is exactly why
  glare and reflection cannot be proven here);
- camera mounts → fixed joints (wrist) and static models (station cams)
  in the SDF.

The honest gap: synthetic images skip the hardest real problems —
transparent glass, clear liquid, label and meniscus glare, sensor noise,
and changing light. Those are validated only on hardware bring-up.

## How it connects

- **`02-vial-handling-and-gripping.md`** — perception locates the vial
  to pick and confirms it is in the gripper after the grasp-fix grip.
- **`03-decapping-and-capping.md`** — gates confirm the cap link is
  actually off before fill, and seated after re-cap.
- **`04-liquid-handling-and-sample-prep.md`** — the approximate level /
  spill check independently confirms the dispenser's fill-volume change
  visibly happened.
- **`05-tray-loading-and-positioning.md`** — slot-occupancy and seated
  checks confirm the right slot is empty and the vial is fully down.
- **`08-orchestration-error-handling-and-safety.md`** — a failed gate is
  the trigger the Behavior Tree branches on (retry / quarantine / stop).
- **[`sensor-suite.md`](sensor-suite.md)** — the canonical list of all
  twelve sensors; the three cameras here are entries #1–#3, and the
  co-witnesses the gates fuse with them (#4–#8, #12) are defined there.
- Folder overview: [`README.md`](README.md).
