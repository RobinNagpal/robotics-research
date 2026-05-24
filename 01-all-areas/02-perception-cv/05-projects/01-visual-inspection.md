# Project 1 — Automated visual defect inspection service

> The simplest of the three. A 2D problem: image in, "good / bad" out.
> No 3D geometry, no robot, no camera calibration. If you only build
> one project to show a customer, build this one.

**Timeline: 3-4 weeks** (1 week to learn the tools, 1-2 weeks to build
the pipeline, ~1 week to package and polish a demo).

---

## 1. Problem Statement

Small and mid-size manufacturers — PCB assembly shops, food packers,
plastic-molding lines, textile mills, metal-parts suppliers — have to
check every product for defects. Today they pick one of three bad
options:

- **A human eyeballs each part.** Slow, inconsistent, tired by the
  afternoon, and realistically catches ~80% of defects.
- **A machine-vision system from Cognex or Keyence.** Works well, but
  costs $30-80k plus weeks of integration, and has to be
  re-programmed by a specialist whenever the product changes.
- **Nothing.** They ship defects and eat the cost in returns,
  warranty claims, and lost customers.

These companies have **no machine-learning staff**. What they *do*
have is a hard drive full of photos of good parts, and a smaller pile
of photos of bad ones. They want a system that watches the line and
flags the bad parts — without hiring a vision PhD.

The money math is already on your side. A defect caught on the line
costs $X to scrap. The same defect shipped to a customer costs
**10-100× more** (recall, returns, warranty, reputation). The factory
manager doesn't need convincing that catching defects is worth money —
they just don't have the tool.

**The key idea you're selling: anomaly detection.** You might assume
you'd train the model on every kind of defect. You can't — defects are
rare, varied, and you'll never have enough examples of each. So you
flip it around: you teach the model what a **good** part looks like,
using the thousands of good images the factory already has, and the
model flags anything that *deviates* from good. This is what makes the
project tractable: you only need lots of "good" images (easy to get)
and few or even zero "bad" ones.

---

## 2. Why this is unique, demo-able, and sellable

**Demo-able — this is the strongest selling point.** You can train on
the customer's *own* images and, in the same meeting, show the system
catching real defects they recognize. Nothing closes a deal like
holding up a scratched part and showing the model's heatmap lighting
up exactly where the scratch is. The entire demo is a laptop plus
their image folder — no hardware to ship, no robot to set up.

**Unique — you sit in a gap nobody else fills.** The off-the-shelf
choices are a $50k hardware system on one side, or a generic cloud
vision API (never trained on *their* parts) on the other. You're in
the middle: trained on their data, deployed on *their* line PC, at one
tenth the price of the hardware option.

**Sellable — the buyer has clean ROI math.** The quality manager is
measured on "escape rate" (defects that reach the customer). You give
them a number that maps straight to their bonus: *"catches 94 of every
100 defects, false-alarms 3 times per 1000 good parts."* It's pure
software, runs on hardware they already own, and the re-training work
(new products, new defect types) is recurring revenue.

It's also the **lowest-risk project to start with**: a 2D
image-in/label-out problem with no 3D math, no robot integration, and
no calibration. You can ship it solo in a month.

---

## 3. Technologies to learn to get started

If you already know Python and web development, the genuinely new
material here is small — about 3-5 days of focused study before you're
productive.

**Image basics (1 day).**
- Loading, resizing, and normalizing images with **OpenCV** and
  **NumPy**. Internalize that an image is just an `H × W × 3` array of
  pixel values (height, width, 3 color channels).

**The anomaly-detection concept (1 day).**
- One-class learning: train only on "good" examples; at inference,
  score how far a new image is from "good." Understand why this beats
  trying to enumerate every defect type.

**The core library — `anomalib` (2-3 days).**
- `anomalib` is an open-source library (MIT license) with ready-made
  implementations of the standard models: **PatchCore**,
  **EfficientAD**, **PaDiM**. Learn to point it at your image folder,
  train, and read the anomaly heatmap it outputs. A first working
  model is a weekend's work.
- **DINOv2 embeddings + nearest-neighbor** as a strong baseline: a
  pretrained vision model turns each image into a vector ("embedding");
  bad images land far from the tight cluster of good vectors. At this
  data scale it often beats more complex supervised approaches.

**Evaluation vocabulary (1 day — do not skip).**
- **Precision** and **recall**, the trade-off between them, and how to
  pick a decision threshold. This is the one thing you *must* be able
  to explain in dollars to a non-technical buyer. Build a single slide
  that maps precision/recall onto scrap cost vs. escape cost and reuse
  it in every pitch.

**Deployment (you may already know most of this).**
- Export the trained model to **ONNX** (and optionally **OpenVINO** or
  **TensorRT** for speed on the customer's hardware).
- Wrap it in a **FastAPI** endpoint and package it as a **Docker**
  image the customer drops onto their line PC.
- A small **React** upload UI for sending images and viewing results,
  plus **Stripe** for billing — standard web work.

**Hardware needed:** none special to start. A laptop trains the
baseline models. The customer runs the final Docker container on their
existing line PC.
