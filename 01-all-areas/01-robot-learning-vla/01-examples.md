# Examples of Work

This file is a tour of "things that exist in this field." If you're new,
treat it like skimming the showcase page of a JS framework: you don't
need to understand every entry, just absorb the shape of the landscape.

## Production / near-production VLAs (real robots running these today)

These are the equivalent of "GPT-4 in production" — the headline models
that the industry watches.

- **Figure Helix** (announced Feb 2025) — runs on the Figure 02
  humanoid. Uses a "System 1 / System 2" split: a small fast network
  (~200 Hz) does the low-level motor control, a big slow VLM
  (~7-9 Hz) does the reasoning. Same idea as a fast UI thread plus a
  slow worker thread.
- **Physical Intelligence pi0 and pi0.5** (Oct 2024 / Apr 2025) —
  open-weights generalist policies. "pi0" uses flow-matching (a
  diffusion-model variant) for action generation. pi0.5 added language
  reasoning and broader generalization. Physical Intelligence has a
  $2.4B valuation off these models alone.
- **Google DeepMind RT-2, RT-X, Gemini Robotics** (2023-2025) —
  Google's line of VLAs. Gemini Robotics (2025) is Gemini fine-tuned
  for embodied tasks: speech in, joint angles out.
- **NVIDIA GR00T N1** (Mar 2025) — open-weights foundation model
  aimed at humanoids. Shipped with full training code on Hugging Face.
- **Tesla Optimus** — internal-only, but Tesla has shown end-to-end
  imitation policies for laundry-folding, factory work, etc.
- **1X NEO + World Model** (2024-2025) — 1X uses a generative video
  model as the "imagined future" for planning. Think of it as letting
  the policy hallucinate the next 5 seconds before deciding what to do.
- **Skild AI "Skild Brain"** (2024) — a single policy meant to be
  dropped onto many different robot bodies.

## Landmark research papers (the canon — read these eventually)

The papers that shaped the modern VLA stack. Order matters: each builds
on the previous.

- **RT-1 -> RT-2 -> RT-X** (Google, 2022-2023) — RT-2 was the first
  big demonstration that you can take an off-the-shelf vision-language
  model (PaLI-X) and fine-tune it to output robot actions. This is
  the "GPT-3 paper" moment for robotics.
- **Open X-Embodiment** (CoRL 2023, updated 2024) — 21 institutions
  pooled their robot data: ~970k trajectories across 22 different
  robot bodies. People call this "the ImageNet moment for robotics"
  because suddenly there was a big shared dataset.
- **OpenVLA-7B** (Stanford / Berkeley, June 2024) — first fully open
  VLA, fine-tunable on a single A100 GPU. If you only run one model
  hands-on, run this one.
- **Diffusion Policy** (Chi et al., RSS 2023) — uses a diffusion
  model (same math as Stable Diffusion, but generating actions instead
  of pixels) for the policy. State of the art on a lot of benchmarks.
- **ACT / ALOHA** (Zhao et al., Stanford 2023) — introduced
  "action chunking" (predict the next 50 actions instead of just one)
  and a $20k bimanual teleop rig. The follow-up "Mobile ALOHA" went
  viral on Twitter for cooking shrimp.
- **pi0 / pi0-FAST / pi0.5** (Physical Intelligence, 2024-2025) —
  flow-matching for high-frequency control. pi0-FAST uses DCT
  (discrete cosine transform — yes, the JPEG one) to compress actions
  into tokens an LLM can output.
- **HumanPlus, OKAMI, H1-2 policies** (2024) — humanoids that imitate
  poses from regular human YouTube video.
- **DreamerV3, TD-MPC2** — the world-model branch of robot learning:
  the network learns to predict what happens next, then plans against
  its own imagination.

## Open-source stack (the equivalent of "npm packages you'll actually use")

- **LeRobot** (Hugging Face) — the closest thing to a Rails for robot
  learning. Includes dataset format, training scripts, model zoo, and
  drivers for cheap arms (SO-100, Koch, ALOHA).
- **OpenVLA, pi0-base, RDT-1B, Octo** — open-weight VLA checkpoints
  on Hugging Face. Download and `model.generate()`.
- **Open X-Embodiment, BridgeData V2, DROID** — the big public
  training datasets.
- **Robosuite, RoboCasa, LIBERO, Meta-World** — simulator benchmarks.
  Like Jest test suites for policies.
- **OpenPI** (Physical Intelligence) — official training code for the
  pi0 family. Apache-2.0 licensed.
