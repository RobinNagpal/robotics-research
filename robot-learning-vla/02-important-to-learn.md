# Important Things to Learn

## ML foundations (assume Stanford CS229 + CS231n level)

- Transformers end to end (Karpathy nanoGPT, GPT-from-scratch).
- VLMs: CLIP, SigLIP, LLaVA, PaliGemma — understand how vision tokens
  are fused with language.
- Diffusion models: DDPM, DDIM, score-based, flow matching.
- Tokenization for actions (RT-2 style discrete bins; pi0-FAST DCT;
  continuous via diffusion).

## Robot learning fundamentals

- **Imitation learning:** behavior cloning, DAgger, action chunking
  (ACT), diffusion policies.
- **Reinforcement learning:** PPO, SAC, TD3; offline RL (CQL, IQL,
  TD3+BC); world-model RL (Dreamer, TD-MPC2). RL is a +33% salary skill.
- **Sim-to-real:** domain randomization, system identification,
  RMA-style adaptation, real-to-sim distillation.
- **Multi-task / generalist policies:** Open X-Embodiment, RT-X
  recipes.

## VLA-specific

- Read RT-1, RT-2, OpenVLA, pi0, pi0.5, Octo, RDT papers end to end.
- Understand action heads: discrete-bin, MLP regression, diffusion,
  flow-matching.
- Data: how to collect, version, clean, and curate teleop datasets;
  LeRobot dataset format.
- Inference: 5-30 Hz constraints, action chunking, async inference.

## Tools and infra

- PyTorch 2.x, HuggingFace Transformers, Accelerate, FSDP, DeepSpeed.
- LeRobot, OpenPI, robosuite, MuJoCo / MJX, Isaac Lab.
- W&B or MLflow for experiment tracking.
- vLLM / TensorRT-LLM for deployment (yes, VLAs use the same serving
  infra as LLMs).

## Must-read papers (in order)

1. RT-1, RT-2
2. ACT / Aloha
3. Diffusion Policy
4. Open X-Embodiment + RT-X
5. OpenVLA
6. pi0 + pi0-FAST + pi0.5
7. Dreamer V3 / TD-MPC2 (for the RL world-model wing)
