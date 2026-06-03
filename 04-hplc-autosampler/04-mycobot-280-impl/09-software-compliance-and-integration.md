# Part 09 — Software, compliance & integration (myCobot 280 simulation)

> **Sim goal:** Prove that the *defensible* part of the product — the
> controller, the audit trail, the access/e-signature controls, and
> the LIMS/CDS hand-off — runs **identically** against the simulated
> myCobot 280 cell and against any real cell, so you can build roughly
> ~90% of it now with **zero hardware** and with no dependence on which
> arm you eventually buy.

This mirrors the high-level
[`../01-high-level-solution/09-software-compliance-and-integration.md`](../01-high-level-solution/09-software-compliance-and-integration.md).
New robotics terms are defined in
[`../../03-place-items-on-shelf/02-glossary.md`](../../03-place-items-on-shelf/02-glossary.md).

## What we can prove in simulation

This whole layer is **pure software**, and — the key point for this
folder — it is **arm-agnostic**. It never commands a motor or reads a
camera directly. It ingests a worklist, issues high-level steps to the
orchestration layer (Part 08), and records what happened. The
orchestrator speaks the same ROS 2 interfaces
(`FollowJointTrajectory`, `GripperCommand`, the mock-station services)
whether the arm underneath is the Gazebo **myCobot 280** twin, a
**reBot**, a **UR3e/UR5e**, or the real myCobot driven by
`pymycobot`. So **every line of this layer you write against the
simulated 280 cell carries over unchanged** — both to the real arm and
to a *different* arm if the platform decision in Part 10 changes. That
makes this the safest, highest-value code to build first.

A few acronyms used throughout:

- **LIMS — Laboratory Information Management System.** The lab's
  database of record for samples (what arrived, who owns it, which
  tests it needs, the results).
- **CDS — Chromatography Data System.** The software that drives the
  **HPLC** (High-Performance Liquid Chromatography) instrument and
  holds the **worklist** — the ordered list of which vial runs with
  which method. Dominant products: **Waters Empower** and **Thermo
  Scientific Chromeleon**.
- **21 CFR Part 11.** The US FDA (Food and Drug Administration) rule
  that says electronic records and signatures must be as trustworthy
  as wet-ink paper — controlled, attributable, and traceable. (EU
  equivalent: **EU GMP Annex 11**.)
- **ALCOA+.** A memory aid for good data: **A**ttributable,
  **L**egible, **C**ontemporaneous (recorded at the time),
  **O**riginal, **A**ccurate — plus Complete, Consistent, Enduring,
  Available.

**Can prove fully now (software, no hardware):**

- **Worklist ingestion.** The controller reads a worklist — a **CSV**
  (plain spreadsheet export) for v1 — and turns each row into a
  prep-and-load job.
- **Driving the Behavior Tree.** The controller issues high-level
  steps to the Part 08 orchestrator and consumes the results, replay
  after replay, against the Gazebo myCobot 280 cell.
- **Immutable audit trail.** Every action (who/what/when, and why) is
  written to an **append-only** store — see below. You can run a batch
  and then inspect the exact trail an auditor would read.
- **Role-based access control (RBAC)** — named operator / reviewer /
  administrator users, no shared logins, each action attributed.
- **Electronic review / approval / e-signature** — a reviewer
  inspects the as-prepared record in the UI and signs it before the
  tray is "released," with the signature capturing who/what/when/
  meaning.
- **Mock LIMS/CDS integration** — a stand-in service supplies the
  worklist and receives the "ready to inject" hand-off, exercising
  the integration contract end to end.

**Honest limits (cannot be simulated):**

- **IQ/OQ/PQ qualification** — **I**nstallation / **O**perational /
  **P**erformance **Q**ualification: documented proof the system was
  installed right, operates right, and performs right *in real use*.
  You cannot qualify a simulated installation.
- **CSV — Computer System Validation** — the documented lifecycle that
  keeps the software in a validated state. This is a funded,
  specialised, hardware-and-process effort, not a sim artefact.
- **Real CDS API behaviour** — Empower / Chromeleon toolkits,
  licensing, and quirks must be tested against the real product; our
  mock proves the *shape* of the integration, not the vendor's actual
  API.

So sim proves the **software logic, the data-integrity story, and the
integration contract** end to end. It does **not** discharge the
regulatory **validation** obligation — that is explicitly deferred
(see the moat note below).

## Open-source tools

| Tool | Role | Bottom line |
|------|------|-------------|
| **FastAPI** (Python) | Hosts the **mock LIMS/CDS** service and the controller's REST API/UI endpoints | Stands in for Empower/Chromeleon to serve the worklist + take the hand-off |
| **SQLite** | Append-only **audit-trail** store and worklist/RBAC tables; single-file, easy to inspect | Immutable log on our side, zero infra to run |
| **Hash-chained JSONL** (optional) | Alternative tamper-evident audit log — each line carries a hash of the previous, so silent edits show up | Makes "immutable" provable, not just policy |
| **BehaviorTree.CPP** (+ Groot2) | The orchestration the controller drives (Part 08); the controller logs every tick/decision | The controller issues steps, the BT executes them |
| **ROS 2** (Humble/Jazzy) | Carries the controller↔orchestrator messages, identical in sim and on any arm | Same interface whether myCobot 280, reBot, or UR is underneath |
| **Gazebo Harmonic** | Hosts the simulated myCobot 280 cell the controller drives during replay | The "cell" the software talks to before hardware exists |
| **RViz2 / Foxglove** | Watch the controller drive the cell; Foxglove panels can show audit events live | Eyeball the run and the trail together |

## How to simulate it now

**1. Stand up the mock LIMS/CDS.** A small **FastAPI** service with two
endpoints:

- `GET /worklist` — returns a sequence of rows (sample ID, recipe,
  order, target slot), loaded from a **CSV** file you control. This is
  the stand-in for pulling a sequence from Empower/Chromeleon.
- `POST /ready-to-inject` — receives the controller's as-prepared
  record (which vial went to which slot, with the audit references)
  when the tray is loaded and signed off. This is the hand-off the
  real CDS would consume to start the run.

**2. Run the controller alongside the Gazebo myCobot 280 cell.** The
controller:

- Pulls the worklist from the mock CDS.
- For each row, calls the Part 08 orchestrator (Behavior Tree) to prep
  and load that vial in Gazebo — driving the 280 URDF exactly as it
  would drive a real arm.
- Writes an **audit event** for every meaningful action and decision —
  worklist imported, vial picked, decapped, dispensed, recapped,
  placed in slot, verified, any retry or quarantine — each stamped
  with the **user**, a **UTC timestamp**, the **vial/sample ID**, and
  the **outcome**. Write-once: never overwrite, never delete.

**3. Enforce access control + e-signature.** Seed a few named users
with roles (operator runs batches; reviewer approves; admin manages
users). Before the controller calls `/ready-to-inject`, require a
**reviewer e-signature** on the as-prepared record — captured as its
own audit event (who, what record, when, the meaning of the signature,
e.g. "reviewed and approved for injection").

**4. Replay batches and inspect the evidence.** Run several worklists
through the simulated cell, including ones where Part 08 injects
failures (missed slot, decap fault). Then:

- Dump the **audit trail** and read it as an auditor would — confirm
  every action is attributable, contemporaneous, and complete
  (ALCOA+), and that failures and retries are all recorded.
- If using the hash-chained log, run the verifier to show the chain is
  intact (tamper-evident).
- Confirm no `/ready-to-inject` hand-off ever fires without a valid
  reviewer e-signature in the trail.

**Workflow per batch:** pull worklist (mock CDS) → controller drives BT
per row against the Gazebo myCobot 280 → log every action to the
append-only store → reviewer e-signs the as-prepared record →
controller posts `ready-to-inject` → inspect audit trail + e-sign
records.

## Additional hardware needed

| Real hardware | Why | How mocked / handled |
|---------------|-----|----------------------|
| **None for development** | This layer is pure software; it runs against the simulated cell exactly as against a real one | The Gazebo 280 twin *is* the cell; mock FastAPI *is* the CDS/LIMS |
| *(production)* real **CDS/LIMS** (Empower / Chromeleon / OpenLab) | Live worklist pull + run trigger in the actual lab | Mock FastAPI service proves the integration contract; swap in the vendor toolkit later |
| *(production)* a **qualified industrial PC** | A controlled, validatable host the software runs on in the lab | Develop on any workstation; the software is identical |

Because the layer is software and arm-agnostic, **the whole thing can
be built and demonstrated now** — the only "hardware" it needs is the
simulator standing in for the cell, and nothing here changes if you
later trade the 280 for a 320 or a UR arm.

## How it connects

- [`06-identification-labeling-and-tracking.md`](06-identification-labeling-and-tracking.md)
  — supplies the sample IDs and the worklist this controller ingests,
  and consumes the as-prepared record; the audit trail ties each ID to
  its actions.
- [`08-orchestration-error-handling-and-safety.md`](08-orchestration-error-handling-and-safety.md)
  — the controller drives this Behavior Tree and **logs every
  decision, retry, and failure** it reports into the audit trail.
- [`10-hardware-platform-and-capital-model.md`](10-hardware-platform-and-capital-model.md)
  — validation and containment requirements here drive the hardware
  and layout choices there (a cell you can put a boundary around is a
  cell you can IQ/OQ/PQ).
- Mirrors
  [`../01-high-level-solution/09-software-compliance-and-integration.md`](../01-high-level-solution/09-software-compliance-and-integration.md);
  back to the index: [`README.md`](README.md).

> **The moat.** Pure-robotics teams underestimate this layer. An arm
> that picks a vial is a solved-ish problem; a controller an FDA or EU
> inspector will accept — Part 11 audit trail, e-signatures, RBAC, a
> CSV/IQ/OQ/PQ package, clean CDS integration — is months of
> specialised work most robotics teams lack. Crucially, because it is
> **arm-agnostic**, this software is reusable across *every* platform
> choice in Part 10: it is the asset that survives whether you ship a
> myCobot, a reBot, or a UR cell. Sim lets you build and prove ~90% of
> it *before* spending on hardware, which is exactly why this layer,
> not the arm, is the real competitive moat. **Re-verify** the exact
> Part 11 / Annex 11 / ALCOA+ expectations against current FDA/EU
> guidance and the customer's own quality SOPs before quoting
> anything — interpretation drifts.
