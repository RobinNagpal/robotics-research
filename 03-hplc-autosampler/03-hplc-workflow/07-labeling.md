# Step 7 — Labeling

> **In one line:** mark each vial so we always know exactly what is
> inside it and where it came from.

This is the seventh of the eight steps (see the
[overview](README.md)). It follows
[Step 6 — Capping](06-capping.md).

## The words you need here

- **Label** — a small sticker (or some writing) on the vial that says
  **what is inside**. As a verb, "to label" means "to put that
  identification on."
- **Sample ID** — a short **name or number** that uniquely identifies
  one sample, like "P-001" or "Brand-A-rep2." No two samples in a run
  should share an ID.
- **Barcode** — the pattern of black stripes (or a square QR-style code)
  that a scanner can read instantly. A barcode is just a **machine-
  readable version of the Sample ID** — faster and less error-prone than
  reading handwriting.
- **Dilution factor** — the "how many times weaker" number from
  [Step 3 — Dilution](03-dilution.md). It is often recorded with the
  sample so the final maths is correct.
- **Traceability** — being able to follow a result **all the way back**
  to the exact sample, person, date, and steps that produced it. In
  regulated labs this is a legal requirement; a result you cannot trace
  back is worthless.
- **LIMS** — short for *Laboratory Information Management System*: the
  lab's computer system that hands out Sample IDs and keeps the master
  list of what each one is. (You do not need this for our small example,
  but the word appears often in real labs.)

## Why we do this

A tray may hold **dozens** of vials that look **completely identical** —
the same little glass bottles full of the same clear liquid. Without
labels, they are impossible to tell apart, and a single mix-up ruins the
whole run: a result would be pinned to the wrong product.

The label answers the most important question about every vial: **"which
sample is this, exactly?"** It is what links the number the machine
prints back to a real tablet or a real bottle of ketchup. This linking —
**traceability** — is the entire point of being careful: an answer is
only useful if you are certain *what* it is an answer *to*.

## What you actually do (the general routine)

1. Get the correct **Sample ID** for the vial (from your notes or the
   lab's computer system).
2. Write it on the vial, or — much more common today — **print a sticky
   label with a barcode** and wrap it around the vial.
3. Often include extra useful details: the **date**, the **dilution
   factor**, and your initials.
4. Double-check the label matches the vial's actual contents **before**
   moving on.

## Paracetamol example (the easy case)

- Each vial gets a clear, simple label, for example:
  - `In-house batch`
  - `Brand A`, `Brand B`, `Brand C`, `Brand D`
  - `Standard` (the reference)
  - `Blank` (solvent only — a check for contamination)
- Because there are only a handful of vials, the labels are easy to keep
  straight.

## Ketchup example (the hard case)

- Food testing often involves **more vials**: several **supplier
  batches**, each prepared **2–3 times** (repeats), plus a standard and
  a blank. So you might label something like:
  - `Supplier-1 / batch-A / rep-1`, `... / rep-2`, `... / rep-3`
  - `Supplier-2 / batch-B / rep-1` … and so on.
- The action is identical to the drug case, but with **more vials and
  longer IDs**, the **risk of a labelling mix-up is higher**. This is
  why barcodes are so valued: a scanner never misreads a "1" as a "7."

So once again, the difference is not the difficulty of the motion — it
is the **number of items** and the bookkeeping around them.

## What can go wrong

- **Wrong label on a vial** → the result is attributed to the wrong
  sample. This is one of the most damaging errors possible, because the
  numbers themselves look perfectly fine.
- **Smudged or fallen-off label** → the vial becomes an anonymous
  mystery.
- **Two vials with the same ID** → impossible to tell which is which.
- **Forgetting the dilution factor** → the final calculation is wrong.

## For the robot arm

Labeling is one of the **easier** steps to automate. It does **not**
need fine physical precision — sticking a label roughly straight onto a
vial is forgiving. The real value of automating it is **accuracy of
information**, not of motion: a machine that prints and applies a
barcode, and logs the ID automatically, **never mismatches** a label the
way a tired human at the bench can. In fact, a robot naturally keeps a
perfect record of every vial it handles — turning this step into a
reliability *gain*, not just a task it copies.

## Objects needed in the simulation scene

Beyond the **shared workcell** (arm, gripper, table, overhead + wrist
cameras, a YOLO object detector, racks), this step adds:

| Object | What it is | Mock node / topic |
|---|---|---|
| **Barcode label stock** | The sticky barcode labels applied to each vial | — |
| **Label printer** | A mock that prints + applies a label and logs each ID, asserting uniqueness | `mock_printer` → `/mock_printer/apply`, `/traceability/log` |
| **Capped vial** | The vial from Step 6 being labelled | shared with Stage 4 |

These are **Stage 6** of the ketchup scene's
[object list](../05-mycobot-280-impl/01-only-code/01-simulation/01-ketchup-experiment-objects.md).

---

**Next step:** put each finished, labelled vial into its exact slot in
the machine → [Step 8 — Placement in the autosampler](08-placement-in-autosampler.md).
