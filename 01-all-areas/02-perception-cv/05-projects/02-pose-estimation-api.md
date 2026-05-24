# Project 2 — 6-DoF pose-estimation API for industrial parts

> Medium difficulty. Now you're in 3D: depth cameras, camera
> intrinsics, synthetic training data, and a live hardware demo. A
> clear step up from Project 1, but a foundation model does most of
> the heavy lifting.

**Timeline: 4-5 weeks** (1 week to learn 3D/RGB-D basics, ~1 week to
get the pose model running, 1-2 weeks for the synthetic-data and API
pipeline, ~1 week to polish a hardware demo).

---

## 1. Problem Statement

A robot arm that picks parts out of a bin has to know, for each part,
**exactly where it is and how it's rotated** in 3D space. That answer
is a **6-DoF pose**: 3 numbers for position (x, y, z) and 3 for
orientation (roll, pitch, yaw). Without the pose, the gripper has no
idea where to close.

The customers here are **bin-picking integrators** and factory
automation shops — the companies that install robot cells for
manufacturers. Every time their client introduces a new part (a new
"SKU"), someone has to make the vision system recognize that part and
output its pose. Historically this was a multi-week custom engineering
job *per part*, which is why integrators quietly pad **$15-50k of
"perception engineering"** into every cell quote to cover unknown
future parts.

Foundation models changed this. **FoundationPose** and **MegaPose**
can produce a 6-DoF pose from just a **CAD model** of the part plus a
single **RGB-D image** — often with little or no training. Most
integrators haven't internalized this yet, which is the opening.

**What you sell:** the customer uploads a CAD model (a STEP or STL
file). Your service generates synthetic training images from it,
configures/fine-tunes a pose model, and returns a **Docker endpoint**
that takes an RGB-D frame and returns the part's 6-DoF pose. You
collapse their unpredictable "$15-50k of future perception work" into
a fixed per-SKU fee with a turnaround SLA — so you become a *line item
in their proposal*, not a competitor.

**Term to define up front: RGB-D camera.** A camera (Intel RealSense,
Orbbec) that returns color *and* a per-pixel depth value (distance to
each point, in meters). The depth channel is what makes recovering a
3D pose from a single shot possible.

---

## 2. Why this is unique, demo-able, and sellable

**Demo-able.** Bring an Intel RealSense camera and a real (or
3D-printed) part to the meeting. Set the part on the table and show
the system drawing the 3D coordinate axes locked onto it as you pick
it up and rotate it. Watching the axes stay glued to the object as it
moves is visually unmistakable — even a non-technical buyer instantly
gets it.

**Unique.** Because integrators currently bury that perception cost in
every quote, a predictable per-SKU price with an SLA is something the
market doesn't offer. You're not competing with the integrator — you're
removing a risk from their bid, which makes you easy to say yes to.

**Sellable.** It's recurring by nature (new SKUs keep arriving), the
deliverable is concrete (a `docker pull` command), and you're riding a
capability — modern foundation-model pose estimation — that most of
the market hasn't caught up to yet. You can honestly tell them: *"I
add a new part to your bin-picker in 48 hours for a flat fee."*

This is harder than Project 1 because it adds 3D geometry, a depth
sensor, synthetic-data generation, and a hardware-in-the-loop demo —
but a pretrained foundation model carries most of the technical load.

---

## 3. Technologies to learn to get started

**3D and camera fundamentals (3-4 days).**
- **The pinhole camera model and intrinsics:** how pixels map to 3D
  rays via focal length and principal point. You don't need to derive
  the math — you need to understand what the numbers mean and how to
  read them off the camera.
- **RGB-D capture:** grabbing aligned color + depth frames from an
  Intel RealSense (`pyrealsense2`) or Orbbec camera.
- **The 6-DoF pose representation:** position + orientation, the 4×4
  transform matrix, and rotations as quaternions or matrices. Learn to
  *visualize* a pose as three colored axes drawn on the object.

**The pose model — FoundationPose / MegaPose (~1 week).**
- **FoundationPose** (NVIDIA, Apache 2.0) and/or **MegaPose** are the
  base models. Learn the model-based path: feed a CAD mesh plus an
  RGB-D frame, get a pose back. Budget about a week to get it running
  cleanly on one sample object.

**Synthetic data generation (3-4 days).**
- **BlenderProc** or **NVIDIA Isaac Sim Replicator** render thousands
  of labeled images of the CAD model under varied lighting and poses.
- **Domain randomization:** the basic idea that varying textures,
  lighting, and backgrounds in simulation makes the model generalize
  to the real part.
- **The sim-to-real gap:** understand why a model trained purely on
  synthetic images degrades on real ones, and learn the standard
  mitigation — collect 100-500 real images and fine-tune on them.

**Deployment.**
- **NVIDIA Triton Inference Server**, or **FastAPI + ONNX Runtime**,
  serving the model.
- **Docker** image as the deliverable.
- A **GPU** for inference — a Jetson AGX Orin for an edge demo, or a
  workstation GPU.
- Optional: a **React** dashboard for CAD upload and accuracy
  monitoring.

**One hard reality to learn early.** Shiny and textureless metal parts
are the classic failure case for vision-based pose — there's nothing
for the model to lock onto. Learn the mitigations (structured-light
sensor, a second camera view, or adding a fiducial marker) so you can
scope engagements honestly instead of promising what physics won't
allow.
