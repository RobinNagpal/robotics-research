# Four Projects You Can Build and Sell

## 1. VLA fine-tuning service for niche tasks (~3 weeks)

Take OpenVLA-7B or pi0-base; build a clean fine-tuning pipeline that
takes 50-200 customer demonstrations and produces a deployable policy
for one specific repetitive task (warehouse pick-pack subtypes, lab
pipetting, retail shelf-stocking, kitchen prep).

- **Stack:** LeRobot dataset format, OpenVLA / pi0 fine-tuning,
  LoRA + 8-bit, eval on a fixed holdout, deployable container.
- **Buyers:** integrators, automation shops, robot OEMs with no ML team.
- **Pricing:** $15-50k per task setup; recurring fee for updates.

## 2. Synthetic demonstration generator (~3 weeks)

Tool that takes a single human teleoperated demo and generates 1,000+
augmented variations (object positions, lighting, distractors,
viewpoints) for VLA training.

- **Stack:** Isaac Sim Replicator or MuJoCo MJX + a kinematic replay
  layer + diffusion-based image augmentation (Stable Diffusion + IP-Adapter).
- **Buyers:** robotics startups burning cash on data collection.
- **Pricing:** SaaS credit pack ($0.05-$0.20 per generated episode) or
  $2-10k flat per dataset.

## 3. VLA evaluation harness (~2-3 weeks)

Customer uploads a policy checkpoint; you return a benchmark report
across LIBERO, RoboCasa, Meta-World, with success rates, generalization
scores, failure-mode taxonomy, and a per-task PDF.

- **Stack:** dockerized eval workers on GPU, parallel rollout, automated
  failure clustering with CLIP embeddings, PDF report generator.
- **Buyers:** robotics teams that have policies but no rigorous eval.
- **Pricing:** $500-$2k per run, $1-5k/mo subscription for nightly
  regression suite.

## 4. Natural-language -> robot task DSL (~4 weeks)

Web tool where a non-technical operator types "pick up red blocks and
place them in the bin on the left, ignore green ones" and outputs a
structured task spec + few-shot examples that a downstream VLA consumes.

- **Stack:** LLM (Claude / GPT) with a structured task schema, prompt
  examples derived from RoboCasa, optional sim demo loop.
- **Buyers:** robot OEMs, no-code automation platforms, integrators.
- **Pricing:** $20-100k licensing per OEM; SaaS for SMBs.
