# 00 — Robotics foundation models: introduction

> **What this folder profiles:** the flagship robot "brains" from the
> leading labs — Google DeepMind's **Gemini Robotics**, Physical
> Intelligence's **π** ("pi") models, and NVIDIA's **GR00T**. These are
> the products people mean when they say "robotics is having its
> ChatGPT moment."
>
> Part of [`../`](../README.md). Read
> [`../02-vision-language-action-models/00-introduction.md`](../02-vision-language-action-models/00-introduction.md)
> first — these are mostly Vision-Language-Action models.

## What "robotics foundation model" means

A **foundation model** (the term is explained in
[`../01-basics/02-training-vs-inference.md`](../01-basics/02-training-vs-inference.md))
is a single large model **pre-trained once** on an enormous, general
dataset, then cheaply **fine-tuned** for many specific jobs. The phrase
"foundation" captures that it is meant to be a reusable base, not a
one-task tool.

A **robotics foundation model** applies that idea to *robot control*: it
is pre-trained on a huge, mixed pile of robot experience (and usually on
web images and text too), so that — out of the box — it already
"understands" everyday objects, instructions, and motions, and can be
adapted to your robot and task with relatively little data. Almost all
of them are **Vision-Language-Action models** (see
[`../02-vision-language-action-models/00-introduction.md`](../02-vision-language-action-models/00-introduction.md)):
they take in camera images plus a plain-language instruction and output
robot motion.

## Why these deserve their own folder

Folders [02–08](../README.md) explain *techniques*. This folder profiles
*products*. The distinction matters because, with these flagship models,
the decision you actually face is rarely "which architecture?" — it is:

- **Can I even get it?** Some are fully open (download the weights and
  run them); others you can only **call over the internet** through an
  **Application Programming Interface** (API — a set of functions a
  provider exposes over the network); others are limited to hand-picked
  partners.
- **What body does it target?** Some aim at simple arms, others at
  full **humanoids** (two-armed, sometimes two-legged robots).
- **What ecosystem does it lock me into?** A model tied to one company's
  simulator and cloud is a different commitment from a standalone file.

So each product gets one document covering all of that, rather than
being scattered across the technique folders.

## The two ideas you need before reading the product pages

- **Open weights vs closed/API-only.** "**Open weights**" means the
  trained model file is published, so you can download it, run it on
  your own hardware, and fine-tune it. "**Closed**" or "**API-only**"
  means you cannot have the file — you send your images to the
  provider's servers and get actions back. Open is more controllable and
  private; API-only is often more capable but depends on a vendor and a
  network connection.
- **Cross-embodiment (cross-body).** Older robot models were trained for
  one specific robot. A **cross-embodiment** model is trained on data
  from **many different robot bodies** at once, so a single model can
  drive several robots and transfer skills between them. All three
  products here lean on this idea; it is a big reason they generalise.

## How the three compare, in one breath

- **Gemini Robotics (Google DeepMind)** — the most capable *generalist*,
  built on the Gemini multimodal models, but the **least open**: you
  mostly access it through Google rather than hosting it. A companion
  model, **Gemini Robotics-ER** ("Embodied Reasoning"), is offered
  through the cloud API for the *thinking/planning* half of the job.
- **Physical Intelligence π0 / π0.5** — the most capable model you can
  **fully download and run yourself** (open code and weights via the
  `openpi` release), known for smooth, dexterous manipulation.
- **NVIDIA GR00T N1 / N1.5** — an **open**, **humanoid**-focused
  foundation model, tightly integrated with NVIDIA's simulator and
  training tools (the Isaac stack).

## How this repository treats them

Consistent with the rest of the repo: these are a **later upgrade**, not
a starting point. Prove a task with simple, predictable methods first
(geometric perception, scripted or imitation-learned motion), then reach
for a frontier foundation model when you genuinely need its generality —
the same staging argued in
[`../02-vision-language-action-models/00-introduction.md`](../02-vision-language-action-models/00-introduction.md)
and
[`../../01-all-areas/01-robot-learning-vla/README.md`](../../01-all-areas/01-robot-learning-vla/README.md).

## See also

- [`01-gemini-robotics.md`](01-gemini-robotics.md) — Google DeepMind.
- [`02-physical-intelligence-pi.md`](02-physical-intelligence-pi.md) —
  Physical Intelligence.
- [`03-nvidia-groot.md`](03-nvidia-groot.md) — NVIDIA.
- How a VLA works inside:
  [`../02-vision-language-action-models/01-working.md`](../02-vision-language-action-models/01-working.md).
