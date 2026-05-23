# Five Projects You Can Build and Sell

Each scoped to 2-4 weeks of solo work, with a concrete buyer, and
reusing skills a web developer already has (FastAPI / Express, Docker,
React, GitHub Actions). The simulation-specific parts are clearly
flagged.

A note on pricing: ranges below are realistic for **2025-2026 in North
America / Western Europe**. NVIDIA-ecosystem startups and robotics
primes pay the high end; SMB manufacturers and seed-stage robotics
startups pay the low end. Always quote a fixed-fee "discovery phase"
first ($2-5k) to de-risk both sides.

---

## 1. Custom Isaac Lab training environment as a service (~3-4 weeks)

**What you're selling.** A customer (a robotics startup, a research
lab, a defense integrator) describes a task they want to train a
policy for and provides assets (URDF / CAD / scan). You deliver a
**parameterized Isaac Lab environment** with proper domain
randomization, reward shaping, and a baseline PPO / SAC training
script that converges out of the box.

**Why it works.** Isaac Lab is rapidly becoming the standard, but
its learning curve is real — its abstractions (ManagerBased vs.
Direct workflows, AssetCfg, ActionTerm) are not obvious to a fresh
RL engineer. Many startups need *one* trained policy fast and have
no in-house Isaac Lab specialist. You sit in that gap.

**Stack:**
- **Isaac Sim 4.x + Isaac Lab** for the env and training loop.
- **USD asset cleanup** with NVIDIA's Asset Validator + custom
  Python; SimReady metadata.
- **Replicator** for domain randomization.
- **W&B** for experiment tracking; the customer gets a shared
  dashboard.
- Custom **Hydra / OmegaConf** config so the customer can sweep
  parameters without touching code.

**Pricing:** $15-60k per environment + $2-5k/month retainer for
updates, retraining, and adding new task variants.

**What you need first:** one open-source reference env you've built
end-to-end (publish on GitHub). Use it as the proof artifact in
sales calls.

---

## 2. Procedural warehouse / factory generator (~4 weeks)

**What you're selling.** A tool that takes a CAD floor plan (or a
parametric description: "30m x 50m, 200 shelves, 12 charging
stations") and emits **hundreds of randomized USD scenes** —
varying lighting, shelf layouts, object placement, clutter, agent
positions — ready to load into Isaac Sim or Gazebo for training
mobile robots and perception models.

**Why it works.** AMR (autonomous mobile robot) companies need
massive training-scene diversity. Hiring a 3D artist to make 1,000
warehouses is impossible. Existing tools (Omniverse Kit, BlenderProc)
exist but require deep expertise to wire up. You ship the
opinionated pipeline.

**Stack:**
- **USD Python API** (`pxr`) for scene composition.
- **BlenderProc** for procedural placement when Omniverse is overkill.
- **Replicator** for randomization.
- Optional: an **Omniverse Kit extension** as a GUI for sales demos.
- React + FastAPI front-end where users upload a floor plan and
  pick randomization knobs; S3 for storage; Stripe for billing.

**Pricing:** $20-80k license per OEM + $1-5k/month support
subscription. Alternative SaaS model: $0.50-$2 per generated scene.

**Hardest part:** asset quality. Real-world warehouse photoreal
asset libraries are expensive (Turbosquid, Sketchfab Pro). Budget
$3-5k of asset purchases per major engagement.

---

## 3. Sim2Real domain randomization toolkit (~3 weeks)

**What you're selling.** A Python package + small web UI that wraps
Isaac Sim / MuJoCo and exposes **randomization knobs** (physics,
textures, lighting, dynamics, sensor noise) with **sensible presets
per robot type** (quadruped, manipulator, mobile base, drone, humanoid).
Commercial license + paid support.

**Why it works.** Most robotics teams hand-roll their DR config and
get it wrong (too narrow = brittle real-world performance; too wide
= won't converge). You productize the institutional knowledge of
"what DR ranges actually work for ANYmal locomotion" or "for Franka
pick-and-place."

**Stack:**
- **Isaac Lab + MJX** wrappers.
- A **YAML config DSL** for randomization (or Hydra-compatible).
- Preset templates per robot type, derived from published papers
  (RMA, ANYmal, OpenAI Rubik's Cube, DextrAH).
- **Streamlit** dashboard for live config tuning + sweep
  visualization.

**Pricing:** $5-25k/year license + $2-5k onboarding. Realistic ARR
target after 6 months: $30-100k.

**Why this fits a web dev specifically.** Most of the work is
designing the DSL, the React/Streamlit UI, and Docker packaging —
exactly your wheelhouse. The "novel" piece is curating ~15 robot-
specific presets, which is a literature-search task more than a
research task.

---

## 4. Synthetic data pipeline for vision models (~3 weeks)

**What you're selling.** A customer specifies object classes ("our
30 bracket SKUs") and a scene type ("on a conveyor under industrial
lighting"). You return **100k labeled synthetic images** (RGB +
depth + 2D / 3D bounding boxes + instance segmentation) ready to
train a detector or 6-DoF pose estimator. You also include a quick
fine-tune of YOLO v11 or FoundationPose as a baseline.

**Why it works.** Real labeled data is the bottleneck in industrial
CV. A single labeled image from Scale AI / Labelbox is $0.50-$3.
You generate 100k in a weekend at near-zero marginal cost. The
catch is photoreal quality + sim-to-real validation, both of which
are learnable.

**Stack:**
- **Replicator + BlenderProc** for procedural data + annotations.
- Photoreal PBR materials (Quixel Bridge / Polyhaven free assets).
- Automated **COCO** + **BOP** annotation export.
- Pre- and post-fine-tune evaluation on a customer-held-out
  validation set so you can prove transfer.

**Pricing:** $5-50k per dataset depending on diversity, number of
classes, and required real-data validation.

**Buyers:** defense (counter-UAS, ISR), industrial QC, retail self-
checkout, agriculture.

---

## 5. Policy regression-test harness (~4 weeks)

**What you're selling.** A CI-style service that re-runs the
customer's policy nightly across a **fixed scenario suite**, alerts
on regressions, and produces dashboards + PDF reports. Like
**Sentry / Datadog for robot policies**.

**Why it works.** Robotics teams have models but no rigorous eval
infra. When a checkpoint regresses, nobody notices until a customer
complains. There's nothing off-the-shelf for this. You build it.

**Stack:**
- Dockerized eval workers on GPU; parallel rollouts.
- Wrap LIBERO / RoboCasa / Meta-World + customer's custom Isaac Lab
  envs as reproducible jobs.
- **Failure clustering** with DINOv2 / CLIP embeddings of last-frame
  observations — automatically groups regressions by what went
  wrong.
- **WeasyPrint** PDF report; React dashboard for trend lines.
- **GitHub Actions integration** so PRs trigger nightly runs.

**Pricing:** $500-2k per one-off benchmark run; $1-5k/month
subscription for nightly regression. Pure software, recurring
revenue, no hardware coordination — the easiest of the five to
operate.

---

## How to pick which one to start with

- **Cheapest to start, fastest to revenue:** #5 (policy regression
  harness). No customer assets needed, pure software, recurring
  revenue, broad customer pool.
- **Most defensible long-term:** #1 (Isaac Lab env-as-a-service).
  Every engagement makes you better at Isaac Lab; your library of
  reusable env components compounds.
- **Highest ceiling:** #2 (procedural scene generator). If
  warehouse-twin generation becomes standard, this is an acquisition
  target for NVIDIA / Autodesk / Applied Intuition.
- **Most volume potential:** #4 (synthetic data pipeline). Every
  industrial CV team needs this; the constraint is your time per
  engagement, not demand.
- **Most "pure software developer" feel:** #3 (DR toolkit). A
  package + a dashboard; barely any 3D work.
