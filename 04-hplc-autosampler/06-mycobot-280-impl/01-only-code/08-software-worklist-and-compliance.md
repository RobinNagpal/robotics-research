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

The shape of the hash-chained log, before any library detail:

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

## Electronic review and signature

- **The moment:** before results are released, a reviewer must approve them
  and disposition the quarantined and flagged vials under their identity.
- **How, in depth:** the review step captures **user, timestamp, and the
  meaning of the signature** on the record — the shape 21 CFR Part 11
  expects — and locks the signed record against silent edits.
- **Edge case it survives:** a reviewer who is not the operator (segregation
  of duties) — distinct identities are recorded for prepare vs approve, so
  the trail shows who did what.
- **Walkthrough:** (1) present results for review; (2) capture the
  reviewer's identity, timestamp, and the meaning of the signature; (3)
  bind that signature to the record; (4) lock it against any silent edit.
- **In the scene:** a reviewer sits with the night's results, approves the
  good ones and dispositions the two flagged vials, and their name, the
  time, and the meaning of that approval are locked onto the record —
  accountability fused to the data itself.
- **Why it's done this way:** regulators require a named person to take
  responsibility for releasing results; capturing identity, time, and
  intent on the record — rather than in a side spreadsheet — is what makes
  that accountability auditable and tamper-resistant.
- **In the full loop:** this closes the loop after the run — once the tray
  is built and the per-vial records exist, a human reviews and signs, the
  gate between the cell's work and releasing results.
- **Value:** accountability is built into the data, not bolted on in a
  spreadsheet afterwards.

### Meta code

The shape of the e-signature, before any library detail:

```text
# present a result record for review (its data + any flags)
# capture the signature: {user, role, ts, meaning}   (e.g. "approved" / "rejected")
# enforce segregation of duties: signer.user != record.operator
# bind it: hash(record + signature) -> proves the signature covers THIS exact record
# write a SIGN event to the audit trail; the signed record is now locked by the chain
```

### Real code

A 21 CFR Part 11-shaped signing helper with a segregation-of-duties check.
**Illustrative teaching code** — compliance certification is a quality
owner's call; re-verify before use; every line is commented.

```python
import hashlib, json, time                              # bind the signature by hash; timestamps


class SignatureError(Exception):                        # raised when a signature is not allowed
    pass                                                # e.g. the signer also prepared the batch


def sign(record, signer, meaning, audit):               # apply an e-signature to a result record
    if signer["user"] == record.get("operator"):        # segregation of duties: signer != operator
        raise SignatureError("signer also prepared the batch")  # a different person must approve
    sig = {"user": signer["user"],                      # WHO is signing...
           "role": signer["role"],                      # ...in what role...
           "ts": time.time(),                           # ...WHEN...
           "meaning": meaning}                          # ...and the MEANING (approved / rejected)
    sig["binds_to"] = hashlib.sha256(                   # bind the signature to THIS exact record:
        json.dumps({"record": record, "sig": sig},      # hash the record + the signature together
                   sort_keys=True).encode()).hexdigest()  # the tie that locks them as a pair
    audit.append(signer["user"], "SIGN", {              # write the signing event to the audit trail
        "record_id": record["id"],                      # which record was signed...
        "meaning": meaning,                             # ...with what meaning...
        "binds_to": sig["binds_to"]})                   # ...and the binding hash (now chain-locked)
    return sig                                          # the signature to store on the record
```

## Instrument hand-off over a standard interface

- **The moment:** the verified load order must reach the HPLC autosampler —
  today against a mock, tomorrow against the real instrument.
- **How, in depth:** a **SiLA 2** mock receives the final sequence in
  only-code; because it speaks the production interface, swapping in the
  real instrument later changes the backend, not the control flow above.
- **Edge case it survives:** an instrument that rejects or re-orders a row —
  the SiLA reply is checked, so a refused load surfaces as an error the
  cell handles instead of a silent mismatch between tray and sequence.
- **Walkthrough:** (1) assemble the verified load order; (2) send it over
  the SiLA 2 interface (a mock now); (3) check the instrument's reply; (4)
  on a rejection surface an error instead of a silent tray/sequence
  mismatch.
- **In the scene:** the finished, verified load order is handed across to
  the HPLC over a standard interface; the instrument acknowledges, and the
  cell checks that acknowledgement rather than blindly assuming the tray
  and the sequence agree.
- **Why it's done this way:** the cell's output only matters if the
  instrument actually runs the right sequence, and integration is where
  deployments usually stall; building against the real SiLA 2 interface
  from day one, and checking the instrument's reply, is what de-risks that
  last mile.
- **In the full loop:** this is the loop's final output step — after the
  tray is loaded and verified, the load order goes to the instrument over
  SiLA 2, connecting the cell's prep loop to the HPLC's own injection
  sequence.
- **Value:** the integration that usually blocks deployment is designed and
  proven before the instrument is even connected.

### Meta code

The shape of the SiLA 2 hand-off, before any library detail:

```text
# assemble the verified load order: ordered [{slot, sample_id, method}]
# send it to the instrument's SiLA 2 "LoadSequence" command (mock now, real gRPC later)
# read the reply:
#     ACCEPTED            -> return the instrument's sequence id (tray + instrument agree)
#     REJECTED/REORDERED  -> raise an error the cell handles (never assume success)
```

### Real code

A SiLA 2-shaped autosampler client with a swappable mock/real backend.
**Illustrative teaching code** — re-verify before use; every line is
commented.

```python
from dataclasses import dataclass                       # a tidy value type for each load row
from typing import List, Optional                       # type hints for the sequence + channel


class LoadRejected(Exception):                          # the instrument refused the sequence
    pass                                                # the cell handles this, never ignores it


@dataclass
class Row:                                              # one autosampler position to load
    slot: str                                          # the tray slot, e.g. "A3"
    sample_id: str                                     # the sample that belongs there
    method: str                                        # the HPLC method to run on it


class SilaAutosampler:                                 # SiLA 2-shaped client (mock backend now)
    def __init__(self, channel: Optional[object] = None):  # 'channel' is a gRPC channel on hardware
        self._channel = channel                        # None -> use the in-process mock below

    def load_sequence(self, rows: List[Row]) -> str:   # the SiLA 2 "LoadSequence" command
        slots = [r.slot for r in rows]                 # the slots we ask the instrument to expect
        reply = self._call_load(slots)                 # send to the instrument, get its reply
        if reply["status"] != "ACCEPTED":              # did the instrument accept the order?
            raise LoadRejected(reply)                  # no -> surface it; don't assume success
        return reply["sequence_id"]                    # the instrument's id for this run

    def _call_load(self, slots):                       # the swappable backend (mock vs real gRPC)
        if self._channel is None:                      # only-code: a deterministic mock...
            return {"status": "ACCEPTED",              # ...that mimics a healthy instrument
                    "sequence_id": "SEQ-0001"}
        stub = self._channel.LoadSequence              # real hardware: the generated SiLA stub
        return stub(slots)                             # call the real instrument over gRPC
```

## See also

- Folder overview: [`README.md`](README.md)
- Sibling mode (real hardware):
  [`../02-code-plus-hardware/08-software-worklist-and-compliance.md`](../02-code-plus-hardware/08-software-worklist-and-compliance.md)
- [`../foundation-models.md`](../foundation-models.md) — the compliance
  tension a VLA raises lives here: a **non-deterministic, black-box**
  policy is hard to validate under **21 CFR Part 11 / IQ-OQ-PQ**, and it
  adds **model-versioning / training-data audit** (MLOps) concerns.
