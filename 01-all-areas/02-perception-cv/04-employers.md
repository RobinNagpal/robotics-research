# The Perception & Computer Vision Market

> Market intel for our team. The companies below are the landscape we
> operate in as a perception services shop. Some are potential
> customers, some are partners we can integrate with, some are
> competitors, some are talent sources for our hires, and some are
> reference points for stack and case studies. Comp bands are
> included so we set our own salaries fairly against the market.

## What this file is for

When we pitch a new client, we sometimes need to position against
the big names ("we do what Plainsight does, smaller and more
bespoke"). When we hire, we benchmark against NVIDIA / Waymo /
Skydio comp so our offers don't read as low. When we read CVPR
papers, half are from teams listed here. This is our shared map of
the landscape.

See also: `01-examples.md` (deployed products and papers),
`05-projects.md` (what we sell), `06-courses.md` (where our team
learns from), `00-basics.md` (three concrete agency project
patterns).

## How to read each entry

For each company below: what they do, the tech stack they're known
to use, the TC band our team competes with, the location, and
**what they mean to us** — one of:

- *Potential customer* — their internal teams sometimes hire
  agencies for overflow or specialized work.
- *Partner candidate* — they run a formal partner / reseller /
  inception / agency program we could join.
- *Competitor* — they sell into the same RFPs we do.
- *Talent source / talent risk* — we hire from them; our team might
  leave to them.
- *Reference point* — published work, stack, or case studies we
  study but don't directly compete with.

---

## Big tech and established AV / AR labs

Bigger teams, more process, slower cadence. Mostly *reference
points* for stack and case studies, and *talent risks* for senior
ICs.

- **Waymo (Alphabet)** — AV perception (camera + lidar + radar
  fusion, segmentation, tracking, auto-labeling). Stack: C++ +
  PyTorch on TPUs; Bazel for build. Low-hundreds engineers across
  perception. Median TC ~$232k; senior IC $300-450k. SF / Mountain
  View / Pittsburgh / Phoenix.
  *To us:* reference point for multi-sensor fusion architecture and
  for the Waymo Open Dataset; talent risk for senior perception ICs.

- **NVIDIA** — Isaac, GR00T, Cosmos, FoundationPose, FoundationStereo,
  Replicator. Multiple 20-80-engineer teams (Isaac SDK, Isaac Sim,
  GR00T, DRIVE, Research). Stack: C++ + PyTorch + CUDA + TensorRT.
  Median TC ~$270k; senior staff $400k+.
  *To us:* **partner candidate** via NVIDIA Inception (free DGX
  cloud credits, sales co-marketing, NVIDIA Connect introductions);
  reference point for Isaac stack; sometimes a customer for
  outsourced Isaac-Sim integration and Replicator data pipelines.

- **Tesla Autopilot / Optimus** — camera-only AV + humanoid.
  Secretive. PyTorch + custom C++; Dojo training. Base lower than
  Waymo, equity-heavy.
  *To us:* reference point for vision-only architecture and BEV
  occupancy nets; not a partner, not a customer.

- **Mobileye** — vision-centric ADAS. Jerusalem + Detroit + San
  Jose. C++ on custom EyeQ silicon, PyTorch for training. Senior IC
  $230-380k in US, less in Israel.
  *To us:* reference point for ADAS perception at scale.

- **Apple (Vision Products Group, ARKit, camera ISP)** — Vision Pro
  perception, ARKit. Stack: Metal + CoreML + custom C++. Senior IC
  $300-500k.
  *To us:* reference point for on-device 3D perception. Their ARKit
  scan + room mesh output is sometimes an input format for our AEC
  digital-twin work.

- **Meta Reality Labs** — Aria glasses, SAM, DINOv2. Two sub-orgs:
  FAIR (research, mostly PhDs) and RL Product (ships glasses /
  Quest, eng-heavy). PyTorch.
  *To us:* **major reference point** — SAM 2, DINOv2, and
  Depth-Anything (community) come out of this ecosystem. We use
  their open-source models daily.

- **Boston Dynamics (Hyundai)** — Spot, Atlas. Boston. Tens of
  engineers, tightly coupled to controls. C++ first, internal
  state-estimation frameworks. Senior IC $230-380k.
  *To us:* reference point for state estimation and legged-robot
  perception; brand carries credibility on our team's resumes.

- **Zoox (Amazon)** — full AV stack, Foster City CA. C++ + PyTorch;
  Amazon L5/L6 bands.
  *To us:* reference point.

- **Cruise (GM)** — re-staffing through 2025 after the 2023 setback.
  Comp competitive, morale historically bruised.
  *To us:* reference point; watch hiring signal late 2025 / 2026 for
  market direction.

- **Toyota Research Institute (TRI)** — Cambridge MA + Los Altos.
  Open publication culture, PyTorch + JAX. $230-330k.
  *To us:* reference point; some published code is genuinely useful
  (LfD, manipulation policies).

- **Symbotic, Amazon Robotics** — warehouse perception at huge
  deployment volume. Java + C++, ROS-adjacent internal frameworks.
  *To us:* **potential customer** for niche warehouse perception
  consulting; reference point for at-scale industrial deployments.

- **Skydio** — straddles this tier and defense; see below.

---

## Defense / dual-use companies (growing fast since 2022)

Exploded post-2022 with US/EU defense budgets. Comp often beats
commercial robotics. US citizenship required for most US roles; a
subset needs SECRET clearance.

- **Anduril** — Lattice, Ghost, Roadrunner, maritime. Low-hundreds
  across perception. C++ + Rust + PyTorch with in-house data
  platform. Senior IC $350-500k+.
  *To us:* talent risk; not a realistic customer for an outside
  agency (most work is classified or done in-house). Reference
  point for systems-engineering culture.

- **Shield AI** — Hivemind, V-BAT drone autonomy. Tens of perception
  engineers. C++ + PyTorch + custom middleware. Median ~$228k, senior
  IC $300-450k. San Diego.
  *To us:* talent risk; reference point for VIO/SLAM at the edge.

- **Saronic** — autonomous surface vessels. Series-B+ 2024 at $1B+.
  Small team, Austin TX.
  *To us:* reference point for maritime perception, which is a
  potential niche vertical for us.

- **Helsing** (Germany) — defense AI, Munich + London + Paris. EUR
  150-250k + equity.
  *To us:* talent risk on the EU side; reference point.

- **Skydio** — drones for consumer / defense / public safety.
  Redwood City CA. C++ + PyTorch; one of the most polished on-device
  perception stacks. Senior IC $250-400k.
  *To us:* **partner candidate** for drone-based inspection work
  (Skydio's developer SDK is a real platform we can build on);
  reference point for VIO at the edge.

- **Saildrone, Vannevar Labs, HavocAI, Mach Industries** — younger
  dual-use names. Small teams, fast hiring.
  *To us:* mostly reference points; check if any are large enough to
  outsource niche perception (rare).

---

## Perception-heavy startups founded or scaled 2020-2025

Where the explosive growth and comp variance live. Most did not
exist 4 years ago.

- **Wayve** (UK, 2017, Series-C 2024 at $1B+) — end-to-end driving
  foundation models. 100+ across perception/learning. London +
  Mountain View. PyTorch + JAX.
  *To us:* reference point for end-to-end driving; talent risk in
  London.

- **Physical Intelligence (Pi)** (2024) — VLA models with heavy
  perception. $400M Nov 2024 at $2.4B. Under 100 total, high talent
  density. PyTorch + JAX.
  *To us:* reference point for VLA + perception integration.

- **Skild AI** (2023, ex-CMU) — robot-agnostic generalist policy.
  $300M Series A July 2024 at ~$1.5B. PyTorch. Pittsburgh + Bay
  Area.
  *To us:* reference point.

- **Figure AI** (2022) — humanoid + Helix VLA. Cumulative >$1.5B
  raised; Feb 2025 talks at $39.5B. Perception 30-50+ by mid-2025.
  PyTorch + C++ + NVIDIA Isaac. Sunnyvale.
  *To us:* talent risk for our humanoid-curious senior ICs;
  reference point for Isaac-Sim-based pipelines.

- **1X Technologies** (rebranded from Halodi 2022) — NEO consumer
  humanoid + world-model perception. Norway + SF. PyTorch + C++.
  *To us:* reference point.

- **Apptronik** (Apollo humanoid, Mercedes pilots 2023+) — Austin
  TX. More eng-than-research, more shipping-focused.
  *To us:* potential customer for industrial integration work if
  they expand into manufacturing partnerships beyond Mercedes.

- **Cobot** (2022, ex-Amazon Robotics VP Brad Porter) — collaborative
  mobile manipulator. Boston, low-tens. Strong manipulation-
  perception interface.
  *To us:* reference point.

- **Bedrock Robotics** (2023) — autonomous earth-moving. SF.
  *To us:* reference point for off-road / construction perception.

- **Pickle Robot** (2018, scaled 2023+) — truck-unloading. Cambridge
  MA.
  *To us:* reference point — their public material is one of the
  better small-team case studies (see `00-basics.md` use case 1
  references).

- **Field AI** (2023) — outdoor / off-road foundation policies for
  inspection, construction. Mission Viejo / Pasadena.
  *To us:* reference point for off-road perception, which lacks
  lane lines / HD maps and is a distinct skillset.

- **Chef Robotics** (2019, scaled 2023+) — food assembly. SF.
  Deformable, occluded, glossy, wet food is close to medical imaging
  in difficulty.
  *To us:* reference point for hard segmentation problems.

- **Rivr** (2023, Switzerland, ex-ETH) — last-mile delivery robots.
  Lower comp than US.
  *To us:* reference point; potential EU partner if we expand there.

- **Polycam, Luma AI, Spline, Scaniverse (Niantic)** — consumer 3D-
  from-photos. Pure software, remote-friendly, DX-obsessed. PyTorch
  + iOS / web frontend.
  *To us:* **partner candidates / capture-layer platforms** —
  Polycam Pro and Scaniverse are common capture layers for our AEC
  and real-estate digital-twin clients (see `00-basics.md` use case
  2 references). Sometimes a competitor when we pitch end-to-end
  workflows.

- **Niantic** — recently spun out their geospatial / VPS team.
  *To us:* reference point for outdoor VPS / persistent AR.

- **Veo Robotics, Roboflow, Voxel51, Encord, Scale AI** — perception
  infrastructure. Roboflow has TypeScript frontend, Python backend,
  fully remote.
  *To us:* **partner candidates** — Roboflow's partner program lets
  agencies build on top of their labeling + training stack and refer
  customers in. Voxel51 (fiftyone) and Encord are dataset / eval
  tools we use directly.

- **Standard Bots, Dexterity, Covariant (mostly absorbed into
  Amazon)** — warehouse / industrial manipulation. Smaller teams,
  more shipping pressure.
  *To us:* potential customers for occasional perception consulting;
  reference points.

- **Path Robotics, Bright Machines, Machina Labs** — industrial
  perception for welding, electronics assembly, sheet-metal forming.
  Real customers, comp solid.
  *To us:* reference points; potential customers for niche
  consulting.

---

## Competing CV / perception services shops

The agencies and consultancies we'll run into in sales processes.
Most are larger than us; we win against them on responsiveness,
verticalization, and per-customer fine-tuning depth.

- **Landing AI** (Andrew Ng) — ~100 people. Visual inspection
  platform + custom delivery. Verticals: manufacturing, life
  sciences. Published case studies with Foxconn, Bombardier,
  AstraZeneca.
  *Where we beat them:* fixed-cost engagements under $200k; bespoke
  vertical pipelines they wouldn't take on.

- **Plainsight** (formerly Sixgill) — ~50-100 people. CV platform +
  services. Verticals: food processing, energy, agriculture.
  Published with Tyson Foods.
  *Where we beat them:* same as Landing AI — smaller deals, faster
  turnaround, lighter platform lock-in.

- **Cogniac** — ~30-50 people. Industrial CV platform. Verticals:
  steel, rail, manufacturing. Published with U.S. Steel.
  *Where we beat them:* customers wary of platform lock-in.

- **MobiDev** (Ukrainian) — ~400 people across all dev work; CV is
  one vertical. Published vineyard yield case study is widely cited.
  *Where we beat them:* deeper perception specialization vs. their
  generalist outsourcing positioning.

- **InData Labs** (Belarus / EU), **MindTitan** (Estonia), **N-iX**
  (Ukraine / Poland), **Apriorit**, **Sciencesoft**, **Lampa
  Software**, **Innowise**, **Konverge.ai**, **Maruti Techlabs** —
  larger ML consultancies with published CV case studies. Compete
  on price for staff-augmentation work.
  *Where we beat them:* productized verticals, fixed-cost outcomes,
  IP we own rather than billed hourly.

- **Visual Layer**, **Voxel51 services**, **Datature**, **Encord
  Pro Services** — dataset-tool companies that also do paid
  engagements.
  *Where we beat them:* perception delivery beyond dataset curation
  (deployment, edge inference, customer integration).

- **Roboflow Partner Network** (when joined) — fellow Roboflow
  agency partners are *coopetitive*: same partner directory, but
  Roboflow itself routes leads based on vertical fit.
  *Where we beat them:* by being explicit about a vertical (e.g.,
  "we do solar-panel inspection," not "general CV").

- **Smaller regional shops** — too many to name individually
  (Decode UK, Ardas Ukraine, etc.). Most aren't directly
  competitive because their lead pipelines are local.

---

## Partnership and reseller programs worth joining

Concrete programs where applying as an agency unlocks credits,
sales co-marketing, or a customer pipeline.

- **NVIDIA Inception** — free DGX cloud credits, NVIDIA Connect
  intros to enterprise customers, GTC speaking opportunities. Open
  to AI / robotics shops under ~$50M revenue. Apply at
  nvidia.com/en-us/startups.
- **Roboflow Partner Program** — listed in their agency directory,
  shared revenue on referred customers, free Pro accounts for
  agency staff. Apply at roboflow.com/partners.
- **Hugging Face Enterprise Hub / Expert Acceleration Program** —
  partner-tier discounts for our customers; co-marketing on
  customer stories.
- **Matterport Capture Services / Partner Network** — listed as a
  capture-services partner for AEC and real-estate clients;
  referral pipeline for digital-twin work. Especially relevant for
  use case 2 in `00-basics.md`.
- **NavVis Partner Network** — similar to Matterport but for
  industrial AEC (large-site mapping).
- **Pix4D Partner Program** — co-marketing and referral for
  drone-based mapping work; relevant to use case 3.
- **DroneDeploy Partner Network** — same pattern for ag and
  construction drone deployments.
- **OpenSpace, Reconstruct, HoloBuilder partner programs** — for
  construction progress documentation.
- **AWS Activate / Google Cloud for Startups / Microsoft for
  Startups** — $25k-$200k of cloud credits available; useful for
  GPU-heavy photogrammetry and splat training during initial
  customer engagements.
- **DJI Enterprise Software Partner** — for drone-data workflows;
  niche but real.
- **Polycam Pro Custom Integrations** — limited program for
  agencies building on Polycam's capture SDK.

Most of these are free to apply to. The realistic high-value ones
for a CV services shop are: NVIDIA Inception, Roboflow Partner,
Matterport / NavVis, and Pix4D / DroneDeploy.

---

## Comp bands (for setting our own salaries)

Approximate TC bands for senior IC (3-7 years), 2025 Bay Area / NYC.
Sources: levels.fyi, 2025 Robotics Salary Guide, Glassdoor self-
reports, public funding announcements. Startup TC is noisy because
it includes illiquid common shares.

- **NVIDIA, Waymo:** $300-450k (Waymo median $232k across levels)
- **Apple, Meta Reality Labs, Tesla:** $300-500k+
- **Anduril, Shield AI:** $300-500k (heavy equity)
- **Physical Intelligence, Wayve, Skild, Figure, 1X:** $350-600k+
  (equity is the lottery ticket)
- **Boston Dynamics, TRI, Mobileye:** $230-380k
- **Smaller startups (Pickle, Chef, Bedrock, Rivr):** $200-350k
- **Perception SaaS (Roboflow, Voxel51, Polycam, Luma):** $200-330k
  with full-remote optionality
- **CV consultancies (Landing AI, Plainsight, Cogniac):** $180-280k
  + variable bonus; closer to our market

Remote / EU usually 20-40% lower; London / Munich close the gap on
the high end.

**For our hires:** band our base salaries at the perception-SaaS
range or above. Below that and our offers read as low against the
market our team is comparing against. Equity-heavy frontier startups
are not direct comp competitors for our headcount; their candidates
are taking lottery-ticket risk we can't match.

---

## Hiring market signal

From the 2025 Robotics Salary Guide (907 jobs analyzed Nov-Dec 2025):

- Robotics Software Engineer median: **$189k**.
- ML / perception roles command a similar +30% premium to RL /
  diffusion in VLA roles.
- "Computer Vision Engineer" is a named trending title in 2025
  hiring reports.
- Global CV market: **$19.82B in 2024**, **~19.8% CAGR through 2030**
  (Grand View Research, MarketsandMarkets).

Translation: the broadest-applicable robotics specialty. Less
explosive than VLA, much wider customer base. Good market for our
shop's positioning.

---

## Remote / hybrid posture by employer type

Useful for understanding which talent pools are accessible to us
(remote-friendly = larger candidate pool for our remote hires).

- **AV labs (Waymo, Cruise, Zoox):** hybrid 3-5 days on-site; some
  offline / data / training roles flex.
- **Foundation-model perception (FAIR, NVIDIA Research, DeepMind
  Robotics):** remote-friendly for research and ML infra; less for
  product perception.
- **Humanoid startups (Figure, 1X, Apptronik, Cobot):** strictly
  on-site.
- **Defense (Anduril, Shield AI, Saronic, Helsing):** mostly on-
  site; some non-classified hybrid.
- **AR / glasses (Apple, Meta Reality Labs):** on-site for hardware
  work, hybrid for app-layer.
- **Perception SaaS (Polycam, Luma, Roboflow, Voxel51, Veo,
  Encord):** fully remote, globally distributed. Our biggest direct
  competitors for distributed-team talent.
- **Industrial / vertical (Pickle, Chef, Bedrock, Path, Symbotic):**
  on-site in non-major-tech cities.

---

## Title decoder

The same role carries five different names across companies. Use
this when reading job ads (competitor signaling) or when writing
our own postings.

- **Perception Engineer** — umbrella title (Waymo, Zoox, Cruise,
  Skydio, Pickle, Cobot). Owns one pipeline slice end-to-end on-
  robot.
- **Computer Vision Engineer** — more ML / image-focused (Apple,
  Meta RL, Snap, Polycam, Luma, Roboflow, Voxel51). Trains and
  deploys CV models with a product surface.
- **Robotics Software Engineer (Perception)** — generalist with
  ROS / C++ comfort (Figure, 1X, Apptronik, Boston Dynamics,
  Saronic). More systems integration than pure ML.
- **ML Engineer, Perception** — training, infra, scaling (Wayve,
  Tesla, Pi, Skild, FAIR). PyTorch / JAX, distributed training.
- **Sensor Fusion Engineer** — multi-modal (Mobileye, Shield AI,
  some Anduril Lattice, Bosch, ZF). Kalman / factor graphs, C++
  heavy.
- **SLAM Engineer** — narrow specialty (Skydio, Niantic, Magic
  Leap, Apple ARKit, some AV). Pose, loop closure, VIO.
- **3D Vision Engineer** — geometric reconstruction, NeRF, Gaussian
  splatting (Polycam, Luma, Spline, Scaniverse, Niantic). Graphics-
  adjacent.
- **Spatial Computing Engineer** — Apple / Meta marketing variant
  of 3D vision, mostly AR.
- **Autonomy Engineer (Perception)** — defense / drone generalist
  with a perception slant (Anduril, Shield AI, Saronic).

---

## What this means for our positioning

Three short takeaways for the team:

1. **The hyperscalers are reference points, not competitors.** They
   serve different price points (internal headcount, custom silicon)
   than we sell. Mention them only when a customer asks "who else
   does this?"
2. **The CV consultancies are our direct competitors.** Landing AI,
   Plainsight, Cogniac, MobiDev. Win on responsiveness, vertical
   depth, and outcome-based pricing.
3. **The platforms (NVIDIA, Roboflow, Matterport, Pix4D,
   DroneDeploy, Polycam) are where the leverage is.** Joining their
   partner programs early matters more than a marketing budget.
