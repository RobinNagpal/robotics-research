# 01 — Gemini Robotics (Google DeepMind)

> **The product:** Google DeepMind's flagship robot "brain" — a
> Vision-Language-Action model (**VLA**: it looks at cameras, reads a
> plain-language instruction, and outputs robot motion) built on the
> Gemini multimodal models, paired with a separate
> **embodied-reasoning** model you can call over the internet.
>
> Part of [`../`](../README.md). Read
> [`00-introduction.md`](00-introduction.md) first, and the VLA write-up
> it points to:
> [`../02-vision-language-action-models/00-introduction.md`](../02-vision-language-action-models/00-introduction.md).

> **Heavy drift warning.** This is the fastest-moving topic in the repo.
> Every model name, version number, access term and benchmark claim
> below is approximate (`~`) and **must be re-checked** against Google's
> current documentation (<https://ai.google.dev/> and the Gemini Robotics
> pages). The code is a **teaching sketch**, not a guaranteed-runnable
> script.

## What it is

Google DeepMind ships its robotics work as **two** related models, and
keeping them apart is the single most useful thing to understand here:

- **Gemini Robotics** — the **VLA** (Vision-Language-Action model).
  It is built directly on **Gemini**, Google's family of large
  **multimodal** models (models that handle images, text and more in one
  network). It takes the robot's camera images plus a plain-language
  instruction and outputs **action** — the robot's next movements. This
  is the model that actually *moves* a robot.
- **Gemini Robotics-ER** — the **embodied-reasoning** model. **ER**
  stands for **Embodied Reasoning**; "embodied" means "reasoning about a
  physical body acting in real space," as opposed to handling only text.
  It does not emit motor commands. Instead it does the *thinking* half of
  the job: understanding a scene, working out **where** things are,
  **pointing** at locations in the image, and writing a **step-by-step
  plan**. This is the model you can reach through the cloud
  **Application Programming Interface** (**API** — a set of functions a
  provider exposes over the network so your program can call their model
  and get an answer back).

It is **notable** because it is built on a frontier general-purpose
model, so it inherits unusually strong common sense about objects and
words; it is widely cited for strong **generalisation** (handling things
it never saw in training), **dexterity** (delicate two-handed
manipulation), and **reasoning** (it can plan, not just react).

There is also a third, optional variant worth knowing the name of:
**Gemini Robotics On-Device**, a smaller version meant to run **on the
robot itself** rather than in the cloud — useful when a network round
trip would be too slow or unreliable. (Concepts of running a model
locally versus over a network are covered in
[`../01-basics/03-running-models-hardware-and-tools.md`](../01-basics/03-running-models-hardware-and-tools.md).)

## What makes it distinctive

- **Built on a frontier multimodal model.** Most VLAs start from a
  mid-sized vision+language backbone; Gemini Robotics starts from
  Google's top-tier Gemini line, so it brings exceptionally broad
  world knowledge to the robot.
- **Strong semantic and spatial reasoning.** Beyond "what is this
  object," it reasons about *where* and *how* — it can point to a target
  spot in an image, estimate where things are relative to each other, and
  break a vague instruction into concrete steps.
- **The "reason" / "act" split.** Google deliberately separates the
  thinking model (**Gemini Robotics-ER**) from the moving model (**Gemini
  Robotics**). You can use the reasoning model on its own to plan, then
  hand the plan to whatever executes motion — exactly the pattern shown
  in this repo's autosampler exercise
  [`../../04-hplc-autosampler/02-hello-worlds/07-gemini-plans-the-task.md`](../../04-hplc-autosampler/02-hello-worlds/07-gemini-plans-the-task.md).
- **Cross-embodiment (cross-body).** It is trained to drive **several
  different robot bodies** — arms and humanoids — rather than one fixed
  robot, which is a big reason it transfers skills (the idea is explained
  in [`00-introduction.md`](00-introduction.md)).
- **An on-device variant.** Unlike most frontier models, a slimmed-down
  version is offered to run **on the robot**, trading some capability for
  lower latency and no network dependence.

## How you get access

Be candid about this: the two models are **not equally reachable**.

- **Gemini Robotics-ER** (the reasoning/planning model) is the one you
  can realistically touch today. It is offered through the **Gemini API**
  — you sign in, get an **API key** (a long secret string, like a
  password, that proves the request is yours so Google knows whom to
  bill), and call it from code (sketch below). Access to this specific
  model may still be **gated** or in preview; if you cannot get it, the
  same code shape works against a general Gemini vision model so you can
  still see the idea.
- **Gemini Robotics** (the full action/VLA model) is **not openly
  downloadable**. There are **no open weights** ("open weights" means the
  trained model file is published so you can run it yourself — see
  [`00-introduction.md`](00-introduction.md)). Access is **limited** and
  largely through a **partner / trusted-tester program**, so for most
  people you cannot host or fine-tune it the way you can the open models
  in [`02-physical-intelligence-pi.md`](02-physical-intelligence-pi.md)
  and [`03-nvidia-groot.md`](03-nvidia-groot.md).

| Model | What it does | How accessed | Open weights? | Bottom line |
|---|---|---|---|---|
| **Gemini Robotics** (VLA) | Camera + instruction → robot motion | Limited / partner program | No | The most capable generalist robot brain, but you mostly cannot have the file |
| **Gemini Robotics-ER** | Scene understanding, pointing, step-by-step plans (text, not motion) | Gemini cloud **API** (needs a key); may be gated | No | The reachable half — call it to *plan* and *reason*, not to drive motors |
| **Gemini Robotics On-Device** | A smaller action model that runs on the robot itself | Limited release / SDK | No (restricted) | For low-latency, no-network use; availability is narrow |

(**SDK** = **Software Development Kit**: a bundle of code libraries and
tools a vendor gives you to build against their product.)

All three are **closed** in the sense that matters most for this repo:
you do not own the trained file, so you depend on Google and, for the
cloud models, on a network connection.

## A teaching sketch: using Gemini Robotics-ER through the API

The goal here is the *reasoning* half: show the model a workbench photo
plus an instruction, and read back a plan and a pointed-to location. This
mirrors — and extends — the worked, line-by-line example in
[`../../04-hplc-autosampler/02-hello-worlds/07-gemini-plans-the-task.md`](../../04-hplc-autosampler/02-hello-worlds/07-gemini-plans-the-task.md);
read that one for the full beginner walkthrough.

**Install.**

```bash
# Google's official Python library for Gemini. The package name has
# changed once already — check the current docs before relying on it.
pip install google-genai
```

**Minimal code to call it.**

```python
# Goal: hand Gemini Robotics-ER a workbench image + an instruction, and
# print back (a) a step-by-step plan and (b) where it would place an
# object. This is "inference" — using a trained model, not training one.
# It returns TEXT/COORDINATES, not robot motion.

import os                                  # built-in: read the secret key from the environment
from google import genai                   # Google's Gemini client library ("generative AI")
from google.genai import types             # helper shapes, e.g. wrapping an image

# 1. Read the API key from an environment variable, never hard-code it.
#    You set it once in the terminal:  export GEMINI_API_KEY="...".
#    Keeping the secret out of the file means you can share the file safely.
api_key = os.environ["GEMINI_API_KEY"]     # pull the key out by name

# 2. Build the "client" — the object that talks to Google's service over
#    the internet. We hand it the key so every request is signed as ours.
client = genai.Client(api_key=api_key)

# 3. Load the workbench photo as raw bytes (the computer's basic units of
#    data). "rb" = read, in binary, because an image is not text.
with open("workbench.jpg", "rb") as photo_file:
    image_bytes = photo_file.read()

# 4. Wrap those bytes into a "part" — one piece of the message we send.
#    The mime_type label tells the service "these bytes are a JPEG photo."
image_part = types.Part.from_bytes(
    data=image_bytes, mime_type="image/jpeg")

# 5. Write the plain-language instruction. We ask the embodied-reasoning
#    model for two things at once: where to place the block, and the steps.
instruction = (
    "You are reasoning for a small robot arm on this workbench. "
    "Point to where the red block should go (give an image location), "
    "then list the numbered steps to put it there. Keep steps short "
    "and physical."
)

# 6. Send image + instruction together and wait for the answer. The model
#    name string is the part most likely to have changed — verify it in
#    the current docs (it may look like "gemini-robotics-er-1.5").
response = client.models.generate_content(
    model="gemini-robotics-er-1.5",        # the embodied-reasoning model; name WILL drift
    contents=[image_part, instruction])    # the photo and the words as one combined question

# 7. The reply is text. For ER it often includes both the prose plan and
#    pointed-to coordinates in the image; print it and read it.
print("Gemini Robotics-ER says:\n")
print(response.text)
```

**What you should see.** After a short wait, a printed reply: a numbered
plan in plain English, often with a location in the image (for example
pixel coordinates, or a normalised x/y point) where the block should go.
The exact wording and the coordinate format vary run to run and across
versions — that is normal for these models. Nothing moves; this is the
*plan*, which you would then hand to a motion layer or a **behaviour
tree** to actually execute.

## Strengths and limitations

**Strengths**

- **Best-in-class generalisation and reasoning.** Built on a frontier
  multimodal model, it handles unfamiliar objects, messy scenes and vague
  instructions unusually well.
- **Spatial grounding.** It can point to *where* in an image, not just
  name *what* — handy for telling a robot a target location.
- **Clean reason/act split.** You can use ER for planning even if you
  never get the full action model.
- **Cross-body and dexterous.** Reported to drive multiple robot types
  and do delicate two-handed tasks.

**Limitations**

- **Closed and gated.** No open weights; the full VLA is partner-only,
  so most teams **cannot host or fine-tune it**. This is the opposite of
  the open options in
  [`02-physical-intelligence-pi.md`](02-physical-intelligence-pi.md) and
  [`03-nvidia-groot.md`](03-nvidia-groot.md).
- **Vendor and network dependence.** The cloud models need Google and a
  connection; a network round trip adds **latency** (delay), which
  matters for fast control loops. The on-device variant exists partly to
  dodge this.
- **Unpredictability.** Like any large model it can fail in surprising
  ways — uncomfortable for safety-critical settings.
- **Fast-moving and opaque pricing.** Names, access terms and any costs
  drift constantly and must be re-checked before you quote them.

## When to reach for it

Reach for **Gemini Robotics-ER** when you want **frontier-level scene
understanding and planning** through a simple API call — to turn a photo
plus a sentence into a sensible step list or a pointed-to target — and
you are happy depending on the cloud. Reach for the full **Gemini
Robotics** VLA only if you are in a position to get **partner access**;
otherwise an open VLA you can actually run is the practical choice.

Consistent with the rest of this repo: treat any frontier model as a
**later upgrade**. Prove your task with simple, predictable methods
first, then add a model like this when its generality is genuinely worth
the cost and the vendor dependence — the same staging argued in
[`../02-vision-language-action-models/00-introduction.md`](../02-vision-language-action-models/00-introduction.md)
and
[`../../01-all-areas/01-robot-learning-vla/README.md`](../../01-all-areas/01-robot-learning-vla/README.md).

## See also

- The other two flagship products:
  [`02-physical-intelligence-pi.md`](02-physical-intelligence-pi.md)
  (open, downloadable) and
  [`03-nvidia-groot.md`](03-nvidia-groot.md) (open, humanoid-focused).
- What "robotics foundation model", open vs closed, and cross-body mean:
  [`00-introduction.md`](00-introduction.md).
- How a VLA works inside, and the training-vs-inference idea:
  [`../02-vision-language-action-models/01-working.md`](../02-vision-language-action-models/01-working.md)
  and
  [`../01-basics/02-training-vs-inference.md`](../01-basics/02-training-vs-inference.md).
- A full, line-by-line beginner walkthrough of calling Gemini
  Robotics-ER:
  [`../../04-hplc-autosampler/02-hello-worlds/07-gemini-plans-the-task.md`](../../04-hplc-autosampler/02-hello-worlds/07-gemini-plans-the-task.md).
- Where this folder sits overall: [`./README.md`](./README.md).
