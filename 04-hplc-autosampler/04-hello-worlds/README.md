# 02 — Hello worlds: runnable code for every checklist exercise

> **What this folder is.** The learning plan in
> [`../09-learning-checklist.md`](../09-learning-checklist.md) asks you to
> write one small "hello world" program per layer of the robot software
> stack. **This folder contains the actual code for every one of those
> exercises** — and, crucially, **explains every single line in plain
> language**, written for a reader who has *never* worked in robotics and
> is not a confident programmer. Every technical word is spelled out in
> full the first time it appears; there is no assumed vocabulary.

> **Disclaimer.** These are **teaching programs**: deliberately small,
> simplified, and focused on one idea each. They favour clarity over
> production-readiness. Software versions and install commands drift over
> time — if a command fails, check the current documentation for the tool
> in question. Where a program needs the full robot simulator running,
> the file says so plainly.

---

## How every file in this folder is organised

Each numbered file follows the exact same shape, so once you have read
one you know how to read them all:

1. **What this program proves** — in one short paragraph, in plain
   English: what you will see happen, and why it matters.
2. **What you need first** — the software to install, written out as
   simple commands.
3. **The whole program** — the complete code in one block, with a
   filename, so you can copy it and run it.
4. **Every line explained** — we walk through the program from top to
   bottom. Each line (or small group of closely-related lines) gets a
   plain-language explanation. No abbreviation is left undefined.
5. **How to run it, and how you know it worked** — the exact commands,
   and the visible result that means "done."
6. **Where this fits** — links back to the checklist exercise and to the
   deeper write-up of that layer.

---

## A few words that appear in many files (defined once here)

These come up repeatedly. Each file also re-defines the terms it uses,
but here is the short version so the table below makes sense:

- **The Robot Operating System, version 2** (often written "ROS 2"):
  *not* an operating system like Windows. It is a free toolkit that lets
  the many small programs running on a robot find each other and pass
  messages back and forth. We use its **Python** interface, a library
  called **`rclpy`** ("R-C-L-Python," short for "ROS Client Library for
  Python").
- **A node** — one small program that does one job inside this robot
  system (for example, "the program that watches the weighing scale").
- **A topic** — a named channel that nodes use to broadcast a stream of
  readings (for example, a channel called `/balance/mass` carrying the
  weight in grams). One node *publishes* to it; any number *subscribe*.
- **A service** — a request-and-reply between two nodes: one node asks
  ("please remove the cap") and waits for the other to answer ("done").
- **Gazebo** — a free physics simulator: a video-game-like world with
  gravity and collisions, where we test the robot with no real hardware.
- **The myCobot 280** — the small six-joint desktop robotic arm this
  whole project is built around.
- **A 2 millilitre vial** — the small glass sample bottle the arm picks
  up; about 12 millimetres across, the size of a thumb.

---

## The exercises, in order

| Checklist layer | Hello world | Code file |
|---|---|---|
| 1 — Simulator & digital twin | Spawn the cell (arm + table + vial in the simulator) | [`01-spawn-the-cell.md`](01-spawn-the-cell.md) |
| 2 — Middleware & control | The mock decapper (a request/reply service + a reading stream) | [`02-mock-decapper.md`](02-mock-decapper.md) |
| 3 — Arm motion planning | Reach the vial (plan a collision-free arm motion) | [`03-reach-the-vial.md`](03-reach-the-vial.md) |
| 4 — Perception & vision | See the tray (find a printed marker, measure where it is) | [`04-see-the-tray.md`](04-see-the-tray.md) |
| 5 — Grasping | Grab the vial (work out the grip, close the hand, check it) | [`05-grab-the-vial.md`](05-grab-the-vial.md) |
| 5 — Learned policy (stretch) | Run a learned policy (SmolVLA) in the simulator | [`06-run-smolvla-in-sim.md`](06-run-smolvla-in-sim.md) |
| 5 — Frontier planner (stretch) | Let a large model plan the task (Gemini Robotics-ER) | [`07-gemini-plans-the-task.md`](07-gemini-plans-the-task.md) |
| 6 — Identification | Read the vial's identity (decode the barcode) | [`08-read-the-vial-id.md`](08-read-the-vial-id.md) |
| 7 — Orchestration | The per-vial loop (a decision tree that retries on failure) | [`09-per-vial-loop.md`](09-per-vial-loop.md) |
| 8 — Software & compliance | The mock records system and tamper-evident log | [`10-mock-lims-and-audit.md`](10-mock-lims-and-audit.md) |
| S — Sensors | Subscribe to a sense (turn a sensor reading into a pass/fail) | [`11-subscribe-to-a-sense.md`](11-subscribe-to-a-sense.md) |
| 3 ext — Closing the loop | Keep the world current (stream moving obstacles into MoveIt) | [`12-keep-the-world-current.md`](12-keep-the-world-current.md) |
| 3 ext — Closing the loop | Watch the move (command MoveIt continuously, then verify it landed) | [`13-watch-the-move.md`](13-watch-the-move.md) |
| Part C — Capstone | The whole loop, one vial start to finish | [`14-hello-cell-capstone.md`](14-hello-cell-capstone.md) |

---

## See also

- The learning plan these implement:
  [`../09-learning-checklist.md`](../09-learning-checklist.md).
- The deeper, per-layer framework write-ups (pure-simulation versions):
  [`../06-mycobot-280-impl/01-only-code/`](../06-mycobot-280-impl/01-only-code/README.md).
- The problem all of this is solving:
  [`../03-high-level-solution/`](../03-high-level-solution/README.md).
- Plain-language dictionary of robotics words:
  [`../../03-place-items-on-shelf/02-glossary.md`](../../03-place-items-on-shelf/02-glossary.md).
