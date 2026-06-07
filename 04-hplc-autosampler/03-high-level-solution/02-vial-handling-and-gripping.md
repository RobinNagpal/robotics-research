# Part 02 — Vial handling & gripping

> **Problem:** Almost every step in this system begins and ends with the
> arm holding a small glass vial — and a vial that is dropped, crushed,
> or held inconsistently breaks the whole run. Reliable gripping is the
> foundation everything else stands on.

## The problem

A standard HPLC vial is small (~12 mm outside diameter), light (a few
grams empty), made of thin glass, and often has a smooth or even
slightly slippery exterior. That combination is hard for a robot in
several specific ways:

- **Don't crush.** Thin glass cracks or shatters under modest jaw force.
  Cracked glass means broken-glass cleanup, a lost sample, and possible
  contamination of the bench and the arm.
- **Don't drop.** The vial is light and smooth, so a too-gentle or
  poorly aligned grip lets it slip — especially as it gets heavier after
  filling, or when the arm accelerates between stations.
- **Grip the same way every time.** Downstream steps (decapping,
  dispensing, capping, tray insertion) assume the vial is held at a
  known height and orientation. An inconsistent grip throws off every
  pose that follows.
- **Vials arrive in different presentations.** A vial may sit in a
  **rack nest** (a molded hole that locates it) or stand **free** on a
  surface. A nested vial is easy to find but can bind on the way out; a
  free-standing vial can tip.
- **Contamination and fingerprints.** Bare metal or dirty fingertips can
  leave residue on the glass in the optical path or transfer
  carry-over between samples. Grip surfaces must be clean and, ideally,
  contact only the lower body of the vial, away from the neck/septum.
- **Fragile and irreplaceable contents.** Once filled, a dropped vial
  is not just a broken consumable — it is a lost, often
  un-reproducible, sample on the critical path of an analysis.

Why it matters: gripping is not a sub-feature, it is the load-bearing
primitive. If the grip is unreliable, no amount of clever orchestration
above it can be trusted.

## The solution

Two gripper families dominate the sensible options, plus the supporting
techniques that make either one reliable.

| Option | How it grips | Pros | Cons | Bottom line |
|---|---|---|---|---|
| **Parallel-jaw + shaped elastomer fingertips** | Two jaws close on the vial body; soft fingertips with a vial-shaped groove cradle it | Cheap, ubiquitous, easy force control; groove gives repeatable centering; compliant pad spreads load so glass isn't crushed | Slightly less self-centering than a collet; fingertip geometry is vial-specific | **Best v1 choice** — simple, forgiving, one part to design |
| **Collet / centering gripper** | A ring of jaws (or an iris) closes concentrically around the vial | Excellent centering and repeatable orientation regardless of approach | More expensive/specialized; geometry tied to one diameter; harder to swap sizes | Use later if centering precision becomes the limit |

**Grip-force control.** Whichever gripper, the key safety feature is
controlling *how hard* it squeezes — either an electric gripper with
programmable force/current limits or a pneumatic gripper with a
regulated pressure. We pick a force just above what reliably holds a
filled vial through the fastest planned move, and well below what cracks
the glass, then keep a margin.

**Grip-detection feedback** — "did we actually grab it?" The gripper
reports its final jaw width (or position). If the jaws closed *past* the
expected vial diameter, there is no vial between them (a missed pick); if
they stopped *short*, something is wrong (double vial, debris). This
single check catches the most common silent failure and feeds the
verification logic in `07-perception-and-verification.md`.

**Presentation racks with known nests.** The biggest reliability win is
upstream of the gripper: present empty vials in a **supply rack with
molded nests at known positions**. The arm then approaches a taught
pose rather than searching, and the nest holds the vial steady during
the grab. This is why v1 insists on a known-position supply rack.

**Approach and retreat poses.** The arm approaches each vial from
directly above (or along the nest axis), descends to a taught grip
height on the lower vial body, closes, then retreats straight up before
moving laterally — so it never drags the vial against the nest wall.
Capping and tray slots use the same straight-in / straight-out
discipline.

**Regrasping.** Some steps want the vial held differently (e.g. low on
the body for picking, but the cap exposed for decapping). When one grip
can't serve every step, the arm sets the vial in a known holder and
re-grips at a different height. v1 minimizes regrasps by choosing a
single grip pose that clears all stations; richer regrasping is
deferred.

## v1 vs later

**v1 — keep it simple.**

- **One vial size** (the single 2 mL screw-cap vial from
  `01-scope-and-workflow.md`), so fingertip geometry and grip width are
  fixed and tuned once.
- **Nested supply rack with known positions** — no vision-based search
  to pick; the arm goes to a taught pose.
- **A single fixed grip pose** — one height on the vial body, one
  orientation, used everywhere, to avoid regrasping.
- **Parallel-jaw gripper with shaped elastomer fingertips** and
  **force-limited closing + width-based grip detection**.

**Deferred to later.** Multiple vial sizes and cap styles (would need
adjustable or swappable fingertips); **tool-changer swaps** between the
gripper and other end-effectors such as a pipettor or a capper;
collet/iris grippers for tighter centering; vision-guided picking of
free-standing or randomly placed vials; multi-step regrasping
strategies; tactile/slip sensing beyond simple width feedback.

## How it connects

- **`03-decapping-and-capping.md`** — decapping needs the vial held
  steady at a known pose while the cap is turned; the grip here is what
  makes that possible.
- **`04-liquid-handling-and-sample-prep.md`** — the held, open vial is
  presented to the dispense station at a known mouth position.
- **`05-tray-loading-and-positioning.md`** — the same consistent grip
  lets the arm seat the vial straight into a tray slot without binding.
- **`07-perception-and-verification.md`** — grip-detection width and a
  vision check together confirm a vial is actually held before any
  downstream step runs.
- Back to the index: [`README.md`](README.md).
