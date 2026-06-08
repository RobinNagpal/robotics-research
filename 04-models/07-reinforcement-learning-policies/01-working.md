# 01 — How reinforcement-learning policies work

> **Goal of this page.** Open the box: the learning loop, the words you
> will meet (reward function, return, exploration, on/off-policy,
> policy-gradient vs value-based), why training needs millions of
> simulated steps, the sim-to-real tricks, and why running the finished
> policy is cheap. Plain language, no maths. Builds on
> [`00-introduction.md`](00-introduction.md).

## The learning loop

Reinforcement learning is one loop, repeated until the policy is good:

```text
        ┌────────────────────────────────────────────┐
        │                                            ▼
  [ observe state ] ─► [ policy picks action ] ─► [ environment reacts ]
        ▲                                            │
        │                                            ▼
        └──── [ update policy to favour ◄──── [ get reward ]
                higher-reward actions ]
```

1. **Observe** — read the current state (camera, joint angles, …).
2. **Act** — the policy turns that observation into an action.
3. **Get reward** — the environment returns the action's score and the
   new state.
4. **Update** — nudge the policy's weights so that actions which led to
   high reward become *more* likely next time, and low-reward actions
   *less* likely.

Repeat for millions of steps. Slowly, the policy drifts toward behaviour
that scores well. That "nudge in step 4" is the whole game, and the three
algorithms in [`02-top-three-models.md`](02-top-three-models.md) are
different recipes for it.

## Reward and return

- **Reward function** — the rule, written by you, that turns "what just
  happened" into a number. For a walking robot it might be:
  `+forward speed − energy used − big penalty if it falls`. Designing
  this is **reward engineering** (see
  [`00-introduction.md`](00-introduction.md)) and it is where most of the
  human effort goes.
- **Return** — the *total* reward collected over a whole episode (often
  with later rewards counted slightly less than sooner ones). The policy
  is not trying to grab the biggest reward *this step*; it is trying to
  maximise the **return** over the long run. This is why RL can learn
  patience — taking a small loss now for a big gain later.

## Exploration versus exploitation

A learner faces a constant dilemma:

- **Exploitation** — do the action you currently *believe* is best, to
  cash in known reward.
- **Exploration** — try something new and possibly worse, to *discover*
  whether there is something even better you have not found yet.

Too much exploitation and the policy gets stuck in a mediocre habit; too
much exploration and it never settles. Every RL algorithm has some knob
for balancing the two (e.g. adding a little randomness to the actions
early on, then dialling it down).

## On-policy versus off-policy

This is the single biggest dividing line between RL algorithms, and it is
simpler than it sounds. It is about **which experience you are allowed to
learn from.**

- **On-policy** — you may only learn from experience collected by the
  *current* version of the policy. As soon as you update the policy, the
  old experience is stale and thrown away. Think *"learn only from your
  own most recent attempts."* Tends to be **stable but data-hungry**.
  **PPO** is on-policy.
- **Off-policy** — you keep a big memory of *all* past experience (a
  **replay buffer**) and can re-learn from old attempts again and again,
  even ones collected by earlier, worse versions of the policy. Think
  *"learn from a diary of everything you have ever tried."* Tends to be
  more **sample-efficient** (squeezes more learning out of each
  experience) but can be **less stable**. **SAC** and **TD3** are
  off-policy.

That trade-off — stability versus sample-efficiency — is exactly why you
would pick one algorithm over another (see
[`02-top-three-models.md`](02-top-three-models.md)).

## Policy-gradient versus value-based methods

Two intuitions for *how* the update in step 4 is computed:

- **Value-based methods** learn a **value**: a guess of "how much total
  reward will I eventually get if I take this action from here?" The
  policy then simply picks the action with the highest predicted value.
  You learn *to judge*, then act greedily on the judgement.
- **Policy-gradient methods** adjust the policy's weights **directly** in
  the direction that made high-return actions more likely — no separate
  "judge" strictly required. You learn *to act* directly.

In practice the best modern methods are **hybrids** called
**actor-critic**: an **actor** (the policy that acts) plus a **critic**
(a value estimate that tells the actor how good its actions were). All
three algorithms in the next file are actor-critic — they just differ in
the on/off-policy choice and the stabilising tricks bolted on.

## Why training takes millions of steps

RL learns from *outcomes*, not instructions, so it must try an action
many times in many situations before it can tell whether that action is
reliably good. That adds up fast: a typical legged-locomotion policy
needs on the order of **tens of millions to billions of simulated time
steps** to train well. (Figures approximate — re-check.)

That is only affordable because of **massively parallel simulation**.
Modern tools run **thousands of copies of the robot at once** on a single
GPU, all practising in parallel, so the experience needed piles up in
hours instead of years.

- **Isaac Lab** (built on NVIDIA Isaac Sim) and the earlier
  **legged_gym / Isaac Gym** are the standard tools for this — they
  simulate thousands of robots on the GPU simultaneously. (Naming and
  versions drift — re-check.)

## Sim-to-real tricks: domain randomization

Recall the **sim-to-real gap** from
[`00-introduction.md`](00-introduction.md): a policy trained in a perfect
simulator can fail on the messy real robot. The main fix is
**domain randomization**.

The idea: instead of training in one perfectly-tuned simulator, you
**randomly vary the simulation** every episode — change the floor
friction, the robot's mass, the motor strength, the lighting, add sensor
noise and small delays. The policy never sees the same world twice, so it
is forced to learn behaviour that is **robust to a whole *range* of
conditions**. The real world then looks like just one more variation it
has already learned to handle. This is the workhorse trick behind most
successful sim-to-real walking robots.

## Inference is cheap

Training is enormous, but the **finished policy is tiny** — usually a
small neural network with a few hidden layers. Running it (inference) is
fast and light:

- It comfortably runs at **hundreds or thousands of decisions per second
  (hundreds-plus hertz)** on a modest onboard computer — far faster than
  a big Vision-Language-Action model.
- It typically needs **no GPU at all** to run; a small embedded processor
  is enough. (See
  [`../01-basics/03-running-models-hardware-and-tools.md`](../01-basics/03-running-models-hardware-and-tools.md).)

So the cost profile is lopsided: **expensive, GPU-heavy training; cheap,
lightweight running.** This is the mirror image of the training/inference
split in [`../01-basics/02-training-vs-inference.md`](../01-basics/02-training-vs-inference.md).

## Limitations and failure modes

- **Reward hacking** — the policy finds a loophole that scores high
  *without* doing what you meant. Reward a cleaning robot for "dirt
  picked up" and it may dump dirt out so it can pick it up again. Any gap
  in the reward function gets exploited.
- **The sim-to-real gap** — even with domain randomization, behaviour
  learned in sim can degrade on hardware.
- **Sample inefficiency** — the sheer amount of practice needed makes
  real-world-only RL impractical for most tasks; you almost always need a
  simulator.
- **Training instability** — RL training can be fiddly: it sometimes
  diverges or collapses, and is sensitive to settings. (This is partly
  why robust defaults like PPO are so popular.)

## Key terms used on this page

- **Reward function** — your rule turning an outcome into a score.
- **Return** — total reward over an episode; what the policy maximises.
- **Exploration / exploitation** — trying new actions vs. cashing in
  known-good ones.
- **On-policy / off-policy** — learn only from current-policy experience
  vs. learn from a stored memory of all past experience.
- **Actor-critic** — a policy (actor) paired with a value estimator
  (critic).
- **Replay buffer** — the stored memory of past experience used by
  off-policy methods.
- **Domain randomization** — randomly varying the simulator so the policy
  transfers to reality.
- **Reward hacking** — gaming the reward without doing the real task.

## See also

- The three most-used RL algorithms, with runnable code:
  [`02-top-three-models.md`](02-top-three-models.md).
- What RL is and when to use it: [`00-introduction.md`](00-introduction.md).
- The demonstration-copying sibling:
  [`../06-imitation-learning-policies/`](../06-imitation-learning-policies/00-introduction.md).
