# The Simulation and Digital-Twin Market

> Market intel for our team. The companies below are the landscape we
> operate in as a simulation / digital-twin services shop. Some are
> potential customers, some are partners we can integrate with, some
> are competitors, some are talent sources for our hires, and some
> are reference points for stack and case studies. Comp bands are
> included so we set our own salaries fairly against the market.

## What this file is for

When we pitch a new client, we sometimes need to position against
the big names ("we deliver a slice of what Applied Intuition does,
smaller and more bespoke", or "we build the same Omniverse pipelines
BMW runs internally, scaled for a mid-market plant"). When we hire,
we benchmark against NVIDIA / Applied Intuition / DeepMind comp so
our offers don't read as low. When we read CoRL / RSS / SIGGRAPH
papers, half are from teams listed here. This is our shared map of
the landscape.

See also: `01-examples.md` (deployed twins and sim products),
`05-projects.md` (what we sell), `06-courses.md` (where our team
learns from), `00-basics.md` (concrete agency project patterns).

## How to read each entry

For each company below: what they do, the tech stack they're known
to use, the TC band our team competes with, the location, and
**what they mean to us** — one of:

- *Potential customer* — their internal teams sometimes hire
  agencies for overflow, integration, or specialized work.
- *Partner candidate* — they run a formal partner / reseller /
  inception / connector program we could join.
- *Competitor* — they sell into the same RFPs we do.
- *Talent source / talent risk* — we hire from them; our team might
  leave to them.
- *Reference point* — published work, stack, or case studies we
  study but don't directly compete with.

---

## Big tech and established labs

Bigger teams, more process, top-of-band comp. Mostly *reference
points* for stack and case studies, *talent risks* for senior ICs,
and a small subset are *partner candidates*.

- **NVIDIA (Isaac Sim, Isaac Lab, GR00T, Omniverse, Cosmos,
  Replicator)** — the single largest robotics-sim employer on Earth.
  The teams behind Isaac Sim, Isaac Lab, Cosmos, Replicator, USD
  tooling. Reported median TC ~$270k; senior staff $400k+. Multiple
  US offices + Tel Aviv + Munich.
  *To us:* **partner candidate** via NVIDIA Inception (free DGX
  cloud credits, NVIDIA Connect intros to enterprise customers, GTC
  speaking slots) and the Omniverse Connector / Solution Partner
  program; reference point for the Isaac stack; sometimes a
  customer for outsourced Isaac Sim integration, Replicator data
  pipelines, and USD asset conversion.

- **Google DeepMind** — MuJoCo team + sim infra for RT-X, Gemini
  Robotics, MuJoCo Playground. Mostly London / Mountain View.
  Famously hard to break into.
  *To us:* reference point for differentiable physics (MJX) and
  RT-X-style data flywheels; talent risk in London.

- **Microsoft (Project AirSim, Mesh, Azure Digital Twins)** — sim
  for AV / robotics / industrial. Redmond + Cambridge UK. AirSim
  itself is archived; Microsoft continues to invest in successor
  work and Azure Digital Twins for industrial / smart-buildings.
  *To us:* **partner candidate** for Azure Digital Twins resale
  through the Microsoft Partner Network; reference point.

- **Apple, Meta Reality Labs** — sim for AR / embodied AI / Habitat.
  Strong research culture; Habitat 3.0 is from Meta.
  *To us:* reference point. Habitat / HM3D is a useful dataset for
  our indoor-scan twins.

- **Toyota Research Institute (TRI)** — Drake + manipulation sim.
  Cambridge MA + Los Altos. Excellent research-grade engineering;
  comp $250-400k.
  *To us:* reference point. Drake is genuinely useful open source
  for contact-rich manipulation sim work we deliver.

- **BMW Group (Digital Twin / Omniverse factory pipelines)** —
  publicly known for running their planning pipeline on NVIDIA
  Omniverse (Plant Munich, Debrecen). German auto-industrial comp;
  on-site Munich / Regensburg.
  *To us:* reference point and **aspirational customer profile** —
  the BMW-on-Omniverse case study is the single best argument we
  make to mid-market manufacturers ("the same stack BMW uses, on
  your scale").

- **Siemens, ABB, FANUC, KUKA** — industrial sim suites (Process
  Simulate, RobotStudio, ROBOGUIDE). European / Japanese; lower
  comp than US tech but stable.
  *To us:* reference points; their CAD / robot-program output is
  often the input format we have to integrate against in factory
  twins.

- **Unity, Unreal / Epic Games** — engine vendors expanding into
  robotics sim. Unity Industrial Collection and Unreal's industrial
  / digital-twin push (Twinmotion, Custom License) are the
  flagships.
  *To us:* **partner candidates** via Unity for Industry partner
  program and Epic's Unreal Engine Verified Service Partner
  program; reference points for non-Omniverse engine choices.

- **Ansys, Altair, Dassault Systemes** — CAE / CFD with robotics
  integration. Heavy mechanical-engineering culture; sim is one
  product line of many.
  *To us:* reference points; potential integration partners when a
  customer already runs Dassault 3DEXPERIENCE.

- **Bentley Systems, Hexagon** — infrastructure / AEC digital twins
  at scale (iTwin platform, Smart Digital Realities). Pittsburgh /
  Stockholm / global. Enterprise comp; sales-led.
  *To us:* **partner candidates** via Bentley iTwin Partner Program
  and Hexagon Smart Digital Realities partner network; reference
  points and route to AEC enterprise deals we couldn't reach alone.

---

## Sim-native startups founded or scaled 2020-2025

Where the explosive growth and comp variance live. Most did not
exist 4 years ago.

- **Applied Intuition** (founded 2017, valued **$15B Mar 2025** at
  $600M Series F) — AV simulation + ADAS / defense test platforms.
  Hiring aggressively across CA / MI / DC. Sim engineers clear
  $300-450k TC.
  *To us:* **direct competitor** in any AV / ADAS sim RFP we
  encounter, and increasingly in defense sim. We win on smaller
  deals, faster turnaround, and per-customer bespoke pipelines
  (their platform play assumes 7-figure ACV). Also a talent risk.

- **Parallel Domain** (founded 2017, scaled 2023+) — synthetic data
  for AV / perception. Acquired by Applied Intuition in 2024.
  *To us:* reference point for procedural synthetic-data generation;
  now part of Applied Intuition's competitive surface.

- **Foretellix** (founded 2018, scaled 2023+) — scenario-based AV
  validation. Israeli / US offices.
  *To us:* reference point and partial competitor on AV scenario
  coverage work.

- **Cognata** (AV simulation, also services) — Israel / US. Has a
  meaningful services arm beyond the product.
  *To us:* **direct competitor** on AV sim services work; reference
  point.

- **NODAR** — AV sim adjacent (stereo perception sim). Raised
  meaningful rounds 2023-2024.
  *To us:* reference point.

- **DUALITY AI** — Falcon synthetic-data / sim platform. US-based;
  positions explicitly as services + platform.
  *To us:* **competitor candidate** on Omniverse-adjacent
  synthetic-data engagements; we haven't run against them in a
  pitch yet, but expect to. Hedge until we have direct experience.

- **Genesis Project** (CMU + collaborators, 2024) — open universal
  sim. Pre-product / research-focused; will likely spin out a
  company.
  *To us:* reference point and a stack we should be fluent in
  (differentiable, fast, free).

- **Hillbot** (2024, ex-Stanford) — generative sim assets via
  diffusion models.
  *To us:* reference point.

- **Foxglove** (2021, ex-Cruise founders) — observability for
  robotics, sim-adjacent tooling.
  *To us:* tool we use; **partner candidate** if they formalize a
  consulting partner directory.

- **Spear AI, Cogniteam** — observability + sim-adjacent tooling
  for robotics teams.
  *To us:* reference points.

- **Cesium (ion + Cesium for Omniverse)** — geospatial digital
  twins; dominant 3D-tiles platform.
  *To us:* **partner candidate** via the Cesium Certified Developer
  program — a real route into geospatial-twin engagements where we
  need streaming tiled terrain in Omniverse / Unreal.

- **Skild AI, Physical Intelligence, Figure, 1X, Apptronik,
  Generalist** — all have growing internal sim / synthetic-data
  teams to feed VLA training. Comp at the high end ($350-600k TC at
  senior IC).
  *To us:* talent risks for our humanoid-curious senior ICs;
  reference points for Isaac-Sim-based VLA pipelines.

- **Matterport, Polycam, Luma AI, Scaniverse (Niantic)** —
  consumer-side 3D capture, increasingly used by industrial
  customers.
  *To us:* **partner candidates / capture-layer platforms** —
  Matterport Capture Services Partner Network and Polycam Pro
  custom integrations are the realistic ones. Common capture layer
  for AEC and real-estate twins we deliver.

- **NavVis** — industrial AEC mapping (large-site indoor / outdoor
  scans).
  *To us:* **partner candidate** via NavVis Partner Network for
  industrial AEC twins.

- **Diffuse Bio / Diffuse Drive** (small but emerging, 2024+) —
  diffusion-based sim asset generation. Watch list.
  *To us:* reference points; hedge — we haven't validated their
  commercial maturity.

- **NVIDIA Cosmos partner ecosystem** — a growing number of new
  startups building products on top of Cosmos world models. Likely
  a meaningful 2026 hiring source and partnering surface.
  *To us:* watch list; potential co-marketing surface if we ship a
  reference Cosmos integration.

---

## Defense and dual-use simulation

Growing fast since 2022 alongside the broader defense-tech wave.
Comp often beats commercial; US citizenship / clearance gates many
US roles.

- **Forterra** (formerly Robotic Research) — autonomy stack for
  ground vehicles with substantial in-house sim. US, defense-
  heavy.
  *To us:* **competitor** on defense-sim services where we both
  bid; reference point.

- **Anduril, Shield AI, Saronic, Helsing** — defense primes / scale-
  ups with internal sim teams.
  *To us:* talent risks; not realistic agency customers (most work
  is classified or in-house). Reference points for systems culture.

- **Tata Elxsi simulation services, HCLTech, TCS, Wipro** —
  large-services firms with AV / defense sim divisions; staff-aug
  pricing.
  *To us:* **competitors** on enterprise RFPs that price on
  headcount; we win on speed and depth, lose on scale.

---

## Competing simulation and digital-twin services shops

The agencies and consultancies we'll run into in sales processes.
Most are larger than us; we win on responsiveness, verticalization,
and depth on a specific stack (Omniverse + Isaac Lab + USD, or
iTwin / Cesium for AEC twins). We can name a handful with
confidence; the long tail of regional shops is real but harder to
size from public info.

- **Cognata (services arm)** — AV sim services beyond their
  platform. Real published work.
  *Where we beat them:* smaller bespoke deals, non-AV verticals.

- **DUALITY AI** — Falcon platform plus services. Pitches into
  Omniverse-adjacent synthetic-data work.
  *Where we beat them:* per-customer fine-tuning depth; we don't
  push a platform.

- **Forterra (ex-Robotic Research)** — defense ground-autonomy
  sim work.
  *Where we beat them:* commercial / industrial twins outside
  defense.

- **Tata Elxsi, HCLTech, TCS, Wipro AV-sim divisions** — large
  Indian-services firms with growing AV / industrial sim
  practices. Staff-augmentation pricing.
  *Where we beat them:* productized outcomes, fixed-cost
  engagements, IP we own rather than billed hourly.

- **MathWorks consultancy partners (Simulink integrators)** — many
  small shops in the MathWorks Consulting Partner directory deliver
  Simulink / Simscape-based sim work, which crosses our path on
  controls-heavy twins.
  *Where we beat them:* modern stacks (Isaac Lab, MuJoCo, USD)
  where they're locked to MATLAB.

- **Mid-tier Bentley iTwin / Cesium / Hexagon partner shops** —
  many AEC consultancies hold these partner badges; some are real
  competitors when an AEC client picks a twin platform first and
  shops integrators second.
  *Where we beat them:* robotics-fluent integration (most AEC
  partners are CAD / surveying houses, not robotics shops); we win
  the deal when the twin must drive a robot.

- **Smaller regional shops** — too many to name individually. Most
  aren't directly competitive because their lead pipelines are
  local. Hedge: we should expect to discover one or two strong
  regional competitors per major sales region.

---

## Partnership and reseller programs worth joining

Concrete programs where applying as an agency unlocks credits,
sales co-marketing, customer pipeline, or technical certification
we can put in proposals.

- **NVIDIA Inception** — the highest-leverage one for our shop.
  Free DGX cloud credits, NVIDIA Connect intros to enterprise
  customers, GTC speaking slots, marketing co-promotion. Open to
  AI / robotics shops under ~$50M revenue. Apply at
  nvidia.com/en-us/startups.
- **NVIDIA Omniverse Connector / Solution Partner program** —
  formal recognition for shipping Omniverse Kit extensions or
  Connectors. Drives both technical credibility and enterprise
  referrals into Omniverse engagements.
- **Bentley iTwin Partner Program** — partner badge plus access to
  iTwin developer SDKs, co-marketing on AEC / infrastructure twin
  case studies, route into enterprise deals we couldn't reach
  cold.
- **Hexagon Smart Digital Realities partner network** — similar
  AEC / industrial-twin partner channel.
- **Matterport Capture Services / Partner Network** — listed as a
  capture-services partner for AEC and real-estate twins;
  referral pipeline for digital-twin work.
- **NavVis Partner Network** — industrial AEC mapping (large-site
  twins).
- **Unity for Industry partner program** — Unity's industrial /
  digital-twin partner channel; relevant when a customer is
  Unity-standardized.
- **Epic Games Unreal Engine Custom License + Verified Service
  Partner** — official Unreal industrial / digital-twin services
  badge.
- **Cesium Certified Developer program** — technical certification
  for Cesium ion / Cesium for Omniverse work; useful for
  geospatial-twin proposals.
- **MathWorks Consulting Partner program** — partner badge for
  Simulink / Simscape integration work; relevant when a customer's
  controls team is MATLAB-native.
- **AWS Activate / Google Cloud for Startups / Microsoft for
  Startups (Azure)** — $25k-$200k of cloud credits available;
  useful for GPU-heavy Isaac Lab training and Omniverse rendering
  during initial customer engagements.
- **Hugging Face Enterprise Hub / Expert Acceleration Program** —
  partner-tier discounts for our customers when policies / models
  trained in sim are deployed via HF.
- **Applied Intuition partner program** — public surface is thin
  on details. Hedge: worth applying or asking, but don't assume
  it exists as a defined channel.

Most of these are free to apply to. The realistic high-value ones
for a sim / digital-twin services shop are: NVIDIA Inception,
NVIDIA Omniverse Solution Partner, Bentley iTwin, Cesium Certified
Developer, and Matterport / NavVis.

---

## Comp bands (for setting our own salaries)

Approximate TC bands for senior IC (3-7 years exp), 2025-2026 Bay
Area / NYC / Seattle. Sources: levels.fyi, 2025 Robotics Salary
Guide, public funding rounds. Startup TC is noisy because it
includes illiquid common shares.

- **NVIDIA:** $300-450k+ (median $270k all levels; staff/principal
  $500k+)
- **Applied Intuition:** $300-450k
- **Apple, Meta Reality Labs:** $300-500k
- **Google DeepMind:** $300-500k
- **TRI:** $250-400k
- **Foretellix, Parallel Domain (now Applied Intuition):** $230-380k
- **Top humanoid startups (Figure, 1X, PI, Skild, Apptronik):**
  $350-600k+ (heavy equity, lottery-ticket weighting)
- **Industrial / CAE primes (Siemens, ABB, FANUC, Ansys,
  Dassault):** $180-280k
- **Sim-adjacent tooling startups (Foxglove, Spear AI, Cesium):**
  $200-350k
- **Bentley, Hexagon, Matterport, NavVis:** $180-300k enterprise
  bands; less variance, more equity-in-public-stock.

US / EU remote roles are usually 20-40% lower; London is a partial
exception thanks to DeepMind + Wayve compression.

**For our hires:** band our base salaries at the sim-tooling /
CAE-prime range or above. Below that and our offers read as low
against the market our team is comparing against. Equity-heavy
frontier humanoid startups are not direct comp competitors for our
headcount; their candidates are taking lottery-ticket risk we
can't match.

---

## Hiring market signal

From the 2025 Robotics Salary Guide and market reports:

- The Robotic Simulator market is **software-dominated** (~72%
  software share in 2025).
- Physical-AI simulation + digital-twin market projected to grow
  **$3.8B (2025) -> $34.6B (2034), ~28.5% CAGR**, the highest of
  any segment in this analysis.
- NVIDIA has hired aggressively around Isaac Sim / Isaac Lab
  through 2024-2025; hundreds of Isaac-adjacent roles open at any
  given time.
- "RL" carries a **+33% salary premium** when listed as a required
  skill; "Isaac" / "Omniverse" / "USD" each show similar premiums
  in 2025 postings.

Translation: this is the highest-growth segment in robotics by
both market CAGR and headcount. Broad employer pool, pure-software
delivery, low hardware-risk for our shop. Good market to be
positioning into.

---

## Remote / hybrid posture by employer type

Useful for understanding which talent pools are accessible to us
(remote-friendly = larger candidate pool for our remote hires).

- **AV-sim primes (Applied Intuition, Foretellix, Cognata):**
  hybrid 3-5 days on-site at HQs; some training / data roles
  flex.
- **NVIDIA Isaac / Omniverse:** hybrid; Bay Area / Austin / Tel
  Aviv / Munich.
- **Foundation-model sim (DeepMind MuJoCo, NVIDIA Research):**
  remote-friendly for research and ML infra; less for product
  Omniverse work.
- **Humanoid startups with sim teams (Figure, 1X, Apptronik):**
  strictly on-site.
- **Industrial CAE (Siemens, ABB, Dassault, Ansys):** hybrid; many
  EU / Japan locations.
- **AEC twin platforms (Bentley, Hexagon, Matterport, NavVis):**
  hybrid; large field-service component.
- **Sim-adjacent tooling (Foxglove, Cesium):** fully remote,
  globally distributed. Our biggest direct competitors for
  distributed-team sim talent.

---

## Title decoder

The same role carries five different names across companies. Use
this when reading competitor job ads or when writing our own
postings.

- **Sim Software Engineer** — umbrella title (NVIDIA, Applied
  Intuition, Cognata). Owns env construction, training
  integration, synthetic-data generation.
- **Robotics Simulation Engineer** — slightly more robotics-fluent
  variant (Figure, 1X, Apptronik, TRI). Often ROS-adjacent.
- **Digital Twin Engineer** — AEC / industrial framing (Bentley,
  Hexagon, BMW, Siemens). USD / iTwin / IFC-fluent; CAD
  integration is half the job.
- **RL Research Engineer (Sim)** — training-focused (DeepMind,
  NVIDIA Research, PI, Skild). JAX / PyTorch heavy.
- **Synthetic Data Engineer** — narrow specialty (Parallel Domain
  / Applied Intuition, NVIDIA Replicator team, DUALITY).
  Procedural generation, randomization, validation.
- **3D / USD / Asset Engineer** — overlaps with technical artist
  (NVIDIA, BMW, Unity, Unreal). Houdini, Blender, USD pipeline.
- **Scenario Engineer** — AV-specific (Foretellix, Applied
  Intuition, Cognata). OpenSCENARIO / OpenDRIVE-fluent.
- **Geospatial / 3D Tiles Engineer** — niche (Cesium, NavVis,
  Hexagon). Streaming tiled data, geo coordinate systems.
- **Simulation Infrastructure Engineer** — platform-side
  (large teams at NVIDIA, Applied Intuition, Waymo-sim). GPU
  orchestration, distributed sim.

---

## What this means for our positioning

Four short takeaways for the team:

1. **Applied Intuition is our direct competitor in AV sim, and
   increasingly defense sim.** Win on smaller bespoke deals,
   non-AV verticals, and per-customer pipelines. Don't try to
   out-platform them.
2. **NVIDIA Omniverse is the platform leverage point.** Joining
   Inception and pursuing Omniverse Solution Partner status early
   matters more than a marketing budget. The BMW-on-Omniverse case
   study is our best mid-market pitch anchor.
3. **AEC twins are a real second front.** Bentley iTwin, Cesium,
   Matterport, NavVis partner programs open enterprise channels we
   can't reach cold. Robotics fluency is our differentiator inside
   that crowd.
4. **The hyperscalers and humanoid frontiers are reference points,
   not competitors.** They serve different price points (internal
   headcount, custom silicon, frontier equity) than we sell.
   Mention them when a customer asks "who else does this?" — not
   in our positioning.
