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
02-sim-vs-perception/      A focused decision note comparing two of the top picks.
03-place-items-on-shelf/   *** THE MAIN WORKING PROJECT (see below) ***
```

## The main project: 03-place-items-on-shelf

**This is the active working area now.** Everything new happens here
unless told otherwise. It is a concrete, buildable robotics project — a
**mobile manipulator that stocks a grocery shelf** — worked out from
requirements down to a per-layer technology stack. It is
**simulation-first**: prove the whole pick-drive-place loop in a
simulator, then transfer to hardware.

Structure (the numeric prefix is the intended reading order):

```
01-requirements.md     The "simplest viable version" — scope constraints, the robot, the
                       9-step functional loop, non-goals, definition of done.
02-glossary.md         Plain-language definitions (1-2 sentences each) of every technical term
                       used in the tech docs. READ THIS FIRST when a term is unfamiliar.
03-high-level-tech.md  The "Stack at a glance" table + narrative: the 7 layers and the
                       recommended framework for each.
03-stack/              One deep-dive file per stack layer:
                         01-simulator, 02-middleware, 03-mobile-base-navigation,
                         04-arm-motion-planning, 05-perception, 06-grasping, 07-orchestration.
                       Each file follows the same shape:
                         - intro blockquote ("Job:" — what the layer does)
                         - "How this layer fits into the architecture" (plain-language, cross-linked)
                         - a comparison table of candidate frameworks on 5-7 parameters + a
                           "Bottom line" column
                         - "Top choice" (technical pick)
                         - "Cost, hardware & where it runs" (best-in-class / cheapest /
                           best cost-for-performance tiers, with machine requirements and cost)
```

The recommended stack at a glance: **Isaac Sim** (sim, with Gazebo
first), **ROS 2** (middleware), **Nav2** (navigation), **MoveIt 2** (arm
motion), **RGB-D + FoundationPose / geometric** (perception), **analytical
→ AnyGrasp** (grasping), **Behavior Trees** (orchestration). Keep
recommendations consistent across files — if a pick changes in one
place, reconcile every file that references it.

## Conventions to follow

- **Numeric filename prefixes** (`01-`, `02-`, …) encode reading order.
  When inserting a file in the middle, renumber with `git mv` so history
  is preserved; then fix every reference to the renamed/renumbered file
  (grep for the old name to confirm none are left).
- **Plain language first.** This material is read by non-experts. Define
  jargon on first use or point to `02-glossary.md`. Short sentences.
- **Tables for comparisons**, prose for the "why." Every comparison table
  ends with a "Bottom line"/verdict column and is followed by a clear top
  pick.
- **Markdown style** already in use: wrap prose at ~72 columns, use
  `**bold**` for the key term in a bullet, fenced code blocks for trees
  and diagrams, relative links between files (e.g. `02-middleware.md`,
  `../01-requirements.md`).
- **Keep the v1 "keep it simple" framing**: geometric/known-pose methods
  first, learned methods deferred to later milestones. Don't add scope.
- **Cost/spec figures are approximate and drift** — hedge them (`~`) and
  flag that they should be re-checked before being quoted.

## Git workflow

- Default branch is `main`. Commit with clear, descriptive messages and
  push when a unit of work is complete. Do not open pull requests unless
  explicitly asked.
- Prefer staging files by name over `git add -A`.
- Use `git mv` for renames/moves so history is preserved.
