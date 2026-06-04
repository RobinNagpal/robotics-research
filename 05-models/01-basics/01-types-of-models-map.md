# 01 — A map of the model types used in robotics

> **Goal of this page.** Give you a single mental map of the kinds of
> model a robotics team uses, and a quick test for telling them apart, so
> the per-type folders that follow have somewhere to hang. Every type
> listed here has its own folder in [`../`](../README.md).

## The big split: perception versus policy

Almost every robotics model falls on one side of a line:

- **Perception models** answer *"what is true about the world right
  now?"* They take in sensor data (usually camera images) and output a
  description: what objects are present, where they are, how they are
  oriented. They do **not** decide what the robot should do.
- **Policy models** answer *"what should the robot do next?"* They take
  in some description of the situation and output an **action** — a
  motion command for the motors. ("Policy" is the standard word for a
  decision-making function in this field; think of it as *the robot's
  decision rule*.)

A working robot chains perception into policy: first understand, then
act. Hold onto this split — it explains why there are so many model
types.

## The perception family

| Model type | Question it answers | Folder |
|---|---|---|
| **Perception / vision** | "What objects are in this image, and what is their outline?" | [`../03-perception-vision-models/`](../03-perception-vision-models/00-introduction.md) |
| **6-DoF pose estimation** | "Exactly where is this object, and which way is it turned?" | [`../04-pose-estimation-models/`](../04-pose-estimation-models/00-introduction.md) |
| **Grasp generation** | "Where on this object should the gripper grip, and at what angle?" | [`../05-grasp-generation-models/`](../05-grasp-generation-models/00-introduction.md) |

"**6-DoF**" is read "six degrees of freedom": three numbers for position
(left-right, forward-back, up-down) plus three for orientation (the
three ways a thing can be rotated). Together they pin down an object
completely in space.

## The policy family

| Model type | How it learns to act | Folder |
|---|---|---|
| **Vision-Language-Action (VLA)** | Pre-trained on huge mixed-robot data, then told what to do in plain language | [`../02-vision-language-action-models/`](../02-vision-language-action-models/00-introduction.md) |
| **Imitation-learning policy** | Copies a human's demonstrated motions | [`../06-imitation-learning-policies/`](../06-imitation-learning-policies/00-introduction.md) |
| **Reinforcement-learning policy** | Practises by trial and error against a reward score | [`../07-reinforcement-learning-policies/`](../07-reinforcement-learning-policies/00-introduction.md) |

The three differ only in **how they are trained**, not in what they
produce — all three output robot actions. A VLA is, in fact, usually
trained *by* imitation; we keep it separate because the "huge
pre-training + plain-language instruction" recipe makes it feel and
behave like a different animal.

## The odd one out: world models

A **world model** ([`../08-world-models/`](../08-world-models/00-introduction.md))
does not fit the perception/policy split neatly. Instead of describing
the present or choosing an action, it learns to **predict the future**:
"if the robot does X, the scene will then look like Y." Given that
ability, the robot can *imagine* several possible actions and pick the
one whose imagined future looks best — planning without touching the
real world. It is the newest and most research-flavoured family here.

## A quick "which type is it?" test

Ask, in order:

1. **Does it output an action (a motor command)?** If yes, it is a
   *policy* — go to the policy family above and ask *how it was trained.*
2. **Does it predict a future observation?** If yes, it is a *world
   model.*
3. **Otherwise it describes the present** — it is a *perception* model;
   ask *what it describes* (objects? exact pose? a grip?).

## What you now know

- Robotics models split into **perception** (understand the world) and
  **policy** (decide the action), with **world models** as a third,
  predict-the-future family.
- Each type in this map has a dedicated folder.

Next: [`02-training-vs-inference.md`](02-training-vs-inference.md)
explains the two phases every one of these models goes through.
