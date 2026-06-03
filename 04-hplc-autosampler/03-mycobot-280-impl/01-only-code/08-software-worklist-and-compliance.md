# Layer 08 — Software, worklist & compliance (only-code)

> **Job:** In pure-software mode, ingest the worklist, drive the
> cell, and keep a tamper-evident record of everything that
> happened — all of it running identically in simulation, with no
> real lab system attached.

A quick vocabulary check before the comparison, because the rest of
this page leans on these terms (see also `../02-glossary.md` style
plain-language definitions):

- **Worklist** — the to-do list the lab hands the cell: which
  vials, which samples, in what order, with what prep steps. It is
  the input to everything else here.
- **LIMS (Laboratory Information Management System)** — the lab's
  database of samples, tests, and results. It usually *issues* the
  worklist and expects results back.
- **CDS (Chromatography Data System)** — the software that runs the
  HPLC instrument and stores its chromatograms (e.g. Waters
  Empower, Thermo Chromeleon). The autosampler tray ultimately
  feeds it.
- **SiLA 2 (Standardization in Lab Automation, version 2)** — an
  open standard for talking to lab instruments over the network
  using well-defined "features." Vendor-neutral, modern.
- **OPC UA (Open Platform Communications Unified Architecture)** —
  an industrial machine-to-machine protocol common on PLCs
  (programmable logic controllers) and factory devices.
- **21 CFR Part 11** — the US FDA rule on electronic records and
  electronic signatures: it says when an electronic record can
  legally replace paper, and what controls (audit trail, access
  control, signatures) you need.
- **Audit trail** — an immutable, time-stamped log of who did what,
  when, and (ideally) why. The backbone of regulated software.

Crucially, **this layer is almost entirely software**, so it runs
the same whether the arm is real or simulated. That is why you can
build roughly **~90% of it now**, in only-code mode, against mocked
instruments — and carry it over to hardware nearly unchanged. The
sibling file covers what the remaining ~10% (real instruments, real
validation) adds.

## The five at a glance

| Framework | Role | Tier | One-liner |
|-----------|------|------|-----------|
| **SiLA 2 (sila_python)** + PostgreSQL/asyncua | Standards-based instrument + data stack | Best-in-class | Vendor-neutral instrument standard over a robust store; the long-term moat. |
| **FastAPI + SQLite + hash-chained JSONL audit** | Controller, store, append-only log | Cheapest | One Python process gives you an API, a worklist store, and a tamper-evident trail. |
| **FastAPI + SQLite + SiLA 2 mock** | Controller over a mocked instrument | Best-practical | Build the real control flow now against a SiLA 2 stub you swap for hardware later. |
| **OPC UA (asyncua)** — mocked | Device/PLC protocol | Alternative | Industrial protocol you can mock now to rehearse PLC-style device talk. |
| **Node-RED / Prefect** | Visual or code workflow engine | Alternative | A workflow tool to sequence prep steps without hand-rolling orchestration. |

Tier note: the named slots are about *the shape of the stack you
commit to*, not single tools. Best-in-class is the standards-based
combination you would validate for production; cheapest is the
smallest thing that still keeps a defensible audit trail; and
best-practical is the middle path that builds the real flow now
against a swappable mock. The two Alternatives are pieces you can
fold into any of those.

## SiLA 2 (sila_python) + PostgreSQL/asyncua

**What it is.** SiLA 2 is an open, vendor-neutral standard for
controlling lab instruments over a network. Each instrument exposes
"features" (commands and properties) with a formal definition, so
your software talks to *any* SiLA-compliant device the same way.
`sila_python` is the reference Python implementation. Paired with
**PostgreSQL** (a mature, transactional relational database) as the
record store and **asyncua** (a Python OPC UA library) for any
PLC-style devices, this is the full standards-based stack. In
only-code mode you run SiLA *servers as mocks* — software stubs that
speak the real protocol but pretend to be a dispenser or a
decapper — so your controller code is already written against the
production interface.

**How it's good.** This is the only option here that builds toward
a genuine *moat*. Because SiLA 2 and OPC UA are recognized
standards, a cell built on them can integrate with instruments from
many vendors without bespoke glue, which is exactly what regulated
labs want to hear. PostgreSQL gives you transactional integrity,
concurrent access, and real backup/replication — properties an
audit trail in a regulated setting eventually needs. And because the
mock speaks the same protocol as the real device, the code you
debug in simulation is the code that ships. You are not throwing
away a prototype.

**How it's bad (vs the other four).** It is the heaviest to stand
up. Compared with the **FastAPI + SQLite** options, you are running
SiLA servers, a PostgreSQL instance, and protocol tooling before a
single vial moves — a lot of ceremony for an early milestone where
you only want to prove the loop. `sila_python`'s ecosystem is
smaller and changes faster than, say, FastAPI's, so expect more
reading of the spec and fewer ready answers. And versus a
**workflow tool** like Node-RED, there is no drag-and-drop: you
write the orchestration yourself. The payoff is real but deferred,
which is why this is the *target*, not the *starting point*.

## FastAPI + SQLite + hash-chained JSONL audit

**What it is.** FastAPI is a modern Python web framework for
building HTTP APIs (and, with templates, simple web pages — here,
the screens a reviewer uses to approve a run and apply an
electronic signature). SQLite is a tiny, file-based SQL database
that needs no server. The audit trail is a **hash-chained JSONL**
file: each event is one line of JSON, and each line includes a
cryptographic hash of the previous line, so any later edit or
deletion breaks the chain and is detectable. The worklist arrives
as a plain **CSV** file. This whole stack is one Python process and
two files.

**How it's good.** It is the cheapest, fastest path to a working,
*defensible* system. You get a controller API, a worklist store, a
review-and-e-sign UI, and a tamper-evident log with essentially no
infrastructure — no database server, no broker, no protocol stack.
The hash chain is a real integrity control: it gives you an
append-only, tamper-*evident* trail that is genuinely useful
evidence, which is far more than a plain log file offers. For a
solo developer proving the concept in sim, nothing here gets in
your way.

**How it's bad (vs the other four).** It is the least like
production. SQLite handles one writer at a time and has no built-in
user roles, replication, or point-in-time recovery, so it does not
scale to a multi-user validated deployment the way **PostgreSQL**
does. The CSV worklist and file hand-off are convenient but
non-standard — they will not interoperate with a real LIMS or
instrument the way **SiLA 2** or **OPC UA** would. And rolling your
own hash chain means *you* own the correctness of that integrity
control, with no third-party validation behind it. It is excellent
scaffolding and a weak final foundation.

> Re-verify: a hash-chained file is tamper-*evident*, not
> tamper-*proof*, and on its own it is **not** a certified 21 CFR
> Part 11 solution. Treat it as a strong starting control whose
> Part 11 sufficiency must be assessed with a quality/compliance
> owner before any regulated use.

## FastAPI + SQLite + SiLA 2 mock

**What it is.** This is the deliberate middle path: keep FastAPI as
the controller and the review/e-sign UI, keep SQLite as the easy
store, but talk to instruments through a **SiLA 2 mock** rather than
a CSV hand-off. The mock is a small SiLA server that answers the
same calls a real dispenser or decapper would, so your control flow
is written against the production-shaped interface from day one,
while the surrounding plumbing stays lightweight.

**How it's good.** It captures most of the upside of the
standards-based stack at a fraction of the setup cost. The part
that is *hard to change later* — how your controller commands
instruments — is built correctly now against SiLA 2, so the
hardware transition is mostly "swap the mock for the real server."
Meanwhile SQLite and FastAPI keep day-to-day development friction
near zero. This is the best balance of "builds the right thing" and
"builds it cheaply," which is why it is the practical pick for the
only-code phase.

**How it's bad (vs the other four).** It inherits SQLite's ceiling:
the store is still single-writer and unvalidated, so it is not the
production record system **PostgreSQL** is in the best-in-class
stack. It carries more weight than the pure **FastAPI + SQLite +
JSONL** option — you now run a SiLA mock and learn enough of the
spec to write a faithful one — so it is not the absolute cheapest.
And it stops short of the full standards stack: no OPC UA device
layer, no validated data store. It is the right amount of
investment for *this* phase, not the end state.

## OPC UA (asyncua) — mocked

**What it is.** OPC UA is an industrial protocol for talking to
machine controllers — PLCs, drives, sensors — common in factory and
process automation. `asyncua` is a pure-Python OPC UA library
(client and server). In only-code mode you stand up an OPC UA
*server mock* that exposes device variables (e.g. a decapper's
"capped/uncapped" state, a dispenser's "ready" flag) so your
controller can rehearse PLC-style interactions before any PLC
exists.

**How it's good.** Where parts of the cell are likely to be driven
by industrial controllers rather than lab-standard instruments, OPC
UA is the right vocabulary, and mocking it now means that
integration is rehearsed rather than discovered late. `asyncua` is
mature and well-documented, and like the SiLA mock it lets you
write against the production protocol from the start. It complements
SiLA 2: SiLA for lab instruments, OPC UA for machine-level devices.

**How it's bad (vs the other four).** For a benchtop myCobot cell,
much of the hardware may speak SiLA 2 or a vendor SDK rather than
OPC UA, so this can be solving a problem you do not have yet — that
is why it is an *Alternative*. Compared with **SiLA 2**, OPC UA is
less aligned with the lab-instrument world and its data model is
heavier to learn. And on its own it is only a protocol, not a
controller, store, or UI — you still need the **FastAPI** stack
around it. Mock it if PLC-driven devices are on your roadmap;
otherwise defer it.

## Node-RED / Prefect

**What it is.** These are workflow engines for sequencing the prep
steps (fetch vial → decap → dispense → recap → place on tray →
report). **Node-RED** is a visual, flow-based tool where you wire
nodes together in a browser. **Prefect** is a Python orchestration
framework for defining, scheduling, and observing task pipelines in
code. Either can sit above the controller and drive the ordered
steps of a worklist run.

**How it's good.** They save you from hand-rolling sequencing,
retries, and run visibility. Node-RED's visual flows make the
process legible to non-programmers — useful when a lab scientist
wants to see or tweak the steps. Prefect gives you code-defined
workflows with built-in retries, logging, and a dashboard, which is
handy once runs get long or need scheduling. Both shorten the path
from "I have a controller" to "I can run a whole worklist."

**How it's bad (vs the other four).** They add a moving part that
the lightweight options do without — for a strictly ordered,
mostly-linear prep loop, a plain state machine inside **FastAPI**
(or the Behavior-Tree orchestration discussed in layer 07) may be
simpler and easier to validate. In a regulated context, an extra
engine is an extra thing to qualify and keep in a controlled state,
which cuts against the **SiLA 2 / PostgreSQL** stack's goal of a
tight, auditable core. That is why it is an *Alternative*: helpful
for complex flows, unnecessary overhead for a simple one.

## Verdict

- **Best-in-class — SiLA 2 (sila_python) + PostgreSQL/asyncua in a
  validatable stack.** Standards-based instrument and device
  protocols over a robust transactional store: the combination a
  regulated lab can actually validate and the one that becomes a
  defensible moat. In only-code mode you run it all as mocks, so
  the production-shaped code is written from the start.
- **Cheapest — FastAPI + SQLite + hash-chained JSONL audit + CSV
  worklist.** One Python process and two files give you an API, a
  store, a review/e-sign UI, and a tamper-evident trail with
  near-zero infrastructure. Great scaffolding; not a production
  foundation.
- **Best-practical — FastAPI + SQLite + a SiLA 2 mock.** Build the
  real control flow now against the production interface, keep the
  surrounding plumbing light, and make the eventual hardware swap a
  matter of replacing the mock. Best balance of correctness and
  cost for the only-code phase.

Keep the v1 "keep it simple" framing: start from the cheapest
stack to prove the loop, move to the best-practical mock early so
the instrument interface is right, and treat the full standards
stack as the destination you grow into.

> Note: tooling maturity, licences, and especially **compliance
> claims drift and are context-specific**. Nothing on this page is
> a certified 21 CFR Part 11 solution by itself; re-verify all
> compliance and integrity claims with a quality owner before
> quoting them or relying on them.

## See also

- Folder overview: [`README.md`](README.md)
- Sibling mode (real hardware):
  [`../02-code-plus-hardware/08-software-worklist-and-compliance.md`](../02-code-plus-hardware/08-software-worklist-and-compliance.md)
