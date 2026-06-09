# Ketchup Experiment — Objects to Add to the Simulation Scene

> **Job:** List the objects the Gazebo twin must spawn so the myCobot
> 280 can run the **tomato ketchup → 5-HMF** prep loop end to end, in
> software alone — organised by the **six prep-workflow stages** so the
> scene can be built one stage at a time.

This file is the scene-building checklist for the ketchup use case. It
takes the prose of the
[sample-prep primer](../../02-lab-bench-new.md) (Worked Example B,
ketchup) and the
[digital-twin layer](../01-simulation-and-digital-twin.md) and turns it
into a concrete bill of materials, **grouped by workflow stage**.

Each stage below links to its full plain-language walkthrough in the
[`03-hplc-workflow/`](../../03-hplc-workflow/README.md) folder — open
that file to understand *why* the stage exists and what each object does.

**Why ketchup, not paracetamol.** Ketchup is the *messy* case: a thick,
pulpy, sugary matrix that must be **extracted, spun clear, and filtered**
before a drop can enter a vial. Building the harder case first means the
cleaner paracetamol case mostly falls out for free.

**The prep loop these objects serve** (from the primer, Example B):

```
weigh ketchup -> 1) dissolution/extraction -> 2) dilution
-> 3) filtering -> 4) transfer to vial -> 5) capping -> 6) labeling
-> place in autosampler
```

**Conventions for this list.**

- Every object is something the twin must **spawn, pose, and (often)
  attach a mock-station node to**. The twin models the *manipulation and
  choreography*, never the chemistry — "ketchup" is a viscous body to
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

## Shared workcell — used in every stage (objects 1–10)

Load these once. They are the arm, the fixed furniture, the eyes, and the
racks that every stage below poses its objects against.

| # | Object | What it models in the twin | Why every stage needs it |
|---|---|---|---|
| 1 | **myCobot 280 arm** (URDF from `mycobot_ros`) | The 6-DOF arm — links, joints, joint limits | The actor; performs every reach, pour, and place |
| 2 | **Parallel-jaw gripper** | The fingers that grip vessels, the pipette, and vials | Every stage is grip-and-carry; the smooth 2 mL vial is the delicate grasp |
| 3 | **Workbench tabletop** | The fixed work surface (a static collision plane) | Defines the world frame everything else is posed against |
| 4 | **Overhead RGB-D camera** | A depth camera looking down on the cell | Locates beakers, racks, and vials for the perception layer |
| 5 | **Wrist-mounted camera** | A close-range camera on the gripper | Fine alignment over the narrow vial mouth and barcode reads |
| 6 | **Scene lighting + matte backdrop** | An LED panel and plain backdrop, varied run-to-run (domain randomization) | Gives the cameras clean, varied frames so the **YOLO** detector trains on synthetic data and runs reliably |
| 7 | **Prep-vessel rack** | A rack holding beakers / tubes / flasks | Keeps prep glassware at repeatable poses so YOLO-located grasps are reliable |
| 8 | **Vial rack / nest** | A staging block of 2 mL vial slots | Holds empty and filled vials at known poses between stages |
| 9 | **Autosampler tray / carousel** | The final destination, known slots (~96–120) | Where a finished vial is placed — the loop's exit |
| 10 | **Waste container** | A bin for spent tips, clogged filters, decant liquid | Receives the consumables the messy ketchup run burns through |

**Bottom line:** items 1–2 are the robot; 3–10 are the fixed reference
frame, eyes, staging, and lighting that let the **YOLO** detector and
fixed rack/tray geometry place every object reliably.

---

## Stage 1 — Dissolution / extraction (objects 11–15)

> **In plain words:** get the sample (or just the part we care about)
> into a liquid.
> **Full walkthrough:**
> [`03-hplc-workflow/02-dissolution-and-extraction.md`](../../03-hplc-workflow/02-dissolution-and-extraction.md)

Ketchup will not politely dissolve, so we **extract**: add solvent, stir,
and warm gently to pull the 5-HMF out of the pulp. The result is a cloudy,
pulpy liquid (cleared later, in Stage 3).

| # | Object | What it models in the twin | Why this stage needs it |
|---|---|---|---|
| 11 | **Ketchup stock container** (jar/squeeze bottle) | A vessel holding the raw, viscous sample body | The source the arm draws the ~5 g sample from — the thing under test |
| 12 | **Extraction beaker** | The roomy prep vessel for solvent + ketchup + heat | Where extraction happens; the arm carries it to the mixer |
| 13 | **Solvent reservoir — water / dilute acid** | A bottle of the extraction solvent | `mock_dispenser` draws from it to coax 5-HMF out of the matrix |
| 14 | **Dispenser station** — `mock_dispenser` → `/mock_dispenser/volume_ml` | A mock that "pours" a measured solvent volume | Adds the measured extraction solvent to the beaker |
| 15 | **Heated mixer / sonicator** — `mock_mixer` → `/mock_mixer/run`, `/mock_mixer/heat`, `/prep/dissolved` | A mock stir-and-heat station that raises a "done" flag | Ketchup needs **heat=on** and a **long dwell** — the warm-extraction branch |

**Bottom line:** this is where ketchup first looks harder than a tablet —
heat, a long dwell, and a cloudy result that still needs clearing.

---

## Stage 2 — Dilution (objects 16–20)

> **In plain words:** make that liquid weaker so the machine can read it.
> **Full walkthrough:**
> [`03-hplc-workflow/03-dilution.md`](../../03-hplc-workflow/03-dilution.md)

The extract's 5-HMF level is unknown, so it is diluted hard (1:10–1:100),
often in two gentle stages. The difficulty lives in the **tool** (a
precise pipette/handler), not the arm's muscles.

| # | Object | What it models in the twin | Why this stage needs it |
|---|---|---|---|
| 16 | **Volumetric flask** | The graduated vessel diluted "up to the mark" | Where the 1:10–1:100 dilution is made up to a known volume |
| 17 | **Solvent reservoir — diluent** | A bottle of the top-up solvent | Supplies the "make up to volume" liquid for each dilution stage |
| 18 | **Manual pipette** (arm-gripped tool) | The precise liquid-handling tool the gripper operates | The POC's deliberate "arm drives a manual pipette" choice for exact aliquots |
| 19 | **Pipette-tip rack** | A tray of disposable tips | A fresh tip per transfer — avoids cross-contamination between batches |
| 20 | **Liquid-handler station** — `mock_handler` → `/mock_handler/transfer`, `/prep/concentration` | A mock that performs aliquot + top-up and reports strength | Runs each ≤10× dilution stage and confirms the target concentration |

**Bottom line:** exact volumes are the whole game here; the arm's job is
precise positioning and choreography around a good pipetting tool.

---

## Stage 3 — Filtering (objects 21–25)

> **In plain words:** strain out tiny solid bits that would block the
> machine.
> **Full walkthrough:**
> [`03-hplc-workflow/04-filtering.md`](../../03-hplc-workflow/04-filtering.md)

This is where ketchup diverges most: pulp would clog a filter instantly,
so the loop **spins it clear first** (centrifuge → pour off the clear top
layer) and only then pushes it through the syringe filter.

| # | Object | What it models in the twin | Why this stage needs it |
|---|---|---|---|
| 21 | **Centrifuge tube** | A capped tube that goes into the spinner | Holds the pulpy extract for the ketchup-only clarify step |
| 22 | **Centrifuge station** — `mock_centrifuge` → `/mock_centrifuge/run` | A mock that "spins down" solids, then decant | Drops the tomato pulp to the bottom before filtering |
| 23 | **Syringe** | A plunger tube that pushes liquid through the filter | The force-controlled push the arm drives |
| 24 | **Syringe filter** | A fine membrane disc (~0.45/0.22 µm) on the syringe | Traps the last particles so nothing clogs the HPLC column |
| 25 | **Filter station** — `mock_filter` → `/mock_filter/push`, `/mock_filter/pressure` | A mock that reports rising back-pressure | Lets the twin prove clog-handling: push, watch pressure, swap on a spike |

**Bottom line:** ketchup's **spin → pour off → filter** detour is the
extra work the food matrix forces; paracetamol needs only the filter.

---

## Stage 4 — Transfer to vial (objects 26)

> **In plain words:** move the finished liquid into the little glass
> bottle.
> **Full walkthrough:**
> [`03-hplc-workflow/05-transfer-to-vial.md`](../../03-hplc-workflow/05-transfer-to-vial.md)

The project-defining motion: aim over the **narrow 2 mL vial mouth** and
pour without spilling. By now the liquid is thin and clear, so the pour
matches paracetamol — ketchup just has more vials to track.

| # | Object | What it models in the twin | Why this stage needs it |
|---|---|---|---|
| 26 | **2 mL HPLC vials** — `mock_vial` → `/vial/fill_ml`, `/vial/spill` | The narrow-mouth final containers, with fill + spill feedback | The millimetre-scale pour target — the clearest single test of arm accuracy |

**Bottom line:** *can the arm hit the vial mouth reliably, every time?*
is the one question this stage exists to answer.

---

## Stage 5 — Capping (objects 27–28)

> **In plain words:** close the bottle with a lid (and a pierceable seal).
> **Full walkthrough:**
> [`03-hplc-workflow/06-capping.md`](../../03-hplc-workflow/06-capping.md)

Identical for ketchup and paracetamol: place the cap squarely and screw
to a torque that is firm enough to seal but gentle enough not to crack the
glass.

| # | Object | What it models in the twin | Why this stage needs it |
|---|---|---|---|
| 27 | **Vial caps + septa** | The screw caps (with pierceable septa) the capper seats | What capping torques onto; the needle later pierces the septum |
| 28 | **Capper station** — `mock_capper` → `/mock_capper/screw`, `/capper/torque` | A mock that ramps and reports applied torque | Lets the twin stop inside the seal-don't-crack acceptance band |

**Bottom line:** a small, repeatable, judgement-free motion — exactly what
an arm is best at, the same code for both samples.

---

## Stage 6 — Labeling (objects 29–30)

> **In plain words:** write on the bottle what is inside.
> **Full walkthrough:**
> [`03-hplc-workflow/07-labeling.md`](../../03-hplc-workflow/07-labeling.md)

The motion is forgiving; the real point is **information** — every vial
gets a *unique*, logged Sample ID so a result can always be traced back.
Ketchup's many supplier/batch/replicate IDs make uniqueness the thing to
assert.

| # | Object | What it models in the twin | Why this stage needs it |
|---|---|---|---|
| 29 | **Barcode label stock** | The sticky barcode labels applied to each vial | The physical mark that carries the Sample ID |
| 30 | **Label printer** — `mock_printer` → `/mock_printer/apply`, `/traceability/log` | A mock that prints + applies a label and logs the ID | Guarantees a unique ID per vial and a perfect audit record |

**Bottom line:** automating this turns a forgiving motion into a
reliability *gain* — a robot never mismatches a label.

---

## Object count at a glance

| Stage | Objects | Count |
|---|---|---|
| Shared workcell (every stage) | 1–10 | 10 |
| 1 — Dissolution / extraction | 11–15 | 5 |
| 2 — Dilution | 16–20 | 5 |
| 3 — Filtering | 21–25 | 5 |
| 4 — Transfer to vial | 26 | 1 |
| 5 — Capping | 27–28 | 2 |
| 6 — Labeling | 29–30 | 2 |
| **Total** | | **30** |

*(Weighing the ~5 g of ketchup happens before Stage 1 and placement into
the autosampler happens after Stage 6; both reuse the shared workcell —
see [`01-weighing.md`](../../03-hplc-workflow/01-weighing.md) and
[`08-placement-in-autosampler.md`](../../03-hplc-workflow/08-placement-in-autosampler.md).)*

---

## Notes on building these in Gazebo

- **Start with the shared workcell.** The arm, table, cameras, lighting,
  and racks define the world frame; build them and one of each vessel
  before multiplying counts.
- **Then build stage by stage, in order.** Each stage section above maps
  one-to-one to a `mock_*` station and a workflow file, so the twin can
  be stood up and tested one capability at a time.
- **Multiply only where ketchup demands it.** A realistic ketchup run is
  ~8–12 vials (several batches × 2–3 replicates + a 5-HMF standard + a
  blank). Spawn vials and tips as *arrays* parameterised by the worklist,
  not as hand-placed bodies.
- **Mock stations are nodes, not just meshes.** Each station needs a
  visual body **and** a small ROS 2 node publishing the topics listed —
  a station with no node is just scenery the loop can't gate on.
- **Viscosity is faked.** Gazebo will not model true ketchup rheology;
  represent the sample as a simple body (or a fill level on `/vial/...`)
  and let the *manipulation* be the thing under test.
- **Detect with YOLO.** The cell locates vials, racks, beakers, and the
  tray with a **YOLO** detector trained on synthetic data rendered from
  this scene, then lifts each detection to 3-D using the RGB-D depth;
  fixed rack/tray geometry indexes the individual slots. Defer heavier
  learned 6-DoF pose models to a later milestone.

## See also

- [`../01-simulation-and-digital-twin.md`](../01-simulation-and-digital-twin.md)
  — the six prep-step use cases and every `mock_*` station these objects host.
- [`../../02-lab-bench-new.md`](../../02-lab-bench-new.md) — the
  sample-prep primer; Worked Example B is the ketchup workflow above.
- [`../../03-hplc-workflow/README.md`](../../03-hplc-workflow/README.md)
  — the eight prep steps in beginner detail (each now lists its own objects).
