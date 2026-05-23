# Robot Learning & Foundation Models (VLA) — The Basics

> Written for a web developer who has never touched a robot. Read this
> before the other files in this folder.

## What is this field, in detail?

For 50 years, programming a robot meant writing **explicit code per
task**. A pick-and-place arm had a script: "move to coordinate (0.3,
0.1, 0.5), open gripper, descend, close gripper, lift, traverse." Every
new task, every new object, every new lighting condition meant new code
written by a robotics engineer. This is why industrial robots are
common in highly controlled factories (auto assembly lines, where the
parts are always in the same place, oriented identically) and rare
everywhere else.

**Robot learning** replaces hand-written control code with a **neural
network**. Instead of programming the robot, you *show* it what to do
— either by demonstrating the task with a teleoperation rig (a human
guiding the robot), or by letting the robot practice in a simulator
with a reward signal. The network learns the mapping `(what I see) ->
(what I should do)` and generalizes (with luck) to new objects,
positions, and lighting.

The **Vision-Language-Action (VLA) model** is the current hot flavor of
this idea. Mechanically a VLA is just a **multimodal LLM** (like
GPT-4o, Claude, Gemini) with three key changes:

1. **Inputs**: camera frames from the robot's eyes + an optional text
   instruction ("put the red mug in the sink").
2. **Output head**: instead of producing text tokens, it produces
   robot actions — joint angles, end-effector poses, or gripper
   commands.
3. **Training data**: instead of trillions of web tokens, it's trained
   on millions of robot trajectories (recorded teleoperation episodes
   + simulator rollouts).

The "foundation model" framing matters because VLAs are
**pre-trained** on enormous mixed-robot data (Open X-Embodiment has
970k trajectories across 22 different robot bodies), then **fine-tuned**
on a customer's specific task with just 50-500 demonstrations. This is
the same pretrain-then-fine-tune pattern that made BERT and GPT
viable — applied to robot policies. Before VLAs, every task needed a
custom policy from scratch.

### Why this exists now (and not in 2018)

Three things converged in 2022-2024:

1. **Transformers got cheap enough** to fine-tune at billion-parameter
   scale on commodity GPUs.
2. **The data pipeline got built**: Open X-Embodiment (2023),
   BridgeData V2, DROID, LeRobot community datasets — finally enough
   training data outside of one lab's silo.
3. **Inference latency dropped** to where a 7B parameter model can run
   at 10+ Hz on a Jetson — fast enough to control a robot in the real
   world.

The first credible VLA, **RT-2** (Google, mid-2023), was the GPT-3
moment for robotics. Since then: **OpenVLA-7B** (June 2024, first
fully open), **pi0** (Physical Intelligence, Oct 2024), **NVIDIA
GR00T N1** (Mar 2025), **Figure Helix** (Feb 2025), **Google Gemini
Robotics** (2025), **pi0.5** (Apr 2025). The pace is roughly one major
release per month.

### What does the day-to-day work actually look like?

A working VLA engineer spends their time on:

- **Data engineering**: collecting / cleaning teleoperation episodes,
  converting between formats (LeRobot, RLDS, Open X-Embodiment), and
  managing terabyte-scale image datasets.
- **Fine-tuning loops**: running LoRA / full fine-tunes on cloud GPUs,
  watching W&B dashboards, tweaking learning rates and reward shapes.
- **Evaluation**: running policies in simulators (LIBERO, RoboCasa,
  Meta-World, SimplerEnv) and on real hardware, debugging
  distribution-shift failures.
- **Deployment**: quantizing, exporting to ONNX/TensorRT, wrapping
  the model in a FastAPI / ROS2 inference service, getting it to hit
  the robot's control frequency on edge hardware.

Roughly 80% of the work is Python + PyTorch + Hugging Face +
Docker — exactly the same stack a web dev who's done LLM work
already knows. The remaining 20% is robotics-specific: coordinate
frames, control rates, sim-to-real, teleoperation rigs.

---

## Three fully developed real-world use cases

These are deployed VLA systems in 2025. For each one we list the
**hardware** (what's physical) and the **software** (what's the model
+ training stack + deployment).

---

### Use case 1 — Figure 02 + Helix VLA (commercial humanoid in BMW factory)

**What it does.** Figure 02 is a 5'6" humanoid robot that performs
warehouse and factory tasks: moving totes off a conveyor, sorting
parts, picking and placing objects on shelves. Figure has been running
Figure 02 units at the BMW Spartanburg plant since 2024, doing tasks
like inserting sheet metal parts into bodyshop fixtures. The control
brain is **Helix**, a VLA that Figure announced in February 2025.

**The technical novelty.** Helix uses a **dual-system architecture**
that mirrors how human motor control is thought to work:

- **System 2**: a ~7B parameter VLM that runs at **7-9 Hz**, doing
  the slow "what should I be doing right now" reasoning given the
  scene and the task.
- **System 1**: a smaller (~80M parameter) network that runs at
  **200 Hz**, taking System 2's latent plan and producing the
  fine-grained motor commands.

This is the same idea as a fast UI thread + slow worker thread in a
web app. The fast thread keeps the robot smooth; the slow thread does
the thinking.

**Hardware stack.**

- **Robot body**: Figure 02 humanoid. 5 fingers per hand (16 DoF per
  hand), 6-DoF arm + wrist, hip + leg actuators for bipedal balance.
  Total ~40+ degrees of freedom.
- **Sensors**: stereo + RGB cameras in the head, microphones, IMU,
  joint encoders, force/torque sensors at the wrists and feet.
- **On-board compute**: Figure has confirmed an **NVIDIA RTX
  embedded GPU** on the robot for real-time inference. Helix runs
  entirely on-board (no cloud round-trip).
- **Battery**: ~5 hours of operation between charges.
- **Teleoperation rig**: VR headset + hand-trackers for human
  operators to record demonstration data.

**Software stack.**

- **Foundation model**: Helix's System 2 is reportedly a fine-tuned
  open-source VLM in the 7B range (the exact base model is
  proprietary).
- **Training framework**: PyTorch + FSDP (Fully Sharded Data
  Parallel) for multi-GPU training on Figure's internal cluster.
- **Data format**: LeRobot-compatible episode format + Figure's
  internal extensions for the dual-system labels.
- **Action representation**: continuous joint velocities for the
  high-rate System 1; latent embeddings between System 2 and
  System 1.
- **Inference runtime**: TensorRT for System 1 (the 200 Hz hot path),
  custom CUDA kernels for the System 1 / System 2 bridge.
- **Robot OS**: custom proprietary stack (not ROS); communicates
  with motor controllers over EtherCAT.

**Why this matters.** Helix is the first VLA-controlled humanoid
deployed in a real commercial factory, paying its way against
established industrial automation. If it works at scale, every BMW /
Mercedes / Ford / Honda plant becomes a customer.

---

### Use case 2 — Physical Intelligence pi0.5 (generalist tabletop manipulation)

**What it does.** Physical Intelligence's pi0 / pi0.5 family is the
most credible attempt at a **truly general** robot policy: one model
that performs novel household tasks across multiple robot bodies. In
demos, pi0.5 (April 2025) folds laundry, bus tables, makes coffee,
loads dishwashers — without per-task retraining, on robots it has
never seen during training.

**The technical novelty.** pi0 uses **flow matching** (a diffusion-
model variant) to generate continuous action chunks at high
frequency. pi0.5 adds explicit language reasoning ("first I need to
clear the table, then wipe it"), letting one model decompose long-
horizon tasks. The pi0-FAST variant compresses actions using **DCT**
(discrete cosine transform — yes, the JPEG one) so an LLM-style
discrete token decoder can output them.

**Hardware stack.**

- **Robot bodies tested**: 7-DoF Franka Emika Panda, Trossen
  WidowX 250s, Universal Robots UR5, bimanual ALOHA setups, Mobile
  ALOHA (bimanual on a mobile base). pi0 is explicitly multi-
  embodiment.
- **Sensors**: 1-3 RGB cameras (wrist-mounted + shoulder-mounted +
  scene cameras). Some setups add depth from Intel RealSense.
- **Compute during training**: thousands of NVIDIA H100 GPUs on
  Physical Intelligence's internal cluster.
- **Compute during inference**: a single RTX 4090 or A6000 is
  sufficient for a tabletop robot. Cloud inference is also
  supported.
- **Teleoperation rigs**: ALOHA leader-follower arms (~$20k each, or
  ~$5k via the LeRobot ALOHA kit) for data collection.

**Software stack.**

- **Foundation model**: pi0 is built on top of **PaliGemma** (Google's
  3B vision-language model). The action head is a flow-matching
  decoder trained on top.
- **Training framework**: JAX with Flax + Optax. Physical Intelligence
  open-sourced training code as **OpenPI** (Apache 2.0).
- **Data sources**: Open X-Embodiment (970k trajectories, 22 robot
  bodies), plus Physical Intelligence's own large internal dataset
  collected with their fleet of teleoperated robots.
- **Action representation**: continuous joint deltas, generated 50
  actions at a time (action chunking).
- **Inference**: pi0-FAST uses discrete tokenization for compatibility
  with standard LLM serving; pi0 uses continuous flow-matching
  decoding via PyTorch or JAX.
- **Robot integration**: LeRobot-compatible runtime, or direct ROS2
  bridge for industrial arms.

**Why this matters.** pi0 is **open-weights** under Apache 2.0 — you
can download it from Hugging Face today and fine-tune it on your own
task. This is the most-used open VLA in 2025 hobby and academic
robotics, and the one most relevant to "build a VLA project in your
spare time."

---

### Use case 3 — Google DeepMind Gemini Robotics (2025 generalist manipulation + planning)

**What it does.** Gemini Robotics (announced March 2025) takes
Google's flagship Gemini 2.0 model and fine-tunes it for embodied
tasks. Demonstrated capabilities: folding origami, packing a snack
box, plugging cables into ports — long-horizon tasks that require
both careful manipulation and high-level reasoning. The companion
**Gemini Robotics-ER** ("embodied reasoning") variant generates
robot code, plans, and spatial queries from a single multimodal
prompt.

**The technical novelty.** Gemini Robotics is the first VLA to
demonstrate **strong language-conditioned generalization** — it
handles instructions like "fold the paper into a fox" or "put the
green block to the left of the red one" zero-shot. It also runs in
two modes: an **on-device** small variant (low latency, manipulator
control) and a **cloud-backed** large variant (long-horizon planning).

**Hardware stack.**

- **Primary robot platform**: **Apptronik Apollo humanoid** (Google
  partnered with Apptronik in 2024 to use Apollo as the embodied
  reference platform). Apollo is a 5'8" bipedal humanoid with
  6-DoF arms and 5-finger hands.
- **Secondary platforms**: ALOHA bimanual rigs, Franka arms, and
  Google's own internal manipulation setups.
- **Sensors**: stereo cameras in the head, RGB-D cameras at the
  wrists, force/torque sensors, microphones for voice input.
- **Cloud compute**: Google TPU v5p pods for training; per-task
  fine-tuning on a small cluster.
- **Edge compute**: Apollo runs an embedded NVIDIA Jetson Thor for
  on-board inference of the smaller Gemini Robotics variant.

**Software stack.**

- **Foundation model**: **Gemini 2.0 Flash** as the VLM backbone,
  fine-tuned for robotics with action-output heads. Gemini Robotics-
  ER uses the full Gemini 2.0 Pro as the planner.
- **Training framework**: JAX on TPU pods, internal Google
  infrastructure.
- **Data sources**: massive internal dataset (RT-2 / RT-X lineage)
  plus simulator-generated data from Google's manipulation sim
  pipeline.
- **Action representation**: discrete action tokens for the small
  on-device model (RT-2-style 256-bin per-joint discretization);
  continuous for the larger Cloud variants.
- **Planning layer**: Gemini Robotics-ER outputs Python code that
  calls a library of skills — closer to the "agent" pattern in LLM
  applications than to end-to-end behavior cloning.
- **Robot integration**: Google's internal robot stack; Apptronik
  integration via custom middleware.
- **Safety layer**: a separate constraint-checker that rejects
  unsafe actions before they reach the motor controllers.

**Why this matters.** Gemini Robotics is the first VLA from a
hyperscaler that is **explicitly product-bound** (Apptronik is
selling Apollo commercially). It demonstrates that the LLM-style
"prompt + code generation" pattern works for robot planning, which
opens up the natural-language → robot DSL product category that
several startups are now targeting.

---

## What ties the three use cases together

All three systems share the same five layers:

1. **A pretrained VLM** (PaliGemma, Gemini, or a proprietary 7B-class
   model) as the perception + language backbone.
2. **An action-output head** trained on robot trajectories (discrete
   tokens, flow matching, or continuous joint deltas).
3. **A large multi-embodiment training dataset** (Open X-Embodiment,
   plus internal data).
4. **A fast inference runtime** on edge hardware (Jetson, RTX
   embedded, or custom silicon) so the policy hits 10-200 Hz.
5. **A teleoperation data-collection pipeline** to keep the model
   improving as it meets new tasks.

If you internalize these five layers, you can read the technical
blog post or paper of any new VLA and immediately know which slot
each component fills.

---

## What's next to read

- `01-examples-of-work.md` — the broader landscape of who's building
  what.
- `02-important-to-learn.md` — the layered curriculum to build the
  skills above.
- `03-how-to-start.md` — a concrete 8-week ramp-up.
- `06_courses.md` — courses (both basics + project-driven) to take.
