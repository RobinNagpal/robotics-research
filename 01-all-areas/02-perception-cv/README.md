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
RANSAC, ORB-SLAM) still ship, but they're being augmented or replaced
by **foundation models** for vision — the same kind of pretrained
giant-model pattern that took over NLP with GPT.

## Why is this called "computer vision," and what's different about the robotics flavor?

Computer vision is a broader academic field that includes everything
from face filters on Instagram to medical imaging. **Robotics
perception** is a specific application: real-time (often 30-60 Hz),
geometry-aware (the answer must be a 3D pose, not just a label), and
deployed on edge hardware (a Jetson, not an AWS GPU). It cares about
things classical CV mostly ignores — sensor calibration, time
synchronization, multi-camera fusion, and operating safely under
adversarial real-world lighting.

## Why is this one of the top-3 picks?

- **Broadest customer base.** Every robot, drone, AR headset, AV, and
  industrial inspection rig needs perception. You can sell to
  warehouses, hospitals, farms, defense, automakers, and consumer-AR
  companies with overlapping skills.
- **Easiest demos.** A laptop webcam + a phone is enough hardware for
  most portfolio projects. No expensive arms or simulators required to
  show off.
- **Three converging tailwinds.** (1) Every humanoid/AMR/AV/drone
  startup needs perception engineers; (2) Gaussian Splatting and
  learned 3D are mainstream now, opening new product surfaces (digital
  twins from a phone scan, automatic CAD-from-reality); (3) Vision
  foundation models (SAM 2, DINOv2, Depth-Anything v2) make
  once-PhD-grade problems tractable in days.
- **Strong pay.** Robotics Software Engineer median is **$189k**
  nationally; perception specialists at AV/AR shops clear $200k base
  with $300k+ TC. Source: 2025 Robotics Salary Guide; levels.fyi.
- **Pulls from web-dev skills.** OpenCV in Python, FastAPI services
  for inference, Docker, Hugging Face — the operational stack maps
  directly onto things you've shipped before.

## Files in this folder

- [01-examples-of-work.md](01-examples-of-work.md) — production
  systems, landmark papers, and the open-source stack.
- [02-important-to-learn.md](02-important-to-learn.md) — layered
  curriculum from "what's a camera matrix" to "what's a Gaussian
  splat."
- [03-how-to-start.md](03-how-to-start.md) — a concrete 8-week ramp-up.
- [04-major-new-employers.md](04-major-new-employers.md) — who hires
  perception engineers, with comp bands.
- [05-projects-to-sell.md](05-projects-to-sell.md) — four projects you
  can ship and bill for.

## Glossary (read this once before the other files)

- **Pixel** — the input. A camera frame is an `H x W x 3` tensor
  (height, width, RGB). Just an array, exactly like the `ImageData`
  you'd get from a `<canvas>`.
- **Intrinsics / extrinsics** — every camera has an "intrinsic" matrix
  (focal length, principal point — how it warps the world onto the
  sensor) and an "extrinsic" matrix (where it sits in the world).
  Together they convert pixels to 3D rays. Calibration is the act of
  measuring these.
- **Depth** — distance from the camera to each pixel, in meters.
  Either measured directly (RGB-D camera, LiDAR) or predicted by a
  neural net (monocular depth).
- **Point cloud** — an unordered list of 3D points (often millions),
  the typical output of a LiDAR scan. Think `Array<{x, y, z, color}>`.
- **Mesh** — a 3D surface made of connected triangles. Like the .obj
  files game engines load.
- **Pose** — the position + orientation of an object. 6 numbers (x, y,
  z, roll, pitch, yaw), often written as a 4x4 matrix. "6-DoF pose."
- **SLAM** (Simultaneous Localization and Mapping) — the algorithm
  that figures out, in real time, "where am I" AND "what does the room
  around me look like," from a moving camera. It's both the GPS and
  the cartographer.
- **NeRF** (Neural Radiance Field) — a small neural network that
  represents a 3D scene as `(x, y, z, viewing direction) -> (color,
  density)`. You query it like a function to render new viewpoints.
- **Gaussian Splatting** — a newer (2023) representation that
  describes a scene as millions of fuzzy 3D blobs ("Gaussians"). Much
  faster to render than NeRF, and the current default for photoreal
  3D-from-photos.
- **Segmentation** — labeling every pixel with what it belongs to
  ("table", "mug", "background"). Like CSS selectors but for images.
- **6-DoF pose estimation** — given an image, find the precise 3D
  position and orientation of a known object. The core problem for
  robot grasping.
- **Feature** — a small distinctive patch of an image (a corner, an
  edge) that you can match across frames. The currency of classical
  CV.
- **Bundle adjustment** — joint optimization of camera poses + 3D
  point positions so everything is geometrically consistent. The math
  engine inside every SLAM system.
