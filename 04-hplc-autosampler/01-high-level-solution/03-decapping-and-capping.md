# Part 03 — Decapping & capping

> **Problem:** Before liquid can go into or out of a vial it must be
> opened, and before it is injected it must be re-closed — and doing
> that reliably with a robot, under controlled torque and without
> contaminating or mixing up caps, is the single hardest piece of
> manipulation in this whole system.

## The problem

A **vial** is the small glass container (commonly 2 mL) that holds a
sample. Its cap is what keeps the liquid sealed, clean, and from
evaporating. Three cap families show up in HPLC labs:

- **Screw caps with a septum.** A threaded plastic cap; the **septum**
  is a thin silicone/PTFE disc in the cap that the autosampler needle
  pierces to draw liquid. Opening and closing means *threading* —
  turning the cap onto matching threads at a controlled torque.
- **Snap / press caps.** Pushed straight down to seal, pulled or pried
  off to open. No threading, but they need a firm axial push and a
  defined pull-off force.
- **Crimp caps.** A soft aluminium cap crimped (mechanically deformed)
  over the vial lip with a crimping tool, and removed with a
  *decrimper*. These give the best seal for volatile samples but are
  effectively one-way — you destroy the cap to open it — and crimping
  needs a dedicated tool with real force.

What makes this hard for a robot, in plain terms:

- **Controlled torque.** Too loose and the vial leaks or the
  autosampler reports a bad seal; too tight and you **cross-thread**
  (the cap bites the threads at an angle and jams or strips them) or
  crack the glass. A human feels this; a robot needs torque sensing.
- **Precise alignment.** The cap and vial axes must line up within a
  fraction of a millimetre before the first turn, or the very first
  thread cross-threads.
- **Holding the vial against rotation.** When you twist a cap, the vial
  wants to spin too. Something must grip the vial body firmly enough to
  resist the capping torque without crushing thin glass — see
  [`02-vial-handling-and-gripping.md`](02-vial-handling-and-gripping.md).
- **Septum contamination.** Touching, breathing on, or dropping debris
  on the septum surface ruins the analysis. Caps must be handled by the
  rim, kept upright, and kept clean.
- **Cap tracking.** In many workflows the *same* cap must go back on the
  *same* vial (cross-contamination, labeling). Lose track of which cap
  is which and the whole tray is suspect.

Mistakes here are expensive: a single leaking or cross-threaded vial can
fail a regulated batch and trigger an investigation.

## The solution

The core design choice is **where the torque comes from**: a dedicated
**decapper/capper station** that the arm feeds vials into, or a
**torque-controlled end-effector tool** the arm picks up from a
tool-changer (a quick-connect interface that lets one arm swap between
gripper, decapper, pipettor, etc.).

**Recommended: a dedicated station.** The arm presents the vial to a
fixed station that does the actual gripping-and-twisting with purpose-
built jaws, a calibrated torque motor, and a known geometry. The arm
only has to position the vial accurately and hold it — the hard,
safety-critical torque control lives in a proven, single-purpose device.
Lab-automation vendors already sell exactly these (automated
decappers/cappers and crimpers), so this is buying a solved problem
rather than inventing one.

A **tool-changer decapper** flips the responsibility: the arm carries a
motorised, torque-sensing capping tool and does the work itself. It is
more flexible (no separate station footprint, the arm can decap in
place) but pushes all the alignment and torque control onto the arm and
its tool, which is the part most likely to mis-thread.

Either way the system needs:

- **Cap parking / handling.** Once removed, a cap must go somewhere
  clean, upright, and tracked — a per-vial parking nest beside the vial,
  or a one-cap-per-position fixture — so the right cap returns to the
  right vial. For disposable workflows, removed caps can be discarded
  and fresh caps fitted at recap, which sidesteps tracking entirely.
- **Torque sensing.** Measure the turning resistance so the system can
  stop at the target torque, detect a cross-thread early (torque spikes
  far too soon), and confirm a removed cap actually let go.
- **Recap integrity check.** After closing, confirm the seal — by final
  torque reached, cap seating height (a properly seated cap sits at a
  known height), or vision; see
  [`07-perception-and-verification.md`](07-perception-and-verification.md).

### Options compared

| Approach | Torque control | Flexibility | Footprint / cost | Risk | Bottom line |
|---|---|---|---|---|---|
| **Dedicated decap/cap station** (arm feeds vial) | Excellent — calibrated, purpose-built | One station per cap type | Extra bench station; ~moderate | Low — proven devices | **Recommended for v1.** Buys a solved problem; arm just presents the vial. |
| **Torque-controlled tool on tool-changer** | Good, but on the arm | High — decap anywhere, no station | Tool + changer cost; saves bench space | Higher — alignment/cross-thread on the arm | Powerful later, once the arm and tool are trusted. |
| **Plain gripper, no torque sensing** | None — open-loop turns | Low | Cheapest | Unacceptable — cross-threads, cracks glass | Don't. False economy in a regulated lab. |
| **Manual decap, robot does the rest** | Human | n/a | Lowest capital | Defeats the purpose | Only as a stopgap during bring-up. |

**Top choice: a dedicated decapping/capping station the arm feeds**, with
torque sensing in the station and a per-vial cap parking nest. It
isolates the riskiest physics in a proven device and keeps the arm's job
to accurate presentation and holding.

## v1 vs later

**v1 (simplest that proves the loop):**

- **Screw caps only**, one vial type, one cap geometry.
- A **single dedicated decapping/capping station**; the arm presents the
  vial and holds it against rotation while the station does the turning.
- Torque sensing in the station with fixed open/close torque targets.
- Simple recap check (target torque reached + cap seating height).
- One cap per vial, parked in a known nest beside the vial, or a fresh
  disposable cap at recap so there is nothing to track.
- Human supervising, ready to intervene on a flagged failure.

**Deferred to later:**

- **Crimp caps and decrimping** (destructive, needs a crimper tool and
  more force) and **snap/press caps**.
- A **torque-controlled tool-changer decapper** for in-place decapping.
- **Multi-cap handling** — many cap types/sizes in one run, automatic
  cap-type recognition, and large cap inventories.
- Vision-based seal/septum-integrity inspection beyond the basic check.

## How it connects

- [`02-vial-handling-and-gripping.md`](02-vial-handling-and-gripping.md)
  — the arm must already be holding the vial securely (and resisting
  rotation) before this step can twist a cap.
- [`04-liquid-handling-and-sample-prep.md`](04-liquid-handling-and-sample-prep.md)
  — decapping is what makes the vial *open* so liquid can be dispensed
  into or drawn from it; recapping happens after prep.
- [`07-perception-and-verification.md`](07-perception-and-verification.md)
  — vision/sensing confirms the cap was actually removed before
  dispensing and properly seated after recap.
- [`08-orchestration-error-handling-and-safety.md`](08-orchestration-error-handling-and-safety.md)
  — defines what happens on a decap/cap failure (cross-thread, cap won't
  release, bad seal): retry, quarantine the vial, or safe-stop.
- Back to the index: [`README.md`](README.md).
