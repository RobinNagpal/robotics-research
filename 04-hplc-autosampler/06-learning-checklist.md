# 06 — Learning checklist: from zero to a credible robotics-agency pitch

> **Job:** Give you and your team a **3–4 day**, checkbox-driven plan to
> learn *just enough* of the robotics landscape — concepts, the
> framework/sensor/hardware comparison, and **one "hello world" per
> layer** — to (a) genuinely understand how companies solve problems
> like our [HPLC autosampler](01-high-level-solution/README.md) or
> [shelf placement](../03-place-items-on-shelf/01-requirements.md), and (b) email
> robotics-adjacent companies saying *"we've worked in robotics and have
> a team that can help you"* and back it up in the call that follows.
>
> Everything here is framed around the stack we already worked out in
> **[`03-mycobot-280-impl/01-only-code/`](03-mycobot-280-impl/01-only-code/README.md)**
> — the fully open-source, simulation-first myCobot 280 cell — so the
> hello worlds build the *same* system, on the *same* problem, that we
> would pitch.

> **Disclaimer.** This is a learning plan, not a course. Tool versions
> and install steps drift — follow each project's current docs. Time
> estimates are aggressive on purpose; the point is breadth + one
> working demo per layer, not mastery.

---

## How to use this checklist

- Tick `- [ ]` items as you go. Each hello world has a **Done when…**
  line — that is the bar; don't gold-plate.
- **Split the work across the team.** The 8 layers are independent
  enough that 2–3 people can each own a few layers in parallel, then
  demo to each other on day 4. One shared simulator world (Layer 1) is
  the only hard dependency.
- **Goal of the whole thing:** by the end you can stand up the digital
  twin, move the arm, see a fiducial, grasp a vial, read a barcode, run
  a behavior tree, and serve + log a worklist — *and* explain each piece
  to a non-robotics buyer in terms of **their** problem.
- New term? Keep
  [`../03-place-items-on-shelf/02-glossary.md`](../03-place-items-on-shelf/02-glossary.md)
  open in a tab.

---

## Why these exact topics (the pitch we're preparing for)

We are positioning as a **software-primary robotics agency** that builds
**simulation-first** automation: prove the whole loop in an open-source
simulator, then transfer to hardware. To send a credible cold email and
survive the first call, the team must be able to:

1. **Speak the language** — robotics subfields, ROS 2, digital twins,
   motion planning, perception, grasping, orchestration, and (for labs)
   the compliance vocabulary.
2. **Show we've actually run the stack** — not slides, but a working
   sim of a real task (HPLC vial prep → tray loading).
3. **Map a stranger's problem onto our 8-layer stack** in real time, and
   honestly scope what simulation proves vs. what needs hardware.

The checklist is organized to deliver exactly those three things.

---

## Part A — The landscape (½ day, do this first)

Before any tool, get the mental map. This is what lets you *talk* to a
prospect even about a problem we haven't built yet.

- [ ] **Read our own strategic overview** —
  [`../README.md`](../README.md) (the 9 robotics subfields + market
  framing) and skim [`../03-place-items-on-shelf/`](../03-place-items-on-shelf/01-requirements.md)
  so you can speak to a *second* example, not just HPLC.
- [ ] **Read the problem we'll demo** —
  [`01-high-level-solution/README.md`](01-high-level-solution/README.md)
  and its 10 parts (skim), so the hello worlds have meaning.
- [ ] **Internalize the cross-cutting concepts** (one sentence each, from
  the glossary): **ROS 2**, **node / topic / service / action**,
  **URDF**, **tf frame**, **digital twin**, **motion planning**,
  **inverse kinematics**, **RGB-D**, **point cloud**, **fiducial /
  AprilTag**, **grasp pose**, **behavior tree**, **sim-to-real**.
- [ ] **Lab-automation vocabulary** (so you don't sound naïve to an
  instrument company): **LIMS**, **CDS** (Empower / Chromeleon),
  **SiLA 2**, **OPC UA**, **21 CFR Part 11**, **ALCOA+**, **audit
  trail**, **IQ/OQ/PQ**, **CSV (computer-system validation)**. See
  [`01-high-level-solution/09-software-compliance-and-integration.md`](01-high-level-solution/09-software-compliance-and-integration.md).
- [ ] **Know the sensor story** — read
  [`03-mycobot-280-impl/sensor-suite.md`](03-mycobot-280-impl/sensor-suite.md)
  so you can explain *how a cell sees and feels* (3 cameras + gripper
  feedback + load cell + balance + presence/safety + IMU) and the
  "keep the wrist light, sense off the arm" payload rule.

**Done with Part A when:** anyone on the team can whiteboard the
8-layer stack and say, in plain English, what each layer does and where
a given client problem would touch it.

---

## Part B — The 8-layer stack: concept → comparison → hello world

These are the **same 8 layers** as
[`03-mycobot-280-impl/01-only-code/`](03-mycobot-280-impl/01-only-code/README.md).
For each: understand the idea, know the framework comparison (we already
wrote it — just read and confirm), and **build the one hello world**.
Every hello world uses the **HPLC vial / tray** as its subject.

> **Setup once (Layer 0):** install **ROS 2** (Humble or Jazzy) and
> **Gazebo Harmonic** on Ubuntu (or a container), and clone
> `mycobot_ros`. This single environment carries every hello world
> below. Budget a couple of hours for this; it's the only real
> yak-shave.

### Layer 1 — Simulator & digital twin (Gazebo)

- [ ] **Understand:** what a physics simulator and a digital twin are;
  why sim-first de-risks a purchase. Read
  [`01-only-code/01-simulation-and-digital-twin.md`](03-mycobot-280-impl/01-only-code/01-simulation-and-digital-twin.md).
- [ ] **Know the comparison:** Gazebo Harmonic vs MuJoCo vs Isaac Sim
  vs PyBullet vs Webots — and *why we pick Gazebo* (open, ROS-native).
- [ ] **Hello world — "spawn the cell":** load the **myCobot 280 URDF**
  into an empty Gazebo world with a **table** and a **2 mL vial** model;
  view it in **RViz2**. *Done when:* the arm and a vial appear in both
  Gazebo and RViz, and you can see `/joint_states` and the tf tree.

### Layer 2 — Middleware & control (ROS 2)

- [ ] **Understand:** ROS 2 nodes, topics, services, actions; what
  `ros2_control` does. Read
  [`01-only-code/02-middleware-and-control.md`](03-mycobot-280-impl/01-only-code/02-middleware-and-control.md).
- [ ] **Know the comparison:** ROS 2 vs bare middleware; rclpy vs rclcpp;
  CycloneDDS vs FastDDS (just the gist).
- [ ] **Hello world — "the mock decapper":** write a tiny **rclpy**
  node that offers a `/decap` **service** (returns "cap removed") and a
  publisher that streams a fake `/balance/mass` reading. Call the
  service from the CLI (`ros2 service call …`). *Done when:* you can
  call `/decap` and echo `/balance/mass` from another terminal — you've
  built the pattern every mock station uses.

### Layer 3 — Arm motion planning (MoveIt 2)

- [ ] **Understand:** motion planning, inverse kinematics, collision
  checking, planning scene. Read
  [`01-only-code/03-arm-motion-planning.md`](03-mycobot-280-impl/01-only-code/03-arm-motion-planning.md).
- [ ] **Know the comparison:** MoveIt 2 vs raw OMPL vs writing your own
  IK; MoveIt Servo and MoveIt Task Constructor at a glance.
- [ ] **Hello world — "reach the vial":** with the `mycobot_ros` MoveIt
  config, plan and execute (in sim) a collision-free motion from home to
  a **named pose above the vial**, then to a **tray slot** pose. *Done
  when:* the arm moves between the supply nest and a tray slot in
  RViz/Gazebo without colliding with the table.

### Layer 4 — Perception & 3D vision

- [ ] **Understand:** RGB vs RGB-D, point clouds, fiducials, camera
  intrinsics, hand-eye calibration (concept only). Read
  [`01-only-code/04-perception-and-vision.md`](03-mycobot-280-impl/01-only-code/04-perception-and-vision.md).
- [ ] **Know the comparison:** OpenCV vs Open3D vs PCL; apriltag_ros;
  camera SDKs (RealSense / OAK / Orbbec) for later hardware.
- [ ] **Hello world — "see the tray":** add a **simulated camera** to the
  Gazebo world, put an **AprilTag** on the tray, run **apriltag_ros**
  (or the `apriltag` lib on a saved frame) and **print the tag's pose**;
  as a bonus, use **OpenCV** to find the vial **rim** (a circle) in the
  same image. *Done when:* a script prints the tray tag's 6-number pose
  and draws the detected vial rim.

### Layer 5 — Grasping & manipulation

- [ ] **Understand:** grasp pose, antipodal grasp, parallel-jaw gripper;
  analytical vs learned grasping. Read
  [`01-only-code/05-grasping-and-manipulation.md`](03-mycobot-280-impl/01-only-code/05-grasping-and-manipulation.md).
- [ ] **Know the comparison:** analytical/antipodal (Open3D) vs MoveIt
  Task Constructor vs Contact-GraspNet / AnyGrasp — and why **analytical
  wins for one known vial**.
- [ ] **Hello world — "grab the vial":** compute an **antipodal pinch**
  on the vial cylinder (jaws perpendicular to its axis, just under
  ~12 mm), command the **sim gripper** (`GripperCommand`) to close, and
  use the **grasp-fix attach** so the vial follows the gripper. *Done
  when:* the arm picks the vial, lifts it, and the **gripper width +
  effort** confirm a hold (the two-witness check from the sensor suite).

### Layer 6 — Identification & barcode

- [ ] **Understand:** 1D/2D barcodes, why every vial is tracked, the
  vial→worklist mapping. Read
  [`01-only-code/06-identification-and-barcode.md`](03-mycobot-280-impl/01-only-code/06-identification-and-barcode.md).
- [ ] **Know the comparison:** ZBar/pyzbar vs OpenCV QR vs a cloud OCR
  (and why local/open is enough here).
- [ ] **Hello world — "read the vial ID":** generate a **QR code** for a
  sample ID, render it on a vial label in an image, and decode it with
  **pyzbar** — then look the ID up in a tiny worklist dict. ~10 lines:
  ```python
  from pyzbar.pyzbar import decode; from PIL import Image
  code = decode(Image.open("vial_label.png"))[0].data.decode()
  print("sample:", code, "->", worklist.get(code, "UNKNOWN"))
  ```
  *Done when:* a label image resolves to a known worklist row (and an
  unknown code is flagged).

### Layer 7 — Orchestration & task logic (Behavior Trees)

- [ ] **Understand:** behavior trees vs state machines; sequence /
  fallback / retry; the "sensor → gate → retry/quarantine/stop" model.
  Read
  [`01-only-code/07-orchestration-and-task-logic.md`](03-mycobot-280-impl/01-only-code/07-orchestration-and-task-logic.md).
- [ ] **Know the comparison:** BehaviorTree.CPP (+ Groot2) vs **py_trees**
  vs SMACH/YASMIN/FlexBE.
- [ ] **Hello world — "the per-vial loop":** in **py_trees** (fastest in
  Python) build a tree: `pick → [gate: held?] → place → [gate: seated?]`
  with a **fallback that retries** a failed gate once then quarantines.
  Tick it with mocked gate results. *Done when:* a forced gate-failure
  visibly triggers the retry/quarantine branch instead of charging on.

### Layer 8 — Software, worklist & compliance

- [ ] **Understand:** worklist, audit trail, why a regulated lab needs
  ALCOA+ / 21 CFR Part 11, what SiLA 2 / OPC UA are for. Read
  [`01-only-code/08-software-worklist-and-compliance.md`](03-mycobot-280-impl/01-only-code/08-software-worklist-and-compliance.md).
- [ ] **Know the comparison:** FastAPI + SQLite (our mock) vs a real
  LIMS/CDS; a SiLA 2 mock vs the real standard.
- [ ] **Hello world — "the mock LIMS + audit log":** a small **FastAPI**
  service that serves a **worklist** (`GET /worklist`) and accepts step
  events (`POST /event`) which it writes — append-only, timestamped,
  with the **sensor reading that gated each step** — into **SQLite**.
  *Done when:* you can pull a worklist and see an immutable audit row
  per completed step, including which sensor value opened/blocked it.

### Layer S — Sensors (woven through, do alongside 4/5/7)

- [ ] **Understand:** the [sensor suite](03-mycobot-280-impl/sensor-suite.md)
  — 3 cameras, gripper feedback, load cell, balance, presence, safety,
  IMU — and the off-arm payload rule.
- [ ] **Hello world — "subscribe to a sense":** echo a **simulated
  force-torque** or **IMU** topic from Gazebo (or the gripper
  **effort**) and print a PASS/FAIL when it crosses a threshold. *Done
  when:* a number from a simulated sensor drives a boolean gate — the
  atom that makes the whole cell non-blind.

---

## Part C — The capstone "hello cell" (½ day, day 4)

Chain the hello worlds into the **smallest end-to-end loop**, because
*this* is what you screen-record for the pitch:

- [ ] **One vial, start to finish, in sim:** `read worklist (L8)` →
  `locate vial via tag (L4)` → `pick + verify hold (L5+S)` →
  `call mock /decap (L2)` → `place in tray slot + verify seated (L3+L4)`
  → `log every step + its gating sensor to the audit trail (L8)`,
  all sequenced by the **behavior tree (L7)**.
- [ ] **Record a 60–90 s screen capture** of it running in Gazebo/RViz
  with the audit log scrolling. This clip is your proof-of-competence
  attachment / demo.

**Done with Part C when:** you have a single command that runs one vial
through the loop in sim, and a recording of it.

---

## Part D — The conversation (do in parallel, finalize day 4)

Learning the tools is half the job; you also have to **sell and scope**.

- [ ] **Discovery questions to ask a prospect** (write these on a card):
  - What's the task today, who does it, how many hours/day?
  - What does an error cost (a re-run, a ruined sample, downtime)?
  - Regulated environment? (GxP / 21 CFR Part 11 / ISO?)
  - Fixed station or does it need a flexible arm?
  - What instruments / software must we integrate with (LIMS, CDS)?
  - Throughput target, footprint, budget range, timeline?
- [ ] **Map their problem onto our 8 layers** live — practice on 3 made-up
  prospects (a pipetting lab, a kitting line, a shelf-stocking store) so
  you can do it on the call.
- [ ] **The wedge / ROI language:** technician-hours saved, fewer
  re-runs, walk-away/overnight throughput, **flexibility** vs fixed
  liquid handlers (Hamilton/Tecan/Opentrons). See
  [`03-mycobot-280-impl/10-hardware-platform-and-capital-model.md`](03-mycobot-280-impl/10-hardware-platform-and-capital-model.md).
- [ ] **Honest scoping** — be able to say clearly **what simulation
  proves** (layout, reachability, sequencing, perception pipeline,
  software/audit, cycle-time *estimates*) and **what needs hardware**
  (grasp friction on glass, decap torque, dispense accuracy, optics on
  clear glass, IQ/OQ/PQ). Over-promising here is the fastest way to lose
  trust. See "What sim can and can't prove" in the impl READMEs.
- [ ] **Know the arm trade-offs** so you can answer "what hardware?" —
  skim [`05-arms-comparison.md`](05-arms-comparison.md) (myCobot 280 vs
  reBot vs PiPER) and why we'd dev on a cheap arm and deploy on a bigger
  one.
- [ ] **Draft the cold email** (3–4 sentences): who we are, the sim-first
  approach, the HPLC demo clip as proof, one sentence of ROI, a soft ask
  for a 20-minute call. Keep one reusable template + a per-company line.

**Done with Part D when:** anyone on the team can take a cold problem,
map it to the 8 layers, name what's sim vs hardware, and give a
ballpark ROI — without notes.

---

## The 3–4 day plan at a glance

| Day | Morning | Afternoon |
|-----|---------|-----------|
| **1** | Part A landscape; Layer 0 setup (ROS 2 + Gazebo) | Layer 1 (spawn the cell) + Layer 2 (mock decapper) |
| **2** | Layer 3 (reach the vial / MoveIt) | Layer 4 (see the tray) + Layer S (sense → gate) |
| **3** | Layer 5 (grab the vial) | Layer 6 (read ID) + Layer 7 (per-vial BT) |
| **4** | Layer 8 (mock LIMS + audit) | Part C capstone + record clip; Part D conversation prep |

> **If you only have 3 days:** drop the bonus items (OpenCV rim find,
> MoveIt Servo, multiple prospects), and treat Contact-GraspNet,
> MuJoCo, and real SiLA 2 as *read-only* (know the comparison, skip the
> hello world). The capstone (Part C) and Part D are **not** optional —
> they're what the pitch rests on.

---

## Definition of done (the whole checklist)

You're ready to send the email and take the call when, as a team, you
can:

- [ ] Stand up the **digital twin** (arm + vial + tray in Gazebo/RViz).
- [ ] **Plan and execute** a collision-free arm motion in sim.
- [ ] **Detect** a fiducial and print its pose; find the vial.
- [ ] **Grasp** the vial and **verify the hold** from sensor feedback.
- [ ] **Decode** a vial barcode and map it to a worklist.
- [ ] Run a **behavior tree** that retries/quarantines on a failed gate.
- [ ] Serve a **worklist** and write an **append-only audit trail**.
- [ ] Run the **end-to-end one-vial loop** and show the recording.
- [ ] **Explain every layer** to a non-robotics buyer and **map their
  problem** onto it, honestly scoping sim vs hardware.

---

## See also

- The stack these hello worlds build:
  [`03-mycobot-280-impl/01-only-code/`](03-mycobot-280-impl/01-only-code/README.md)
  (and the hardware-mode sibling
  [`02-code-plus-hardware/`](03-mycobot-280-impl/02-code-plus-hardware/README.md)).
- The problem being demoed:
  [`01-high-level-solution/`](01-high-level-solution/README.md).
- Sensors, in depth:
  [`03-mycobot-280-impl/sensor-suite.md`](03-mycobot-280-impl/sensor-suite.md).
- Which arm to actually buy: [`05-arms-comparison.md`](05-arms-comparison.md).
- Robotics vocabulary:
  [`../03-place-items-on-shelf/02-glossary.md`](../03-place-items-on-shelf/02-glossary.md).
- The wider strategic picture: [`../README.md`](../README.md).
