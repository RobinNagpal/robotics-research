# 00 — Vision-Language-Action models: introduction

> **Job of this model type:** look at the robot's cameras, read a
> plain-language instruction ("put the red mug in the sink"), and output
> the robot's next motions directly. One model, from pixels and words to
> motor commands.
>
> Part of [`../`](../README.md). New to model vocabulary? Read
> [`../01-basics/`](../01-basics/README.md) first.

## What a Vision-Language-Action model is

A **Vision-Language-Action model** — almost always shortened to **VLA** —
is a single neural network that takes in:

1. **Vision** — one or more camera images (what the robot sees), and
2. **Language** — a text instruction in plain English,

and produces:

3. **Action** — the robot's next movements (joint angles, or where to
   move the hand, plus open/close the gripper).

The whole appeal is in that straight line. Older robot software needed a
separate perception model, a separate planner, and hand-written glue
(the pipeline in [`../README.md`](../README.md)). A VLA collapses much of
that into **one model you can simply *tell* what to do**.

## Where it comes from (and why it works)

A VLA is, mechanically, a **multimodal large language model** — the same
technology as a chat assistant that can see images — with its output
swapped from "produce text" to "produce robot actions." It inherits the
chat model's hard-won common sense about objects and words, then learns
to move.

Three changes turn a chat model into a VLA:

- **Inputs**: camera frames plus an optional instruction.
- **Output**: instead of writing words, it emits **actions** (see
  [`01-working.md`](01-working.md) for exactly how).
- **Training**: instead of web text, it is pre-trained on **millions of
  robot trajectories** — recordings of robots doing tasks — then
  fine-tuned on a specific robot and job (the recipe from
  [`../01-basics/02-training-vs-inference.md`](../01-basics/02-training-vs-inference.md)).

This is the same **foundation-model** recipe that made chat assistants
work, applied to robot motion. The first convincing VLA, Google's
**RT-2** (2023), is widely called robotics' "GPT moment."

## What it is good at, and what it is not

**Strengths**

- **Generalisation**: because of broad pre-training, a good VLA can often
  handle objects, positions, and phrasings it never saw in your
  fine-tuning data — sometimes *zero-shot* (with no extra training).
- **Plain-language control**: you direct it with a sentence, not code.
- **Less glue**: one model replaces several hand-built pipeline stages.

**Weaknesses**

- **Speed**: a billion-parameter model is heavy; running it fast enough
  to control motors smoothly is a real engineering problem (see latency
  in [`01-working.md`](01-working.md)).
- **Data hunger**: good results still need decent task demonstrations.
- **Unpredictability**: like any large model it can fail in surprising
  ways, which is uncomfortable for safety-critical or regulated settings.
- **Hardware**: training and even running it wants a capable GPU.

## When to reach for a VLA

Reach for a VLA when the task is **varied or hard to script** — many
objects, changing layouts, instructions that differ each time — and you
can gather demonstrations. For a **fixed, repetitive** motion in a
controlled cell, a simpler imitation policy
([`../06-imitation-learning-policies/`](../06-imitation-learning-policies/00-introduction.md))
or even classical hand-written motion is cheaper and more predictable.

This repository deliberately treats VLAs as a **later upgrade**: prove
the task with simple methods first, then add a VLA when generality is
worth the cost — see the same staging in
[`../../01-all-areas/01-robot-learning-vla/`](../../01-all-areas/01-robot-learning-vla/README.md).

## See also

- How a VLA works inside: [`01-working.md`](01-working.md).
- The three most famous VLAs, with code: [`02-top-three-models.md`](02-top-three-models.md).
- The field write-up this draws on:
  [`../../01-all-areas/01-robot-learning-vla/00-basics.md`](../../01-all-areas/01-robot-learning-vla/00-basics.md).
