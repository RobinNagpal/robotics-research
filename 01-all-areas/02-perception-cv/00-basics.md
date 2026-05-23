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

**Web-dev analogy.** Think of perception as the "parsing + state
hydration" layer of a robot's app. Sensors emit a chaotic firehose
of bytes (similar to a raw WebSocket stream of `MessageEvent`s).
Perception code is the equivalent of `JSON.parse` plus your Zod /
io-ts schema validators plus your Redux reducers, except instead
of producing a typed React state tree it produces a typed 3D world
state. Downstream consumers (the motion planner, the grasp picker)
are like your React components: they re-render — i.e., re-plan —
whenever the world-state store updates. If the parsing layer
emits garbage, every component downstream rerenders garbage.

**Why this is the unsexy-but-load-bearing part of robotics.**
The flashy demos (a humanoid pouring coffee, a Waymo doing a
California stop) are visible because the perception stack made
them legible. Without perception, every other system has to
guess. Most robotics startups that fail do so because the
perception stack was 80% reliable when it needed to be 99.5% —
the difference between "cool demo" and "cool product."

### How perception differs from "computer vision"

Computer vision is a broad academic field that includes everything
from Instagram face filters and TikTok background blur to medical
imaging and satellite analysis. **Robotics perception** is a specific
application of computer vision with extra constraints:

- **Real-time.** Most robotics perception runs at 10-60 Hz. A
  perception delay of 200 ms can crash a quadcopter or topple a
  bipedal robot. *Web-dev analogy: imagine if your React app had to
  hit 60 fps not because users prefer it, but because dropping below
  60 fps physically damages the laptop.* The "frame budget" (16.6 ms
  at 60 Hz, 33 ms at 30 Hz, 11 ms at 90 Hz) is treated like a
  contract, not a target.
- **Geometry-aware.** The answer must be a 3D pose / mesh /
  trajectory, not just a label. "It's a chair" isn't enough; you
  need "the seat surface is here, the legs are there, the back is
  oriented this way." *Web-dev analogy: every detection has to come
  back with `{label, position3D, orientation3D, confidence}` —
  not just a string. Think of it as a stricter TypeScript type
  on every model output.*
- **Multi-sensor.** Production robots fuse RGB + depth + IMU + LiDAR
  + sometimes radar. Time-syncing and cross-calibrating these
  sensors is most of the engineering work. *Web-dev analogy: it's
  like merging events from five different microservices, each with
  its own clock, into one ordered event stream — except the clocks
  drift by microseconds and a 5 ms misalignment can move a
  pedestrian by 30 cm at highway speed.*
- **Edge-deployed.** Inference runs on a Jetson, an embedded RTX, or
  custom silicon — not on an A100 in a data center. Model size and
  TensorRT optimization matter. *Web-dev analogy: like shipping a
  React Native app to a budget Android phone — except instead of
  jank you get dropped frames that cause physical collisions.*
- **Safety-critical.** A misclassification on a Tesla isn't a bad UX,
  it's a crash. Perception engineers deal with failure-mode analysis
  the way frontend devs deal with bug tickets — except the bug
  tracker is sometimes a regulator and the "P0" can be a recall.

### Coordinate frames: the part nobody warned you about

Every sensor, every joint, every object has its own coordinate
frame. The camera thinks "+Z is forward, +X is right, +Y is down"
(OpenCV convention); ROS thinks "+X forward, +Y left, +Z up"; the
arm base has its own frame; the world has yet another. You will
spend an embarrassing amount of your first year converting between
them.

*Web-dev analogy:* the tf2 transform tree (the ROS library that
tracks frame relationships) is like React's component tree, but
for coordinate systems. Each "child" frame is defined relative to
its "parent" via a 4x4 homogeneous transform — basically a `props`
object that gets composed as you walk up the tree. Pose lookups
are like calling `useContext()`: "give me the transform from
`base_link` to `camera_color_optical_frame` as of timestamp T."

A common bug-class: forgetting to wait for a transform to become
available (the buffer is empty at startup) is the perception
equivalent of `Cannot read property 'x' of undefined`.

### The four canonical perception sub-problems

Almost every robotics perception task is one of these four (or a
combination):

1. **Detection / segmentation** — "what objects are in this image,
   and which pixels belong to each one?" (YOLO, DETR, SAM 2, Mask2Former.)
   - *Worked example:* a warehouse robot looks at a shelf; the
     detector returns a list of `{bbox, mask, label, confidence}`
     tuples — one per item. The mask is a per-pixel boolean array
     (think `Uint8Array` the size of the image) that tells the
     grasp planner exactly which pixels are "this box" vs "the
     shelf behind it."
   - *One-liner to try locally:*
     `pip install ultralytics` then
     `from ultralytics import YOLO; m = YOLO("yolov8n.pt"); m("img.jpg")`.
   - *Hugging Face entry point:* `facebook/sam2-hiera-large` (Segment
     Anything 2) for promptable segmentation; load via
     `transformers.Sam2Model.from_pretrained(...)`.
2. **6-DoF pose estimation** — "where is this specific object in 3D
   space, and how is it rotated?" (FoundationPose, MegaPose.) Core
   problem for grasping.
   - *Worked example:* given an RGB-D crop of a power drill and
     its CAD mesh, the model returns a 4x4 transform `T_camera_drill`
     — "the drill's local origin is at this XYZ in the camera
     frame, rotated by this 3x3 matrix." The grasp planner then
     transforms its pre-computed "where to grip a drill" poses
     into the camera frame.
   - *One-liner:* `git clone https://github.com/NVlabs/FoundationPose`
     and follow their conda env; the model card is on the NVIDIA
     GitHub. (No `pip install` shortcut yet — research code.)
3. **Depth and 3D reconstruction** — "how far is each pixel from
   the camera, and what does the 3D scene look like?" (Depth-Anything,
   NeRF, Gaussian Splatting, COLMAP.)
   - *Worked example:* a drone flying over a vineyard takes 200
     overlapping photos; COLMAP estimates the camera pose of each
     photo and reconstructs a dense 3D point cloud of the vines,
     which downstream code uses to count grape clusters per vine.
   - *One-liner:* `pip install transformers` then
     `from transformers import pipeline; depth = pipeline(task="depth-estimation", model="depth-anything/Depth-Anything-V2-Small-hf")`.
4. **SLAM (Simultaneous Localization and Mapping)** — "given a moving
   camera, where am I, and what does the map of my environment look
   like?" (ORB-SLAM3, VINS-Fusion, DROID-SLAM.) The "GPS + cartographer"
   for indoor robots.
   - *Worked example:* a Roomba-like robot drops into a new
     apartment; visual-inertial SLAM builds an occupancy map as it
     drives, while continuously estimating its own pose to within
     a few centimeters so it can come back to the dock.
   - *One-liner:* not a `pip install` — clone
     `https://github.com/UZ-SLAMLab/ORB_SLAM3`, build with CMake
     against OpenCV + Pangolin + Eigen. (SLAM is mostly C++.) The
     Python-friendly option is DROID-SLAM:
     `git clone https://github.com/princeton-vl/DROID-SLAM`.

*Web-dev analogy for picking among these:* think of detection as
your "list view" component, pose estimation as the "detail view"
for one selected object, depth as a global "background layer," and
SLAM as the routing layer that knows where the user (robot) is in
the whole app (world). Most real pipelines use 2-3 of these
together.

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
  lots of checkerboards. *Web-dev analogy: sensor calibration is
  TypeScript type-checking between modules. Get the conversion
  wrong once (e.g., units in mm vs m, or a flipped axis) and
  every downstream consumer is silently wrong forever — except
  there's no `tsc` to catch it for you.*
- **Pipeline building**: wiring detection -> tracking -> 3D
  triangulation -> SLAM -> map publication, all in ROS2 or a
  proprietary middleware. *Web-dev analogy: a ROS2 topic is a
  typed pub/sub channel — basically a Redis stream or a Kafka
  topic, but with `.msg` files instead of protobuf and with QoS
  knobs for reliability vs latency.*
- **Model integration**: taking a research-grade model (SAM 2,
  FoundationPose, ORB-SLAM3) and making it run at 30+ Hz on a
  Jetson with TensorRT. *Web-dev analogy: like taking a chunky
  npm dependency and tree-shaking + minifying + code-splitting
  it for a mobile bundle, except instead of bundle size you
  optimize for FLOPs and GPU memory.*
- **Failure-mode triage**: when the model misses a black object on
  a black background, when the depth camera dies in sunlight, when
  the SLAM diverges in a featureless hallway.
- **Data pipelines**: collecting, labeling, augmenting, validating.

About 60% Python, 40% C++ (most production SLAM and high-rate
perception is C++).

### A typical week of a junior perception engineer

This is a composite week from real new-hire schedules at AV /
warehouse / humanoid shops. Hours are rough; the actual mix
varies. The point is to give you a felt sense of "what do I
actually do all day."

**Monday (~8 hrs).**

- 1 hr: standup + reading overnight CI logs (your offline-eval
  job ran on the new model; mAP dropped 0.4 points — why?).
  *Like reading a failing Vercel preview deploy.*
- 3 hrs: bisect the regression by re-running yesterday's
  evaluation harness with different subsets of training data.
  *Like git-bisecting a frontend bug across commits.*
- 2 hrs: pair with a senior engineer on a TensorRT engine that
  refuses to compile a custom ONNX op. *3 hrs writing a TensorRT
  plugin is roughly 3 hrs writing a custom Webpack loader, except
  the failure mode is a segfault in C++ with no stack trace,
  not a JS console error.*
- 2 hrs: write a bag-replay script that pulls a 30-second rosbag
  from S3 and reruns your detector on it. *Like writing a
  fixtures script that hydrates a staging DB from prod snapshots.*

**Tuesday (~8 hrs).**

- 4 hrs: data labeling QA. You spot-check 200 of yesterday's
  contractor-labeled images, find 18 are wrong (the "forklift"
  class label is being applied to pallet jacks). Write a
  one-pager for the labeling vendor. *Like reviewing a contractor's
  PR — except the bug compounds across a million training samples.*
- 2 hrs: tweak data augmentation (random brightness, motion blur)
  in your PyTorch `Dataset.__getitem__`. Kick off an overnight
  training run on an 8xH100 node. *Like changing a Jest fixture
  generator, except each run costs $200 in cloud GPU time.*
- 2 hrs: triage a Jira ticket where the depth camera reads
  "NaN" for the first 50 ms after boot. Probably a driver bug.

**Wednesday (~8 hrs).**

- 2 hrs: calibration day. You and a teammate hold a 1m checkerboard
  in front of three cameras and an IMU, in 40 different poses,
  while Kalibr crunches the geometry. Output: new YAML files
  with sub-millimeter intrinsics. *Like running `prisma generate`
  after a schema change — every consumer must use the new file.*
- 3 hrs: build a ROS2 node (in C++ this time) that subscribes
  to `/camera/image_raw`, runs your detector, and publishes
  `/perception/detections`. *Like writing an Express middleware
  that listens to a Redis channel and writes back to another.*
- 3 hrs: chase down why the new node drops every 5th frame.
  (Answer: you forgot to set the QoS profile to `SensorDataQoS`.)

**Thursday (~8 hrs).**

- 4 hrs: deep work — read the FoundationPose paper, prototype
  a new pose-estimation node in a Jupyter notebook against a
  saved rosbag. *Like reading API docs for a new library and
  building a CodeSandbox proof-of-concept before you wire it
  into the real app.*
- 2 hrs: model surgery — quantize a PyTorch model to INT8 and
  benchmark it on a Jetson Orin. Latency goes from 45 ms to
  18 ms; accuracy drops 1.2 points. Decide whether that's worth it.
- 2 hrs: code review for two teammates' PRs.

**Friday (~6 hrs, half-day for many shops).**

- 2 hrs: demo your week's work in a "perception sync" meeting.
  Replay a rosbag, show before/after on a tricky failure case.
- 2 hrs: write a one-page design doc for next sprint's task
  (adding nighttime support to the cyclist detector). *Like an
  RFC for a new feature.*
- 2 hrs: cleanup — close out stale branches, push docs updates,
  reply to the offline-eval Slack channel.

**Themes across the week.**

- ~40% writing / running code.
- ~25% reading data (rosbags, logs, label sets).
- ~20% meetings, reviews, docs.
- ~15% physical-world work (calibration, sensor mounts, robot
  pilots). This is the part with no web-dev equivalent. You will
  spend more time on your knees with a tripod than you expect.

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

**What would surprise a web dev.** Each camera's intrinsic
matrix (focal length, principal point, distortion coefficients)
is calibrated to roughly micrometer precision and is then treated
as a near-constant for the life of that camera — the way you'd
treat a database schema. If a vehicle is in a fender-bender that
shifts a sensor by 0.5 mm, the car can be flagged out of service
until it's recalibrated. The other surprise: the perception stack
is *not* one giant end-to-end neural net. It's a graph of dozens
of smaller models and classical algorithms wired together —
closer to a microservice architecture than a monolithic LLM.

**Failure modes they specifically engineer around.**

- *Sensor occlusion:* mud, snow, bird droppings, or sunscreen
  smears on a single camera or LiDAR. The fusion layer is
  designed to gracefully degrade when one modality goes dark.
- *Adversarial pedestrians:* people in costumes, on scooters
  carrying mirrors, holding open umbrellas that change silhouette
  frame to frame. The detector ensemble includes "novelty"
  detectors that flag low-confidence regions for slower, more
  cautious behavior.
- *Phantom braking from radar multi-path:* a radar return
  bouncing off an overpass can look like a stopped vehicle in
  the lane. Cross-checking against camera + LiDAR catches this.

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

**What would surprise a web dev.** The "motion-to-photon" latency
budget is on the order of 12 ms — i.e., from the moment your
head physically moves to the moment the new pixels are on the
display has to be under ~12 ms or your inner ear notices and
nausea sets in. Compare that to a typical web app where 100 ms
of input latency is invisible. The other surprise: the
pass-through view you "see" is not a passthrough at all — it's
a fully rendered 3D reconstruction of the room with the live
camera feed warped onto it. Every frame is a render, not a
relay. *It's as if your `<video>` tag were actually a Three.js
scene that re-built the geometry on every frame.*

**Failure modes they specifically engineer around.**

- *Texture-poor rooms* (a freshly painted white wall, a long
  empty hallway) starve visual SLAM of features. The LiDAR
  scanner is the backup.
- *Rapid head motion* (sneezing, sports) can blur the cameras
  and saturate the IMU. The R1's tight VIO loop is tuned to
  recover within a couple frames.
- *Re-localization after taking the headset off and back on*
  needs to land in the exact same world frame, or your virtual
  monitors hop a foot to the left. Persistent map storage and
  re-localization are a major engineering investment.

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
- **Cameras**: multiple RGB-D cameras (publicly demonstrated
  units have resembled the Intel RealSense D400-series family —
  active-stereo depth, 1280x720 depth at 30 FPS, ~0.3-3 m
  effective range) mounted on the arm and on the gantry for full
  coverage of the trailer interior. *Web-dev analogy: an RGB-D
  camera is like an `<input type="file">` that returns both a
  PNG and a parallel `Float32Array` of per-pixel depths in
  meters.*
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
  discussed using ROS2, with recent industry-wide migrations
  landing on the Humble or Iron LTS distros). PyTorch for
  perception (likely 2.x series with TensorRT export for the
  hot path); OpenCV for image preprocessing; Open3D for
  point-cloud processing.
- **Failure recovery**: if a grasp fails or an item is too heavy,
  a fallback policy kicks in (try a different angle, switch end-
  effector, escalate to remote human review).
- **Fleet management**: a cloud dashboard that monitors uptime,
  throughput, and failure modes across deployments.

**What would surprise a web dev.** There is no "training set"
for what shows up in a trailer. Every truck is different, every
load is different, and many SKUs the robot has literally never
seen before. The system can't rely on a fixed class taxonomy —
it has to generalize to novel objects on the first frame.
*Web-dev analogy: imagine if your product-recommendation model
had to work on a brand-new product category, with zero training
examples, the first time a user saw it — and had to physically
pick the item up.* This is why generalist foundation models
(SAM 2, FoundationPose) are such a big deal for this class of
work: they collapse the "but we don't have data for this SKU"
problem.

**Failure modes they specifically engineer around.**

- *Collapsing pile:* you grab the top box, two others slide
  into the gap, the geometry of the whole pile is now stale.
  The system re-perceives between every grasp instead of
  trusting a planned sequence.
- *Shrink-wrapped or shiny boxes:* specular reflections wreck
  the active-stereo depth signal. Multiple camera angles plus
  RGB-only fallback pose estimation cover this.
- *Crushed / non-rectangular items:* the box-prior model
  expects a cuboid; a crushed box isn't one. The fallback is
  to run a generalist segmenter and grasp the largest flat
  patch the suction cups can seal against.

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

## Mental model: how a perception frame flows through the system

The single most useful diagram to internalize. Each box is a
"node" in the ROS2 sense (a process subscribing to topics and
publishing to others). Times are typical budgets for a 30 Hz
indoor manipulator, not Waymo-class hardware — your mileage will
vary by a factor of 2-5 either direction.

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
              |  this is usually the biggest single chunk)
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

**Total wall-clock budget at 30 Hz:** ~33 ms per frame. The
inference node usually eats half of that on its own. Anything
above 33 ms means you're dropping frames and your downstream
consumers are reading stale state.

*Web-dev analogy:* each node is an Express middleware in a
pipeline; topics are the request/response objects that flow
between them; the 33 ms budget is your equivalent of a Vercel
Edge function's cold-start budget. If any one middleware blows
its time budget, the whole request times out — and "timing out"
in robotics means a dropped detection, not a 504.

---

## What you DON'T have to know on day one

Juniors over-stress about advanced topics that they will not be
asked to touch for 6-12 months (often longer). If you can write
ergonomic Python, read C++ headers, and reason about coordinate
frames, you are employable. Specifically, these can wait:

1. **Hard real-time C++.** You will read a lot of C++ before you
   write any. The "make this 30 Hz node hit its deadline 99.9%
   of the time" work is usually owned by senior engineers.
   *Web-dev analogy: like assuming a junior frontend dev needs
   to optimize V8 hidden classes on day one. They don't.*
2. **Custom CUDA kernels.** TensorRT, torch.compile, and ONNX
   Runtime cover 95% of real-world inference acceleration. Hand-
   writing CUDA is a senior specialty.
3. **Embedded Linux kernel debugging.** Yes, the Jetson sometimes
   misbehaves at the driver level. No, you do not need to know
   how to write a kernel module in your first year. File the
   ticket, work around it.
4. **Proprietary calibration rigs.** Big shops have multi-axis
   robotic calibration stations. You will use them, not design
   them. Knowing OpenCV's `calibrateCamera` and Kalibr is enough
   for the first year.
5. **SLAM from scratch.** Almost nobody re-implements ORB-SLAM3.
   You learn to *use* it, tune it, and triage its failures.
   Building a new SLAM system is a multi-PhD effort.
6. **Custom silicon programming** (TPUs, NPUs, weird ASICs).
   Even at shops that use custom chips, there's an internal
   compiler team that handles the lowering. You write models;
   they get compiled.
7. **Sensor electrical / FPGA work.** If a camera's GMSL link
   is flaky, you escalate to the hardware team. Knowing that
   GMSL exists is enough; knowing how to scope-probe it is not.

What you DO need on day one: solid Python, willingness to read
C++, comfort with Linux, basic linear algebra (matrix multiply,
rotation matrices, quaternions), and the patience to debug
problems that span three sensors, two coordinate frames, and a
30-second rosbag.

---

## What's next to read

- `01-examples.md` — the broader landscape of who's building
  what.
- `02-learn.md` — the layered curriculum to build the
  skills above.
- `03-start.md` — a concrete 8-week ramp-up.
- `06-courses.md` — courses (both basics + project-driven) to take.
