# 00 — Reinforcement-learning policies: introduction

> **Job of this model type:** learn how to act by trial and error.
> The robot tries an action, gets a numeric **reward** (a score saying
> how well it did), and gradually adjusts its behaviour to earn more
> reward — usually by practising millions of times in a simulator before
> ever touching real hardware.
>
> Part of [`../`](../README.md). New to model vocabulary? Read
> [`../01-basics/`](../01-basics/01-types-of-models-map.md) first.

## What reinforcement learning is

**Reinforcement learning** — almost always shortened to **RL** — is a way
to teach a robot to act *without showing it what to do*. Instead of
giving it correct answers, you give it a **reward**: a single number that
says "that was good" (high) or "that was bad" (low). The robot then tries
things, watches its reward go up or down, and learns to act so that the
reward stays high. It is learning by **trial and error**, the same way a
child learns to ride a bike — wobble, fall, adjust, repeat.

The thing being trained is a **policy** — the robot's decision rule. You
hand the policy a description of the current situation and it hands back
an **action** (a motor command). The whole point of RL is to *find a good
policy* purely from rewards.

## The vocabulary, in plain language

RL has its own small dictionary. These seven words appear everywhere:

- **Agent** — the learner and decider. In our case, the robot (really,
  the policy controlling it).
- **Environment** — everything outside the agent that it acts on and
  senses: the world, the objects, the floor, the simulator. The agent
  acts; the environment reacts.
- **State / observation** — the description of the situation right now.
  Strictly, the **state** is the full true situation and the
  **observation** is the part the agent actually sees (e.g. camera
  images, joint angles). People often use the words interchangeably.
- **Action** — what the agent does this step: a motor command (a target
  joint angle, a wheel speed, open/close the gripper).
- **Reward** — the score the environment gives back after an action. The
  designer defines it: e.g. +1 for moving forward, −1 for falling over.
- **Episode** — one complete attempt at the task, from start to finish
  (e.g. one walk until the robot falls or a timer runs out). Training
  runs through many thousands of episodes.
- **Policy** — the decision rule itself: the function (a small neural
  network) that turns an observation into an action. This is what gets
  trained and what you eventually run on the robot.

The loop these connect into — observe, act, get reward, learn — is laid
out step by step in [`01-working.md`](01-working.md).

## The central role of the simulator

Trial and error means a *lot* of mistakes. A real robot learning to walk
by falling over a few million times would destroy itself (and take
years). So RL for robots almost always happens in a **simulator** — a
physics-based video game of the robot and its world.

A simulator gives you three things the real world cannot:

- **Safety** — a simulated robot can fall, crash, or flail with no
  damage and no human nearby.
- **Speed** — simulators run faster than real time, and you can run
  **thousands of copies of the robot at once**, all practising in
  parallel, so weeks of "experience" pile up in hours.
- **Free resets** — at the end of every episode you instantly teleport
  the robot back to the start, perfectly, for free.

This is why RL and simulators are inseparable. The catch is what happens
next.

## The sim-to-real gap

A policy trained only in simulation has only ever seen the simulator. The
real world is never quite the same — real motors are slightly weaker,
real floors are slightly more slippery, real cameras are noisier, and the
physics is only approximated. So a policy that walks beautifully in sim
can stumble on the real robot. This mismatch is called the
**sim-to-real gap**.

Closing it is a whole craft (the main trick, **domain randomization**, is
explained in [`01-working.md`](01-working.md)). For now, just hold the
idea: *training in sim is cheap and safe, but transferring to reality is
the hard part of RL robotics.*

## How RL differs from imitation learning

The sibling family,
[**imitation-learning policies**](../06-imitation-learning-policies/00-introduction.md),
learns by **copying human demonstrations** — you show the robot the task
a few hundred times and it mimics you. RL is the opposite trade-off:

- **No demonstrations needed.** You never have to perform the task. This
  is a huge win for skills humans *cannot* easily demonstrate — like
  balancing a 12-jointed legged robot.
- **But you must design a reward.** Turning "walk nicely" into a precise
  numeric score is surprisingly hard, and a sloppy reward produces weird
  behaviour. This work is called **reward engineering**, and it is the
  main pain of RL — the equivalent of imitation learning's
  "collect demonstrations" chore.

A rough rule: **if it is easy to *show* the task, lean imitation; if it
is easy to *score* the task but hard to show, lean RL.**

## Where RL shines

- **Locomotion** — making legged robots (two-, four-, many-legged) walk,
  run, and recover from shoves. This is RL's flagship success: almost
  every modern walking-robot controller is RL-trained in simulation.
- **Hard-to-demonstrate skills** — fast, dynamic, or high-frequency
  control where a human cannot provide good demonstrations (balancing,
  dribbling, agile flight).
- **Squeezing out performance** — when you want behaviour that is *better
  than* any human demonstration, not just a copy of it.

## Strengths and weaknesses

**Strengths**

- **No demonstrations required** — learns from scratch given a reward.
- **Can exceed human performance** — it optimises the score directly,
  not a human example.
- **Cheap to run once trained** — the trained policy is a small network
  (see inference below).

**Weaknesses**

- **Reward engineering is hard** — a bad reward gives bad or gamed
  behaviour ("reward hacking", in [`01-working.md`](01-working.md)).
- **The sim-to-real gap** — what works in sim may not survive contact
  with reality.
- **Sample-inefficient** — it needs an enormous amount of practice
  (millions of steps), which is only practical in simulation.

## When to reach for RL

Reach for RL when the task is **easy to score but hard to demonstrate** —
classically, legged locomotion and other dynamic, high-frequency control
— and you have a decent simulator of the robot. For tasks you can simply
*show* a few times (many pick-and-place jobs), an imitation policy or even
hand-written motion is faster to get working and more predictable.

As with the other model types, this repository treats RL as a tool for
the right job, not a default — prove the task with the simplest method
that works first, in the same spirit as
[`../../01-all-areas/01-robot-learning-vla/`](../../01-all-areas/01-robot-learning-vla/README.md).

## See also

- How RL works inside, step by step: [`01-working.md`](01-working.md).
- The three most-used RL algorithms, with code:
  [`02-top-three-models.md`](02-top-three-models.md).
- The sibling that copies demonstrations instead:
  [`../06-imitation-learning-policies/`](../06-imitation-learning-policies/00-introduction.md).
- A model family that *imagines* the future to plan:
  [`../08-world-models/`](../08-world-models/00-introduction.md).
