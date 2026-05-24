# Perception projects you can build and sell

Three projects, ordered simple → complex, each scoped to **3-6 weeks**
and each demo-able to a real customer. Build them in order: each one
teaches a layer of perception you'll reuse in the next.

| # | Project | Timeline | Core idea | Difficulty |
|---|---------|----------|-----------|------------|
| [01](01-visual-inspection.md) | Visual defect inspection service | 3-4 weeks | 2D anomaly detection — image in, good/bad out | Simple |
| [02](02-pose-estimation-api.md) | 6-DoF pose-estimation API | 4-5 weeks | 3D pose from RGB-D + a CAD model | Medium |
| [03](03-phone-scan-digital-twin.md) | Phone-scan to robot-ready 3D twin | 5-6 weeks | Full 3D reconstruction pipeline → USD/URDF | Complex |

Each project file has the same three sections: **Problem Statement**,
**Why this is unique, demo-able, and sellable**, and **Technologies to
learn to get started**.

The complexity ramp is deliberate: Project 1 is a flat 2D image
problem, Project 2 adds depth sensors and 3D pose, Project 3 is a full
multi-stage 3D pipeline. Skills compound — RGB-D and intrinsics from
#2 feed directly into #3.

Cross-references: `../00-basics.md` for vocabulary, `../01-examples.md`
for code snippets, `../02-learn.md` for the curriculum, `../03-start.md`
for the zero-to-first-commit ramp, `../04-market.md` for who is buying.

---

## How to scope a discovery phase

Before committing to any of the three builds, sell a short, fixed-fee
discovery phase. It de-risks both sides.

- **Duration:** 1-2 weeks, never longer.
- **Price:** $2-5k flat, paid up front.
- **Deliverable 1:** a 5-10 page written assessment — what they
  actually need, what's realistically possible, honest
  accuracy/latency/cost numbers.
- **Deliverable 2:** a working proof-of-concept notebook that runs
  end-to-end on a sample of *their* data — proof the hard parts aren't
  show-stoppers, not production code.
- **Deliverable 3:** a fixed-fee quote for the full build with three
  scope options (minimum / recommended / all the bells), each with a
  price, timeline, and explicit out-of-scope list.

About a third of customers will read the assessment and decline — the
best possible outcome, since they keep the value and you keep the cash
and a case study without sinking weeks into a doomed build. Insisting
on discovery first is also what signals "consultancy" rather than
"freelancer."

---

## Pricing principles

1. **Charge per outcome, not per hour.** Customers pay to transfer
   risk to you; per-hour caps your upside.
2. **Always sell discovery before quoting a build** — especially to
   impatient customers, who tend to have the expectations that blow up
   fixed-fee margins.
3. **Line-item recurring revenue separately from setup.** Customers
   accept clearly named recurring fees ("re-training subscription,"
   "support retainer") but resent fees buried in setup.
4. **Anchor against the incumbents** — Cognex, Keyence, Matterport,
   Polycam. Hedge ("comparable industrial vision starts in the
   $40-80k range") rather than quoting unpublished competitor numbers.
5. **Raise prices 25% every 3 paying customers.** Confidence lags
   reality; this corrects it.

Rough pricing per project: #1 visual inspection $5-25k setup +
$200-1000/mo; #2 pose API $2-10k per part + a flat monthly plan; #3
digital twin $1-5k per scene or a $500/mo subscription.

---

## Sample contract clauses to insist on

Not legal advice — pay a lawyer $500-1500 for a template. These are
the perception-specific clauses a generic services contract misses:

- **Generic code IP stays with you.** Base Docker image, FastAPI
  scaffolding, React UI, evaluation harness — yours, reusable;
  customer gets a non-exclusive license.
- **Per-customer fine-tuned weights belong to the customer.** Pose
  models on their CAD, anomaly detectors on their defects — theirs,
  transferable, deletable on request.
- **Customer data stays customer data; you keep anonymized aggregate
  metrics** (latency, failure-mode frequency).
- **Force-majeure for upstream model breakage.** If Meta restricts
  SAM 2 or NVIDIA changes the FoundationPose license, you're not in
  breach; commit to a best-effort replacement within 60 days.
- **Liability capped at fees paid in the last 12 months.** Without it,
  one bin-picking failure that damages a robot arm ends the agency.

---

## Tooling stack for the agency

- **Billing:** Stripe + Stripe Tax (handles VAT/GST/US sales tax).
- **Project management:** Linear. **Async demos:** Loom.
- **Client wikis:** Notion or Obsidian Publish, one workspace per
  customer (architecture, calibration files, checkpoints, changelog).
- **Legal/banking:** one LLC, one bank account, one bookkeeping system
  from day one (Mercury, Wise Business, or local equivalent).
- **Insurance:** professional liability / E&O ($50-200/mo) — larger
  customers require proof before signing.
- **Ops glue:** Sentry for the FastAPI services; Tailscale for
  accessing customer hardware (with written permission); Cal.com for
  booking.

---

## Which one to start with

- **Fastest to revenue, lowest risk:** #1 (visual inspection). Pure
  software, huge customer pool, short cycle, laptop demo.
- **Most defensible long-term:** #2 (pose API). Each customer's
  fine-tuned model and accuracy benchmarks become your moat.
- **Highest ceiling:** #3 (digital twin). The kind of product an
  NVIDIA / Matterport / Polycam might one day acquire.

A sensible path: ship #1 first to get a paying customer and a case
study, use that revenue and credibility to land #2, and only attempt
#3 once you're comfortable with depth sensors and 3D from the first
two.
