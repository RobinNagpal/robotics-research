# Project 1 — Rental unit condition & damage inspection

> The simplest of the three. A 2D problem: photo in, "damage / no
> damage" out. No 3D geometry, no robot, no camera calibration. If you
> only build one project to show a customer, build this one.
>
> Scenario: residential property management companies in Ontario,
> Canada.

**Timeline: 3-4 weeks** (1 week to learn the tools, 1-2 weeks to build
the pipeline, ~1 week to package and polish a demo).

---

## 1. Problem Statement

Property management companies across the Greater Toronto Area (GTA) and
the rest of Ontario each manage hundreds to thousands of rental units.
Between tenancies ("turnover") and during routine inspections, a
property manager or building superintendent walks every unit and
photographs it — walls, floors, kitchen, bathroom, appliances. They're
hunting for damage: holes and dents in drywall, burns and stains on
carpet, cracked tiles, water damage, mold, broken fixtures, missing
appliances.

Today this is entirely manual. A staff member shoots dozens of phone
photos, then either eyeballs them or dumps them in a folder with no
analysis. It's inconsistent between staff, easy to miss damage during a
rushed turnover, and painful to assemble into a clean before/after
record.

**The Ontario angle — this is why they'll pay.** Under Ontario's
*Residential Tenancies Act*, a landlord **cannot collect a damage
deposit** — only last month's rent. The only way to recover the cost of
tenant-caused damage (beyond normal wear and tear) is to apply to the
**Landlord and Tenant Board (LTB)**, which is heavily backlogged and
decides on the strength of your **evidence**. Vague or missing
documentation means the landlord simply eats the repair bill. Turnover
damage routinely runs $500-$5,000+ per unit, so for a firm managing
thousands of doors, weak documentation is a real, recurring loss — not
a hypothetical one.

**What you sell:** a mobile-friendly web app where field staff upload a
unit's photos (a move-in set, a move-out set, or a routine inspection).
The system flags the photos that show likely damage, highlights the
damaged region, and assembles a dated, organized report — LTB-ready
evidence instead of a messy camera roll.

**The technique: anomaly detection.** You might assume you'd train a
model on every kind of damage. You can't — damage is endlessly varied.
So you flip it around: you teach the model what an *undamaged* surface
looks like (clean walls, intact flooring, normal fixtures) using the
huge volume of "good condition" photos these firms already have, and
the model flags anything that *deviates*. You only need lots of "good"
photos (trivial to collect) and few or even zero examples of each
specific defect.

---

## 2. Why this is unique, demo-able, and sellable

**Demo-able — this is the strongest selling point.** Photograph a clean
apartment, then add a few damaged spots (a drywall hole, a carpet
stain, a cracked tile), train on the clean set, and in the same meeting
show the model flagging the damaged photos with a heatmap over the
exact spot — on *their* building, with *their* photos. The whole demo
is a laptop and a phone, no hardware to ship.

**Unique — you add the layer everyone else is missing.** Property
managers already pay for photo-inspection apps (HappyCo, zInspector,
RentCheck, and the inspection modules in Yardi and AppFolio), which
proves the willingness to pay. But those tools only *organize* photos —
a human still has to spot the damage and decide what matters. Your
differentiator is the computer-vision layer that *finds* the damage
automatically and turns it into a highlighted, LTB-ready report. You're
not displacing their workflow; you're removing the tedious, error-prone
part of it.

**Sellable — the ROI is tied to money they already lose.** Every unit
where damage is missed or poorly documented is a repair bill the
landlord can't recover at the LTB. You can frame your fee against that
loss directly, and the product is exactly the model these firms already
buy: recurring **per-door** SaaS. Pricing follows the inspection-app
market — a per-unit-inspection fee or a per-door monthly fee, plus a
modest onboarding fee to load each firm's "good condition" baseline.

It's also the **lowest-risk project to start with**: a 2D
photo-in/flag-out problem with no 3D math, no robot integration, and no
calibration. You can ship it solo in a month.

---

## 3. Technologies to learn to get started

If you already know Python and web development, the genuinely new
material here is small — about 3-5 days of focused study before you're
productive.

**Image basics (1 day).**
- Loading, resizing, and normalizing photos with **OpenCV** and
  **NumPy**. Internalize that an image is just an `H × W × 3` array of
  pixel values (height, width, 3 color channels).
- Handling phone-photo realities: reading **EXIF** orientation so
  sideways photos don't break the model, and normalizing for the wildly
  different lighting you get across real units.

**The anomaly-detection concept (1 day).**
- One-class learning: train only on "good condition" examples; at
  inference, score how far a new photo is from "good." Understand why
  this beats trying to enumerate every kind of damage.

**The core library — `anomalib` (2-3 days).**
- `anomalib` is an open-source library (MIT license) with ready-made
  implementations of the standard models: **PatchCore**,
  **EfficientAD**, **PaDiM**. Learn to point it at your photo folder,
  train, and read the anomaly heatmap it outputs. A first working model
  is a weekend's work.
- **DINOv2 embeddings + nearest-neighbor** as a strong baseline: a
  pretrained vision model turns each photo into a vector ("embedding");
  damaged photos land far from the tight cluster of clean ones. At this
  data scale it often beats more complex supervised approaches.
- **Optional extension — named damage categories.** Once the anomaly
  baseline works, a small **YOLO** object detector trained on a few
  hundred labeled examples can name the common, high-value categories
  (water stain, mold, drywall hole, broken fixture) so the report says
  *what* the damage is, not just *where*.

**Evaluation vocabulary (1 day — do not skip).**
- **Precision** and **recall**, the trade-off between them, and how to
  pick a decision threshold. This is the one thing you *must* be able
  to explain in plain English to a non-technical property manager.
  Build a single slide that maps "missed damage" (unrecovered repair
  cost) against "false alarms" (staff time wasted re-checking) and
  reuse it in every pitch.

**Deployment — a cloud web/mobile app, not on-prem.** Unlike a factory,
field staff inspect units on a phone, so this is a hosted service:
- A mobile-friendly **React** (or PWA) front-end for capturing and
  uploading a unit's photos in the field, viewing flagged results, and
  exporting the report.
- A **FastAPI** backend with the model served behind it; export the
  model to **ONNX** for fast, cheap inference.
- **Stripe** for per-door / per-inspection billing.
- **Canadian data residency (PIPEDA).** These are photos of people's
  homes, so host in a Canadian region (e.g. AWS `ca-central-1`) and be
  ready to say, in writing, that tenant data never leaves Canada — this
  is a real procurement question for Ontario property managers.

**Hardware needed:** none special. A laptop trains the baseline models;
the service runs in the cloud and staff use the phones they already
carry.
