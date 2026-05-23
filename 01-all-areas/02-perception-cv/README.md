# Perception & Computer Vision

> Written for a web developer new to robotics. Every term is defined.

## What this field is

Perception turns raw sensor data (camera frames, depth maps, LiDAR
point clouds) into structured information a robot can act on: "there
is a red mug at (0.3, 0.1, 0.7), 80 cm in front of me, on a table."

It's the input layer of every robot — without it, the planner and
controller are blind.

The classical algorithms (SIFT, RANSAC, ORB-SLAM) still ship, but
foundation models (SAM 2, DINOv2, Depth-Anything v2, FoundationPose)
have replaced or augmented most of them since 2023.

## Robotics perception vs. general computer vision

Computer vision covers everything from Instagram filters to medical
imaging. Robotics perception is a specific application with extra
constraints:

- **Real-time.** 10-60 Hz, with sub-100 ms latency budgets.
- **Geometry-aware.** The output is a 3D pose, mesh, or trajectory —
  not just a class label.
- **Multi-sensor.** RGB + depth + IMU + LiDAR, time-synced and
  cross-calibrated.
- **Edge-deployed.** Inference runs on a Jetson or embedded GPU, not
  a cloud A100.
- **Safety-critical.** A misclassification can crash a car or topple
  a humanoid.

## Why this is one of the top-3 picks

- **Broadest customer base.** Every robot, drone, AV, AR headset, and
  inspection rig needs perception.
- **Cheap to get started.** A laptop webcam and a phone are enough
  for most portfolio projects.
- **Three tailwinds.** Humanoid/AV/drone startups are hiring; learned
  3D (Gaussian Splatting) opened new product surfaces; vision
  foundation models made once-PhD problems solvable in days.
- **Strong pay.** Robotics Software Engineer median is $189k (2025
  Robotics Salary Guide); perception specialists at AV/AR shops
  clear $300k+ TC.
- **Reuses web-dev skills.** Python, FastAPI, Docker, Hugging Face,
  CI/CD — most of the operational stack is familiar.

## How to read this folder in 30 minutes

1. Finish this README (5 min).
2. Skim `00-basics.md`, especially the three use cases (Waymo,
   Vision Pro, Pickle Robot) — 10 min.
3. Skim `01-examples.md` to recognize the company/paper/library
   names — 10 min.
4. Glance at Week 1 of `03-start.md` to see what your first weekend
   would look like — 5 min.

The deeper files (`02-learn.md`, `04-employers.md`, `05-projects.md`,
`06-courses.md`) are reference material — open them when you need
them.

## Files in this folder

- [00-basics.md](00-basics.md) — what the field is, with three
  deployed use cases (Waymo, Apple Vision Pro, Pickle Robot) and
  their full hardware + software stacks.
- [01-examples.md](01-examples.md) — production systems, landmark
  papers, and the open-source stack.
- [02-learn.md](02-learn.md) — layered curriculum from camera math
  to neural rendering.
- [03-start.md](03-start.md) — concrete 8-week ramp-up.
- [04-employers.md](04-employers.md) — who hires perception
  engineers, with comp bands.
- [05-projects.md](05-projects.md) — projects you can ship and bill
  for.
- [06-courses.md](06-courses.md) — curated online courses, books, and
  YouTube playlists.

## Glossary

- **Pixel** — one element of an `H × W × 3` image tensor.
- **Intrinsics / extrinsics** — the matrices that describe a
  camera's optical properties (intrinsics: focal length, principal
  point) and its position in the world (extrinsics). Together they
  convert pixels to 3D rays. "Calibration" is measuring these.
- **Depth** — distance from camera to each pixel, in meters. Measured
  directly (RGB-D camera, LiDAR) or predicted (monocular depth net).
- **RGB-D camera** — a camera that returns color + depth per pixel.
  Intel RealSense D435 is the canonical example.
- **LiDAR** — a laser-based depth sensor. Longer range than depth
  cameras, more accurate, less dense, ~10x more expensive.
- **Point cloud** — an unordered list of 3D points. The native output
  of LiDAR.
- **Mesh** — a 3D surface made of connected triangles.
- **Voxel** — a 3D pixel; a cube in space marked occupied or free.
- **Pose** — position + orientation. 6 numbers (x, y, z, roll, pitch,
  yaw), usually stored as a 4×4 matrix. "6-DoF pose."
- **SLAM** (Simultaneous Localization and Mapping) — figuring out
  "where am I" and "what does the room look like" at the same time,
  from a moving camera.
- **VIO / VO** — Visual-Inertial Odometry / Visual Odometry. The
  "where am I" part of SLAM, without building a reusable map.
- **NeRF** (Neural Radiance Field) — a small neural network that
  represents a 3D scene. Slow to render. The 2020 breakthrough.
- **Gaussian Splatting** — a 2023 alternative: a scene as millions of
  fuzzy 3D blobs. Much faster than NeRF; the current default for
  photoreal 3D-from-photos.
- **Segmentation** — labeling every pixel with what it belongs to.
  "Instance segmentation" separates two of the same class; "semantic
  segmentation" just labels the class.
- **Detection** — bounding box + class per object. Cheaper than
  segmentation. YOLO and DETR are the main families.
- **6-DoF pose estimation** — find a known object's 3D position and
  orientation in an image. Core problem for grasping. FoundationPose
  is the modern default.
- **Feature** — a small distinctive image patch you can match across
  frames. SIFT (1999), ORB, SuperPoint (2018), LightGlue (2023).
- **Bundle adjustment** — joint optimization of camera poses and 3D
  points to minimize reprojection error. The math engine inside
  every SLAM system.
- **Occupancy grid** — a 2D/3D grid where each cell is free,
  occupied, or unknown. Standard map representation for navigation.
- **BEV** (Bird's-Eye View) — top-down rendering of the world. The
  coordinate frame most AV perception works in.
- **IoU** — Intersection over Union. Overlap metric for two bounding
  boxes. 0 = no overlap, 1 = identical.
- **mAP** — mean Average Precision. Headline detection benchmark
  metric.
- **NMS** — Non-Maximum Suppression. Deduplicates overlapping
  detections.
- **Sim2Real** — the gap between simulation-trained models and
  real-robot performance.
- **TensorRT / ONNX / Triton** — NVIDIA's deployment stack. ONNX is
  the cross-framework model format; TensorRT compiles it to a fast
  `.engine`; Triton serves it.
- **ROS2 topic** — a typed pub/sub channel between robot processes.

## Common abbreviations

- **AV** — Autonomous Vehicle.
- **AMR** — Autonomous Mobile Robot.
- **ADAS** — Advanced Driver-Assistance Systems.
- **EKF / UKF** — Extended / Unscented Kalman Filter.
- **IMU** — Inertial Measurement Unit (accelerometer + gyro).
- **GNSS / GPS** — Global Navigation Satellite System.
- **ToF** — Time-of-Flight (a depth-sensor type).
- **DoF** — Degrees of Freedom.
- **HD map** — High-Definition map (lane-level, used by AVs).
- **VPS** — Visual Positioning System (the indoor / urban-canyon
  equivalent of GPS).
- **PnP** — Perspective-n-Point. The "given 3D points and their
  pixel observations, solve camera pose" problem.
- **SfM** — Structure from Motion. The offline cousin of SLAM.
