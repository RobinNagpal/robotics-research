# 02 — Training versus inference: a model's two phases

> **Goal of this page.** Explain the two phases of every model's life —
> **training** (the expensive one-off process of learning) and
> **inference** (the cheap, repeated process of using what was learned) —
> plus the words you will meet around each: dataset, fine-tuning,
> pre-training, and so on.

## The two phases, in one picture

```text
   data ──►  [ TRAINING ]  ──►  trained weights  ──►  [ INFERENCE ]  ──►  answers
            (slow, once)        (a saved file)        (fast, many times)
```

- **Training** happens **once** (or occasionally), usually in a data
  centre, and can take hours, days, or weeks on expensive hardware. Its
  product is the **weights** file (see
  [`00-what-is-a-model.md`](00-what-is-a-model.md)).
- **Inference** is **running** the finished model to get answers. It
  happens constantly — on a robot, many times per second. It is far
  cheaper than training, but it still has to be **fast enough**: a robot
  that takes two seconds to decide each move is useless.

Most robotics teams **never train a model from scratch.** They download
weights someone else trained and either use them directly or adjust them
slightly. The next sections explain that.

## Datasets: the examples a model learns from

A **dataset** is the collection of examples used for training. Its
quality and size largely decide how good the model gets.

- For a perception model, the dataset is images with labels ("this box
  is a cup").
- For a robot **policy**, the dataset is **trajectories**: recordings of
  a robot (often guided by a human) actually doing the task — at each
  instant, what the cameras saw and what motion was commanded. One
  recorded attempt is called an **episode** or a **demonstration**.
- A famous robotics dataset, **Open X-Embodiment**, pooled ~970,000
  trajectories from 22 different robot types so models could learn from
  many bodies at once. (Figure approximate — re-check.)

## Pre-training, fine-tuning, and "foundation models"

These three words describe the dominant modern recipe:

- **Pre-training** — the big, expensive first training run on a huge,
  general dataset. It teaches broad competence ("how objects and motions
  generally work") but not your specific task.
- A **foundation model** is the reusable result of that big pre-training
  run — a strong, general starting point meant to be adapted, not used
  raw.
- **Fine-tuning** — a short, cheap second training run that nudges a
  pre-trained model toward *your* task using a small dataset (often just
  50–500 demonstrations). This is what most teams actually do, and it is
  affordable on modest hardware.

This "pre-train once, fine-tune cheaply many times" pattern is exactly
why the model types in this area became practical: you inherit someone
else's million-dollar pre-training and pay only for the cheap last step.

## A few more inference-time words

- **Checkpoint** — a saved weights file. "Load the checkpoint" means
  "load these particular trained weights."
- **Latency** — how long one inference takes, e.g. 50 milliseconds. Low
  latency matters enormously for robots controlling motors in real time.
- **Throughput / control rate** — how many decisions per second the
  model can produce, often written in **hertz (Hz)**, meaning
  "times per second." A policy running at **10 Hz** outputs ten motion
  commands every second.
- **Zero-shot** — using a model on a task or object it was never
  specifically trained for, with no extra training. "It grasped the
  novel object zero-shot" means "with no task-specific fine-tuning."

## What you now know

- A model is **trained once** (slow, expensive) and **runs at inference
  many times** (fast, must hit a latency/rate budget).
- It learns from a **dataset**; for policies, examples are
  **trajectories / demonstrations / episodes**.
- The standard recipe is **pre-train a foundation model, then fine-tune
  cheaply** on your task.

Next: [`03-running-models-hardware-and-tools.md`](03-running-models-hardware-and-tools.md)
covers what you physically run all this on.
