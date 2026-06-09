# 00 — Imitation-learning policies: introduction

> **Job of this model type:** watch a human do a task a few times, then
> copy them. The model learns the mapping "what I see right now → what to
> do next," straight from recorded demonstrations — no rules to write, no
> reward to design.
>
> Part of [`../`](../README.md). New to model vocabulary? Read
> [`../01-basics/`](../01-basics/01-types-of-models-map.md) first.

## What imitation learning is

An **imitation-learning policy** is a robot **policy** — a decision rule
that outputs an **action** (a motor command) — that is trained by
**copying examples a human provided**. Show it enough recordings of the
task being done well, and it learns to reproduce the same motions in the
same situations.

The technical name for the most common version is **behavior cloning**:
the model "clones" the behaviour in the recordings. Mechanically it is
the simplest idea in robot learning. At every instant of every recording
you have a pair:

- what the robot **saw** (the *observation* — camera images, plus the
  arm's current joint readings), and
- what the human **did** next (the *action* — the motor command).

The model is trained to look at the observation and predict the action,
over and over, until it can fill in the action by itself. That is all
"learn the mapping observation → action" means. The mechanics are in
[`01-working.md`](01-working.md).

## Where the demonstrations come from: teleoperation

The demonstrations are recorded by **teleoperation** — a human operating
the robot remotely or by hand while the system records everything.

**Teleoperation** ("tele" = at a distance) just means a person drives the
robot directly instead of the robot deciding for itself. Common rigs:

- A **leader-follower** pair: the human moves a small copy of the arm
  (the *leader*); the real arm (the *follower*) mirrors it. The famous
  **ALOHA** setup works this way for two-armed tasks.
- A **joystick, 3-D mouse, or hand-tracking** controller.
- **Kinesthetic teaching** — literally grabbing the robot and guiding its
  arm through the motion by hand.

While the human guides the robot, the system saves, many times per
second, the camera frames and the commanded motion. Each complete attempt
is one **demonstration** (also called an **episode** or **trajectory** —
see
[`../01-basics/02-training-vs-inference.md`](../01-basics/02-training-vs-inference.md)).
Collect a few dozen to a few hundred of these and you have a training
**dataset**.

## How it differs from the neighbours

All three policy families output the same thing — a robot action — and
differ only in **how they learn**. The map in
[`../01-basics/01-types-of-models-map.md`](../01-basics/01-types-of-models-map.md)
lays this out; here is the short version.

- **Versus reinforcement learning.** A **reinforcement-learning** policy
  ([`../07-reinforcement-learning-policies/`](../07-reinforcement-learning-policies/00-introduction.md))
  learns by **trial and error**: it tries things, gets a numeric score (a
  *reward*) for how well it did, and gradually favours high-scoring
  behaviour. Imitation learning skips all that — it never experiments and
  needs no reward; it just mimics what it was shown. That makes imitation
  far simpler to set up, but it cannot discover anything the
  demonstrations did not contain.
- **Versus Vision-Language-Action models.** A **Vision-Language-Action
  model** ([`../02-vision-language-action-models/`](../02-vision-language-action-models/00-introduction.md)),
  or **VLA**, is *usually trained by imitation too* — so a VLA is, in a
  sense, a giant imitation-learning policy. The difference is **scale and
  language**: a VLA is first **pre-trained** on millions of trajectories
  from many robots, then takes a plain-English instruction at run time.
  The policies in this folder are small, single-task, and learned from
  *your* handful of demonstrations only — no huge pre-training, usually no
  language input. Think of these as the lightweight, focused cousin of the
  VLA.

## Where it sits in the system

This is the **policy / action stage** itself — the part that decides and
commands motion. In a classic robotics pipeline, perception models first
say *what is where* and then a policy says *what to do*; an
imitation-learning policy is that second box. Many imitation policies are
trained **end to end**, meaning they go straight from raw camera pixels to
motor commands without a separate perception step.

## Strengths and weaknesses

**Strengths**

- **Simple to set up.** No reward to design, no rules to hand-code — just
  record good examples and fit the model.
- **Data-efficient for a fixed task.** A well-chosen ~50–200
  demonstrations can teach one specific skill (figure approximate —
  re-check for your task).
- **Captures human "feel."** It copies the smooth, sensible way a person
  did the task, including subtleties that are hard to write as rules.
- **Predictable scope.** It does one job, the way it was shown.

**Weaknesses**

- **Only as good as the demonstrations.** Sloppy, inconsistent, or
  too-few demos give a sloppy policy. Garbage in, garbage out.
- **Compounding errors / distribution shift.** This is the central
  problem. The model only ever saw situations the *expert* led it
  through. The moment its own small mistakes carry it into a situation the
  demonstrations never covered, it has no idea what to do, makes a bigger
  mistake, drifts even further off — and the errors **compound**. The gap
  between "states the expert visited" and "states the policy now finds
  itself in" is called **distribution shift**. (Tricks that fight it —
  predicting short *chunks* of motion, and *diffusion* policies — are
  explained in [`01-working.md`](01-working.md).)
- **No generalisation beyond the demos.** Change the task, the objects,
  or the layout much and you usually need to record new demonstrations.

## When to reach for one

Reach for an imitation-learning policy when:

- the task is **specific and repeatable** (one shelf, one set of items),
- you **can demonstrate it** by teleoperation, and
- you do **not** need plain-language control or broad generalisation.

If the task is varied or you want to *tell* the robot what to do in
English, prefer a VLA
([`../02-vision-language-action-models/`](../02-vision-language-action-models/00-introduction.md)).
If there is a clear success score and a simulator to practise in safely,
reinforcement learning
([`../07-reinforcement-learning-policies/`](../07-reinforcement-learning-policies/00-introduction.md))
may discover better behaviour than any human demo. This repository's
staging advice — prove the task with the simplest method first — is the
same one in
[`../../01-all-areas/01-robot-learning-vla/`](../../01-all-areas/01-robot-learning-vla/README.md).

## See also

- How these policies work inside: [`01-working.md`](01-working.md).
- The three best-known models, with code:
  [`02-top-three-models.md`](02-top-three-models.md).
- The training/inference vocabulary used here:
  [`../01-basics/02-training-vs-inference.md`](../01-basics/02-training-vs-inference.md).
