# Four Projects You Can Build and Sell

## 1. Custom Isaac Lab training environment as a service (~3-4 weeks)

Customer describes a task and provides assets; you deliver a
parameterized Isaac Lab environment with domain randomization, reward
shaping, and a baseline PPO/SAC training script.

- **Stack:** Isaac Sim + Isaac Lab + USD asset cleanup, Replicator for
  DR, W&B for tracking.
- **Buyers:** robotics startups that lack an Isaac Lab specialist.
- **Pricing:** $15-60k per environment; recurring fee for updates.

## 2. Procedural warehouse / factory generator (~4 weeks)

Tool that takes a CAD floor plan and generates hundreds of randomized
USD scenes (lighting, object placement, clutter, agents) for training
mobile robots and perception models.

- **Stack:** USD Python API, BlenderProc for procedural placement,
  Replicator for randomization, optional Omniverse Kit extension.
- **Buyers:** AMR companies, warehouse-automation primes.
- **Pricing:** $20-80k license + $1-5k/mo support.

## 3. Sim2Real domain randomization toolkit (~3 weeks)

Python package + small web UI that wraps Isaac Sim / MuJoCo and exposes
randomization knobs (physics, textures, lighting, dynamics) with sensible
presets per robot type. Commercial license + paid support.

- **Stack:** Isaac Lab / MJX wrappers, YAML config DSL, Hydra,
  Streamlit dashboard.
- **Buyers:** mid-tier robotics teams without a dedicated sim engineer.
- **Pricing:** $5-25k/yr license + onboarding.

## 4. Synthetic data pipeline for vision models (~3 weeks)

Customer specifies object classes and a scene type; you return 100k
labeled synthetic images + 3D bounding boxes for training detectors and
pose estimators.

- **Stack:** Replicator + BlenderProc, photoreal materials, automated
  COCO/BOP annotation export, pre/post fine-tuning eval.
- **Buyers:** defense (counter-UAS), industrial QC, retail self-checkout.
- **Pricing:** $5-50k per dataset depending on diversity.
