# Four Projects You Can Build and Sell

Each scoped to 2-4 weeks of solo work, with a concrete buyer, and
reusing skills a web developer already has (FastAPI / Express, Docker,
GitHub Actions, Postgres, React). The perception-specific parts are
clearly flagged.

A note on pricing: ranges below are realistic for **2025-2026 in North
America / Western Europe**. Big robotics primes and AV teams pay the
high end; seed-stage robotics startups and manufacturing SMBs pay the
low end. Always quote a fixed-fee "discovery phase" first ($2-5k) to
de-risk both sides before quoting a full build.

---

## 1. Phone-scan -> robot-ready 3D environment (~4 weeks)

**What you're selling.** A web service: the customer walks around a
room with their phone (5 minutes), uploads the video, and receives
back a Gaussian splat + collision mesh + per-object semantic
segmentation, all packaged as a USD (Universal Scene Description) or
URDF file that loads directly into Isaac Sim or Gazebo.

**Why it works.** Every robotics startup needs digital twins of
customer sites (for sim2real training, for sales demos, for
sim-based validation). Hiring a 3D artist or sending an engineer
on-site costs $5-20k each time. You sell a $1-5k self-serve
alternative.

**Stack:**
- **iPhone capture** with Polycam, Scaniverse, or a custom
  ARKit/AVFoundation app.
- **COLMAP** or **glomap** for structure-from-motion (camera poses
  + sparse point cloud).
- **Nerfstudio + gsplat** for Gaussian splat training.
- **SAM 2** to project semantic masks across views, fused into the
  3D scene.
- **Open3D** to mesh-extract a collision proxy.
- **USD / URDF export** with the `usd-core` Python library and
  `pxr` from NVIDIA's USD SDK.
- React + FastAPI front-end with an S3-backed job queue (Celery /
  RQ). Stripe for billing.

**Pricing:** $1-5k per scene; or $500/mo subscription for unlimited
small scenes. Realistic ARR target after 6 months: $5-15k MRR.

**What you need first:** one happy reference customer. Hang out in
the Isaac Sim and LeRobot Discords, offer a free first scan in
exchange for a public testimonial.

---

## 2. 6-DoF pose-estimation API for industrial parts (~3 weeks)

**What you're selling.** A customer uploads a CAD model of a part
they need to pick (a fitting, a bracket, an SKU). Your service
returns a fine-tuned **FoundationPose** / **MegaPose** checkpoint +
a Dockerized REST endpoint that takes an RGB-D image and returns a
6-DoF pose for that part.

**Why it works.** Bin-picking integrators (Pickle, Kindred,
hundreds of system integrators worldwide) are constantly being
asked to add new SKUs. The "right" answer used to be a
multi-week PhD project per SKU. FoundationPose changed that.
Most integrators haven't internalized it yet — you sit in that
gap.

**Stack:**
- **FoundationPose** (NVIDIA, Apache 2.0) as the base model.
- A small **synthetic data pipeline** in BlenderProc or Isaac Sim
  Replicator to generate training images of the part in varied
  lighting / backgrounds / occlusions.
- **NVIDIA Triton Inference Server** or a simple FastAPI + ONNX
  Runtime endpoint for serving.
- **Docker image** as the deliverable.
- Optional React dashboard for the customer to upload CAD,
  monitor accuracy, and re-train.

**Pricing:** $2-10k setup per part + $0.01-0.10 per inference (or
a $500-2k/mo all-you-can-eat plan).

**Hardest part:** getting accuracy good enough on shiny / textureless
metal parts (the bane of vision-based pose estimation). Have a
mitigation ready: combine with a structured-light sensor or
fall-back tactile retry strategy.

---

## 3. Visual-inspection-as-a-service (~2-3 weeks)

**What you're selling.** A web UI where a small-to-mid manufacturer
uploads 50-100 "good" and 50-100 "bad" product images. Your service
trains an anomaly-detection model (PatchCore / EfficientAD / DINOv2
+ kNN) and ships back a Docker container with a REST endpoint that
classifies new images. The customer drops it onto their line PC.

**Why it works.** Visual QC departments at small-to-mid
manufacturers (PCB shops, food packers, fabric mills, parts
suppliers) pay well and have **zero ML staff**. Their existing
options are buying a $50k+ Cognex / Keyence system or doing nothing.
You undercut Cognex on price and beat "doing nothing" by miles.

**Stack:**
- **anomalib** (OpenVINO toolkit, MIT licensed) for the model zoo.
- Or **DINOv2 + nearest-neighbor on embeddings** as a baseline that
  often beats supervised approaches with limited data.
- **ONNX / TensorRT** export for deployment speed.
- Docker image with FastAPI inference endpoint.
- React upload UI; Stripe billing.

**Pricing:** $5-25k per defect class deployed, plus $200-1000/mo
support / re-training subscription. Pure software, recurring
revenue, no on-site work needed.

**Why this fits a web dev specifically.** Three of four layers
(upload UI, billing, Docker delivery) are exactly what you already
build. The ML piece is a 200-line `anomalib` config plus some
evaluation code.

---

## 4. Real-time SLAM benchmark + tuning service (~3 weeks)

**What you're selling.** Customer uploads a ROS bag (or any
video + IMU). Your service runs **ORB-SLAM3**, **VINS-Fusion**, and
**DROID-SLAM** with several parameter sets, evaluates each against
their ground-truth trajectory (if available) or against
self-consistency loop closures (if not), and returns a tuning
report with parameter recommendations and an accuracy comparison.

**Why it works.** Drone, AMR, and AR startups have engineers who
know perception well enough to tune one SLAM stack, but rarely
have the bandwidth to comparison-shop across the four big options.
You provide that "Sentry for SLAM" service — like a CI step that
catches drift / scale errors before customers do.

**Stack:**
- **evo** (Python eval tool) for trajectory comparison.
- Dockerized **ORB-SLAM3**, **VINS-Fusion**, **OpenVSLAM**, and
  **DROID-SLAM** images, all pinned.
- Parameter sweep harness (Ray Tune or even just a YAML matrix).
- **WeasyPrint** or **Puppeteer** for the PDF report.
- **GitHub Actions integration** so a PR can trigger a nightly run.

**Pricing:** $2-5k per benchmark report; $500-2k/mo for nightly CI
add-on. Pure software, no hardware coordination needed.

---

## How to pick which one to start with

- **Cheapest to start, fastest to revenue:** #3 (visual inspection).
  Pure SaaS, no hardware, customer pool is enormous (every small
  factory).
- **Most defensible long-term:** #2 (6-DoF pose API). Each customer's
  fine-tuned model and accuracy benchmarks are your moat.
- **Highest ceiling:** #1 (phone-scan to digital twin). If digital
  twins of customer sites become a default robotics workflow, this
  could be acquired by NVIDIA / Matterport / Polycam.
- **Easiest to charge premium for:** #4 (SLAM tuning). One report
  pays for a month of your time; harder pipeline to keep busy.
