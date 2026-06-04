# 01 — How imitation-learning policies work

> **Goal of this page.** Open the box: what goes in, what comes out, how
> behavior cloning actually learns, why these policies drift off course,
> and the two tricks — *action chunking* and *diffusion* — that fix it.
> Plain language, no maths. Builds on
> [`00-introduction.md`](00-introduction.md).

## Inputs and outputs, precisely

**Inputs — the observation**

At each moment the policy is handed an **observation**: a snapshot of what
the robot senses right now.

- **Images** — one or more camera frames. Often a fixed "scene" camera
  plus a "wrist" camera mounted on the hand. Each frame is just a grid of
  colour values (pixels).
- **Robot state** — the arm's current joint readings (and sometimes
  gripper open/close). This is the robot's sense of where its own body is.

Unlike a VLA, a plain imitation policy usually takes **no text
instruction** — it does the one task it was trained for.

**Output — the action**

The output is an **action**: a small list of numbers telling the motors
what to do next. Two common forms:

- **Joint positions** — the target angle for each joint of the arm.
- **End-effector pose** — where to move the hand (the *end effector* is
  whatever is on the end of the arm — a gripper, say), as a position plus
  orientation, plus one number for open/close gripper.

Most modern imitation policies do not output a single move. They output
an **action chunk** — a short *sequence* of the next several moves (say
the next ~0.5–1 second of motion) in one go. Why that helps is the heart
of this page.

## Behavior cloning is just supervised learning

**Behavior cloning** is **supervised learning** on observation→action
pairs. "Supervised learning" means: you give the model many
input→correct-answer pairs and it learns to reproduce the answers.

- The **input** is an observation (images + state).
- The **correct answer** is the action the human demonstrated at that
  instant.

Training breaks every recorded **demonstration** (see
[`../01-basics/02-training-vs-inference.md`](../01-basics/02-training-vs-inference.md))
into thousands of these pairs and adjusts the model's internal numbers
(its *weights*) until its predicted action matches the human's action as
closely as possible. That is the entire training idea: **show, copy,
repeat.** No reward, no trial and error.

## The distribution-shift problem (why naive cloning drifts)

Here is the catch that defines this whole field.

During training the model only ever sees observations from a **good run**
— the expert never crashes, never freezes, never ends up in a weird pose.
So the model never learns what to do from those bad situations, because it
never saw one.

At run time the model controls the robot itself. Its tiny prediction
errors nudge the robot slightly off the expert's path — into an
observation a bit unlike anything in training. From there its next guess
is worse, pushing it further off, and the errors **compound** until the
robot is somewhere the demonstrations never covered and the policy is
guessing blindly. This mismatch between *training situations* and
*situations the policy actually reaches* is **distribution shift**.

Two design ideas dramatically reduce it.

### Trick 1 — action chunking

Instead of predicting one move at a time, the policy predicts a whole
**action chunk** — the next several moves at once — and the robot executes
them before asking again.

- **Fewer decision points** means fewer chances to drift, and the
  small errors do not get re-amplified every single step.
- The motion comes out **smoother**, because a chunk is planned as one
  coherent stroke rather than stitched from many independent guesses.
- It also **hides model slowness**: the robot plays out the chunk while
  the model computes the next one.

### Trick 2 — diffusion (a diffusion policy)

A second, complementary idea is to use a **diffusion policy**. To
understand it, first the plain-language picture of **diffusion**:

> Imagine you want to carve a smooth motion, but you start with a block of
> pure random static — meaningless noise. A diffusion model has learned to
> **chip away the noise in small, repeated passes**, each pass making the
> shape a little cleaner, until a smooth, sensible action sequence emerges.
> It is like **sculpting motion out of static.**

So a diffusion policy generates an action chunk by **starting from random
noise and repeatedly denoising it**, guided by the current observation,
into a clean sequence of moves. Two reasons this is popular:

- **Very smooth motion**, which suits delicate manipulation.
- **It handles multi-modal behaviour.** "Multi-modal" means there is **more
  than one equally-good way** to do the task — you could go round the cup
  on the left *or* the right. A naive model, asked to predict one answer,
  tends to average the options and aim straight at the cup (a bad blend of
  both). A diffusion policy can commit to one valid option at a time
  instead of averaging, so it does not get stuck in the muddled middle.

## The architecture, in plain language

```text
 camera image(s) ─►[ vision encoder ]─┐
                                      ├─►[ policy network ]─► action chunk ─► motor commands
 joint readings  ─►[ state encoder  ]─┘   (a Transformer or
                                           a diffusion model)
```

- A **vision encoder** turns images into a compact numeric summary.
- A **state encoder** does the same for the joint readings.
- A **policy network** mixes them and produces the action chunk. Depending
  on the model this is a **Transformer** (the dominant network layout, the
  same family used by chat models) or a **diffusion** model as above.

## How one is trained

It follows the recipe in
[`../01-basics/02-training-vs-inference.md`](../01-basics/02-training-vs-inference.md),
but usually **without the huge pre-training step** a VLA has:

1. **Collect demonstrations** by teleoperation (see
   [`00-introduction.md`](00-introduction.md)) — typically ~50–300
   episodes of the one task (figure approximate — re-check).
2. **Fit the model** by behavior cloning: feed it the observation→action
   pairs until its predictions match the demonstrations. On a single
   modern GPU this often takes hours, not weeks, because the model is
   small and the dataset is modest.

That low cost is the whole appeal: you can record demos in the morning and
have a working policy by the afternoon.

## What it costs to run (inference)

Because these models are far smaller than a VLA, they are **cheap and fast
to run**.

- **Latency** — one inference is typically on the order of a few to a few
  tens of milliseconds on a modest GPU; diffusion policies are a bit
  slower because they denoise in several passes (figures approximate).
- **Control rate** — chunking means one inference covers many steps, so
  effective rates of ~10 commands per second (10 Hz) and higher are
  comfortable for arm manipulation.
- **Hardware** — many of these run on a modest GPU, and some run (slowly)
  even without one. See
  [`../01-basics/03-running-models-hardware-and-tools.md`](../01-basics/03-running-models-hardware-and-tools.md).

## Limitations and failure modes

- **Distribution shift / compounding errors** — the core weakness above;
  chunking and diffusion reduce it but do not erase it.
- **Demo-bound** — it can only do what was demonstrated, the way it was
  demonstrated; new objects or layouts usually mean new demos.
- **Sensitive to demo quality** — inconsistent or careless teleoperation
  produces an inconsistent, careless policy.
- **No built-in recovery** — without demonstrations of *recovering* from
  mistakes, it rarely recovers on its own.

## Key terms used on this page

- **Behavior cloning** — training a policy by copying demonstrated
  observation→action pairs (supervised learning).
- **Teleoperation** — a human directly driving the robot to record
  demonstrations.
- **Action chunk** — a short predicted sequence of upcoming moves output
  in one go (fewer decision points → less drift, smoother motion).
- **Diffusion** — generating an output by starting from random noise and
  repeatedly denoising it into a clean result; a **diffusion policy** does
  this to produce action chunks.
- **Distribution shift** — the mismatch between the situations seen in
  training and the situations the running policy actually reaches; the
  cause of compounding errors.

## See also

- What these are and when to use them:
  [`00-introduction.md`](00-introduction.md).
- The three best-known models, with runnable-style code:
  [`02-top-three-models.md`](02-top-three-models.md).
- The bigger, language-driven cousin:
  [`../02-vision-language-action-models/01-working.md`](../02-vision-language-action-models/01-working.md).
