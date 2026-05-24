# The Robotics Infrastructure and Middleware Market

> Market intel for our team. The companies below are the landscape
> we operate in when we take on robotics infrastructure and
> middleware work. Some are potential customers, some are partners
> we can integrate with, some are competitors, some are talent
> sources for our hires, and some are reference points for stack
> and architecture. Comp bands are included so we set our own
> salaries fairly against the market.
>
> Infra and middleware is the highest-leverage corner of the
> robotics services market and one of the most underserved. Every
> robotics team that ships a product eventually needs the same
> things: a working CI loop with hardware-in-the-loop, log capture
> and visualization, deployment to fleets, observability, OTA, and
> some form of MLOps for the perception and policy models on board.
> Almost none of them have all of it well-built. That gap is our
> opportunity.

## What this file is for

When we pitch a new client, we sometimes need to position against
the platform vendors ("we wire up Foxglove and Formant for you,
faster and cheaper than building it yourselves"). When we hire, we
benchmark against NVIDIA Isaac, Apex.AI, and Foxglove comp so our
offers don't read as low. When we read ROSCon talks or Open
Robotics discourse threads, most are from teams listed here. This
is our shared map of the landscape.

See also: `01-examples.md` (deployed infra and OSS projects),
`05-projects.md` (what we sell), `06-courses.md` (where our team
learns from), `00-basics.md` (concrete agency project patterns).

## How to read each entry

For each company below: what they do, the tech stack they're known
to use, the TC band our team competes with, the location, and
**what they mean to us** — one of:

- *Potential customer* — their internal teams sometimes hire
  agencies for overflow or specialized infra work.
- *Partner candidate* — they run a formal partner / reseller /
  inception / solutions program we could join.
- *Competitor* — they sell into the same RFPs we do.
- *Talent source / talent risk* — we hire from them; our team
  might leave to them.
- *Reference point* — published stack, architecture, or RFC work
  we study but don't directly compete with.

---

## Foundational middleware vendors

The teams that own the layers everything else sits on. Slow to
move, deeply technical, and high-trust relationships with the rest
of the ecosystem.

- **Open Robotics (now under OSRA — Open Source Robotics
  Alliance)** — stewards ROS 2, Gazebo, and the OSRF
  infrastructure. The Alliance was formed late 2024 as a
  vendor-neutral governance home, with Intrinsic (Alphabet),
  Apex.AI, ZettaScale, eProsima, NVIDIA, Bosch and others as
  founding members. Stack: C++ + Python, Bazel / colcon, lots of
  CMake. Small core team (low tens of engineers across OR /
  Intrinsic robotics infra). Comp ~$180-280k, academic-adjacent
  for the OR side.
  *To us:* **partner candidate** via OSRA membership — the formal
  way to influence ROS 2 roadmap and get listed as a credentialed
  services provider. Reference point for ROS 2 architecture and
  REP process. Occasionally a talent source for very senior
  middleware engineers.

- **Apex.AI** — Apex.OS, a safety-certified (ISO 26262 ASIL-D)
  fork and hardening of ROS 2 for automotive and other regulated
  domains. Also a major contributor upstream. Stack: C++ on
  certified RTOS targets; deep DDS expertise. Palo Alto + Berlin
  + Stuttgart. Senior IC $230-380k.
  *To us:* **partner candidate** via their services partner
  ecosystem (hedge — confirm current program structure). Talent
  risk for senior middleware ICs. Reference point for what
  production-grade ROS 2 looks like.

- **ZettaScale** — maintainers of Eclipse Zenoh, a federated
  pub/sub/query protocol that's been replacing DDS in many ROS 2
  deployments since the rmw_zenoh implementation matured. Strong
  on WAN, multi-robot, and intermittent-connectivity scenarios.
  France + Italy + UK. EU comp, roughly EUR 90-160k for senior
  ICs.
  *To us:* **partner candidate** — early Zenoh expertise is a
  differentiator in any fleet or multi-robot RFP. Reference point
  for next-gen middleware. Occasional partner on integration
  work.

- **eProsima** — Fast DDS, the default ROS 2 RMW implementation.
  Madrid. Smaller team, deeply specialized. Senior IC EUR
  70-120k.
  *To us:* **partner candidate** via their commercial support
  partner network (hedge — verify formal program). Reference
  point for DDS internals. We use Fast DDS daily on any ROS 2
  engagement and a support contract is a normal upsell for our
  enterprise customers.

- **RTI (Real-Time Innovations)** — Connext DDS, the premium
  safety-certified DDS implementation used heavily in defense,
  aerospace, and medical robotics. Sunnyvale CA. Senior IC
  $200-320k.
  *To us:* reference point and occasional integration partner.
  Most of our customers don't pay RTI's enterprise pricing, but
  defense-adjacent customers sometimes mandate Connext, in which
  case we integrate.

---

## NVIDIA's robotics infra stack

NVIDIA deserves its own section because it's effectively a parallel
universe of robotics infrastructure that customers either fully
adopt or deliberately avoid.

- **NVIDIA Isaac SDK / Isaac ROS** — accelerated ROS 2 packages
  (NITROS for zero-copy GPU pipelines, VSLAM, Nvblox, FoundationPose
  bridges). Stack: C++ + CUDA + TensorRT, tightly coupled to
  Jetson. Median TC ~$270k for senior IC; staff $400k+.
- **Isaac Sim** — Omniverse-based simulator with photoreal
  rendering and PhysX. The de facto sim for Isaac users.
- **Isaac Lab** — RL training framework on top of Isaac Sim,
  superseded most of the Isaac Gym workflow.
- **Isaac CloudXR** — remote teleoperation streaming pipeline.
  Niche but a real product.
- **Isaac Mission Dispatch** — cloud-native VDA 5050-compatible
  fleet dispatcher for AMRs.
- **Isaac Perceptor** — reference perception pipeline (depth,
  obstacle detection, 3D reconstruction) packaged as Isaac ROS
  graphs.

*To us collectively:* **partner candidate** via NVIDIA Inception
(free DGX cloud credits, Connect intros, GTC speaking slots, Isaac
ROS partner directory listing — verify Mission Dispatch is
included in current partner tier). Reference point for the
GPU-accelerated robotics stack. Frequent customer ask: "integrate
Isaac ROS into our existing ROS 2 graph without breaking realtime."
That integration work is bread-and-butter infra consulting.

---

## Observability and debugging

The fastest-growing slice of the infra market. Every robotics team
captures logs; almost none have visualization and observability
that meets their actual debugging needs.

- **Foxglove** (2021) — the dominant ROS bag viewer and
  observability platform. Foxglove Studio (now also forked, see
  Lichtblick) plus Foxglove Data Platform. Raised a Series A
  around $15M in 2022 (hedge — confirm current totals). Stack:
  TypeScript frontend, Rust/Go backend, MCAP underneath. Fully
  remote. Senior IC $230-350k.
  *To us:* **partner candidate** — Foxglove Partner Network
  exists in some form (hedge — confirm current name and
  enrollment). Wiring Foxglove into a customer's stack and
  building custom panels is one of our most repeatable
  engagements. Talent risk for senior infra ICs who want
  remote.

- **Lichtblick** — Bosch's open-source fork of Foxglove Studio
  after the original Studio went source-available. Practical
  fallback for customers who need a fully open viewer.
  *To us:* reference point and integration option; sometimes the
  right answer for customers averse to Foxglove's commercial
  terms.

- **PlotJuggler** — open-source time-series signal plotting,
  ubiquitous in ROS workflows. Maintained largely by one engineer
  with broad contributor base.
  *To us:* reference point and tool we install on day one of any
  engagement.

- **rerun.io** (2022) — newer 3D-native multimodal logging and
  visualization. Strong traction 2023-2025 in robotics + ML
  research. Stack: Rust core, Python / C++ / Rust SDKs. Stockholm
  + remote. Comp similar to Foxglove range, lower base, more
  equity (hedge).
  *To us:* **partner candidate**; reference point for modern
  log-and-replay UX. We integrate rerun into customer pipelines
  whenever the data is heavy on 3D / tensor / video where
  Foxglove is less ergonomic.

- **Rocon / Rocon Robotics** — older multi-robot orchestration
  middleware (Yujin Robot origins). Niche today but still
  referenced.
  *To us:* reference point.

- **MCAP** — Foxglove's open logging container format, now widely
  adopted as the successor to ROS bag. Not a company, but the de
  facto interchange format for robot logs.
  *To us:* every customer engagement eventually involves MCAP.
  Familiarity is table stakes.

---

## Simulation infra (overlap with sim-twins area)

Adjacent to our main infra work but listed here because customers
often ask us to wire simulation into CI. See the sim-twins area
file for the deeper sim landscape.

- **NVIDIA Omniverse** — the foundation under Isaac Sim. USD-based
  scene format, GPU rendering, OpenUSD ecosystem.
- **Open Robotics Gazebo Sim** (formerly Ignition) — the open
  default for ROS 2 sim. Less photoreal than Isaac Sim, more
  hackable, no Jetson dependency.
- **AWS RoboMaker** — AWS's managed simulation service. Note:
  AWS announced RoboMaker is being wound down (hedge — verify
  current EOL timeline); some customers still on it.
- **Microsoft Project Bonsai** — Microsoft's machine-teaching
  platform; sim integration for industrial control. Status post-
  2023 reorg is unclear (hedge).

*To us collectively:* reference points and integration surfaces.
Wiring Gazebo or Isaac Sim into a customer's GitHub Actions
pipeline so PRs run sim regressions is a productizable offering
for us.

---

## Cloud and fleet ops platforms

The layer above middleware. These are the platforms that take a
fleet of robots and give the operator a single dashboard, OTA, and
remote intervention. Direct partners or competitors depending on
how we position the engagement.

- **Formant** (2017, scaled post-2022) — fleet management SaaS,
  observability, teleop. Raised around $14M in 2024 (hedge —
  confirm round size and date). SF + remote. Senior IC
  $200-330k.
  *To us:* **partner candidate** via Formant Solutions Partner
  program (hedge — verify current name). Frequent integration
  customer ask.

- **InOrbit** (2018) — fleet management SaaS, RobOps community
  steward. Mountain View. Similar comp band to Formant.
  *To us:* **partner candidate**; runs the RobOps conference,
  which is a useful business-development venue.

- **Freedom Robotics** (2018) — fleet ops, lower-profile than
  Formant / InOrbit but still active. SF.
  *To us:* reference point; occasional partner.

- **Transitive Robotics** — newer entrant focused on browser-based
  agent and capability framework for robots.
  *To us:* reference point.

- **AWS IoT / IoT Greengrass / IoT Core** (and the rest of the
  RoboMaker ecosystem) — AWS's robotics-relevant managed
  services beyond RoboMaker proper.
  *To us:* **partner candidate** via AWS Partner Network; we
  build on these for fleet-cloud bridges.

- **Microsoft Azure IoT Edge / Azure IoT Hub** — Microsoft's
  equivalent stack.
  *To us:* **partner candidate** via Microsoft for Startups and
  Azure partner program.

- **Google Cloud IoT** — note Google Cloud officially deprecated
  the IoT Core service in 2023; customers now self-assemble with
  Pub/Sub + GKE. Still a real deployment target.
  *To us:* reference point; reasonable second-tier cloud option.

---

## MLOps adapted for robotics

General ML tooling that customers use for the learning side of
their robotics stacks. We bridge these into the ROS / middleware
side.

- **Weights & Biases** — broad ML experiment tracking, widely
  adopted in robotics research and product teams. Fully remote.
  Senior IC $230-380k.
  *To us:* **partner candidate** via their solutions partner
  program; reference point for experiment tracking patterns we
  bring into customer environments.

- **CometML** — competitor to W&B. Similar positioning, smaller
  footprint.
  *To us:* reference point.

- **ClearML** — open-core MLOps platform, on-prem-friendly. Often
  the right answer for customers who can't ship data to a
  vendor cloud.
  *To us:* **partner candidate**; reference point for self-hosted
  MLOps.

- **fiftyone (Voxel51)** — dataset observability and curation.
  Useful for both perception and policy data work in robotics.
  *To us:* **partner candidate** via Voxel51's services / partner
  program; tool we use directly.

- **DVC + Studio (Iterative.ai)** — data and model versioning
  layered on git. Common in robotics data pipelines.
  *To us:* **partner candidate** via Iterative's partner program
  (hedge — confirm formal program); reference point.

---

## AV-specific infra

A parallel infra ecosystem because AV scale and regulatory
requirements push different tradeoffs than general robotics.

- **Tier IV** (Japan) — primary maintainers of Autoware, the open
  AV stack. Run a large services arm around Autoware integration.
  *To us:* **partner candidate** (Autoware Foundation member) and
  reference point. Also a competitor for any AV-stack infra RFP.

- **AVS / Open Source Auto Stack** — broader umbrella of open
  automotive software efforts.
  *To us:* reference point.

- **Cariad (Volkswagen)** — VW's software org, large internal
  middleware and platform investment.
  *To us:* reference point and occasional talent source in
  Germany.

---

## Competing robotics-infra services shops

The agencies and consultancies we'll run into in sales processes
for infra and middleware work. Honest accounting: several of these
are deeper than us in specific niches and we'll lose to them on
those niches.

- **PickNik Robotics** — MoveIt maintainers; the dominant
  ROS 2 + MoveIt + manipulation services shop. Boulder CO + remote.
  Deep credibility in arm manipulation infra.
  *Where we beat them:* engagements outside manipulation
  (perception infra, fleet, observability) and customers who
  don't need MoveIt.

- **Open Robotics services arm (under Intrinsic / OSRA)** — the
  smallest but highest-credibility shop for "vanilla" ROS 2
  infrastructure work.
  *Where we beat them:* responsiveness on smaller engagements;
  we'll take work they decline.

- **Tangram Vision** (2020) — perception infrastructure and
  calibration services, sensor fusion middleware.
  *Where we beat them:* infra engagements outside their
  perception-calibration core (fleet, observability, CI).

- **Foxglove enterprise consulting** — Foxglove the company also
  takes paid integration engagements for enterprise customers.
  *Coopetitive*: same partner directory if we join Foxglove's
  network, but they typically route smaller deals out.
  *Where we beat them:* by being the agency they route deals to.

- **ZettaScale enterprise consulting** — same pattern for Zenoh
  deployments.
  *Where we beat them:* same — we become the implementation
  partner.

- **Apex.AI services** — services wrap around Apex.OS adoption.
  *Where we beat them:* engagements that don't require
  ISO 26262 certification (most non-automotive work).

- **Intermodalics** (Belgium) — long-running ROS / ROS 2 services
  consultancy. Strong on perception and navigation integration.
  *Where we beat them:* US-time-zone responsiveness; vertical
  productization.

- **Magazino's services arm** (Germany) — internal stack made
  externally available in places. Smaller external surface than
  Intermodalics. (Hedge — confirm current external services
  posture.)
  *Where we beat them:* most engagements outside their warehouse
  focus.

- **Robotec.ai** (Poland) — ROS 2 + Autoware + simulation
  services. Strong on AV-adjacent infra.
  *Where we beat them:* non-AV verticals; faster turnaround on
  small contracts.

- **Smaller regional ROS 2 consultancies** — too many to name
  individually. Most aren't directly competitive because their
  lead pipelines are local.

---

## Partnership and reseller programs worth joining

Concrete programs where applying as an agency unlocks credits,
sales co-marketing, or a customer pipeline.

- **OSRA membership (Open Source Robotics Alliance)** — the
  formal way to influence ROS 2 roadmap and be listed as a
  credentialed services provider. Membership tiers vary; smaller
  shops can apply at supporter / contributor levels. Hedge —
  confirm current dues and tiering.
- **ROS Industrial Consortium (Americas / Europe / Asia
  Pacific)** — industry-focused ROS adoption body; pipeline of
  industrial customers. Membership has annual dues; smaller-shop
  tiers exist.
- **NVIDIA Inception** — free DGX cloud credits, Connect intros,
  GTC speaking opportunities, Isaac ROS partner directory listing.
  Open to robotics / AI shops under ~$50M revenue. Apply at
  nvidia.com/en-us/startups.
- **Foxglove Partner Network** — partner program for agencies
  building Foxglove integrations and custom panels. Hedge —
  confirm current name and enrollment route.
- **Formant Solutions Partner** — partner tier for agencies
  implementing Formant for fleet customers. Hedge — confirm
  current program structure.
- **Apex.AI partner program** — services partner ecosystem
  around Apex.OS adoption. Hedge — confirm tiering.
- **eProsima support partner** — partner tier for offering Fast
  DDS commercial support. Hedge — confirm formal program.
- **ZettaScale partner** — Zenoh services partner program.
  Hedge — confirm.
- **AWS Activate / Google Cloud for Startups / Microsoft for
  Startups (Azure)** — $25k-$200k of cloud credits available;
  useful for sim regression CI and fleet-cloud demos during
  initial customer engagements.
- **Iterative.ai partner (DVC + Studio)** — partner tier for
  agencies implementing DVC pipelines. Hedge — confirm.

Most of these are free or low-cost to apply to. The realistic
high-value ones for an infra services shop are: OSRA, NVIDIA
Inception, Foxglove Partner Network, Formant Solutions Partner,
and ROS Industrial Consortium.

---

## Comp bands (for setting our own salaries)

Approximate TC bands for senior IC (3-7 years), 2025 Bay Area /
NYC. Sources: levels.fyi, 2025 Robotics Salary Guide, Glassdoor
self-reports, public funding announcements. Startup TC is noisy
because it includes illiquid common shares.

- **NVIDIA Isaac:** $270k median, senior staff $400k+
- **Apex.AI:** $230-380k
- **Open Robotics / Intrinsic robotics infra:** $180-280k
  (academic-adjacent on the OR side, full Alphabet bands on the
  Intrinsic side)
- **Fleet-ops SaaS startups (Formant, InOrbit, Freedom):**
  $200-330k, often remote
- **Foxglove:** $230-350k, fully remote
- **rerun.io, ZettaScale, eProsima:** EU bands, EUR 90-160k for
  senior ICs; US-equivalent roles cluster around $200-300k
- **AV labs infra (Waymo, Zoox, Cruise):** $300-450k — among the
  best-paid infra ICs in robotics
- **Defense infra (Anduril Lattice, Shield AI platform):**
  $300-500k with heavy equity

Remote / EU usually 20-40% lower; London / Munich close the gap on
the high end.

**For our hires:** band our base salaries at the fleet-ops-SaaS
range or above. Below that and our offers read as low against the
market our team is comparing against. AV-lab and defense bands are
not realistic comp competitors for our headcount unless we're
specifically poaching senior platform ICs.

---

## Hiring market signal

From the 2025 Robotics Salary Guide and recent ROSCon hiring
threads:

- "Robotics Infrastructure Engineer", "Robotics Platform
  Engineer", "ROS 2 Engineer", and "MLOps for Robotics" are
  growing but still-niche titles. Demand outstrips named-title
  supply because most teams hire under generic "Robotics Software
  Engineer".
- The "Embedded Systems + Real-Time + Linux + Cloud" combination
  is called out specifically as undersupplied in the 2025 Salary
  Guide.
- Foxglove's growth trajectory is the clearest signal that there's
  a real enterprise market for robotics observability — not just
  internal-tool budget.
- ROS 2 + DDS / Zenoh expertise commands a meaningful premium over
  generalist robotics software comp, because the supply of
  engineers who've shipped production middleware is tiny.

Translation: the underlying demand is large and the named-title
supply is small. Good market for our shop's positioning.

---

## Remote / hybrid posture by employer type

Useful for understanding which talent pools are accessible to us
(remote-friendly = larger candidate pool for our remote hires).
Infra and middleware is generally **more remote-friendly than
hardware-bound robotics work**, because middleware engineers don't
need physical access to a specific robot most of the time.

- **AV labs (Waymo, Cruise, Zoox) infra teams:** hybrid 3-5 days
  on-site; some flex for pure platform work.
- **NVIDIA Isaac:** mostly hybrid Santa Clara / Bay Area, some
  remote for senior ICs.
- **Apex.AI:** hybrid Palo Alto / Berlin / Stuttgart.
- **Open Robotics / Intrinsic:** historically remote-friendly on
  the OR side; Intrinsic more on-site.
- **Foxglove, rerun.io:** fully remote, globally distributed.
  Our biggest direct competitors for distributed-team talent.
- **Formant, InOrbit, Freedom Robotics:** remote-friendly.
- **ZettaScale, eProsima:** EU-based, generally remote-friendly
  within EU time zones.
- **Defense infra (Anduril, Shield AI):** mostly on-site; some
  non-classified platform work is hybrid.
- **Tier IV, Robotec.ai, Intermodalics:** regional on-site or
  hybrid; sometimes remote for senior ICs.

---

## Title decoder

The same role carries five different names across companies. Use
this when reading job ads (competitor signaling) or when writing
our own postings.

- **Robotics Infrastructure Engineer** — broad umbrella, often
  covers CI, build systems, log capture, observability wiring.
  Common at fleet-ops SaaS and at larger product companies.
- **Robotics Platform Engineer** — internal-platform-team flavor
  (Waymo, Zoox, Cruise, Anduril). Owns the shared stack the rest
  of engineering depends on.
- **ROS 2 Engineer** — explicit middleware framing (PickNik,
  Intermodalics, Open Robotics, Apex.AI). C++ heavy, comfortable
  in REP discussions.
- **Middleware Engineer** — narrower DDS / Zenoh / RMW focus
  (eProsima, ZettaScale, RTI, Apex.AI). Deep on transport layers
  and QoS.
- **DevOps for Robotics / Robotics DevOps Engineer** — CI,
  hardware-in-the-loop, deployment automation. Increasingly
  common title.
- **Robotics MLOps Engineer** — data pipelines, model deployment,
  experiment tracking adapted for embodied data. Newer title,
  expect to see it more 2025-2026.
- **Fleet Software Engineer** — focused on fleet-ops backend
  (Formant, InOrbit, Freedom, in-house at any larger AMR
  company).
- **Robotics CI Engineer** — narrower variant focused on the
  build / test / sim regression loop. Rarer named title but real
  work.

---

## What this means for our positioning

Three short takeaways for the team:

1. **Robotics infra services are extremely high-leverage.** Every
   robotics team has the same underlying needs — CI with
   hardware-in-the-loop, log capture, observability, deployment,
   fleet ops, OTA. A productized service offering for any one of
   these scales across customers far better than bespoke
   perception or controls work. The same engagement template
   ships at three different customers.
2. **Foxglove's growth proves there is an enterprise market
   here.** Robotics observability used to be considered internal
   tooling that no one would pay for. Foxglove's funding and
   revenue trajectory says otherwise. We can ride that proven
   demand without competing with Foxglove directly — we wire it
   in, build custom panels, and own the integration layer.
3. **The middleware vendors (Open Robotics / OSRA, Apex.AI,
   ZettaScale, eProsima, NVIDIA, Foxglove, Formant, InOrbit) are
   where partner-program leverage lives.** Joining OSRA, NVIDIA
   Inception, the Foxglove Partner Network, and Formant Solutions
   Partner early matters more than a marketing budget for an infra
   services shop.
4. **The named-title supply is small.** "ROS 2 Engineer" and
   "Robotics Platform Engineer" are still rare enough that
   showing up in the top search results — through OSS
   contributions, ROSCon talks, OSRA visibility — pays off
   disproportionately for both hiring and inbound sales.
