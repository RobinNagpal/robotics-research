# CLAUDE.md

Guidance for Claude when working in this repository.

## What this repo is

A **documentation / research repository** — there is no application code,
no build, and no test suite. It is a structured written analysis of the
robotics landscape, used to decide what a small software-primary team
should build and sell. Everything here is Markdown prose, tables, and
the occasional ASCII diagram.

Because there is nothing to compile or run, "doing a task" here means
**writing, restructuring, and cross-linking Markdown** — accurately, in
plain language, and consistently with the conventions below.

## Layout

```
README.md                  Strategic overview: the 9 robotics subfields, top-3 picks, market data
01-all-areas/              One folder per subfield (robot-learning, perception-cv, sim-twins, slam-nav,
                           manipulation, motion-planning, hri-language, multi-robot, infra-middleware).
                           Each holds the same numbered files: 00-basics, 01-examples, 02-learn,
                           03-start, 04-market, 05-projects, 06-courses, README.
02-hplc-autosampler/       *** THE MAIN WORKING PROJECT (see below) ***
03-models/                 Per-type deep dives on the AI/robotics model families (VLAs, perception,
                           grasp-generation, robotics foundation models, …) the project can draw on.
```

## The main project: 02-hplc-autosampler

**This is the active working area now.** Everything new happens here
unless told otherwise. It is a concrete, buildable robotics project — a
**fixed robot arm that prepares and loads sample vials for an HPLC
autosampler**, automating the slow, manual vial-prep in front of the
instrument. It is **simulation-first**: prove the whole
pick-decap-dispense-cap-label-load loop in a simulator, then transfer to
hardware.

Structure (the numeric prefix is the intended reading order):

```
01-hplc-intro.md          Plain-language intro to HPLC and what an autosampler does — start here.
02-lab-bench-new.md       Sample-prep primer: how prep works in a real lab, broken into the discrete
                          tasks a robotic arm could automate (two worked examples).
03-hplc-workflow/         One deep, beginner file per sample-prep step (weigh, dissolve, dilute, filter,
                          transfer, cap, label, place), each walked through the same two examples.
04-mycobot-280-impl/      The per-concern implementation worked out on the low-cost myCobot 280 — fully
                          open-source, simulation-first. Holds the 10 development-layer files (simulator,
                          middleware, motion, perception, grasping, …) plus sensor-suite.md and
                          foundation-models.md.
05-arms-comparison.md     Which candidate arm to simulate first, scored on 30 parameters.
06-learning-checklist.md  A checkbox plan to learn just enough robotics to build and pitch this.
```

The recommended open-source stack at a glance: **Gazebo Harmonic** (sim),
**ROS 2** (middleware), **MoveIt 2** (arm motion), **RGB-D + YOLO
object detection** (perception), **analytical grasping** (with VLAs as a
deferred upgrade), **Behavior Trees** (orchestration) — on the **myCobot
280** for a cheap, simulation-first proof of concept. Keep
recommendations consistent across files — if a pick changes in one
place, reconcile every file that references it.

## Conventions to follow

- **Numeric filename prefixes** (`01-`, `02-`, …) encode reading order.
  When inserting a file in the middle, renumber with `git mv` so history
  is preserved; then fix every reference to the renamed/renumbered file
  (grep for the old name to confirm none are left).
- **Plain language first.** This material is read by non-experts. Define
  jargon on first use (the sample-prep primer `02-lab-bench-new.md` and
  the `03-hplc-workflow/` files do this). Short sentences.
- **Tables for comparisons**, prose for the "why." Every comparison table
  ends with a "Bottom line"/verdict column and is followed by a clear top
  pick.
- **Markdown style** already in use: wrap prose at ~72 columns, use
  `**bold**` for the key term in a bullet, fenced code blocks for trees
  and diagrams, relative links between files (e.g. `02-lab-bench-new.md`,
  `../01-hplc-intro.md`).
- **Keep the v1 "keep it simple" framing**: analytical/geometric methods
  first for motion and grasping, with **YOLO object detection** (trained
  on synthetic data from the twin) as the real perception workflow;
  heavier learned methods (e.g. VLAs) stay deferred to later milestones.
  Don't add scope.
- **Cost/spec figures are approximate and drift** — hedge them (`~`) and
  flag that they should be re-checked before being quoted.

## Git workflow

- Default branch is `main`. Commit with clear, descriptive messages and
  push when a unit of work is complete. Do not open pull requests unless
  explicitly asked.
- Prefer staging files by name over `git add -A`.
- Use `git mv` for renames/moves so history is preserved.
