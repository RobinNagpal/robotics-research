# Part 06 — Identification, labeling & tracking (simulation)

> **Sim goal:** Prove the whole identity chain in software — give
> each simulated vial a unique ID, **read** it (via a real
> barcode-decode pipeline or a mock scan service), build the
> registry that ties vial → slot → worklist → LIMS, and show that a
> deliberate **mix-up** is caught and quarantined — all before a real
> scanner exists.

This mirrors the high-level
[`../03-high-level-solution/06-identification-labeling-and-tracking.md`](../03-high-level-solution/06-identification-labeling-and-tracking.md).
New robotics terms are defined in
[`../../03-place-items-on-shelf/02-glossary.md`](../../03-place-items-on-shelf/02-glossary.md).

## What we can prove in simulation

In a regulated lab the unbroken record of "which sample is where, at
every step" is the **chain of custody**, and the worst failure is a
**sample mix-up** — good data attributed to the wrong sample. The
defence is three things working together: a unique **ID** on every
vial, a reliable way to **read** it, and a **software registry** that
**reconciles** physical reading against the expected worklist.

All three are mostly *software*, so simulation proves a lot:

**Can prove fully in open-source sim:**

- **The vision/decode pipeline.** Render a real **1D barcode**
  (stripes, e.g. Code128) or **2D barcode** (a grid of dots, e.g. QR
  or Data Matrix) as a texture on the vial, point a simulated camera
  at it, and **decode it with OpenCV + pyzbar** — the exact same code
  that will run on hardware images.
- **The registry and reconciliation logic** — the table mapping
  vial ID → slot → worklist row → LIMS sample ID, and the checks that
  fire at intake, at placement, and before hand-off.
- **The mix-up / quarantine path** — inject a wrong vial or a
  duplicate ID and confirm the system **stops, flags, and
  quarantines** rather than guessing.
- **End-to-end traceability** — that every step writes to the audit
  trail (Part 09) so the chain of custody is unbroken in the records.

**Honest limits (need real hardware to settle):**

- **Real scanner read-rate.** Whether a real scanner reliably reads a
  small, curved, possibly glare-hit label on a 2 mL vial is a
  physical question. Sim decodes a clean rendered texture, so it
  proves the *logic* and *software* but **inflates** read success.
- **Print/label quality and adhesion** (if printing is ever added)
  are real-world failure modes sim does not model.

So sim proves the **decode pipeline, the registry, reconciliation,
and the quarantine path**; the real-world **read-rate** is a hardware
number.

## Open-source tools

| Tool | Role | Bottom line |
|------|------|-------------|
| **OpenCV** | Generate barcode/QR textures; grab and pre-process simulated camera frames | The image plumbing for the decode path |
| **ZBar / pyzbar** | Decode 1D/2D barcodes from those frames | The actual reader; identical code on hardware |
| **Gazebo Harmonic** | Hosts vials carrying barcode textures and a simulated **scanner camera** sensor | Where the rendered-and-decode loop runs |
| **`/scan` mock service** (ROS 2) | The simpler "virtual ID" path — returns the ID attached to a spawned vial | Lets you skip vision while building the registry |
| **SQLite** | Stores the registry table + audit trail | Durable, file-based system of record |
| **FastAPI** | Mock **LIMS/CDS** service that owns sample IDs and the worklist | Stands in for the lab system of record |
| **RViz2 / Foxglove** | Inspect the camera image and the decoded result | Eyeball that the right ID came back |

## How to simulate it now

There are **two ways** to give a simulated vial an identity; build
the registry the same way regardless of which you pick.

**Path A — real decode pipeline (proves the vision path).**

1. For each vial, **generate a barcode image** (QR / Data Matrix /
   Code128) encoding its ID with OpenCV (or `python-barcode`/`qrcode`)
   and apply it as a **texture** on the vial model.
2. Add a **simulated scanner camera** in Gazebo at a fixed `scanner`
   tf frame (a "read station"). The arm presents the vial to it —
   reusing the camera modelling from
   [`07-perception-and-verification.md`](07-perception-and-verification.md).
3. A `barcode_reader` node subscribes to the camera image, runs
   **pyzbar** decode, and publishes the decoded ID (or "unreadable").

**Path B — virtual ID (simpler, skips vision).**

- Each spawned vial carries an **ID property**. A `/scan` mock-station
  **service** at the `scanner` frame returns that ID when the arm
  presents a vial. Use this to develop the registry fast, then swap in
  Path A to validate the real decode.

**Build the registry node.**

- A `registry` node maintains the mapping
  `vial ID → tray slot (A1…) → worklist row → LIMS sample ID` in
  **SQLite**, sourcing the worklist/sample IDs from the **FastAPI**
  mock LIMS.
- **Reconcile** at each step:
  - **Intake** — decoded ID must match a sample known to the
    worklist; unknown → reject.
  - **Placement** — the ID just placed (from Part 05) must equal the
    ID the registry expects for that slot.
  - **Pre-hand-off** — re-read every occupied slot and match each to
    its worklist row.

**Test the deliberate mix-up.**

- Spawn a vial whose ID does **not** match the slot the worklist
  expects (or a **duplicate** ID), run the loop, and assert that
  reconciliation **raises a mismatch event** and the
  **quarantine path fires** — the vial is set aside, flagged, and the
  position refuses to run. This is the headline test of the part.

**Workflow:** spawn IDs (texture or property) → present to scanner →
decode (pyzbar) or `/scan` → registry lookup + reconcile → on match,
proceed and log; on mismatch, raise event → Part 08 quarantines.

## Additional hardware needed

| Real hardware | Why | How mocked in sim |
|---------------|-----|-------------------|
| **Barcode scanner** (fixed reader or camera) | Reads the unique ID off each real vial | A simulated **camera + ZBar/pyzbar**, or a **`/scan` mock service** returning a virtual ID |
| *(optional)* **Label printer / applicator** | Prints and applies a barcode to unlabelled vials (deferred — v1 uses pre-barcoded vials) | Render the barcode as a vial **texture** at spawn time; no print/apply physics |

Neither blocks the digital twin: identity is a texture or a property,
and the registry is pure software.

## How it connects

- [`04-liquid-handling-and-sample-prep.md`](04-liquid-handling-and-sample-prep.md)
  — the decoded vial ID selects which **recipe** to apply to each
  sample.
- [`05-tray-loading-and-positioning.md`](05-tray-loading-and-positioning.md)
  — consumes the vial→slot mapping defined here and realises it
  physically; reports back the slot actually used so the registry
  stays truthful.
- [`08-orchestration-error-handling-and-safety.md`](08-orchestration-error-handling-and-safety.md)
  — owns the mismatch/quarantine handling triggered by a failed
  reconciliation here.
- [`09-software-compliance-and-integration.md`](09-software-compliance-and-integration.md)
  — home of the **worklist**, the **LIMS** link, the **audit trail**,
  and the **data-integrity** rules that govern this registry.
- Mirrors
  [`../03-high-level-solution/06-identification-labeling-and-tracking.md`](../03-high-level-solution/06-identification-labeling-and-tracking.md);
  back to the overview: [`README.md`](README.md).
