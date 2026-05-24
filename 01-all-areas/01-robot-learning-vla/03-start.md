# How the Team Ramps on VLA

A concrete 8-week plan our team works through to build VLA delivery
capability. The goal isn't to read everything — it's to ship a
working policy the team can demo end to end, both as an internal
reference build and as a credibility-anchor demo for client pitches.
Treat it like learning a new web framework: build a toy project
first, then go back and read the docs that suddenly make sense.

## Prerequisites (1 week, can overlap with Week 1)

- Comfortable Python.
- A Hugging Face account.
- A GPU. You have three options:
  - **Rent**: Lambda Labs, RunPod, Modal, Vast.ai. ~$0.40-$2/hr
    for an A100/H100. This is by far the easiest start.
  - **Colab Pro** ($10/mo) — fine for tutorials, not for fine-tuning a
    7B VLA.
  - **Local 24GB GPU** (RTX 3090 / 4090) — great if you already own one.
- Basic Git + Docker.

## Week 1: Stand up the stack and run inference

Goal: load a pretrained VLA and watch it produce actions.

- Install [LeRobot](https://github.com/huggingface/lerobot) — follow
  the README. It's a `pip install` + a couple of dataset downloads.
- Run the LeRobot "pretrained policy in simulation" tutorial. You
  should see a sim robot in a window doing a task.
- Download **OpenVLA-7B** from Hugging Face. Run inference on a
  single image + instruction. Print the action it predicts. Don't
  worry that the action is meaningless yet — the goal is "I can
  call `.generate()` on a VLA."
- Read the README files of LeRobot and OpenVLA cover to cover.

## Week 2: Train a small policy from scratch

Goal: get the "hello world" of imitation learning working.

- Use LeRobot to train **ACT** or **Diffusion Policy** on the bundled
  **PushT** dataset (cursor pushing a block — a 2D toy task) or the
  **ALOHA-Sim** insertion dataset.
- Reproduce the published success rate (typically 80-95%). When you
  hit it, you've validated your pipeline.
- Skim the LeRobot source for the trainer loop. It's only ~500
  readable lines.

## Week 3: Fine-tune a real VLA

Goal: take a pretrained 7B model and adapt it.

- Pick a small slice of **BridgeData V2** (~200 episodes of a single
  task) or record your own teleop data if you have hardware.
- Fine-tune OpenVLA-7B with **LoRA** (low-rank adapters — same trick
  used to fine-tune LLaMA). This makes training fit on a single
  24GB GPU.
- Compare zero-shot vs fine-tuned success rate on **LIBERO** (a
  standard benchmark — 130 tasks split into 4 suites).

## Week 4: Sim deployment or real deployment

Goal: see your policy control something.

**Path A (sim only):** run your fine-tuned policy in **RoboCasa**
(kitchen tasks, runs on Robosuite/MuJoCo). You'll get a video.

**Path B (real hardware):** if you have or rent an arm, deploy it.
Cheap options below.

## Weeks 5-8: Ship one substantial internal reference build

Pick something the shop can keep as an internal reference and reuse
as a credibility-anchor demo when pitching VLA work to clients.
Some patterns we've found land well in sales conversations:

- A LeRobot fine-tune for one specific task with a clean internal
  repo, demo video, and a HF model card we can show to prospective
  clients.
- A "VLA inference server" that wraps OpenVLA in a FastAPI app —
  POST an image + instruction, get back actions. Add streaming.
  Doubles as the deployment template we reuse across engagements.
- A benchmark dashboard that runs LIBERO on every commit (CI for
  policies). Easy to walk a client through; also the eval harness
  we ship inside client repos.
- A small dataset the team collected with an SO-100 arm, uploaded
  to Hugging Face Datasets, with a baseline policy trained on it.
  Useful as a teleop-pipeline reference for clients who haven't
  collected demonstrations before.

## Datasets you should know by name

- **Open X-Embodiment** — 970k trajectories, 22 robots. The big one.
- **BridgeData V2** — Berkeley, single-arm tabletop manipulation.
- **DROID** — Stanford et al., 2024, ~76k trajectories across many
  scenes; high quality.
- **LeRobot community datasets** — small but growing fast.
- **RT-1 data** — Google's original, single robot, kitchen tasks.

## Benchmarks (so you can compare your numbers to papers)

- **LIBERO** — 130 tasks, four suites (spatial, object, goal, long).
- **RoboCasa** — large kitchen sim built on Robosuite.
- **Meta-World MT-50** — 50 tabletop tasks; an old but standard RL
  benchmark.
- **SimplerEnv** — sim that's calibrated to match real WidowX / Google
  Robot setups, so sim scores predict real-world scores.
- **CALVIN** — long-horizon language-conditioned tasks.

## Cheap hardware (optional but motivating)

Prices fluctuate; ranges below reflect Q1 2025:

- **SO-100 / SO-ARM100** (~$100-$200 in parts) — 6-DoF arm designed
  by Hugging Face's LeRobot team. The cheapest path to real-robot
  experiments.
- **Koch v1.1** (~$500-$700 in parts) — leader-follower bimanual
  teleop, also LeRobot-native.
- **LeRobot ALOHA kit** (~$5k) — full bimanual ALOHA pipeline at
  about a quarter of the original $20k cost.
- **WidowX 250s** (Trossen Robotics, ~$5-6k) — used in BridgeData and
  many OpenVLA experiments.

## Communities

- **CoRL, RSS, NeurIPS** robotics workshops (papers + recorded talks).
- **LeRobot Discord** — most beginner-friendly.
- **OpenVLA Slack** — research-leaning.
- **r/robotics, r/MachineLearning** — for general lurking.
- X/Twitter: @chelseabfinn, @svlevine, @kvfrans, @physical_int,
  @drjimfan.
