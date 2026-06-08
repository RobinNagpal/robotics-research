# Part 06 — Identification, labeling & tracking (myCobot 280 simulation)

> **Sim goal:** Prove that every vial the **myCobot 280** handles
> carries a known **identity**, that we can read that identity, and
> that we keep an exact, auditable chain of *which vial → which tray
> slot → which worklist row → which LIMS sample*. We prove the real
> **barcode-decode pipeline** end to end in Gazebo, and we show that a
> deliberate mix-up is caught and quarantined — all before any
> scanner hardware exists. (**LIMS** = Laboratory Information
> Management System, the lab's system of record for samples.)

New robotics and lab terms are defined on first use in the
[sample-prep primer](../02-lab-bench-new.md) and the
[HPLC workflow](../03-hplc-workflow/README.md).

## What we can prove in simulation

There are two honest ways to give a simulated vial an identity. Build
both; they share the same downstream registry.

- **(a) Real barcode pipeline.** Render an actual 1D/2D barcode
  (Code128 or QR) as a **texture** on each vial model, point a
  **simulated camera** at it, and decode it with **OpenCV +
  pyzbar**. This exercises the *exact* software path the hardware
  scanner will use — image in, decoded string out — so the decode
  code is proven, not stubbed.
- **(b) Virtual ID (simpler).** Each spawned vial carries an **ID
  property** (set at spawn time), and a `/scan` **mock-station
  service** simply returns it. No image processing. This is the fast
  path for testing the *tracking logic* when you do not care about
  the optics.

**Can prove fully in open-source sim:**

- **The decode pipeline works** — generated barcode → sim camera →
  pyzbar → correct string, including framing, lighting, and
  resolution sensitivity you can dial in the sim camera.
- **The identity chain is consistent** — vial-ID → tray-slot →
  worklist-row → LIMS sample-ID, held in one registry and
  reconciled against the worklist.
- **Mismatch handling fires** — inject a wrong vial into a slot and
  confirm the system raises a **mismatch / quarantine** event rather
  than silently mis-recording it.
- **Audit completeness** — every scan, mapping, and decision is
  written so Part 09 can show an unbroken trail.

**Honest limits (need real hardware to settle):**

- **Real scanner read-rate.** Sim renders a clean, undamaged barcode
  under controlled "lighting." Real labels are curved on round vials,
  smudged, frosted, condensation-covered, or partly peeled. The true
  first-pass read-rate and the **no-read** frequency can only be
  measured on hardware with a real scanner.
- **Label application.** If a printer/applicator is in scope, whether
  labels go on straight and stick is purely a hardware question.
- **Pose for the read.** Whether the 280 can reliably present a vial
  to a fixed scanner (or position a camera to a label) at the right
  standoff is approximated in sim by ideal poses.

So sim proves the **decode software, the tracking/registry logic, and
the quarantine behaviour**; it does not prove **real-world read-rates
or label physics**.

## Open-source tools

| Tool | Role | Bottom line |
|------|------|-------------|
| **OpenCV** | Grabs frames from the sim camera, pre-processes (crop, threshold, undistort) before decode | Standard CV glue for the read step |
| **pyzbar** (ZBar) | Decodes 1D/2D barcodes (Code128, QR) from an image to a string | The decoder that runs identically in sim and on hardware |
| **Barcode generator** (e.g. `python-barcode`, `qrcode`) | Renders the label images that become vial textures | Makes the "real" codes the pipeline reads |
| **Gazebo Harmonic** (camera sensor) | Provides the simulated scanner camera + textured vial models | Source of the images to decode |
| **`/scan` mock service** (ROS 2 node) | Path (b): returns the virtual ID for a vial at the scan frame | Fast identity without optics |
| **Registry node** (ROS 2 + **SQLite**) | Holds vial-ID ↔ slot ↔ worklist-row ↔ LIMS sample-ID; reconciles vs. worklist | The single source of "what is where" |
| **FastAPI** | Exposes the registry / worklist for inspection and for Part 09's LIMS bridge | Thin query + ingest surface |
| **RViz2 / Foxglove** | Visualise the scan camera feed, decoded IDs, and slot assignments | Eyeball the chain as it builds |

## How to simulate it now

**1. Give every vial a real barcode (path a).**

- For each sample, **generate** a Code128 or QR image encoding its
  vial-ID (`python-barcode` / `qrcode`).
- Apply the image as a **texture** on the vial model's label band so
  it spawns into Gazebo already "labelled."
- Keep path (b) available too: the same spawn step also writes the ID
  as a model **property**, so the `/scan` mock service can return it
  without a camera when you want to test logic only.

**2. Add a sim scanner camera + decode node.**

- Place a **camera sensor** in the world at a fixed `scan_station`
  tf frame (a station the arm presents vials to — see the mock
  stations pattern in Part 08), publishing on an image topic.
- A `barcode_reader` node subscribes to that image, uses **OpenCV**
  to crop/threshold, and calls **pyzbar** to decode. It publishes the
  decoded vial-ID on `/vial_id` (or answers a `/read_barcode`
  service). This is the same node you later point at a real camera.

**3. Populate the registry (SQLite).**

- A `registry` node ingests the **worklist** (each row = expected
  sample-ID, target slot, recipe ref for Part 04) into SQLite.
- On each successful read, it records `vial_id → slot → worklist_row
  → lims_sample_id` with a timestamp, and **reconciles**: does the
  vial scanned for this row match the row's expected sample?
- Expose it via **FastAPI** for Part 09's audit trail / LIMS bridge.

**4. Test a deliberate mix-up.**

- Spawn a vial whose barcode/ID does **not** match the worklist row
  about to be filled (or swap two vials).
- Confirm the reconcile step flags a **mismatch**, raises a
  **quarantine** event (vial set aside, not placed / flagged in the
  slot), and writes the discrepancy to the audit log — handed to
  Part 08 for the actual stop/retry/alert behaviour.

**Workflow per vial:** spawn (textured + ID property) → present to
`scan_station` → camera frame → OpenCV + pyzbar decode (or `/scan`
mock) → registry lookup vs. worklist → match? record `vial → slot →
row → LIMS` : raise mismatch/quarantine → continue. Every step is
logged.

## Additional hardware needed

| Real hardware | Why | How mocked in sim |
|---------------|-----|-------------------|
| **Barcode scanner** (fixed-mount or handheld-style imager) | Reads the real label on the real vial | A Gazebo **camera sensor** + OpenCV/pyzbar decode node, **or** the `/scan` mock service returning a virtual ID |
| *(optional)* **Label printer / applicator** | Prints and applies labels if vials arrive unlabelled | Skipped in sim, or modelled as a texture written at spawn time |
| *(optional)* lighting / fixture for the read | Stable, repeatable scanner reads | Ideal sim camera pose + lighting; real standoff/lighting tuned on hardware |

The decode *software* is fully built and proven in sim; what the
hardware adds is the **real read-rate** and **label handling**.

## How it connects

- [`04-liquid-handling-and-sample-prep.md`](04-liquid-handling-and-sample-prep.md)
  — the identity resolved here selects the **recipe / prep** for each
  sample; wrong ID means wrong prep, so the read gates the pour.
- [`05-tray-loading-and-positioning.md`](05-tray-loading-and-positioning.md)
  — provides the **vial → slot** placement this doc records; we store
  the slot actually used against the vial-ID.
- [`08-orchestration-error-handling-and-safety.md`](08-orchestration-error-handling-and-safety.md)
  — consumes the **mismatch / no-read / quarantine** events and
  decides stop, retry-scan, or set-aside-and-alert.
- [`09-software-compliance-and-integration.md`](09-software-compliance-and-integration.md)
  — owns the **worklist ingest, LIMS sample-IDs, audit trail, and
  data-integrity** rules the registry feeds.
- Back to the overview: [`README.md`](README.md).
