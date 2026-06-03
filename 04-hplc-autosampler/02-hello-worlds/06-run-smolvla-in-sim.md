# 06 — Run SmolVLA in simulation (a learned policy drives a pick)

> Checklist exercise: **Layer 5 — "run a Vision-Language-Action model
> in simulation" (the first of two stretch exercises).**
> See [`../07-learning-checklist.md`](../07-learning-checklist.md).

**This is a stretch / optional exercise.** Everything before it used
hand-written rules: you told the arm exactly where to go. This exercise
is your first taste of a *learned* approach, where a trained neural
network decides the motion for you. It is harder to set up, it needs a
bigger computer, and the exact commands change often. Treat it as an
eye-opener, not as a required step. If it does not run on your machine,
that is fine — you can read it, understand the shape of it, and come
back later.

## What this program proves

Up to now, every motion in this project was something *you* spelled out.
This exercise runs a **Vision-Language-Action model** instead. A
Vision-Language-Action model is a single trained neural network (a big
mathematical function whose millions of internal numbers were tuned by
showing it many examples) that takes in **camera pictures plus a typed
instruction** and outputs **robot movements**. People shorten the name
to "VLA"; we will keep saying "Vision-Language-Action model."

The specific model we run is called **SmolVLA**. It is an **open** model
(its trained numbers are published for anyone to download for free) and
it is **compact**: about 450 million internal numbers, which is small as
these models go, so it can run on ordinary hardware rather than a room
full of servers. It is published by a company called Hugging Face.

We load SmolVLA using a free toolkit called **LeRobot** (an open library
for robot learning — "Le Robot" is a small French-language joke; it just
means "the robot"). Then we run it inside a **simulation** (the
video-game-like physics world from exercise 01) and watch the learned
policy drive a pick. The word **policy** here means "the thing that
decides what to do next" — for us, the trained network.

If you can watch a downloaded, pretrained policy move a simulated arm
toward the vial, you have proven something real: you can actually *run* a
modern learned model, not merely read about one. That is the whole point
of this exercise.

> **Honesty note.** LeRobot and SmolVLA are fast-moving tools. The exact
> class names, method names, and the available simulation environments
> change between versions — sometimes month to month. The program below
> is written to be as close to runnable as possible and to teach the
> *shape* of the task, but you should expect to adjust a name or two
> against the current documentation:
> <https://github.com/huggingface/lerobot>.

## What you need first

- **Python**, version 3.10 or newer.
- The **LeRobot** library, installed with its simulation extras. At the
  time of writing this is done with the Python installer:
  ```bash
  pip install "lerobot[sim]"
  ```
  (Check the LeRobot install page for the current package name and
  extras — they drift.)
- A **Graphics Processing Unit** is strongly recommended. A Graphics
  Processing Unit, often shortened to "GPU," is a chip that does the
  heavy mathematics neural networks need. SmolVLA is small enough that it
  *can* run on an ordinary central processor, but it will be slow; with a
  Graphics Processing Unit it runs comfortably.
- An internet connection the first time you run it, because the trained
  model is downloaded from Hugging Face on first use.

Unlike the earlier exercises, this one does **not** need the robot
framework (the Robot Operating System) to be running. LeRobot talks to
its own simulation directly.

## The whole program

Save this as a file named `run_smolvla.py`:

```python
from lerobot.common.policies.smolvla.modeling_smolvla import SmolVLAPolicy
import gymnasium as gym
import lerobot_sim_envs  # noqa: F401  (registers the simulation worlds)


def main():
    policy = SmolVLAPolicy.from_pretrained("lerobot/smolvla_base")
    policy.eval()

    env = gym.make("lerobot/pick-vial-v0", render_mode="human")
    observation, info = env.reset()

    instruction = "pick up the vial QC-007 from tray slot A3"

    for step in range(300):
        observation["task"] = instruction
        action = policy.select_action(observation)
        observation, reward, terminated, truncated, info = env.step(action)

        if step % 20 == 0:
            print(f"step {step}: reward so far = {reward}")

        if terminated or truncated:
            print("Episode finished.")
            break

    env.close()


if __name__ == "__main__":
    main()
```

## Every line explained

**`from lerobot.common.policies.smolvla.modeling_smolvla import SmolVLAPolicy`**
The word `import` means "bring in ready-made code so I can use it." This
long line reaches deep inside the LeRobot library and brings out one
specific tool, `SmolVLAPolicy` — the piece of code that knows how to load
and run the SmolVLA model. (This exact path is the part most likely to
have been renamed by the time you read this; if Python complains it
cannot find it, search the current LeRobot documentation for
"SmolVLAPolicy.")

**`import gymnasium as gym`**
This brings in a library called **Gymnasium**, the standard toolkit for
*simulation environments* used in robot learning. An **environment** is a
self-contained little world that you can reset, observe, and step
forward. The `as gym` part gives it the shorter nickname `gym`, which is
what almost everyone types, so the rest of the code can say `gym.make`
instead of the longer name.

**`import lerobot_sim_envs  # noqa: F401`**
This brings in a package whose only job is to **register** (announce the
existence of) the specific simulated worlds we want — including the
pick-the-vial world we ask for below. We never call anything from it by
name; importing it is enough to make its worlds available. The
`# noqa: F401` on the end is a polite note to code-checking tools meaning
"yes, I know this import looks unused — leave it alone, it has a side
effect." (The real package name for the simulation worlds varies; this
stands in for whichever one your LeRobot version provides.)

**`def main():`**
The word `def` begins a named block of instructions (a "function"). We
name this one `main`; it holds the whole program and runs when we launch
the file.

**`policy = SmolVLAPolicy.from_pretrained("lerobot/smolvla_base")`**
This is the heart of the exercise. **`from_pretrained`** means "fetch a
model whose internal numbers have already been trained, and load them
ready to use." The text `"lerobot/smolvla_base"` is the model's address
on Hugging Face's online model store. The first time you run this, it
**downloads** those hundreds of millions of trained numbers to your
computer (a few hundred megabytes) and caches them, so later runs are
fast. The loaded, ready-to-use model is stored in the name `policy` —
this is the trained brain that will choose the movements.

**`policy.eval()`**
This switches the model into **evaluation mode**, meaning "we are only
*using* you to make decisions now, not *training* you." Neural networks
behave slightly differently while learning versus while being used; this
line tells it to behave in the using way. You call it once, before the
loop.

**`env = gym.make("lerobot/pick-vial-v0", render_mode="human")`**
This creates the **simulation environment** — the little physics world
the arm lives in. `gym.make` means "build me the world registered under
this name." The name `"lerobot/pick-vial-v0"` stands for a
pick-up-the-vial task (`v0` just means "version zero," the first
version). `render_mode="human"` means "open a window so I can watch it on
screen" (as opposed to running invisibly in the background). The built
world is stored in `env`.

**`observation, info = env.reset()`**
**`reset`** puts the world back to a fresh starting state — arm at home,
vial in its slot — the way you reset a board game before playing. It
hands back two things: the first **observation**, which we store in
`observation`, and a bundle of extra `info` we will not use. An
**observation** is the model's view of the world *right now*: the camera
picture (or pictures) and the arm's current joint positions, packaged
together. The model reads an observation and produces an action; that is
the entire conversation between the two.

**`instruction = "pick up the vial QC-007 from tray slot A3"`**
This stores the typed, plain-English **instruction** we want the model to
follow. A Vision-Language-Action model is special precisely because it
takes words like these as part of its input; the same model could be told
to do a different task just by changing this sentence. We mention our
sample, QC-007, and its tray slot, A3, so the instruction is concrete.

**`for step in range(300):`**
The word `for` begins a **loop** — a block of instructions that repeats.
`range(300)` produces the numbers 0, 1, 2, … up to 299, so the block
below runs up to 300 times, with `step` holding the current number each
time. A loop is how we step the simulation forward little by little: read
the world, decide a move, apply it, repeat. Three hundred steps is just a
safety cap so the program cannot run forever.

**`observation["task"] = instruction`**
This tucks our instruction sentence *into* the observation under the
label `"task"`, because the model expects to receive the picture, the arm
state, **and** the words all in one bundle. (The exact label the model
looks for — here `"task"` — can differ by version; the documentation
lists it.)

**`action = policy.select_action(observation)`**
This is the model thinking. **`select_action`** hands the current
observation to the trained network and gets back an **action** — the next
movement for the arm, expressed as a set of numbers (for example, how
much to change each joint, or where to move the gripper). We store it in
`action`. Nothing has moved yet; the action is just a decision.

**`observation, reward, terminated, truncated, info = env.step(action)`**
**`step`** applies the chosen action to the simulated world and advances
the physics by one tick. It hands back five things. The new
`observation` is the world *after* the move (we overwrite the old one, so
the next loop reads the fresh view). `reward` is a single number scoring
how well things are going (higher is better — getting closer to a
successful pick). `terminated` is a yes/no flag meaning "the task finished
properly" (the vial was picked). `truncated` is a yes/no flag meaning
"we ran out of allotted time." `info` is extra detail we ignore.

**`if step % 20 == 0:`**
This prints a progress line only occasionally, so the terminal is not
flooded. The symbol `%` gives the remainder after division; `step % 20`
is zero only on steps 0, 20, 40, and so on. So the next line runs once
every twenty steps.

**`print(f"step {step}: reward so far = {reward}")`**
This prints a short status line. The `f"..."` is an **f-string**, a
Python way of dropping live values straight into text: `{step}` is
replaced by the current step number and `{reward}` by the current score.
Watching the reward gives you a feel for whether the policy is making
progress.

**`if terminated or truncated:`**
This checks whether *either* finishing flag has turned true — the task
succeeded, or time ran out. The word `or` means "if at least one of these
is true."

**`print("Episode finished.")`** and **`break`**
If the episode is over, we print a note and then `break`, which means
"jump out of the loop immediately." (An **episode** is one full attempt
at the task, from reset to finish.) There is no reason to keep stepping a
world that has already finished.

**`env.close()`**
After the loop, this shuts the simulation window and frees its resources
cleanly — the tidy way to end.

**`if __name__ == "__main__":`**
A standard Python guard meaning "only run the next line if this file was
launched directly, not imported by another file." It keeps the program
from starting itself unexpectedly when reused.

**`main()`**
This finally calls the `main` function, setting everything above in
motion.

## How to run it, and how you know it worked

In a terminal, from the folder containing the file:

```bash
python3 run_smolvla.py
```

The **first** run pauses for a while as it downloads the trained model
from Hugging Face — that is normal, and it only happens once. Then a
simulation window opens and you watch the arm move. The terminal prints a
reward line every twenty steps; if the policy is doing well, those
numbers trend upward, and eventually you see `Episode finished.`

**Done when:** the pretrained SmolVLA model loads, a simulation window
opens, and you watch a *learned* policy — not your own hand-written
rules — drive the arm toward the vial. Even a clumsy, half-successful
pick counts: the goal is to have *run* the model.

**If it does not run:** that is expected on this fast-moving stack. The
most common problems are (1) a class or method that was renamed — check
the current LeRobot documentation for the new name; (2) the simulation
world `lerobot/pick-vial-v0` not existing under that exact name — list
the environments your version ships and pick the closest pick task; or
(3) no Graphics Processing Unit, making it too slow — try a smaller or
shorter run. Reading and understanding the shape of the program is itself
a valid outcome for a stretch exercise.

## Where this fits

- This is the first of the two **Layer 5** stretch exercises in
  [`../07-learning-checklist.md`](../07-learning-checklist.md). The
  second, [`07-gemini-plans-the-task.md`](07-gemini-plans-the-task.md),
  uses a *closed* frontier model as a planner instead of a policy.
- The deeper write-up comparing open and closed Vision-Language-Action
  models (and why SmolVLA is the friendly first one to try) is
  [`../04-mycobot-280-impl/foundation-models.md`](../04-mycobot-280-impl/foundation-models.md).
- A learned policy like this is one possible replacement for the
  hand-written grasping logic discussed in
  [`../04-mycobot-280-impl/01-only-code/05-grasping-and-manipulation.md`](../04-mycobot-280-impl/01-only-code/05-grasping-and-manipulation.md).
  For version 1 we keep the simple hand-written approach and treat
  learned policies like this one as a later milestone.
```