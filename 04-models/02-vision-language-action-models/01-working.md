# 01 — How Vision-Language-Action models work

> **Goal of this page.** Open the box: what exactly goes in, what comes
> out, how the network is shaped, how it is trained, and what it costs to
> run. Plain language, no maths. Builds on
> [`00-introduction.md`](00-introduction.md).

## Inputs and outputs, precisely

**Inputs**

- **Images** — one or more camera frames. Often a fixed "scene" camera
  plus a "wrist" camera mounted on the hand. Each frame is just a grid of
  colour values (pixels).
- **Instruction** — a line of text, e.g. `"pick up the red block"`. Some
  VLAs also take the robot's current joint readings (its *state*) as a
  third input.

**Output: actions**

The output is an **action** — a small list of numbers telling the motors
what to do next. Two common forms:

- **Joint positions** — the target angle for each joint of the arm.
- **End-effector pose** — where to move the hand (the *end effector* is
  whatever is on the end of the arm — a gripper, say), given as a
  position plus orientation, plus one number for "open/close gripper."

Crucially, most modern VLAs output an **action chunk**: not one move but
a short *sequence* of the next several moves (say the next 0.5–1 second
of motion) in a single inference. This makes motion smoother and hides
the model's slowness — the robot executes the chunk while the model
thinks about the next one.

## How an instruction and an image become numbers

Two ideas do the heavy lifting:

- **Tokens.** A large language model does not read text as letters; it
  chops it into chunks called **tokens** (roughly, word-pieces) and turns
  each into numbers. The same trick extends to images: a picture is cut
  into patches, and each patch becomes a token too. So image + text
  become one long list of tokens the model can chew on together — this is
  what "multimodal" means in practice.
- **Action as just more tokens (one popular approach).** Some VLAs treat
  the *output* the same way: they split the range of each motor command
  into bins and emit a "token" naming the bin. The model literally
  "writes" the action the way a chat model writes the next word. RT-2 and
  OpenVLA work this way.
- **A separate action head (the other popular approach).** Other VLAs
  bolt a small specialised output module — an **action head** — onto the
  language model. A common choice is a **diffusion** or **flow** head,
  which is good at producing smooth continuous motion. π0 works this way.
  (Diffusion is explained in
  [`../06-imitation-learning-policies/01-working.md`](../06-imitation-learning-policies/01-working.md).)

You do not have to choose — just know both styles exist, and the
top-three page says which each model uses.

## The architecture, in plain language

```text
 camera image(s) ─► [ vision encoder ]─┐
                                       ├─► [ Transformer backbone ]─► [ action output ]─► motor commands
 "pick up the mug" ─►[ text tokenizer ]┘     (a pre-trained
                                              language-vision model)
```

- A **vision encoder** turns images into tokens.
- A **tokenizer** turns text into tokens.
- A **Transformer backbone** — the large pre-trained language-vision
  model — mixes them and reasons over them. (Transformer: the dominant
  network layout, see
  [`../01-basics/00-what-is-a-model.md`](../01-basics/00-what-is-a-model.md).)
- An **action output** (bin-tokens or an action head) converts the
  backbone's thinking into motor commands.

## How a VLA is trained

It follows the standard two-step recipe from
[`../01-basics/02-training-vs-inference.md`](../01-basics/02-training-vs-inference.md):

1. **Pre-training** on a large, mixed pile of robot **trajectories**
   (recordings of robots doing tasks across many bodies — e.g. the
   ~970k-trajectory Open X-Embodiment collection). This is done once, by
   a well-resourced lab, and is what you download.
2. **Fine-tuning** on **your** robot and task with a modest set of
   demonstrations (often 50–500). This is the cheap step a normal team
   does. The training itself is **imitation learning** — the model is
   shown the human-demonstrated action at each instant and adjusts its
   weights to reproduce it (see
   [`../06-imitation-learning-policies/01-working.md`](../06-imitation-learning-policies/01-working.md)).

## What it costs to run (inference)

This is the practical catch. A VLA is large, and a robot needs decisions
several times per second.

- **Latency** — one inference on a 7-billion-parameter VLA is on the
  order of tens to ~100+ milliseconds on a good GPU. **Action chunking**
  (above) is the main trick that makes this usable: predict a burst of
  moves, execute them while thinking about the next burst.
- **Hardware** — comfortably running a 7B VLA wants a GPU with ~16+
  gigabytes of memory; on the robot that usually means a high-end NVIDIA
  **Jetson** or a nearby workstation GPU. (Figures approximate — re-check
  against the specific model.)
- **Control rate** — effective rates of ~10 commands per second (10 Hz)
  and up are typical for arm manipulation with chunking.

## Limitations and failure modes

- **Slow and hardware-hungry** relative to a hand-coded motion.
- **Brittle outside its experience** — strange lighting or a very
  unusual object can produce confident nonsense.
- **Hard to certify** — its decisions are not human-readable, awkward in
  regulated/safety-critical settings.
- **Still data-dependent** — "foundation model" does not mean "needs no
  data"; quality fine-tuning demonstrations still matter.

## Key terms used on this page

- **Action chunk** — a short predicted sequence of upcoming moves output
  in one go.
- **End effector** — the tool on the end of the arm (e.g. a gripper).
- **Token** — a small chunk of input (word-piece or image patch) turned
  into numbers.
- **Action head** — a specialised output module that converts the
  model's reasoning into continuous motion.

## See also

- The three most famous VLAs, with runnable code:
  [`02-top-three-models.md`](02-top-three-models.md).
- Imitation learning, the training method underneath:
  [`../06-imitation-learning-policies/`](../06-imitation-learning-policies/00-introduction.md).
