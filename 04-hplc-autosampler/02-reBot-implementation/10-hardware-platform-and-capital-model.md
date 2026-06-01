# Part 10 — Hardware platform & capital model (simulation)

> **Sim goal:** Use the **digital twin** — the Gazebo cell built
> across Parts 01–09 — to **de-risk the hardware and business
> decision before spending a dollar**: compare arms, prove the tool
> changer, measure cycle time, and lay out the bench, all as
> swappable models.

This mirrors the high-level
[`../01-high-level-solution/10-hardware-platform-and-capital-model.md`](../01-high-level-solution/10-hardware-platform-and-capital-model.md).
New robotics terms are defined in
[`../../03-place-items-on-shelf/02-glossary.md`](../../03-place-items-on-shelf/02-glossary.md).

## What we can prove in simulation

The whole point of a **simulation-first** programme is that the most
expensive, hardest-to-reverse decision — *which arm and cell to buy*
— can be rehearsed in software. Because every layer above (motion,
perception, orchestration, the controller) talks to the arm through
standard ROS 2 interfaces, you can **swap the arm model and re-run
the same batch**, and most of the stack does not notice.

Four experiments the twin lets you run now:

**(a) Platform comparison — swap arm URDFs in the SAME world.** A
**URDF** (Unified Robot Description Format) is the file that
describes a robot's links, joints, limits, and meshes. Drop a
different arm's URDF into the identical Gazebo bench and re-run:

- **reBot Arm B601-DM** — open URDF + `rebotarm_ros2` workspace, our
  baseline (GitHub `Seeed-Projects/reBot-DevArm`).
- **UR3e / UR5e** — from `Universal_Robots_ROS2_Description`; the
  de-facto cobot standard, large ecosystem.
- **Franka** — from `franka_description`; research-friendly, sensitive
  force control.

For each, measure **reach** (can it cover every station from a fixed
base?), **collision-free access** to all stations (vial store,
decapper, dispenser, tray), and where joint limits or self-collision
block a slot. This tells you the *geometric* fit before any quote.

**(b) Tool changer — attach/detach end-effector models.** Simulate
the wrist swapping among a **vial gripper**, a **decapper** (Part 03),
and a **pipetting tool** (Part 04) by attaching/detaching the matching
end-effector model in sim. Proves the multi-tool choreography and
that each tool can still reach its station.

**(c) Cycle time — seconds per vial.** Time a full Behavior Tree run
(Part 08) in sim to get **simulated seconds-per-vial**, which feeds
the ROI model directly. Compare arms and layouts on this number.

**(d) Layout / enclosure / safety zones.** Lay out the bench,
station nests, and guarding as models; check reachability and that
the planned motions stay inside the intended **safety zones**.

**Honest limits (need real hardware/vendors):**

- **Real repeatability** (~0.05–0.1 mm class) — sim joints are
  perfect; the real number must come from the vendor datasheet and
  bring-up. This is the spec that decides whether the arm can hit a
  tight slot.
- **Real payload, reach edges, and tool-changer mechanics** —
  confirm with hardware.
- **Real cost** — every figure below is a placeholder for vendor
  quotes.
- **Validation** — IQ/OQ/PQ and CSV (see Part 09) are a funded
  hardware/process effort, not a sim output.

So sim de-risks the **choice** and supplies **numbers** (geometry,
cycle time, reach) for the business case; it does not finally settle
repeatability, payload, cost, or validation.

## Open-source tools

| Tool | Role | Bottom line |
|------|------|-------------|
| **Gazebo Harmonic** | The single shared world the bench, stations, and *any* arm model load into | Swap the arm, keep the cell — the comparison rig |
| **reBot URDF** (`rebotarm_ros2`) | Baseline arm model + ROS 2 workspace | Our default platform under test |
| **`Universal_Robots_ROS2_Description`** | UR3e / UR5e URDFs for comparison | Drop-in alternative arm, large ecosystem |
| **`franka_description`** | Franka URDF for comparison | Drop-in alternative, force-control reference |
| **MoveIt 2** | Plans against each arm (config generated from its URDF); reports reach/collision per station | Owns "can this arm reach every station cleanly?" |
| **`ros2_control` + `gz_ros2_control`** | Runs each arm's joint controllers in sim | Same interface for every candidate arm |
| **BehaviorTree.CPP** (+ Groot2) | Runs the full prep-and-load loop so you can **time** it | Source of the seconds-per-vial number |
| **RViz2 / Foxglove** | Visualise reach, tool swaps, layout, and safety zones | Eyeball fit and catch unreachable stations |

## How to simulate it now

**1. Build one canonical bench world.** Fix the station nests (vial
store, decapper, dispenser, tray) at known tf frames — the same world
Parts 02–08 already use. The arm is the only thing that changes.

**2. Run the platform-swap experiment.** For each of reBot, UR3e/UR5e,
and Franka:

- Load the arm's **URDF** at the bench mount point.
- Generate its **MoveIt 2** config from the URDF.
- Run a **reachability sweep**: ask MoveIt to plan to every station
  pose and every tray slot; record which it can reach collision-free
  and which it cannot.
- Record the verdict in a comparison table (reach, blocked slots,
  notes).

**3. Run the tool-changer experiment.** Script attach → use → detach
for the gripper, decapper, and pipetting tool; confirm each tool
reaches its station for the chosen arm(s).

**4. Run the cycle-time experiment.** Execute the full Behavior Tree
for a representative worklist and log **wall-clock simulated seconds
per vial** for each candidate arm and layout. Capture the numbers
that feed the ROI model.

**5. Lay out and check safety zones.** Model the enclosure/guarding;
confirm planned trajectories stay inside the intended zones and that
all stations remain reachable inside the guarding.

**Workflow:** one bench world → swap each arm URDF → reachability +
tool-swap + cycle-time runs → record (reach, blocked stations,
sec/vial, layout fit) → feed those numbers straight into the capital
story below.

## Capital & business model (hedged)

HPLC instruments and lab automation already run **~$50–150K+**, so
labs are accustomed to budgeting **instrument-grade capital**. An
arm-based prep-and-load cell can be priced the same way.

- **Rough price point:** **~$75–250K** depending on arm, tooling,
  enclosure, and safety scheme. *Placeholder — validate with real
  customer conversations and vendor quotes; do not quote as firm.*
- **Hardware cost tiers** (all `~`, **re-verify with current
  vendor quotes**):

| Tier | Build sketch | Approx. hardware | Bottom line |
|---|---|---|---|
| **Best-in-class** | Precision arm or UR5e + tool changer + multi-tool set + full enclosure + fume extraction + force/torque sensing | ~$120–250K+ | Highest throughput, contained, validation-ready |
| **Cheapest** | reBot or UR3e (or used cobot) + single fixed gripper + open bench + minimal guarding | ~$40–75K | Proves the loop cheaply; supervised, limited scope |
| **Best value** | reBot/UR3e/UR5e + tool changer + 2-tool set + modest guarded enclosure | ~$75–150K | Flexible, safe enough, priced as instrument capital |

**ROI for the buyer** (the cycle-time number from the sim feeds this):

- **Lab-tech hours saved** — vial prep and tray loading is tedious
  manual work; automating it frees skilled chemists for analysis.
- **Fewer prep errors / re-runs** — a mis-prepared or mis-placed vial
  wastes a costly HPLC run; consistency cuts that.
- **Throughput + walk-away time** — the cell can prep and load
  overnight/unattended, adding capacity without adding staff. The
  simulated **seconds-per-vial** turns directly into a throughput
  estimate here.

> All cost and ROI figures are illustrative and must be re-verified
> with the customer's own labour rates, run costs, and volumes, and
> with current vendor quotes.

**Versus fixed liquid handlers** (**Hamilton**, **Tecan**,
**Opentrons** — established automated pipetting platforms): they win
on raw pipetting throughput for a fixed deck, but they **cannot pick
up a vial, decap it, and seat it in an autosampler tray**. Our wedge
is **flexibility** — one arm, swappable tools, re-teachable stations,
doing the whole front-end loop and reconfigurable when the workflow
changes. The sim platform-swap is exactly how we demonstrate that
flexibility before committing to hardware.

## Additional hardware needed

This part **is** the eventual shopping list — in sim every item is an
interchangeable model.

| Real hardware | Why | How mocked in sim |
|---------------|-----|-------------------|
| **The chosen arm** | Does the whole job; the platform-swap picks it | Any of the candidate URDFs in the shared world |
| **Tool changer** | Lets one arm carry gripper/decapper/pipettor | Attach/detach of end-effector models |
| **End-effectors** (gripper, decapper, pipetting tool) | The actual tools | Separate models swapped per task |
| **Enclosure + safety guarding + spill/fume containment** | Contains volatile HPLC solvents, protects people | Static models; safety zones checked geometrically |
| **Qualified industrial PC** | Validatable host for the controller (Part 09) | Develop on any workstation; software identical |

**Honest note:** real **repeatability, payload, cost, and
validation** must be confirmed with vendors and hardware. The sim
narrows the field and supplies the geometry/timing numbers — it does
not replace the quote or the qualification.

## How it connects

- [`02-vial-handling-and-gripping.md`](02-vial-handling-and-gripping.md)
  — the gripper this platform carries; payload/precision serve that
  grip.
- [`03-decapping-and-capping.md`](03-decapping-and-capping.md)
  — the decapper is one of the tools the tool changer swaps in.
- [`04-liquid-handling-and-sample-prep.md`](04-liquid-handling-and-sample-prep.md)
  — the dispenser/pipetting tool integrates onto this same arm.
- [`08-orchestration-error-handling-and-safety.md`](08-orchestration-error-handling-and-safety.md)
  — the Behavior Tree run here is what we **time** for cycle-time /
  throughput.
- [`09-software-compliance-and-integration.md`](09-software-compliance-and-integration.md)
  — validation and containment requirements there **drive** the
  enclosure, safety scheme, and layout chosen here.
- Mirrors
  [`../01-high-level-solution/10-hardware-platform-and-capital-model.md`](../01-high-level-solution/10-hardware-platform-and-capital-model.md);
  back to the index: [`README.md`](README.md).
