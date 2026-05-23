# Robot Learning & Foundation Models (VLA)

> Written for someone whose day job is React / Node / TypeScript and who
> has never touched a robot. We'll define every term and lean on
> analogies from web development.

## What is this subfield, in one paragraph?

Traditionally, a robot was programmed task-by-task: an engineer wrote
explicit code to "move arm to coordinate X, close gripper, lift, place."
That doesn't scale. **Robot learning** replaces that hand-written code
with a neural network — you show the robot what to do (or let it
practice in simulation), and the network figures out the motor commands.

The hottest flavor right now is the **Vision-Language-Action (VLA)
model**. Think of it as a multimodal LLM (like GPT-4o or Gemini) that:

- takes in **camera frames** + a **text instruction** ("put the red mug
  in the sink"),
- and outputs **robot joint angles** or **gripper commands** instead of
  text tokens.

If you've used a vision-language model to caption images, a VLA is the
same architecture — just with a different output head.

## Why is this called a "foundation model"?

Same reason GPT is. You pre-train one large model on a giant pile of
robot data (millions of demos across hundreds of tasks), then
**fine-tune** it for whatever specific job a customer needs. This is
the same workflow as taking a pretrained CLIP/LLaMA off Hugging Face
and adapting it to your app — except the "tokens" are robot actions.

## Why is this one of the top-3 picks?

- **Highest pay in robotics.** ML / VLA engineers regularly hit
  $300k-$600k total compensation at top startups (Physical Intelligence,
  Figure, Skild, NVIDIA GEAR). Source: 2025 Robotics Salary Guide,
  startup levels.fyi data.
- **Almost entirely software.** You can do 80% of this work from a
  laptop + cloud GPU. Hardware is optional (you can rent simulator
  time, or buy a $100 SO-100 arm).
- **The field is brand new.** RT-2 (the first real VLA) is from
  mid-2023. The open-source stack (OpenVLA, LeRobot, pi0-base) only
  arrived in 2024. A web dev who learns the basics in 3 months is not
  behind anyone — there isn't a behind yet.
- **Pulls from skills you may already have.** PyTorch, HuggingFace,
  Docker, GPU rentals, Python web servers. The hard parts are ML
  intuition and patience, not exotic robotics tooling.

## Files in this folder

- [01-examples-of-work.md](01-examples-of-work.md) — what's been built
- [02-important-to-learn.md](02-important-to-learn.md) — what to study
- [03-how-to-start.md](03-how-to-start.md) — week-by-week ramp-up
- [04-major-new-employers.md](04-major-new-employers.md) — who hires
- [05-projects-to-sell.md](05-projects-to-sell.md) — what to ship

## Glossary (read this once before the other files)

- **Policy** — the function `(observation) -> action`. In web terms,
  the request handler. The neural network IS the policy.
- **Action** — what the robot does this tick. Usually a small vector:
  joint angles, end-effector pose, or gripper open/close.
- **Episode / trajectory** — one recorded attempt at a task (like a
  Cypress test recording). Datasets are collections of episodes.
- **Imitation learning (IL)** — supervised learning where the labels
  are "what the human teleoperator did." Behavior cloning is the
  simplest form.
- **Reinforcement learning (RL)** — the robot tries actions, gets a
  reward signal, and learns by trial and error. A/B testing taken to
  its logical extreme.
- **Teleoperation** — a human controlling the robot live (VR headset,
  joystick, leader arm) to record demonstrations.
- **Sim-to-real** — train in a simulator (free, fast), deploy on a
  real robot (expensive, slow). The gap between the two is what
  research papers call the "reality gap."
- **End-effector** — the business end of a robot arm: gripper, hand,
  suction cup.
- **DoF (degrees of freedom)** — how many independent joints. A
  typical arm is 6-7 DoF; a humanoid is 30-50.
