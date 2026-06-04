# 02 — Top three imitation-learning policies (with code)

> **Goal of this page.** Name the three best-known imitation-learning
> policies you can actually download and run, compare them, and give a
> short, commented code sample for each. Builds on
> [`00-introduction.md`](00-introduction.md) and
> [`01-working.md`](01-working.md).
>
> **Read me first — all numbers are approximate and drift fast.** Demo
> counts, library names and especially install/run commands change often.
> Treat every code block as a *teaching sketch* that shows the shape of
> the application programming interface (API — the set of functions you
> call), not a guaranteed-runnable script. Always check the model's
> current documentation.

## Why these three (and one library for all of them)

All three policies below ship inside **LeRobot**, Hugging Face's
open-source robot-learning library. That is deliberate: it means one
install command (`pip install lerobot`) and the **same usage shape** for
every model — load a pretrained policy, build an *observation* (what the
robot senses), and ask it for an action. Learn the pattern once and all
three feel the same.

These three are also the standard, well-documented choices for **small,
single-task** imitation learning — the lightweight cousin of the giant
Vision-Language-Action models in
[`../02-vision-language-action-models/`](../02-vision-language-action-models/00-introduction.md).

| Model | Core idea | Output style | ~Demos needed | Library | Bottom line |
|---|---|---|---|---|---|
| **ACT** | Predict a chunk of moves with a Transformer | Action chunk | ~50 | LeRobot | The go-to for fine, precise manipulation from few demos |
| **Diffusion Policy** | Sculpt the action chunk out of noise | Action chunk (denoised) | ~100–200 | LeRobot | Smoothest motion; best when a task has several valid solutions |
| **VQ-BeT** | Tokenize actions, predict them like words | Action tokens | ~100 | LeRobot | Fast; handles several valid solutions; language-model-style |

"Action chunk," "diffusion" and "multi-modal" (several valid ways to do
a task) are all explained in [`01-working.md`](01-working.md).

---

## 1. ACT (Action Chunking Transformer)

**What it is.** **ACT** stands for **Action Chunking Transformer**. It is
the policy behind the **ALOHA** project — a popular low-cost two-armed
("bimanual") teleoperation setup for delicate tasks. ACT uses a
**Transformer** (the same network family chat models use) to predict an
**action chunk** — the next several moves at once — from camera images
plus the arm's current joint readings. Its claim to fame is learning
**fine manipulation** (threading, plugging, careful placing) from just a
**handful of demonstrations** (~50 is often enough).

**Install.**

```bash
pip install lerobot              # Hugging Face's robot-learning library
```

**Minimal code to run it.**

```python
# Goal: load a pretrained ACT policy and get one action from a single
# observation. This is "inference" — using a trained model, not training
# one. LeRobot's APIs move quickly, so class paths may differ — check the
# current LeRobot docs.

import torch  # PyTorch: runs the neural network
from lerobot.common.policies.act.modeling_act import ACTPolicy

# 1. Download a pretrained ACT checkpoint (the trained weights) from the
#    Hugging Face hub. First run downloads; afterwards it is cached.
policy = ACTPolicy.from_pretrained("lerobot/act_aloha_sim_transfer_cube_human")
policy.eval()        # put the model in "use it", not "train it", mode

# 2. Assemble one observation as PyTorch tensors (a tensor is just an
#    array the GPU understands). Here we use blank stand-ins; on a real
#    robot these come from the cameras and the joint sensors. The exact
#    key names depend on the checkpoint's robot — check its model card.
observation = {
    "observation.images.top": torch.zeros(1, 3, 480, 640),  # one blank camera frame
    "observation.state": torch.zeros(1, 14),                # 14 joint readings (two arms)
}

# 3. Ask for the next action. select_action returns the motor command to
#    send to the robot for this step. (ACT predicts a chunk internally
#    and feeds it out one step at a time.)
with torch.no_grad():            # "don't track gradients" — we're not training
    action = policy.select_action(observation)

print("next action:", action)
```

**What you should see.** A small tensor of action numbers — the joint
targets for the next step. On a real robot you would send these to the
motion controller; here we just print them.

---

## 2. Diffusion Policy

**What it is.** **Diffusion Policy** represents the action chunk with a
**diffusion model**. As explained in [`01-working.md`](01-working.md),
that means it **starts from random noise and repeatedly denoises it** —
sculpting a smooth sequence of moves out of static, guided by the current
observation. Two pay-offs: the motion is **very smooth**, and it handles
**multi-modal** tasks — those with **more than one equally-good way** to
succeed — without averaging the options into a bad blend. It usually
wants a few more demonstrations than ACT (~100–200).

**Install.**

```bash
pip install lerobot              # same library as the others
```

**Minimal code to run it.**

```python
# Goal: load a pretrained Diffusion Policy and get one action from a
# single observation. Class paths may differ across LeRobot versions —
# check the current docs.

import torch
from lerobot.common.policies.diffusion.modeling_diffusion import DiffusionPolicy

# 1. Download a pretrained checkpoint from the Hugging Face hub.
policy = DiffusionPolicy.from_pretrained("lerobot/diffusion_pusht")
policy.eval()        # inference mode, not training

# 2. Build one observation. The "pusht" checkpoint above is a simple
#    pushing task; key names and shapes always depend on the checkpoint,
#    so treat these as illustrative.
observation = {
    "observation.image": torch.zeros(1, 3, 96, 96),   # one blank camera frame
    "observation.state": torch.zeros(1, 2),           # robot state (here: 2 numbers)
}

# 3. Ask for the next action. Internally the policy denoises a chunk of
#    moves from random noise, then hands them out one step at a time.
with torch.no_grad():
    action = policy.select_action(observation)

print("next action:", action)
```

**What you should see.** A small tensor of action numbers for the next
step. Because diffusion denoises in several passes, one inference is a
little slower than ACT's — but the resulting motion is noticeably
smoother (see latency notes in [`01-working.md`](01-working.md)).

---

## 3. VQ-BeT (Vector-Quantized Behavior Transformer)

**What it is.** **VQ-BeT** stands for **Vector-Quantized Behavior
Transformer**. "Vector quantization" is just a way of turning continuous
motions into a fixed menu of discrete **action tokens** — small reusable
motion building-blocks. The model then **predicts those tokens the way a
language model predicts the next word**. Because it treats actions like
language, it is **fast** and naturally **multi-modal** (it can pick among
several valid next moves rather than averaging them). A good middle
ground: roughly ACT's data appetite (~100 demos) with snappy inference.

**Install.**

```bash
pip install lerobot              # same library again
```

**Minimal code to run it.**

```python
# Goal: load a pretrained VQ-BeT policy and get one action from a single
# observation. NOTE: the exact LeRobot class name and import path for
# VQ-BeT have moved between versions — this is a clearly-labelled
# teaching sketch; verify the current path in the LeRobot docs before
# running.

import torch
from lerobot.common.policies.vqbet.modeling_vqbet import VQBeTPolicy  # path may differ

# 1. Download a pretrained checkpoint from the Hugging Face hub. Use a
#    real checkpoint id from the LeRobot model hub; the name below is a
#    placeholder for illustration.
policy = VQBeTPolicy.from_pretrained("lerobot/vqbet_pusht")  # id may differ
policy.eval()        # inference mode

# 2. Build one observation (blank stand-ins; real values come from the
#    cameras and joint sensors). Keys/shapes depend on the checkpoint.
observation = {
    "observation.image": torch.zeros(1, 3, 96, 96),   # one blank camera frame
    "observation.state": torch.zeros(1, 2),           # robot state
}

# 3. Ask for the next action. VQ-BeT picks the next action token(s) like
#    predicting words, then turns them back into a motor command.
with torch.no_grad():
    action = policy.select_action(observation)

print("next action:", action)
```

**What you should see.** A small tensor of action numbers for the next
step — produced quickly, since predicting a token is cheap. If the import
above fails, the class has likely been renamed or moved; search the
current LeRobot source or docs for "VQBeT".

---

## Choosing between them

- **Fine, precise manipulation from very few demos** → **ACT** (the
  ALOHA default; the easiest first win for delicate tasks).
- **Smoothest motion, or a task with several valid solutions** →
  **Diffusion Policy** (best multi-modal behaviour, slightly slower).
- **Fast inference with multi-modal behaviour, language-model style** →
  **VQ-BeT** (a snappy middle ground).

All three are small enough to train in hours on a single modest GPU and
to run comfortably on robot-grade hardware — the opposite trade-off from
a heavyweight VLA (see
[`../02-vision-language-action-models/00-introduction.md`](../02-vision-language-action-models/00-introduction.md)).

## See also

- What these are and when to use them:
  [`00-introduction.md`](00-introduction.md).
- The mechanics behind the code (action chunks, diffusion, distribution
  shift): [`01-working.md`](01-working.md).
- What you physically run these on:
  [`../01-basics/03-running-models-hardware-and-tools.md`](../01-basics/03-running-models-hardware-and-tools.md).
- The bigger, language-driven cousin:
  [`../02-vision-language-action-models/00-introduction.md`](../02-vision-language-action-models/00-introduction.md).
</content>
</invoke>
