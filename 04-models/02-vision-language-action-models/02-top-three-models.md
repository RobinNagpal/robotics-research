# 02 — Top three Vision-Language-Action models (with code)

> **Goal of this page.** Name the three most famous *open* VLAs you can
> actually download and run, compare them, and give a short, commented
> code sample for each. Builds on [`00-introduction.md`](00-introduction.md)
> and [`01-working.md`](01-working.md).
>
> **Read me first — all numbers are approximate and drift fast.**
> Parameter counts, licences and especially install/run commands change
> often. Treat every code block as a *teaching sketch* that shows the
> shape of the API, not a guaranteed-runnable script. Always check the
> model's current documentation. Running any of these needs a capable
> GPU (see [`01-working.md`](01-working.md)).

## Why these three

The best-known VLA, Google's **RT-2**, is **not** publicly downloadable,
so you cannot run it. The three below are the most famous VLAs whose
weights are **open**, which is what lets us show code:

| Model | Maker | ~Size | Action output style | Licence | Bottom line |
|---|---|---|---|---|---|
| **OpenVLA-7B** | Stanford + others | ~7B params | Action-as-tokens | Open (permissive) | The default open VLA to learn on — well documented, huge community |
| **π0 (pi-zero)** | Physical Intelligence | ~3B params | Flow-matching action head | Open weights + code (`openpi`) | Strongest open *continuous-control* VLA; smooth dexterous motion |
| **SmolVLA** | Hugging Face (LeRobot) | ~0.45B params | Action head | Open (permissive) | The small, cheap one — trains and runs on modest hardware |

The output styles are the two designs from
[`01-working.md`](01-working.md): "action-as-tokens" versus an "action
head."

---

## 1. OpenVLA-7B

**What it is.** The first widely adopted *open* VLA (Stanford and
collaborators, 2024). About 7 billion parameters, built on a vision +
language backbone, trained on the large Open X-Embodiment trajectory
collection. It outputs actions as **tokens** (the bin approach from
[`01-working.md`](01-working.md)). It is the standard starting point
because its weights, code and tutorials are all public.

**Install.**

```bash
# A recent NVIDIA GPU with ~16+ GB of memory is expected.
pip install torch torchvision           # PyTorch: the core model library
pip install transformers pillow         # Hugging Face loader + image handling
```

**Minimal code to run it.**

```python
# Goal: hand OpenVLA one camera image + one instruction, and print the
# action (the motor command) it proposes. This is "inference" — using a
# trained model, not training one.

from transformers import AutoModelForVision2Seq, AutoProcessor
from PIL import Image          # PIL = Python Imaging Library: opens images
import torch                   # PyTorch: runs the neural network

# 1. Download the trained weights from the Hugging Face hub (first run
#    only; afterwards they are cached on disk). The "processor" knows how
#    to turn an image + text into the tokens the model expects.
processor = AutoProcessor.from_pretrained(
    "openvla/openvla-7b", trust_remote_code=True)
model = AutoModelForVision2Seq.from_pretrained(
    "openvla/openvla-7b",
    torch_dtype=torch.bfloat16,   # use a compact number format to save memory
    trust_remote_code=True,
).to("cuda")                      # move the model onto the GPU

# 2. Load the picture the robot's camera sees, and write the instruction.
image = Image.open("robot_camera_view.jpg")
instruction = "pick up the red block"

# 3. Pack image + text into model inputs, then ask for an action.
#    "unnorm_key" tells it which robot's action scale to use; the value
#    depends on the dataset the checkpoint was tuned for.
inputs = processor(instruction, image).to("cuda", dtype=torch.bfloat16)
action = model.predict_action(**inputs, unnorm_key="bridge_orig",
                              do_sample=False)

# 4. "action" is a short list of numbers: usually how far to move the
#    hand in each direction, how to turn it, and whether to open/close
#    the gripper. You would now send these numbers to the robot.
print("proposed action:", action)
```

**What you should see.** After the (large) download, a printed array of
numbers — the proposed motion. On a real robot you would feed that array
to the motion controller; in this snippet we just print it.

---

## 2. π0 ("pi-zero")

**What it is.** A ~3-billion-parameter VLA from Physical Intelligence
(2024) aimed at **smooth, dexterous, continuous control**. Instead of
emitting action *tokens*, it uses a **flow-matching action head** (a
close cousin of diffusion) to generate fluid motion — which is why it
shines on delicate manipulation. Released open as the **`openpi`**
code-and-weights package.

**Install.**

```bash
# Cloned and installed from source; openpi ships its own instructions.
git clone https://github.com/Physical-Intelligence/openpi.git
cd openpi
pip install -e .                 # "-e" installs it in editable form
```

**Minimal code to run it.**

```python
# Goal: load a pretrained pi-zero policy and ask it for an action chunk
# given a camera image + a state + an instruction. API names follow the
# openpi package and may change — check its README.

import numpy as np                       # NumPy: arrays of numbers
from openpi.training import config as _config
from openpi.policies import policy_config

# 1. Pick a published pi-zero configuration and download its checkpoint
#    (the trained weights) from the project's model store.
cfg = _config.get_config("pi0_base")
checkpoint_dir = "s3://openpi-assets/checkpoints/pi0_base"
policy = policy_config.create_trained_policy(cfg, checkpoint_dir)

# 2. Build one "observation": what the robot currently senses. Images are
#    arrays of pixels; "state" is the arm's current joint readings.
observation = {
    "image": {                            # one or more camera views
        "base_0_rgb": np.zeros((224, 224, 3), dtype=np.uint8),
    },
    "state": np.zeros(8, dtype=np.float32),   # current joint positions
    "prompt": "pick up the red block",        # the plain-language task
}

# 3. Ask the policy for an action. pi-zero returns an *action chunk* —
#    several upcoming moves at once (see 01-working.md) — which the robot
#    plays out before asking again.
result = policy.infer(observation)
print("action chunk shape:", np.shape(result["actions"]))
```

**What you should see.** The shape of an action chunk, e.g.
`(50, 7)` — fifty future timesteps, seven numbers each (six for the
hand's motion plus one gripper command). On a robot you would execute
those rows in order.

---

## 3. SmolVLA

**What it is.** A deliberately **small** VLA (~450 million parameters)
from the Hugging Face LeRobot team (2025), designed to train and run on
ordinary hardware — even, slowly, without a top-end GPU. It is the
friendliest VLA to *experiment* with, and integrates directly with the
**LeRobot** library (see
[`../01-basics/03-running-models-hardware-and-tools.md`](../01-basics/03-running-models-hardware-and-tools.md)).

**Install.**

```bash
pip install lerobot              # Hugging Face's robot-learning library
```

**Minimal code to run it.**

```python
# Goal: load the pretrained SmolVLA policy and get one action from a
# single observation. LeRobot APIs move quickly — check current docs.

import torch
from lerobot.common.policies.smolvla.modeling_smolvla import SmolVLAPolicy

# 1. Download the pretrained SmolVLA weights from the Hugging Face hub.
policy = SmolVLAPolicy.from_pretrained("lerobot/smolvla_base")
policy.eval()                    # put the model in "use it", not "train it", mode

# 2. Assemble one observation as PyTorch tensors (a tensor is just an
#    array the GPU understands). Here we use blank stand-ins; on a real
#    robot these come from the camera and the joint sensors.
observation = {
    "observation.image": torch.zeros(1, 3, 256, 256),  # one blank image
    "observation.state": torch.zeros(1, 6),            # six joint readings
    "task": ["pick up the red block"],                 # the instruction
}

# 3. Ask for the next action. select_action returns the motor command to
#    send to the robot for this step.
with torch.no_grad():            # "don't track gradients" — we're not training
    action = policy.select_action(observation)

print("next action:", action)
```

**What you should see.** A small tensor of action numbers for the next
step. Because the model is small, this runs far faster and on much
cheaper hardware than the two above — its trade-off is somewhat lower
peak capability.

---

## Choosing between them

- **Learning the ropes / strong all-rounder** → **OpenVLA-7B** (most
  tutorials and community help).
- **Best smooth, dexterous manipulation** → **π0**.
- **Limited hardware, fast iteration, fine-tuning on a laptop-class GPU**
  → **SmolVLA**.

## See also

- What these are and when to use them:
  [`00-introduction.md`](00-introduction.md).
- The mechanics behind the code: [`01-working.md`](01-working.md).
- A runnable SmolVLA exercise in this repo's autosampler project:
  [`../../03-hplc-autosampler/04-hello-worlds/06-run-smolvla-in-sim.md`](../../03-hplc-autosampler/04-hello-worlds/06-run-smolvla-in-sim.md).
