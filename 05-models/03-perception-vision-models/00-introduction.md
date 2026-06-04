# 00 — Perception & vision models: introduction

> **Job of this model type:** look at a camera image and answer "what
> objects are in this picture, and where are they?" — drawing a box
> around each object, or tracing its exact outline. These models
> *describe the present*; they do **not** decide what the robot should do.
>
> Part of [`../`](../README.md). New to model vocabulary? Read
> [`../01-basics/00-what-is-a-model.md`](../01-basics/00-what-is-a-model.md)
> first.

## What a perception / vision model is

A **perception model** (also called a **vision model** or **computer
vision model**) takes one image and finds the objects in it. Give it a
photo of a kitchen counter and it will tell you "there is a mug here, a
bottle there, a sponge over there," and mark each one on the image.

The word **computer vision** just means "getting a computer to extract
useful information from images." A perception model is the modern,
learned way to do that (a learned function, in the sense of
[`../01-basics/00-what-is-a-model.md`](../01-basics/00-what-is-a-model.md)),
as opposed to hand-written pixel rules.

These models come in two main flavours, and the difference matters:

- **Object detection** — draws a **bounding box** (a rectangle) around
  each object and labels it: "mug, 0.94 confidence." Fast and cheap.
  It tells you roughly *where* an object is, not its precise shape.
- **Image segmentation** — produces a **mask**: it marks the *exact
  pixels* that belong to each object, tracing its outline precisely.
  More work, but you get the true shape, not just a rectangle.

A picture is worth a paragraph:

```text
  detection:                     segmentation:
  ┌───────────┐                  ┌───────────┐
  │  ┌─────┐  │                  │   ▟▆▆▆▙    │
  │  │ mug │  │  box around       │  ▟█████▙   │  pixels that
  │  └─────┘  │  the object       │  ▜█████▛   │  ARE the object
  └───────────┘                  └───────────┘
```

## Why these models exist

Almost every robot task starts with the same question: *what is in front
of me, and where?* Before a robot can pick up a mug, something has to
find the mug in the camera image. Writing that "find the mug" rule by
hand is hopeless — mugs come in many shapes, colours, and lighting (the
exact trap described in
[`../01-basics/00-what-is-a-model.md`](../01-basics/00-what-is-a-model.md)).
A perception model learns it from thousands of labelled example images
instead.

## Where it sits in the robot pipeline

Perception is the **first stage** of the classic robot pipeline. It does
not move the robot; it hands clean information to the stages that do:

```text
 camera image
      │
      ▼
 [ PERCEPTION ]  ← you are here: find & outline objects
      │   "there is a mug, here is its box / mask"
      ▼
 [ POSE ESTIMATION ]  ← exactly how the mug is positioned & rotated
      │
      ▼
 [ GRASPING ]  ← where to put the gripper fingers
      │
      ▼
 [ MOTION / ACTION ]  ← actually move
```

- Detection or segmentation **crops the scene down** to "just the mug,"
  which is what
  [`../04-pose-estimation-models/00-introduction.md`](../04-pose-estimation-models/00-introduction.md)
  needs to work out the object's full 3-D position and rotation.
- That pose then feeds
  [`../05-grasp-generation-models/00-introduction.md`](../05-grasp-generation-models/00-introduction.md),
  which decides where to grip.

A **Vision-Language-Action model**
([`../02-vision-language-action-models/00-introduction.md`](../02-vision-language-action-models/00-introduction.md))
folds all of these stages into one network — but the pipeline approach,
with a dedicated perception model out front, is simpler to build, debug,
and trust, which is why this repository reaches for it first.

## What it is good at, and what it is not

**Strengths**

- **Fast and mature**: detection models run in real time (many frames
  per second) on modest hardware, including small on-robot computers.
- **Well understood**: decades of research, huge labelled datasets, and
  off-the-shelf models you can use without training your own.
- **General**: a single model can recognise dozens or hundreds of
  everyday object categories out of the box.

**Weaknesses**

- **2-D only**: a box or mask lives in the flat image. It tells you
  *where in the picture*, not *how far away* or *which way it is facing*
  — that is the job of pose estimation, not perception.
- **Fixed vocabulary (often)**: a standard detector only knows the
  categories it was trained on. Ask for "the antique sugar bowl" and it
  will not have a label for it (open-vocabulary detectors, explained in
  [`01-working.md`](01-working.md), relax this).
- **Confident mistakes**: odd lighting, clutter, or an unusual object can
  produce a wrong label with a high confidence score.

## When to reach for one

Reach for a perception model whenever a downstream step needs to know
*what is in the image and where* — which is almost always the very first
thing a manipulation or navigation robot must figure out. Use plain
**detection** when a rough rectangle is enough (counting items, "is the
shelf empty?"); use **segmentation** when you need the true outline (for
example, to cleanly separate two touching objects before grasping).

This repository treats perception as a foundational, build-it-first
layer — see the field write-up in
[`../../01-all-areas/02-perception-cv/README.md`](../../01-all-areas/02-perception-cv/README.md).

## See also

- How these models work inside (inputs, outputs, training, cost):
  [`01-working.md`](01-working.md).
- The three most famous perception models, with code:
  [`02-top-three-models.md`](02-top-three-models.md).
- The map of all model families:
  [`../01-basics/01-types-of-models-map.md`](../01-basics/01-types-of-models-map.md).
- A hands-on perception exercise in this repo's autosampler project:
  [`../../04-hplc-autosampler/02-hello-worlds/04-see-the-tray.md`](../../04-hplc-autosampler/02-hello-worlds/04-see-the-tray.md).
