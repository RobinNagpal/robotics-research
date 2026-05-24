# Project 3 — Phone-scan to robot-ready 3D digital twin

> The most complex of the three. A full multi-stage 3D pipeline —
> capture, reconstruction, segmentation, mesh, export — wrapped in an
> async web service. The highest ceiling and the most failure modes.

**Timeline: 5-6 weeks** (2 weeks to learn the 3D reconstruction
stack, 2 weeks to build the pipeline end-to-end, 1-2 weeks for the web
service, export formats, and QA on real scans).

---

## 1. Problem Statement

Robotics teams — warehouse-robot startups, humanoid companies, AMR
(autonomous mobile robot) makers — constantly need a 3D model of a
customer's site. They use it to **train robots in simulation**
(so-called sim2real), to build **sales demos**, and to **validate** a
deployment before sending real hardware. Today they get that 3D model
one of two painful ways:

- **Fly an engineer to the site** with a scanner — expensive and slow.
- **Hand-author the environment in Blender** — days of work per room
  by someone who'd rather be doing robotics.

Consumer tools like **Matterport** and **Polycam** already make
good-looking 3D scans, but for *real estate*, not robotics. None of
them output what a robot simulator actually needs:

- a **collision mesh** (a simplified solid surface the physics engine
  uses so a simulated robot doesn't fall through the floor),
- **semantic labels** (this is a chair, that is a wall, this is the
  floor), and
- a **USD or URDF** file that loads directly into **Isaac Sim** or
  **Gazebo**, the two standard robot simulators.

**What you sell:** a web service. The customer walks a room with their
phone for about 5 minutes and uploads the video. Roughly 20 minutes
later they get back a photo-realistic 3D scene plus a collision mesh,
per-object segmentation, and a ready-to-load USD/URDF file.

**The pipeline stages, in plain terms:**
- **Structure from Motion (SfM):** from many overlapping photos,
  recover where the camera was for each shot and a sparse 3D point
  cloud of the scene.
- **Gaussian Splatting:** a 2023 method that represents a scene as
  millions of fuzzy 3D blobs. It renders photo-realistic 3D quickly
  and is the current default for turning photos into 3D.
- **Segmentation (SAM 2):** label every object/pixel so the twin knows
  what's a chair versus a wall versus the floor.
- **Collision mesh:** a simplified solid surface extracted for the
  physics engine.
- **USD / URDF:** the file formats the simulators read.

---

## 2. Why this is unique, demo-able, and sellable

**Demo-able.** Record a phone video of the meeting room you're sitting
in, and by the end of the call show that room loaded and navigable
inside Isaac Sim. "Your room is now in the simulator" is a striking
moment that makes the value obvious instantly.

**Unique.** Nobody targets *robotics-grade* capture. You're not
competing with Polycam (which serves real estate) — you're competing
with a roboticist hand-building a kitchen in Blender on a Saturday.
The collision mesh, semantic labels, and URDF/USD output are the moat;
the pretty visual is table stakes.

**Sellable.** Every robotics startup needs digital twins *repeatedly*,
and each one currently costs $5-20k of engineer or 3D-artist time.
Once a buyer sees that neither Matterport nor Polycam ships a URDF,
they'll happily pay a premium for a phone-to-simulator pipeline that
does.

This is the most complex project of the three: a multi-stage 3D
pipeline (capture → SfM → splat → segmentation → mesh → export), an
async job queue, and the largest number of ways things can go wrong.
Start it only after you're comfortable with the first two.

---

## 3. Technologies to learn to get started

**3D reconstruction stack (about 2 weeks — the bulk of the learning).**
- **Photogrammetry / SfM with COLMAP** (or the faster **glomap**): run
  it on a folder of video frames to get camera poses and a sparse
  point cloud. Budget 3-4 days to learn.
- **Gaussian Splatting via Nerfstudio + gsplat** (the `splatfacto`
  method): train a splat from the SfM output and export it. Understand
  at a high level how **NeRF** and Gaussian Splatting differ — you'll
  use splatting because it's faster.
- **SAM 2** (Meta) for segmentation, fused across multiple camera
  views so the labels are consistent in 3D rather than per-frame.
- **Open3D** for point-cloud and mesh processing, including extracting
  a simplified **collision-proxy mesh** from the dense reconstruction.

**Export formats (3-4 days).**
- **USD** via `usd-core` / NVIDIA's `pxr` library, and **URDF** if you
  add articulated parts (doors, drawers). Learn what **Isaac Sim** and
  **Gazebo** expect so the output loads without manual fixups.

**Capture (1-2 days).**
- Start with **Polycam** or **Scaniverse** on an iPhone for capture.
- Later, a custom **ARKit** (iOS) capture app gives you control over
  frame rate and lets you record camera-pose hints alongside the
  video.

**Web service and infrastructure (you likely know most of this).**
- A **React** upload UI, a **FastAPI** backend, an **S3**-backed
  **async job queue** (the pipeline takes minutes, so it can't be a
  synchronous request), completion notifications, and **Stripe** for
  billing.
- A **GPU** for splat training — a cloud GPU or a workstation.

**The operational skill that decides success.** Capture failures — bad
lighting, motion blur, reflective or glass surfaces, blank textureless
walls — are the number-one problem, and no amount of model tuning
fixes a bad capture. Learn to diagnose them, write a clear re-capture
instruction template for customers, and plan a human QA pass on every
delivery for at least your first ~20 scans.
