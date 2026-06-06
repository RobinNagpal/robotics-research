# Part 10 — Hardware platform & capital model

> **Problem:** The physical cell has to be precise enough to seat a
> 2 mL vial in a slot, safe enough to sit in a lab, and priced so a
> lab that already buys $50–150K+ instruments sees it as ordinary
> instrument-grade capital — not an exotic robotics splurge.

## The problem

This is a **pure-arm** system: a single fixed-mount robotic arm with
a gripper is the entire robot — there is **no mobile base**. The arm
sits on a bench and reaches a small set of fixed stations (vial
store, decapper, dispenser, tray). Two questions decide the
hardware:

- **What physical platform** — arm, gripper/tooling, bench layout,
  enclosure, and safety scheme — actually does the job reliably and
  fits a lab?
- **What is the business model** — how do we price it, what is the
  return on investment (ROI) for the buyer, and how do we compare to
  the fixed liquid-handling robots labs already know?

The platform constraints come straight from the task. Vials are
small (2 mL); tray slots have only millimetres of clearance (see
`05-tray-loading-and-positioning.md`); decapping and pipetting need
different tools. So the arm must be **precise**, **light-payload**,
and able to **swap tools**, inside an enclosure that contains
solvents and protects people.

## The solution

**The arm.** A **6-DoF bench cobot** ("6-DoF" = six degrees of
freedom, i.e. it can reach a position *and* any orientation;
"cobot" = collaborative robot, designed to work safely near people
with built-in force limiting). Requirements:

- **Reach** ~500–850 mm — enough to cover the bench stations from a
  fixed base.
- **Payload** light — a vial plus gripper is well under a kilogram.
- **Repeatability** ~0.05–0.1 mm — this is the number that matters,
  because it sets whether the arm can reliably hit a tight slot.

Candidate arms: **Universal Robots UR3e / UR5e** (the de-facto cobot
standard, large ecosystem), **Franka** (research-friendly, sensitive
force control), or a **precision/SCARA-style arm** where tighter
repeatability is needed.

**Gripper + tool changer.** A **tool changer** is a quick-swap
coupling on the wrist that lets the arm drop one tool and pick up
another mid-task — so the same arm can carry a **vial gripper**, a
**decapper** (see `03-decapping-and-capping.md`), and/or a
**pipetting tool** (see `04-liquid-handling-and-sample-prep.md`)
without a human changing end-effectors.

**Bench layout.** Fixed **nests/jigs** — precisely located holders —
for each station (vial store, decapping station, dispenser, tray).
Fixed locations let us calibrate once and trust the geometry.

**Enclosure.** A guarded housing that provides: **safety guarding**
(keeps hands out of the work zone), **solvent/fume containment**
(HPLC uses volatile solvents — methanol, acetonitrile — that need
extraction or containment), and **spill management** (a contained,
wipeable tray under the cell).

**Safety scheme** — two broad options:

| Scheme | How it works | Pros | Cons | Bottom line |
|---|---|---|---|---|
| **Collaborative (speed/force limits)** | Cobot's built-in limits stop it on contact; can run open or lightly guarded | Smaller footprint, easy access, simpler install | Slower; force limits can constrain throughput; solvent containment still needed | Good default for v1 in a supervised lab |
| **Guarded cell with interlocks** | Full enclosure; door **interlocks** (door open = motion stops) let the arm run faster inside | Faster motion, cleaner containment, easier to validate as a unit | Larger footprint, more cost, less casual access | Better for production throughput and qualification |

**Recommended:** start **collaborative + light guarding** for v1;
move toward a **guarded, interlocked, contained cell** for
production, because it both raises throughput and is easier to
qualify (the validation discussion in
`09-software-compliance-and-integration.md` directly drives this —
a cell you can put a boundary around is a cell you can IQ/OQ/PQ).

### Tiered hardware options

| Tier | Build | Approx. hardware cost* | Bottom line |
|---|---|---|---|
| **Best-in-class** | Precision arm or UR5e + tool changer + multi-tool set + full enclosure with fume extraction + force/torque sensing | ~$120–250K+ | Highest throughput, fully contained, validation-ready |
| **Cheapest** | UR3e (or used cobot) + single fixed gripper + open bench + minimal guarding + manual reagent refill | ~$40–75K | Proves the loop cheaply; limited scope, supervised only |
| **Best value** | UR3e/UR5e + tool changer + 2-tool set + modest guarded enclosure + standard gripper | ~$75–150K | The sweet spot: flexible, safe enough, priced as instrument capital |

\*Rough estimates — hardware prices, cobot list prices, and
enclosure costs drift; **re-verify with current vendor quotes**
before quoting a customer.

### Capital & business model

HPLC instruments and lab automation already run **~$50–150K+**, so
labs are accustomed to budgeting **instrument-grade capital**. An
automation **cell add-on** can be priced the same way.

- **Price point:** **~$75–250K** depending on tier and tooling.
  *This is a rough placeholder to validate with real customer
  conversations and quotes — do not quote it as firm.*
- **Margin wedge:** because the buyer frames this against
  six-figure instruments (not against a cheap robot arm), there is
  room for healthy margin on a well-integrated, compliant cell.

**ROI story for the buyer:**

- **Lab-tech hours saved** — vial prep and tray loading is tedious
  manual work; automating it frees skilled chemists for analysis.
- **Fewer prep errors / re-runs** — a mis-prepared or mis-placed
  vial means a wasted, costly HPLC run; consistency cuts that.
- **Higher throughput & walk-away time** — the cell can prep and
  load **overnight/unattended**, adding capacity without adding
  staff.

**Simple ROI sketch** (illustrative — plug in real local numbers):

```
Say a tech spends ~2 hr/day on vial prep + loading.
At a loaded labour cost of ~$50/hr  ->  ~$100/day  ->  ~$25K/yr.
Add avoided re-runs (each wasted run = solvent + column +
instrument time + analyst time) and overnight throughput gains.
A ~$100K cell then targets payback in roughly ~2–4 years on
labour alone, faster once re-runs and added capacity count.
```

> All ROI figures are illustrative and must be re-verified with the
> customer's own labour rates, run costs, and volumes.

**Versus fixed liquid-handling robots** (e.g. **Hamilton**,
**Tecan**, **Opentrons** — established automated pipetting/
liquid-handling platforms):

| Aspect | Fixed liquid handlers | Our arm-based cell | Bottom line |
|---|---|---|---|
| **Throughput** | Very high for their fixed workflow | Lower per-hour | They win on raw volume |
| **Flexibility / reconfigurability** | Locked to deck layout & pipetting | One arm, swappable tools, re-teachable stations; handles decapping, transport, *and* loading | We win on adaptability |
| **Footprint** | Often large deck | Compact bench cell | Comparable / ours can be smaller |
| **Best fit** | High-volume, fixed assay | Mixed, lower-volume, "front-end of HPLC" prep + loading | Different niches |

Our wedge is **flexibility**: a fixed liquid handler pipettes fast
but cannot pick up a vial, decap it, and seat it in an autosampler
tray. The arm does the whole front-end loop and can be reconfigured
when the workflow changes.

## v1 vs later

**v1 (keep it simple):**

- **Off-the-shelf cobot** (e.g. UR3e/UR5e) — no custom arm.
- **Standard single gripper** — no tool changer yet.
- **Simple bench** with fixed nests, light guarding.
- **Manual reagent refill** — a human tops up solvents/reagents.
- Supervised operation.

**Defer to later:**

- **Tool changer + multi-tool set** (gripper + decapper +
  pipettor).
- **Full enclosure** with fume extraction and spill containment.
- **Guarded, interlocked cell** for higher-speed, validatable
  production.
- **Force/torque sensing** for the tightest insertions.
- Automated reagent supply and tray exchange.

## How it connects

- `02-vial-handling-and-gripping.md` — the gripper this platform
  carries; payload and precision here serve that grip.
- `03-decapping-and-capping.md` — the decapper is one of the tools
  the tool changer swaps in.
- `04-liquid-handling-and-sample-prep.md` — the dispenser/pipetting
  tool integrates onto this same arm.
- `09-software-compliance-and-integration.md` — validation and
  containment requirements drive the enclosure, safety scheme, and
  layout chosen here.
- Back to the overview: `README.md`.
