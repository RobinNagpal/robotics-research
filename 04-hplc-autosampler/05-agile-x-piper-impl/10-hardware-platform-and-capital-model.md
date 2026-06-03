# Part 10 — Hardware platform & capital model (AgileX PiPER simulation)

> **Sim goal:** Use the **digital twin** — the Gazebo cell built across
> Parts 01–09 around the **AgileX PiPER** — to **de-risk the platform
> and business decision before spending real money**: compare arms in
> the same world, prove the tool changer, measure cycle time, and lay
> out the bench, all as swappable models. The crux question this doc
> answers: *is the cheap, mid-reach PiPER enough for the product, or
> does a validated production cell need an industrial cobot?*

This mirrors the high-level
[`../01-high-level-solution/10-hardware-platform-and-capital-model.md`](../01-high-level-solution/10-hardware-platform-and-capital-model.md).
New robotics terms are defined in
[`../../03-place-items-on-shelf/02-glossary.md`](../../03-place-items-on-shelf/02-glossary.md).

## What we can prove in simulation

The whole point of a **simulation-first** programme is that the most
expensive, hardest-to-reverse decision — *which arm and cell to buy* —
can be rehearsed in software. Because every layer above (motion,
perception, orchestration, the controller) talks to the arm through
standard ROS 2 interfaces, you can **swap the arm model and re-run the
same batch**, and most of the stack does not notice. The compliance
layer (Part 09) is fully arm-agnostic, so the *only* thing changing
between experiments is the arm's geometry and limits.

Four experiments the twin lets you run now:

**(a) Platform comparison — swap arm URDFs in the SAME world.** A
**URDF** (Unified Robot Description Format) is the file that describes a
robot's links, joints, limits, and meshes. Drop a different arm's URDF
into the identical Gazebo bench and re-run the same worklist:

- **AgileX PiPER** — open URDF + interfaces from `piper_ros`, driven in
  sim by `gz_ros2_control` + MoveIt 2; our low-cost baseline (~600 mm
  reach, ~1.5 kg payload — `~`, verify). Lightweight 6-DoF, also
  Hugging Face **LeRobot** compatible for later imitation learning.
- **myCobot 280 / 320** — open URDF + ready-made Gazebo + MoveIt config
  from `mycobot_ros` (280: ~280 mm reach, ~250 g payload; 320: ~500 mm,
  ~1 kg — `~`, verify); the sibling implementation's baselines.
- **reBot Arm** — open URDF + workspace (GitHub
  `Seeed-Projects/reBot-DevArm`); another sibling baseline.
- **UR3e / UR5e** — from `Universal_Robots_ROS2_Description`; the
  de-facto industrial cobot standard, large ecosystem, validated
  controllers and support.
- **Franka** — from `franka_description`; research-friendly, sensitive
  force control (optional reference point).

For each, measure **reach** (can it cover every station — vial store,
decapper, dispenser, tray — from a fixed bench base?), **repeatability**,
**payload**, and **collision-free access** to all stations, noting where
joint limits or self-collision block a station or slot. **The honest
expected finding: the PiPER hits a sweet spot of LOW COST + adequate
reach (~600 mm) and payload (~1.5 kg) for a strong proof-of-concept
(PoC)** — enough to cover a compact multi-station cell and carry a light
tool — *while a fully validated PRODUCTION cell may still favour an
industrial cobot (UR-class) for repeatability, support, and a mature
safety/validation story.* State this even-handedly: the PiPER is an
excellent simulated and bench PoC arm and may well be production-viable
for a small cell, but the twin lets you decide that on a reachability
map and a repeatability spec rather than on a hunch.

**(b) Tool changer — attach/detach end-effector models.** Simulate the
arm swapping tools at a parking dock: **gripper ↔ decapper ↔ pipetting
tool**. In sim a tool change is an **attach/detach** of an end-effector
model at the wrist flange, with the matching MoveIt end-effector config
loaded. This proves the *sequence and reachability* of tool changes
(does the arm reach the dock? does each tool clear neighbouring
stations?) without a real changer existing yet. The PiPER's ~1.5 kg
payload (`~`, verify) comfortably bounds a single light tool; a heavy
multi-tool turret is the kind of mass you would check here before
committing.

**(c) Cycle time — seconds per vial.** Run the full Behavior Tree (Part
08) over a batch in Gazebo and **measure simulated seconds per vial** end
to end (pick → decap → dispense → recap → place → verify). Repeat per
candidate arm. These numbers feed the throughput and ROI (Return On
Investment) case directly — and they are a fair *relative* comparison
even if absolute sim timing needs a real-hardware reality check.

**(d) Layout / enclosure as models.** Model the bench, station placement,
cable runs, and a notional **enclosure / safety zones** as collision
geometry. Check that every station is reachable, that the arm stays
inside its safety envelope, and that the cell footprint is plausible for
a lab bench. This de-risks the physical layout before any fabrication.

**Honest limits (need vendors / hardware to settle):** true reach,
payload, and repeatability under load; real tool-changer mechanics and
mass; absolute cycle time; and — critically — real **cost** and
**validation** (IQ/OQ/PQ, see Part 09). The twin ranks and de-risks the
options; it does not replace a vendor quote or a bench trial.

## Open-source tools

| Tool | Role | Bottom line |
|------|------|-------------|
| **Gazebo Harmonic** | Hosts the one bench world into which each arm URDF is swapped | The shared world that makes the comparison apples-to-apples |
| **`piper_ros`** | URDF + ROS 2 interfaces for the AgileX PiPER (our baseline) | Drives the PiPER twin via `gz_ros2_control`; same interface as the real arm |
| **`mycobot_ros` / Universal_Robots_ROS2_Description / franka_description / reBot URDF** | URDFs for the comparison arms (myCobot 280/320, UR3e/UR5e, Franka, reBot) | Drop-in alternatives in the same world |
| **MoveIt 2** | Reachability maps + collision-free planning per arm | Decides geometric fit before any quote |
| **`ros2_control` + `gz_ros2_control`** | Runs each arm's joint controllers in sim | Same control interface across all candidates |
| **BehaviorTree.CPP** (+ Groot2) | Runs the full prep-and-load loop to time it | Source of the cycle-time numbers |
| **Grasp-fix / attach-detach plugin** | Models tool-changer attach/detach of gripper/decapper/pipette | Proves tool-swap sequence with no real changer |
| **RViz2 / Foxglove** | Visualise reach maps, tool swaps, layout, safety zones | Eyeball each experiment and capture screenshots for the business case |

## How to simulate it now

**1. Run the platform-swap experiment.** Keep the bench, stations, and
worklist fixed. For each arm URDF (PiPER, myCobot 280/320, reBot,
UR3e/UR5e), load it into the world, build a **reachability map** over
every station and tray slot (loop IK + plan in MoveIt 2, colour
reachable / unreachable in RViz2), and record which stations/slots are
covered. Tabulate reach, payload, repeatability (from spec), and
coverage per arm.

**2. Run the tool-changer experiment.** Add a parking dock with gripper,
decapper, and pipette models. Script attach/detach swaps and confirm
each tool reaches the dock and clears neighbours. Note any arm where
payload or reach makes a given swap impractical.

**3. Run the cycle-time experiment.** Execute the full Part 08 Behavior
Tree over a representative batch per arm and log **simulated
seconds-per-vial**. Record the numbers (and the failure/retry rate) for
the ROI model.

**4. Record everything for the business case.** Produce one comparison
table (arm × reach / payload / repeatability / coverage / cycle time /
tool-swap feasibility) plus the reachability-map screenshots. This is
the deliverable that feeds the capital story below.

### The capital story (all figures hedged — re-verify)

- **The PiPER is cheap** — roughly **~$1.5–2.5K** (`~`, verify) — which
  makes it an ideal **low-risk arm for the simulated and bench PoC**.
  You can prove the whole loop, time it, and demo it for a small
  fraction of one HPLC instrument's cost.
- **HPLC + automation is expensive.** A lab HPLC plus front-end
  automation typically runs **~$50–150K+** (`~`, rough — verify with
  vendors). That is the world the product sells into.
- **So the eventual PRODUCT** — a capable arm (the PiPER itself if the
  experiments above hold, or a UR-class cobot if production needs more
  repeatability/support) + the stations + the compliant arm-agnostic
  software (Part 09) — is priced as **instrument-grade capital,
  ~$75–250K** (`~`, rough — must be validated with real costs). The
  cheap PiPER may ship in a small cell or stay the dev/PoC tool; the
  twin tells you which.
- **ROI** comes from **technician-hours saved**, **fewer re-runs**
  (consistent prep), **higher throughput**, and **walk-away time**
  (unattended overnight batches).
- **The wedge** vs fixed liquid handlers (**Hamilton**, **Tecan**,
  **Opentrons**) is **flexibility**: a reprogrammable arm + compliant
  software adapts to new vial types, trays, and workflows where a fixed
  deck cannot.

## Additional hardware needed

| Real hardware | Why | How handled in sim |
|---------------|-----|--------------------|
| **The chosen production arm** (the PiPER, or a UR-class step-up if validation/repeatability demand it) | Real reach/payload/repeatability under load decide whether the PiPER ships or stays the PoC arm | Interchangeable URDF in the same Gazebo world |
| **Tool changer** + **end-effectors** (gripper, decapper, pipette) | Real swapping mechanics, mass, and repeatability | Attach/detach of end-effector models at the flange |
| **Enclosure + safety** (guarding, interlocks, e-stop) | A cell you can put a boundary around is a cell you can validate | Collision geometry + safety-zone models |
| **Controller PC** | Hosts the controller + compliant software in the lab | Any workstation in dev; the software is identical |
| **HPLC autosampler + stations** | The real instruments the cell serves | Mock service/action nodes at fixed tf frames (Parts 01–08) |

This is the eventual **shopping list**; in sim every item is an
interchangeable model, so the list firms up *after* the platform-swap
experiment, not before.

## How it connects

- [`02-vial-handling-and-gripping.md`](02-vial-handling-and-gripping.md)
  — the gripper end-effector this doc swaps on the tool changer.
- [`03-decapping-and-capping.md`](03-decapping-and-capping.md)
  — the decapper tool the tool-changer experiment attaches/detaches.
- [`04-liquid-handling-and-sample-prep.md`](04-liquid-handling-and-sample-prep.md)
  — the dispenser/pipetting tool, the third tool in the swap set.
- [`08-orchestration-error-handling-and-safety.md`](08-orchestration-error-handling-and-safety.md)
  — the Behavior Tree run that produces the cycle-time numbers.
- [`09-software-compliance-and-integration.md`](09-software-compliance-and-integration.md)
  — validation needs there drive the layout/enclosure design here, and
  its arm-agnostic software is what survives any platform swap.
- For the sibling comparisons, see
  [`../03-reBot-implementation/10-hardware-platform-and-capital-model.md`](../03-reBot-implementation/10-hardware-platform-and-capital-model.md)
  and
  [`../04-mycobot-280-impl/10-hardware-platform-and-capital-model.md`](../04-mycobot-280-impl/10-hardware-platform-and-capital-model.md).
- Mirrors
  [`../01-high-level-solution/10-hardware-platform-and-capital-model.md`](../01-high-level-solution/10-hardware-platform-and-capital-model.md);
  back to the index: [`README.md`](README.md).
