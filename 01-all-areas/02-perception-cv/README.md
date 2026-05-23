# Perception & Computer Vision

> Written for a web developer who has never touched a robot. Every term
> is defined; analogies come from React / Node / TypeScript land.

## What is this subfield, in one paragraph?

A robot is blind until perception code turns its raw camera (and LiDAR,
and depth-sensor) pixels into something it can reason about: "there is
a red mug at coordinates (0.3, 0.1, 0.7), oriented 45 degrees off-axis,
sitting on a table 80 cm in front of me." **Perception is the
input-parsing layer** of every robot, the same way a JSON parser is the
input layer of an API server. The output is structured data: 3D
positions, object identities, surface normals, segmentation masks,
collision meshes.

The interesting part right now is that this whole layer is being
**rewritten by neural networks**. The classical algorithms (SIFT,
RANSAC, ORB-SLAM) still ship — the same way `grep` and `sed` still ship
inside container images even after every tool got a fancy GUI — but
they're being augmented or replaced by **foundation models** for vision.
That's the same pretrained-giant-model pattern that took over NLP with
GPT, applied to pixels.

## Why is this called "computer vision," and what's different about the robotics flavor?

Computer vision is a broad academic field that includes everything
from face filters on Instagram to medical imaging. **Robotics
perception** is a specific application: real-time (often 30-60 Hz),
geometry-aware (the answer must be a 3D pose, not just a label), and
deployed on edge hardware (a Jetson, not an AWS GPU). It cares about
things classical CV mostly ignores — sensor calibration, time
synchronization, multi-camera fusion, and operating safely under
adversarial real-world lighting.

The web-dev analogy: general computer vision is like front-end web
development for any-old-page. Robotics perception is like front-end
work for a real-time trading dashboard — same DOM, same React, but
suddenly latency is measured in milliseconds, frame-drops are bugs,
and "it works on my machine" doesn't fly because the machine is a
500W embedded GPU strapped to a moving robot.

## Why is this one of the top-3 picks?

- **Broadest customer base.** Every robot, drone, AR headset, AV, and
  industrial inspection rig needs perception. You can sell to
  warehouses, hospitals, farms, defense, automakers, and consumer-AR
  companies with overlapping skills. (Compare to "you build React
  components — every web team needs you" vs. "you build Solidity
  smart contracts — a much smaller pool.")
- **Easiest demos.** A laptop webcam + a phone is enough hardware for
  most portfolio projects. No expensive arms or simulators required to
  show off. Compare to backend work where you can demo a deployed API,
  vs. trying to demo a database optimization — perception lets you
  show pixels.
- **Three converging tailwinds.** (1) Every humanoid/AMR/AV/drone
  startup needs perception engineers; (2) Gaussian Splatting and
  learned 3D are mainstream now, opening new product surfaces (digital
  twins from a phone scan, automatic CAD-from-reality); (3) Vision
  foundation models (SAM 2, DINOv2, Depth-Anything v2) make
  once-PhD-grade problems tractable in days. The analogous web-era
  shift was when jQuery → React turned three months of cross-browser
  bug-fixing into a Friday afternoon.
- **Strong pay.** Robotics Software Engineer median is **$189k**
  nationally; perception specialists at AV/AR shops clear $200k base
  with $300k+ TC. Source: 2025 Robotics Salary Guide; levels.fyi.
- **Pulls from web-dev skills.** OpenCV in Python, FastAPI services
  for inference, Docker, Hugging Face — the operational stack maps
  directly onto things you've shipped before. The new vocabulary is
  small; the new math is finite; the new ecosystem (PyTorch, ROS2,
  CUDA) is well-documented.

## How to read this folder in 30 minutes

If you only have a coffee break:

1. **5 min** — finish this README (you're almost done).
2. **10 min** — skim `00-basics.md`, especially the three use-case
   sections (Waymo, Vision Pro, Pickle Robot). Treat them like reading
   three case studies on a tech blog.
3. **10 min** — skim `01-examples.md` to know the names of the
   companies, papers, and libraries. You don't need to remember them
   yet, just to recognize them when they show up.
4. **5 min** — glance at the "Week 1" entry in `03-start.md` to see
   what your first weekend would actually look like.

After that, the deeper reads (`02-learn.md`, `04-employers.md`,
`05-projects.md`, `06-courses.md`) are reference material — open them
when you need them, not in one sitting.

## Files in this folder

- [00-basics.md](00-basics.md) — what the field is, with three
  fully-developed deployed use cases (Waymo, Apple Vision Pro, Pickle
  Robot) and their full hardware + software stacks.
- [01-examples.md](01-examples.md) — production systems, landmark
  papers, and the open-source stack.
- [02-learn.md](02-learn.md) — layered curriculum from "what's a
  camera matrix" to "what's a Gaussian splat."
- [03-start.md](03-start.md) — a concrete 8-week ramp-up.
- [04-employers.md](04-employers.md) — who hires perception
  engineers, with comp bands.
- [05-projects.md](05-projects.md) — projects you can ship and bill
  for.
- [06-courses.md](06-courses.md) — curated online courses, books, and
  YouTube playlists, sequenced for a junior web dev.

## Web-dev to perception, conceptually

A quick map of "your existing mental model → the perception equivalent"
so the rest of this folder reads like translation rather than
revelation:

- **HTTP request / response** ↔ **frame in / structured-data out.**
  Each camera frame is the request; the perception node's output
  (bounding boxes + depth + pose) is the response. A perception
  pipeline is mostly a streaming service that processes one of these
  every 33 ms (30 Hz).
- **JSON parser** ↔ **detector / segmenter.** Takes a noisy blob
  (pixels), returns a typed structure (objects with labels and
  positions).
- **Database schema** ↔ **camera calibration file.** The schema
  everyone trusts as ground truth. If it's wrong, every downstream
  query (3D triangulation) is silently wrong.
- **TypeScript types** ↔ **coordinate frames (tf2).** Compile-time
  protection against mixing world-frame and camera-frame values. If
  you skip this discipline, your code "works" until the robot reaches
  for a coffee mug 90 degrees rotated from where it actually is.
- **Webpack / esbuild** ↔ **TensorRT.** The optimizer that turns the
  source artifact (a PyTorch model) into a smaller, faster, deployable
  one (an `.engine` file).
- **Docker container** ↔ **ROS2 node.** A self-contained process with
  declared inputs and outputs, designed to be composed with others
  over a message bus.
- **Redis pub/sub** ↔ **ROS2 topics.** Typed pub/sub channels that
  let independent processes share data without knowing about each
  other.
- **React component tree** ↔ **tf2 transform tree.** A hierarchy of
  named coordinate frames (world → robot_base → arm → end_effector
  → camera) — children inherit their parents' transform the way React
  children inherit context.
- **npm ecosystem** ↔ **Hugging Face + PyPI + ROS index.** Three
  package registries you'll mix daily. HF for foundation models, PyPI
  for everything Python, ROS index for sensor drivers and middleware.
- **CI/CD pipeline** ↔ **rosbag-replay regression tests.** Instead of
  running unit tests against mocked data, you replay a recorded log
  of real sensor data and assert your perception output hasn't
  regressed.

## Glossary (read this once before the other files)

- **Pixel** — the input. A camera frame is an `H x W x 3` tensor
  (height, width, RGB). Just an array, exactly like the `ImageData`
  you'd get from a `<canvas>`.
- **Intrinsics / extrinsics** — every camera has an "intrinsic" matrix
  (focal length, principal point — how it warps the world onto the
  sensor) and an "extrinsic" matrix (where it sits in the world).
  Together they convert pixels to 3D rays. Calibration is the act of
  measuring these. Think `process.env` for the camera — global config
  that the rest of the app reads and trusts.
- **Depth** — distance from the camera to each pixel, in meters.
  Either measured directly (RGB-D camera, LiDAR) or predicted by a
  neural net (monocular depth). Depth is a second image, same shape
  as the RGB, but each value is a meter measurement instead of a
  color.
- **RGB-D camera** — a camera that returns both color (RGB) and depth
  (D) per pixel. The Intel RealSense D435 is the canonical example,
  iPhone Pro models also count via their LiDAR scanner.
- **LiDAR** — Light Detection And Ranging. A sensor that shoots
  invisible laser beams and times their return to compute distance.
  Output is a "point cloud," not an image. Compare to depth cameras:
  LiDAR is longer-range, more accurate, less dense, and roughly 10x
  more expensive.
- **Point cloud** — an unordered list of 3D points (often millions),
  the typical output of a LiDAR scan. Think `Array<{x, y, z, color}>`.
  Unlike images, point clouds have no native grid — you can't iterate
  "the pixel at row 5, column 3."
- **Mesh** — a 3D surface made of connected triangles. Like the .obj
  files game engines load.
- **Voxel** — a 3D pixel; a small cube in space, marked "occupied" or
  "free." Used by occupancy networks (Tesla FSD's bet).
- **Pose** — the position + orientation of an object. 6 numbers (x, y,
  z, roll, pitch, yaw), often written as a 4x4 matrix. "6-DoF pose"
  (six degrees of freedom). Compare to a 2D position + heading, which
  is "3-DoF" and what most ground robots actually need.
- **SLAM** (Simultaneous Localization and Mapping) — the algorithm
  that figures out, in real time, "where am I" AND "what does the room
  around me look like," from a moving camera. It's both the GPS and
  the cartographer. The web-dev analogy is null because there isn't
  one — SLAM is genuinely a new concept.
- **VIO / VO** — Visual-Inertial Odometry / Visual Odometry. The
  "where am I" part of SLAM, without the map-building part. VIO adds
  IMU data to VO.
- **NeRF** (Neural Radiance Field) — a small neural network that
  represents a 3D scene as `(x, y, z, viewing direction) -> (color,
  density)`. You query it like a function to render new viewpoints.
  The "AlexNet moment" for 3D vision (2020).
- **Gaussian Splatting** — a newer (2023) representation that
  describes a scene as millions of fuzzy 3D blobs ("Gaussians"). Much
  faster to render than NeRF, and the current default for photoreal
  3D-from-photos. The analogy: NeRF is React server-rendered (slow,
  correct); Gaussian Splatting is React client-rendered with
  pre-rendered assets (fast, cheaper, what shipped).
- **Segmentation** — labeling every pixel with what it belongs to
  ("table", "mug", "background"). Like CSS selectors but for images.
  "Instance segmentation" separates two of the same class (mug-A,
  mug-B); "semantic segmentation" just labels the class.
- **Detection** — drawing a bounding box around each object of
  interest, with a class label. Cheaper than segmentation. YOLO and
  DETR are the canonical families.
- **6-DoF pose estimation** — given an image, find the precise 3D
  position and orientation of a known object. The core problem for
  robot grasping. FoundationPose is the modern default.
- **Feature** — a small distinctive patch of an image (a corner, an
  edge) that you can match across frames. The currency of classical
  CV. SIFT (1999), ORB, SuperPoint (learned, 2018), LightGlue (2023).
- **Bundle adjustment** — joint optimization of camera poses + 3D
  point positions so everything is geometrically consistent. The math
  engine inside every SLAM system.
- **Occupancy grid** — a 2D or 3D grid where each cell is "free,"
  "occupied," or "unknown." The map representation most ground robots
  navigate on. Tesla's "occupancy networks" are a learned 3D version.
- **BEV** (Bird's-Eye View) — a top-down rendering of the world,
  often the coordinate frame AV perception works in. "Project all the
  camera feeds + LiDAR into a single top-down map, then plan in
  that."
- **IoU** (Intersection over Union) — the standard metric for "how
  much do two bounding boxes overlap?" 0 = no overlap, 1 = identical.
- **mAP** (mean Average Precision) — the headline metric for
  detection benchmarks. Higher is better. You'll see "0.45 mAP on
  COCO" in every paper.
- **NMS** (Non-Maximum Suppression) — the post-processing step that
  deduplicates overlapping bounding boxes from a detector. Three lines
  of OpenCV, ubiquitous.
- **Sim2Real** — the gap between a model trained in simulation and
  its performance on the real robot. A perpetual headache; whole
  sub-fields exist to close it (domain randomization, domain
  adaptation).
- **TensorRT, ONNX, Triton** — NVIDIA's deployment stack. ONNX is the
  cross-framework model format (think a .gltf for ML models);
  TensorRT is the compiler that turns it into a fast `.engine`;
  Triton is the inference server that hosts it. The trio is
  "Webpack + minifier + nginx" for ML models.

## Common abbreviations cheatsheet

- **AV** — Autonomous Vehicle.
- **AMR** — Autonomous Mobile Robot (warehouse / hospital).
- **AGV** — Automated Guided Vehicle (older, follows a fixed track).
- **ADAS** — Advanced Driver-Assistance Systems (lane-keep, AEB).
- **EKF / UKF** — Extended / Unscented Kalman Filter; the workhorse
  state estimators.
- **IMU** — Inertial Measurement Unit (accelerometer + gyro).
- **GNSS / GPS** — Global Navigation Satellite System.
- **ToF** — Time-of-Flight (a depth-sensor type).
- **DoF** — Degrees of Freedom.
- **HD map** — High-Definition map (lane-level, used by AVs).
- **VPS** — Visual Positioning System (the GPS analog for indoor /
  urban-canyon AR).
- **PnP** — Perspective-n-Point (the math for "given 3D points and
  their pixel observations, solve camera pose").
- **SfM** — Structure from Motion (the offline cousin of SLAM).
