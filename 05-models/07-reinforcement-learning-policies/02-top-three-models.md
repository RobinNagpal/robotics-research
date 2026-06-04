# 02 — Top three reinforcement-learning algorithms (with code)

> **Goal of this page.** Name the three reinforcement-learning (RL)
> algorithms most used to train robot policies, compare them, and give a
> short, commented code sample for each. Builds on
> [`00-introduction.md`](00-introduction.md) and
> [`01-working.md`](01-working.md).
>
> **Read me first — these are algorithms, not downloadable models.**
> Unlike the Vision-Language-Action page, there is no "trained file" to
> grab here. RL is a *training method*: you run the algorithm and it
> produces *your* policy. So each "model" below is really a famous
> **recipe for training a policy**.
>
> **All numbers and commands are approximate and drift.** Library names
> and APIs change often. Treat every code block as a *teaching sketch*
> that shows the shape of the API, not a guaranteed-runnable script.
> Always check the library's current documentation.

## Why these three

These are the three algorithms you will see again and again in robot
control. To make them runnable on an ordinary machine, the code uses
**Stable-Baselines3** — a popular, beginner-friendly Python library that
ships clean implementations of all three. We train a tiny policy on a
standard practice task (a simple control "toy problem") so you can watch
the loop run in seconds, not days.

For *real* robot-scale training — thousands of simulated robots at once
on a GPU — teams instead use **Isaac Lab** or **legged_gym** (see
[`01-working.md`](01-working.md)). Those tools use the very same
algorithms below (PPO especially); they just run them at massive scale.

| Algorithm | On/off-policy | Continuous actions? | Typical robot use | Library | Bottom line |
|---|---|---|---|---|---|
| **PPO** | On-policy | Yes (and discrete) | Legged locomotion, most sim-to-real | SB3, Isaac Lab, legged_gym | The robust default workhorse — start here |
| **SAC** | Off-policy | Yes (continuous only) | Arm / manipulation control | SB3 | Most sample-efficient for continuous control |
| **TD3** | Off-policy | Yes (continuous only) | Continuous control (arms, locomotion) | SB3 | Strong, stable refinement of older DDPG |

"On-policy" vs "off-policy" and "continuous actions" are explained in
[`01-working.md`](01-working.md). "Continuous" just means the action is a
smooth number (a joint angle), not a pick-one-of-N choice.

**One-time install for all three examples:**

```bash
# Stable-Baselines3: ready-made RL algorithms in Python.
# gymnasium: the standard package of practice "environments" (toy tasks).
pip install stable-baselines3 gymnasium
```

No GPU is needed for these tiny examples; a normal laptop is fine.

---

## 1. PPO (Proximal Policy Optimization)

**What it is.** The **robust, default on-policy workhorse** of RL. PPO's
trick is to update the policy in **small, capped steps** — it refuses to
change the policy too much at once ("proximal" means "stay close to where
you were"), which is what makes its training so stable and forgiving. It
needs more practice data than the off-policy methods, but in simulation
data is cheap, so PPO is the overwhelming favourite for **legged
locomotion** and most **sim-to-real** work. If you do not know what to
pick, pick PPO.

**Install.**

```bash
pip install stable-baselines3 gymnasium   # see note above
```

**Minimal code to run it.**

```python
# Goal: train a tiny PPO policy on a standard toy control task, then ask
# the trained policy for one action. This is the full RL loop in
# miniature — training, then inference.

import gymnasium as gym                 # the toy-environment library
from stable_baselines3 import PPO       # the PPO algorithm

# 1. Make the environment (the "world" the agent practises in).
#    "Pendulum-v1" is a classic continuous-control task: swing a pole
#    upright and hold it there. The agent's action is a smooth number
#    (how hard to push), so it is a good stand-in for a robot joint.
env = gym.make("Pendulum-v1")

# 2. Create the agent. "MlpPolicy" means the policy is a small plain
#    neural network (MLP = multilayer perceptron — a few dense layers),
#    which is the standard tiny network used for state-vector inputs.
model = PPO("MlpPolicy", env, verbose=1)

# 3. Train. "total_timesteps" is how many practice steps to take in the
#    environment. 20,000 is tiny (seconds of compute) — enough to see
#    learning start. A real robot policy uses tens of millions or more.
model.learn(total_timesteps=20_000)

# 4. Inference: use the trained policy. Reset the env to get a starting
#    observation, then ask the policy what to do.
obs, _ = env.reset()
#    "deterministic=True" returns the policy's *mean* (best-guess) action
#    with no exploration randomness — what you want when actually running.
action, _ = model.predict(obs, deterministic=True)
print("proposed action:", action)
```

**What you should see.** During `learn(...)`, a table of training
statistics scrolling by, with the average episode reward trending upward
as the policy improves. At the end, a printed action array (here a single
number — how hard to push the pendulum). On a real robot you would send
that array to the motor controller instead of printing it.

---

## 2. SAC (Soft Actor-Critic)

**What it is.** A **sample-efficient off-policy** method built for
**continuous control** — exactly the kind of smooth joint commands an
**arm or manipulator** needs. Being off-policy, SAC keeps a memory of all
past attempts (a **replay buffer**, see [`01-working.md`](01-working.md))
and re-learns from them repeatedly, so it squeezes far more learning out
of each step than PPO. Its signature idea is rewarding the policy for
staying a bit **random ("soft")** on purpose, which keeps it exploring
and tends to make training stable. When practice steps are expensive or
you want strong manipulation performance, SAC is a top choice.

**Install.**

```bash
pip install stable-baselines3 gymnasium   # same as above
```

**Minimal code to run it.**

```python
# Goal: train a tiny SAC policy on the same toy control task, then take
# one action. Note how little of the code changes from PPO — swapping the
# algorithm is usually a one-line change.

import gymnasium as gym
from stable_baselines3 import SAC        # the SAC algorithm

# 1. Same continuous-control environment as before. SAC only works on
#    continuous actions, so a smooth task like Pendulum is required.
env = gym.make("Pendulum-v1")

# 2. Same small neural-network policy ("MlpPolicy"). Under the hood SAC
#    also trains a "critic" that judges actions (see actor-critic in
#    01-working.md), but the library handles that for you.
model = SAC("MlpPolicy", env, verbose=1)

# 3. Train for a small number of steps. Because SAC is sample-efficient,
#    it often reaches good behaviour in *fewer* environment steps than
#    PPO — one of its main selling points.
model.learn(total_timesteps=20_000)

# 4. Inference: get a starting observation and ask for the best action.
obs, _ = env.reset()
#    deterministic=True drops SAC's exploration randomness and returns the
#    policy's mean action — the one to use when running for real.
action, _ = model.predict(obs, deterministic=True)
print("proposed action:", action)
```

**What you should see.** The same kind of training table during
`learn(...)`, and a printed action number at the end. With the same step
budget, SAC will often reach a higher average reward than PPO on this task
— a small taste of why off-policy methods are prized for their
sample-efficiency.

---

## 3. TD3 (Twin Delayed Deep Deterministic policy gradient)

**What it is.** A **strong off-policy continuous-control** method, and a
careful refinement of an older algorithm called **DDPG** (Deep
Deterministic Policy Gradient). DDPG worked but was famously unstable —
it tended to *over-estimate* how good actions were. TD3 fixes this with
two tricks baked into its name: **"twin"** (it trains two critics and
trusts the more pessimistic of the two, curbing over-optimism) and
**"delayed"** (it updates the policy less often than the critics, for
stability). The result is a reliable continuous-control workhorse — a
good alternative to SAC when you want stable, deterministic control of an
arm or a legged robot.

**Install.**

```bash
pip install stable-baselines3 gymnasium   # same as above
```

**Minimal code to run it.**

```python
# Goal: train a tiny TD3 policy on the same toy task and take one action.
# Again, only the algorithm name changes from the previous two examples.

import gymnasium as gym
from stable_baselines3 import TD3        # the TD3 algorithm

# 1. Same continuous-control environment. TD3, like SAC, is continuous-
#    only, so Pendulum (a smooth-action task) fits.
env = gym.make("Pendulum-v1")

# 2. Same small network policy. TD3 quietly trains the *two* critics its
#    name refers to; the library sets all that up from this one line.
model = TD3("MlpPolicy", env, verbose=1)

# 3. Train for a small step budget. As an off-policy method, TD3 also
#    reuses past experience from a replay buffer, so it learns efficiently.
model.learn(total_timesteps=20_000)

# 4. Inference: starting observation in, best action out.
obs, _ = env.reset()
#    TD3 is "deterministic" by design: given a state it always returns the
#    same action. deterministic=True simply strips the exploration noise
#    it adds during training, leaving that clean mean action.
action, _ = model.predict(obs, deterministic=True)
print("proposed action:", action)
```

**What you should see.** Once more, a scrolling training table with
reward climbing, then a printed action number. TD3's behaviour on this
task is typically close to SAC's — both are strong continuous-control
methods; the differences show up more on harder, larger problems.

---

## Choosing between them

- **A safe default, or anything legged / sim-to-real** → **PPO**. It is
  the most robust, the most documented, and the algorithm behind almost
  every modern walking-robot controller (run at scale in Isaac Lab or
  legged_gym).
- **Sample-efficient continuous control, especially arms / manipulation**
  → **SAC**. Best when each practice step is precious.
- **A stable, deterministic continuous-control alternative** → **TD3**.
  Reach for it when SAC is fiddly on your task or you want deterministic
  actions.

A practical workflow: prototype with PPO because it "just works"; if you
need more performance out of fewer steps on a continuous task, try SAC,
then TD3, and keep whichever trains most reliably for *your* problem.

## See also

- What RL is and when to use it: [`00-introduction.md`](00-introduction.md).
- The learning loop and the on/off-policy distinction behind these picks:
  [`01-working.md`](01-working.md).
- The demonstration-copying sibling family:
  [`../06-imitation-learning-policies/`](../06-imitation-learning-policies/00-introduction.md).
- Where these trained policies actually run:
  [`../01-basics/03-running-models-hardware-and-tools.md`](../01-basics/03-running-models-hardware-and-tools.md).
