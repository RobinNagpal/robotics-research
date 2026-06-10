# Synthetic-Data Services: What We Can Sell, To Whom, and What to Learn

> **Job:** Companion to
> [`SIMULATION-SERVICES.md`](SIMULATION-SERVICES.md). That file covers
> the full simulation service catalog; this one goes deep on the
> single biggest line inside it — **synthetic data** (Task B in
> [`GOAL.md`](GOAL.md)). It lists the **types of synthetic-data work**
> we can deliver to the companies in
> [`04-outreach/01-companies.md`](04-outreach/01-companies.md), maps
> them to the sectors that buy, adds the offshore-delivery specifics,
> and ends with a **learning checklist**.

**Plain-language note.** *Synthetic data* is training/testing data
that is **generated** rather than collected: images, depth maps,
lidar scans, or whole robot trajectories rendered from a simulated
scene, with **labels produced automatically** (the renderer knows
where every object is, so every box, mask, and pose comes free and is
pixel-perfect). The buyer's question is always the same: *does a
model trained on your generated data work on my real robot?* —
everything in this file is organized around answering yes, with
evidence.

---

## 1. Why robotics companies buy synthetic data

- **Real data collection doesn't scale.** A warehouse robot meets
  thousands of new SKUs; a weeding robot meets every growth stage of
  every weed in every light. Photographing and hand-labeling all of
  it costs more per image than rendering, and hand labels carry
  errors; rendered labels don't.
- **The long tail is unphotographable.** The cases that break robots
  — torn boxes, overlapping vials, a weed half-hidden by a crop leaf,
  a person stepping out from behind a shelf — are rare, dangerous, or
  unethical to stage. In a renderer they are one parameter change.
- **Some data is locked away.** Surgical video is privacy-bound and
  regulated; defect imagery belongs to the client's customers.
  Synthetic stand-ins are often the only data that can legally exist
  at scale.
- **New product, no data.** Every company shipping a new robot or
  entering a new site starts with zero examples. Synthetic data is
  how they bootstrap perception before the first deployment.

---

## 2. The service lines (types of synthetic-data work)

Six lines, ordered roughly from easiest-to-sell to most advanced.
Lines 2.1–2.2 are the same Task B already chosen in
[`GOAL.md`](GOAL.md), made concrete.

### 2.1 Detection & segmentation imagery (the bread and butter)

Rendered RGB images with automatic bounding boxes and segmentation
masks, **domain-randomized** (lighting, textures, camera pose,
clutter, backgrounds) so models generalize to reality. This is the
highest-volume, most-requested form: *"50,000 labeled images of our
30 SKUs in tote/conveyor scenes."* Deliverable is the dataset in the
client's format (COCO, YOLO, …) **plus the generation pipeline**, so
adding SKU #31 is a re-run, not a new project.

Typical tools: **Isaac Sim Replicator**, **BlenderProc**, **Unity
Perception**; the scene assets come from the digital-twin work in
[`SIMULATION-SERVICES.md` §2.1](SIMULATION-SERVICES.md).

### 2.2 Manipulation labels: depth, 6-DoF pose, grasp points

Picking robots need more than boxes: per-pixel **depth**, full
**6-DoF object pose** (position + orientation), **keypoints**, and
**grasp annotations** (where a gripper or suction cup can hold the
object). These labels are nearly impossible to hand-annotate on real
images and trivial to emit from a renderer — which is why
manipulation companies are the natural synthetic-data buyer.

### 2.3 Non-camera sensor data

Simulated **lidar point clouds**, **thermal**, **radar**,
**ultrasonic/sonar**, and **IMU** streams with realistic noise
models. Fewer vendors can do this, so it commands better margins:
inspection robots (ultrasonic wall-thickness), maritime robots
(sonar), and outdoor autonomy (lidar in dust/rain/fog) all need it.
Builds directly on the sensor-simulation line
([`SIMULATION-SERVICES.md` §2.5](SIMULATION-SERVICES.md)).

### 2.4 Rare-event & edge-case datasets

Deliberately generated *hard* data: occlusions, damaged goods,
defects on inspection surfaces, sensor glare, people in the robot's
path, spills. Sold either as training data (teach the model the long
tail) or as **test sets** (prove the client's perception fails
gracefully — which feeds their safety case). Recurring by nature:
every field incident becomes a new chapter of the library.

### 2.5 Demonstration & trajectory data for robot foundation models

The newest market: VLA / foundation-model companies train on **robot
episodes** (observations + actions over time), not single images. We
collect demonstrations by teleoperating in sim, then **multiply**
them — MimicGen-style augmentation turns tens of human demos into
thousands of varied synthetic ones across randomized scenes.
Highest skill bar, least competition, and the best-funded buyers
(the entire humanoid sector).

### 2.6 Dataset engineering & validation

The meta-service that makes the rest credible, sold standalone to
clients who already generate their own data:

- **Sim-to-real gap measurement** — train on synthetic, evaluate on
  a curated real test set, report where and why it breaks.
- **Real + synthetic mixing studies** — find the blend that maximizes
  accuracy per labeling dollar.
- **Dataset QA & curation** — de-duplication, class-balance audits,
  label-error detection on the client's *real* datasets.
- **Pipeline hardening** — turn a researcher's render script into a
  versioned, one-command, CI-run data factory.

| # | Service line | Deliverable | Effort to learn | Demand |
|---|--------------|-------------|-----------------|--------|
| 2.1 | Detection/segmentation imagery | Labeled image sets + pipeline | Low — Task B in [`GOAL.md`](GOAL.md) | Broadest |
| 2.2 | Depth / pose / grasp labels | Manipulation datasets | Medium | High (picking) |
| 2.3 | Non-camera sensor data | Lidar/thermal/sonar sets | Medium–high | Niche, good margin |
| 2.4 | Rare-event & edge cases | Long-tail train/test sets | Medium | High, recurring |
| 2.5 | Demonstrations / trajectories | Episode datasets | High | Hot, uncrowded |
| 2.6 | Dataset engineering & validation | Reports + hardened pipelines | Medium | Cross-sells everything |

**Bottom line:** sell **2.1** first (it is literally the
[`GOAL.md`](GOAL.md) Task B portfolio), attach **2.6** to every deal
(the validation report is what makes a prospect trust us), grow into
**2.2/2.4** with picking and safety-minded clients, and build toward
**2.5** because that is where humanoid money is going.

---

## 3. Mapping services to the outreach sectors

Sectors are the seven sections of
[`04-outreach/01-companies.md`](04-outreach/01-companies.md).

| Sector (from the list) | Synthetic data they need | Best-fit lines | Example prospects |
|---|---|---|---|
| 1. Humanoids & general-purpose intelligence | Manipulation episodes at scale, dexterous-grasp labels, household/factory object variety | 2.5, 2.2, 2.1 | Dyna, Sunday, mimic, Flexion, Galbot, Tacta |
| 2. Warehouse, logistics & manufacturing | Per-SKU detection sets, grasp/pose labels for picking, damaged-parcel edge cases | 2.1, 2.2, 2.4 | Sereact, Nimble, Dexterity, Nomagic, Pickle, Contoro |
| 3. Agriculture, construction & energy | Crop/weed imagery across growth stages & weather, dusty-lidar data, terrain edge cases | 2.1, 2.4, 2.3 | Carbon Robotics, Ecorobotix, Bonsai, Tevel, Four Growers |
| 4. Medical, surgical & lab automation | Privacy-free surgical/anatomy imagery, instrument pose, validation evidence for regulators | 2.1, 2.6, 2.4 | ForSight, Vitestro, Mendaera, CMR Surgical, Automata |
| 5. Drones, maritime, inspection & defense | Defect imagery (corrosion, cracks), sonar/ultrasonic/thermal data, degraded-visibility edge cases | 2.3, 2.4, 2.6 | Gecko*, ANYbotics, Voliro, Aerones, Square Robot |
| 6. Service, delivery, consumer & recycling | Waste-stream and food-item variety, pedestrian/sidewalk edge cases, in-home object diversity | 2.1, 2.4 | Glacier, AMP, Starship, Coco, Chef Robotics, Matic |
| 7. Mixed (tractors, yard trucks, indoor drones) | Barcode/inventory imagery, trailer/yard object detection, orchard-row variety | 2.1, 2.6 | Corvus, Gather AI, Simbe, Outrider, Burro |

\* Defense-funded prospects carry export-control restrictions for an
offshore vendor — see
[`SIMULATION-SERVICES.md` §4](SIMULATION-SERVICES.md).

**Where the pain is sharpest:**

- **Warehouse (2) is the volume buyer.** Every onboarding of a new
  customer site means hundreds of new SKUs to recognize and grasp —
  a *per-SKU, per-site* recurring sale of 2.1 + 2.2. This is the
  beachhead.
- **Recycling & food (in 6) is warehouse's twin.** Infinite object
  variety (crushed bottles, mixed ingredients) with no catalog to
  photograph — Glacier and AMP literally cannot collect what they
  need to see.
- **Agriculture (3) buys seasons.** A weed model can only be trained
  on real data once a year; synthetic growth-stage imagery is how
  they iterate in winter. Lighting/weather randomization skills carry
  straight over from 2.1.
- **Medical (4) buys legality.** Synthetic anatomy/instrument imagery
  sidesteps patient privacy entirely, and the 2.6 validation report
  speaks the regulatory language (evidence, traceability) they
  already live in.
- **Humanoids (1) buy episodes, not images.** They have in-house data
  engines but are bottlenecked on environment and demonstration
  variety — sell 2.5 as capacity, priced per validated episode batch.
- **Inspection (5, civilian) buys what cameras can't see.** Defect
  and ultrasonic/thermal data (2.3/2.4) for companies like Gecko and
  Voliro — few competitors can simulate their sensors at all.

**Bottom line:** open with **sector 2 plus the recycling/food slice
of 6** (the per-SKU recurring model), use **agriculture (3)** as the
second beachhead in the off-season, and treat **2.5 for humanoids**
as the build-toward prize. Defense stays out of scope for the
offshore entity, as established in
[`SIMULATION-SERVICES.md` §4](SIMULATION-SERVICES.md).

---

## 4. Offshore delivery: what's specific to synthetic data

The company setup — entity, compute, NDA/IP hygiene, export-control
policy, team shape — is shared with the simulation services and
already covered in [`SIMULATION-SERVICES.md` §4](SIMULATION-SERVICES.md).
What is *different* when the product is data:

- **Acceptance is a number.** Every SOW should name the metric and
  the test set up front: *"YOLO trained on our synthetic data reaches
  ≥ X% mAP on a held-out set of N real images supplied by you."* This
  protects both sides and forces the quality bar into the contract.
- **Price the pipeline, not the pixels.** Per-image pricing races to
  the bottom (render farms are cheap). Price the *capability*: a
  fixed fee for the tuned pipeline + asset setup, then a modest
  per-batch or per-new-SKU fee. The pipeline handoff is also our
  differentiator versus dataset marketplaces.
- **The client's real data is the crown jewels.** To validate, the
  client sends us real images of their sites, products, or failures —
  often their most sensitive asset. Per-client isolation, encrypted
  transfer, deletion-on-completion clauses, and (for medical) written
  data-handling procedures are not optional.
- **Licensing flows into the dataset.** Every 3D asset, texture, and
  HDRI used in a render licenses the *output*. Keep an auditable
  asset manifest per dataset; ship only assets we may redistribute.
  One contaminated texture pack can poison a deliverable.
- **The honest threat is generative AI.** Diffusion/world models are
  starting to generate plausible training imagery without 3D scenes.
  Our defense: physics-grounded labels (pose, depth, grasp, contact —
  things image generators can't label), non-camera sensors (2.3), and
  the validation discipline (2.6). Pure pretty-picture rendering will
  commoditize first; stay above it.
- **Turnaround is the offshore superpower.** Dataset work is
  iterative ("more occlusion, fewer reflections, re-render"). An
  overnight iteration loop against a US/EU client's review cycle is
  a structural advantage — say so in the pitch.

---

## 5. Learning checklist

Builds on two things: the HPLC stack checklist
([`02-hplc-autosampler/06-learning-checklist.md`](02-hplc-autosampler/06-learning-checklist.md))
for ROS 2 / Gazebo / YOLO foundations, and Parts A–C of the
[`SIMULATION-SERVICES.md` checklist](SIMULATION-SERVICES.md) for
simulators and the asset pipeline (scenes are the raw material of
data). This list adds the *data-side* skills. Tick items as you go;
each part has a **Done when** bar.

### Part A — Perception-ML literacy (judge data like a buyer)

We sell to ML engineers; we must speak evaluation fluently.

- [ ] **Train a detector properly** — YOLO on a public dataset:
  train/val/test split discipline, when to stop, what overfitting
  looks like.
- [ ] **Metrics fluency** (one sentence each): **precision, recall,
  mAP, IoU, confusion matrix** — and segmentation/pose equivalents.
- [ ] **Label taxonomy** — know every label type we might sell:
  boxes, instance/semantic masks, keypoints, 6-DoF pose, depth,
  optical flow, grasp annotations; and the file formats (COCO, YOLO,
  Pascal VOC, BOP for pose).
- [ ] **Read 2–3 published sim-to-real synthetic-data write-ups**
  (NVIDIA Replicator case studies, BlenderProc papers, the
  Sereact/Galbot-style "trained largely on synthetic data" posts in
  our own outreach list) to learn the buyer's vocabulary and honest
  failure modes.

**Done when:** shown someone else's dataset, anyone on the team can
critique it (class balance, label quality, gap risks) in ML terms.

### Part B — The rendering & randomization stack (service line 2.1)

- [ ] **Isaac Sim Replicator end-to-end** — ketchup scene → RGB +
  boxes + masks; write randomizers for lighting, materials, camera,
  and distractor clutter.
- [ ] **BlenderProc end-to-end** — same scene, open-source route;
  understand the photorealism-vs-throughput trade and when each
  wins.
- [ ] **PBR rendering basics** — materials, HDRI environment
  lighting, why physically-based rendering narrows the sim-to-real
  gap.
- [ ] **Scale it** — render 10k+ images headless (batch/cloud),
  with seeds and config files so any batch is exactly reproducible.
- [ ] **Dataset packaging** — auto-generated datasheet per dataset:
  contents, class counts, randomization ranges, asset manifest +
  licenses, known limitations.

**Done when:** one command produces a reproducible, documented,
10k-image labeled dataset from any of our scenes.

### Part C — Manipulation & advanced labels (service line 2.2)

- [ ] **Emit depth and 6-DoF pose** from the renderer; visualize and
  sanity-check them (re-project poses onto images).
- [ ] **Grasp annotation** — generate analytical grasp/suction
  points for our asset pack (ties into the grasping layer of the
  HPLC stack) and export them in a documented format.
- [ ] **Train one pose or grasp model** on our synthetic output —
  even a small one — to prove the labels are consumable.

**Done when:** our ketchup-scene dataset carries boxes, masks,
depth, pose, *and* grasp labels, and at least one model has trained
on each label type.

### Part D — Non-camera sensors & edge cases (service lines 2.3, 2.4)

- [ ] **Simulated lidar** — generate point clouds from a scene in
  Gazebo or Isaac; add a realistic noise/dropout model.
- [ ] **One exotic sensor study** — read how thermal, ultrasonic,
  *or* sonar is simulated (pick whichever target sector we pursue
  first); know the honest limits.
- [ ] **Build an edge-case generator** — parameterize one scene for
  failure modes (occlusion %, damage, glare, spills) and produce a
  graded-difficulty test set with a manifest.
- [ ] **Degraded conditions** — render the same scene in dust / fog /
  low light / motion blur and measure how much a trained detector
  degrades (that measurement *is* the sales demo for 2.4).

**Done when:** we can show a client a "hard cases" test set that
measurably stresses a model trained on clean data.

### Part E — Validation discipline (service line 2.6, the trust-maker)

- [ ] **Build a real test set** — photograph ~50–100 real images of
  our ketchup-scene objects, label them carefully once; this is our
  permanent measuring stick.
- [ ] **Run the gap experiment** — train synthetic-only, evaluate on
  real; then synthetic + a few real images; chart accuracy vs. % real
  data. Write up the result honestly.
- [ ] **Ablate the randomizers** — turn randomizations off one at a
  time and measure which ones actually buy real-world accuracy.
- [ ] **Template the report** — turn the above into the standard
  validation report we attach to every dataset deliverable.

**Done when:** we have a one-page, numbers-backed validation report
format that any prospect's ML lead would accept as evidence.

### Part F — Demonstrations & business (service line 2.5 + founder track)

- [ ] **Record sim demonstrations** — teleoperate a pick task in
  sim, save episodes in a standard format (e.g. LeRobot dataset
  format); know what observation/action streams VLA trainers expect.
- [ ] **Study demo augmentation** — read MimicGen (and successors)
  closely enough to scope a "tens of demos in → thousands out"
  engagement.
- [ ] **Pricing sheet** — draft pipeline-fee + per-batch pricing for
  2.1/2.2 and per-episode-batch pricing for 2.5, with the acceptance
  metric named in each.
- [ ] **Data-handling one-pager** — our written policy for client
  real-data custody (isolation, encryption, deletion) to attach to
  proposals; medical prospects will ask first.
- [ ] **Case study** — package the Part E gap experiment as the
  public portfolio piece for cold outreach.

**Done when:** we can answer a prospect's "how do you price it, how
do you prove it works, and how do you handle our data?" with three
documents already written.

---

## 6. Suggested order of attack

1. **Finish [`GOAL.md`](GOAL.md) Task B** (ketchup, then paracetamol
   datasets) — it is Parts B + E in disguise and produces the
   portfolio and validation report.
2. **Parts A–B** across the team, in parallel with the
   [`SIMULATION-SERVICES.md`](SIMULATION-SERVICES.md) checklist
   (shared scenes, shared tools — do them together).
3. **Part E early** — the validation report is the single most
   persuasive sales artifact; build it before broad outreach.
4. **Parts C–D** as warehouse/recycling pilots demand manipulation
   labels and edge cases.
5. **Part F's demo work** when targeting the humanoid sector.

*Tool versions, license terms, metrics, and company details drift —
re-verify anything in this file before quoting it to a prospect.*
