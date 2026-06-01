# Part 06 — Identification, labeling & tracking (AgileX PiPER simulation)

> **Sim goal:** Prove, in open-source simulation, that every vial
> keeps a verified identity from supply to tray slot — by either
> decoding a *real* barcode rendered on the vial with a simulated
> camera, or carrying a virtual ID per vial, then reconciling
> vial-ID → slot → worklist-row → LIMS sample-ID in a registry that
> raises a quarantine event on any mismatch.

A **barcode** is a printed pattern (1-D stripes like Code128, or a
2-D **QR** square) that encodes a short ID string. **LIMS** is the
Laboratory Information Management System — the lab's database of
samples and their sample-IDs. **Quarantine** here means: stop, flag
the vial, and do not let it reach the tray until a human resolves
it. New to a term? See
`../../03-place-items-on-shelf/02-glossary.md`.

## What we can prove in simulation

Identity is mostly a *software and data* problem, so almost all of
it lives in sim:

- **The decode pipeline** — that a camera image of a barcode is
  correctly turned into an ID string by the same OpenCV + pyzbar
  code the real system would run. This is the genuinely transferable
  proof: the decoder does not know it is looking at a simulated
  image.
- **The registry / tracking logic** — a single source of truth
  mapping **vial-ID → tray-slot → worklist-row → LIMS sample-ID**,
  kept consistent as vials move.
- **Reconciliation against the worklist** — confirming the scanned
  vial is the one the worklist expects for the next slot.
- **Mismatch handling** — that a deliberate mix-up actually fires a
  **quarantine** event rather than silently loading the wrong vial.
- **The audit trail** — every scan and mapping change recorded for
  later (Part 09).

**Honest limits (need hardware):** real-world **read rate** — how
often a real scanner reads a real label under real lighting, on
curved glass, with glare, smudges, or condensation. Sim can render
a clean or even a degraded texture, but it cannot reproduce a real
optical scanner's failure modes. Label **printing/application**
quality is likewise a hardware question.

## Open-source tools

| Tool | Role | Bottom line |
|------|------|-------------|
| **OpenCV** | Grabs/preprocesses the simulated camera image (crop, threshold) | Standard CV front-end to the decoder |
| **ZBar / pyzbar** | Decodes 1-D/2-D barcodes from the image into an ID string | The decode step that transfers 1:1 to hardware |
| **Gazebo camera sensor** | The simulated "scanner" that views the vial's barcode texture | Stands in for the real fixed/handheld scanner |
| **A barcode-image generator** (e.g. `python-barcode`, `qrcode`) | Bakes a real Code128/QR image to use as a vial texture | Makes textures the *real* decoder can read |
| **`/scan` mock service node** | Alternative path: returns the virtual ID of the vial in view | Simplest identity path; no rendering needed |
| **SQLite** | Stores the registry + scan log | Lightweight, file-based audit store |
| **BehaviorTree.CPP / py_trees** | Triggers scan, reconcile, and quarantine steps in the sequence | Wires identity into orchestration |

## How to simulate it now

Pick *one* of two identity paths (or run both to compare):

**Path (a) — real decode (proves the pipeline).**

1. **Generate barcode images.** For each vial-ID, generate a real
   **QR or Code128** PNG with a barcode library.
2. **Texture the vial model.** Apply that PNG as a texture (decal)
   on the side of each spawned vial in Gazebo, so the label is
   physically present in the scene.
3. **Add a sim scanner camera.** Place a Gazebo camera sensor at a
   fixed **scan station** tf frame (`scan_station`) the arm presents
   each vial to, or a wrist camera that looks at the label.
4. **Decode.** A `barcode_decoder` node subscribes to the camera
   image, runs **OpenCV → pyzbar**, and publishes the decoded ID.
   This is the exact code the real arm would use.

**Path (b) — virtual ID (simplest).**

1. Each spawned vial carries an **ID property** (set at spawn time).
2. A **`/scan` mock-station service** node, when called with the
   vial currently at `scan_station`, simply returns that ID. No
   rendering or CV — useful when you only want to test the tracking
   logic, not the optics.

**Then, for either path:**

5. **Populate the registry (SQLite).** A `registry` node maintains
   the table **vial-ID → tray-slot → worklist-row → LIMS sample-ID**.
   When Part 05 seats a vial in slot A1, the registry binds that
   vial-ID to A1 and to the worklist row that requested it.
6. **Reconcile against the worklist.** Before placing, compare the
   scanned ID with the ID the worklist expects for the next slot.
7. **Test a deliberate mix-up.** Spawn a vial whose ID does *not*
   match the next worklist row, scan it, and confirm the registry
   raises a **mismatch/quarantine** event (a topic Part 08 watches)
   — the vial is held, not loaded, and the event is logged.

**Key tf frames:** `scan_station`, `gripper_tip`, `tray/Ax` (from
Part 05). **Mock interfaces:** `/scan` service (Path b) or the
`barcode_decoder` topic (Path a); a `quarantine_event` topic; the
SQLite-backed `registry` node.

## Additional hardware needed

Beyond the **PiPER arm + gripper**, the real system needs:

| Real hardware | Why | Mocked in sim as |
|---------------|-----|------------------|
| **Barcode/QR scanner** (fixed or wrist) | Reads the real label to confirm identity | Gazebo camera + OpenCV/pyzbar, or `/scan` mock service |
| **Label printer / applicator** (optional) | Prints and sticks a label if vials arrive unlabelled | Skipped in sim — vials spawn pre-textured or pre-IDed |
| **Scan-station lighting / fixture** | Consistent reads on curved glass | Fixed camera pose + clean rendered texture |

Real **read rate and label quality** are the items to validate on
the bench — sim proves the decode *logic*, not optical reliability.

## How it connects

- `04-liquid-handling-and-sample-prep.md` — the sample-ID drives
  *which recipe* a vial gets; identity must be fixed before prep.
- `05-tray-loading-and-positioning.md` — supplies the vial→slot
  binding this registry records and reconciles.
- `08-orchestration-error-handling-and-safety.md` — consumes the
  mismatch/quarantine event and decides the recovery action.
- `09-software-compliance-and-integration.md` — owns the worklist,
  the LIMS link, and the audit trail / data-integrity guarantees
  this registry feeds.
- Matching high-level doc:
  `../01-high-level-solution/06-identification-labeling-and-tracking.md`.
- Back to the overview: `README.md`.
