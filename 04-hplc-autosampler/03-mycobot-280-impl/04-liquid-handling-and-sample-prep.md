# Part 04 — Liquid handling & sample prep (myCobot 280 simulation)

> **Sim goal:** Prove the *sample-prep logic* on the myCobot 280 — which
> vial gets which volume of which reagent, in what order, with washes
> between — by tracking liquid as a **number**, not by simulating any
> fluid dynamics.

## What we can prove in simulation

The real chemistry (microlitre-accurate volumes, dilution to a target
concentration, carryover) is physics and chemistry we will **not**
simulate — see the matching
[`../01-high-level-solution/04-liquid-handling-and-sample-prep.md`](../01-high-level-solution/04-liquid-handling-and-sample-prep.md).
Computational fluid dynamics (CFD — software that models how fluids
flow) is overkill and still wouldn't prove real accuracy. So we abstract
a vial's contents to a **scalar fill-volume** (a single number, e.g.
millilitres) plus a small **contents / recipe tag** (what's in it). A
mock dispenser *service* mutates that state.

**Can prove in open-source sim:**

- The **dispense choreography**: grip open vial → drive under the nozzle
  frame → call `/dispense` → state updates → move on.
- The **reachability of the dispense pose**. With the 280's
  **~280 mm working radius** (`~` figure — verify), the
  `dispense_nozzle` frame must be kept close to the arm base, clustered
  with the decapper (Part 03) and supply rack. Proving the arm can place
  an open vial mouth under the nozzle *without* over-extending is a key
  sim result that feeds the bench-layout decision (Part 10).
- The **recipe execution**: turning a worklist row ("sample S-014:
  50 µL internal standard + 950 µL diluent") into an ordered list of
  `/dispense` calls and confirming the resulting fill-volume / tag match.
- The **wash / carryover *policy*** as logic and timing: a wash step is
  modelled as a state change ("path clean") and elapsed time, so the
  sequencer's "wash between samples" rule is exercised — *not* the
  physical cleaning.
- An optional **gravimetric check** (a weight-based volume check) as
  bookkeeping: a mock balance "reads" mass derived from the fill state
  and the sequencer compares it to the expected value.
- **Cycle-time** estimates for the prep phase that feed the ROI model
  (Part 10).

**Cannot be proven in sim (needs hardware):** real **volume accuracy and
precision**, **carryover** between samples, **bubble-free** dispensing,
**mixing/dilution** behaviour, and **volatile-solvent** effects
(evaporation, fumes). These are exactly the things the abstraction
hides; they must be validated on the real dispenser. Note the arm's
**~250 g payload** is ample for a 2 mL vial of liquid (a few grams), so
payload is not the constraint here — reach and the fluidics are.

## Open-source tools

| Tool | Role | Bottom line |
|------|------|-------------|
| **ROS 2** (Humble/Jazzy) | Carries the `/dispense` service + the per-vial fill-volume state | Same interface on real hardware. |
| **Gazebo Harmonic** (`gz-sim`) | Hosts the nozzle frame and (optional) the scaling liquid-level mesh | Primary world. |
| **`mycobot_ros`** | Ready-made myCobot 280 URDF + MoveIt config driven under the nozzle | BSD; no model-building. |
| **`gz_ros2_control`** | Drives the myCobot 280 URDF joints in sim (no `pymycobot`) | No real driver needed. |
| **MoveIt 2** | Plans the collision-free move to the dispense pose | Config from `mycobot_ros`. |
| **SQLite** | Stores the per-vial fill-volume + recipe-tag registry (audit trail) | Ties into the worklist (Part 09). |
| **BehaviorTree.CPP** (+ Groot2) | Sequences present → dispense → wash → recheck, with fault branches | Orchestration (Part 08). |
| **Open3D / OpenCV** | (Part 07) "reads" a rendered level if you visualise it | Verification, not measurement. |

## How to simulate it now

**The core abstraction.** Each vial owns a **fill-volume** (a float) and
a **contents/recipe tag** (e.g. `{"diluent": 0.95, "istd": 0.05}`). A
`/dispense` call adds to the volume and merges the tag. No droplets, no
flow, no CFD.

1. **Build a per-vial state registry.** A ROS 2 node (backed by SQLite)
   holds `{vial_id -> {fill_volume, contents_tag, last_path_clean}}`.
   It publishes each vial's state on a latched topic so perception
   (Part 07) and orchestration (Part 08) can read it.

2. **Write the mock dispenser node.** Advertise `/dispense` with a small
   custom service: `{vial_id, volume, reagent} -> {success,
   new_volume}`. On call it (a) checks the vial is *open* (`cap_present`
   is false — see Part 03), (b) adds `volume` to that vial's
   fill-volume, (c) merges `reagent` into the contents tag, (d) marks
   the fluid path "dirty" for the wash logic, and (e) returns the new
   volume. Reject or flag overflow past the vial's nominal capacity.

3. **Expose the nozzle tf frame — close to the arm.** Publish a static
   transform `dispense_nozzle`, placed deliberately near the arm base so
   it stays inside the short 280 workspace. The arm plans a **dispense
   pose** placing the open vial mouth under that frame; sanity-check
   reachability in RViz2.

4. **(Optional) visualise the level.** Add a thin **cylinder mesh**
   inside the vial whose vertical scale is set from the fill-volume
   (driven by a tiny node that subscribes to the state topic). This is
   purely cosmetic — and gives Part 07 something to "read."

5. **Model wash as state + time.** A `/wash` service marks the path
   "clean" after a configurable delay. The behavior tree's rule is
   "wash between samples"; in sim that's a state transition and a timer,
   not real cleaning.

6. **(Optional) mock balance.** A `/weigh {vial_id} -> {mass}` service
   computes mass from the fill-volume (× an assumed density) and returns
   it, so a **gravimetric check** branch can be exercised: dispense →
   weigh → compare to expected → pass/flag.

7. **Drive the full sequence.** With the vial gripped (Part 02) and open
   (Part 03): for each recipe line, `MoveToPose` → `dispense_nozzle` →
   call `/dispense` → optionally `/weigh` → on the last line, optionally
   `/wash` → hand back for recapping. Part 07 then "reads" the level
   (from state or the rendered cylinder) to confirm the fill before
   proceeding.

## Additional hardware needed

Beyond the **myCobot 280 + gripper**, the real bench needs the actual
fluidics:

- a **syringe pump**, **bottle-top** or **peristaltic dispenser**, or an
  **OEM pipetting head** (sized to the method's µL–mL range);
- **disposable tips** (fresh tip per sample) and/or a **wash station**
  to control carryover;
- an optional **analytical balance** for the gravimetric check.

Because the 280 cannot carry a heavy pipetting tool on a changer, the
recommended pattern is **fixed dispensing stations the arm presents
vials to** — keeping the fluidics off the arm and clustered tightly
within the compact workspace.

**How it's mocked in sim:** every one of the above is a **service stub +
state**. The pump/pipettor is the `/dispense` service; tips and wash are
the `/wash` state/time model; the balance is the `/weigh` service
reading the simulated fill. **No real volume accuracy, carryover,
mixing, or evaporation is represented** — those are deferred to hardware
validation.

## How it connects

- [`02-vial-handling-and-gripping.md`](02-vial-handling-and-gripping.md)
  & [`03-decapping-and-capping.md`](03-decapping-and-capping.md) — the
  vial must be **held** and **open** (cap detached) before `/dispense`
  will act on it.
- [`06-identification-labeling-and-tracking.md`](06-identification-labeling-and-tracking.md)
  — tells the dispenser *which recipe* applies to each `vial_id`.
- [`07-perception-and-verification.md`](07-perception-and-verification.md)
  — "reads" the fill level (from state or the rendered cylinder) to
  verify the dispense before recapping.
- [`09-software-compliance-and-integration.md`](09-software-compliance-and-integration.md)
  — the **worklist** is the source of the volumes/reagents each
  `/dispense` uses, and the SQLite registry is the audit trail.
- Matching high-level note:
  [`../01-high-level-solution/04-liquid-handling-and-sample-prep.md`](../01-high-level-solution/04-liquid-handling-and-sample-prep.md).
- Back to the index: [`README.md`](README.md).
