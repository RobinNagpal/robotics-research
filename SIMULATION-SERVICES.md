# Simulation Services: What We Can Sell, To Whom, and What to Learn

> **Job:** Turn the strategy in [`GOAL.md`](GOAL.md) ("services first,
> products later") into a concrete service catalog. This file lists the
> **types of simulation work** we can deliver to the 103 funded
> robotics companies in
> [`04-outreach/01-companies.md`](04-outreach/01-companies.md), maps
> each service line to the sectors that buy it, sketches how an
> **offshore services company** would deliver it, and ends with a
> **learning checklist** of what the team must know first.

**Plain-language note.** A *simulation* here means a physics-based 3D
software copy of a robot and its workplace (a *digital twin*) in which
the robot can be tested without touching real hardware. *Synthetic
data* means training images/sensor readings rendered from such a
simulation instead of collected in the real world, with labels
generated automatically.

---

## 1. Why robotics companies buy simulation work

Every company on the outreach list shares the same three pains:

- **Real-world data is expensive.** Collecting and hand-labeling
  photos of every parcel, weed, vein, or pallet a robot will meet
  costs far more than rendering them. Synthetic data with automatic
  labels is the standard workaround.
- **Real-world testing is slow and risky.** A forklift company cannot
  crash a real forklift a thousand times; a surgical-robot company
  cannot rehearse on a thousand patients. Simulation is the only place
  to test rare and dangerous cases at scale.
- **Their engineers are busy shipping robots.** Scene building, asset
  modeling, domain randomization, and dataset generation are
  self-contained, hand-off-able jobs — exactly the kind of work a
  small outside team can take on (the premise of
  [`GOAL.md`](GOAL.md)).

---

## 2. The service lines (types of simulation work)

Six service lines, ordered roughly from easiest-to-sell to most
advanced. The first two are the same Task A / Task B already chosen in
[`GOAL.md`](GOAL.md); the rest are natural extensions.

### 2.1 Digital-twin & simulation-scene creation

Build the simulated world itself: the robot model (URDF/MJCF/USD),
the workcell or site around it, accurate physics properties (mass,
friction, joint limits), and simulated sensors. Variants:

- **Workcell twins** — an arm plus its fixtures, totes, conveyor,
  vials, parts (our ketchup/paracetamol scenes are exactly this).
- **Facility twins** — a warehouse aisle, a greenhouse row, a
  recycling line, a hospital room.
- **Asset libraries** — packs of simulation-ready 3D objects (SKUs,
  crops, tools) with correct collision meshes and physics, the raw
  material every other service consumes.

Typical tools: **Gazebo Harmonic**, **NVIDIA Isaac Sim** (USD),
**MuJoCo**, **Blender** for asset modeling.

### 2.2 Synthetic-data generation for perception

Render labeled training data from the twin: RGB images, depth, point
clouds, segmentation masks, bounding boxes, 6-DoF object poses —
thousands of variations per hour with **domain randomization**
(random lighting, textures, camera angles, clutter) so models trained
on it survive the real world. Deliverable is a dataset in the format
the client's training pipeline expects (COCO, YOLO, …) plus the
generation pipeline itself so they can re-run it.

Typical tools: **Isaac Sim Replicator**, **BlenderProc**, **Unity
Perception**; validated by training a detector (e.g. **YOLO**) on the
output and testing on a small real-image set. This line is big enough
to be its own catalog — see
[`SYNTHETIC-DATA-SERVICES.md`](SYNTHETIC-DATA-SERVICES.md) for the
full breakdown of synthetic-data offerings.

### 2.3 Reinforcement-learning training environments

For companies that *learn* their robot skills (most of the humanoid
and foundation-model sector), the bottleneck is well-built,
massively-parallel training environments: the scene, the task
definition, the reward function, the randomization ranges, and the
sim-to-real gap analysis. We build and maintain those environments;
the client's ML team trains in them.

Typical tools: **Isaac Lab**, **MuJoCo (MJX)**, **Genesis**.

### 2.4 Scenario libraries & simulation-based regression testing

Procedurally generate the *situations* a robot must handle — a
blocked aisle, a torn box, a child stepping in front of a sidewalk
robot, a dropped instrument — and wire them into the client's CI so
every software release replays the whole library automatically and
reports pass/fail. This is recurring-revenue work: the library grows
with every field incident the client wants to never see again.

### 2.5 Sensor simulation & validation

Model the client's exact sensor suite — camera intrinsics and noise,
depth-sensor artifacts, lidar returns, IMU drift — so that what the
software sees in sim statistically matches the real device. This is
the unglamorous layer that makes 2.2–2.4 trustworthy, and a service
line in itself for companies with unusual sensors (ultrasonic
inspection, underwater, radar).

### 2.6 Demonstration data & teleoperation in sim

Foundation-model companies are hungry for robot *demonstrations*
(trajectories of a task being done), not just images. We can build
teleoperation setups inside the simulator, record demonstrations, and
multiply a handful of human demos into thousands of varied synthetic
ones (MimicGen-style augmentation). This is the newest and least
commoditized line — and the strongest fit for the humanoid sector.

| # | Service line | Deliverable | Effort to learn | Demand |
|---|--------------|-------------|-----------------|--------|
| 2.1 | Scene / digital-twin creation | Sim worlds + asset packs | Low — we are doing it now | Broad |
| 2.2 | Synthetic perception data | Labeled datasets + pipeline | Low–medium | Broadest |
| 2.3 | RL training environments | Isaac Lab / MuJoCo tasks | Medium–high | High (humanoids) |
| 2.4 | Scenario libraries + sim CI | Test suites in client CI | Medium | High, recurring |
| 2.5 | Sensor simulation | Validated sensor models | Medium | Niche but sticky |
| 2.6 | Demos / teleop in sim | Trajectory datasets | High | Hot, uncrowded |

**Bottom line:** start selling **2.1 + 2.2** (we are building exactly
that portfolio per [`GOAL.md`](GOAL.md)), grow into **2.4** for
recurring revenue, and learn toward **2.3/2.6** because that is where
the best-funded buyers (humanoids, foundation models) spend.

---

## 3. Mapping services to the outreach sectors

The sectors below are the seven sections of
[`04-outreach/01-companies.md`](04-outreach/01-companies.md).

| Sector (from the list) | What they need from simulation | Best-fit lines | Example prospects |
|---|---|---|---|
| 1. Humanoids & general-purpose intelligence | Massive RL environments, demo data, dexterous-manipulation scenes | 2.3, 2.6, 2.2 | Agility, Flexion, mimic, Dyna, Genesis AI, Sunday |
| 2. Warehouse, logistics & manufacturing | SKU/parcel asset packs, warehouse twins per customer site, pick-point datasets | 2.1, 2.2, 2.4 | Dexterity, Nimble, Sereact, Pickle, Nomagic, Brightpick |
| 3. Agriculture, construction & energy | Procedural outdoor worlds (crops, weather, dust, terrain), off-season testing | 2.2, 2.4, 2.1 | Carbon Robotics, Ecorobotix, Bonsai, Agtonomy, Bedrock |
| 4. Medical, surgical & lab automation | Synthetic imagery where real data is regulated/scarce, lab-cell twins, validation evidence | 2.2, 2.5, 2.4 | CMR Surgical, ForSight, Vitestro, Cellares, Automata |
| 5. Drones, maritime, inspection & defense | GPS-denied flight scenarios, swarm/sea-state sims, defect imagery for inspection | 2.4, 2.5, 2.2 | Skydio*, Gecko*, ANYbotics, Saildrone*, Voliro |
| 6. Service, delivery, consumer & recycling | Sidewalk/pedestrian scenario libraries, waste-stream and food-item datasets | 2.4, 2.2 | Starship, Coco, Glacier, AMP, Chef Robotics, Simbe |
| 7. Mixed (tractors, yard trucks, indoor drones) | Site twins, fleet-behavior testing, inventory-scan datasets | 2.1, 2.4, 2.2 | Monarch, Outrider, Burro, Corvus, Ati Motors |

\* Defense-funded prospects carry export-control restrictions for an
offshore vendor — see §4.

**Where the pain is sharpest (why each sector buys):**

- **Humanoids (1):** they live or die by sim-to-real; every dollar of
  their funding is bet on training in simulation. Highest budgets,
  most sophisticated buyers — they will outsource *environment
  building* but keep model training in-house.
- **Warehouse (2):** every new customer site and every new SKU is a
  new perception problem. A repeatable "site twin + SKU dataset"
  package can be sold over and over to the *same* client.
- **Field robotics (3):** crops grow once a year — a missed test
  window costs a season. Simulated fields with randomized growth
  stages, lighting, and dust are the only way to iterate year-round.
- **Medical (4):** real procedure data is privacy-bound and scarce;
  synthetic imagery and simulated procedure runs are often the only
  scalable training/validation evidence. Longest sales cycles, but
  the stickiest contracts once in.
- **Drones/maritime/defense (5):** the scenarios that matter (GPS
  loss, swarms, storms) are exactly the ones you cannot stage in
  reality. Big demand, but for an offshore company the defense subset
  is largely off-limits (§4) — target the *civilian inspection*
  companies (ANYbotics, Voliro, Aerones, Square Robot) instead.
- **Service/consumer (6):** robots among people means safety cases
  and infinite object variety — scenario libraries (2.4) and
  long-tail object datasets (2.2) map one-to-one onto that.

**Bottom line:** the beachhead is **sectors 2 and 6** (warehouse +
service robots) sold the productized "twin + dataset" package, with
**sector 1** (humanoids) as the growth account for RL environments
and demo data, and civilian inspection (in 5) plus lab automation
(in 4) as adjacent niches. Defense work stays out of scope until the
company has an onshore presence.

---

## 4. The offshore simulation-services company

The plan: a small offshore team (e.g. registered in India, serving
US/EU clients remotely) selling the §2 service lines as fixed-scope,
productized packages.

### Why simulation work suits an offshore company

- **The deliverable is digital.** Scenes, datasets, and pipelines are
  git repos and cloud buckets — nothing to ship, no site visits
  required for v1 engagements.
- **The work is self-contained.** A scene or dataset job can be
  specified in a document, built independently, and accepted against
  objective criteria (e.g. "detector trained on your data reaches X%
  mAP on our real test set") — the "outsourceable layer" property
  that [`GOAL.md`](GOAL.md) selected for.
- **Cost structure wins.** The competition for this work is the
  client's own senior engineers (expensive) or US/EU sim consultancies.
  An offshore team can price a workcell twin or a 50k-image dataset
  at a fraction of either and still earn good margins.
- **Time zones help, not hurt.** Overnight turnaround on dataset
  iterations ("we re-rendered with the fixes; review when you wake
  up") is a genuine selling point.

### How to package and sell it

- **Productize, don't body-shop.** Sell outcomes with fixed scope and
  price: *"Simulation-ready digital twin of one workcell — 2–3
  weeks"*, *"50,000 labeled synthetic images for N SKUs + the
  generation pipeline"*, *"scenario regression suite wired into your
  CI"*. Avoid open-ended staff augmentation at the start; it
  commoditizes us.
- **Pilot-first pricing.** A small paid pilot (one scene, one
  dataset) de-risks us for the buyer; the expansion path is more
  sites, more SKUs, more scenarios — all repeat business.
- **Portfolio before outreach.** The ketchup and paracetamol scenes
  and datasets (the [`GOAL.md`](GOAL.md) checklist) *are* the
  portfolio: a public repo + a 2-minute video per service line beats
  any slide deck. Each demo should be in the buyer's vocabulary
  (a picking scene for warehouse prospects, not a chemistry lab).
- **Acceptance criteria in every proposal.** Synthetic data is judged
  by one number: does a model trained on it work on real images?
  Put that test in the contract — it is also our quality bar.

### Operational requirements (what to set up)

- **Compute:** 2–3 RTX-class GPU workstations to start; burst to
  cloud GPUs for large renders/RL runs. Isaac Sim requires NVIDIA
  RTX hardware; budget for that explicitly.
- **Licensing hygiene:** Gazebo, MuJoCo, Blender, BlenderProc, and
  Genesis are free/open-source. Isaac Sim is free to use, but check
  current NVIDIA license terms for *commercial service* use before
  quoting Isaac-based work. Never ship client deliverables containing
  3D assets whose licenses forbid redistribution.
- **IP and security posture:** clients hand us CAD files, site scans,
  and failure data — all sensitive. NDAs by default, per-client
  repo/credential isolation, no client data in personal accounts or
  public model-training services. Medical clients will additionally
  ask about data-handling procedures in writing.
- **Export control (the hard limit):** US defense-funded companies
  (much of section 5 of the outreach list — Skydio, Saildrone,
  HavocAI, Overland AI, Neros, …) operate under ITAR/EAR rules that
  generally bar sharing controlled technical data with a foreign
  company. Do not pitch them from the offshore entity; revisit only
  with proper legal advice or an onshore subsidiary.
- **Team shape (first hires):** 2–3 simulation engineers (ROS 2 /
  Gazebo / Isaac), 1 3D artist (Blender, asset + CAD cleanup), 1 ML
  engineer (dataset QA, detector training, later RL). Founders cover
  sales and scoping.
- **Legal/financial basics:** an entity that can sign US/EU
  contracts and invoice in USD/EUR, standard MSA + SOW templates,
  and professional-liability insurance. (Specifics vary by
  jurisdiction — get local advice; out of scope for this doc.)

### Honest risks

- **Genesis-style generation is improving fast** — generative
  sim/data tools may commoditize the simplest rendering work. Defense
  against that: move up the stack (2.3–2.6), own the *validation*
  story, not just the rendering.
- **Trust barrier:** robotics startups guard their data. Expect the
  first deal to be small and the portfolio to do the convincing.
- **Key-person risk:** with a 5-person team, document everything;
  the packaged-pipeline deliverable style (client gets the pipeline,
  not just files) doubles as our own internal documentation.

---

## 5. Learning checklist

What the team must learn to deliver §2 credibly. This **builds on**
the HPLC checklist —
[`02-hplc-autosampler/06-learning-checklist.md`](02-hplc-autosampler/06-learning-checklist.md)
covers ROS 2, Gazebo, MoveIt 2, YOLO, and the 8-layer stack on the
ketchup problem; do that first (or in parallel). This list adds what
a *simulation-services vendor* needs beyond it. Tick items as you go;
each part has a **Done when** bar — don't gold-plate.

### Part A — Simulator breadth (know the big three, not just Gazebo)

Clients will name their simulator in the first call; we must not
flinch.

- [ ] **Gazebo Harmonic** — already covered by the HPLC checklist
  (our ketchup scene). Know SDF/URDF, plugins, sensor models.
- [ ] **NVIDIA Isaac Sim** — install, complete the core tutorials,
  rebuild the ketchup workcell scene in it; learn **USD** (the scene
  format) well enough to structure assets the way Isaac expects.
- [ ] **MuJoCo** — work through the basics, load an arm model
  (MJCF), understand why RL teams prefer it (speed, stable contacts).
- [ ] **Know of the rest** (one honest sentence each, no install
  needed): **Genesis**, **Isaac Lab**, **Unity**, **Unreal/AirSim
  successors**, **CARLA** (driving), **Webots**.
- [ ] **Comparison fluency:** be able to recommend a simulator given
  a client's robot type, sensor suite, and goal (RL vs perception vs
  testing) — and say *why* in plain language.

**Done when:** the same small scene exists in Gazebo, Isaac Sim, and
MuJoCo, and anyone on the team can explain when to choose each.

### Part B — Asset & scene pipeline (the 3D-artist muscle)

- [ ] **Blender fundamentals** — model a clean, low-poly object with
  correct scale and origin; UV-unwrap and texture it.
- [ ] **CAD → sim conversion** — take a STEP/STL file (clients send
  these), decimate it, generate convex collision meshes, assign
  plausible mass/inertia/friction.
- [ ] **Format fluency** — convert one asset URDF ↔ MJCF ↔ USD and
  know what survives each conversion (and what silently breaks).
- [ ] **Build a small asset pack** — 10 simulation-ready objects
  (totes, boxes, bottles…) with a README, license note, and preview
  renders: our first portfolio artifact.
- [ ] **Physical accuracy check** — drop/stack/grasp the assets in
  sim and tune until behavior looks right; document the tuning.

**Done when:** given a random client CAD file, anyone can produce a
sim-ready, physically plausible asset in under a day.

### Part C — Synthetic-data pipeline (service line 2.2, the core skill)

- [ ] **Isaac Sim Replicator** — complete the Replicator tutorials;
  generate RGB + bounding boxes + segmentation from the ketchup
  scene.
- [ ] **BlenderProc** — same exercise, fully open-source route;
  understand when its photorealism beats real-time renderers.
- [ ] **Domain randomization** — implement randomized lighting,
  textures, camera pose, and distractor clutter; be able to explain
  *why* randomization closes the sim-to-real gap.
- [ ] **Dataset formats** — export COCO and YOLO formats; write the
  dataset README a client's ML engineer would want.
- [ ] **The proof loop (most important):** train YOLO on synthetic
  images only, evaluate on ~50 real photos of the same objects,
  report mAP honestly, iterate randomization until real-world
  performance is respectable. This loop *is* the product.

**Done when:** we have one end-to-end case study — synthetic-only
training data, measured real-world accuracy, write-up — ready to show
a prospect.

### Part D — RL environments & sim-to-real (service lines 2.3, 2.6)

Deeper water; needed for the humanoid sector, not for the first sale.

- [ ] **RL vocabulary** (one sentence each): policy, reward,
  episode, PPO, parallel environments, curriculum, sim-to-real gap,
  domain randomization (again — it's the bridge).
- [ ] **Isaac Lab walkthrough** — run a provided example (e.g. cube
  lifting or quadruped locomotion) end to end on our GPU.
- [ ] **Build one custom task** — define scene, observations,
  rewards, and randomization for a simple pick task; train until it
  works in sim.
- [ ] **Teleop & demonstrations** — collect a few demonstrations of
  a sim task (keyboard/space-mouse/VR — whatever is available) and
  read up on demo-augmentation approaches (e.g. MimicGen) to speak
  to service line 2.6.
- [ ] **Read 2–3 sim-to-real case studies** from humanoid/quadruped
  companies (ANYbotics, Agility, and Flexion publish talks/posts) so
  we know the buyer's vocabulary.

**Done when:** we can demo one trained-in-sim skill and hold a
30-minute technical conversation with an RL engineer without bluffing.

### Part E — Testing, scenarios & delivery engineering (service line 2.4)

- [ ] **Headless & scripted sim** — run Gazebo/Isaac without a GUI,
  drive scenarios from Python/CLI, produce pass/fail output.
- [ ] **Sim in CI** — wire one scenario into a GitHub Actions (or
  similar) pipeline that runs on every push and posts results.
- [ ] **Procedural scenario generation** — parameterize one scene
  (object positions, lighting, failures) and auto-generate 100
  variants with a manifest.
- [ ] **Packaging discipline** — every deliverable ships as: repo +
  README + pinned dependencies (container) + a one-command
  reproduction script. Practice on our own scenes first.

**Done when:** a stranger can clone one of our deliverable repos and
reproduce the dataset/scenario run with one command.

### Part F — Business knowledge (founder track, parallel to A–E)

- [ ] **Re-read the outreach list**
  ([`04-outreach/01-companies.md`](04-outreach/01-companies.md)) and
  tag each target sector-by-sector with the §2 service line we'd
  pitch (the §3 table is the template).
- [ ] **Licensing check** — read the current Isaac Sim / Omniverse
  license terms for commercial service work; confirm our open-source
  stack (Gazebo, MuJoCo, Blender, BlenderProc) is clean for client
  deliverables.
- [ ] **Export-control awareness** — read an ITAR/EAR primer; write
  our one-page internal policy on which prospects the offshore
  entity must not pitch.
- [ ] **Proposal template** — draft the standard SOW: scope,
  acceptance criteria (the Part C proof loop), timeline, price,
  IP/data-handling terms.
- [ ] **Two case-study write-ups** — ketchup scene (2.1) and the
  Part C dataset (2.2), each as a 1-page PDF + short video.

**Done when:** we can send a credible cold email with a portfolio
link the same day a prospect replies "show me".

---

## 6. Suggested order of attack

1. **Finish the [`GOAL.md`](GOAL.md) checklist** (ketchup +
   paracetamol scenes and datasets) — that is Parts B/C in disguise
   and produces the portfolio.
2. **Parts A–C above** in parallel across the team (~2–3 weeks of
   focused work).
3. **Part F** as soon as one case study exists; start outreach with
   sectors 2 and 6 of the company list.
4. **Parts D–E** while the first pilots run, opening the humanoid
   sector and recurring-revenue testing work.

*Tool versions, license terms, and company details drift — re-verify
anything in this file before quoting it to a prospect.*
