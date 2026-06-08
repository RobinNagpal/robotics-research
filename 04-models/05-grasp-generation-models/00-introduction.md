# 00 — Grasp generation models: introduction

> **Job of this model type:** look at an object (usually as a depth
> picture or a 3D point cloud), and propose *where* on it a gripper
> should close and *at what angle* — one or many candidate grips, each
> with a quality score. It does not move the robot; it hands those
> proposals to a motion planner to execute.
>
> Part of [`../`](../README.md). New to model vocabulary? Read
> [`../01-basics/01-types-of-models-map.md`](../01-basics/01-types-of-models-map.md)
> first.

## What a grasp generation model is

Once a robot knows an object is there and roughly where it is, it faces
a surprisingly hard question: **how do I actually pick this up?** A mug
can be grabbed by the rim, the body, or the handle; a screwdriver wants
to be held by the shaft, not the tip. A **grasp generation model**
answers exactly this. Given a view of the scene, it outputs **grasp
proposals** — concrete poses for the gripper that, if the robot moves
there and closes, should result in a stable hold.

It is a **perception** model in the map sense (see
[`../01-basics/01-types-of-models-map.md`](../01-basics/01-types-of-models-map.md)):
it describes a *possibility about the world* ("a good grip exists
here") rather than commanding the motors. The command comes later, from
the motion planner.

## The input: a depth image or a point cloud

Grasping needs **shape**, not just colour, so the input is almost
always 3D:

- **Depth image** — like an ordinary photo, but each pixel stores *how
  far away* that point is from the camera instead of its colour.
  Produced by a **depth camera** (also called an **RGB-D camera**: it
  gives Red-Green-Blue colour *plus* Depth). The depth tells the model
  the object's surface shape.
- **Point cloud** — a **set of 3D dots** sampled off the surfaces the
  camera can see. Each dot is just three numbers: its left-right,
  forward-back, and up-down position in space. Thousands of these dots
  together trace out the visible shape of the scene, like a sculpture
  made of pinpricks. A point cloud is usually computed *from* a depth
  image. Many grasp models prefer it because it is a direct,
  camera-angle-free description of geometry.

Optionally, the model is also handed a **target object mask** — a
black-and-white stencil marking which pixels belong to the object you
want, so it grips *that* and not its neighbour. The mask typically comes
from a perception/vision model
([`../03-perception-vision-models/00-introduction.md`](../03-perception-vision-models/00-introduction.md)).

## The output: candidate grasp poses with scores

The output is **one or many candidate grasps**. Each candidate bundles:

- a **pose** — where to put the gripper and how to orient it (the full
  6-DoF position-plus-orientation; "6-DoF" is unpacked in
  [`01-working.md`](01-working.md)),
- a **grip width** — how far apart to open the fingers, and
- a **quality score** — the model's confidence that this grip will hold,
  usually a number from 0 to 1. The robot tries the highest-scoring
  reachable grasp first.

So the model does not give one answer; it gives a *ranked menu*, and
downstream code picks the best one the arm can actually reach.

## Two kinds of gripper the proposals target

- **Parallel-jaw gripper** — the common two-finger "pincer." Two flat
  jaws slide together in a straight line, like a clamp or a pair of
  tongs. Simple, cheap, and reliable, so most grasp models target it.
  A grasp for it is mostly "where to place the pinch and how to angle
  it."
- **Multi-finger gripper** — a hand with several jointed fingers (three,
  four, or five), able to wrap and cradle awkward shapes. Far more
  capable but much harder to control, so fewer models target it. This
  repo sticks to parallel-jaw grippers for the first version.

A widely used idea for parallel jaws is the **antipodal grasp**: a grip
with two contact points that face *directly opposite* each other (anti =
opposite, podal = foot/point), so the closing fingers squeeze the object
between them without pushing it away. Picture pinching a coin between
thumb and forefinger — the two presses point straight at one another.

## Two ways to come up with a grasp

- **Analytical / geometric grasping** — *hand-computed* grips worked out
  from the object's known shape and the laws of physics, with no machine
  learning at all. For example: if you already know the object is a
  cylinder of a given size and where it sits, you can calculate a pinch
  across its middle directly. Predictable, explainable, and needs no
  training data or GPU — but it only works when you *know* the shape and
  pose in advance, and it copes badly with clutter and novel objects.
- **Learned grasping** — a **neural network trained on grasp data** that
  looks at the raw point cloud and proposes grips, even for objects it
  has never seen and whose exact shape is unknown. Far more general and
  robust in messy real scenes, but it needs a trained model, usually a
  GPU to run, and its choices are not as easy to explain.

This repository deliberately prefers the **simple geometric approach
first**, and treats learned grasping as a **later milestone** — see the
manipulation field write-up
([`../../01-all-areas/05-manipulation/README.md`](../../01-all-areas/05-manipulation/README.md))
and the hands-on "grab the vial" exercise
([`../../03-hplc-autosampler/04-hello-worlds/05-grab-the-vial.md`](../../03-hplc-autosampler/04-hello-worlds/05-grab-the-vial.md)),
which starts from a known pose and a hand-computed grip.

## Where it sits in the pipeline

```text
  perception/vision ─► pose estimation ─► GRASP GENERATION ─► motion planning ─► motors
  "what & where is it" "exactly how is   "where/how to grip"  "a safe path to   "go"
                        it turned"        (this page)          that grip"
```

Grasp generation runs **after** the model knows what and where the
object is (perception
[`../03-perception-vision-models/00-introduction.md`](../03-perception-vision-models/00-introduction.md)
and pose estimation
[`../04-pose-estimation-models/00-introduction.md`](../04-pose-estimation-models/00-introduction.md))
and **before** the motion planner figures out a collision-free path to
the chosen grip and drives the arm there. It is the bridge between
"I see it" and "here is how to hold it."

## Strengths and weaknesses

**Strengths**

- **Handles unknown objects** (learned models): proposes grips on things
  it was never explicitly programmed for.
- **Ranked options**: returns many candidates, so if the best one is
  unreachable the robot can fall back to the next.
- **Decoupled**: it only suggests grips; pairing it with any motion
  planner keeps the system modular.

**Weaknesses**

- **Depends on good depth.** Shiny, transparent, or very dark surfaces
  fool depth cameras, so the point cloud is wrong and the grasp is bad.
- **Clutter is hard.** Objects touching or stacked confuse where one
  ends and the next begins.
- **It does not check reachability.** A high-scoring grasp may be
  physically impossible for *your* arm; the motion planner has to filter.
- **Learned versions need a GPU** and, sometimes, a paid licence.

## When to prefer a simple geometric grasp

Reach for **analytical/geometric grasping** when the objects are **few,
known, and rigid**, their pose is already estimated, and the scene is
tidy — exactly the v1 setup this repo favours. You get a reliable grip
with no model, no GPU, and behaviour you can fully explain.

Reach for a **learned model** only once you face **many unknown or
varied objects in clutter**, where hand-computing a grip for each is
impractical. That is the upgrade, not the starting point.

## See also

- How grasp models work inside, with inputs/outputs:
  [`01-working.md`](01-working.md).
- The three best-known grasp models, with code:
  [`02-top-three-models.md`](02-top-three-models.md).
- The manipulation field this draws on:
  [`../../01-all-areas/05-manipulation/README.md`](../../01-all-areas/05-manipulation/README.md).
