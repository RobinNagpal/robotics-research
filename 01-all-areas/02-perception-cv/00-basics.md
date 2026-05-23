# Perception & Computer Vision — The Basics

> Written for a web developer who has never touched a robot. Read
> this before the other files in this folder.

## What is this field, in detail?

A robot is blind until perception code turns its raw sensor data —
camera pixels, LiDAR returns, depth maps, IMU readings — into
**structured knowledge of the world**. Specifically: "there is a red
mug at world coordinates (1.23, -0.45, 0.78), oriented 30 degrees
off-axis, sitting on a table 80 cm in front of me, and the detected
human face is looking away."

If LLMs are about understanding language, perception is about
understanding the physical scene in front of a robot, accurately
enough that downstream code (motion planner, grasp selector, safety
monitor) can act on it without crashing into things or breaking the
part it just picked up.

Think of perception as the parse + hydrate layer of the robot's
app: sensors emit a firehose of bytes; perception is the
`JSON.parse` + schema validator + reducer producing a typed 3D
world-state that every downstream consumer reads. Garbage in,
garbage everywhere downstream.

Flashy demos (a humanoid pouring coffee, a Waymo doing a California
stop) work because the perception stack made the scene legible.
Most robotics startups that fail do so because perception was 80%
reliable when it needed to be 99.5%.

### How perception differs from "computer vision"

Computer vision spans Instagram filters, medical imaging, and
satellite analysis. **Robotics perception** is CV with extra
constraints:

- **Real-time.** Most perception runs at 10-60 Hz. A 200 ms delay
  can crash a quadcopter or topple a bipedal robot. The frame
  budget (16.6 ms at 60 Hz, 33 ms at 30 Hz, 11 ms at 90 Hz) is a
  contract, not a target.
- **Geometry-aware.** Output is a 3D pose / mesh / trajectory, not
  just a label. "It's a chair" isn't enough; you need where the
  seat is, where the legs are, which way the back faces.
- **Multi-sensor.** Production robots fuse RGB + depth + IMU + LiDAR
  + sometimes radar. Time-syncing and cross-calibrating these
  sensors is most of the engineering work. A 5 ms misalignment can
  move a pedestrian by 30 cm at highway speed.
- **Edge-deployed.** Inference runs on a Jetson, an embedded RTX, or
  custom silicon — not on an A100 in a data center. Model size and
  TensorRT optimization matter.
- **Safety-critical.** A misclassification on a Tesla isn't bad UX,
  it's a crash. Perception engineers do failure-mode analysis the
  way frontend devs handle bug tickets, except the "P0" can be a
  recall.

### Coordinate frames: the part nobody warned you about

Every sensor, joint, and object has its own coordinate frame. The
camera thinks "+Z forward, +X right, +Y down" (OpenCV); ROS thinks
"+X forward, +Y left, +Z up"; the arm base has its own; the world
has yet another. You will spend an embarrassing amount of your
first year converting between them. The `tf2` transform tree lets
you ask "give me the transform from `base_link` to
`camera_color_optical_frame` as of timestamp T." Common bug-class:
forgetting to wait for a transform to become available at startup.

### The four canonical perception sub-problems

Almost every robotics perception task is one of these four, or a
combination:

1. **Detection / segmentation** — what objects are in this image,
   and which pixels belong to each. (YOLO, DETR, SAM 2, Mask2Former.)
   - *Example:* a warehouse robot looks at a shelf; the detector
     returns `{bbox, mask, label, confidence}` per item. The mask
     is a per-pixel boolean telling the grasp planner which pixels
     are "this box" vs "shelf behind it."
   - *Try locally:* `pip install ultralytics` then
     `from ultralytics import YOLO; m = YOLO("yolov8n.pt"); m("img.jpg")`.
   - *Hugging Face entry:* `facebook/sam2-hiera-large` via
     `transformers.Sam2Model.from_pretrained(...)`.
2. **6-DoF pose estimation** — where is this specific object in 3D
   space, and how is it rotated. (FoundationPose, MegaPose.) Core
   problem for grasping.
   - *Example:* given an RGB-D crop of a power drill and its CAD
     mesh, the model returns a 4x4 transform `T_camera_drill`. The
     grasp planner transforms its pre-computed "how to grip a drill"
     poses into the camera frame.
   - *Try locally:* `git clone https://github.com/NVlabs/FoundationPose`
     and follow the conda env. No `pip install` shortcut yet —
     research code.
3. **Depth and 3D reconstruction** — how far is each pixel, and what
   does the 3D scene look like. (Depth-Anything, NeRF, Gaussian
   Splatting, COLMAP.)
   - *Example:* a drone flies over a vineyard taking 200 overlapping
     photos; COLMAP estimates each camera pose and reconstructs a
     dense point cloud used to count grape clusters.
   - *Try locally:* `pip install transformers` then
     `from transformers import pipeline; depth = pipeline(task="depth-estimation", model="depth-anything/Depth-Anything-V2-Small-hf")`.
4. **SLAM (Simultaneous Localization and Mapping)** — given a moving
   camera, where am I, and what does the map look like. (ORB-SLAM3,
   VINS-Fusion, DROID-SLAM.) The GPS + cartographer for indoor robots.
   - *Example:* a Roomba-like robot enters a new apartment;
     visual-inertial SLAM builds an occupancy map as it drives while
     estimating its own pose to a few centimeters, so it can return
     to the dock.
   - *Try locally:* SLAM is mostly C++. Clone
     `https://github.com/UZ-SLAMLab/ORB_SLAM3`, build with CMake
     against OpenCV + Pangolin + Eigen. Python-friendly option:
     `git clone https://github.com/princeton-vl/DROID-SLAM`.

Most real pipelines use 2-3 of these together.

### Why this is one of the most reliable robotics specialties

- **Broadest customer base.** Every robot, drone, AV, AR headset,
  inspection rig, and security camera needs perception. You can
  sell into warehouses, hospitals, farms, defense, automotive, and
  AR with overlapping skills.
- **Foundation models changed everything.** SAM 2 (Meta, 2024),
  DINOv2 (Meta, 2023), Depth-Anything v2 (2024), FoundationPose
  (NVIDIA, 2024) turned problems that required PhD-level expertise
  in 2020 into "load the model from Hugging Face and call it."
- **Strong pay bands.** Robotics Software Engineer median is $189k
  (2025 Robotics Salary Guide); perception specialists at AV / AR
  shops clear $300k+ TC.

### What the day-to-day work looks like

- **Sensor calibration.** Intrinsics and extrinsics. Camera-to-camera,
  camera-to-IMU, camera-to-LiDAR. Lots of Kalibr, lots of
  checkerboards. Get a unit wrong (mm vs m) or flip an axis and
  every downstream consumer is silently wrong forever.
- **Pipeline building.** Wiring detection -> tracking -> 3D
  triangulation -> SLAM -> map publication, in ROS2 or proprietary
  middleware. A ROS2 topic is a typed pub/sub channel — like a
  Kafka topic, but with `.msg` files and QoS knobs.
- **Model integration.** Taking a research model (SAM 2,
  FoundationPose, ORB-SLAM3) and making it run at 30+ Hz on a Jetson
  with TensorRT.
- **Failure-mode triage.** A black object on a black background, a
  depth camera dying in sunlight, SLAM diverging in a featureless
  hallway.
- **Data pipelines.** Collecting, labeling, augmenting, validating.

About 60% Python, 40% C++ (most production SLAM and high-rate
perception is C++).

### A typical week of a junior perception engineer

Composite from real new-hire schedules at AV / warehouse / humanoid
shops.

- **Monday:** standup + overnight CI triage (mAP dropped 0.4 points
  — why?); bisect the regression across training-data subsets; pair
  on a TensorRT engine that won't compile a custom ONNX op (segfault
  in C++, no stack trace); write a bag-replay script that pulls a
  30-second rosbag from S3 and reruns your detector.
- **Tuesday:** data labeling QA — spot-check 200 contractor-labeled
  images, find 18 wrong (the "forklift" class is being applied to
  pallet jacks), write a one-pager for the vendor; tweak data
  augmentation (brightness, motion blur) in your PyTorch
  `Dataset.__getitem__` and kick off an overnight 8xH100 run that
  costs $200; triage a depth camera that reads NaN for the first
  50 ms after boot.
- **Wednesday:** calibration day — hold a 1m checkerboard in front
  of three cameras and an IMU in 40 poses while Kalibr crunches
  geometry, output new YAML with sub-millimeter intrinsics; build a
  ROS2 node in C++ that subscribes to `/camera/image_raw`, runs your
  detector, publishes `/perception/detections`; chase down why the
  new node drops every 5th frame (you forgot `SensorDataQoS`).
- **Thursday:** deep work — read the FoundationPose paper, prototype
  a pose-estimation node in a notebook against a saved rosbag;
  quantize a PyTorch model to INT8 on a Jetson Orin (45 ms -> 18 ms,
  accuracy drops 1.2 points — worth it?); code review for two
  teammates.
- **Friday:** demo the week in a perception sync (replay a rosbag,
  show before/after); write a one-page design doc for next sprint
  (nighttime cyclist detector); cleanup.

Rough mix: ~40% code, ~25% data, ~20% meetings/reviews/docs, ~15%
physical-world work (calibration, sensor mounts, robot pilots).

---

## Three fully developed real-world use cases

Deployed perception systems as of 2025. For each, the **hardware**
(sensors, compute) and **software** (models, frameworks, libraries).

---

### Use case 1 — Waymo robotaxi (multi-sensor AV perception)

**What it does.** Waymo runs fully driverless robotaxi service in
Phoenix, San Francisco, Los Angeles, Austin, and Atlanta. Their
6th-generation Driver must detect and track every car, pedestrian,
cyclist, traffic light, lane marking, construction sign, and
unexpected obstacle at highway speeds, in heavy rain, at night, and
inside underground parking garages — all on-vehicle.

**The technical novelty.** Waymo fuses RGB cameras + LiDAR + radar
+ ultrasonics into a unified "occupancy + trajectory" representation.
Their stack is the most-tested in the industry: 30+ million
autonomous miles on public roads and tens of billions of simulator
miles by 2024.

**Hardware stack.**

- **Vehicles:** Jaguar I-PACE (current fleet), Geely Zeekr (next-gen,
  announced 2024).
- **Cameras:** 29+ per vehicle — long-range telephoto for highway,
  wide-angle for intersections, perimeter for cyclists / pedestrians.
  Multiple exposure modes for HDR.
- **LiDAR:** Waymo's proprietary long-range LiDAR + perimeter
  short-range LiDARs. 5 LiDARs per vehicle in the 6th-gen system.
- **Radar:** 6 imaging radars for adverse-weather and long-range
  velocity sensing.
- **Compute:** custom Waymo-designed platform (proprietary; widely
  reported to use NVIDIA + custom ASICs). On the order of 100-300 W
  for inference.
- **Cooling:** liquid cooling for the compute stack.
- **Data backhaul:** 4G/5G + offline upload at depots; petabytes of
  recordings per day across the fleet.

**Software stack.**

- **Detection / segmentation:** custom transformer-based detectors
  trained on Waymo Open Dataset + internal data. Published papers
  include MultiPath++ (trajectory prediction), MVF (multi-view
  fusion), Wayformer.
- **3D object detection:** PointPillars, CenterPoint, VoxelNet
  variants for LiDAR.
- **Sensor fusion:** occupancy networks that consume camera + LiDAR
  + radar and emit a unified 3D voxel grid.
- **Tracking:** custom multi-object trackers with per-class motion
  models.
- **Trajectory prediction:** transformer-based predictors
  (MultiPath++, Wayformer).
- **Localization:** HD map matching with LiDAR + visual features.
- **Calibration:** custom rigs and self-calibration routines that
  run every drive.
- **Frameworks:** internal stack on top of **TensorFlow**
  (historically a TF shop, though PyTorch usage has grown); C++ for
  inference hot paths; Bazel for build.
- **Sim:** tightly coupled with Waymo's internal AV simulator
  (CarCraft) for training and validation.
- **Edge inference:** custom-tuned model graphs, low-precision
  quantization, custom kernels.

**What would surprise a web dev.** Each camera's intrinsic matrix
(focal length, principal point, distortion) is calibrated to roughly
micrometer precision and then treated as a near-constant for the
life of the camera. A fender-bender that shifts a sensor by 0.5 mm
can flag the vehicle out of service. The other surprise: the
perception stack is not one giant end-to-end net. It's a graph of
dozens of smaller models and classical algorithms wired together —
closer to a microservice architecture than a monolithic LLM.

**Failure modes they specifically engineer around.**

- *Sensor occlusion:* mud, snow, bird droppings, sunscreen smears.
  The fusion layer gracefully degrades when one modality goes dark.
- *Adversarial pedestrians:* people in costumes, on scooters
  carrying mirrors, holding umbrellas that change silhouette
  frame-to-frame. Novelty detectors flag low-confidence regions for
  more cautious behavior.
- *Phantom braking from radar multi-path:* a radar return bouncing
  off an overpass can look like a stopped vehicle. Cross-checking
  against camera + LiDAR catches this.

**Why this matters.** Waymo is the proof point that multi-sensor
perception can be reliable enough for unsupervised public deployment.
Almost every other AV team has converged on a variant of this recipe
(Cruise, Zoox, Mobileye, Pony.ai all run camera + LiDAR + radar
fusion; only Tesla diverges with vision-only).

---

### Use case 2 — Apple Vision Pro (real-time spatial scene understanding)

**What it does.** A head-mounted mixed-reality device that does what
Waymo does, but on a head, at 90 Hz, with single-digit-millisecond
motion-to-photon latency. The perception stack handles 6-DoF head
tracking, real-time 3D scene reconstruction (mesh of your room),
plane detection, sub-millimeter hand tracking, 240 Hz gaze tracking,
and persistent room-scale mapping that survives reboots.

**The technical novelty.** Entirely on-device. Two custom Apple
chips split the workload: M2 does general compute; R1 does sensor
I/O and fusion with sub-12 ms latency. The combination of latency,
accuracy, and power efficiency is unmatched.

**Hardware stack.**

- **Cameras:** 12 total — 2 main pass-through (high res), 2
  lower-res for world tracking, 4 IR for hand tracking, 4 IR for
  eye tracking.
- **Sensors:** TrueDepth (structured light) for face tracking, LiDAR
  for room reconstruction, IR illuminators for hand tracking in the
  dark, IMUs, ambient light sensors.
- **Compute:** Apple M2 + Apple R1. R1 has 256 GB/s memory bandwidth.
- **Displays:** dual 4K micro-OLED, 90/96/100 Hz refresh.
- **Power:** ~2-2.5 hours per external battery; ~30 W total.

**Software stack.**

- **OS:** visionOS, derived from iOS / macOS XNU kernel.
- **Spatial framework:** **ARKit** (extended for visionOS) plus
  internal extensions.
- **Hand tracking:** per-finger 3D pose from IR cameras. Custom
  Apple neural net on the R1.
- **Eye tracking:** 240 Hz pupil + gaze, used for input (look +
  pinch) and foveated rendering (only the pixels you're looking at
  render at full quality).
- **Scene reconstruction:** real-time mesh from LiDAR + RGB.
  Persistent across sessions ("World Sense").
- **Plane / surface detection:** same lineage as ARKit on iPhones,
  but real-time and 3D.
- **SLAM:** visual-inertial SLAM. Apple doesn't publish details, but
  the system is known to combine VIO + LiDAR + persistent map
  alignment.
- **Foveated rendering:** dynamically lowers resolution outside the
  gaze cone. Cuts GPU load ~50%.
- **Developer frameworks:** ARKit, RealityKit, Metal, SwiftUI with
  spatial extensions.

**What would surprise a web dev.** The motion-to-photon budget is
~12 ms — from physical head motion to new pixels on display.
Anything more and your inner ear notices and nausea sets in. Compare
that to a web app where 100 ms of input latency is invisible. The
other surprise: the "pass-through view" is not a passthrough at all.
It's a fully rendered 3D reconstruction of the room with the live
camera feed warped onto it. Every frame is a render, not a relay.

**Failure modes they specifically engineer around.**

- *Texture-poor rooms* (white walls, empty hallways) starve visual
  SLAM of features. LiDAR is the backup.
- *Rapid head motion* (sneezing, sports) blurs cameras and saturates
  the IMU. The R1's tight VIO loop recovers within a couple frames.
- *Re-localization* after taking the headset off and back on has to
  land in the same world frame, or virtual monitors hop a foot to
  the left. Persistent map storage and re-localization are a major
  engineering investment.

**Why this matters.** The most polished consumer perception stack on
Earth. Head-worn, battery-powered, no perceptible latency — those
constraints push every part of the pipeline. Almost every CV
technique you'll learn for robotics shows up here, with
consumer-product discipline applied.

---

### Use case 3 — Pickle Robot (autonomous truck unloading)

**What it does.** Pickle's robot sits at the back of a 53-foot
semi-trailer and unloads packages (1-65 lbs, random shapes,
sometimes crushed or wedged) onto a conveyor. It handles 1000+
packages per hour, runs unsupervised, and has been in commercial
deployment with Maersk, Estes, and Wilson Logistics since 2023.

**The technical novelty.** Trailer unloading is one of the hardest
in-the-wild perception problems: cluttered, occluded, SKU-diverse,
lighting-variable, time-pressured. The stack does real-time 6-DoF
pose estimation on arbitrary boxes (no CAD models), plans grasps
that won't damage fragile items, and continuously re-perceives as
the pile collapses.

**Hardware stack.**

- **Robot:** custom mobile gantry with a multi-DoF arm optimized
  for trailer geometry. Multiple end-effectors (suction cup arrays
  for boxes, custom grippers for irregular items).
- **Cameras:** multiple RGB-D cameras (publicly demonstrated units
  resemble Intel RealSense D400-series — active-stereo depth,
  1280x720 at 30 FPS, ~0.3-3 m effective range) mounted on the arm
  and gantry for full interior coverage. An RGB-D camera returns
  both a color image and a parallel per-pixel depth array in meters.
- **Lighting:** on-board LED arrays — trailers are pitch dark.
- **Force / torque sensors:** on the end-effector for contact and
  weight detection.
- **Compute:** industrial PC (likely NVIDIA RTX-based) on the mobile
  base. Some inference offloaded to a nearby edge server.
- **Safety:** light curtains and area scanners around the work cell
  (humans can't be in the trailer while it operates).

**Software stack.**

- **Detection + segmentation:** custom-trained detectors (likely
  YOLO / Mask R-CNN lineage) for box detection and instance
  segmentation, plus generalist segmenters (SAM 2 lineage) for
  novel item types.
- **6-DoF pose estimation:** per-box pose from RGB-D using a mix of
  classical PCA-on-point-cloud and learned methods
  (FoundationPose-style render-and-compare).
- **Grasp planning:** a separate "where to suction" planner that
  scores candidate grasp points.
- **Motion planning:** collision-aware trajectory generation through
  a chaotic, ever-changing pile.
- **State estimation / tracking:** the pile shifts constantly, so the
  system re-perceives after every grasp instead of trusting an old
  map.
- **Frameworks:** ROS2 for middleware (Pickle has publicly discussed
  ROS2, on Humble or Iron LTS distros). PyTorch for perception
  (likely 2.x with TensorRT export for the hot path); OpenCV for
  image preprocessing; Open3D for point-cloud processing.
- **Failure recovery:** if a grasp fails or an item is too heavy, a
  fallback policy kicks in (different angle, switch end-effector,
  escalate to remote human review).
- **Fleet management:** cloud dashboard monitoring uptime, throughput,
  and failure modes across deployments.

**What would surprise a web dev.** There is no training set for
what shows up in a trailer. Every truck is different, every load is
different, and many SKUs the robot has never seen before. The system
can't rely on a fixed class taxonomy — it must generalize to novel
objects on the first frame. This is why generalist foundation models
(SAM 2, FoundationPose) are a big deal for this class of work: they
collapse the "we don't have data for this SKU" problem.

**Failure modes they specifically engineer around.**

- *Collapsing pile:* grab the top box, two others slide into the
  gap, the pile geometry is now stale. Re-perceive between every
  grasp.
- *Shrink-wrapped or shiny boxes:* specular reflections wreck
  active-stereo depth. Multiple angles plus RGB-only fallback pose
  estimation cover this.
- *Crushed / non-rectangular items:* the box-prior model expects a
  cuboid. Fallback: run a generalist segmenter and grasp the largest
  flat patch the suction cups can seal against.

**Why this matters.** Pickle is a perception-heavy product company
that's profitable per-deployment — a rare outcome in robotics. It
proves that foundation models + cleverly engineered hardware can
displace a million-dollar union loader job at price points shippers
will pay. Many techniques are public (job listings, conference
talks, trade press), making it one of the best case studies for a
junior engineer to study.

---

## What ties the three use cases together

All three share five layers:

1. **A sensor suite** chosen for the failure modes that matter
   (LiDAR for adverse weather + long range in Waymo; LiDAR + IR in
   Vision Pro for low-light hand tracking; RGB-D + on-board lighting
   in Pickle for dark trailers).
2. **Calibration infrastructure** to keep all those sensors in a
   consistent coordinate frame.
3. **A perception model stack** mixing classical techniques (feature
   matching, EKF, point-cloud processing) with learned models
   (transformers for detection, NN depth, learned pose estimators).
4. **An edge-inference runtime** that hits real-time frame rates on
   whatever compute fits the form factor.
5. **A failure-mode-aware safety layer** that catches mistakes before
   they propagate to actuation.

Understand these five and you can read any robotics perception job
description and immediately know which slot each required skill fills.

---

## How a perception frame flows through the system

Each box is a "node" in the ROS2 sense (a process subscribing to
topics and publishing to others). Times are typical budgets for a
30 Hz indoor manipulator, not Waymo-class hardware.

```
   [Sensor: RGB-D camera @ 30 Hz]
              |
              | (raw bayer + depth frame, ~2-5 ms over USB3 / GMSL)
              v
   [Driver node: ros2_realsense or similar]
              |
              | publishes /camera/image_raw, /camera/depth/image_raw
              | (~1-3 ms: format conversion, timestamping)
              v
   [Preprocess node: rectify + crop + resize]
              |
              | (~2-4 ms: undistort using calibrated intrinsics,
              |  resize to model input shape)
              v
   [Neural net inference node: YOLO / SAM2 / pose estimator]
              |
              | (~8-25 ms on a Jetson Orin with TensorRT INT8;
              |  usually the biggest single chunk)
              v
   [Postprocess node: NMS + 2D -> 3D lift using depth]
              |
              | (~2-5 ms: non-max suppression, deproject pixels
              |  into camera-frame XYZ using depth + intrinsics)
              v
   [Tracker / fusion node: associate detections across frames]
              |
              | (~1-3 ms: Hungarian assignment, Kalman update)
              v
   [tf2 transform: camera frame -> world / base_link frame]
              |
              | (<1 ms: matrix multiply by current camera pose)
              v
   [Published topic: /perception/world_objects @ 30 Hz]
              |
              v
   [Downstream: motion planner, grasp picker, safety monitor]
```

Total wall-clock budget at 30 Hz: ~33 ms per frame. The inference
node usually eats half of that. Anything above 33 ms means you're
dropping frames and downstream consumers are reading stale state.

---

## What's next to read

- `01-examples.md` — the broader landscape of who's building what.
- `02-learn.md` — the layered curriculum to build the skills above.
- `03-start.md` — a concrete 8-week ramp-up.
- `06-courses.md` — courses (basics + project-driven) to take.
