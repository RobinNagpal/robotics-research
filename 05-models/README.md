# 05 — Models: the kinds of AI models used in robotics

> **What this area is.** Modern robots increasingly run on **machine
> learning models** — neural networks trained on data rather than rules
> written by hand. This area is a guided tour of the *types* of model a
> robotics team actually uses, organised one folder per type. It is
> written for a software developer who has never trained a model and has
> never touched a robot. Plain language first; every abbreviation is
> spelled out the first time it appears.

> **How to read it.** Start with [`01-basics/`](01-basics/README.md) to
> learn what a "model" even is and the vocabulary used everywhere else.
> Then read whichever model-type folder interests you. The folders are
> numbered only to give a sensible reading order — you can jump around.

---

## Why split robotics models by type?

A robot is not driven by one giant brain. It is a **pipeline of
models**, each doing one job, plus old-fashioned hand-written code
gluing them together. A grocery-shelf robot might, in a single second:

1. **see** the scene and find objects (a *perception* model),
2. work out exactly **where** each object is in space (a *pose
   estimation* model),
3. decide **where to grip** an object (a *grasp generation* model),
4. and **choose the next motion** (a *policy*, which may be a
   *vision-language-action* model, an *imitation-learning* policy, or a
   *reinforcement-learning* policy).

These are genuinely different kinds of model, trained on different data,
with different inputs and outputs. Lumping them together hides what
matters. This area keeps them separate so you can learn one at a time.

---

## The model types covered here

Each folder below contains three documents — `00-introduction.md` (what
it is, in plain language), `01-working.md` (how it works under the
hood), and `02-top-three-models.md` (the three most famous examples,
with runnable code for each).

| # | Folder | What kind of model | One-line job |
|---|---|---|---|
| 01 | [`01-basics/`](01-basics/README.md) | *(foundations, not a model type)* | What a model is, how it is trained and run, and the vocabulary |
| 02 | [`02-vision-language-action-models/`](02-vision-language-action-models/00-introduction.md) | Vision-Language-Action (VLA) | See + read an instruction → output robot motion |
| 03 | [`03-perception-vision-models/`](03-perception-vision-models/00-introduction.md) | Perception / vision | Find and outline objects in a camera image |
| 04 | [`04-pose-estimation-models/`](04-pose-estimation-models/00-introduction.md) | 6-DoF pose estimation | Work out an object's exact position *and* orientation |
| 05 | [`05-grasp-generation-models/`](05-grasp-generation-models/00-introduction.md) | Grasp generation | Propose where and how a gripper should grip |
| 06 | [`06-imitation-learning-policies/`](06-imitation-learning-policies/00-introduction.md) | Imitation-learning policy | Copy motions from human demonstrations |
| 07 | [`07-reinforcement-learning-policies/`](07-reinforcement-learning-policies/00-introduction.md) | Reinforcement-learning policy | Learn motions by trial and error against a reward |
| 08 | [`08-world-models/`](08-world-models/00-introduction.md) | World model | Learn to *predict* what happens next, and plan in imagination |

---

## How these fit together (a concrete example)

For the **pick-and-place** task this repository keeps returning to —
a small arm moving objects on a bench — a typical stack is:

```
camera image
   │
   ▼
[03 perception]  "there is a cup, here is its outline"
   │
   ▼
[04 pose]        "the cup is at x=0.2 m, y=0.0 m, tilted 12°"
   │
   ▼
[05 grasp]       "grip across the rim, fingers 7 cm apart"
   │
   ▼
[06/07/02 policy] "move joint 1 by +5°, joint 2 by −3°, … close gripper"
```

The first three boxes are **perception** (understanding the world); the
last box is a **policy** (deciding what to do). [08 world models] are a
newer idea that can *replace* several boxes at once by learning to
predict the future and planning inside that prediction.

The same split shows up across the rest of this repository — see the
field-by-field write-ups in
[`../01-all-areas/`](../01-all-areas/) and the buildable projects in
[`../03-place-items-on-shelf/`](../03-place-items-on-shelf/) and
[`../04-hplc-autosampler/`](../04-hplc-autosampler/).

---

## A standing warning about numbers and commands

Model names, parameter counts, licences, install commands and benchmark
scores **drift quickly** — this is one of the fastest-moving corners of
software. Every figure here is marked approximate (`~`) and every code
sample is a **teaching example**: short, clarity-first, and not
guaranteed to run unchanged a year from now. Always check the model's
own current documentation before you rely on it.
