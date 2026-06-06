# Part 10 — Hardware platform & capital model (myCobot 280 simulation)

> **Sim goal:** Use the **digital twin** — the Gazebo cell built across
> Parts 01–09 around the **myCobot 280** — to **de-risk the platform
> and business decision before spending real money**: compare arms in
> the same world, prove the tool changer, measure cycle time, and lay
> out the bench, all as swappable models. The crux question this doc
> answers: *is the cheap, short-reach 280 enough, or does production
> need a bigger arm?*

This mirrors the high-level
[`../02-high-level-solution/10-hardware-platform-and-capital-model.md`](../02-high-level-solution/10-hardware-platform-and-capital-model.md).
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
**URDF** (Unified Robot Description Format) is the file that describes
a robot's links, joints, limits, and meshes. Drop a different arm's
URDF into the identical Gazebo bench and re-run the same worklist:

- **myCobot 280** — open URDF + ready-made Gazebo + MoveIt config from
  `mycobot_ros`; our cheap baseline (~280 mm reach, ~250 g payload —
  `~`, verify). The most sim-ready arm here *today*.
- **myCobot 320** — same `mycobot_ros` family, ~500 mm reach, ~1 kg
  payload (`~`, verify); the natural step up if the 280 is too small.
- **reBot Arm** — open URDF + workspace (GitHub
  `Seeed-Projects/reBot-DevArm`); the sibling implementation's
  baseline.
- **UR3e / UR5e** — from `Universal_Robots_ROS2_Description`; the
  de-facto industrial cobot standard, large ecosystem, validated
  controllers.
- **Franka** — from `franka_description`; research-friendly, sensitive
  force control (optional reference point).

For each, measure **reach** (can it cover every station — vial store,
decapper, dispenser, tray — from a fixed base?), **repeatability**,
**payload**, and **collision-free access** to all stations, noting
where joint limits or self-collision block a station or slot. **The
280's ~280 mm reach is the crux finding**: as flagged in Part 05, it
likely cannot cover a full standard autosampler tray from a fixed
bench seat. The honest expected verdict: *the 280 is a great cheap
arm for the simulated and bench proof-of-concept (PoC), but a
production cell almost certainly needs more reach — a 320 or a UR
arm.* The twin lets you show that with a reachability map rather than
discovering it after purchase.

**(b) Tool changer — attach/detach end-effector models.** Simulate the
arm swapping tools at a parking dock: **gripper ↔ decapper ↔ pipetting
tool**. In sim a tool change is an **attach/detach** of an
end-effector model at the wrist flange, with the matching MoveIt
end-effector config loaded. This proves the *sequence and reachability*
of tool changes (does the arm reach the dock? does each tool clear
neighbouring stations?) without a real changer existing yet. Note the
280's low payload makes a heavy multi-tool turret unrealistic on that
arm specifically — another input to the platform call.

**(c) Cycle time — seconds per vial.** Run the full Behavior Tree
(Part 08) over a batch in Gazebo and **measure simulated seconds per
vial** end to end (pick → decap → dispense → recap → place → verify).
Repeat per candidate arm. These numbers feed the throughput and ROI
(Return On Investment) case directly — and they are a fair *relative*
comparison even if absolute sim timing needs a real-hardware reality
check.

**(d) Layout / enclosure as models.** Model the bench, station
placement, cable runs, and a notional **enclosure / safety zones** as
collision geometry. Check that every station is reachable, that the
arm stays inside its safety envelope, and that the cell footprint is
plausible for a lab bench. This de-risks the physical layout before
any fabrication.

**Honest limits (need vendors / hardware to settle):** true reach,
payload, and repeatability under load; real tool-changer mechanics and
mass; absolute cycle time; and — critically — real **cost** and
**validation** (IQ/OQ/PQ, see Part 09). The twin ranks and de-risks
the options; it does not replace a vendor quote or a bench trial.

## Open-source tools

| Tool | Role | Bottom line |
|------|------|-------------|
| **Gazebo Harmonic** | Hosts the one bench world into which each arm URDF is swapped | The shared world that makes the comparison apples-to-apples |
| **`mycobot_ros`** | URDF + Gazebo + MoveIt config for myCobot 280 **and** 320 | One package covers both the baseline and the step-up arm |
| **Universal_Robots_ROS2_Description / franka_description / reBot URDF** | URDFs for the comparison arms (UR3e/UR5e, Franka, reBot) | Drop-in alternatives in the same world |
| **MoveIt 2** | Reachability maps + collision-free planning per arm | Decides geometric fit before any quote |
| **`ros2_control` + `gz_ros2_control`** | Runs each arm's joint controllers in sim | Same control interface across all candidates |
| **BehaviorTree.CPP** (+ Groot2) | Runs the full prep-and-load loop to time it | Source of the cycle-time numbers |
| **Grasp-fix / attach-detach plugin** | Models tool-changer attach/detach of gripper/decapper/pipette | Proves tool-swap sequence with no real changer |
| **RViz2 / Foxglove** | Visualise reach maps, tool swaps, layout, safety zones | Eyeball each experiment and capture screenshots for the business case |

## How to simulate it now

**1. Run the platform-swap experiment.** Keep the bench, stations, and
worklist fixed. For each arm URDF (280, 320, reBot, UR3e/UR5e), load
it into the world, build a **reachability map** over every station and
tray slot (loop IK + plan in MoveIt 2, colour reachable / unreachable
in RViz2), and record which stations/slots are covered. Tabulate reach,
payload, repeatability (from spec), and coverage per arm.

**2. Run the tool-changer experiment.** Add a parking dock with
gripper, decapper, and pipette models. Script attach/detach swaps and
confirm each tool reaches the dock and clears neighbours. Note any arm
(notably the 280) where payload or reach makes the swap impractical.

**3. Run the cycle-time experiment.** Execute the full Part 08 Behavior
Tree over a representative batch per arm and log **simulated
seconds-per-vial**. Record the numbers (and the failure/retry rate) for
the ROI model.

**4. Record everything for the business case.** Produce one comparison
table (arm × reach / payload / repeatability / coverage / cycle time /
tool-swap feasibility) plus the reachability-map screenshots. This is
the deliverable that feeds the capital story below.

### The capital story (all figures hedged — re-verify)

- **The 280 is cheap** — roughly **~$700** (`~`, verify) — which makes
  it an ideal **low-risk arm for the simulated and bench PoC**. You can
  prove the whole loop, time it, and demo it for the price of a laptop
  accessory.
- **HPLC + automation is expensive.** A lab HPLC plus front-end
  automation typically runs **~$50–150K+** (`~`, rough — verify with
  vendors). That is the world the product sells into.
- **So the eventual PRODUCT** — a more capable arm (likely a 320 or
  UR-class, per the experiments above) + the stations + the compliant
  arm-agnostic software (Part 09) — is priced as **instrument-grade
  capital, ~$75–250K** (`~`, rough — must be validated with real
  costs). The cheap 280 is the dev/PoC tool, not the shipped arm.
- **ROI** comes from **technician-hours saved**, **fewer re-runs**
  (consistent prep), **higher throughput**, and **walk-away time**
  (unattended overnight batches).
- **The wedge** vs fixed liquid handlers (**Hamilton**, **Tecan**,
  **Opentrons**) is **flexibility**: a reprogrammable arm + compliant
  software adapts to new vial types, trays, and workflows where a fixed
  deck cannot.
- **The sensor suite is a real line item — and another input to the
  platform call.** The [`sensor-suite.md`](sensor-suite.md) is designed
  *around* the 280's limits: with ~250 g payload and no joint
  force/torque sensing, the wrist carries only a tiny RGB module and all
  the heavy/depth sensing is pushed **off the arm** (fixed cameras,
  station load cells + balance, per-station proximity, cell-boundary
  safety sensors). A bigger arm (**320 / UR-class**) can instead carry a
  **wrist RGB-D camera and a wrist force/torque sensor**, folding several
  off-arm sensors back onto the wrist and *simplifying* the suite — so
  the arm choice and the sensor BOM are coupled, and both feed the buy
  decision. Rough per-sensor costs (hedged — re-verify):

  | Sensor | ~Cost (USD) |
  |--------|-------------|
  | Overhead RGB-D (#1) | ~$150–350 |
  | Station camera (#2) | ~$50–250 |
  | Wrist RGB module (#3) | ~$30–100 |
  | Gripper feedback (#4) | ~$0 (built in) |
  | Decapper load cell / torque (#5) | ~$20–200 |
  | **Analytical balance (#6)** | **~$300–2,000** |
  | Proximity / presence ×~4 (#7) | ~$10–40 each |
  | Liquid-level sensor (#8) | ~$10–100 |
  | **Light curtain / laser scanner (#10)** | **~$200–1,500** |
  | Door interlock + e-stop (#11) | ~$30–150 |
  | Base IMU (#12) | ~$0 (on-board) |

  The **big swings are the balance (#6) and the safety light curtain
  (#10)** — both are where lab-grade and safety-rated parts cost real
  money, so the twin lets you decide which are truly needed *before*
  buying. In **only-code** every line above is a free Gazebo plugin or
  mock topic — ~$0. (Homing/limit switches #9 are part of the arm.)

## Additional hardware needed

| Real hardware | Why | How handled in sim |
|---------------|-----|--------------------|
| **The chosen production arm** (likely a step up from the 280 — a 320 or UR-class) | The 280's ~280 mm reach / ~250 g payload likely won't cover a full tray or carry a tool turret | Interchangeable URDF in the same Gazebo world |
| **Tool changer** + **end-effectors** (gripper, decapper, pipette) | Real swapping mechanics, mass, and repeatability | Attach/detach of end-effector models at the flange |
| **Enclosure + safety** (guarding, interlocks, e-stop) | A cell you can put a boundary around is a cell you can validate | Collision geometry + safety-zone models |
| **Sensor suite** (cameras, gripper feedback, load cell, balance, proximity, level, safety curtain, interlock, IMU — see [`sensor-suite.md`](sensor-suite.md)) | The off-arm sensing the 280's payload forces; balance (#6) + light curtain (#10) are the cost swings | Gazebo sensor plugins + mock topics (~$0 in sim) |
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
- [`sensor-suite.md`](sensor-suite.md) — the canonical sensor list and
  full BOM; the per-sensor costs above are summarised from it, and the
  arm choice directly shapes how much of that suite must live off-arm.
- For the reBot comparison, see
  [`../04-reBot-implementation/10-hardware-platform-and-capital-model.md`](../04-reBot-implementation/10-hardware-platform-and-capital-model.md).
- Mirrors
  [`../02-high-level-solution/10-hardware-platform-and-capital-model.md`](../02-high-level-solution/10-hardware-platform-and-capital-model.md);
  back to the index: [`README.md`](README.md).
