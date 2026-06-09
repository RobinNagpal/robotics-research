# Ketchup Experiment — Objects to Add to the Simulation Scene

> **Job:** List the **30 objects** that must exist inside the Gazebo
> twin so the myCobot 280 can run the **tomato ketchup → 5-HMF** prep
> loop end to end, in software alone, before a cent is spent on
> hardware.

This file is the scene-building checklist for the ketchup use case. It
turns the prose of the
[sample-prep primer](../../../02-lab-bench-new.md) (Worked Example B,
ketchup) and the
[digital-twin layer](../01-simulation-and-digital-twin.md) (the six prep
steps and their `mock_*` stations) into a concrete bill of materials for
the simulated workcell.

**Why ketchup, not paracetamol.** Ketchup is the *messy* case: a thick,
pulpy, sugary matrix that must be **extracted, spun clear, and filtered**
before a drop can enter a vial. That extra clarifying detour is exactly
why the scene needs a centrifuge tube, a `mock_centrifuge`, and a heated
mixer that paracetamol could skip. Building the harder case first means
the cleaner one falls out for free.

**The prep loop these objects serve** (from the primer, Example B):

```
weigh ketchup -> extract (solvent + heat + stir) -> clarify
(centrifuge + filter) -> dilute (1:10..1:100) -> filter into vial
-> cap -> label -> place in autosampler
```

**Conventions for this list.**

- Every object is something the twin must **spawn, pose, and (often)
  attach a mock-station node to**. The twin models the *manipulation and
  choreography*, never the chemistry — so "ketchup" is a viscous body to
  pick, pour, and not spill, not a real 5-HMF reaction.
- Mock stations reuse the **exact ROS 2 topic names** from the
  [digital-twin layer](../01-simulation-and-digital-twin.md)
  (`/mock_dispenser/volume_ml`, `/mock_centrifuge/run`,
  `/mock_filter/pressure`, …) so what the twin proves, the bench
  inherits unchanged.
- **Cost/spec figures are approximate** (`~`) and should be re-checked
  before being quoted — vial volumes, tray counts, and torque bands are
  illustrative.

---

## A. Robot & workcell fixtures (objects 1–6)

The arm and the static furniture everything else is posed against. These
are loaded once and rarely move.

| # | Object | What it models in the twin | Why the ketchup loop needs it |
|---|---|---|---|
| 1 | **myCobot 280 arm** (URDF from `mycobot_ros`) | The 6-DOF arm itself — links, joints, joint limits | The actor; performs every reach, pour, and place in the loop |
| 2 | **Parallel-jaw gripper / end-effector** | The fingers that grip vessels, the pipette, and vials | Ketchup prep is all grip-and-carry; the smooth 2 mL vial is the delicate grasp |
| 3 | **Workbench tabletop** | The fixed work surface (a static collision plane) | Defines the world frame every station and rack is posed against |
| 4 | **Overhead RGB-D camera** | A depth camera looking down on the cell | Locates beakers, racks, and vials for the perception layer above |
| 5 | **Wrist-mounted camera** | A close-range camera on the gripper | Fine alignment over the narrow vial mouth and barcode reads |
| 6 | **AprilTag fiducial markers** | Printed-tag bodies on bench, racks, and stations | Give the twin known, calibratable poses — the cheap "known-pose" anchor v1 relies on |

**Bottom line:** items 1–2 are the robot; 3–6 are the fixed reference
frame and eyes that let known-pose manipulation work without learned
vision.

---

## B. Sample source & weighing (objects 7–9)

Where the raw ketchup enters the cell and is measured out — the start of
the loop.

| # | Object | What it models in the twin | Why the ketchup loop needs it |
|---|---|---|---|
| 7 | **Ketchup stock container** (jar/squeeze bottle) | A vessel holding the raw, viscous sample body | The source the arm draws the ~5 g sample from — the thing under test |
| 8 | **Weigh boat / weighing dish** | A small disposable dish the sample is dosed into | Holds the weighed ketchup before it goes to the extraction beaker |
| 9 | **`mock_balance` (analytical balance)** | A mock weighing station that publishes a settled mass | Proves the weigh-out choreography (place dish, dose, read flag) without modelling real mg metrology |

**Bottom line:** the twin fakes the milligram physics; what it proves is
the arm placing, dosing, and reading the balance in the right order.

---

## C. Prep glassware & solvents (objects 10–17)

The larger glassware the messy work happens in, plus the solvents and the
liquid-handling tool. Prep never happens in the HPLC vial — it happens
here.

| # | Object | What it models in the twin | Why the ketchup loop needs it |
|---|---|---|---|
| 10 | **Extraction beaker** | The prep vessel for solvent + ketchup + heat | Where extraction (step 2) happens; the arm carries it to the mixer |
| 11 | **Centrifuge tube** | A capped tube that goes into the spinner | Ketchup-only clarify step — holds the pulpy extract for `mock_centrifuge` |
| 12 | **Volumetric flask** | The graduated vessel for accurate dilution | Where the 1:10–1:100 dilution (step 4) is made up to the mark |
| 13 | **Solvent reservoir — water / dilute acid (extraction)** | A bottle of the extraction solvent | `mock_dispenser` draws from it to pull 5-HMF out of the matrix |
| 14 | **Solvent reservoir — diluent** | A bottle of the top-up solvent for dilution | Supplies the "make up to volume" liquid for each dilution stage |
| 15 | **Manual pipette** (arm-gripped tool) | The liquid-handling tool the gripper picks up and operates | The POC's deliberate "arm drives a manual pipette" choice for aliquots |
| 16 | **Pipette-tip rack** | A tray of disposable tips | Source of a fresh tip per transfer — avoids cross-contamination between batches |
| 17 | **Stir rod / stir bar** | The stirring element in the mixer/beaker | Part of the mix-and-extract motion the twin sequences |

**Bottom line:** this is the "back half" glassware the primer says the
arm actually handles — transfers, dilutions, and pours, not mg dispensing.

---

## D. Mock processing stations (objects 18–24)

Each physical device is stood in for by a **mock station node** that
publishes the same ROS 2 topics its real counterpart would. These are the
stations the
[digital-twin layer](../01-simulation-and-digital-twin.md) names directly.

| # | Object | Mock node / topic it carries | Why the ketchup loop needs it |
|---|---|---|---|
| 18 | **Dispenser station** | `mock_dispenser` → `/mock_dispenser/volume_ml` | Pours the measured extraction solvent into the beaker (step 1, dissolution) |
| 19 | **Heated mixer / sonicator** | `mock_mixer` → `/mock_mixer/run`, `/mock_mixer/heat`, `/prep/dissolved` | Ketchup needs **heat=on** and a **long dwell** — the warm-extraction branch |
| 20 | **Centrifuge** | `mock_centrifuge` → `/mock_centrifuge/run` | The ketchup-only spin-down that drops the pulp before filtering (step 3) |
| 21 | **Syringe + syringe filter** | The consumable `mock_filter` acts on | The force-controlled push that strains particles before the vial |
| 22 | **Filter station** | `mock_filter` → `/mock_filter/push`, `/mock_filter/pressure` | Publishes rising back-pressure so the twin can prove clog-handling and filter swaps |
| 23 | **Capper station** | `mock_capper` → `/mock_capper/screw`, `/capper/torque` | Screws the cap to a torque inside the seal-don't-crack band (step 5) |
| 24 | **Label printer** | `mock_printer` → `/mock_printer/apply`, `/traceability/log` | Prints + applies the barcode and logs the unique Sample ID (step 6) |

**Bottom line:** because each station's topic names match the hardware
mode, the whole ketchup loop built against these mocks transfers to a
real bench without a rewrite.

---

## E. Vials, caps & racks (objects 25–28)

The injection-ready containers and the staging furniture that keeps the
many ketchup vials straight.

| # | Object | What it models in the twin | Why the ketchup loop needs it |
|---|---|---|---|
| 25 | **2 mL HPLC vials** | The narrow-mouth final containers (`mock_vial` → `/vial/fill_ml`, `/vial/spill`) | The millimetre-scale pour target — the single clearest test of arm accuracy |
| 26 | **Vial caps + septa** | The screw caps the capper seats | The thing capping torques onto; the needle later pierces the septum |
| 27 | **Vial rack / nest** | A staging block of vial slots | Holds empty and filled vials at known poses between pour, cap, and label |
| 28 | **Prep-vessel rack** | A rack holding beakers / tubes / flasks | Keeps the prep glassware at repeatable poses so known-pose grasps work |

**Bottom line:** ketchup's many supplier/batch/replicate vials make the
racks (and their fixed slot poses) essential bookkeeping, not decoration.

---

## F. Output & housekeeping (objects 29–30)

Where finished vials go and where waste lands.

| # | Object | What it models in the twin | Why the ketchup loop needs it |
|---|---|---|---|
| 29 | **Autosampler tray / carousel** | The final destination with known slot positions (~96–120 slots) | The "place vial into a known position" end of the loop — well-defined fixed targets |
| 30 | **Waste container** | A bin for spent tips, clogged filters, decant liquid | Receives the swapped filters and used tips the messy ketchup run generates |

**Bottom line:** these two close the loop — a vial leaves prep, lands in a
known tray slot, and the consumables the food matrix burns through have
somewhere to go.

---

## Object count at a glance

| Group | Objects | Count |
|---|---|---|
| A. Robot & workcell fixtures | 1–6 | 6 |
| B. Sample source & weighing | 7–9 | 3 |
| C. Prep glassware & solvents | 10–17 | 8 |
| D. Mock processing stations | 18–24 | 7 |
| E. Vials, caps & racks | 25–28 | 4 |
| F. Output & housekeeping | 29–30 | 2 |
| **Total** | | **30** |

---

## Notes on building these in Gazebo

- **Start with the fixtures (A) and one of each vessel.** The arm, table,
  cameras, and AprilTags define the world frame; everything else is posed
  against it. Get one beaker, one vial, and one rack placed before
  multiplying counts.
- **Multiply only where ketchup demands it.** The realistic ketchup run
  is ~8–12 vials (several batches × 2–3 replicates + a 5-HMF standard +
  a blank). Spawn the vials and tip rack as *arrays* parameterised by the
  worklist, not as 12 hand-placed bodies.
- **Mock stations are nodes, not just meshes.** Objects 18–24 each need a
  visual body **and** a small ROS 2 node publishing the topics listed
  above. A station with no node is just scenery the loop can't gate on.
- **Viscosity is faked.** Gazebo will not model true ketchup rheology;
  represent the sample as a simple body (or a fill level on `/vial/...`)
  and let the *manipulation* — grip, carry, pour-without-spill — be the
  thing under test.
- **Keep v1 known-pose.** Per the project framing, rely on AprilTags and
  fixed rack slots first; defer learned 6-DoF pose estimation to a later
  milestone.

## See also

- [`../01-simulation-and-digital-twin.md`](../01-simulation-and-digital-twin.md)
  — the six prep-step use cases and every `mock_*` station these objects host.
- [`../../../02-lab-bench-new.md`](../../../02-lab-bench-new.md) — the
  sample-prep primer; Worked Example B is the ketchup workflow above.
- [`../../../03-hplc-workflow/README.md`](../../../03-hplc-workflow/README.md)
  — the eight prep steps in beginner detail.
