# 02 — Top three world models (with code)

> **Goal of this page.** Name the three landmark world-model systems you
> can actually download and run, compare them, and give a short, commented
> code sample for each. Builds on [`00-introduction.md`](00-introduction.md)
> and [`01-working.md`](01-working.md).
>
> **Read me first — these are research code, not products.** Unlike a
> polished library you `pip install`, world models are almost always run
> by **cloning a research repository** (downloading the authors' own code
> from a site like GitHub) and following its README. Code, command names
> and defaults change often. Treat every code block below as a *teaching
> sketch* that shows the *shape* of the entry point — the command or
> function you start things with — not a guaranteed-runnable script.
> Always check the project's current documentation. Running any of these
> wants a capable GPU (graphics processing unit); see
> [`../01-basics/03-running-models-hardware-and-tools.md`](../01-basics/03-running-models-hardware-and-tools.md).

## Why these three

All three are influential, openly available, and trace one family line:
**PlaNet** introduced learning to predict the future in a compact
[latent space](01-working.md); **DreamerV3** grew out of it and made
"learn a policy purely in imagination" work across many tasks with one
setting; **TD-MPC2** pairs a learned latent world model with
[model-predictive control](01-working.md) for strong continuous control.

| Model | Core idea | Control style | Licence | Bottom line |
|---|---|---|---|---|
| **DreamerV3** | Learn a latent world model, then train a policy *entirely in imagination* | Learned policy ("dreaming") | Open (permissive) | The landmark general world-model agent — one config works across many domains |
| **TD-MPC2** | Learned latent world model + short imagined rollouts planned every step | Model-predictive control | Open (permissive) | Best-in-class continuous control; plans fresh each step so errors do not run away |
| **PlaNet** | First to learn latent dynamics and *search* action sequences in latent space | Planning by search (no policy) | Open (permissive) | The foundational ancestor — simplest to understand, the predecessor to Dreamer |

The control styles are the two from
[`01-working.md`](01-working.md): "learn a policy in a dream" versus
"plan a few steps ahead each step" (model-predictive control). PlaNet is
a plain version of the latter — it searches for good action sequences but
trains no policy at all.

---

## 1. DreamerV3

**What it is.** The landmark general world-model agent (Danijar Hafner
and colleagues, 2023). It learns a **latent world model** — a compressed
predictor of the future, the
[latent state](01-working.md) idea — and then trains a **policy purely in
imagination**: the policy practises against the model's predicted futures,
never touching the real environment during that practice (the "learning
in a dream" idea from [`01-working.md`](01-working.md)). Its headline
result is robustness: **one configuration** works across a wide range of
domains — control tasks, games, even Minecraft — without per-task tuning.

**Install.**

```bash
# Cloned from the authors' research repository, not pip-installed.
git clone https://github.com/danijar/dreamerv3.git
cd dreamerv3
pip install -e .                 # "-e" installs it in editable form
```

**Minimal code to run it (teaching sketch).**

```bash
# DreamerV3's entry point is a training *script*, not a library call you
# import. You point it at an environment and a logging folder, and it
# starts learning a world model AND a policy together. Here we train on a
# standard continuous-control task (a simulated walking robot).
#
# This single command does it all: collect a little real experience,
# improve the world model, then practise the policy inside the model's
# imagined rollouts (see 01-working.md) — looping until it is good.

python dreamerv3/main.py \
  --logdir ./logs/walker_walk \
  --configs dmc_proprio \
  --task dmc_walker_walk
#   --logdir  : where to save checkpoints and metrics
#   --configs : the single preset that works across domains
#   --task    : which environment to learn (DeepMind Control "walker, walk")
```

**What you should see.** A long training run that prints a rising score
(reward) over time as the policy gets better — all the heavy practice
happening in imagination, with only occasional real steps. Checkpoints
(saved copies of the trained model) appear under the log folder. Because
training is the expensive phase, expect this to run for hours on a GPU.

---

## 2. TD-MPC2

**What it is.** A model that combines a **learned latent world model**
with **model-predictive control** (Nicklas Hansen and colleagues, 2024).
At every step it imagines several **short** rollouts of candidate action
sequences, scores them, executes only the first move of the best, then
re-plans from the newest real observation — the loop described in
[`01-working.md`](01-working.md). Keeping the imagined horizon short and
re-planning constantly is what stops small prediction errors from
compounding. It is especially strong on **continuous control** (smooth
motion of arms and legs) and, like DreamerV3, aims to work across many
tasks with one recipe.

**Install.**

```bash
git clone https://github.com/nicklashansen/tdmpc2.git
cd tdmpc2
pip install -e .
```

**Minimal code to run it (teaching sketch).**

```bash
# TD-MPC2 is also driven by a train/eval *script*. You name a task and it
# learns the latent world model, then uses it for model-predictive control
# (plan short rollouts each step, take the best first action).

python tdmpc2/train.py \
  task=walker-walk \
  steps=1000000
#   task  : which continuous-control environment to learn
#   steps : how many environment steps to train for (more = better, slower)

# To watch a *trained* model act (evaluation only), you point the same
# script at a saved checkpoint instead of training from scratch:
python tdmpc2/evaluate.py \
  task=walker-walk \
  checkpoint=./logs/walker-walk/models/final.pt
```

**What you should see.** During training, a rising reward as the world
model and its planner improve. During evaluation, the agent controls the
simulated robot by planning short imagined rollouts at each step and
executing the best first action — visibly smoother and more deliberate
than blind trial and error.

---

## 3. PlaNet (Deep Planning Network)

**What it is.** The influential ancestor of the Dreamer family (Danijar
Hafner and colleagues, 2019). Full name **Deep Planning Network**,
shortened to **PlaNet**. It was the first to show you could learn a
**latent dynamics model** — a future-predictor working in the compact
[latent space](01-working.md) — purely from images, and then **plan by
searching action sequences in that latent space**: try many candidate
sequences in imagination, keep the best-scoring ones, refine, and execute
the first move (a plain form of the model-predictive control loop, with
**no learned policy** at all). It is included here as the foundational
example — understand PlaNet and you understand the idea every later world
model builds on. In short: **PlaNet is the predecessor to Dreamer.**

**Install.**

```bash
# The original authors' research code (TensorFlow). Community PyTorch
# re-implementations also exist and are often easier to read.
git clone https://github.com/google-research/planet.git
cd planet
pip install -e .
```

**Minimal code to run it (teaching sketch).**

```bash
# PlaNet is launched as a training script too. It learns the latent
# dynamics model from image observations, then plans by searching action
# sequences in latent space (no policy is trained — planning IS the
# decision-making each step).

python -m planet.scripts.train \
  --logdir ./logs/cheetah_run \
  --params '{tasks: [cheetah_run]}'
#   --logdir : where checkpoints and metrics go
#   --params : the task to learn (here, a simulated running "cheetah")
```

**What you should see.** A training run that steadily improves at the task
while learning entirely from pixels, choosing each move by searching
imagined action sequences rather than by consulting a trained policy.
Expect rougher edges than DreamerV3 or TD-MPC2 — it is the oldest of the
three and predates many later refinements.

---

## Choosing between them

- **Best general-purpose starting point / "learn a policy in a dream"** →
  **DreamerV3** (one config across many domains, most actively used).
- **Best smooth continuous control with plan-every-step safety against
  compounding error** → **TD-MPC2**.
- **Understanding the core idea from the ground up** → **PlaNet**, the
  foundational ancestor — simplest to read, though the least polished to
  run.

A reminder from the top of the page: all three are **research code**. Plan
on reading the repository's README, matching its exact dependency
versions, and adapting commands — far more hands-on than installing a
finished library. This is the price of working at the frontier (see the
research caveat in [`00-introduction.md`](00-introduction.md)).

## See also

- What world models are and when to use them:
  [`00-introduction.md`](00-introduction.md).
- The mechanics behind the code — latent states, rollouts, dreaming,
  model-predictive control: [`01-working.md`](01-working.md).
- The trial-and-error learning these make affordable:
  [`../07-reinforcement-learning-policies/00-introduction.md`](../07-reinforcement-learning-policies/00-introduction.md).
- Where world models fit among all model types:
  [`../01-basics/01-types-of-models-map.md`](../01-basics/01-types-of-models-map.md).
