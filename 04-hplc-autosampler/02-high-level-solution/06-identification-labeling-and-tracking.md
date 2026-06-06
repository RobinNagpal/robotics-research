# Part 06 — Identification, labeling & tracking

> **Problem:** Every sample must be uniquely identified and
> traceable from the moment it enters the system to the data it
> produces — because the worst failure in a QC lab is a **mix-up**:
> correct results attributed to the wrong sample.

## The problem

In a regulated lab, knowing *which* sample produced *which* result
is not optional — it is the whole point. The unbroken record of
"who held this sample and where it was, at every step" is called
the **chain of custody**. If that chain breaks, the data is
worthless and, in pharma, potentially a compliance violation.

The central risk our system must defend against is a **sample
mix-up**: a vial physically ends up associated with the wrong
identity, so good analytical data gets attributed to the wrong
sample. This can happen if a vial goes into the wrong slot, if two
vials are swapped, or if the software's idea of "what is where"
drifts away from physical reality.

To prevent this we need three things working together:

1. A **unique identifier** on every vial that a machine can read.
2. A reliable way to **read** that identifier at the right moments.
3. A **software registry** that ties identifier → location →
   worklist position → lab record, and that **reconciles** itself
   against the worklist so any disagreement is caught immediately.

A note on barcodes (the usual identifier):

- **1D barcode** — the familiar stripes; encodes a short number or
  code. Needs reasonable width and a fairly square-on read.
- **2D barcode** (e.g. a Data Matrix or QR code) — a grid of dots;
  packs far more data into a tiny square, tolerates damage better,
  and can be read at more angles. Better suited to the small,
  curved surface of a 2 mL vial or its cap.

Barcodes can be **on the vial body** or **on the cap**. Cap labels
read well from straight above; body labels read from the side but
can be hidden by how the vial is rotated.

## The solution

**Labeling — where the identifier comes from:**

| Option | How it works | Pros | Cons | Bottom line |
|---|---|---|---|---|
| **Pre-barcoded vials** | Buy vials that already carry a unique 2D barcode from the supplier | No printer, no applicator, no print errors; identity is fixed and trusted | Must associate each barcode to a sample once at intake; limited label content | Simplest and most reliable; the v1 choice |
| **Print-and-apply (in-line)** | A label printer prints a barcode on demand and an applicator sticks it on the vial | Encode anything; label on the fly | Adds a printer + applicator + adhesion/placement failure modes; print quality must be verified | Powerful but more moving parts and more ways to fail; defer |

**Reading — how we capture the identifier:**

- A **fixed scanner** — a dedicated barcode reader at a known spot;
  the arm presents the vial to it (or rotates it past it). Fast and
  very reliable for the one job of decoding.
- A **camera** — the same vision used elsewhere
  (`07-perception-and-verification.md`) decodes the barcode. Fewer
  parts; needs good lighting and resolution. May require rotating
  the vial so a body label faces the lens.

For v1 we **read and verify only** — we do not create or print
identities, we confirm the ones already on the vials.

**The software registry** is the heart of traceability. It is a
table the orchestrator maintains that maps, for every vial:

```
vial barcode ID  →  tray slot (A1…)  →  worklist row  →  LIMS sample ID
```

A **LIMS** (Laboratory Information Management System) is the lab's
system of record — it owns sample IDs, tests requested, and
results. The **worklist** is the ordered run list the autosampler
executes (see `09-software-compliance-and-integration.md`).

**Reconciliation** is the safety mechanism. At each meaningful step
the system checks the physical reading against the expected record:

- At **intake**, the read barcode must match a sample known to the
  worklist/LIMS.
- At **slot placement**, the vial ID just placed must equal the ID
  the registry expects for that slot.
- Before **handing the tray to the autosampler**, every slot's
  occupant is re-read and matched to the worklist row.

On **any mismatch** — unknown barcode, unreadable code, wrong vial
for a slot, duplicate ID — the system **does not guess**. It raises
an error and **quarantines** the affected vial(s): set aside, flag
for a human, and refuse to run that position. Detailed handling of
these failures lives in
`08-orchestration-error-handling-and-safety.md`.

## v1 vs later

**v1 (keep it simple):**

- **Pre-barcoded vials** (2D barcode), one vial type — no printing,
  no applicator.
- **Read-and-verify only**: decode the existing barcode and check
  it against the worklist.
- A **software registry** mapping vial ID → slot → worklist row →
  LIMS sample ID, with reconciliation at intake, placement, and
  hand-off.
- Mismatch → stop, flag, quarantine; a human supervises.

**Defer to later:**

- **In-line label printing and application** for unlabelled vials.
- Print-quality verification (grading the printed barcode).
- Reading **damaged or partially obscured** labels with retries and
  re-orientation.
- Handling **multiple vial/label types** and label-on-cap vs
  label-on-body automatically.

## How it connects

- `04-liquid-handling-and-sample-prep.md` — the vial ID selects
  which **recipe** to apply to each sample.
- `05-tray-loading-and-positioning.md` — consumes the vial→slot
  mapping defined here and realises it physically; reports back the
  slot actually used.
- `08-orchestration-error-handling-and-safety.md` — owns the
  mismatch/quarantine handling triggered by failed reconciliation.
- `09-software-compliance-and-integration.md` — home of the
  worklist, the LIMS link, the audit trail, and the data-integrity
  rules that govern this registry.
- Back to the overview: `README.md`.
