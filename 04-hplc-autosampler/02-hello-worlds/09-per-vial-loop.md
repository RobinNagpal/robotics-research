# 09 — The per-vial loop (Orchestration)

> Checklist exercise: **Layer 7 — "the per-vial loop."**
> See [`../07-learning-checklist.md`](../07-learning-checklist.md).

## What this program proves

A robot must never **charge ahead** when a step has quietly failed. If the
arm tries to *place* a vial it never actually picked up, it will drop an
imaginary vial onto the tray and ruin the run. So the most important skill
in this whole project is not moving the arm — it is *deciding what to do
next*, and in particular *what to do when a step does not work*.

The clean way to write that decision logic is a **behaviour tree** (a
standard way to organise a robot's decisions as a tree of simple steps).
Instead of a tangle of "if this then that, but if also that, unless this"
statements, you build a small tree of named steps, and a rulebook decides
which step runs next based on whether the last one **succeeded** or
**failed**.

This program builds the per-vial decision logic as such a tree and runs
it on your computer — no robot, no simulator. The tree does this:

1. **Pick** the vial.
2. **Check it is held** — and if it is not, **retry the pick** once.
3. **Place** the vial in its slot.
4. **Check it is seated** — and if it is not, send the vial to
   **quarantine** (set it aside) instead of carrying on.

To prove the safety branches really fire, the program is rigged so the
first "check it is held" *fails on purpose*. You will watch the tree
notice the failure, retry the pick, and recover — and in a second run you
will force a hard failure so you can watch the quarantine branch fire.

> This is teaching code: the "pick," "place," and "check" steps are mock
> stand-ins that just print and return success or failure, so you can see
> the decision logic on its own. The real steps — which drive the arm and
> read sensors — live in the deeper write-up linked at the bottom.

## What you need first

This exercise needs **no robot and no simulator** — it is plain Python.
You only need one small library (a **library** is a bundle of ready-made
code you bring into your program):

- `py_trees` — a behaviour-tree library. It builds and runs the tree of
  decisions entirely on its own, without the robot framework, which makes
  it ideal for learning the idea in isolation.

Install it like this:

```bash
pip install py_trees
```

Three words used throughout will help to know up front:

- A **tick** is one pass through the tree, top to bottom, asking each step
  in turn "what is your status right now?" A running robot ticks its tree
  many times a second; here we tick it by hand so we can read each pass.
- A step's **status** after a tick is one of three words: **SUCCESS** (it
  is done and it worked), **FAILURE** (it is done and it did not work), or
  **RUNNING** (it is still working, ask again next tick).
- A **Sequence** and a **Selector** are the two ways to join steps; they
  are explained line by line below, but in one breath: a Sequence is an
  *and* (do all of these, in order, stop on the first failure), and a
  Selector is an *or* (try these in order, stop on the first success).

## The whole program

Save this as a file named `per_vial_loop.py`:

```python
import py_trees


class Pick(py_trees.behaviour.Behaviour):
    def update(self):
        print("  pick: closing gripper on the vial")
        return py_trees.common.Status.SUCCESS


class CheckHeld(py_trees.behaviour.Behaviour):
    def __init__(self, name, fail_first=False):
        super().__init__(name)
        self.fail_first = fail_first
        self.times_checked = 0

    def update(self):
        self.times_checked += 1
        if self.fail_first and self.times_checked == 1:
            print("  check-held: gripper is EMPTY (failed)")
            return py_trees.common.Status.FAILURE
        print("  check-held: vial is held (ok)")
        return py_trees.common.Status.SUCCESS


class RetryPick(py_trees.behaviour.Behaviour):
    def update(self):
        print("  retry-pick: opening, re-aligning, picking again")
        return py_trees.common.Status.SUCCESS


class Place(py_trees.behaviour.Behaviour):
    def update(self):
        print("  place: lowering the vial into its slot")
        return py_trees.common.Status.SUCCESS


class CheckSeated(py_trees.behaviour.Behaviour):
    def __init__(self, name, always_fail=False):
        super().__init__(name)
        self.always_fail = always_fail

    def update(self):
        if self.always_fail:
            print("  check-seated: vial is NOT seated (failed)")
            return py_trees.common.Status.FAILURE
        print("  check-seated: vial is seated (ok)")
        return py_trees.common.Status.SUCCESS


class Quarantine(py_trees.behaviour.Behaviour):
    def update(self):
        print("  QUARANTINE: setting the vial aside, run continues safely")
        return py_trees.common.Status.SUCCESS


def build_tree(held_fails_first, seating_always_fails):
    held = py_trees.composites.Selector(name="ensure-held", memory=True)
    held.add_children([
        CheckHeld("check-held", fail_first=held_fails_first),
        RetryPick("retry-pick"),
    ])

    seated = py_trees.composites.Selector(name="ensure-seated", memory=True)
    seated.add_children([
        CheckSeated("check-seated", always_fail=seating_always_fails),
        Quarantine("quarantine"),
    ])

    root = py_trees.composites.Sequence(name="per-vial", memory=True)
    root.add_children([Pick("pick"), held, Place("place"), seated])
    return root


def run(label, held_fails_first=False, seating_always_fails=False):
    print(f"\n=== {label} ===")
    tree = build_tree(held_fails_first, seating_always_fails)
    for tick in range(1, 6):
        print(f"tick {tick}:")
        tree.tick_once()
        print(f"  -> root status: {tree.status.name}")
        if tree.status != py_trees.common.Status.RUNNING:
            break


def main():
    run("Happy path (everything works)")
    run("Held check fails once, then recovers",
        held_fails_first=True)
    run("Seating keeps failing -> quarantine",
        seating_always_fails=True)


if __name__ == "__main__":
    main()
```

## Every line explained

**`import py_trees`**
The word `import` means "bring in a library of ready-made code so I can
use it." `py_trees` is the behaviour-tree library; every tool we use
below (the kinds of step, the joiners, the status words) comes out of it.

**`class Pick(py_trees.behaviour.Behaviour):`**
The word `class` starts the definition of one **kind of step** in the
tree. We name this one `Pick`. The `(py_trees.behaviour.Behaviour)` part
means "build it on top of the library's basic step blueprint," so it
automatically knows how to live inside a tree and report a status.

**`def update(self):`**
`def` begins a named block of instructions (a "function"). The special
name `update` is the one the library calls **once per tick** to ask this
step "what is your status right now?" Whatever this function returns is
the step's answer for that tick. The word `self` means "this particular
step."

**`print("  pick: closing gripper on the vial")`**
This prints a line so that, when the tree ticks, you can *see* this step
run. In the real robot this is where the arm would actually close its
gripper; here it just announces itself.

**`return py_trees.common.Status.SUCCESS`**
The word `return` hands an answer back. Here the answer is the status
**SUCCESS** — "I am done and it worked." A `Status` is one of three fixed
words (SUCCESS, FAILURE, RUNNING) the library understands; this is how a
step reports its outcome. Our mock pick always succeeds.

**`class CheckHeld(py_trees.behaviour.Behaviour):`**
Defines a second kind of step: the check that asks "is the vial actually
in the gripper?" This is the step we will rig to fail the first time, to
prove the retry branch works.

**`def __init__(self, name, fail_first=False):`**
The special name `__init__` is "the set-up steps that run once, the moment
this step is created." It takes a `name` (a label for the step) and a
switch `fail_first`, which defaults to `False` — meaning "behave normally
unless told otherwise."

**`super().__init__(name)`**
This runs the library's own set-up first, registering the step under the
name we gave it. `super()` means "the blueprint we were built on top of."

**`self.fail_first = fail_first`**
This stores the switch inside the step so the `update` function can read
it later. `self.fail_first` is this step's own private copy.

**`self.times_checked = 0`**
This starts a counter at zero. Each time the check runs it will add one,
so the step can tell whether this is the *first* time it has been asked.

**`def update(self):`** (inside `CheckHeld`)
The once-per-tick function again, this time deciding whether the vial is
held.

**`self.times_checked += 1`**
This adds one to the counter. `+= 1` means "take the current value and
increase it by one." After the first tick it is 1, after the second it is
2, and so on.

**`if self.fail_first and self.times_checked == 1:`**
This asks two questions joined by **and** (both must be true): "are we in
fail-on-purpose mode?" *and* "is this the very first check?" Only when
both hold do we fake a failure. `== 1` means "is exactly equal to one."

**`print("  check-held: gripper is EMPTY (failed)")`**
Announces the (faked) failure so you can see it happen.

**`return py_trees.common.Status.FAILURE`**
Reports the status **FAILURE** — "I am done and it did not work." This is
the trigger that will make the tree try the retry step next.

**`print("  check-held: vial is held (ok)")` and `return ... SUCCESS`**
Otherwise — not the first check, or not in fail mode — the vial is held,
so we say so and report SUCCESS. After a retry, this is the line that
runs, which is how the tree *recovers*.

**`class RetryPick(...)` with its `update`**
A step that re-does the pick: open the gripper, line up again, and pick
once more. Our mock version just prints and returns SUCCESS. In a real
cell this would actually re-drive the arm.

**`class Place(...)` with its `update`**
The step that lowers the vial into its tray slot. Mock version prints and
returns SUCCESS.

**`class CheckSeated(py_trees.behaviour.Behaviour):`**
The check that asks "did the vial actually settle into its slot?" We give
this one an `always_fail` switch so we can force a *hard*, never-recovers
failure and watch the quarantine branch fire.

**`def __init__(self, name, always_fail=False):` … `self.always_fail = always_fail`**
The same set-up pattern as before: take a name and a switch, run the
library's set-up, and store the switch for later. `always_fail` defaults
to `False`.

**`if self.always_fail:` … `return ... FAILURE`**
When the switch is on, this step fails *every* tick — it never recovers,
which is exactly the situation where carrying on would be dangerous.

**`else` branch: `print(... seated (ok))` and `return ... SUCCESS`**
When the switch is off, the vial is seated, so the step succeeds and the
vial is finished cleanly.

**`class Quarantine(...)` with its `update`**
The safety step: set the vial aside and let the run continue without it.
Crucially it returns **SUCCESS** — quarantining *is* the correct outcome
when a vial cannot be seated, so from the tree's point of view this branch
"worked."

**`def build_tree(held_fails_first, seating_always_fails):`**
Begins the function that assembles the whole tree. The two switches it
takes let us turn the two failure scenarios on or off without touching the
steps themselves.

**`held = py_trees.composites.Selector(name="ensure-held", memory=True)`**
This makes a **Selector** (also called a **fallback**). A Selector is an
*or*: it tries its children in order and **stops at the first one that
returns SUCCESS**; it only reports FAILURE if *every* child fails. That is
exactly the "try A, and if A fails fall back to B" shape we want.
`memory=True` tells it to remember where it got to between ticks rather
than restarting from the first child each tick.

**`held.add_children([CheckHeld(...), RetryPick("retry-pick")])`**
This fills the Selector with its two children **in order**: first try
`check-held`; only if that fails, fall back to `retry-pick`. The square
brackets make a list. So: if the vial is held, we are done; if not, we
retry the pick. We pass `fail_first=held_fails_first` so the rigged
failure is switched on only when we ask for it.

**`seated = py_trees.composites.Selector(name="ensure-seated", memory=True)`**
A second Selector, for the seating check, built the same way.

**`seated.add_children([CheckSeated(...), Quarantine("quarantine")])`**
Its two children in order: first try `check-seated`; only if that fails,
fall back to `quarantine`. So a seated vial finishes normally, and an
unseatable one is set aside instead of being processed.

**`root = py_trees.composites.Sequence(name="per-vial", memory=True)`**
This makes the top of the tree, a **Sequence**. A Sequence is an *and*: it
runs its children **in order** and **stops at the first one that returns
FAILURE**; it only reports SUCCESS if *every* child succeeds. This is the
backbone "do this, then this, then this — but stop the moment a step
fails" shape that stops the robot charging ahead.

**`root.add_children([Pick("pick"), held, Place("place"), seated])`**
This lays out the per-vial plan in order: **pick**, then the **ensure-held**
Selector, then **place**, then the **ensure-seated** Selector. Notice that
a child can itself be a whole Selector — that nesting is what makes a tree
a *tree*. Because it is a Sequence, if "ensure-held" ever reported FAILURE,
"place" would never run — the safety guarantee, for free.

**`return root`**
Hands the finished tree back to whoever asked to build it.

**`def run(label, held_fails_first=False, seating_always_fails=False):`**
Begins a helper that builds one tree and ticks it a few times so we can
watch it. `label` is just a heading to print; the two switches choose
which scenario to run.

**`print(f"\n=== {label} ===")`**
Prints a heading for this run. The `f` before the quotation marks makes it
a **formatted string**, so `{label}` is replaced by its real value; `\n`
adds a blank line above for readability.

**`tree = build_tree(held_fails_first, seating_always_fails)`**
Builds a fresh tree for this run, with the chosen switches.

**`for tick in range(1, 6):`**
This **loops** up to five times, with `tick` taking the values 1, 2, 3, 4,
5 in turn. `range(1, 6)` produces those numbers (it stops *before* 6).
Each pass of the loop is one tick of the tree.

**`print(f"tick {tick}:")`**
Prints which tick we are on, so the output is easy to follow.

**`tree.tick_once()`**
This is the heart of it: **tick the tree once** — make one pass through it,
asking each step in turn for its status and letting the Sequences and
Selectors decide what runs. The steps' `print` lines appear as this runs.

**`print(f"  -> root status: {tree.status.name}")`**
After the tick, this prints the overall status of the whole tree
(SUCCESS, FAILURE, or RUNNING). `.name` turns the status into its plain
word for printing.

**`if tree.status != py_trees.common.Status.RUNNING:`**
This checks whether the tree has *finished* — that is, whether its status
is anything other than RUNNING. `!=` means "is not equal to." A finished
tree has nothing left to do, so there is no point ticking it again.

**`break`**
The word `break` stops the loop early. Together with the line above, it
means "as soon as the tree finishes, stop ticking." (Our mock steps finish
in a single tick, so each run here ends on tick 1; the loop is written to
allow more ticks because real steps often report RUNNING for a while.)

**`def main():`**
Begins the program's main routine — the steps that run when you launch the
file.

**`run("Happy path (everything works)")`**
Runs the tree with both switches off: every step succeeds, so the vial is
picked, confirmed held, placed, confirmed seated — done.

**`run("Held check fails once, then recovers", held_fails_first=True)`**
Runs it with the held-check rigged to fail the first time. Watch the
Selector notice the failure, fall back to `retry-pick`, and then — on the
retry — confirm the vial is held. This is the **retry-then-recover**
branch.

**`run("Seating keeps failing -> quarantine", seating_always_fails=True)`**
Runs it with the seating check rigged to fail forever. Watch that
Selector exhaust its first child and fall back to `quarantine`, setting
the vial aside instead of continuing. This is the **quarantine** branch.

**`if __name__ == "__main__":`**
A standard Python guard meaning "only run the next line if this file was
launched directly, rather than being imported by another file." It keeps
the program from starting itself when its steps are reused elsewhere.

**`main()`**
Finally calls the main routine, setting everything above in motion.

## How to run it, and how you know it worked

In a terminal, from the folder containing the file:

```bash
python3 per_vial_loop.py
```

You should see three runs. The happy path looks roughly like this:

```
=== Happy path (everything works) ===
tick 1:
  pick: closing gripper on the vial
  check-held: vial is held (ok)
  place: lowering the vial into its slot
  check-seated: vial is seated (ok)
  -> root status: SUCCESS
```

The second run shows the **retry** firing — the held check fails, the
retry pick runs, and the vial ends up held:

```
=== Held check fails once, then recovers ===
tick 1:
  pick: closing gripper on the vial
  check-held: gripper is EMPTY (failed)
  retry-pick: opening, re-aligning, picking again
  place: lowering the vial into its slot
  check-seated: vial is seated (ok)
  -> root status: SUCCESS
```

The third run shows **quarantine** firing — the seating check fails and
the vial is set aside, yet the run ends safely (SUCCESS, because
quarantining was the right thing to do):

```
=== Seating keeps failing -> quarantine ===
tick 1:
  pick: closing gripper on the vial
  check-held: vial is held (ok)
  place: lowering the vial into its slot
  check-seated: vial is NOT seated (failed)
  QUARANTINE: setting the vial aside, run continues safely
  -> root status: SUCCESS
```

**Why this beats a tangle of if-statements:** each step is a tiny,
self-contained piece that only reports success or failure; the Sequence
and Selector rules decide the flow. To add a new safety check you drop in
one more step — you do not rewrite a giant nest of conditions, and you can
never accidentally "place" after a failed "pick," because the Sequence
stops on the first failure for you.

**Done when:** the happy path runs clean, the rigged held-check failure
visibly triggers the retry and then recovers, and the forced seating
failure visibly sends the vial to quarantine instead of charging ahead.

## Where this fits

- This is the runnable version of the **Layer 7** exercise in
  [`../07-learning-checklist.md`](../07-learning-checklist.md).
- The deeper write-up of orchestration — why a behaviour tree is the right
  way to structure the robot's decisions, and how the real steps plug in —
  is
  [`../04-mycobot-280-impl/01-only-code/07-orchestration-and-task-logic.md`](../04-mycobot-280-impl/01-only-code/07-orchestration-and-task-logic.md).
- The capstone, [`12-hello-cell-capstone.md`](12-hello-cell-capstone.md),
  wraps the real pick, place, and check steps in this very tree so the
  whole loop retries and quarantines exactly as you saw here.
