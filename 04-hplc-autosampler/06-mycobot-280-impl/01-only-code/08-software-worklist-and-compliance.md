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

## Realistic scenario & use cases

> **Why this matters for automation.** This layer is what makes the cell
> *trustable* rather than merely functional: it ingests the worklist,
> records who/what/when/why for every vial, takes electronic signatures,
> and hands the verified order to the instrument. Its automation value is
> turning the arm's actions into a **defensible record** — without it, a
> regulated lab can't use the cell at all, no matter how well it grips.

**The scenario.** An auditor reviews last night's run. The cell ingested
a 96-row worklist, but **vial 53 was quarantined** (barcode mismatch) and
**vial 61 flagged** (two grasp slips). Mid-run an operator **inserted 4
priority STAT samples**. The auditor must be able to see an **immutable,
tamper-evident** account of every action and decision per vial, an
**electronic signature** on the review and the disposition of the two bad
vials, the exact **load order sent to the HPLC**, and proof that the STAT
insert didn't corrupt any of it. The whole point of the cell rests on
being able to answer "prove it."

The layer must therefore serve several **distinct use cases**:

1. **Ingest and validate a worklist.** Read the worklist (CSV / LIMS /
   SiLA) and bind each row to a tray slot, sample ID, and method.
   - *How the solution handles it:* a FastAPI endpoint parses the worklist
     into validated **SQLite** rows; malformed or duplicate rows are
     rejected up front rather than discovered mid-run.

2. **Tamper-evident audit trail (ALCOA+).** Record every action and
   decision per vial so the record is *Original* and *Accurate*.
   - *How:* a **hash-chained JSONL** audit log — each entry hashes the
     previous one — so any after-the-fact edit breaks the chain and is
     detectable, which is exactly what the auditor checks.

3. **Electronic review and signature.** A reviewer approves results and
   dispositions the flagged vials under their own identity.
   - *How:* a review step captures **user, timestamp, and meaning of
     signature** on the record (the shape 21 CFR Part 11 expects — though
     certification is a quality-owner matter, per the note above).

4. **Instrument hand-off over a standard interface.** Pass the verified
   load order to the HPLC autosampler.
   - *How:* a **SiLA 2 mock** receives the final sequence in the
     only-code phase; because it is production-shaped, swapping in the
     real instrument later changes the backend, not the control flow.

5. **Mid-run worklist amendment.** Absorb the 4 STAT inserts without
   corrupting state or the trail.
   - *How:* the worklist is **append-only and versioned**; the amendment
     is itself an audited event, and orchestration (Layer 07) re-reads the
     new rows — so the history stays intact and explains itself.

**Where the pick flexes.** FastAPI + SQLite + a SiLA 2 mock
(best-practical) gives the real control flow and a tamper-evident trail at
near-zero infrastructure, covering all five use cases in only-code. The
move to a **validatable production stack** — full **SiLA 2 (sila_python)
over PostgreSQL/asyncua** — is the destination for use cases 2–4 once the
lab is validating for real; the cheapest CSV/JSONL stack is the scaffold
you start on.

## Deep dive: the three highest-value use cases

The five above all matter; these three carry the most weight for the
software, worklist & compliance layer — what makes the cell *trustable*.

## Tamper-evident audit trail (ALCOA+)

A lab assistant in a regulated lab documents everything as they go — every
weight, every dilution, every step, signed and dated in a notebook or
electronic record. That record is not paperwork for its own sake; it's the
evidence that the result can be trusted. This use case is the cell keeping
that record automatically and making it tamper-evident: every action it
takes is written into a chained log where any later alteration is
detectable.

The bigger experiment is the HPLC batch run under GMP, where a result is
only usable if its full history is provably unaltered. The instrument
produces a number, but the number means nothing without a trustworthy
account of how the sample that produced it was prepared. The audit trail
is what turns the cell's mechanical actions into that account — and
chaining the entries is what makes "provably unaltered" true rather than
assumed.

For the assistant, documentation is continuous — it accompanies
essentially every action, all day, every day. The cell writes an audit
entry for every step of every per-vial cycle, so the trail grows
constantly through a run; the verification (re-checking the chain) is run
whenever the record is reviewed or audited, which in a regulated lab is
routine.

- **The moment:** an auditor needs proof that the record of last night's
  run wasn't altered after the fact.
- **How, in depth:** every action and decision is appended to a
  **hash-chained JSONL** log where each entry hashes the previous one, so
  any edit or deletion breaks the chain and is detectable on verification.
- **Edge case it survives:** an attempt to quietly "fix" vial 53's record —
  the recomputed chain hash no longer matches, exposing the change rather
  than hiding it.
- **Walkthrough:** (1) on each action build a record; (2) hash it together
  with the previous entry's hash; (3) append it to the JSONL log; (4)
  re-verify the chain on read to detect any tampering.
- **In the scene:** every action the cell takes drops a sealed entry into a
  ledger, each one cryptographically knotted to the one before it. An
  auditor months later can tug on the chain and instantly see whether a
  single link was ever altered.
- **Why it's done this way:** in a regulated lab a result is only usable
  if its history is provably unaltered; a plain log can be quietly edited,
  so chaining each entry to the last is what turns the cell's record into
  evidence rather than mere notes.
- **In the full loop:** this records every step of every per-vial cycle
  from Layers 03–07 — each pick, scan, decision, and place becomes a
  chained entry, so this is the layer that makes the whole loop accountable
  after the fact.
- **Value:** the cell's actions become a defensible, *Original and Accurate*
  record — the precondition for a regulated lab using it at all.

### Meta code

This meta borrows the idea behind a blockchain, scaled down to a single
file: make every record depend cryptographically on the one before it, so
the whole history is locked together. The pipeline keeps a running "chain
head" — the hash of the most recent entry — starting from a fixed genesis
value when the log is empty.

To record an action, it builds an entry containing what happened
(timestamp, actor, action, payload) plus the current chain head as its
"previous" link. It then computes a SHA-256 hash over the canonical form
of that entry and appends both the entry and its hash as one line of the
log, advancing the chain head to the new hash.

Because each entry embeds the previous entry's hash, and each entry's own
hash covers its full content, the log is a tamper-evident chain: altering
any past entry changes its hash, which breaks the "previous" link of every
entry after it.

Verification walks the file from the start, recomputing each entry's hash
and checking that each entry's "previous" matches the prior line's hash;
the first mismatch pinpoints exactly where the record was altered. The log
in pseudocode:

```text
# keep the previous entry's hash (the chain head); start from a genesis hash
# to append an action:
#     entry = {ts, actor, action, payload, prev_hash}
#     entry_hash = sha256(canonical_json(entry))
#     write {entry, hash} as one JSONL line; advance the head to entry_hash
# to verify the log:
#     walk the lines; each entry.prev must equal the prior line's hash
#     recompute each entry's hash and compare -> any mismatch exposes the altered line
```

### Real code

An append-only, hash-chained audit log with a verifier. **Illustrative
teaching code** — re-verify before use; every line is commented.

```python
import json, hashlib, time                              # JSONL records, SHA-256 chaining, timestamps

GENESIS = "0" * 64                                      # the chain's starting "previous hash"


class AuditLog:                                         # an append-only, hash-chained audit trail
    def __init__(self, path="audit.jsonl"):            # one log file on disk
        self.path = path                               # where the JSONL lines live
        self.head = self._last_hash()                  # resume the chain from the last line's hash

    def _last_hash(self):                              # find the current chain head on startup
        head = GENESIS                                 # default if the file is empty / new
        try:                                           # the file may not exist yet
            with open(self.path) as fh:                # read every existing line...
                for line in fh:                        # ...keeping the last one's hash
                    head = json.loads(line)["hash"]    # the most recent entry hash = the head
        except FileNotFoundError:                      # first run, no file yet
            pass                                       # stay at GENESIS
        return head                                    # the hash the next entry will chain onto

    def append(self, actor, action, payload):          # record one action, tamper-evidently
        entry = {"ts": time.time(), "actor": actor,    # who / when...
                 "action": action, "payload": payload,  # ...what happened...
                 "prev": self.head}                    # ...linked to the previous entry
        digest = hashlib.sha256(                        # hash the canonical JSON of the entry
            json.dumps(entry, sort_keys=True).encode()).hexdigest()
        with open(self.path, "a") as fh:               # append one line (never rewrite history)
            fh.write(json.dumps({"entry": entry, "hash": digest}) + "\n")
        self.head = digest                             # advance the chain head

    def verify(self):                                  # re-derive the chain; (ok, bad_line_no)
        prev = GENESIS                                 # start from the genesis hash
        with open(self.path) as fh:                    # walk every line in order
            for n, line in enumerate(fh, 1):           # n = line number for error reporting
                rec = json.loads(line)                 # {"entry": ..., "hash": ...}
                if rec["entry"]["prev"] != prev:       # does this entry link to the previous one?
                    return False, n                    # no -> tampering at this line
                redo = hashlib.sha256(                 # recompute the entry's own hash
                    json.dumps(rec["entry"], sort_keys=True).encode()).hexdigest()
                if redo != rec["hash"]:                # was the entry's content altered?
                    return False, n                    # yes -> tampering at this line
                prev = rec["hash"]                     # advance to check the next link
        return True, None                              # the whole chain verifies
```

## Per-vial status tracking in the worklist store

A lab assistant keeps constant track of where each sample is in the
process — which ones are weighed, which are diluted, which are loaded —
usually by marking up the worklist or updating the LIMS as they go. That
running status is how anyone can tell, at a glance, what's done and what's
left. This use case is the cell maintaining the same live status for every
vial in the worklist store: pending, prepared, placed, or quarantined,
updated the moment each step completes.

The bigger experiment is the HPLC batch, tracked vial by vial. The status
store is what the orchestration reads to know the next vial to work, and
what an operator (or a recovery on restart) consults to see the run's
state. It is the cell's live picture of the tray as it's built — distinct
from the immutable audit trail, which records *what happened*; this records
*where things stand now*.

The assistant updates a sample's status at every step — many times per
vial, all day. The cell writes a status update for every vial as it moves
through the loop — prepared, placed, or quarantined — so the store is
touched constantly, on the order of thousands of writes across an
overnight batch.

- **The moment:** a vial finishes a step (prepared, placed, or
  quarantined); the worklist store must reflect its new status
  immediately.
- **How, in depth:** orchestration updates the vial's row in the store
  (SQLite/LIMS) with its new status and a timestamp, so the current state
  of the tray is always queryable.
- **Edge case it survives:** a query mid-run — because the store is updated
  per step, an operator or a restart sees an accurate, up-to-the-moment
  picture rather than a stale one.
- **Walkthrough:** (1) a step completes for a vial; (2) update its status
  field (+timestamp) in the store; (3) orchestration reads the store to
  pick the next pending vial; (4) repeat to the end of the tray.
- **In the scene:** a live table of the tray fills in as the run proceeds
  — slot A1 "placed," A2 "placed," A3 "quarantined," the rest "pending" —
  refreshing vial by vial.
- **Why it's done this way:** a long, unattended run needs a single source
  of truth for "what's done"; updating per step keeps that picture
  accurate so the loop, operators, and any restart all agree.
- **In the full loop:** this is written on every per-vial step, so it's the
  running state every other layer's progress is recorded against.
- **Value:** the exact state of the tray is always known and queryable,
  vial by vial, throughout the run.

### Meta code

This meta keeps a mutable, queryable record of the tray's current state,
separate from the immutable audit log. Where the audit trail answers "what
happened, provably," this store answers "where does each vial stand right
now" — and it is updated in place as the run proceeds.

Each worklist row has a status field — pending, prepared, placed, or
quarantined — plus a timestamp of the last change. When orchestration
finishes a step for a vial, it writes the new status to that row. Because
the write is keyed by slot, the update is a simple, fast, indexed
operation.

Orchestration also reads the store to drive the loop: "the next vial to
work is the first one still pending." So the same store that records
progress also sequences the run, which keeps the two perfectly
consistent.

Because every status change is persisted immediately, any consumer — an
operator dashboard, a monitoring view, or a restart reconciling against
reality — sees an accurate, current picture rather than a guess. The store
in pseudocode:

```text
# the worklist store has one row per slot: {slot, sample_id, method, status, updated_at}
# status starts as "pending" for every row
# when orchestration finishes a step for a vial:
#     UPDATE the row's status (-> prepared / placed / quarantined) + updated_at = now
# to choose the next vial:
#     SELECT the first row WHERE status = 'pending'                 (drives the loop)
# any operator / dashboard / restart can SELECT to see the live tray state
```

### Real code

A small SQLite-backed status store that also sequences the loop.
**Illustrative teaching code** — re-verify before use; every line is
commented.

```python
import sqlite3, time                                    # the worklist store + change timestamps


class WorklistStore:                                    # live, queryable per-vial status of the tray
    def __init__(self, path="worklist.db"):             # one SQLite file
        self.db = sqlite3.connect(path)                 # open (or create) the store
        self.db.execute(                                # one row per tray slot...
            "CREATE TABLE IF NOT EXISTS vials ("        # ...if it doesn't exist yet
            "slot TEXT PRIMARY KEY, sample_id TEXT, method TEXT, "  # the worklist columns
            "status TEXT, updated_at REAL)")            # current status + when it changed
        self.db.commit()                                # persist the schema

    def load(self, rows):                               # seed the store from a worklist (all pending)
        for r in rows:                                  # one row per worklist entry
            self.db.execute(                            # insert it as pending...
                "INSERT OR REPLACE INTO vials VALUES (?,?,?,?,?)",
                (r["slot"], r["sample_id"], r["method"], "pending", time.time()))
        self.db.commit()                                # persist the seeded tray

    def set_status(self, slot, status):                 # update one vial's status (per step)
        self.db.execute(                                # write the new status + timestamp...
            "UPDATE vials SET status=?, updated_at=? WHERE slot=?",
            (status, time.time(), slot))                # keyed by slot (fast, indexed)
        self.db.commit()                                # persist immediately (always current)

    def next_pending(self):                             # the next vial the loop should work
        cur = self.db.execute(                          # the first row still pending...
            "SELECT slot FROM vials WHERE status='pending' ORDER BY slot LIMIT 1")
        row = cur.fetchone()                            # None when the tray is complete
        return row[0] if row else None                  # the slot to process next, or None

    def snapshot(self):                                 # the live tray state (dashboards / restart)
        return dict(self.db.execute(                    # {slot: status} for every vial
            "SELECT slot, status FROM vials").fetchall())
```

## Per-vial provenance & measurement capture

For every sample, a lab assistant records the actual numbers — the weight
they measured, the dilution they made, the volume dispensed, the ID they
read — because those values *are* the result's provenance: the proof of
how this specific sample was prepared. This use case is the cell capturing
the same per-vial measurements as structured data: the weight, dilution
factor, fill, scan ID, and timestamps, recorded for every vial as it's
processed.

The bigger experiment is the HPLC batch, whose every result must be
traceable to exactly how its sample was prepared. The instrument later
produces a number per vial; this captured provenance is what lets that
number be interpreted and trusted — and it's the data a reviewer signs off
and an auditor inspects. Capturing it per vial, as it happens, is what
makes the whole batch defensible.

The assistant records these numbers for every sample at every measuring
step — many values per vial, all day. The cell captures provenance on
every vial as it moves through prep, so the records accumulate
continuously — thousands of values across an overnight batch.

- **The moment:** a vial is weighed, diluted, dispensed, and scanned; each
  measured value must be captured against that vial as it happens.
- **How, in depth:** orchestration records a structured per-vial record
  (weight, dilution factor, fill, scan ID, timestamps) keyed by slot,
  building the provenance the result will later be interpreted against.
- **Edge case it survives:** a value captured but a later step failing —
  the partial record still exists, so a quarantined vial carries the
  provenance of what *was* done to it.
- **Walkthrough:** (1) at each measuring step, read the value; (2) write it
  into that vial's provenance record; (3) accumulate the full record as the
  vial is processed; (4) finalize it when the vial is placed or
  quarantined.
- **In the scene:** as each vial passes the balance, the dispenser, and
  the scanner, its little dossier fills in — 12.503 g, ×10 dilution,
  1.4 mL, "ABC-123" — a complete account of its preparation.
- **Why it's done this way:** a result is only interpretable with its
  provenance, and provenance can't be reconstructed after the fact;
  capturing each value the moment it's measured is what makes the batch
  traceable and defensible.
- **In the full loop:** this is captured at every measuring step of every
  vial, building the data the review/sign and the instrument hand-off
  later rely on.
- **Value:** every result traces back to exactly how its vial was prepared,
  because the provenance was captured per vial, as it happened.

### Meta code

This meta accumulates a structured record per vial as it moves through the
prep steps, so that by the time a vial is placed, its full provenance —
every value measured for it — exists as one object. The record is keyed by
slot, the same key the status store and audit trail use, so the three line
up.

At each measuring step, orchestration writes the relevant value into that
vial's record: the weighed mass at the balance, the dilution factor and
dispensed volume at the dispenser, the measured fill from perception, the
decoded ID at the scanner — each with the time it was taken.

The record grows incrementally rather than being assembled at the end,
which matters for two reasons: a vial that fails partway still carries the
provenance of what was done to it, and the data is captured at the moment
it's true rather than reconstructed (which a regulated record forbids).

When the vial is placed or quarantined, its record is finalized and handed
to the review/sign step and, ultimately, paired with the instrument's
result. The capture in pseudocode:

```text
# each vial has a provenance record keyed by slot: {weights, dilution, fill, scan_id, timestamps}
# at each measuring step for a vial:
#     balance    -> record the weighed mass + time
#     dispenser  -> record the dilution factor + dispensed volume + time
#     perception -> record the measured fill + time
#     scanner    -> record the decoded ID + time
# the record grows incrementally (a failed vial keeps the partial provenance)
# on place / quarantine -> finalize the record -> review/sign + pair with the result
```

### Real code

A per-vial provenance recorder that finalizes one dossier per vial.
**Illustrative teaching code** — re-verify before use; every line is
commented.

```python
import json, time                                       # serialize records; timestamp each value


class ProvenanceBook:                                   # accumulates a per-vial preparation record
    def __init__(self, path="provenance.jsonl"):        # finalized records are appended here
        self.path = path                                # the file of completed vial dossiers
        self.open = {}                                  # slot -> the record being built

    def record(self, slot, key, value):                 # capture one measured value for a vial
        rec = self.open.setdefault(                      # start the dossier if this slot is new...
            slot, {"slot": slot, "events": []})         # ...with an empty list of measurements
        rec["events"].append({                          # append this measurement...
            "key": key, "value": value, "t": time.time()})  # ...with the time it was taken

    def weigh(self, slot, grams):                       # convenience: a balance reading
        self.record(slot, "mass_g", grams)              # store the weighed mass

    def dilute(self, slot, factor, volume_ml):          # convenience: a dispense step
        self.record(slot, "dilution", factor)           # store the dilution factor...
        self.record(slot, "dispensed_ml", volume_ml)    # ...and the dispensed volume

    def scan(self, slot, sample_id):                    # convenience: a barcode read
        self.record(slot, "scan_id", sample_id)         # store the decoded ID

    def finalize(self, slot, disposition):              # the vial is placed or quarantined
        rec = self.open.pop(                            # take its accumulated dossier...
            slot, {"slot": slot, "events": []})         # ...(empty if nothing was recorded)
        rec["disposition"] = disposition                # placed / quarantined
        with open(self.path, "a") as fh:                # append the finished record...
            fh.write(json.dumps(rec) + "\n")            # ...one JSON line per vial
        return rec                                      # the full provenance, ready for review/sign
```

## See also

- Folder overview: [`README.md`](README.md)
- Sibling mode (real hardware):
  [`../02-code-plus-hardware/08-software-worklist-and-compliance.md`](../02-code-plus-hardware/08-software-worklist-and-compliance.md)
- [`../foundation-models.md`](../foundation-models.md) — the compliance
  tension a VLA raises lives here: a **non-deterministic, black-box**
  policy is hard to validate under **21 CFR Part 11 / IQ-OQ-PQ**, and it
  adds **model-versioning / training-data audit** (MLOps) concerns.
