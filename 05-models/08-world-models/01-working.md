# 01 — How world models work

> **Goal of this page.** Open the box: what goes in, what comes out, how
> a world model predicts the future in a compact space, how a robot plans
> or learns *inside* those predictions, how it is trained, and what it
> costs. Plain language, no maths. Builds on
> [`00-introduction.md`](00-introduction.md).

## Inputs and outputs, precisely

**Inputs**

- **A history of observations** — what the robot has recently sensed,
  usually the last few camera frames (each frame is just a grid of colour
  values, i.e. pixels), and often the arm's joint readings too.
- **An action** — the move the robot is considering taking next (e.g. the
  target joint angles, or where to move the hand).

**Outputs**

- **The predicted next observation** — its best guess at what the robot
  *would* sense one step later, having taken that action.
- **A predicted reward** — a single number scoring how good that
  predicted next situation is for the task at hand. ("Reward" is the
  same scoring idea used in reinforcement learning, see
  [`../07-reinforcement-learning-policies/00-introduction.md`](../07-reinforcement-learning-policies/00-introduction.md).)

That pair — *next observation* plus *how good it is* — is everything you
need to imagine and judge a possible future.

## The "latent" idea: predicting in a compact space

A camera frame is huge — hundreds of thousands of pixel values. Trying to
predict the *exact next picture*, pixel by pixel, is wasteful and hard:
most of those pixels are background the robot does not care about.

So modern world models do something cleverer. They **compress** each
observation down to a small set of numbers that captures only what
matters — the gist of the scene. That compact summary is called a
**latent state**. "Latent" just means *hidden / not directly shown* —
these numbers are not anything you can read off the image directly; they
are the model's own internal shorthand for "the situation, boiled down."

Think of it like describing a kitchen as "mug on the left edge of the
table, gripper open, 10 cm away" instead of sending a full photo. Far
fewer numbers, and they hold the parts that matter.

The world model then does its prediction **in this compact latent space,
not in pixels**:

```text
 camera frames ─►[ encoder ]─► latent state ─┐
                                             ├─►[ dynamics ]─► predicted next latent state
 action ─────────────────────────────────────┘                       │
                                                                      ├─► predicted reward
                                                            (optional) └─► [ decoder ]─► predicted next image
```

- The **encoder** squeezes raw observations into the latent state.
- The **dynamics** part is the heart of it: given the current latent
  state and an action, it predicts the *next* latent state — the future,
  expressed in shorthand.
- A small head reads off the **predicted reward** from that latent state.
- An optional **decoder** can expand a latent state back into a picture,
  which is handy for *seeing* what the robot imagined (and helps
  training), but the planning itself stays in the cheap latent space.

## Rolling out an imagined trajectory

Because the dynamics part turns "latent state + action" into "next latent
state," you can **chain it**: feed the predicted next state straight back
in with another action, predict the state after that, and so on. Each
loop also gives you a predicted reward.

Run that loop, say, 15 steps forward and you have an **imagination
rollout**: a whole imagined future — a sequence of predicted states and
the rewards along the way — for one candidate plan, produced without the
robot moving a muscle. Add up the rewards and you have a score for that
plan.

## Two ways to use the rollouts

**Way 1 — learn a policy "in a dream."** Instead of practising in the
real world, you let a reinforcement-learning-style **policy**
([`../07-reinforcement-learning-policies/00-introduction.md`](../07-reinforcement-learning-policies/00-introduction.md))
practise entirely inside the world model's imagined rollouts. The policy
proposes actions, the world model predicts the resulting futures and
rewards, and the policy improves from that imagined feedback. People
literally call this **learning in a dream** or *training in imagination*.
It is wildly cheaper than real practice — this is how DreamerV3 works (see
[`02-top-three-models.md`](02-top-three-models.md)).

**Way 2 — model-predictive control.** Here there is no pre-trained
policy. At **every single step**, the robot:

1. invents many candidate action *sequences* for the next few moves;
2. imagines each one as a rollout and scores it;
3. executes just the **first action** of the best-scoring sequence;
4. then throws the rest away and **re-plans from scratch** next step,
   using the newest real observation.

This "plan a few steps ahead, take one step, re-plan" loop is called
**model-predictive control** (often shortened to **MPC**). Constantly
re-planning from fresh, real observations keeps the small prediction
errors from running away. TD-MPC2 works this way.

## How a world model is trained

A world model learns from **logged experience** — a pile of recorded
sequences of *observation, action, next observation, reward*, gathered by
letting the robot (or a person) operate and saving what happened. Its
training goal is simply **"predict the next observation and reward as
accurately as possible"** across all those recordings. No human has to
label anything; the future *is* the answer key, because the recording
already shows what actually happened next.

This is the same two-phase pattern as every model here
([`../01-basics/02-training-vs-inference.md`](../01-basics/02-training-vs-inference.md)):
a heavy **training** phase that fits the predictor, then a cheap
**inference** phase where you query it to imagine futures. In the most
sample-efficient setups the two are interleaved — act a little, add the
new experience, improve the model, repeat.

## What it costs to run

- **Training** is the expensive part and usually wants a capable GPU
  (graphics processing unit), often for hours to days depending on the
  task. (Figures approximate — re-check per system.)
- **Inference** in the cheap latent space is fast, which is exactly what
  makes model-predictive control's "imagine many plans every step"
  practical at robot control rates.
- See [`../01-basics/03-running-models-hardware-and-tools.md`](../01-basics/03-running-models-hardware-and-tools.md)
  for the general hardware picture.

## Limitations and failure modes

- **Compounding error.** The deepest problem. A small mistake in step one
  of a rollout feeds into step two, and so on, so imagined futures **drift
  from reality the further ahead you look**. This is why short rollouts
  plus constant re-planning (model-predictive control) are common — they
  keep the horizon short enough to trust.
- **Hard to train well.** Getting a world model to predict a rich, varied
  world accurately is an open research problem; results are sensitive to
  many details.
- **The dreamed world can be subtly wrong** in ways the policy then
  exploits — a plan that looks brilliant in imagination but fails in
  reality.
- **Research-grade tooling**, with all the rough edges that implies.

## Key terms used on this page

- **World model** — a learned predictor of the next observation (and
  reward) given the current situation and an action.
- **Latent state** — a small set of numbers that compresses an
  observation down to just what matters; the model predicts the future in
  this compact space rather than in raw pixels.
- **Imagination rollout** — an imagined future produced by chaining the
  predictor forward several steps for a candidate plan, with no real
  action taken.
- **Model-predictive control (MPC)** — plan a few steps ahead in
  imagination each step, execute only the first action, then re-plan from
  the newest real observation.
- **Sample efficiency** — how much useful learning you get per real
  attempt; world models score highly because they practise in
  imagination.

## See also

- Why this family exists and when to use it:
  [`00-introduction.md`](00-introduction.md).
- The three landmark systems, with code sketches:
  [`02-top-three-models.md`](02-top-three-models.md).
- The trial-and-error learning it makes affordable:
  [`../07-reinforcement-learning-policies/00-introduction.md`](../07-reinforcement-learning-policies/00-introduction.md).
