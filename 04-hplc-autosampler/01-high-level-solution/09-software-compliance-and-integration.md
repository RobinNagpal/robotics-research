# Part 09 — Software, compliance & integration

> **Problem:** In a regulated lab the robot is the easy part — the
> hard, defensible part is software that talks to the lab's existing
> systems and proves, to an auditor's standard, exactly what was done
> to every sample.

## The problem

A robotic arm that prepares and loads vials does not run in a
vacuum. It has to fit into the way a real quality-control (QC) or
pharmaceutical lab already works, and that work is governed by
**regulation**, not just convenience. Two things make the software
the centre of gravity for this product:

**1. It must integrate with the lab's existing software.** Two
acronyms matter:

- **LIMS — Laboratory Information Management System.** The lab's
  system of record for samples: what arrived, who owns it, what
  tests it needs, and the results once they exist. Think of it as
  the database that tracks every sample through the building.
- **CDS — Chromatography Data System.** The software that actually
  drives the HPLC instrument and captures/processes the
  chromatogram (the data the instrument produces). The dominant
  products are **Waters Empower** and **Thermo Scientific
  Chromeleon**; **Agilent OpenLab** is a third. The CDS holds the
  **worklist** (also called the **sequence**): the ordered list of
  which vial gets run, with which method/recipe, in what order.

Our system sits *upstream* of the CDS. The flow we must support:

```
LIMS / CDS  --(worklist: samples, recipes, order)-->  our controller
our controller  --(prepares & loads vials per worklist)-->  tray
our controller  --(reports what was actually prepared/loaded)-->  CDS
CDS  --(starts the HPLC run on the loaded tray)-->  instrument
```

If we cannot pull the worklist and report back accurately, the lab
has to re-type everything by hand — which destroys the time savings
and *introduces* the transcription errors automation is supposed to
remove.

**2. It must satisfy data-integrity regulation.** Pharma and many
QC labs operate under **GxP** — a family of "Good Practice" quality
regulations (GMP = Good Manufacturing Practice is the relevant one
here). For software and records the key rules are:

- **21 CFR Part 11** — the US FDA regulation that says when you keep
  records and signatures electronically (instead of on paper), they
  must be trustworthy: controlled, traceable, and as reliable as a
  wet-ink signature. (The EU equivalent is **EU GMP Annex 11**.)
- **ALCOA+** — a memory aid for what good data must be:
  **A**ttributable (who did it), **L**egible, **C**ontemporaneous
  (recorded at the time), **O**riginal, **A**ccurate — plus
  Complete, Consistent, Enduring, and Available. Every action our
  system takes has to produce data that meets this bar.
- **Audit trail** — an **immutable** (cannot be silently edited or
  deleted) timestamped log of who did what, when, and why, for
  every meaningful action. "Immutable" is the load-bearing word: an
  auditor must be able to trust that the log was not rewritten after
  the fact.
- **Access control / roles** — only authorised users can act, each
  has a defined role (operator, reviewer, administrator), and the
  system records *which* user did each thing. No shared logins.
- **Validation** — documented proof that the system does what it
  claims, reliably. The standard ritual is **IQ/OQ/PQ**
  (Installation / Operational / Performance **Q**ualification:
  proof it was installed right, operates right, and performs right
  in real use) wrapped in **CSV — Computer System Validation**, the
  documented lifecycle that keeps the software in a validated state.

**Why this is the moat.** Competitors who come from a pure-robotics
or pure-mechanical background consistently underestimate this layer.
Building an arm that picks a vial is a solved-ish engineering
problem; building a controller that an FDA or EU inspector will
accept — Part 11 audit trail, e-signatures, role-based access, a
validation package, and clean CDS integration — is months of
specialised work plus domain knowledge most robotics teams lack. A
lab will not buy a beautifully engineered arm that breaks their
compliance posture. This software is what makes the product
*sellable* into regulated labs, and it is hard to copy. Treat it as
a core differentiator, not an add-on.

## The solution

A **controller application** that is the brain and the system of
record for the cell. Responsibilities:

- **Ingest the worklist** from the CDS/LIMS (which samples, which
  recipe, which order, which slot).
- **Drive the cell** by calling the orchestration layer (see
  `08-orchestration-error-handling-and-safety.md`) — it does not
  re-implement motion; it issues high-level steps and consumes the
  results.
- **Log an immutable audit trail** — every decision and action,
  attributed to a user and timestamped, write-once.
- **Support electronic review / approval / e-signature** — a
  reviewer can inspect what was prepared and sign off before the run
  is released.
- **Integrate with LIMS/CDS** — pull the sequence, push back the
  as-prepared record, and hand off to the CDS to start the run.

How each regulatory requirement is met:

| Requirement | How we meet it | Bottom line |
|---|---|---|
| **21 CFR Part 11 (e-records)** | Write-once audit store; controlled, attributable records of every action | Records are trustworthy and inspectable |
| **21 CFR Part 11 (e-signatures)** | Per-user credentials; signing captures who/what/when/meaning | Sign-off is as binding as wet ink |
| **ALCOA+** | Contemporaneous timestamping at the moment of action; original record never overwritten | Data integrity by construction, not policy |
| **Audit trail (immutable)** | Append-only log, tamper-evident (hash-chained), no silent edits/deletes | Auditor can trust the history |
| **Access control / roles** | Named users, role-based permissions (operator/reviewer/admin), no shared logins | Right people, recorded, only allowed actions |
| **Validation (IQ/OQ/PQ + CSV)** | Versioned, documented, testable software; install/operate/perform test scripts; change control | System is provably fit for use |
| **LIMS/CDS integration** | Worklist import + as-prepared export; handoff to start run | No manual re-keying; closes the loop |

The controller is the **single point of truth**: nothing happens in
the cell that the controller did not authorise and record.

## v1 vs later

**v1 (keep it simple, but compliance-credible):**

- **Import a simple worklist** — e.g. a **CSV** file (a plain
  spreadsheet export of samples, recipes, order, slots) rather than
  a live CDS connection.
- **Full local audit log** — append-only, timestamped, attributed;
  immutable on our side.
- **Role-based access control** — named operator/reviewer/admin
  users, no shared logins.
- **Manual e-signature approval** — a reviewer signs off the
  as-prepared record in our UI before the tray is released to the
  CDS.
- **Manual handoff** — a human starts the CDS run once the tray is
  loaded.

This proves the data-integrity story end to end without depending on
a vendor API on day one.

**Defer to later (required for production; a funded effort):**

- **Deep CDS API integration** — live two-way connection to Empower
  / Chromeleon / OpenLab to pull sequences and push results, and to
  trigger the run automatically. Each CDS has its own toolkit
  (e.g. Empower Toolkit) and licensing.
- **Full GxP validation package** — the complete IQ/OQ/PQ
  documentation and CSV lifecycle a customer's quality unit will
  demand before production use. This is substantial, specialised
  work and should be planned and resourced explicitly.
- **LIMS integration** beyond the CDS, plus enterprise SSO/identity,
  centralised audit aggregation, and electronic-batch-record hooks.

> **Note:** Specific regulatory references (21 CFR Part 11, Annex
> 11, ALCOA+) and the exact validation expectations should be
> re-verified against current FDA/EU guidance and the target
> customer's own quality SOPs before being quoted in a proposal —
> interpretation drifts and customers vary.

## How it connects

- `06-identification-labeling-and-tracking.md` — supplies the
  sample IDs and the worklist this controller ingests, and consumes
  the as-prepared record; the audit trail ties each ID to its
  actions.
- `08-orchestration-error-handling-and-safety.md` — the controller
  calls the orchestrator and logs every orchestration decision,
  retry, and failure into the audit trail.
- `10-hardware-platform-and-capital-model.md` — validation and
  containment requirements here drive hardware and footprint
  choices (e.g. an enclosure that can be qualified, a layout that
  supports IQ/OQ).
- Back to the overview: `README.md`.
