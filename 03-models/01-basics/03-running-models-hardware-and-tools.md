# 03 — What you run models on: hardware and tools

> **Goal of this page.** Explain, in plain language, the chips you run
> models on, the software libraries you write them in, and the "model
> hubs" you download them from — so the install commands and code in the
> per-type folders make sense.

## The chip: why everyone talks about GPUs

A **GPU** ("graphics processing unit") is a chip originally built to draw
video-game graphics. It turns out the maths that draws graphics is the
same maths that runs neural networks — lots of small calculations done
in parallel — so GPUs became the workhorse of machine learning.

- A **CPU** ("central processing unit," the normal main chip in any
  computer) *can* run small models, just slowly. Big models on a CPU are
  often too slow for a robot.
- **NVIDIA** is the dominant GPU maker, and its software toolkit,
  **CUDA** ("Compute Unified Device Architecture" — you never need the
  full name), is what most machine-learning code expects underneath. When
  an install guide says "you need CUDA," it means "you need an NVIDIA GPU
  and its drivers."
- **VRAM** ("video memory," the GPU's own memory) is the number to watch:
  a model's weights must fit in it. A 7-billion-parameter model needs
  very roughly ~14–16 gigabytes of VRAM to run comfortably. (Approximate
  — depends heavily on settings; re-check.)

### On the robot itself: edge computers

A robot cannot tow a data-centre GPU. For running models *on board* a
robot, NVIDIA's **Jetson** family of small, low-power computers (with a
built-in GPU) is the common choice. Running a model on the robot rather
than in the cloud is called running it **at the edge** ("edge" = out at
the device, away from central servers). Edge inference avoids the delay
and unreliability of a network round-trip — important when motors are
waiting on an answer.

## The libraries you write models in

- **Python** is the near-universal language for machine learning. All
  code in this area is Python.
- **PyTorch** is the most popular library for building and running
  models. When you see `import torch`, that is PyTorch. (You will also
  meet **TensorFlow**, an older alternative from Google; PyTorch
  dominates current robotics work.)
- **NumPy** (`import numpy`) is the basic library for working with arrays
  of numbers — images, sensor readings, motion vectors. Nearly every
  example uses it.

## Where models live: hubs and a few key tools

- **Hugging Face** is the dominant public "hub" for sharing models — a
  website plus a library that downloads weights for you with one line of
  code. When code says `from_pretrained("some/model-name")`, it is
  fetching that checkpoint from Hugging Face. Think "the package
  registry, but for trained models."
- **LeRobot** is a Hugging Face library aimed specifically at robot
  learning — it bundles robot datasets, several ready-made policies, and
  the code to train and run them. It appears repeatedly in the policy
  folders.
- **ONNX** ("Open Neural Network Exchange") is a portable file format
  for a trained model, so a model built in one library can run in
  another or on specialised hardware. You convert *to* ONNX when you want
  to deploy efficiently. You can ignore it until deployment.

## A realistic split of where each phase runs

| Phase | Typical hardware | Why |
|---|---|---|
| **Pre-training** | Many data-centre GPUs, for days | Enormous one-off compute; almost no team does this themselves |
| **Fine-tuning** | One or a few GPUs (cloud or a good workstation), for hours | Small dataset, short run — affordable |
| **Inference on a robot** | An on-board **Jetson** (or a nearby workstation GPU) | Must be low-latency and run without the cloud |

## What you now know

- Models run on **GPUs** (NVIDIA + CUDA dominate); the key budget is
  **VRAM**. On a robot, you run **at the edge** on a **Jetson**.
- You write them in **Python** with **PyTorch** and **NumPy**.
- You download trained weights from **Hugging Face** (and **LeRobot** for
  robot policies); **ONNX** is the portability format for deployment.

You now have the full foundation. Continue to any model-type folder
listed in [`../README.md`](../README.md); a good first stop is the
vision-language-action models in
[`../02-vision-language-action-models/`](../02-vision-language-action-models/00-introduction.md).
