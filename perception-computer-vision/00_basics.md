# Perception & Computer Vision — The Basics

> Written for a web developer who has never touched a robot. Read
> this before the other files in this folder.

## What is this field, in detail?

A robot is blind until perception code turns its raw sensor data —
camera pixels, LiDAR returns, depth maps, IMU readings — into
**structured knowledge of the world**. Specifically: "there is a red
mug at world coordinates (1.23, -0.45, 0.78), oriented 30 degrees
off-axis, with surface normal pointing up, and it's sitting on a
table 80 cm in front of me, on top of a tablecloth, and the
human-detected face is looking away from me."

If LLMs are about understanding language, perception is about
**understanding the physical scene** in front of a robot — in
real-time, accurately enough that downstream code (motion planner,
grasp selector, safety monitor) can act on it without crashing into
things or breaking the part it picked up.

### How perception differs from "computer vision"

Computer vision is a broad academic field that includes everything
from Instagram face filters and TikTok background blur to medical
imaging and satellite analysis. **Robotics perception** is a specific
application of computer vision with extra constraints:

- **Real-time.** Most robotics perception runs at 10-60 Hz. A
  perception delay of 200 ms can crash a quadcopter or topple a
  bipedal robot.
- **Geometry-aware.** The answer must be a 3D pose / mesh /
  trajectory, not just a label. "It's a chair" isn't enough; you
  need "the seat surface is here, the legs are there, the back is
  oriented this way."
- **Multi-sensor.** Production robots fuse RGB + depth + IMU + LiDAR
  + sometimes radar. Time-syncing and cross-calibrating these
  sensors is most of the engineering work.
- **Edge-deployed.** Inference runs on a Jetson, an embedded RTX, or
  custom silicon — not on an A100 in a data center. Model size and
  TensorRT optimization matter.
- **Safety-critical.** A misclassification on a Tesla isn't a bad UX,
  it's a crash. Perception engineers deal with failure-mode analysis
  the way frontend devs deal with bug tickets.

### The four canonical perception sub-problems

Almost every robotics perception task is one of these four (or a
combination):

1. **Detection / segmentation** — "what objects are in this image,
   and which pixels belong to each one?" (YOLO, DETR, SAM 2, Mask2Former.)
2. **6-DoF pose estimation** — "where is this specific object in 3D
   space, and how is it rotated?" (FoundationPose, MegaPose.) Core
   problem for grasping.
3. **Depth and 3D reconstruction** — "how far is each pixel from
   the camera, and what does the 3D scene look like?" (Depth-Anything,
   NeRF, Gaussian Splatting, COLMAP.)
4. **SLAM (Simultaneous Localization and Mapping)** — "given a moving
   camera, where am I, and what does the map of my environment look
   like?" (ORB-SLAM3, VINS-Fusion, DROID-SLAM.) The "GPS + cartographer"
   for indoor robots.

### Why this is one of the most reliable robotics specialties

- **Broadest customer base.** Every robot, drone, AV, AR headset,
  industrial inspection rig, and security camera needs perception.
  You can sell into warehouses, hospitals, farms, defense,
  automotive, and AR with overlapping skills.
- **Foundation models changed everything.** SAM 2 (Meta, 2024),
  DINOv2 (Meta, 2023), Depth-Anything v2 (2024), FoundationPose
  (NVIDIA, 2024) made problems that required PhD-level expertise
  in 2020 into "load the model from Hugging Face and call it"
  problems in 2025.
- **Strong, well-defined pay bands.** Robotics Software Engineer
  median is $189k (2025 Robotics Salary Guide); perception specialists
  at AV / AR shops clear $300k+ TC.

### What the day-to-day work looks like

A working perception engineer spends their time on:

- **Sensor calibration**: getting intrinsics and extrinsics right.
  Camera-to-camera, camera-to-IMU, camera-to-LiDAR. Lots of Kalibr,
  lots of checkerboards.
- **Pipeline building**: wiring detection -> tracking -> 3D
  triangulation -> SLAM -> map publication, all in ROS2 or a
  proprietary middleware.
- **Model integration**: taking a research-grade model (SAM 2,
  FoundationPose, ORB-SLAM3) and making it run at 30+ Hz on a
  Jetson with TensorRT.
- **Failure-mode triage**: when the model misses a black object on
  a black background, when the depth camera dies in sunlight, when
  the SLAM diverges in a featureless hallway.
- **Data pipelines**: collecting, labeling, augmenting, validating.

About 60% Python, 40% C++ (most production SLAM and high-rate
perception is C++).

---

## Three fully developed real-world use cases

These are deployed perception systems in 2025. For each one we list
the **hardware** (sensors, compute) and the **software** (models,
frameworks, libraries).

---

### Use case 1 — Waymo robotaxi (multi-sensor AV perception)

**What it does.** Waymo runs fully driverless robotaxi service in
Phoenix, San Francisco, Los Angeles, Austin, and Atlanta as of
2025. Their 6th-generation Driver perception system must detect
and track every car, pedestrian, cyclist, traffic light, lane
marking, construction sign, and unexpected obstacle (couches in
the road, plastic bags blowing across an intersection) at highway
speeds, in heavy rain, at night, and inside underground parking
garages — all while running entirely on-vehicle compute.

**The technical novelty.** Waymo fuses RGB cameras + LiDAR + radar
+ ultrasonic sensors into a unified "occupancy + trajectory"
representation. Their stack is famously the most-tested in the
industry: 30+ million autonomous miles on public roads and tens of
billions of simulator miles by 2024.

**Hardware stack.**

- **Vehicles**: Jaguar I-PACE (current production fleet), Geely
  Zeekr (next-gen, announced 2024).
- **Cameras**: 29+ cameras per vehicle — long-range telephoto for
  highway, wide-angle for intersections, perimeter cameras for
  cyclist / pedestrian detection. Multiple exposure modes for HDR.
- **LiDAR**: Waymo's own proprietary long-range LiDAR + perimeter
  short-range LiDARs. 5 LiDARs per vehicle in the 6th-gen system.
- **Radar**: 6 imaging radars per vehicle for adverse-weather and
  long-range velocity sensing.
- **Compute**: custom Waymo-designed compute platform (details
  proprietary; widely reported to use NVIDIA + custom ASICs). On
  the order of 100-300 W power budget for inference.
- **Cooling**: liquid cooling for the compute stack.
- **Data backhaul**: 4G/5G + offline upload at depots; petabytes of
  recordings per day across the fleet.

**Software stack.**

- **Detection / segmentation**: custom transformer-based detectors
  trained on Waymo Open Dataset + internal data. Published papers
  include MultiPath++ (trajectory prediction), MVF (multi-view
  fusion), Wayformer.
- **3D object detection**: PointPillars, CenterPoint, VoxelNet
  variants for LiDAR.
- **Sensor fusion**: occupancy networks that consume camera + LiDAR
  + radar and emit a unified 3D voxel grid.
- **Tracking**: custom multi-object trackers with motion models
  per object class.
- **Trajectory prediction**: transformer-based future-trajectory
  predictors (MultiPath++, Wayformer).
- **Localization**: HD map matching with LiDAR + visual features.
- **Calibration**: custom-built calibration rigs and self-
  calibration routines that run every drive.
- **Frameworks**: internal stack on top of **TensorFlow** (Waymo
  has historically been a TF shop, though PyTorch usage has grown);
  C++ for inference hot paths; Bazel for build.
- **Sim integration**: tightly coupled with Waymo's internal AV
  simulator (CarCraft) for training and validation.
- **Edge inference**: custom-tuned model graphs, low-precision
  quantization, custom kernels.

**Why this matters.** Waymo is the proof point that multi-sensor
robotics perception can be made reliable enough for unsupervised
public deployment. Almost every other AV team has converged on a
variant of the Waymo recipe (Waymo, Cruise, Zoox, Mobileye, Pony.ai
all run camera + LiDAR + radar fusion; only Tesla diverges with
vision-only).

---

### Use case 2 — Apple Vision Pro (real-time spatial scene understanding)

**What it does.** Apple Vision Pro is a head-mounted mixed-reality
device that needs to do **everything Waymo does, but on a head, in
real-time, at 90 Hz, with single-digit-millisecond motion-to-photon
latency**. The perception stack does: 6-DoF head tracking, 3D scene
reconstruction (real-time mesh of your room), plane detection,
hand tracking (sub-millimeter), gaze tracking (eye direction at
240 Hz), and persistent room-scale mapping that survives reboots.

**The technical novelty.** The whole thing runs on-device with no
cloud round-trip. Two custom Apple chips (M2 + R1) split the
workload: M2 does general compute; R1 does sensor I/O and fusion
with sub-12 ms latency. The combination of latency, accuracy, and
power efficiency is unmatched in the industry.

**Hardware stack.**

- **Cameras**: 12 cameras total — 2 main pass-through cameras (high
  resolution, for what you see), 2 lower-resolution cameras for
  world tracking, 4 IR cameras for hand tracking, and 4 IR cameras
  for eye tracking.
- **Sensors**: a TrueDepth (structured light) sensor for face
  tracking, a LiDAR scanner for room reconstruction, IR illuminators
  for hand tracking in the dark, IMUs, ambient light sensors.
- **Compute**: Apple M2 (general compute) + Apple R1 (sensor
  fusion + scene understanding). The R1 has 256 GB/s memory
  bandwidth.
- **Displays**: dual 4K micro-OLED panels, 90/96/100 Hz refresh.
- **Power**: ~2-2.5 hours per external battery; ~30 W total
  consumption.

**Software stack.**

- **OS**: visionOS, derived from iOS / macOS XNU kernel.
- **Spatial computing framework**: **ARKit** (extended for visionOS),
  plus Apple-internal extensions.
- **Hand tracking**: per-finger 3D pose from IR cameras. Custom
  Apple neural network running on the R1.
- **Eye tracking**: 240 Hz pupil + gaze estimation. Used both for
  UI input (look + pinch) and for foveated rendering (only the
  pixels you're looking at are rendered at full quality).
- **Scene reconstruction**: real-time mesh generation from LiDAR +
  RGB. Persistent across sessions ("World Sense").
- **Plane / surface detection**: same lineage as ARKit's plane
  detection on iPhones, but real-time and 3D.
- **SLAM**: visual-inertial SLAM. The technical details are not
  published in academic papers (Apple does not publish much), but
  the system is known to combine VIO + LiDAR + persistent map
  alignment.
- **Foveated rendering**: dynamically lowers render resolution
  outside the gaze cone. Cuts GPU load ~50%.
- **Frameworks for developers**: ARKit, RealityKit, Metal, SwiftUI
  with spatial extensions.

**Why this matters.** Vision Pro is the most polished consumer
perception stack on Earth as of 2025. The constraints (head-worn,
battery-powered, no perceptible latency) push every part of the
perception pipeline. Almost every CV technique you'll learn for
robotics shows up in Vision Pro — but with consumer-product
discipline applied.

---

### Use case 3 — Pickle Robot (autonomous truck unloading)

**What it does.** Pickle Robot's autonomous trailer-unloading robot
sits at the back of a 53-foot semi-trailer and unloads packages —
each weighing 1-65 lbs, in random shapes and sizes, sometimes
crushed, sometimes wedged — onto a conveyor. It handles 1000+
packages per hour, runs unsupervised, and has been in commercial
deployment with major shippers (Maersk, Estes, Wilson Logistics)
since 2023.

**The technical novelty.** Trailer unloading is one of the hardest
"in-the-wild" perception problems in robotics: cluttered, occluded,
SKU-diverse, lighting-variable, and time-pressured. Pickle's
perception stack must do real-time 6-DoF pose estimation on
arbitrary boxes (no CAD models), plan a grasp that won't damage
fragile items, and continuously update as the box-pile collapses
unpredictably.

**Hardware stack.**

- **Robot**: custom-designed mobile gantry with a multi-DoF arm
  optimized for trailer geometry. Multiple end-effectors (suction
  cup arrays for boxes, custom grippers for irregular items).
- **Cameras**: multiple RGB-D cameras (Intel RealSense or
  equivalent depth cameras) mounted on the arm and on the gantry
  for full coverage of the trailer interior.
- **Lighting**: on-board LED arrays — trailers are pitch dark inside.
- **Force / torque sensors**: on the end-effector to detect contact
  and item weight.
- **Compute**: industrial PC (likely NVIDIA RTX-based) on the
  mobile base. Some inference offloaded to nearby edge server.
- **Safety**: light curtains and area scanners around the work cell
  (humans can't be in the trailer while it operates).

**Software stack.**

- **Detection + segmentation**: custom-trained detectors (likely
  YOLO / Mask R-CNN lineage) for box detection and instance
  segmentation, plus generalist segmenters (SAM 2 lineage) for
  novel item types.
- **6-DoF pose estimation**: per-box pose from RGB-D using a
  combination of classical PCA-on-point-cloud techniques and
  learned methods (FoundationPose-style render-and-compare).
- **Grasp planning**: a separate "where to suction" planner that
  scores candidate grasp points on each box.
- **Motion planning**: collision-aware trajectory generation; the
  arm threads through a chaotic, ever-changing pile.
- **State estimation / tracking**: the box-pile is constantly
  shifting, so the system re-perceives after every grasp instead of
  trusting an old map.
- **Frameworks**: ROS2 for middleware (Pickle has publicly
  discussed using ROS2). PyTorch for perception; OpenCV for
  image preprocessing; Open3D for point-cloud processing.
- **Failure recovery**: if a grasp fails or an item is too heavy,
  a fallback policy kicks in (try a different angle, switch end-
  effector, escalate to remote human review).
- **Fleet management**: a cloud dashboard that monitors uptime,
  throughput, and failure modes across deployments.

**Why this matters.** Pickle is a perception-heavy product company
that's actually profitable on a per-deployment basis — a rare
outcome in robotics. It proves that the "modern perception
foundation models + cleverly engineered hardware" combo can
displace a million-dollar union loader job at price points
shippers are willing to pay. Many of the techniques are public
(via job listings, conference talks, and trade press), making it
one of the best case studies for a junior engineer to study.

---

## What ties the three use cases together

All three systems share five layers:

1. **A sensor suite** chosen for the failure modes that matter
   (LiDAR for adverse weather + long range in Waymo; LiDAR + IR
   in Vision Pro for low-light hand tracking; RGB-D + on-board
   lighting in Pickle for dark trailers).
2. **Calibration infrastructure** to keep all those sensors in a
   consistent coordinate frame.
3. **A perception model stack** that mixes classical techniques
   (feature matching, EKF, point-cloud processing) with learned
   models (transformers for detection, NN-based depth, learned
   pose estimators).
4. **An edge-inference runtime** that hits real-time frame rates
   on whatever compute fits in the form factor.
5. **A failure-mode-aware safety layer** that catches the perception
   stack's mistakes before they propagate to actuation.

If you understand these five layers, you can read any robotics
perception job description and immediately know which slot each
required skill fills.

---

## What's next to read

- `01-examples-of-work.md` — the broader landscape of who's building
  what.
- `02-important-to-learn.md` — the layered curriculum to build the
  skills above.
- `03-how-to-start.md` — a concrete 8-week ramp-up.
- `06_courses.md` — courses (both basics + project-driven) to take.
