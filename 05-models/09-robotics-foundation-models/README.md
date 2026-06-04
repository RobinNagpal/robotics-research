# 09 — Robotics foundation models from the leading labs

> **What this folder is.** Folders [02–08](../README.md) sort models by
> *kind*. This folder is different: it profiles the **headline robotics
> foundation models** shipped by the leading companies — one document per
> product — because the interesting thing about them is the *whole
> package* (the model, the data behind it, how you get access), not just
> the technique. Most of these are **Vision-Language-Action models**, so
> read [`../02-vision-language-action-models/`](../02-vision-language-action-models/00-introduction.md)
> first; this folder assumes it.

> **Heavy drift warning.** This is the single fastest-moving topic in the
> whole repository. Version numbers, access terms, prices and benchmark
> claims here change month to month. Every figure is approximate (`~`)
> and every code block is a **teaching sketch**. Always check the
> product's own current documentation before relying on anything.

---

## The documents in this folder

Start with the introduction, then read whichever product interests you.

| # | File | Company | The model(s) |
|---|---|---|---|
| 00 | [`00-introduction.md`](00-introduction.md) | — | What a "robotics foundation model" is, and how to read this folder |
| 01 | [`01-gemini-robotics.md`](01-gemini-robotics.md) | Google DeepMind | Gemini Robotics + Gemini Robotics-ER |
| 02 | [`02-physical-intelligence-pi.md`](02-physical-intelligence-pi.md) | Physical Intelligence | π0 ("pi-zero") and π0.5 |
| 03 | [`03-nvidia-groot.md`](03-nvidia-groot.md) | NVIDIA | GR00T N1 / N1.5 (Isaac GR00T) |

## At a glance

The three differ most in **how open they are** — which decides whether
you can actually download and run them, or only call them over the
internet. (All figures approximate; re-check.)

| Model | Body it targets | How you access it | Open weights? | Bottom line |
|---|---|---|---|---|
| **Gemini Robotics** | Arms, humanoids | Mostly partner / limited access; **Gemini Robotics-ER** reasoning model via the cloud Application Programming Interface (API) | No | The most capable generalist, but the least open — you mostly *call* it, not host it |
| **π0 / π0.5** | Many arms (cross-body) | Open code + weights (`openpi`) | **Yes** | The most capable model you can fully download and run yourself |
| **GR00T N1 / N1.5** | Humanoids especially | Open code + weights on the model hub, plus NVIDIA's training tools | **Yes** | The open humanoid-focused option, tightly tied to NVIDIA's simulator stack |

"Cross-body" (also called *cross-embodiment*) means one model trained to
drive **several different robot bodies**, not just one — explained in
[`00-introduction.md`](00-introduction.md).

## See also

- The technique these are built on:
  [`../02-vision-language-action-models/`](../02-vision-language-action-models/00-introduction.md).
- What "open weights", "fine-tuning" and "API" mean:
  [`../01-basics/`](../01-basics/README.md).
- The field-level write-up of robot foundation models:
  [`../../01-all-areas/01-robot-learning-vla/README.md`](../../01-all-areas/01-robot-learning-vla/README.md).
