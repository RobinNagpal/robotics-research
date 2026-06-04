# 01 — How 6-DoF pose estimation models work

> **Goal of this page.** Open the box: what exactly goes in, what comes
> out, how the model arrives at a pose, how it is trained, and what it
> costs to run. Plain language, no maths. Builds on
> [`00-introduction.md`](00-introduction.md).

## Inputs and outputs, precisely

**Inputs**

- **An RGB image** — a normal colour photo from the camera (**RGB** =
  **red-green-blue**, the three colour channels). Always required.
- **A depth image** (usually) — a second picture where every pixel holds
  *how far away* that point is. Colour + depth together is **RGB-D**
  (**red-green-blue-plus-depth**); see
  [`00-introduction.md`](00-introduction.md). Most accurate methods want
  it.
- **A 3D CAD model** (for *model-based* methods) — a precise 3D drawing
  of the object, stored as a *mesh* file (a surface built from many small
  triangles). **CAD** = **computer-aided design**.
- **An initial detection box or mask** (often) — a rough hint of *where*
  in the image the object is, supplied by a detection model run just
  before (see
  [`../03-perception-vision-models/00-introduction.md`](../03-perception-vision-models/00-introduction.md)).
  A **mask** is a per-pixel outline saying "these pixels are the object."

**Output: a pose**

The output is a **pose** — the object's position *and* orientation. You
will see it written in three interchangeable forms; they all carry the
same information.

- **A 4x4 transform matrix.** A grid of 16 numbers. Read it as a single
  instruction that "transforms" a point from the object's own coordinates
  into the camera's coordinates — it bundles the three position numbers
  and the three orientation numbers into one tidy block. The top-left 3x3
  corner holds the rotation; the right-hand column holds the position
  (often in metres); the bottom row is just padding (`0 0 0 1`). This is
  the form robot software passes around most.

  ```text
  [ r r r  x ]   r = rotation (3x3 corner)   x,y,z = position
  [ r r r  y ]
  [ r r r  z ]
  [ 0 0 0  1 ]   <- padding row, always 0 0 0 1
  ```

- **A quaternion + position.** A **quaternion** is just four numbers that
  encode an orientation. It looks odd but is popular because it never
  "jams" the way other angle formats can, and is smooth to interpolate.
  Pair it with three position numbers and you have the full pose.
- **Euler angles + position.** **Euler angles** are the intuitive form:
  three rotation amounts, often called **roll, pitch, yaw** (tilt
  side-to-side, tilt front-to-back, turn left-right). Easy for humans to
  picture; paired with three position numbers, again the full pose.

Software converts freely between these, so which one a model prints is a
detail, not a deep choice.

## How a pose estimator actually finds the pose

The dominant idea is **render-and-compare** (also called *refinement*).
In plain language:

1. **Guess** a pose for the object.
2. **Render** it — draw the object's CAD model on a virtual screen *as if*
   it were sitting at that guessed pose. ("Render" just means "draw the
   3D model into a 2D picture," the same thing a video game does.)
3. **Compare** that drawing against what the real camera sees. Do the
   edges line up? Does the depth match?
4. **Adjust** the guess to reduce the mismatch, and repeat.

After a few rounds the rendered object snaps into alignment with the real
one, and the pose that produced that alignment is the answer. Model-free
methods use the same compare-and-adjust loop but build their notion of
the object's shape from reference images instead of a CAD file.

```text
  guess pose ─► render the model ─► compare with camera image
       ▲                                      │
       └────────── adjust to reduce mismatch ─┘   (repeat a few times)
```

### The role of depth

Depth is what makes the position numbers trustworthy. From a flat RGB
photo alone, a small-and-close object and a large-and-far object can look
identical — the image cannot tell you the true distance. Depth pins the
distance down directly, so the "compare" step above can check not just
"do the outlines match?" but "is every surface point the right distance
away?" That extra check is why RGB-D methods are markedly more accurate
than RGB-only ones.

### Single-shot versus tracking

- **Single-shot** — estimate the pose fresh from one frame, no history.
  Robust and simple, but it redoes all the work every time.
- **Tracking** — once you have a pose in one video frame, *follow* the
  object across the next frames by nudging the previous pose to fit the
  new image. Far cheaper per frame and smoother, because each frame only
  needs a small adjustment, not a fresh search. The catch: if the object
  is lost (fully hidden, or moves too fast), tracking must *re-initialise*
  with a fresh single-shot estimate. The best modern models
  ([`02-top-three-models.md`](02-top-three-models.md)) do both.

## How a pose estimator is trained

The hard part of training is getting **ground-truth** poses — the known,
correct answer for each training image. Measuring true 6-DoF poses by
hand for thousands of real photos is painful, so the field leans heavily
on **synthetic data**.

**Synthetic data** means training images that are *generated by a
computer* rather than photographed. Because a CAD model can be dropped
into a simulated scene at a pose *you choose*, the correct answer is
known for free, and you can churn out millions of varied images
(different lighting, backgrounds, clutter, viewpoints) cheaply. The
trick that makes this work is **domain randomisation** — wildly varying
the synthetic appearance so the model learns to ignore surface
differences and focus on shape, which helps it transfer to real photos.

In short: render the object at random known poses → train the model to
recover those poses → it generalises to real RGB-D input.

## What it costs to run (inference)

- **Speed** — varies a lot by method. A lightweight RGB-only model can
  run at video rates (tens of frames per second) on a modest GPU. A
  heavy render-and-compare model doing a fresh single-shot estimate may
  take a fraction of a second to ~1 second per object; in *tracking*
  mode the same model is much faster per frame. (All figures approximate
  and drift — re-check against the specific model and hardware.)
- **Hardware** — the strong modern models want an NVIDIA GPU; the heavier
  ones expect a few gigabytes of GPU memory and benefit from a desktop
  card. Lightweight RGB-only models can run on an embedded board such as
  an NVIDIA **Jetson**. See
  [`../01-basics/03-running-models-hardware-and-tools.md`](../01-basics/03-running-models-hardware-and-tools.md).
- **A depth camera** is itself part of the "cost" — budget for an RGB-D
  sensor unless you have chosen an RGB-only method.

## Limitations and failure modes

- **Symmetric or textureless objects** — a plain ball, a smooth
  cylinder, a featureless box looks the same from many angles, so its
  orientation is *genuinely* ambiguous; the model cannot recover what the
  image does not contain.
- **Occlusion** — when the object is partly hidden behind something else,
  there is less evidence to fit, and the pose degrades.
- **Depth dependence** — accuracy usually drops without depth, and depth
  cameras themselves struggle with shiny, transparent, or very dark
  surfaces (they return noisy or missing distance readings).
- **CAD-model burden** — model-based accuracy assumes you actually have a
  good 3D model of each object.
- **Reliance on the detection step** — a bad initial box or mask can send
  the refinement loop off to the wrong place.

## Key terms used on this page

- **Pose** — an object's position *and* orientation, six numbers total.
- **Transform matrix (4x4)** — one tidy grid encoding the whole pose.
- **Quaternion** — four numbers encoding an orientation.
- **Euler angles (roll, pitch, yaw)** — the intuitive three-rotation form.
- **Render** — draw a 3D model into a 2D picture.
- **Render-and-compare** — guess a pose, draw the model, compare with the
  camera, adjust, repeat.
- **Mask** — a per-pixel outline of which pixels are the object.
- **Synthetic data** — computer-generated training images with known
  correct answers.

## See also

- The three best-known models, with runnable-shaped code:
  [`02-top-three-models.md`](02-top-three-models.md).
- What this model type is and when to use it:
  [`00-introduction.md`](00-introduction.md).
- The step after a pose is known (grasping):
  [`../05-grasp-generation-models/00-introduction.md`](../05-grasp-generation-models/00-introduction.md).
