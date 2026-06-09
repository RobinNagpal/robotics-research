# 00 — 6-DoF pose estimation models: introduction

> **Job of this model type:** given a camera view of an object, work out
> *exactly where it is and which way it is turned* in 3D space — its full
> position and orientation — so the robot can reach out and grip it.
>
> Part of [`../`](../README.md). New to model vocabulary? Read
> [`../01-basics/`](../01-basics/01-types-of-models-map.md) first.

## What 6-DoF pose estimation is

"**6-DoF**" is read "**six degrees of freedom**." It means six numbers:

- **three for position** — left-right, forward-back, up-down — *where*
  the object is, and
- **three for orientation** — the three ways a rigid thing can be
  rotated — *which way it is turned.*

Together those six numbers pin an object down completely in space. A
**6-DoF pose estimation model** looks at a picture (and usually a depth
reading — explained below) and outputs that **pose**: position plus
orientation, measured relative to the camera.

This is the perception step that comes *after* "what objects are here?"
and *before* "where do I grip?" It is the difference between knowing a
mug is somewhere in the frame and knowing the mug is *12 cm forward, 3 cm
left, 5 cm down, with its handle pointing at 30 degrees to the right.*
Only the second is enough to plan a grip.

## How this differs from plain object detection

A plain **detection** model (the
[`perception / vision`](../03-perception-vision-models/00-introduction.md)
family) draws a **box** around the object in the flat image and labels
it: "mug, here." That box lives in the 2D picture. It tells you *roughly
where to look*, not *where the object actually is in the room* or *how it
is oriented.*

| Question | Detection | 6-DoF pose estimation |
|---|---|---|
| What is it? | Yes (a label) | Often assumed already known |
| Where, in the flat image? | Yes (a 2D box) | Goes further |
| Where, in real 3D space? | No | Yes (position) |
| Which way is it turned? | No | Yes (orientation) |
| Bottom line | "There is a mug, roughly there" | "The mug is *exactly here*, turned *this way*" |

A robot hand needs the full 3D answer. You cannot close a gripper around
a 2D box.

## The pose: six numbers relative to the camera

The pose is always measured **relative to something** — almost always
the camera. Think of the camera as the origin of a tape measure. The
pose says, in effect: "starting from the camera, go forward this far,
right this far, down this far, then rotate the object by this much around
each of three axes." [`01-working.md`](01-working.md) shows the exact
forms these numbers take (a transform matrix, a quaternion, Euler
angles) and explains each in plain terms.

## Two inputs you will keep meeting

Two terms come up constantly, so define them once here:

- **Depth camera / RGB-D.** A normal colour camera gives **RGB** —
  **red-green-blue**, the three colour channels of an ordinary photo. A
  **depth camera** adds a fourth channel: for every pixel, *how far away*
  that point is from the camera. The pair together is called **RGB-D**
  (**red-green-blue-plus-depth**). Depth turns a flat photo into a cloud
  of 3D points, which makes finding an object's true 3D position far
  easier. Common depth cameras include the Intel RealSense and Microsoft
  Azure Kinect families.
- **CAD model.** **CAD** is **computer-aided design**. A **CAD model** is
  a precise 3D drawing of an object's shape — the kind an engineer makes
  before manufacturing it, often stored as a `.obj`, `.stl`, or `.ply`
  *mesh* file (a "mesh" is a surface built from many small triangles). If
  you have the object's CAD model, a pose estimator can *render* (draw) it
  at a guessed pose and check whether the drawing lines up with the
  camera image — the core trick explained in
  [`01-working.md`](01-working.md).

## Model-based versus model-free

Pose estimators split into two camps by *whether they need the object's
3D model in advance*:

- **Model-based** — you give it the object's **CAD model** ahead of time.
  Knowing the exact shape makes the pose much easier and more accurate.
  Good when you handle a fixed, known set of products.
- **Model-free** — no CAD model needed. The model figures out a usable
  pose from the images alone (sometimes from a few reference photos of
  the object). More flexible for novel objects, usually a bit less
  precise. The newest models (see
  [`02-top-three-models.md`](02-top-three-models.md)) can work *either*
  way.

For a grocery-shelf robot that handles a known catalogue of products,
model-based is the natural default; model-free is the fallback for items
you have not pre-scanned.

## Where it sits in the pipeline

```text
 [ detection ] ──► [ 6-DoF pose estimation ] ──► [ grasp generation ] ──► motion
   "a mug is          "the mug is exactly           "grip the handle        the arm
    over there"        here, turned this way"        at this angle"          moves
```

Pose estimation is the **bridge between detection and grasping**.
Detection narrows the camera down to the object; pose estimation locks in
its precise 3D placement; [`grasp generation`](../05-grasp-generation-models/00-introduction.md)
then decides where on it to grip.

## What it is good at, and what it is not

**Strengths**

- **Precision** — gives the exact 3D placement a robot hand needs, which
  detection cannot.
- **Reuse** — one pose per object feeds straight into motion planning and
  grasping.
- **Maturity** — for *known* objects with a CAD model, the methods are
  well-proven and reliable.

**Weaknesses**

- **Often needs depth** — best results usually want an RGB-D camera, not
  just a phone photo.
- **Symmetric and textureless objects are hard** — a plain ball or a
  smooth cylinder looks the same from many angles, so its orientation is
  genuinely ambiguous.
- **Occlusion hurts** — if the object is half-hidden, the pose gets
  shaky.
- **CAD models cost effort** — model-based methods need a 3D model of
  each object, which someone has to make or scan.

(See [`01-working.md`](01-working.md) for why each of these is true.)

## When to reach for a pose estimation model

Reach for one whenever the robot must **physically interact** with a
specific rigid object — pick it, place it, insert it — and a 2D box is
not enough. If you only need to *count* objects or *check* that something
is present, plain detection is cheaper and simpler.

This repository's "keep it simple" framing applies: for known products
with known shapes, start with a **model-based** estimator and a CAD
model; defer model-free, novel-object handling until you actually need
it.

## See also

- How a pose estimator works inside: [`01-working.md`](01-working.md).
- The three best-known models, with code:
  [`02-top-three-models.md`](02-top-three-models.md).
- The step before this one (detection):
  [`../03-perception-vision-models/00-introduction.md`](../03-perception-vision-models/00-introduction.md).
- The step after (grasping):
  [`../05-grasp-generation-models/00-introduction.md`](../05-grasp-generation-models/00-introduction.md).
- The wider perception field write-up:
  [`../../01-all-areas/02-perception-cv/README.md`](../../01-all-areas/02-perception-cv/README.md).
