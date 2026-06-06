# Part 05 — Tray loading & positioning

> **Problem:** A prepared vial is worthless if it ends up in the
> wrong slot — the arm must drop each 2 mL vial into the exact
> autosampler-tray position the worklist demands, fully seated and
> without nudging its neighbours.

## The problem

The **autosampler** is the device that automatically draws sample
from a vial and injects it into the HPLC. It reads vials from a
**tray** (also called a rack): a flat holder with many small
cylindrical pockets — **slots** — arranged in a regular grid.

After a vial is prepared (filled, capped, labelled) the arm has to
place it in the *right* slot. "Right" has two meanings:

- **Geometric correctness** — the vial must physically end up
  centred and fully seated in a slot, not perched on the rim,
  tilted, or jammed.
- **Logical correctness** — that slot must be the one assigned to
  this sample by the **worklist** (the ordered run list the
  autosampler executes top to bottom). Worklist row 1 might map to
  physical slot **A1**, row 2 to **A2**, and so on.

Trays come in fixed layouts. Common formats:

- ~48- or ~54-position trays of standard 2 mL vials.
- ~100-position high-density trays.
- **Well-plate-style** holders (a plate of small wells in a grid,
  e.g. 96 positions) for micro-volume work.

All of these share a key property: a **fixed pitch** — the
centre-to-centre spacing between slots is a known constant (often
only a few millimetres of clearance around each vial). That
regular geometry is what makes the placement automatable, but the
tight spacing is also what makes it hard.

The specific challenges:

- **Fine alignment.** Slot clearance is small. The arm must reach
  the slot centre within roughly a millimetre or the vial catches
  on the rim.
- **Seating without jamming.** A vial dropped slightly off-axis
  binds against the slot wall and stops short. Push harder and it
  jams or the gripper slips.
- **Not tipping or knocking neighbours.** In a dense grid the
  gripper fingers and the carried vial pass close to vials already
  placed. A clumsy approach can tip a neighbour.
- **Releasing cleanly.** The gripper must open and withdraw
  straight up without dragging the just-placed vial back out.

## The solution

Treat the tray as a **known model**: a calibrated map from each
slot name (A1, A2, …) to a 3-D position in the arm's coordinate
frame. Because the tray sits at a **fixed, known location** and has
fixed pitch, we only need to calibrate a few reference points and
compute the rest from the grid spacing.

**Calibration** options (how the model learns where the slots
actually are):

- **Fiducials** — a fiducial is a printed marker (e.g. an AprilTag
  or ArUco marker) at a known spot on the tray; a camera sees it
  and locks the tray's position and orientation.
- **Teaching** — a human jogs the arm to a corner slot (or three
  corners) once; the system records those points and derives the
  full grid from the known pitch.

Placement itself uses a **compliance / insertion strategy** so the
vial finds the slot even with small residual error, rather than
demanding perfect aim:

| Strategy | How it works | Hardware need | Robustness | Speed | Bottom line |
|---|---|---|---|---|---|
| **Pure position (open-loop drop)** | Move to the computed slot XYZ, open gripper | None beyond a good model | Low — any small error jams or misses | Fast | Only safe with very accurate calibration; brittle |
| **Compliant insertion (passive)** | A springy/compliant gripper or wrist lets the vial self-centre on the slot taper as it descends | Compliant tool or remote-centre compliance | Medium-high | Fast | Cheap, simple, very effective for tapered slots; v1 favourite |
| **Search pattern** | If the vial stops high, do a small spiral/raster wiggle until it drops in | Position sensing (encoders) + descent check | High | Medium | Robust without force sensing; a few extra seconds |
| **Force-compliant insertion** | A force/torque sensor lets the arm "feel" contact and back off, guiding the vial down with controlled force | Force/torque sensor | High | Medium | Best for tight tolerances; adds cost and tuning |

**Recommended for v1:** passive **compliant insertion** with a
short **search** fallback. The vial self-centres on the slot's
tapered mouth; if it hangs up, a small spiral search finds the
hole. This gets most of the robustness of force control without a
force/torque sensor.

**Seating verification** — confirm the vial actually went all the
way down, every time:

- **Position check** — the gripper reaches the expected release
  height; a vial sitting proud (too high) means it is not seated.
- **Vision check** — a camera confirms the slot is now occupied
  and the vial top is flush with the tray (see
  `07-perception-and-verification.md`).

**Worklist → slot mapping** — the orchestrator keeps an explicit
table: worklist row N → physical slot (A1, A2, …). For v1 we fill
**sequentially** (row 1 → A1, row 2 → A2, …), which makes the map
trivial and easy to audit. The identity registry that ties a
specific vial ID to its slot lives in
`06-identification-labeling-and-tracking.md`.

## v1 vs later

**v1 (keep it simple):**

- **One tray format** at **one fixed, known location** on the
  bench.
- One vial type, one recipe, **known fixed slot positions** from
  teaching or a single fiducial.
- **Sequential fill** (row order = slot order), geometric /
  known-pose placement first.
- Passive compliant insertion + small search; position- and
  vision-based seating check.
- A human supervises and can intervene on any flagged failure.

**Defer to later:**

- **Multiple tray formats** (48 vs 54 vs 100 vs well-plate),
  selected and re-calibrated automatically.
- **Tray exchange** — swapping a full tray for an empty one.
- **Auto-stacking / restocking** of trays from a magazine.
- **Non-sequential fill** (placing into arbitrary slots to match a
  pre-existing worklist).
- Force/torque-guided insertion for the tightest high-density
  trays.

## How it connects

- `02-vial-handling-and-gripping.md` — how the arm grips and
  carries the vial to the tray; the placement here is the end of
  that carry.
- `06-identification-labeling-and-tracking.md` — defines which
  sample (vial ID) belongs in which slot; we just realise that
  mapping physically.
- `07-perception-and-verification.md` — provides slot-occupancy
  sensing and the seating verification that confirms a good place.
- `08-orchestration-error-handling-and-safety.md` — handles
  placement failures (jam, missed slot, tipped neighbour): retry,
  re-search, or quarantine and alert.
- Back to the overview: `README.md`.
