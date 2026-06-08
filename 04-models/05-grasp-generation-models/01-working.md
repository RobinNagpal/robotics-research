# 01 — How grasp generation models work

> **Goal of this page.** Open the box: what exactly goes in, what comes
> out, how a learned grasp model produces and ranks grips, how it is
> trained, and what it costs to run. Plain language, no maths. Builds on
> [`00-introduction.md`](00-introduction.md).

## Inputs and outputs, precisely

**Inputs**

- **A point cloud or depth image** — the 3D shape of the scene. A
  **point cloud** is a set of 3D dots sampled off the visible surfaces
  (each dot is three numbers: its position left-right, forward-back,
  up-down). A **depth image** is a photo whose pixels store distance
  instead of colour; a point cloud is usually computed from it. Many
  models also accept the matching **colour** for each point.
- **(Optional) a target object mask** — a black-and-white stencil saying
  which points belong to the object you want to pick, so grips are
  proposed on *it* and not on the table or a neighbour. It usually comes
  from a perception/vision model.

**Output: ranked grasp candidates**

Each candidate grasp bundles four things:

- **A 6-DoF grasp pose.** "6-DoF" reads "six degrees of freedom": the
  full description of where the gripper goes. Three numbers fix the
  **position** (left-right, forward-back, up-down — where the hand sits
  in space) and three fix the **orientation** (how the hand is turned —
  the three independent ways anything can be rotated). Together they pin
  the gripper down completely, with no ambiguity left.
- **A grip width** — how far apart to open the fingers before closing,
  so they straddle the object rather than crash into it.
- **A quality / confidence score** — a number (often 0 to 1) saying how
  likely this grip is to hold. It is what lets the model **rank** its
  proposals so the robot tries the best one first.

The model typically returns **many** such candidates at once — a whole
ranked list — because the single best grip might be unreachable for your
particular arm, and the next-best is then ready to go.

## How a learned grasp model works, in plain language

The dominant recipe is **"sample many, then score":**

1. **Propose candidates.** From the point cloud, generate a large pile
   of *possible* grips — many positions and angles spread over the
   visible surfaces. Some models do this with simple geometry; others
   have the network propose them directly.
2. **Score each one with a neural network.** The network looks at the
   local shape around each candidate and predicts how good that grip is —
   essentially "if the fingers close here at this angle, will the object
   stay put?"
3. **Return the best.** Sort by score, discard the obviously bad ones,
   and output the top grips as the ranked list above.

A core notion the scorer leans on is the **antipodal grasp**: a grip
whose two contact points face *directly opposite* each other (anti =
opposite, podal = point), so the closing jaws squeeze the object between
them instead of nudging it away. Think of pinching a coin between thumb
and finger — the two presses point straight at one another. Grips that
are roughly antipodal on a solid bit of surface tend to score high.

## The architecture, in plain language

```text
 point cloud / depth ─► [ 3D encoder ]─┐
                                       ├─► [ grasp scorer ]─► ranked list of
 (optional) object mask ───────────────┘   (neural network)   (pose, width, score)
```

- A **3D encoder** digests the cloud of dots into a compact internal
  description of the local geometry. (Point clouds are unordered, so the
  encoder is built to not care what order the dots arrive in.)
- A **grasp scorer** takes candidate grips and rates each, and often
  also nudges each candidate's pose to a better nearby one.
- The result is the **ranked list** of grasps handed to the motion
  planner.

## How a grasp model is trained

Training needs examples of "this grip on this shape held / slipped" — a
lot of them. Labelling those by hand on real robots is painfully slow,
so the field leans heavily on **synthetic data**:

- **Synthetic / simulated grasps.** Object 3D shapes are loaded into a
  **physics simulator** (software that imitates real-world physics), and
  the computer *tries* enormous numbers of grips automatically, checking
  in simulation whether each one would hold. Each attempt becomes a
  labelled example — for free, by the million, overnight. The landmark
  dataset **GraspNet-1Billion** carries roughly a *billion* such grasp
  labels.
- **The network then learns** to predict those held/slipped labels from
  the point cloud, so at run time it can score a brand-new grip without
  trying it. Training is done once by a lab; you download the result.

The catch with synthetic data is the **sim-to-real gap**: simulated
depth is cleaner than a real camera's, so a model can look better in the
lab than on your bench. Good datasets add realistic sensor noise to
close that gap.

## What it costs to run (inference)

Grasp models are much lighter than the giant policy models elsewhere in
this repo:

- **Latency** — a single scene typically scores in the order of tens to
  a few hundred milliseconds on a decent GPU. Fast enough to grasp from
  a fresh camera view each time. (Figures approximate — re-check against
  the specific model.)
- **Hardware** — a mid-range NVIDIA GPU with ~6–8 gigabytes of memory is
  usually plenty; some run on an embedded board like an NVIDIA
  **Jetson**. See
  [`../01-basics/03-running-models-hardware-and-tools.md`](../01-basics/03-running-models-hardware-and-tools.md).
- **Sensor** — you also need a **depth/RGB-D camera**; the model is only
  as good as the point cloud it is fed.

## Limitations and failure modes

- **Clutter.** When objects touch, lean, or stack, the model struggles
  to tell where one ends and the next begins, and may propose a grip that
  spans two objects.
- **Transparent and shiny objects.** Glass, clear plastic, and polished
  metal **fool the depth camera** — the light passes through or scatters,
  so the point cloud has holes or false surfaces and the grasp is wrong.
- **Thin objects.** Sheets of paper, blades, low flat items barely
  register in depth, leaving the model nothing solid to grip.
- **No reachability check.** The top-scored grasp may be physically
  impossible for *your* arm; the motion planner must filter the list.
- **Sim-to-real gap.** As above — lab numbers can flatter real-world
  performance.

## Key terms used on this page

- **Point cloud** — a set of 3D dots sampled off visible surfaces, each
  just a left-right / forward-back / up-down position.
- **6-DoF pose** — six numbers (three position, three orientation) that
  completely fix where and how the gripper sits.
- **Grip width** — how far apart to open the fingers before closing.
- **Antipodal grasp** — a grip whose two contact points face directly
  opposite each other.
- **Quality score** — the model's confidence that a grip will hold; used
  to rank candidates.
- **Sim-to-real gap** — the drop in performance when a model trained on
  clean simulated data meets a noisy real camera.

## See also

- The three best-known grasp models, with runnable-shaped code:
  [`02-top-three-models.md`](02-top-three-models.md).
- What this model type is and when to use it:
  [`00-introduction.md`](00-introduction.md).
- The pose estimation step that often runs just before:
  [`../04-pose-estimation-models/00-introduction.md`](../04-pose-estimation-models/00-introduction.md).
