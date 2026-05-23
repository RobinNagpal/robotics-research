# How to Get Started

## Week 1: Set up the stack

- Install LeRobot from HuggingFace; run the SO-100 / Koch tutorials in
  simulation.
- Pull OpenVLA-7B from HuggingFace; run inference on a sample episode.
- Get one cloud GPU (Lambda / RunPod / Modal) with at least 24 GB.

## Week 2: Train a small behavior-cloning policy

- Use LeRobot to train ACT or Diffusion Policy on the pre-built PushT or
  Aloha-Sim datasets.
- Hit the published numbers; understand exactly which knobs matter.

## Week 3: Fine-tune a real VLA

- Fine-tune OpenVLA-7B on the BridgeData V2 subset or your own small
  LeRobot dataset (~100 episodes).
- Compare zero-shot vs fine-tuned success rate on LIBERO or RoboCasa.

## Week 4: Sim-to-real or simulator-only deployment

- Run your fine-tuned policy in Robosuite or RoboCasa with a robot arm.
- If you have a real arm (SO-100 ~$300, Koch ~$500, or rent time on a
  university Aloha), deploy and iterate.

## Datasets to know

Open X-Embodiment (970k traj), BridgeData V2, DROID (Stanford), RT-1
data, LIBERO, RoboCasa, Meta-World, RoboMimic, ALOHA datasets.

## Benchmarks

LIBERO (4 task suites), RoboCasa (kitchen tasks), Meta-World (MT-50),
SimplerEnv (real-to-sim transfer), CALVIN.

## Cheap hardware to own

- **SO-100** (~$300) — Hugging Face's 6-DoF arm, LeRobot-native.
- **Koch v1.1** (~$500) — leader-follower bimanual teleop.
- **LeRobot Aloha kit** (~$5k) — bimanual + base, full ACT pipeline.
- **WidowX 250s** (~$2k) — BridgeData / OpenVLA native.

## Communities

CoRL, RSS, NeurIPS robotics workshops; LeRobot Discord; OpenVLA Slack;
Physical Intelligence newsletter; X/Twitter: @chelseabfinn,
@svlevine, @kvfrans, @physical_int.
