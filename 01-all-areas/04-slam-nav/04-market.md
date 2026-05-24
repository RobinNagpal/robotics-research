# The SLAM and Navigation Market

> Market intel for our team. The companies below are the landscape we
> operate in as a SLAM / navigation services shop. Some are potential
> customers, some are partners we can integrate with, some are
> competitors, some are talent sources for our hires, and some are
> reference points for stack and case studies. Comp bands are
> included so we set our own salaries fairly against the market.

## What this file is for

When we pitch a new client, we sometimes need to position against
the big names ("we do what Slamcore does, more verticalized and
with bespoke integration"). When we hire, we benchmark against
NVIDIA / Waymo / Skydio comp so our offers don't read as low. When
we read ICRA / IROS / RSS papers on SLAM and motion planning, half
are from teams listed here. This is our shared map of the
landscape.

See also: `01-examples.md` (deployed products and papers),
`05-projects.md` (what we sell), `06-courses.md` (where our team
learns from), `00-basics.md` (concrete SLAM / navigation agency
project patterns).

## How to read each entry

For each company below: what they do in SLAM / navigation, the
tech stack they're known to use, the TC band our team competes
with, the location, and **what they mean to us** — one of:

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

## Big tech and established AV / robotics players

Bigger teams, more process, slower cadence. Mostly *reference
points* for stack and case studies, and *talent risks* for senior
ICs who know LIO-SAM / Cartographer / GTSAM internals.

- **Waymo (Alphabet)** — AV localization, HD-map building, lidar +
  camera + radar fusion, factor-graph state estimation at scale.
  Stack: C++ + custom internal factor-graph libs (Ceres ancestors),
  Bazel, TPU training for learned components. Low-hundreds across
  perception / localization. Median TC ~$232k; senior IC
  $300-450k. SF / Mountain View / Pittsburgh / Phoenix.
  *To us:* reference point for HD-map-based localization at city
  scale; talent risk for senior localization ICs.

- **Cruise (GM)** — re-staffing through 2025 after the 2023
  setback. SF. Historically strong lidar SLAM and HD-mapping team.
  Comp competitive, morale historically bruised.
  *To us:* reference point and talent source — laid-off / departing
  Cruise localization engineers were on the market through 2024-25
  and are still surfacing.

- **Zoox (Amazon)** — full AV stack, Foster City CA. Custom
  vehicle with symmetric sensors. C++ + PyTorch; Amazon L5/L6
  bands.
  *To us:* reference point for sensor-symmetric localization.

- **Pony.ai** — robotaxi + robotruck, China + US. Lidar-heavy
  stack. Recently IPO'd. Comp lower than US AV labs.
  *To us:* reference point.

- **Aurora** — autonomous trucking, Pittsburgh + Bay Area + Dallas.
  Lidar-first, FirstLight FMCW lidar. Senior IC $250-400k.
  *To us:* reference point for highway-scale localization and
  HD-map maintenance.

- **Motional (Hyundai + Aptiv)** — robotaxi, Boston / Pittsburgh /
  Vegas / Singapore. Published nuScenes dataset.
  *To us:* reference point; nuScenes is a core benchmark for our
  fusion work.

- **NVIDIA (Isaac, DRIVE, cuVSLAM, Nova Carter)** — Isaac ROS
  Visual SLAM (cuVSLAM), Isaac Perceptor, nvblox 3D reconstruction,
  Nova Orin reference platform. Stack: C++ + CUDA + ROS 2 + PyTorch
  + TensorRT. Multiple 20-80-engineer teams. Median TC ~$270k;
  senior staff $400k+.
  *To us:* **partner candidate** via NVIDIA Inception (free DGX
  cloud credits, Isaac early access, sales co-marketing); reference
  point for the Isaac ROS 2 stack; sometimes a customer for
  outsourced Isaac Sim integration and Nav2-on-Jetson tuning.

- **Tesla Autopilot** — camera-only mapping-free driving with
  occupancy networks. Secretive. PyTorch + custom C++; Dojo. Base
  lower than Waymo, equity-heavy.
  *To us:* reference point for mapping-free, occupancy-network
  navigation; not a partner, not a customer.

- **Apple (ARKit, Vision Pro)** — visual-inertial SLAM at consumer
  scale, room mesh. Metal + CoreML + custom C++. Senior IC
  $300-500k.
  *To us:* reference point for on-device VIO; ARKit scan output is
  occasionally an input format for our AEC scanning work.

- **Mobileye** — vision-centric ADAS + REM crowd-sourced HD maps.
  Jerusalem + Detroit + San Jose. C++ on EyeQ silicon. Senior IC
  $230-380k in US.
  *To us:* reference point for crowd-sourced HD mapping at scale.

- **Boston Dynamics (Hyundai)** — Spot Autowalk graph-based site
  navigation, Atlas locomotion + perception. Boston. C++ first,
  internal state-estimation frameworks. Senior IC $230-380k.
  *To us:* **potential customer** for Spot SDK integration work for
  enterprise clients; reference point for legged state estimation;
  brand carries credibility on our team's resumes.

- **Skydio** — drones for consumer / defense / public safety.
  Redwood City CA. One of the most polished on-device VIO stacks
  shipping. C++ + PyTorch. Senior IC $250-400k.
  *To us:* **partner candidate** via Skydio Developer SDK for
  drone-based inspection work; reference point for tightly-coupled
  VIO at the edge; talent risk for senior VIO ICs.

- **Amazon Robotics (Kiva ancestry)** — warehouse fleet
  localization at huge deployment volume; fiducial + lidar +
  wheel-odometry fusion across thousands of drives. Java + C++,
  ROS-adjacent internal frameworks. North Reading MA + Bay Area.
  *To us:* **potential customer** for niche warehouse navigation
  consulting; reference point for at-scale industrial deployments.

- **Symbotic** — palletizing AMRs + warehouse autonomy. Wilmington
  MA. Growing fast on Walmart contracts.
  *To us:* potential customer for niche consulting; reference point.

- **iRobot (Roomba), Roborock, Ecovacs** — consumer floor robots.
  vSLAM + lidar SLAM on a $30 BOM. Tight cost / power constraints
  drive impressive engineering. Comp lower than enterprise robotics
  (Roomba $150-220k senior; Chinese shops vary).
  *To us:* reference point for tightly-constrained embedded SLAM;
  occasionally a talent source for ICs who know how to ship on
  cheap silicon.

- **Locus Robotics, Geek+, Fetch (Zebra), 6 River Systems
  (Ocado-then-shutdown 2023)** — warehouse AMRs running ROS-adjacent
  stacks. Locus is Wilmington MA. Geek+ is China. Senior IC
  $180-280k in US; less abroad.
  *To us:* **potential customers** for short-term Nav2 / costmap /
  fleet-coordination contracts; competitive comp band for our own
  hires.

- **DJI Enterprise** — drone VIO + obstacle avoidance shipping at
  the largest unit volume of any drone maker. Shenzhen. Lower base
  comp; large RSU pool for senior.
  *To us:* **partner candidate** via DJI Enterprise SDK for
  drone-data workflows; reference point for VIO at huge volume.

---

## Defense / dual-use companies (growing fast since 2022)

Exploded post-2022 with US/EU defense budgets. Comp often beats
commercial robotics. US citizenship required for most US roles; a
subset needs SECRET clearance.

- **Anduril** — Lattice, Ghost (sUAS), Bolt (loitering munition),
  Roadrunner (counter-UAS), maritime (Dive-LD). Low-hundreds across
  autonomy. C++ + Rust + PyTorch with in-house data platform.
  Senior IC $350-500k+.
  *To us:* talent risk; not a realistic customer for an outside
  agency (most work is classified or in-house). Reference point
  for systems-engineering culture and GPS-denied navigation.

- **Shield AI** — Hivemind autonomy stack for V-BAT and external
  airframes. The reference name for GPS-denied flight in 2024-25.
  C++ + PyTorch + custom middleware. Median ~$228k, senior IC
  $300-450k. San Diego.
  *To us:* talent risk; reference point for VIO + visual-inertial
  navigation in GPS-denied environments.

- **Saronic** — autonomous surface vessels; maritime SLAM under wave
  motion, water-surface and radar-based localization. Series-B+
  2024 at $1B+. Small team, Austin TX.
  *To us:* reference point for maritime SLAM, which is a plausible
  niche vertical for us if we land a port / harbor customer.

- **Helsing** (Germany) — defense AI, Munich + London + Paris. EUR
  150-250k + equity.
  *To us:* talent risk on the EU side; reference point.

- **Saildrone, Vannevar Labs, HavocAI, Mach Industries** — younger
  dual-use names. Small teams, fast hiring.
  *To us:* mostly reference points.

---

## SLAM / nav startups founded or scaled 2020-2025

Where the explosive growth and comp variance live. Most did not
exist 4 years ago.

- **Wayve** (UK, 2017, Series-C 2024 at $1B+) — end-to-end driving
  foundation models, mapping-free navigation. 100+ across perception
  / planning. London + Mountain View. PyTorch + JAX.
  *To us:* reference point for mapping-free end-to-end driving;
  talent risk in London.

- **Nuro** (2016, but scaled and re-focused 2023+) — last-mile
  delivery vehicles, recently pivoted toward licensing the autonomy
  stack. Mountain View. PyTorch + C++.
  *To us:* reference point for low-speed urban navigation.

- **Gatik** (2017) — middle-mile autonomous trucking on fixed
  routes; lighter HD-map burden than open-domain AV. Mountain View
  + Toronto.
  *To us:* reference point for fixed-route autonomy, which is a
  realistic verticalization pattern for our own work.

- **Saronic** — see Defense section above.

- **Bedrock Robotics** (2023) — autonomous earth-moving (excavators,
  bulldozers). SF. Off-road, no lane lines, terrain mapping.
  *To us:* reference point for off-road / construction navigation,
  which is a distinct skillset from on-road AV.

- **Field AI** (2023) — outdoor / off-road foundation policies for
  inspection, construction, mining. Mission Viejo / Pasadena.
  *To us:* reference point for off-road navigation foundation models;
  a possible long-tail talent risk.

- **Cobot** (2022, ex-Amazon Robotics VP Brad Porter) — collaborative
  mobile manipulator running a Nav2-style stack at scale. Boston,
  low-tens.
  *To us:* reference point for production-grade Nav2 deployment;
  potential talent source for engineers who know the BT navigator
  internals.

- **Pickle Robot** (2018, scaled 2023+) — truck-unloading; their
  navigation problem is trailer-interior mapping under sparse
  features and motion. Cambridge MA.
  *To us:* reference point — their public material is one of the
  better small-team case studies we point at in client decks.

- **Anduril Ghost / Bolt / Roadrunner** — see Defense section above.
  Ghost in particular is the canonical reference for GPS-denied
  UAV navigation.

- **Shield AI** — see Defense section above.

- **Reflex Robotics** (2023) — humanoid mobile base. NYC. Tens of
  engineers.
  *To us:* reference point for indoor humanoid navigation.

- **Diligent Robotics (Moxi)** — hospital corridor delivery robot,
  scaled 2022+. Austin TX. Strong on social navigation around staff
  and patients.
  *To us:* reference point for socially-aware navigation in
  occupied environments; potential customer for short-term Nav2
  tuning if their internal team is constrained.

- **Brain Corp** — floor-scrubber and inventory-robot autonomy SDK
  licensed to Tennant, SoftBank Whiz, Dane Technologies, and others.
  San Diego. ROS-adjacent internal stack.
  *To us:* **potential partner** if we deliver vertical
  integrations on top of their SDK; reference point for
  autonomy-as-a-service business model.

- **Verity** (Switzerland) — indoor warehouse drones flying at night
  for inventory; tightly-bounded indoor SLAM at scale. Scaled
  2022+. Zurich.
  *To us:* reference point for indoor drone SLAM; possible EU
  partner.

- **Exotec** (France) — Skypod 3D-grid warehouse navigation. ~$2B
  valuation. Lyon / Bordeaux.
  *To us:* reference point for structured-environment navigation.

- **Physical Intelligence (Pi), Skild, Figure, 1X, Apptronik** —
  humanoid / VLA companies whose locomotion teams overlap with
  navigation. PyTorch + C++ + Isaac Sim.
  *To us:* mostly reference points; talent risk for ICs who can
  cross between SLAM and learned locomotion.

---

## Competing SLAM / nav services shops

Honest list. We'll run into these in sales processes. We're
smaller than most. Hedging where we're uncertain.

- **Spectacular AI** (Finland) — commercial visual-inertial SLAM
  SDK (cross-platform: iOS, Android, Linux, Jetson, RealSense, OAK,
  ZED). Sell both SDK licenses and integration services. ~20
  people, post-seed. Real direct overlap with our integration work.
  *Where we beat them:* full-stack delivery beyond just the SLAM
  module — Nav2 integration, fleet management, customer-facing
  dashboards. They are also a *partner candidate* (see partner
  section below) since their SDK is a credible build-block for our
  delivery.

- **Slamcore** (UK) — commercial visual-inertial SLAM SDK targeting
  AMRs and consumer robots. ARM-Cambridge-backed historically.
  Note: there were 2023-24 signals of restructuring / spin-down;
  treat status as **uncertain** and verify before pitching against
  them in a deck.
  *Where we beat them (if still operating):* integration + vertical
  delivery rather than pure SDK licensing.

- **Inkonova** (Sweden) — drone autonomy and SLAM, with a mining /
  underground focus historically. Small team. Status worth
  verifying before naming them in a competitive context.
  *Where we beat them:* broader vertical coverage outside
  underground / mining.

- **ROS Industrial Consortium services partners** — Southwest
  Research Institute (SwRI), Fraunhofer IPA, PickNik Robotics, and
  the rotating roster of ROS-I consortium members offer SLAM /
  Nav2 / MoveIt integration as services. PickNik in particular is
  one of the more visible US Nav2 / MoveIt consultancies and
  competes directly with us on Nav2 RFPs.
  *Where we beat them:* productized verticals (e.g. "warehouse
  Nav2 tuning package") and fixed-cost outcomes rather than
  hourly T&M.

- **Larger generalist robotics consultancies** — Apex.AI (safety-
  certified ROS 2), eProsima (DDS / FastDDS services), Intermodalics
  (Belgium, ROS 2 services). All are bigger or more specialized
  than us in their respective niches; we don't usually overlap
  except on Nav2 + DDS networking jobs.

- **Smaller regional / freelance shops** — too many to name. Most
  aren't directly competitive because their lead pipelines are
  local.

We are deliberately not listing names where we don't have
confidence about current operating status. Update this section
when we learn more from actually losing or winning deals against
them.

---

## Partnership and reseller programs worth joining

Concrete programs where applying as an agency unlocks credits,
SDK access, sales co-marketing, or a customer pipeline. Hedging
where confidence is low.

- **NVIDIA Inception** — free DGX cloud credits, NVIDIA Connect
  intros to enterprise customers, GTC speaking opportunities, early
  Isaac ROS / Isaac Sim access. Open to AI / robotics shops under
  ~$50M revenue. Apply at nvidia.com/en-us/startups. **High value
  for us** — Isaac ROS Visual SLAM (cuVSLAM), nvblox, and Nova
  Carter are increasingly the default reference stack for new
  AMR deployments.
- **ROS Industrial Consortium (ROS-I)** — paid membership tiers
  (Bronze / Silver / Gold) administered by SwRI in the US and
  Fraunhofer IPA in Europe. Members get roadmap influence, training
  discounts, and visibility in the consortium directory. Worth it
  for credibility on industrial / manufacturing RFPs.
- **Open Source Robotics Alliance (OSRA)** — the post-OSRF
  governance body for ROS 2 / Gazebo / Open-RMF. Membership tiers
  exist; primary value is visibility in the ROS 2 ecosystem and
  modest roadmap influence. Worth it once we have a real ROS 2
  product position.
- **Foxglove** — observability / visualization for robotics. They
  have an enterprise / partner-ish offering and an active community.
  Status of a formal *agency* partner program is **uncertain** —
  worth a direct conversation rather than assuming it exists. In
  any case, Foxglove is the default visualization tool we use for
  debugging SLAM and Nav2 stacks at customer sites.
- **Spectacular AI** — they explicitly invite integration partners
  on their site. A realistic partnership: we deliver vertical
  integrations on top of their VIO SDK and route SDK-license deals
  to them. Worth a direct outreach.
- **AWS RoboMaker** — *partially deprecated* in 2024 (Amazon
  announced the simulation and fleet-management portions are being
  wound down). Cloud-extensions for ROS 2 still exist. **Verify
  status** before building partnership material around it.
- **AWS Activate / Google Cloud for Startups / Microsoft for
  Startups** — $25k-$200k of cloud credits available; useful for
  large-scale offline SLAM bundle adjustment and map-building jobs
  during initial customer engagements.
- **DJI Enterprise Software Partner** — for drone-data and
  drone-navigation workflows; relevant if we take on aerial-mapping
  work.
- **Boston Dynamics Spot Developer Partner / Technology Partner** —
  formal partner tracks exist; relevant if we take on Spot Autowalk
  / Spot mission-planning integrations for enterprise customers.

Most of the high-credit programs are free to apply to. The
realistic high-value ones for a SLAM / nav services shop, in
priority order: NVIDIA Inception, ROS Industrial Consortium,
Spectacular AI integration, and (if it exists in the form we
think) a Foxglove partner relationship.

---

## Comp bands (for setting our own salaries)

Approximate TC bands for senior IC (3-7 years), 2025 Bay Area / NYC.
Sources: levels.fyi, 2025 Robotics Salary Guide, Glassdoor self-
reports, public funding announcements. Startup TC is noisy because
it includes illiquid common shares.

- **NVIDIA, Waymo:** $300-450k (Waymo median $232k across levels,
  NVIDIA median ~$270k)
- **Apple, Tesla AV:** $300-500k+
- **Anduril, Shield AI:** $300-500k (Shield AI median ~$228k;
  heavy equity at both)
- **Wayve, Physical Intelligence, Skild, Figure, 1X:** $350-600k+
  (equity is the lottery ticket)
- **Boston Dynamics, Skydio, Aurora, Motional, Mobileye:**
  $230-400k
- **Mid-tier AMR shops (Locus, Geek+ US, Symbotic, Brain Corp,
  Cobot):** $180-280k
- **Consumer floor robots (iRobot, Roborock, Ecovacs US):**
  $150-220k
- **Perception / robotics SaaS (Foxglove, Spectacular AI,
  Roboflow, Voxel51):** $200-330k with full-remote optionality
- **SLAM / Nav2 consultancies (PickNik, SwRI, smaller shops):**
  $170-260k + variable bonus; closer to our market

Remote / EU usually 20-40% lower; London / Munich / Zurich close
the gap on the high end.

**For our hires:** band our base salaries at the mid-tier AMR
range or above. Below that and our offers read as low against the
market our team is comparing against. Equity-heavy frontier
startups (Wayve, Pi, humanoids) are not direct comp competitors
for our headcount; their candidates are taking lottery-ticket risk
we can't match.

---

## Hiring market signal

From the 2025 Robotics Salary Guide (907 jobs analyzed Nov-Dec
2025):

- Robotics Software Engineer median: **$189k**.
- "SLAM Engineer" and "Localization Engineer" remain among the
  highest-paid robotics-software sub-specialties (typically a
  $20-40k premium over generalist robotics-software roles at the
  same level).
- Defense / dual-use is the fastest-hiring vertical in 2024-25 for
  GPS-denied navigation skills.
- Global SLAM technology market: estimates vary widely
  ($300M-$700M in 2024 depending on definition), with industry
  reports projecting ~30%+ CAGR through 2030 driven by AMRs,
  AR/VR, and drones. Treat any single number with skepticism —
  market sizing for SLAM specifically is noisy because most of it
  sits inside larger AV / robotics / AR market totals.

Translation: SLAM and navigation are a narrower specialty than
generic robotics software, with a comp premium and a customer base
that spans warehouse AMRs, drones, AV, AR, and defense. Good
market for our shop's positioning.

---

## Remote / hybrid posture by employer type

Useful for understanding which talent pools are accessible to us
(remote-friendly = larger candidate pool for our remote hires).

- **AV labs (Waymo, Cruise, Zoox, Aurora, Motional):** hybrid 3-5
  days on-site; some offline / mapping / training roles flex.
- **Foundation-model navigation (Wayve, Pi, Field AI):**
  remote-friendly for research and ML infra; less for product
  navigation.
- **Humanoid startups (Figure, 1X, Apptronik, Cobot, Reflex):**
  strictly on-site.
- **Defense (Anduril, Shield AI, Saronic, Helsing):** mostly on-
  site; some non-classified hybrid.
- **AR / glasses (Apple, Meta Reality Labs):** on-site for hardware
  work, hybrid for app-layer SLAM.
- **Robotics SaaS / SDK shops (Spectacular AI, Foxglove, Brain
  Corp):** typically fully remote or remote-friendly, globally
  distributed. Our biggest direct competitors for distributed-team
  SLAM talent.
- **Industrial / AMR (Locus, Geek+, Symbotic, Verity, Exotec):**
  on-site in non-major-tech cities, often near warehouses or
  customer pilot sites.
- **Consumer floor robots (iRobot, Roborock, Ecovacs):** mostly
  on-site; China-based teams especially so.

---

## Title decoder

The same role carries five different names across companies. Use
this when reading job ads (competitor signaling) or when writing
our own postings.

- **SLAM Engineer** — narrow specialty (Skydio, Niantic, Magic
  Leap, Apple ARKit, Spectacular AI, Slamcore-when-operating, some
  AV labs). Pose, loop closure, VIO, factor graphs.
- **Localization Engineer** — AV-flavored umbrella (Waymo, Cruise,
  Zoox, Aurora, Motional). HD-map matching, particle filters,
  multi-sensor fusion against a prior map.
- **Sensor Fusion Engineer** — multi-modal (Mobileye, Shield AI,
  Anduril Lattice, Bosch, ZF, some AV). EKF / UKF / factor graphs,
  C++ heavy.
- **Nav2 Engineer / ROS 2 Navigation Engineer** — explicit Nav2
  experience (PickNik, SwRI, Locus, Cobot, Diligent, smaller AMR
  shops). Costmaps, planners, behavior trees, recovery behaviors.
- **Mapping Engineer** — HD-map building, change detection,
  semantic-map updates (Waymo, Aurora, Mobileye REM, TomTom,
  HERE). Often more data-engineering than real-time perception.
- **Autonomy Engineer (Navigation)** — defense / drone generalist
  with a navigation slant (Anduril, Shield AI, Saronic, Skydio).
- **Motion Planning Engineer** — adjacent specialty (search / opt
  / sampling-based planners). Sometimes bundled with navigation,
  sometimes separated.
- **State Estimation Engineer** — research-flavored variant of
  sensor fusion (Boston Dynamics, TRI, Pi). Strong factor-graph /
  estimation-theory background expected.
- **Perception & Localization Engineer** — combined role at
  smaller robotics startups where the same IC owns both the
  visual front-end and the back-end localizer.
- **Robotics Software Engineer (Navigation)** — generalist with
  ROS 2 / C++ comfort (Figure, Apptronik, Boston Dynamics, Saronic,
  most AMR shops). More systems integration than pure SLAM math.

---

## What this means for our positioning

Three short takeaways for the team:

1. **The AV labs and defense primes are reference points, not
   competitors.** Different price points (internal headcount,
   classified work) than we sell into. Mention them only when a
   customer asks "who else does this?"
2. **The SDK vendors (Spectacular AI, Slamcore, NVIDIA cuVSLAM)
   are dual-natured.** They are both build-blocks for our delivery
   *and* the competitors a customer might consider instead of us.
   We win by being the team that takes their SDK across the last
   mile — Nav2 integration, fleet, dashboards, and customer
   support — not by re-implementing what they already sell.
3. **The platform partnerships matter more than the marketing
   budget.** NVIDIA Inception for Isaac credibility, ROS Industrial
   Consortium for manufacturing credibility, and a real
   relationship with Spectacular AI and Foxglove for delivery
   leverage are the four levers worth pulling early.
