# Foundation models — VLAs & generalist robot policies (the learned upgrade path)

> **Why this doc exists.** The per-layer guides recommend an
> **analytical-first** stack for v1 — analytical motion and grasping,
> with **YOLO object detection** (trained on synthetic data from the
> twin) for perception — the right call for *one known vial in a known
> tray*. But the fast-moving frontier
> of robotics is **learned generalist policies**: Vision-Language-Action
> (**VLA**) models that take camera frames + a text instruction and emit
> robot actions end-to-end. This doc is the **canonical comparison** of
> the leading models (open and closed) so the team can (a) speak to them
> credibly in a sales call, and (b) know exactly *where* one would slot
> into our stack and *when* it earns its keep. Every other doc that
> mentions a VLA links back here instead of re-listing them.

> **Disclaimer.** This space moves monthly — versions, licences,
> benchmarks, and "open vs closed" status drift fast. Figures are
> approximate (`~`) and reflect **~mid-2026**; re-verify every claim
> before quoting it to a client.

---

## What a VLA / generalist policy actually is

A classic stack (our v1) is a **pipeline**: perception finds the vial
(Layer 04), an analytical method computes a grasp (Layer 05), MoveIt
plans the motion (Layer 03), and a behavior tree sequences it (Layer
07). Each stage is hand-built and inspectable.

A **VLA model** collapses much of that pipeline into **one trained
neural network**. You give it images (and often proprioception — the
arm's joint state) plus a **language instruction** like *"pick up the
vial and place it in slot A3,"* and it outputs **low-level actions**
(joint or end-effector motions) directly, at some control rate. It
learns the perception→grasp→motion mapping from **demonstration data**
rather than from explicit geometry.

> **Where it sits in our 8 layers.** A VLA is not a new layer — it is an
> **alternative implementation that cuts across most of them**. Its
> centre of gravity is **Layer 05 (grasping/manipulation)**, where we
> file it, but be clear in a conversation that it also: **subsumes Layer
> 04 (perception)** and parts of **Layer 03 (motion)** and **Layer 07
> (orchestration)**; is **trained and evaluated in Layer 01 (the
> simulator / digital twin)**, which doubles as its synthetic-data
> factory; runs on **Layer 02 (control)** with real latency/QoS
> concerns; and **collides with Layer 08 (compliance)**, where a
> black-box policy is hard to validate. About the only layer it leaves
> alone is **Layer 06 (barcode)**. Each of those layer files links back
> here.

**The trade in one line:** the analytical pipeline is cheap, exact,
deterministic, and *explainable* for one known task; a VLA is expensive,
data-hungry, and a black box, but it **generalizes** to new vials,
labware, layouts, and spoken instructions in a way hand-coded geometry
never will. For v1 we stay analytical; the VLA is the **deliberate later
upgrade** once "handle anything the lab throws at it" becomes the goal.

---

## The five at a glance

| Model / ecosystem | Who | Open? | Sweet spot | Bottom line |
|---|---|---|---|---|
| **π0 / π0.5 / π0.6** (openpi) | Physical Intelligence | **Open weights + code** | Dexterous, multi-task manipulation; strongest *open* flagship | Best open VLA to actually adopt; flow-matching policy, runs via openpi or LeRobot. |
| **Gemini Robotics 1.5 / -ER / On-Device** | Google DeepMind | Mostly **closed** (On-Device + ER via API/SDK) | Frontier reasoning + dexterity; "thinks before acting" | The capability ceiling, but gated access; On-Device is the fine-tunable, local piece. |
| **OpenVLA (+ OFT)** | Stanford/Berkeley/TRI et al. | **Open weights + code** | A clean 7B open baseline to fine-tune | The well-documented learning/teaching baseline; OFT makes fine-tuning fast and inference real-time. |
| **Isaac GR00T N1.5 / N1.7** | NVIDIA | **Open (Apache-2.0)** | Sim-native training + synthetic data; humanoid-leaning but generalist | Best if you live in Isaac Sim and want a synthetic-data pipeline; heavier, GPU/Isaac-centric. |
| **LeRobot + SmolVLA** | Hugging Face | **Open** | The practical on-ramp: data, training, a tiny model that runs cheap | Where to *start* — hosts π0/ACT/Diffusion-Policy, plus a 450M model that runs on consumer hardware. |

> Two of these are **ecosystems** (openpi, LeRobot) that host multiple
> models, and two are **model families** (Gemini Robotics, GR00T); they
> overlap (LeRobot can run π0 and SmolVLA). They are grouped this way
> because that is how you'd actually choose between them.

---

## Physical Intelligence — π0 / π0.5 / π0.6 (openpi)

**Physical Intelligence (Pi)** open-sourced **π0** ("pi-zero") via the
**`openpi`** repo — a VLA built on a vision-language backbone with a
**flow-matching** action head that generates smooth continuous actions
by iterative denoising. Variants matter: **π0-FAST** tokenizes actions
for faster autoregressive generation; **π0.5** (`~`Sept 2025) adds much
better **open-world generalization** via a hierarchical design (predict
a high-level sub-task in words, then the low-level action) and "knowledge
insulation"; **π0.6** (`~`recent) adds **reinforcement-learning
fine-tuning**. All are pre-trained on `~`10,000+ hours of diverse robot
manipulation data, and the models are runnable from both `openpi` and
**LeRobot** (JAX and PyTorch).

Its strength is being the **strongest genuinely open flagship** — open
weights *and* training code you can fine-tune on your own arm and task.
For a small agency this is the most credible "we can actually deploy a
modern VLA" option, because nothing is gated behind a partner program.
It is built for exactly the dexterous, multi-step manipulation our HPLC
cell needs (pick, place, insert), and the hierarchical π0.5 is the
closest open model to following plain-language task instructions.

Its weakness is the universal VLA cost: it wants a **GPU**, a pile of
**demonstrations** to fine-tune well, and careful evaluation, and like
all learned policies it is a **black box** that is hard to validate for
a regulated lab. Versus Gemini Robotics it is a notch behind on
frontier reasoning; versus the analytical pinch it is wildly heavier for
*one known vial*. It is the open model to **grow into**, not the v1
starting point.

## Google DeepMind — Gemini Robotics 1.5 / -ER / On-Device

Google DeepMind's **Gemini Robotics** family is the frontier. **Gemini
Robotics 1.5** is a VLA that "**thinks before acting**" — it produces an
explicit reasoning trace before motor commands — and is available to
*select partners* only. **Gemini Robotics-ER 1.5** ("embodied
reasoning") is a VLM that reasons about the physical world, calls
digital tools, and builds multi-step plans; it is reachable by
developers through the **Gemini API in Google AI Studio**. **Gemini
Robotics On-Device** is a VLA **optimized to run locally on the robot**,
works without a network (low latency, robust to connectivity), and
**adapts to a new task with as few as `~`50–100 demonstrations**, with a
public **`gemini-robotics-sdk`**.

Its strength is **raw capability and reasoning**: the broad world
knowledge of Gemini, an explicit plan/think step (genuinely useful for a
multi-station workflow), and — via On-Device — **fast local fine-tuning
from a handful of demos**, which is a remarkable data efficiency versus
training an open model from scratch. The -ER model is also a credible
**high-level planner** that could sit above our behavior tree.

Its weakness is **access and openness**: the most capable pieces are
**closed / partner-gated**, so you cannot freely self-host or audit them,
and an API dependency is a hard sell for an air-gapped, validated lab.
Pricing and availability are moving targets. For our open-source-first
positioning, Gemini Robotics is the **"frontier we track and can
integrate where allowed,"** not the default build.

## OpenVLA (+ OFT)

**OpenVLA** is a **7B-parameter open** VLA (`~`2024, Stanford/Berkeley/
Google/TRI) trained on the **Open X-Embodiment** dataset (1M+ episodes,
22 embodiments). It fuses **DINOv2 + CLIP** vision features with a
**Llama-2** backbone and outputs discrete action tokens; on release it
beat the (closed) RT-2 on a manipulation suite despite being smaller.
The **OFT** ("Optimized Fine-Tuning") recipe (`~`2025) then made it
**25–50× faster at inference**, with higher success rates, multi-image
input, and high-frequency bimanual control.

Its strength is being the **clean, well-documented open baseline** — the
model most teams *learn* VLAs on, with abundant tutorials, fine-tuning
(LoRA) examples, and a large community. For our purpose it is the ideal
**"hello world" of VLAs**: fine-tune it on a few simulated or real vial
picks and see a learned policy work end-to-end. OFT removes its biggest
early drawback (slow inference).

Its weakness is that, vanilla, it is **heavier and older** than π0.5 /
SmolVLA and was **clumsy to run in real time** before OFT; it is a
strong baseline rather than the current capability leader. For a tiny
deployable model you'd reach for SmolVLA; for the strongest open policy,
π0.5. OpenVLA's lasting value is as the **teaching/benchmark** rung.

## NVIDIA — Isaac GR00T N1.5 / N1.7

**Isaac GR00T** is NVIDIA's **open (Apache-2.0)** foundation model for
generalist robots — a **dual-system** VLA (a fast "action" system under a
slower "reasoning" VLM). **N1.5** improved grounding (Eagle-2.5 VLM) and
benefited from the **DreamGen** synthetic-data pipeline; **N1.7**
(`~`early-access 2026) adds a new VLM backbone and large-scale human-video
pretraining, and is slated to be fully open-sourced. Its natural home is
the **NVIDIA Isaac Sim / Isaac Lab** simulation world, with tooling
(GR00T-Mimic/Dreams) to **generate synthetic demonstrations** so you can
train without hand-collecting thousands of real episodes.

Its strength is the **sim-native, synthetic-data story** — exactly aligned
with a *simulation-first* agency. If you adopt Isaac Sim (the proprietary-
but-free simulator we list as an alternative to Gazebo), GR00T gives you a
foundation policy plus a way to manufacture training data in sim and
domain-randomize it. It is open and commercially licensable, and it scales
to dexterous, two-armed, even humanoid platforms.

Its weakness for *this* project is **fit and weight**. GR00T is
**humanoid-leaning** and tied to the **NVIDIA stack** (Isaac Sim, capable
GPUs), which is heavier than our Gazebo + ROS 2 default and than a
single-arm desktop cobot needs. The payoff is real only if you commit to
Isaac. For a myCobot-class single-arm cell, π0.5 or SmolVLA via LeRobot is
a lighter path; GR00T is the choice when the **sim + synthetic-data**
pipeline is the point.

## Hugging Face — LeRobot + SmolVLA

**LeRobot** is Hugging Face's **open robotics framework** — not one model
but the **hub**: datasets, training recipes, low-cost-arm support, and a
model zoo that includes **ACT**, **Diffusion Policy**, **π0**, and more.
**SmolVLA** is its own **compact (~450M) open VLA**, pairing a SmolVLM-2
vision-language model with a flow-matching action expert, trained
**entirely on community LeRobot data** — and it reportedly **outperforms
much larger VLAs and the ACT baseline** while running on **consumer
hardware**.

Its strength is being the **practical on-ramp** for a small team. It
standardizes the unglamorous 80% — recording teleop demonstrations,
formatting datasets, training, and evaluating — and lets you run a tiny
model **without a datacenter GPU**. Because it can host π0 and others, you
can start with SmolVLA to learn the workflow, then swap in a bigger policy
without changing your data pipeline. This is where the team should
*begin* any VLA experiment.

Its weakness is **ceiling**: a 450M model is, by design, less capable on
the hardest, most varied tasks than π0.5, Gemini Robotics, or a
fine-tuned GR00T. Its low-cost-arm support centres on the SO-100/SO-101-
class arms; **myCobot 280 support is community-dependent** (verify) and
may need a custom data/driver bridge. SmolVLA is the right *first* VLA,
not necessarily the *final* one.

---

## How a VLA would apply to our HPLC cell

- **only-code mode** (the per-layer guides in this folder): you can
  **evaluate and fine-tune pretrained policies in simulation** with *zero
  hardware* — roll out OpenVLA/π0/SmolVLA on a sim benchmark (LIBERO,
  SIMPLER, ManiSkill) or GR00T in Isaac Lab, generate **synthetic
  demonstrations**, and measure success on a simulated vial-pick. This
  proves the *learning workflow* before a cent is spent.
- **code-plus-hardware mode:**
  you **collect teleop demonstrations on the real arm** (LeRobot's
  recorders), **fine-tune** (LoRA / OFT, or ~50–100 demos for Gemini
  On-Device), and **deploy on-device** — now confronting real inference
  **latency**, **GPU placement**, and **safety** (a black-box policy
  driving a real arm near glass needs the same safety gates from the
  [sensor suite](sensor-suite.md) wrapped around it).

**Compliance reality check.** A learned, non-deterministic policy is hard
to square with **21 CFR Part 11 / IQ-OQ-PQ** validation (you must show the
system does the same correct thing every time). In a regulated lab the
likely pattern is **analytical/deterministic for the validated critical
path, VLA for flexible or non-GxP steps** — say so honestly to a client
rather than overselling end-to-end learning.

---

## Verdict — what to actually do

- **For v1: don't.** Keep the **analytical pinch + MoveIt + behavior
  tree** (Layers 03/05/07). For one known vial it is cheaper, exact,
  explainable, and validatable.
- **To learn VLAs (the on-ramp): LeRobot + SmolVLA** — record a few demos,
  fine-tune the small model, run it in sim. Lowest cost, best docs.
- **Best open model to grow into: π0.5 (openpi)** — the strongest open
  flagship, instruction-following, runnable via LeRobot.
- **Frontier to track / integrate where allowed: Gemini Robotics
  (On-Device + ER)** — most capable, but access-gated and closed.
- **If you commit to Isaac Sim: GR00T N1.5/N1.7** — for its sim-native
  synthetic-data pipeline.
- **As a teaching baseline: OpenVLA (+ OFT)**.

The honest agency line: *"v1 is deterministic and validatable; we track
and can deploy the VLA frontier (π0.5, Gemini Robotics, GR00T) as the
generalization upgrade when your task variety justifies it."*

---

## See also

- The layer this lives under: grasping & manipulation —
  [`05-grasping-and-manipulation.md`](05-grasping-and-manipulation.md).
- Perception it can subsume:
  [`04-perception-and-vision.md`](04-perception-and-vision.md).
- Orchestration it can subsume (and -ER could plan above):
  [`07-orchestration-and-task-logic.md`](07-orchestration-and-task-logic.md).
- Where it's trained / its data factory:
  [`01-simulation-and-digital-twin.md`](01-simulation-and-digital-twin.md).
- Motion it can emit directly (vs MoveIt):
  [`03-arm-motion-planning.md`](03-arm-motion-planning.md).
- The compliance tension it raises:
  [`08-software-worklist-and-compliance.md`](08-software-worklist-and-compliance.md).
- The safety/sensor gates any deployed policy must respect:
  [`sensor-suite.md`](sensor-suite.md).
- The learning plan that includes a VLA hello world:
  [`../06-learning-checklist.md`](../06-learning-checklist.md).
- Folder index: [`README.md`](README.md).
