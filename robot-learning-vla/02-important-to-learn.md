# Important Things to Learn

If you're coming from web dev, the gap is mostly **ML fundamentals**
and **a small amount of robotics vocabulary**. The good news: VLAs use
the same PyTorch + Hugging Face + GPU stack as LLMs, so a lot of
infrastructure knowledge transfers.

## Layer 1: Python + ML basics

Assume you already have Python at the same level you have JS. If not,
spend a week on:

- Python type hints, dataclasses, pathlib, venv / uv.
- **NumPy** — think of it as lodash for numeric arrays.
- **PyTorch** — the neural net library. The mental model: a tensor is
  a multi-dimensional array, and `requires_grad=True` is like setting
  up reactive state — PyTorch tracks every operation so it can
  auto-compute gradients later. Watch Karpathy's "neural networks
  zero-to-hero" series; it's the best free intro that exists.

If you have time, two short Stanford courses are the canonical baseline:
**CS231n** (convnets — vision) and **CS229** (general ML). You don't
need to do the homework; the lecture videos are enough.

## Layer 2: Modern deep learning building blocks

- **Transformers** — the architecture under every LLM and VLA. Build
  one from scratch with Karpathy's nanoGPT (~300 lines). Once you've
  done that, "attention" stops being a magic word.
- **Vision-language models (VLMs):** CLIP, SigLIP, LLaVA, PaliGemma.
  These take pixels + text and produce a shared embedding. A VLA is
  literally a VLM with a different output head.
- **Diffusion models:** DDPM, DDIM, score matching, flow matching.
  Same math that powers Stable Diffusion, but for generating action
  sequences instead of images.
- **Tokenization for actions** — how do you cram a continuous joint
  angle into a discrete token an LLM can output? Three popular
  answers: (a) bucket each joint into 256 bins (RT-2 style),
  (b) DCT-compress chunks of actions (pi0-FAST), (c) skip discretization
  and use diffusion to generate continuous actions directly.

## Layer 3: Robot-learning-specific topics

- **Imitation learning (IL):**
  - *Behavior cloning*: supervised learning, label = "what the human
    did." Easy, but fragile — if the robot deviates from the
    training distribution it's lost.
  - *DAgger*: behavior cloning + interactive corrections.
  - *Action chunking (ACT)*: predict 50 actions in one shot. Solves a
    lot of the fragility.
  - *Diffusion policies*: the current default for high-quality IL.
- **Reinforcement learning (RL):** PPO, SAC, TD3 are the staple
  algorithms. **Offline RL** (CQL, IQL, TD3+BC) is RL that learns
  from a fixed dataset without exploration — useful when running on
  a real robot is expensive. Knowing RL adds about +33% to salary
  (2025 Robotics Salary Guide). World-model RL (Dreamer, TD-MPC2)
  is the cutting edge.
- **Sim-to-real techniques:** domain randomization (vary lighting,
  textures, friction during training so the policy is robust),
  system identification (measure the real robot, plug into sim),
  RMA (rapid motor adaptation), real-to-sim distillation.

## Layer 4: VLA specifics

Read these papers in this order, taking ~3 days each:

1. **RT-1, RT-2** — origin story.
2. **ACT / ALOHA** — action chunking, why predicting many steps helps.
3. **Diffusion Policy** — modern action generation.
4. **Open X-Embodiment + RT-X** — cross-embodiment data recipe.
5. **OpenVLA** — open implementation you can actually run.
6. **pi0, pi0-FAST, pi0.5** — current state of the art.
7. **DreamerV3 / TD-MPC2** — for the world-model angle.

For each paper, write a 1-page summary in your own words. This is the
single highest-leverage habit in this field.

## Layer 5: Tools and infrastructure

- **PyTorch 2.x** — the framework.
- **Hugging Face Transformers, Accelerate, PEFT (LoRA)** — same APIs
  you've seen for LLM work; VLAs reuse all of them.
- **FSDP / DeepSpeed** — distributed training across multiple GPUs.
  You'll meet these the first time a model doesn't fit in VRAM.
- **LeRobot, OpenPI** — the robot-learning-specific libraries.
- **Robosuite, MuJoCo / MJX, Isaac Lab** — simulators. MuJoCo is the
  free MIT-licensed default; Isaac Lab is NVIDIA's GPU-accelerated
  one.
- **Weights & Biases or MLflow** — experiment tracking. Like a
  dashboard for your training runs. Pick one and stick with it.
- **vLLM, TensorRT-LLM** — model serving. The funny part: VLAs are
  served with the exact same infra as LLMs.
- **Docker, CUDA basics** — you'll need to know what a CUDA version is
  and why your container has the wrong one.

## Layer 6: Mathematical comfort

You don't need a PhD. You do need:

- linear algebra: matrices, eigenvectors, dot products;
- multivariable calculus: gradients, chain rule;
- probability: distributions, expectations, KL divergence;
- a little bit of optimization: SGD, Adam, learning-rate schedules.

3Blue1Brown's "Essence of linear algebra" and "Essence of calculus"
playlists are enough as a refresher.

## Communities and people to follow

- Conferences: **CoRL**, **RSS**, **NeurIPS** (robotics workshops).
- Discords: **LeRobot**, **OpenVLA**.
- Twitter/X: @chelseabfinn, @svlevine, @physical_int, @drjimfan,
  @karpathy (general ML).
- Newsletters: Physical Intelligence blog, Hugging Face LeRobot blog.
