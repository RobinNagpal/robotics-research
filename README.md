# Robotics Subfields — Strategic Research

A scan of the robotics landscape, filtered for **software-primary**, **complex**,
**growing**, **well-paid**, and **shippable as a small project** subfields.

The 9 subfields below cover the meaningful territory. The 3 marked with `[*]`
score highest across every criterion and are detailed further down.

## Subfield map

```
                        +-- [*] Perception & Computer Vision  (3D, pose, NeRF, Gaussian splat)
            PERCEPTION -+
           /            +--     SLAM & Navigation             (LiDAR, visual-inertial, planning)
          /
         /              +-- [*] Robot Learning & Foundation   (VLA: RT-2, OpenVLA, pi0, GR00T)
         |              |       Models
ROBOTICS +-- COGNITION -+
         |   / AI       +--     HRI & Language Interfaces     (LLM-on-robot, speech, dialogue)
         |
         |              +--     Motion Planning & Control     (MPC, RL control, trajectory opt.)
          \             |
           \  ACTION   -+--     Manipulation & Grasping       (dexterous, bin-pick, tactile)
            \           |
                        +-- [*] Simulation & Digital Twins    (Isaac Sim/Lab, MuJoCo, Sim2Real,
                        |                                      synthetic data)
                        |
                        +--     Multi-Robot & Swarm Systems   (fleet coordination, MARL, consensus)
                        |
                        +--     Robotics Infra & Middleware   (ROS2, DDS, observability, CI)

  Legend:  [*] = top-3 pick (highest score across all criteria)
```

## How the 9 were chosen

Robotics is huge, so the filter was strict: software-primary, complex, growing,
well-paid, and shippable as a small project. The 9 above cover the meaningful
territory; the rest (industrial controls/PLCs, mechanical design, sensor
electronics, RF/comms) are explicitly hardware-heavy or low-growth and were
excluded by design.

The three marked `[*]` score highest across every criterion. The case for
each follows, pressure-tested against current job-market data (Robotics
Salary Guide 2025, 907 jobs analyzed Nov-Dec 2025) and the latest
market-size forecasts.

---

## Top 3 focus areas — detailed

### 1. Robot learning & foundation models (VLA / embodied AI)

This is the hottest area in robotics right now and the one where a small team
can punch far above its weight, because the entire field is being rebuilt
around foundation models.

- **Software-primary?** Yes — almost entirely ML/Python/PyTorch work. Hardware
  is optional (fine-tune and evaluate on public datasets like Open
  X-Embodiment, LIBERO, RoboCasa, or simulator-only).
- **US jobs growth (last 3 yrs):** ML Engineer roles are the second-highest
  paying IC track in robotics and one of the fastest-growing. Robotics
  Software & AI as an industry pays a $198k median. The skill "Reinforcement
  Learning" carries a +33% salary premium, and ML appears in ~31% of all
  robotics job postings.
- **Pay in US:** Median $200k for ML engineers, $180k-$250k at premium
  employers. NVIDIA pays $270k median for robotics-AI roles, Waymo $232k,
  Shield AI $228k. Physical Intelligence (the leading VLA startup) raised
  $400M at a $2.4B valuation.
- **Hardware involvement:** Minimal. A rented GPU is enough. Demos work in
  simulators or on commodity arms ($3k-$10k SO-100, LeRobot).
- **5-year growth and why:** Embodied AI market projected from $3.3B in 2026
  to $11.7B by 2035 (15.5% CAGR). Healthcare robotics 26% CAGR through 2030.
  VLA models (RT-2, OpenVLA, pi0, Figure Helix, NVIDIA GR00T) are replacing
  decades of bespoke per-task code with general-purpose policies.

**4 projects (each <= 1 month):**

1. **VLA fine-tuning service for niche tasks.** Take OpenVLA-7B or pi0-base,
   build a clean fine-tuning pipeline that takes 50-200 customer
   demonstrations and produces a deployable policy for a specific repetitive
   task (warehouse pick-pack subtypes, lab pipetting, retail shelf-stocking).
   Sold to integrators who don't have ML staff. ~3 weeks.
2. **Synthetic demonstration generator.** Tool that takes a single human
   teleoperated demo and generates 1,000+ augmented variations (object
   positions, lighting, distractors) for VLA training. Sells as a SaaS credit
   pack to robotics startups burning cash on data collection. ~3 weeks.
3. **VLA evaluation harness.** Most teams have no rigorous way to compare
   policies. Build a benchmark service: upload a policy checkpoint, get back
   success rates across standard manipulation suites (LIBERO, RoboCasa,
   Meta-World), generalization scores, failure-mode taxonomies, and PDF
   reports. ~2-3 weeks.
4. **Natural-language -> robot task DSL.** A web tool where a non-technical
   operator types "pick up red blocks and place them in the bin on the left,
   ignore green ones" and outputs a structured task spec + few-shot examples
   that a downstream VLA consumes. Demoable on a sim arm. ~4 weeks.

---

### 2. Perception & computer vision (3D, SLAM, 6-DoF pose)

The workhorse layer of every robot. Always in demand, currently being upended
by neural representations (NeRF, Gaussian splatting, learned depth).

- **Software-primary?** Yes — Python/C++, PyTorch, OpenCV, Open3D. Hardware
  is a USB camera or a public dataset.
- **US jobs growth (last 3 yrs):** One of the most active sub-segments. The
  global CV market was $19.82B in 2024 and is growing at 19.8% CAGR through
  2030. "Computer Vision Engineer" is one of the named trending titles in
  2025 hiring reports.
- **Pay in US:** Robotics Software Engineer median $189k; perception
  specialists in AV hit $200k+. SLAM/perception roles at Waymo/Cruise are
  in the $200k-$260k base range before equity.
- **Hardware involvement:** Light — a single camera (often a laptop webcam
  or iPhone) is enough for most demos. Optionally a depth camera ($200 Intel
  RealSense). No actuators needed.
- **5-year growth and why:** Three converging tailwinds. (a) Every humanoid,
  AMR, AV, and drone needs perception. (b) Gaussian splatting and learned 3D
  are mainstream now, opening a wave of new product surfaces (digital twins
  from a phone scan, automatic CAD-from-reality). (c) Foundation models
  (SAM 2, DINOv2, Depth-Anything) make once-hard problems tractable in days.

**4 projects (each <= 1 month):**

1. **Phone-scan -> robot-ready 3D environment.** User walks around a room
   with their phone; service returns a Gaussian splat + collision mesh +
   semantic segmentation suitable for loading into Isaac Sim or Gazebo.
   Direct sell to robotics teams that need digital twins of customer sites.
   ~4 weeks.
2. **6-DoF pose estimation API for industrial parts.** Customer uploads a
   CAD model; service returns a fine-tuned FoundationPose / MegaPose
   checkpoint and a REST endpoint that returns 6-DoF pose from an RGB-D
   image. Sells to bin-picking integrators. ~3 weeks.
3. **Visual-inspection-as-a-service.** Web UI where a customer uploads 50
   "good" and 50 "bad" product images, you train an anomaly-detection model
   (PatchCore, EfficientAD) and deliver a deployable container. QC
   departments pay well for this. ~2-3 weeks.
4. **Real-time SLAM benchmark + tuning service.** Tool that ingests a
   customer's ROS bag, runs ORB-SLAM3 / VINS-Fusion / OpenVSLAM, and produces
   a tuning report with parameter recommendations and accuracy comparisons.
   Sells to drone and AMR teams. ~3 weeks.

---

### 3. Simulation & digital twins (Sim2Real, Isaac Sim, MuJoCo)

The dark horse — least hardware involvement of all three, and the
fastest-growing market segment in robotics by CAGR.

- **Software-primary?** Most pure of the three. Zero hardware. Everything
  happens in a simulator on a GPU.
- **US jobs growth (last 3 yrs):** Strong and accelerating. NVIDIA hired
  aggressively around Isaac Sim/Lab through 2024-2025. The Robotic Simulator
  market is software-dominated (72% software share in 2025). Roles often sit
  inside ML Engineer or Robotics Software Engineer postings, inheriting
  those salary bands.
- **Pay in US:** Inside Robotics Software & AI ($198k median) and
  Transportation/AV ($200k median) industries. NVIDIA roles in this area are
  in the $200k-$300k range.
- **Hardware involvement:** None to ship the software. A real robot is
  helpful for validation but not required to deliver value to customers —
  many customers will use the output to skip buying real hardware until later.
- **5-year growth and why:** Physical-AI simulation & digital-twin market
  projected to grow from $3.8B in 2025 to $34.6B by 2034 — a **28.5% CAGR**,
  the highest of any segment in this analysis. Drivers: humanoid and AMR
  companies need massive synthetic training data, Sim2Real is now the
  dominant policy-training paradigm, and digital twins are how warehouse
  and factory customers buy automation.

**5 projects (each <= 1 month):**

1. **Custom Isaac Lab training environment as a service.** Customer
   describes a task and provides assets; you deliver a parameterized Isaac
   Lab environment with domain randomization, reward shaping, and a baseline
   PPO/SAC training script. ~3-4 weeks.
2. **Procedural warehouse / factory generator.** Tool that takes a CAD floor
   plan and generates 100s of randomized USD scenes (lighting, object
   placement, clutter, agents) for training mobile robots. Sells to AMR
   companies. ~4 weeks.
3. **Sim2Real domain randomization toolkit.** A Python package + small web
   UI that wraps Isaac Sim / MuJoCo and exposes randomization knobs
   (physics, textures, lighting, dynamics) with sensible presets per robot
   type. License + support. ~3 weeks.
4. **Synthetic data pipeline for vision models.** Customer specifies object
   classes and a scene type; you return 100k labeled synthetic images + 3D
   bounding boxes for training detectors/pose-estimators. Sells well to
   defense and industrial QC. ~3 weeks.
5. **Policy regression-test harness.** CI-style service that re-runs a
   customer's policy nightly across a fixed scenario suite, alerts on
   regressions, and produces dashboards. Robotics teams have nothing like
   this today. ~4 weeks.

---

## Quick scorecard

| Subfield                  | Software-primary | US salary (median) | 3-yr job growth | 5-yr market CAGR | Hardware needed |
|---------------------------|------------------|--------------------|-----------------|------------------|-----------------|
| Robot learning / VLA      | Very high        | ~$200k (ML eng)    | Very high       | ~15-25%          | Optional        |
| Perception / CV           | Very high        | $189k-$200k+       | High            | ~19.8%           | Light (camera)  |
| Simulation / digital twins| Highest          | ~$200k (robotics-AI/AV) | High       | **~28.5%**       | None            |

## Recommended ordering

For a small team that wants to ship and sell, start with **simulation/digital
twins** (fastest market growth, zero hardware, every robotics startup needs
this) and **perception** projects (easiest to demo, broadest customer base),
then layer in **VLA fine-tuning** services once you have customer
relationships from the first two.
