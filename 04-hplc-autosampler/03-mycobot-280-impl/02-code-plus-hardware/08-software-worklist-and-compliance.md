# Layer 08 — Software, worklist & compliance (code-plus-hardware)

> **Job:** With the real myCobot 280 cell running, ingest the
> worklist from real lab systems, drive real instruments, hand
> results to the real Chromatography Data System, and keep a
> regulator-defensible audit trail — the parts that cannot be
> simulated.

A quick vocabulary check before the comparison, because the rest of
this page leans on these terms (see also `../02-glossary.md` style
plain-language definitions):

- **LIMS (Laboratory Information Management System)** — the lab's
  database of samples, tests, and results; it usually *issues* the
  worklist and expects results back.
- **CDS (Chromatography Data System)** — the software that runs the
  HPLC instrument and stores its chromatograms (e.g. Waters
  Empower, Thermo Chromeleon). Your tray ultimately feeds it.
- **SiLA 2 (Standardization in Lab Automation, version 2)** — an
  open, vendor-neutral standard for talking to lab instruments over
  the network via defined "features."
- **OPC UA (Open Platform Communications Unified Architecture)** —
  an industrial machine-to-machine protocol common on PLCs
  (programmable logic controllers) and devices.
- **21 CFR Part 11** — the US FDA rule on electronic records and
  electronic signatures: when an electronic record can replace
  paper, and the controls (audit trail, access control, signed
  records) required.
- **Audit trail** — an immutable, time-stamped log of who did what,
  when, and why.
- **ALCOA+** — a data-integrity checklist: records must be
  Attributable, Legible, Contemporaneous, Original, and Accurate
  (the "+" adds Complete, Consistent, Enduring, Available).
- **IQ/OQ/PQ** — Installation / Operational / Performance
  Qualification: documented proof that a system was installed,
  operates, and performs as intended.
- **CSV (Computer System Validation)** — the documented process of
  proving the whole software system fit for regulated use. (Not to
  be confused with comma-separated-value files.)

The big change from the only-code sibling is that **the things you
could mock are now real**, and a class of work appears that *cannot
be simulated at all*: real Part 11 electronic records and
signatures, ALCOA+ data integrity in practice, and IQ/OQ/PQ + CSV
validation. **This layer is the real differentiator and moat** —
the arm is a commodity; the compliant, integrated software is what
a regulated lab actually buys.

## The five at a glance

| Framework | Role | Tier | One-liner |
|-----------|------|------|-----------|
| **SiLA 2 / OPC UA + validated CDS toolkit + PostgreSQL** | Full standards + CDS + validated store | Best-in-class | Standards to instruments, vendor CDS for chromatography, a robust audited store. |
| **FastAPI + SQLite + CSV/file hand-off to the CDS** | Minimal controller + file bridge | Cheapest | Smallest real integration: drop files the CDS imports, keep a local store. |
| **FastAPI + PostgreSQL + SiLA 2** | Controller over a validated store + standard | Best-practical | Real store and real instrument standard without committing to a commercial CDS SDK yet. |
| **CDS toolkit (Empower Toolkit / Chromeleon SDK)** | Commercial chromatography integration | Alternative | Vendor SDK to drive/extract from the real CDS; powerful, licensed, lock-in. |
| **PostgreSQL** | Validated, robust audit/record store | Alternative | The transactional database under any serious Part 11 record store. |

Tier note: as in the only-code file, the named slots describe the
*shape of the integration you commit to*, not single tools.
Best-in-class is the fully standards-and-CDS stack you would
validate; cheapest is the smallest real hand-off that still works;
best-practical splits the difference. The two Alternatives —
PostgreSQL and the CDS toolkit — are load-bearing pieces that
appear inside the other stacks.

## SiLA 2 / OPC UA + validated CDS toolkit + PostgreSQL

**What it is.** The full production stack. **SiLA 2** (via
`sila_python`) talks to real lab instruments; **OPC UA** (via
`asyncua` in Python, or **open62541**, a mature C OPC UA library,
for embedded/PLC tie-ins) talks to machine controllers; a
**validated CDS toolkit** — Waters **Empower Toolkit** or Thermo
**Chromeleon SDK**, both commercial — drives or exchanges data with
the chromatography system; and **PostgreSQL** holds the records and
audit trail. The mocks from only-code are replaced by their real
counterparts one by one.

**How it's good.** This is the stack a regulated lab can actually
validate and the one that constitutes the moat. Standards-based
instrument control (SiLA 2 / OPC UA) means you integrate broadly
without bespoke glue; the vendor CDS toolkit means your tray and
results line up with the system the lab already trusts for
chromatography; and PostgreSQL gives the transactional integrity,
access control, replication, and backup that a Part 11 record store
needs in practice. Together they support real ALCOA+ data
integrity — attributable, contemporaneous, enduring records — in a
way the lighter stacks cannot.

**How it's bad (vs the other four).** It is the most expensive and
the slowest to stand up. The CDS toolkits are **commercial,
licensed, and vendor-specific** — Empower Toolkit ties you to
Waters, Chromeleon SDK to Thermo — so you inherit lock-in and
licence cost that the **FastAPI + SQLite + file hand-off** option
avoids entirely. Running SiLA servers, OPC UA, a vendor SDK, and
PostgreSQL together is a lot of surface to install, secure, and
*qualify*. And none of that buys you the validation itself: this
stack *enables* compliance but still demands the funded IQ/OQ/PQ +
CSV effort below. It is the right destination, not a quick win.

## FastAPI + SQLite + CSV/file hand-off to the CDS

**What it is.** The minimal real integration. FastAPI is the
controller and review/e-sign UI; SQLite is the local store; and
instead of a live CDS connection, the cell writes **files** — a
worklist or sample-set in the format the CDS can import, and reads
back result files it exports. Many CDS products support exactly this
file-based exchange, so it is a legitimate way to integrate without
a commercial SDK.

**How it's good.** It is the cheapest way to get a *real* cell
talking to a *real* CDS. No SDK licence, no SiLA/OPC UA stack, no
database server — one Python process and a watched folder. For a
first hardware deployment, a small lab, or a pilot where buying the
Empower/Chromeleon toolkit is not yet justified, file hand-off gets
results flowing into the CDS with minimal cost and minimal new
parts to qualify.

**How it's bad (vs the other four).** File hand-off is brittle and
loosely coupled: no live status, no transactional handshake, and
formats that can drift between CDS versions — far less robust than
the **CDS toolkit**'s API. SQLite is single-writer and lacks the
roles, replication, and recovery that **PostgreSQL** brings, so it
is a weak Part 11 record store for multi-user use. And bypassing
**SiLA 2 / OPC UA** means no standards-based instrument control —
the integration is bespoke per file format. It is a pragmatic
bridge, not the moat.

> Re-verify: file-based exchange can still fall under 21 CFR Part 11
> and ALCOA+. Confirm with a quality owner that the file formats,
> transfer integrity, and the SQLite store meet your data-integrity
> obligations before any regulated use.

## FastAPI + PostgreSQL + SiLA 2

**What it is.** The practical middle path for hardware. Keep FastAPI
as the controller and review/e-sign UI, upgrade the store from
SQLite to **PostgreSQL** so the audit trail sits on a validatable,
transactional database, and integrate instruments through real
**SiLA 2** servers — but *defer* the commercial CDS toolkit, using
file hand-off or a later SDK purchase for the chromatography link.

**How it's good.** It gets the two things that are hardest to
retrofit *right* the first time: a robust record store
(PostgreSQL) and standards-based instrument control (SiLA 2). Those
are the parts most entangled with data integrity and compliance, so
building them properly now avoids painful rework. By holding off on
the **Empower/Chromeleon SDK**, you skip the largest licence cost
and the deepest vendor lock-in until the lab's CDS choice and
budget are settled. This is the best balance of "real and
validatable" against "not yet maximally expensive."

**How it's bad (vs the other four).** Without the CDS toolkit, the
chromatography link is still file-based or absent, so it is not the
complete, fully-integrated **best-in-class** stack. It carries more
weight than the **FastAPI + SQLite + file hand-off** option —
PostgreSQL and SiLA servers are real infrastructure to run and
qualify — so it is not the cheapest. And it omits the **OPC UA**
device layer, which you would add if PLC-driven hardware appears.
It is the strongest *starting* hardware stack, expandable toward
best-in-class.

## CDS toolkit (Empower Toolkit / Chromeleon SDK)

**What it is.** Commercial software development kits from the CDS
vendors. **Waters Empower Toolkit** lets your code create
sample-sets, launch acquisitions, and pull results in Empower;
**Thermo Chromeleon SDK** does the equivalent for Chromeleon. They
are the *supported* way to drive and exchange data with those
systems programmatically, rather than via files.

**How it's good.** For a lab already standardized on Empower or
Chromeleon — which is most regulated chromatography labs — this is
the deepest, most reliable, and most *defensible* integration:
live, transactional, vendor-supported, and already part of the
lab's validated environment. It removes the brittleness of file
hand-off and gives you real-time status and results inside the
system auditors already trust. Where it applies, nothing integrates
better.

**How it's bad (vs the other four).** It is **commercial and
vendor-locked** — licence cost, a vendor relationship, and code
that does not move from Empower to Chromeleon without a rewrite.
That is the opposite of the open, portable promise of **SiLA 2 /
OPC UA**, and far heavier than the free **FastAPI + SQLite** file
bridge. It also only solves the CDS link — you still need a
controller, a store, and instrument protocols around it. That is
why it is an *Alternative*: essential when a specific CDS is fixed,
overkill before that decision is made.

## PostgreSQL

**What it is.** A mature, open-source, transactional relational
database. Here it is the **validated, robust store** for the audit
trail and electronic records: append-only audit tables, user and
role controls, point-in-time recovery, replication, and backup —
the database substrate under a serious Part 11 record system.

**How it's good.** When records must be Attributable, Original,
Accurate, and Enduring (the ALCOA+ properties), PostgreSQL's
transactional guarantees, access control, and recoverability are
exactly what you want — and far beyond what **SQLite** offers for a
multi-user, audited deployment. It is free and open, so unlike the
**CDS toolkit** it adds no licence cost or vendor lock-in while
still being production-grade. It is the quiet workhorse inside both
the best-in-class and best-practical stacks.

**How it's bad (vs the other four).** On its own it is *only* a
store — no API, no UI, no instrument protocol, no CDS link — so it
never stands alone; it always pairs with **FastAPI** and the
protocol/CDS layers. Versus **SQLite** it is real infrastructure to
install, secure, back up, and qualify, which is overhead a tiny
pilot may not want. And a database alone does not make you Part 11
compliant — the controls *around* it (signatures, access, the
validation effort below) do. That is why it is an *Alternative*: a
critical ingredient, not a complete answer.

## What hardware and production actually add

These cannot be simulated and must be planned and funded as real
work, not coded away:

- **Real 21 CFR Part 11 electronic records and signatures.** Bound,
  attributable, non-repudiable signatures on real records — with
  access control, signature meaning, and record retention —
  assessed against the actual rule, not a hash chain alone.
- **ALCOA+ data integrity in practice.** Proving records stay
  Attributable, Contemporaneous, Original, Accurate, and Enduring
  across real instruments, the CDS, and the audit store.
- **IQ/OQ/PQ + CSV validation.** Documented qualification that the
  installed system operates and performs as intended. **This is a
  funded effort** — quality, documentation, and test execution —
  that no simulation removes. Budget it explicitly.

> Re-verify: every compliance statement here is general and
> context-dependent. None of these tools is a certified Part 11 /
> ALCOA+ solution by itself; your specific obligations,
> interpretations, and validation scope must be confirmed with a
> qualified quality/compliance owner before any regulated use.

## Verdict

- **Best-in-class — SiLA 2 / OPC UA + a validated CDS toolkit +
  PostgreSQL.** Standards to instruments and devices, the vendor
  CDS toolkit for chromatography, and a robust validatable store:
  the complete, defensible, integrated stack. Most expensive and
  slowest, and the real moat.
- **Cheapest — FastAPI + SQLite + CSV/file hand-off to the CDS.**
  The smallest real integration that still gets results into the
  CDS, with no SDK licence and minimal new parts to qualify.
  Brittle and not multi-user, but a legitimate pilot bridge.
- **Best-practical — FastAPI + PostgreSQL + SiLA 2.** Build the two
  hardest-to-retrofit pieces — a validatable store and
  standards-based instrument control — correctly now, and defer the
  commercial CDS SDK until the lab's CDS and budget are settled.

Keep the v1 "keep it simple" framing on the *tech*, but not on
compliance: the IQ/OQ/PQ + CSV validation effort is real, funded
work, and this layer — not the arm — is where the product's
defensibility lives.

## See also

- Folder overview: [`README.md`](README.md)
- Sibling mode (pure software):
  [`../01-only-code/08-software-worklist-and-compliance.md`](../01-only-code/08-software-worklist-and-compliance.md)
