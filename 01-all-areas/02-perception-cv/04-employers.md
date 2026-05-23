# Major and New Employers

Who pays perception engineers, and what to know about each. Salary
bands are from levels.fyi, the 2025 Robotics Salary Guide, public
funding rounds, and Glassdoor self-reports. Treat as bands, not
guarantees.

The robotics labor market today resembles the JavaScript ecosystem
in 2014-2015: a small set of blue-chip employers, a hot layer of
Series-B/C scaleups, a long tail of vertical plays, and a defense
slice with no real web analog except Palantir.

See also: `00-basics.md` (recruiter-screen vocabulary),
`01-examples.md` (demo ideas), `02-learn.md` (curriculum),
`03-start.md` (30/60/90 plan), `05-projects.md` (portfolio),
`06-courses.md` (paid / structured options).

## Big tech and established AV / AR labs

Bigger teams, more process, strong mentorship, slower cadence.

- **Waymo (Alphabet)** — AV perception (camera + lidar + radar
  fusion, segmentation, tracking, auto-labeling). C++ + PyTorch on
  TPUs; low-hundreds engineers across perception. Five-round loop:
  two coding (LeetCode-medium with vision twist like IoU), one
  ML/CV depth, one system design, one behavioral. Median TC
  **~$232k**; senior IC $300-450k. SF / Mountain View / Pittsburgh
  / Phoenix. Switcher target: L3 SWE II via referral; cold-apply
  is very hard.
- **NVIDIA** — Isaac, GR00T, Cosmos, FoundationPose. Multiple
  20-80-engineer teams (Isaac SDK, Isaac Sim, GR00T, DRIVE,
  Research). C++ + PyTorch + CUDA + TensorRT. Expect a CUDA /
  parallelism question. Median TC **~$270k**; senior staff $400k+.
  Equity tailwind has been enormous. Switcher target: Solutions
  Engineer or DevRel for Isaac converts into core perception in
  18-24 months and is far more open to non-traditional CVs.
- **Tesla Autopilot / Optimus** — camera-only AV + humanoid.
  Secretive, high-pressure. PyTorch + custom C++; Dojo training.
  Interview emphasizes raw coding speed (two back-to-back LeetCode)
  plus deep CV. Base lower than Waymo; equity-heavy. Switcher: tough
  without a strong from-scratch project on a Tesla-relevant problem
  (monocular depth, BEV segmentation).
- **Mobileye** — vision-centric ADAS. Jerusalem + Detroit + San
  Jose. C++ on custom EyeQ silicon, PyTorch for training. Interviews
  lean classical CV (epipolar geometry, calibration, feature
  matching). Senior IC $230-380k in US, less in Israel. US offices
  more open to non-traditional CVs than HQ.
- **Apple** — Vision Pro, ARKit, camera ISP perception, AV residue
  in Vision Products Group. Metal + CoreML + custom C++. Five-to-
  seven opaque, team-dependent rounds. Senior IC $300-500k. Switcher
  angle: a published ARKit / RealityKit demo helps.
- **Meta Reality Labs** — Aria glasses, SAM, DINOv2. Two sub-orgs:
  FAIR (research, mostly PhDs) and RL Product (ships glasses / Quest,
  eng-heavy). PyTorch. RL Product is standard FAANG-with-CV loop;
  FAIR is faculty-talk style. Switcher target: ML Engineer,
  Perception at RL Product — not FAIR.
- **Boston Dynamics (Hyundai)** — Spot, Atlas. Boston. Tens of
  engineers, tightly coupled to controls. C++ first, internal state-
  estimation frameworks. Interviews heavy on Kalman filters, factor
  graphs, ICP. Senior IC $230-380k. Brand carries real premium on a
  resume.
- **Zoox (Amazon)** — full AV stack, Foster City CA. Amazon
  acquisition pushed comp to Amazon L5/L6 bands but slowed shipping.
  C++ + PyTorch.
- **Cruise (GM)** — re-staffing through 2025 after the 2023 setback.
  Comp competitive, morale historically bruised; watch late 2025 /
  2026 signal.
- **Toyota Research Institute (TRI)** — Cambridge MA + Los Altos.
  Open publication culture, PyTorch + JAX. $230-330k.
- **Symbotic, Amazon Robotics** — warehouse perception at huge
  deployment volume. Java + C++, ROS-adjacent internal frameworks.
  Hires generalists and trains them — excellent switcher target.
- **Skydio** — straddles this tier and defense; see below.

## Defense / dual-use companies (massive growth 2022-2025)

Exploded post-2022 with US/EU defense budgets; comp here often beats
commercial robotics. US citizenship required for almost all roles;
a non-trivial subset needs SECRET clearance (employer-sponsored,
6-12 months).

- **Anduril** (perception ramped 2021+) — Lattice, Ghost, Roadrunner,
  maritime. Low-hundreds across perception. C++ + Rust + PyTorch
  with in-house data/labeling platform. Interview emphasizes systems
  thinking ("design the perception stack for a counter-drone turret
  given these constraints"). Senior IC $350-500k+; equity real but
  illiquid. Switcher target: "Mission Software Engineer" is closer
  to product eng and the most open door.
- **Shield AI** (Hivemind, scaled 2022+) — V-BAT drone + autonomy.
  Tens of perception engineers. C++ + PyTorch + custom middleware.
  Interview more classical (state estimation, SLAM). Median
  **~$228k**, senior IC $300-450k. San Diego primarily.
- **Saronic** (2022) — autonomous surface vessels. Series-B+ 2024
  at $1B+ valuation. Single-digit to low-tens perception team,
  Austin TX. Maritime perception (radar, AIS fusion, horizon
  detection, wave-aware tracking) is its own subspecialty with
  almost nobody experienced — a motivated switcher can ramp faster
  than at an AV company. Must relocate.
- **Helsing** (Germany, 2021) — defense AI, Munich + London + Paris.
  More research-y culture; hires more openly in EU. Senior IC EUR
  150-250k + equity.
- **Skydio** — drones for consumer / defense / public safety.
  Founded 2014, scaled post-2022 after pivoting from consumer.
  Strong VIO/SLAM team, Redwood City CA. C++ + PyTorch with one of
  the most polished on-device perception stacks. Classical CV / SLAM
  heavy interviews. Senior IC $250-400k.
- **Saildrone, Vannevar Labs, HavocAI, Mach Industries** — younger
  dual-use names. Mach (2023) reportedly raised a large Series B in
  2025 for autonomous missiles / drones. Small teams, fast hiring.
- **Palmer Luckey-adjacent and ex-SpaceX founder networks** — 2024-
  2025 defense startups recruit heavily here on LinkedIn and X. A
  credible defense-relevant demo (small-object detection on drone
  video) attracts DMs.

## Perception-heavy startups founded or scaled 2020-2025

Where the explosive growth and comp variance live. Most did not
exist 4 years ago.

- **Wayve** (UK, 2017, Series-C 2024 at **$1B+**) — end-to-end
  driving foundation models. 100+ across perception/learning,
  London + Mountain View. PyTorch + JAX. Research-y loop with a
  paper-discussion round. London more open to non-PhD hires.
  Switcher target: "Engineer, Data & Perception" is eng-heavy.
- **Physical Intelligence (Pi)** (2024) — VLA models with heavy
  perception. $400M Nov 2024 at $2.4B. Under 100 total in 2025,
  enormous talent density (ex-Brain, ex-DeepMind, ex-Tesla).
  PyTorch + JAX. Most research-heavy loop on this list.
  Switcher target: ML engineering / infra roles, not research.
- **Skild AI** (2023, ex-CMU) — robot-agnostic generalist policy.
  $300M Series A July 2024 at ~$1.5B. Small, research-dense,
  PyTorch. Pittsburgh + Bay Area. Easier via CMU robotics network
  than the front door.
- **Figure AI** (2022) — humanoid + Helix VLA. Cumulative >$1.5B
  raised; Feb 2025 valuation talks at $39.5B. Perception grew from
  single-digits to 30-50+ by mid-2025. PyTorch + C++ + NVIDIA Isaac.
  On-site 5 days, Sunnyvale. "Ship in 48 hours" take-home plus
  standard coding. Switcher target: "Robotics Software Engineer"
  funnel is more open than the ML side.
- **1X Technologies** (rebranded from Halodi 2022) — NEO consumer
  humanoid + world-model perception. Norway + SF. PyTorch + C++;
  smaller than Figure. Open to strong generalists.
- **Apptronik** (Apollo humanoid, commercial push 2023+) — Mercedes
  pilots. Austin TX. More eng-than-research, more shipping-focused.
  Hires generalists — very good switcher target.
- **Cobot** (2022, ex-Amazon Robotics VP Brad Porter) — collaborative
  mobile manipulator. Boston, low-tens, strong on manipulation-
  perception interface.
- **Bedrock Robotics** (2023) — autonomous earth-moving. Construction
  is perception-rich and GPS-friendly. Small team, SF.
- **Pickle Robot** (2018, scaled 2023+) — truck-unloading. Cambridge
  MA. Occluded variable-shape boxes are surprisingly hard. Excellent
  switcher target — email the CTO.
- **Field AI** (2023) — outdoor / off-road foundation policies for
  inspection, construction. Mission Viejo / Pasadena. Off-road
  perception (no lane lines, no HD map) is a distinct skillset.
- **Chef Robotics** (2019, scaled past 2023) — food assembly. SF.
  Deformable, occluded, glossy, wet food is close to medical imaging
  in difficulty.
- **Rivr** (2023, Switzerland, ex-ETH) — last-mile delivery robots.
  Lower comp than US; lower cost of living outside Zurich.
- **Polycam, Luma AI, Spline, Scaniverse (Niantic)** — consumer 3D-
  from-photos. Pure software, fast hiring, DX-obsessed, remote-
  friendly. PyTorch + iOS / web frontend, which is gold for an ex-
  web dev. Luma and Polycam have hired from non-traditional backgrounds.
- **Niantic** — recently spun out their geospatial / VPS team with
  one of the world's largest AR map datasets; hiring perception
  engineers as of 2025.
- **Veo Robotics, Roboflow, Voxel51, Encord, Scale AI** — perception
  infrastructure. Roboflow is the most web-dev-friendly on this list
  (TypeScript frontend, Python backend, fully remote). Your existing
  web skills are a feature, not a bug.
- **Standard Bots, Dexterity, Covariant (mostly absorbed into
  Amazon)** — warehouse / industrial manipulation. Smaller teams,
  more shipping pressure.
- **Path Robotics, Bright Machines, Machina Labs** — industrial
  perception for welding, electronics assembly, sheet-metal forming.
  Less hyped, real customers, comp solid.

## How they hire

Three buckets. **Realistic target for a junior web dev with ~6
months of ramp: bucket 2.**

- **Research scientist / research perception** — PhD or 2+ first-
  author top-venue papers. Hardest to break in cold.
- **Perception software engineer** — strong eng + working ML chops.
  Integrate models, write inference services, optimize C++ hot paths,
  own the camera pipeline. The bread-and-butter role.
- **Sensor / calibration engineer** — overlaps with EE; hands-on
  calibration, time-sync, multi-sensor fusion. C++ heavy. Underrated
  switcher path: less competition, real shortage, durable moat once
  you've calibrated a multi-camera-lidar rig in anger.

## How to actually apply to each tier

- **Big tech (Waymo, NVIDIA, Apple, Meta Reality Labs, Zoox)** —
  referral path only; cold ATS submissions are discarded. Find five
  L3/L4 perception ICs on LinkedIn and send a three-sentence intro
  citing a specific project of theirs; conversion runs 5-15%.
- **Defense (Anduril, Shield AI, Saronic, Helsing, Skydio)** — apply
  directly Tuesday/Wednesday morning Pacific; mention willingness to
  relocate up front. Recruiters move fast (screen within a week).
- **Hot frontier startups (Figure, 1X, Skild, Pi, Wayve)** —
  recruiters source from X and LinkedIn; post a 30-second working
  demo loop (SLAM trajectory, arXiv mini-paper, hosted detection
  model). They will find you.
- **Smaller perception startups (Pickle, Chef, Rivr, Bedrock, Cobot,
  Field AI)** — email the CTO directly with a two-line pitch and a
  60-second demo; 20-40% reply rate if the demo is good.
- **Perception SaaS / infra (Roboflow, Voxel51, Polycam, Luma)** —
  apply directly and lead with TypeScript / React / Next.js. They
  need engineers who ship a polished developer product.
- **Research labs (FAIR, TRI, NVIDIA Research, DeepMind Robotics)** —
  cold rarely works; coauthor a workshop paper with an insider or
  enter via a research-engineer (non-PhD) role and convert. Not a
  six-month plan.

## Interview prep — what perception interviews actually ask

Listed roughly by frequency in a perception-engineer screen.

- **"Explain a Kalman filter in your own words."** Read Probabilistic
  Robotics ch. 1-3 and implement a 1D constant-velocity filter in
  numpy; know when EKF vs UKF.
- **"Implement RANSAC for line fitting."** Classical-CV FizzBuzz.
  Implement for line, plane, homography on real images; discuss
  inlier threshold and iteration count.
- **"Derive the pinhole projection equation."** Work Hartley &
  Zisserman ch. 6; go from world point through extrinsics,
  intrinsics, distortion to pixel on a whiteboard.
- **"Fuse a noisy IMU with camera poses."** Read VINS-Mono and run
  it on EuRoC; discuss bias estimation, gravity alignment, time-sync.
- **"Debug a drifting SLAM trajectory."** Break ORB-SLAM3 in known
  ways (bad calibration, missing loop closure, sensor desync) and
  learn each failure signature.
- **"Describe a recent vision paper."** Pick two or three (DINOv2,
  SAM 2, FoundationPose, Co-Tracker, recent CVPR) and explain the
  problem, contribution, one limitation. Don't fake reading.
- **"Implement non-maximum suppression."** Cold in 15 minutes with
  IoU helper; know Soft-NMS and DIoU-NMS.

## Red flags when evaluating a perception job

- **No engineer-on-site at the customer.** Ask "when a customer
  reports a perception bug, what's the loop?"
- **No time-sync infrastructure.** Ask how sensors are time-synced;
  if the answer is "system clocks, mostly fine," run. PTP / hardware
  triggers / a sync board is the right answer.
- **One person can debug the camera pipeline.** Ask who could debug
  a calibration drift in production if the perception lead vanished.
- **Data collection requires a tribal-knowledge spreadsheet.**
  Healthy orgs use Roboflow, Voxel51, Encord, Scale, or in-house.
- **No evaluation harness.** Ask for the eval set, run frequency,
  and metrics that gate a release.
- **Equity mentioned but cap table hidden.** At small companies,
  ask for fully-diluted percentage, preference stack, last 409A.
- **Title and actual work don't match.** Ask what the last person
  in this role shipped in the past six months.

## Where perception engineers earn the most

Approximate TC bands for senior IC (3-7 years), 2025 Bay Area / NYC.
Sources: levels.fyi, 2025 Robotics Salary Guide, Glassdoor self-
reports, public funding announcements, Blind / HN compensation
threads. Startup TC is noisy because it includes illiquid common
shares valued at the last preferred-round price.

- NVIDIA, Waymo: $300-450k (Waymo median $232k across levels)
- Apple, Meta Reality Labs, Tesla: $300-500k+
- Anduril, Shield AI: $300-500k (heavy equity)
- Physical Intelligence, Wayve, Skild, Figure, 1X: $350-600k+
  (equity is the lottery ticket)
- Boston Dynamics, TRI, Mobileye: $230-380k
- Smaller startups (Pickle, Chef, Bedrock, Rivr): $200-350k
- Perception SaaS (Roboflow, Voxel51, Polycam, Luma): $200-330k
  with full-remote optionality

Numbers assume Bay Area / NYC / Seattle. Remote / EU usually 20-40%
lower; London Wayve / Helsing close the gap.

**Equity vs cash.** Discount frontier-startup equity 70-90% when
comparing offers; Series-B/C equity 40-60%; public-company RSUs at
face value. Cash is cash. With tight personal runway, bias toward
base at a large company; with 12+ months of runway and high risk
tolerance, frontier startups have meaningfully better expected value
over five years.

## Remote / hybrid posture by employer type

- **AV labs (Waymo, Cruise, Zoox)** — hybrid 3-5 days on-site; some
  offline / data / training roles flex.
- **Foundation-model perception (FAIR, NVIDIA Research, DeepMind
  Robotics)** — remote-friendly for research and ML infra; less so
  for product perception.
- **Humanoid startups (Figure, 1X, Apptronik, Cobot)** — strictly
  on-site; plan to relocate.
- **Defense (Anduril, Shield AI, Saronic, Helsing)** — mostly on-
  site (classified work + hardware); some non-classified hybrid.
- **AR / glasses (Apple Vision Products, Meta Reality Labs)** —
  on-site for hardware-integrated, hybrid for app-layer.
- **Perception SaaS (Polycam, Luma, Roboflow, Voxel51, Veo, Encord)**
  — fully remote, often globally distributed.
- **Industrial / vertical (Pickle, Chef, Bedrock, Path, Symbotic)**
  — on-site in non-major-tech cities; comp adjusts.

## Title decoder ring

Same job carries five names; search job boards under all of these.

- **Perception Engineer** — umbrella title (Waymo, Zoox, Cruise,
  Skydio, Pickle, Cobot). Own one pipeline slice; ship on-robot.
- **Computer Vision Engineer** — more ML / image-focused (Apple,
  Meta RL, Snap, Polycam, Luma, Roboflow, Voxel51). Train and deploy
  CV models, often with a product surface.
- **Robotics Software Engineer (Perception)** — generalist with ROS
  / C++ comfort (Figure, 1X, Apptronik, Boston Dynamics, Saronic).
  More systems integration than pure ML.
- **ML Engineer, Perception** — training, infra, scaling (Wayve,
  Tesla, Pi, Skild, Meta FAIR). PyTorch / JAX, distributed training.
- **Sensor Fusion Engineer** — multi-modal (Mobileye, Shield AI, some
  Anduril Lattice, Bosch, ZF). Kalman / factor graphs, C++ heavy.
- **SLAM Engineer** — narrow specialty (Skydio, Niantic, Magic Leap,
  Apple ARKit, some AV). Pose, loop closure, VIO.
- **3D Vision Engineer** — geometric reconstruction, NeRF, Gaussian
  splatting (Polycam, Luma, Spline, Scaniverse, Niantic). Graphics-
  adjacent.
- **Spatial Computing Engineer** — Apple / Meta marketing variant of
  3D vision, mostly AR.
- **Autonomy Engineer (Perception)** — defense / drone generalist
  with a perception slant (Anduril, Shield AI, Saronic).

## Hiring market signal

From the 2025 Robotics Salary Guide (907 jobs analyzed Nov-Dec 2025):

- Robotics Software Engineer median: **$189k**.
- ML in perception roles commands a similar +30% premium to RL /
  diffusion in VLA roles.
- "Computer Vision Engineer" is a named trending title in 2025.
- Global CV market: **$19.82B in 2024**, **~19.8% CAGR through 2030**
  (Grand View Research, MarketsandMarkets).

Translation: most broadly-applicable robotics specialty. Less
explosive than VLA, but with a wider customer base and dozens of
viable employers in every major US/EU city.

Next: `05-projects.md` for portfolio projects mapped to the interview
patterns (from-scratch RANSAC, VINS-Mono run, small detection
pipeline on a Roboflow dataset); `03-start.md` for the 30/60/90 plan
that gets you to credibly applying to tier-2 startups on this list.
