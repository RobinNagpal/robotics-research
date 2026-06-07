# Part 07 — Perception & verification (simulation)

> **Sim goal:** Put *simulated* cameras into the Gazebo Harmonic
> world — one on the reBot wrist, a few fixed at the stations — and run
> the **exact same** perception code we would run on hardware, so that
> every workflow step has to pass a vision "did this happen?" check
> before the next one is allowed to start.

This part adds eyes to the digital twin built in
`01-scope-and-workflow.md`. The point is not pretty pictures: it is to
prove that the **perception pipeline** and the **verification gates**
work — that detections line up with the world, and that a missed pick
or a still-capped vial gets *caught* instead of silently passing. In
sim we get a luxury we never have on hardware: Gazebo knows the true
position of everything (the **ground truth**), so we can grade our own
detector against the right answer.

A quick vocabulary note, since the rest of the doc leans on it:

- **RGB camera** — an ordinary colour camera; flat picture, no
  distance. Good for barcodes, fiducials, and 2-D position.
- **RGB-D camera** ("D" = depth) — colour *plus* a per-pixel distance,
  so it sees 3-D shape: liquid-column height, whether a slot is empty,
  how far a rim is. This is what we mostly simulate here.
- **AprilTag** — a printed black-and-white square sticker (a
  *fiducial*, i.e. a marker designed to be measured by a camera). Each
  tag has a unique ID and, once detected, gives an exact position and
  orientation (a **pose**). Stick them on stations and the tray and the
  arm gets a precise, self-checking reference frame nearly for free.
- **Point cloud** — the set of 3-D dots an RGB-D camera produces, one
  per pixel; the raw material for depth checks.

## What we can prove in simulation

Entirely before buying a single camera, in the open-source stack we can
prove:

- **The pipeline runs end to end.** Gazebo publishes image / depth /
  point-cloud topics, `apriltag_ros` finds the tags, and our small
  detection node turns frames into PASS / FAIL answers.
- **Known-pose alignment works.** AprilTags on stations and tray let
  the arm correct its taught coordinates — and we can confirm the
  corrected pose matches Gazebo ground truth to within sim tolerance.
- **Verification gates gate.** A deliberately wrong action (skip the
  decap, leave a slot occupied) is *rejected* by the gate, not waved
  through. This is the regulated-lab requirement: no step proceeds on
  faith.
- **Geometric checks are sound.** Rim-finding, "cap on / cap off,"
  liquid-column height, and "slot empty vs filled" all read correctly
  off simulated depth.
- **Two viewpoints cross-check.** Wrist and fixed cameras can confirm
  the same fact independently, the design we want on hardware.

**Honest limits.** Sim proves *logic and geometry*, not optics. Real
glass vials reflect and refract; real lighting flickers and casts
shadows; real depth sensors are noisy at glass and liquid surfaces.
None of that is faithfully reproduced by a clean Gazebo render, so
detector *thresholds* and *robustness* must be re-tuned on hardware.
What carries over unchanged is the **pipeline structure**, the **topic
and tf wiring**, and the **gate logic**. Treat sim pass-rates as an
upper bound; hedge any number with `~`.

## Open-source tools

| Tool | Role | Bottom line |
|------|------|-------------|
| Gazebo Harmonic sensor plugins | Simulate RGB + depth cameras; publish to ROS 2 | Built-in `gz-sensors` camera/depth-camera/rgbd; the source of all sim imagery. |
| `ros_gz_image` / `ros_gz_bridge` | Bridge Gazebo image & camera-info to ROS 2 topics | Makes the sim camera look exactly like a real ROS 2 camera. |
| `apriltag_ros` | Detect AprilTag fiducials → pose + ID | Same package on sim and hardware; known-pose alignment. |
| OpenCV (`cv_bridge`) | 2-D image ops: rim find, cap profile, spill colour | Classic, well-validated; no training data needed for v1. |
| Open3D / PCL | Process point clouds: liquid level, seating depth | Geometric 3-D checks against depth/point cloud. |
| ZBar / `pyzbar` | Decode barcodes/labels in RGB | Ties to `06-identification-labeling-and-tracking.md`. |
| RViz2 / Foxglove | Visualise images, clouds, tag frames | Confirm detections by eye; debug tf alignment. |
| Custom verification node | Wraps checks as ROS 2 services the BT calls | The gate layer — returns PASS / FAIL / UNSURE. |

## How to simulate it now

The reBot exposes its joints and motion interface as described in
`01-scope-and-workflow.md`; here we bolt cameras onto that world.

**1. Add camera sensors to the SDF.** In the world / robot SDF, attach
`<sensor type="rgbd_camera">` (or separate `camera` + `depth_camera`)
elements:

- **Wrist camera** — a sensor on a small link fixed to the reBot's
  end-effector flange, looking down the tool axis. It moves with the
  arm, so it can look straight down a vial about to be picked, read a
  label held in the gripper, or inspect a slot from above. Give it its
  own tf frame, e.g. `wrist_cam_optical_frame`.
- **Fixed station cameras** — static sensors at known poses:
  `dispense_cam` (side-on RGB-D of the dispense station, for liquid
  level), `tray_cam` (top-down RGB-D over the `autosampler_tray`, for
  slot occupancy), optionally `decap_cam`. Each gets a fixed tf frame
  published as a static transform, consistent with the station frames
  from `01-scope-and-workflow.md`.

Set a sensible resolution (~640×480 is plenty for v1), a realistic FOV,
and the `<topic>` each sensor publishes on.

**2. Publish to ROS 2.** Bridge the Gazebo sensor topics into ROS 2
with `ros_gz_bridge` / `ros_gz_image` so each camera produces the
standard ROS 2 set: `image_raw`, `depth/image_raw`, `points`
(point cloud), and `camera_info` (the intrinsics every downstream node
needs). After this step nothing downstream knows or cares that the
camera is simulated.

**3. Run `apriltag_ros`.** Place AprilTag models (textured squares) on
the stations and on the tray corners in the SDF. Launch `apriltag_ros`
against the wrist and tray camera streams; it publishes detected tag
poses on tf. A small alignment node compares the detected station frame
to the taught frame and applies the small correction — exactly the
drift-correction we want on hardware.

**4. Run the detection / level node.** A single Python (or C++) node
subscribes to the camera topics and implements the v1 geometric checks:

- **Vial present / rim centre** — OpenCV circle/edge find on the wrist
  RGB-D image.
- **Cap on vs off** — depth/profile check at the vial mouth.
- **Liquid level** — Open3D/PCL on the `dispense_cam` point cloud:
  height of the meniscus (liquid surface) above the vial base. This is
  *approximate* — a sanity check, not metrology; true volume is the
  dispenser's job in `04-liquid-handling-and-sample-prep.md`.
- **Slot occupancy / seated** — per-cell depth on the `tray_cam` cloud:
  empty vs filled, and "fully down in the right cell."
- **Spill / foam** — colour/texture anomaly in RGB; flag, do not
  proceed.

**5. Wire the verification gates as services.** Wrap each check as a
ROS 2 **service** that returns PASS / FAIL / UNSURE plus the evidence
(measurement, timestamp, and the frame used). The Behavior Tree in
`08-orchestration-error-handling-and-safety.md` calls the right gate
after each action and only ticks onward on PASS:

```
pick ──▶ [gate: in gripper?] ──▶ decap ──▶ [gate: open rim?]
  ──▶ dispense ──▶ [gate: level ok? no spill?] ──▶ cap
  ──▶ [gate: cap seated?] ──▶ scan ──▶ [gate: matches worklist?]
  ──▶ place ──▶ [gate: seated in correct slot?] ──▶ next vial
```

**6. Grade against ground truth.** Because this is sim, query Gazebo's
true object poses and fill-volume state (the dispenser's scalar from
`04-liquid-handling-and-sample-prep.md`) and compare them with what the
detector reported. A run where detections track ground truth across
many vials is the evidence that the *pipeline* is correct — before any
of it meets real glass and real light.

## Additional hardware needed

On the real cell this part needs **RGB-D cameras** (one on the wrist,
two or three fixed) and **controlled lighting** (diffuse, glare-free
illumination so glass and liquid read consistently), plus printed
**AprilTag** stickers and camera mounts. In sim none of this is bought:

- cameras → Gazebo `rgbd_camera` sensor plugins publishing to ROS 2;
- lighting → the world's light sources (clean and constant, which is
  exactly why thresholds must later be re-tuned on hardware);
- AprilTags → textured square models in the SDF.

The fidelity claim is modest on purpose: the *wiring and logic* are
real; the *photons* are not.

## How it connects

- `02-vial-handling-and-gripping.md` — verifies the grasp: vial located
  before the grip, confirmed in the gripper after it.
- `03-decapping-and-capping.md` — gates confirm the vial is open before
  fill and the cap is seated after re-capping.
- `04-liquid-handling-and-sample-prep.md` — the approximate level /
  spill / foam checks verify the dispense visibly happened; ground
  truth is the dispenser's fill-volume state.
- `05-tray-loading-and-positioning.md` — slot-occupancy and seated
  checks confirm the right slot is empty and the vial is fully down.
- `08-orchestration-error-handling-and-safety.md` — a failed gate is
  the event that triggers retry, quarantine, or stop.
- High-level companion:
  `../03-high-level-solution/07-perception-and-verification.md`.
- Folder overview: [`README.md`](README.md).
