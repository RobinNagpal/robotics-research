# 02 — Physical Intelligence: π0 and π0.5

> **The product:** Physical Intelligence's **π0** ("pi-zero") and its
> successor **π0.5** ("pi-zero-point-five") — the most capable robot
> foundation model you can **fully download and run yourself**, shipped
> as open code and weights in the `openpi` package.
>
> Part of [`../`](../README.md). Read
> [`00-introduction.md`](00-introduction.md) and
> [`../02-vision-language-action-models/00-introduction.md`](../02-vision-language-action-models/00-introduction.md)
> first — π is a Vision-Language-Action (VLA) model.

## What it is

**Physical Intelligence** (often written "PI" or "π") is a robotics
startup focused on building a single general-purpose model that can
drive many different robots. Their headline releases:

- **π0** ("pi-zero", ~2024) — a **cross-embodiment** VLA. "VLA" is
  short for **Vision-Language-Action**: a model that takes camera
  images plus a plain-language instruction and outputs robot motion
  (see
  [`../02-vision-language-action-models/00-introduction.md`](../02-vision-language-action-models/00-introduction.md)).
  "Cross-embodiment" (or *cross-body*) means it was trained on data
  from **many different robot bodies** at once, so one model can drive
  several robots — explained in
  [`00-introduction.md`](00-introduction.md). π0's distinguishing trick
  is a **flow-matching action head** (defined below) that produces
  smooth, dexterous motion.
- **π0.5** ("pi-zero-point-five", ~2025) — the follow-up, aimed
  squarely at **open-world generalization**: doing useful work in
  messy, unfamiliar places (a real home it has never seen, say) rather
  than only in the lab setups it was trained on.

Both are released **openly** — code *and* trained weights — through the
**`openpi`** package. That openness is the whole reason π earns its own
page: you can put the actual model file on your own machine.

## What makes it distinctive

- **Flow-matching action head → smooth, dexterous motion.** Most older
  VLAs emit actions as *tokens* (they "write" the motion the way a chat
  model writes words). π instead bolts on an **action head** — a small
  specialised output module — of the **flow-matching** kind.
  **Flow matching**, in one sentence, is a way to generate a smooth
  continuous output by starting from random noise and steadily nudging
  it toward a realistic motion (a close cousin of "diffusion"); both
  are explained in
  [`../02-vision-language-action-models/01-working.md`](../02-vision-language-action-models/01-working.md).
  This is why π is strong at delicate, fluid manipulation — folding
  laundry, handling soft or fiddly objects — rather than just blocky
  pick-and-place.
- **Action chunks, not single twitches.** π outputs an **action
  chunk**: not one move but a short *sequence* of the next several moves
  in one inference (again see
  [`../02-vision-language-action-models/01-working.md`](../02-vision-language-action-models/01-working.md)).
  The robot plays out the chunk while the model thinks about the next
  one, which keeps motion smooth and hides the model's slowness.
- **Cross-embodiment training on large, diverse data.** π was
  pre-trained on a big, mixed pile of manipulation experience spanning
  many robot bodies and tasks — the recipe in
  [`../02-vision-language-action-models/01-working.md`](../02-vision-language-action-models/01-working.md)
  and
  [`../01-basics/02-training-vs-inference.md`](../01-basics/02-training-vs-inference.md).
  That breadth is what lets it generalise.
- **It is OPEN — you download and fine-tune it yourself.** Unlike a
  cloud service, you get the weights. You can run it offline, inspect
  it, and fine-tune it on **your** robot with a modest set of
  demonstrations. Contrast this with **Gemini Robotics**
  ([`01-gemini-robotics.md`](01-gemini-robotics.md)), which is more of a
  generalist but is largely **API-only** — an **API** (Application
  Programming Interface) is a set of functions a provider exposes over
  the network, so you send images to their servers and get actions back
  rather than holding the model yourself.

## How you get access

π is published on a public **GitHub** repository (`openpi`), with the
trained **weights** (checkpoints) hosted on the project's model store /
model hub. You clone the repo, install it, and download a checkpoint.

| Model | Action output | Open weights? | Hardware to run it | Bottom line |
|---|---|---|---|---|
| **π0** (~3B params) | Flow-matching action head → action chunk | **Yes** (`openpi`) | A capable NVIDIA GPU, ~16+ GB memory | The strongest open *continuous-control* VLA; smooth, dexterous |
| **π0.5** | Same head, tuned for open-world tasks | **Yes** (`openpi`) | Similar GPU class | The follow-up; better generalisation to unfamiliar settings |

All figures are approximate (`~`) and **drift fast** — parameter
counts, checkpoint names and licence terms change. Re-check the
`openpi` repository before quoting anything. Running these needs a
capable **GPU** (graphics processing unit); see
[`../01-basics/03-running-models-hardware-and-tools.md`](../01-basics/03-running-models-hardware-and-tools.md).

## A teaching sketch: load π0 and get an action chunk

This is a **teaching sketch** — it shows the *shape* of the `openpi`
interface, not a guaranteed-runnable script. The API names follow the
`openpi` package and **may change**; always check its current README.
You need a capable GPU to actually run it. (It mirrors the π0 sample in
[`../02-vision-language-action-models/02-top-three-models.md`](../02-vision-language-action-models/02-top-three-models.md).)

**Install.**

```bash
# openpi is cloned and installed from source; it ships its own
# up-to-date instructions, so prefer those if they differ.
git clone https://github.com/Physical-Intelligence/openpi.git
cd openpi
pip install -e .                 # "-e" installs it in editable form
```

**Load a policy and ask for an action chunk.**

```python
# Goal: load a pretrained pi-zero policy and ask it for an action chunk
# given a camera image + the arm's state + a plain-language instruction.
# This is "inference" — using a trained model, not training one. API
# names follow the openpi package and may change; check its README.

import numpy as np                       # NumPy: arrays of numbers
from openpi.training import config as _config
from openpi.policies import policy_config

# 1. Pick a published pi-zero configuration. The config bundles the
#    model definition and the input/output formatting it expects.
cfg = _config.get_config("pi0_base")

# 2. Point at a published checkpoint (the trained weights) in the
#    project's model store, and build a ready-to-use policy from it.
#    The weights download on first use, then cache on disk.
checkpoint_dir = "s3://openpi-assets/checkpoints/pi0_base"
policy = policy_config.create_trained_policy(cfg, checkpoint_dir)

# 3. Build one "observation": what the robot senses right now.
#    - "image" holds one or more camera views; each is a grid of pixels.
#    - "state" is the arm's current joint readings (here, 8 numbers).
#    - "prompt" is the plain-language task.
#    We use blank stand-ins; on a real robot these come from the camera
#    and the joint sensors.
observation = {
    "image": {
        "base_0_rgb": np.zeros((224, 224, 3), dtype=np.uint8),  # scene cam
    },
    "state": np.zeros(8, dtype=np.float32),   # current joint positions
    "prompt": "pick up the red block",        # the instruction
}

# 4. Ask the policy for an action. pi-zero returns an *action chunk* —
#    several upcoming moves at once — which the robot plays out before
#    asking again. The flow-matching head is what makes that chunk
#    smooth and continuous.
result = policy.infer(observation)

# 5. Inspect the chunk's shape. On a robot you would send these rows to
#    the motion controller in order, instead of just printing them.
print("action chunk shape:", np.shape(result["actions"]))
```

**What you should see.** After the (large) download, the shape of an
action chunk, e.g. `(50, 7)` — fifty future timesteps, seven numbers
each (six for the hand's motion plus one gripper open/close command).
The exact numbers depend on the checkpoint and the robot it targets.

## Strengths and limitations

**Strengths**

- **Fully open** — weights *and* code. You own the file: run it
  offline, fine-tune it on your robot, keep your data private.
- **Smooth, dexterous manipulation** — the flow-matching head is its
  signature advantage on delicate, continuous tasks.
- **Cross-embodiment** — one model spans several robot bodies, and
  π0.5 pushes generalisation toward unfamiliar real-world settings.
- **Active, documented project** — `openpi` ships configs, checkpoints
  and examples, so fine-tuning is a well-trodden path.

**Limitations**

- **Hardware-hungry and not instant.** Like any billion-parameter VLA
  it wants a capable GPU and is slower than hand-coded motion; action
  chunking softens but does not remove this (see latency in
  [`../02-vision-language-action-models/01-working.md`](../02-vision-language-action-models/01-working.md)).
- **Brittle outside its experience.** Strange lighting or a very
  unusual object can produce confident nonsense — the open-world push
  in π0.5 narrows this gap but does not close it.
- **Still data-dependent.** "Foundation model" does not mean "needs no
  data": good fine-tuning demonstrations still matter.
- **Hard to certify.** Its decisions are not human-readable, which is
  awkward in safety-critical or regulated settings.
- **Fast-moving target.** Versions, checkpoint names and APIs change
  often — pin a version and re-check the repo.

## When to reach for it

Reach for π when you want a **genuinely capable VLA that you can host
yourself** — because you need offline operation, data privacy, the
freedom to fine-tune, or simply the strongest **open** option for
**smooth, dexterous** manipulation. If you instead want the most
capable generalist and are happy to call a cloud service, look at
**Gemini Robotics** ([`01-gemini-robotics.md`](01-gemini-robotics.md));
if your target is a **humanoid** tied to NVIDIA's tools, see **GR00T**
([`03-nvidia-groot.md`](03-nvidia-groot.md)).

Consistent with the rest of this repository: a frontier VLA like π is a
**later upgrade**, not a starting point. Prove your task first with
simple, predictable methods (geometric perception, scripted or
imitation-learned motion — see
[`../06-imitation-learning-policies/00-introduction.md`](../06-imitation-learning-policies/00-introduction.md)),
then add π when its generality is worth the cost.

## See also

- The other two flagship products:
  [`01-gemini-robotics.md`](01-gemini-robotics.md) (Google DeepMind) and
  [`03-nvidia-groot.md`](03-nvidia-groot.md) (NVIDIA).
- The π0 entry with the original code sample:
  [`../02-vision-language-action-models/02-top-three-models.md`](../02-vision-language-action-models/02-top-three-models.md).
- How a VLA works inside (flow matching, action chunks):
  [`../02-vision-language-action-models/01-working.md`](../02-vision-language-action-models/01-working.md).
- Training vs running a model, and the hardware it needs:
  [`../01-basics/02-training-vs-inference.md`](../01-basics/02-training-vs-inference.md)
  and
  [`../01-basics/03-running-models-hardware-and-tools.md`](../01-basics/03-running-models-hardware-and-tools.md).
- The field-level write-up of robot foundation models:
  [`../../01-all-areas/01-robot-learning-vla/README.md`](../../01-all-areas/01-robot-learning-vla/README.md).
- A runnable open-VLA exercise in this repo:
  [`../../04-hplc-autosampler/02-hello-worlds/06-run-smolvla-in-sim.md`](../../04-hplc-autosampler/02-hello-worlds/06-run-smolvla-in-sim.md).
```
