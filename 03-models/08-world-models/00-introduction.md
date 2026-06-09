# 00 — World models: introduction

> **Job of this model type:** learn a *simulator in the robot's head*.
> Given the situation right now and an action the robot is thinking about
> taking, predict what the robot would *sense next*. With that, the robot
> can "imagine" the outcomes of different actions and plan inside the
> imagination — instead of trying everything for real.
>
> Part of [`../`](../README.md). New to model vocabulary? Read
> [`../01-basics/01-types-of-models-map.md`](../01-basics/01-types-of-models-map.md)
> first — it frames the world model as the family's "odd one out."

## What a world model is

A **world model** is a learned predictor of the future. You feed it:

1. the **current situation** (what the robot has been sensing — recent
   camera frames and so on), and
2. a **candidate action** (something the robot could do next),

and it answers: **"if you did that, here is what you would sense
next."** Repeat the question with the predicted result, and the robot can
roll the future forward several steps in its head.

This is genuinely different from the other model types in
[`../01-basics/01-types-of-models-map.md`](../01-basics/01-types-of-models-map.md).
A **perception model** describes the present ("there is a red mug at this
spot"). A **policy** picks an action ("move the hand here"). A world
model does neither directly — it **predicts what comes next**. That is
why the map calls it the odd one out.

The plain image to keep: a world model is a **simulator the robot
learned by watching**, rather than one a human wrote by hand. A
hand-written simulator (the kind in the wider repo's sim layer) knows
physics because a programmer coded the physics. A world model never sees
the physics rules — it learns to predict by being shown lots of real
recordings, the same way it might learn anything else.

## The big idea: planning by imagining

Once you can predict the future, a powerful trick opens up. To decide
what to do, the robot can:

1. **Imagine** taking action A, predict the resulting future, and score
   how good that future looks.
2. Do the same for action B, action C, and so on.
3. **Pick the action whose imagined future scores best**, and actually
   do that one.

All of step 1 and 2 happen *inside the model* — no motors move, no time
is wasted, nothing breaks. The robot only acts in the real world once it
has found a promising plan. This is often called **planning in
imagination** or "dreaming," and it is the whole reason world models are
exciting. [`01-working.md`](01-working.md) shows exactly how a future is
rolled forward and scored.

## Contrast with model-free reinforcement learning

The closest cousin is the **reinforcement-learning policy**
([`../07-reinforcement-learning-policies/00-introduction.md`](../07-reinforcement-learning-policies/00-introduction.md)).
A reinforcement-learning policy learns to act by **trial and error**: it
tries something, gets a **reward** (a score saying how well it did), and
nudges itself toward whatever earned more reward. Crucially, the plain
version — called **model-free** — never tries to *predict* the future. It
just keeps acting and adjusting. That works, but it needs an enormous
number of tries, because every lesson costs a real (or simulated)
attempt.

A world model changes the economics. Because the robot can practise
*inside its own predictions*, it can run thousands of imagined attempts
for the price of one real one. Methods built this way are called
**model-based** (they have a model of the world), and they are far more
**sample-efficient** — they squeeze much more learning out of each real
attempt. World models are how you make reinforcement learning affordable.

There is also overlap with **imitation learning**
([`../06-imitation-learning-policies/00-introduction.md`](../06-imitation-learning-policies/00-introduction.md))
and even
[VLAs](../02-vision-language-action-models/00-introduction.md): all of
these can be *trained* using a world model's imagined experience instead
of, or alongside, real data.

## Why this matters for robotics

Real-world robot practice is **slow, expensive, and risky**. Every
attempt takes wall-clock time, wears out hardware, and can damage the
robot or its surroundings. Imagining, by contrast, is **cheap** — it is
just the model running numbers. So a world model lets a robot:

- **practise mostly in its head**, touching the real world only to
  collect a little fresh experience and to execute its chosen plan;
- **look ahead** before committing, instead of discovering a mistake
  only after making it;
- **reuse one learned model** for many different goals, because
  predicting the future is goal-agnostic — you can ask "what happens if"
  about anything.

## Where it sits in the stack

A world model does not slot neatly into the perception-then-policy
pipeline; it can **replace or augment both ends**:

- Used as **perception**, its compressed internal summary of the scene
  (the *latent state* in [`01-working.md`](01-working.md)) is a learned
  understanding of what is going on.
- Used as **policy**, its imagination either *trains* a policy or is
  *searched* directly for a good action each step.

So you can think of it less as one more box in the pipeline and more as a
different *strategy* for building the acting part of the robot.

## What it is good at, and what it is not

**Strengths**

- **Data efficiency** — by far its headline advantage. Practising in
  imagination means far fewer costly real attempts.
- **Look-ahead planning** — it can weigh consequences before acting.
- **Generality** — one predictor can serve many goals and tasks.

**Weaknesses**

- **Hard to train.** Learning to predict a rich, messy world accurately
  is one of the open problems in the field.
- **Predictions can be wrong, and errors compound.** A small mistake in
  the first predicted step feeds into the second, which feeds into the
  third — so imagined futures drift from reality the further out you
  look (explained in [`01-working.md`](01-working.md)).
- **Research-grade maturity.** The tooling is far less settled than for
  perception models or imitation policies.

## When to use it — and the research caveat

Reach for a world model when **real attempts are precious** — the robot
is slow, fragile, or expensive to run, and you cannot afford millions of
trials. That is exactly when "practise in your head" pays off.

But be clear-eyed: world models are the **newest and most
research-flavoured** family in this folder. Outside a few landmark
systems they are mostly run by **cloning a research repository** and
adapting it, not by installing a polished library. This repository treats
them as a **frontier option to watch**, not a default first build —
prove your task with simpler perception and imitation methods first.

## See also

- How a world model works inside, step by step:
  [`01-working.md`](01-working.md).
- The three landmark world-model systems, with code sketches:
  [`02-top-three-models.md`](02-top-three-models.md).
- The trial-and-error cousin it makes affordable:
  [`../07-reinforcement-learning-policies/00-introduction.md`](../07-reinforcement-learning-policies/00-introduction.md).
- Where it fits among all model types:
  [`../01-basics/01-types-of-models-map.md`](../01-basics/01-types-of-models-map.md).
