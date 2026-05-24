# The Multi-Robot and Fleet-Management Market

> Market intel for our team. The companies below are the landscape we
> operate in as a multi-robot / fleet-management services shop. Some
> are potential customers, some are partners we can integrate with,
> some are competitors, some are talent sources for our hires, and
> some are reference points for stack and case studies. Comp bands
> are included so we set our own salaries fairly against the market.
>
> Multi-robot work is among the highest-leverage verticals our shop
> can sell into. Every warehouse, hospital, mine, or facility that
> runs 5+ robots eventually hits the same problems — traffic
> deadlocks, charging-station contention, mixed-vendor coordination,
> observability gaps, shift-handoff confusion — and those problems
> are recurring operational pain, not one-off integrations. That
> shape favors retainer-style services revenue more than a typical
> integration project does.

## What this file is for

When we pitch a fleet-ops engagement, we sometimes need to position
against the big names ("we do what OpenRMF integrators do, but
embedded with your ops team"). When we hire, we benchmark against
Amazon Robotics / Symbotic / Waymo fleet-routing comp so our offers
don't read as low. When we read fleet-coordination papers and ICRA
multi-robot tracks, half are from teams listed here. This is our
shared map of the landscape.

See also: `01-examples.md` (deployed fleet products and papers),
`05-projects.md` (what we sell), `06-courses.md` (where our team
learns from), `00-basics.md` (concrete agency project patterns for
fleet work).

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

## Warehouse AMR fleet operators

The deepest concentration of real multi-robot deployments. Every
name here runs hundreds-to-thousands of robots in production, which
means real fleet-management problems and real budgets for help.

- **Amazon Robotics** — largest robotic fleet on Earth (reported
  750k+ mobile drive units across the FC network as of 2024-2025).
  WES (Warehouse Execution System) is one of the largest multi-robot
  software stacks in production anywhere. North Reading MA + Seattle
  + Berlin. Stack: Java + C++ on internal frameworks, with ROS-
  adjacent layers for newer Sequoia / Proteus generations. Senior IC
  $230-380k (Amazon L5-L6 bands).
  *To us:* talent source for fleet ICs leaving for smaller shops;
  reference point for at-scale fleet architecture. Not a realistic
  customer — they build everything in-house.

- **Symbotic** — case-handling AMR fleets for Walmart, Albertsons,
  Target distribution centers. 500-2000 bots per site typical.
  Wilmington MA. C++ + Python; tight controls integration. Senior
  IC ~$200-330k.
  *To us:* talent source; *potential customer* for niche overflow
  work around new-site bring-up and observability tooling, though
  most fleet work is internal. Reference point for high-density
  warehouse fleet coordination.

- **Locus Robotics** — third-party warehouse AMR provider (DHL, GXO,
  Boots). Wilmington MA. Fleets of 50-300 LocusBots per site, RaaS
  (robotics-as-a-service) revenue model. ROS-adjacent stack with
  cloud fleet manager. Senior IC ~$200-300k.
  *To us:* *potential customer* — Locus deploys into third-party
  warehouses where the warehouse operator sometimes wants custom
  integrations (WMS interop, custom KPIs) that Locus itself won't
  build. Partner candidate for those deployments.

- **Geek+** — Asia-Pacific warehouse AMR leader, expanding in EU and
  US since 2022. Beijing + Singapore + Dusseldorf. Goods-to-person
  and case-picking fleets. Senior IC EUR / SGD 80-160k.
  *To us:* reference point; potential EU partner if we expand there.

- **Fetch Robotics (Zebra Technologies)** — acquired by Zebra in
  2021 for $290M. Now part of Zebra's broader warehouse-automation
  stack. San Jose + Lincolnshire IL.
  *To us:* reference point; Zebra has a partner ecosystem (see
  partnerships section) which is more realistic to join than working
  with Fetch directly.

- **6 River Systems** — Shopify-spun in 2019, then sold by Shopify
  in 2023 to Ocado Group. Currently a 6 River + Ocado fleet stack.
  Waltham MA. Chuck collaborative AMRs.
  *To us:* reference point. Post-acquisition direction is still
  settling.

- **AutoStore** — cube-storage AMR system. Norwegian-founded; global
  install base in the thousands of sites. Senior IC NOK 800k-1.4M
  in Norway; US comp closer to $180-280k.
  *To us:* *partner candidate* via the AutoStore Authorized Partner
  / Integrator network — integrators do site design, WMS interop,
  and post-install support. Reference point for grid-based fleet
  coordination.

- **Exotec** — Skypod 3D-grid AMR system. French. Customers include
  Gap, Carrefour, Decathlon. Tens of integrator partners globally.
  *To us:* *partner candidate* via Exotec's integrator network;
  reference point for European warehouse fleet design.

- **Hai Robotics** — case-picking AMRs (HaiPick), originally Shenzhen
  with expanding US/EU presence post-2022.
  *To us:* reference point.

- **GreyOrange** — multi-robot warehouse fulfillment (GreyMatter
  fulfillment OS, Ranger AMRs). Atlanta + Gurgaon + Singapore.
  Senior IC $180-280k in US; lower in India.
  *To us:* reference point; their GreyMatter OS is one of the few
  named multi-robot orchestration platforms in market.

- **Ocado Technology** — grid-swarm fulfillment (the Hive). UK +
  Poland + Bulgaria. Hundreds of bots per site at sub-second
  scheduling. Reportedly heavy C++ + custom scheduling.
  *To us:* talent risk in UK / EU; reference point for tight-grid
  swarm coordination, which is closer to flight-control density
  than typical AMR.

- **Brain Corp** — multi-floor-scrubber fleet software (Walmart,
  Sam's Club, Schnucks). San Diego. Less manipulation, more
  scheduling + observability.
  *To us:* reference point; sometimes a *potential customer* for
  custom analytics or integration work.

---

## Drone-swarm players

Smaller fleets per deployment (single-digit to low-hundreds), but
the coordination problem (airspace, comms loss, charging-pad
contention) is harder per-robot than AMR. Defense names dominate
funding here.

- **Skydio** — autonomous drones for defense, inspection, public
  safety. Skydio Dock (2023+) is a fleet product: docked drones
  with autonomous launch / inspection / return. Redwood City CA.
  C++ + PyTorch + custom flight stack. Senior IC $250-400k.
  *To us:* *partner candidate* via Skydio's developer SDK and Dock
  integrations (real inspection-fleet customers want custom routing
  and analytics on top of Dock). Talent risk for senior autonomy
  ICs.

- **Verity** (Zurich, ETH-origin, scaled 2022+) — indoor inventory
  drones for warehouses. Multi-drone autonomous fleets that fly at
  night in retailer DCs. Customers include Maersk, Migros.
  *To us:* reference point for indoor multi-drone coordination;
  potential EU partner.

- **Saildrone** — autonomous sailing fleet for oceanography and
  maritime domain awareness. Alameda CA + Denmark. Fleets of dozens
  at sea simultaneously.
  *To us:* reference point for long-endurance fleet ops (months at
  sea) — different operating tempo than warehouse fleets.

- **Sentera** — drone-based agricultural fleet sensing. Minneapolis.
  Comp closer to $140-220k.
  *To us:* reference point for ag drone deployments; potential
  partner for ag clients.

- **DroneDeploy Fleet** — multi-drone management SaaS for
  construction, energy, ag. San Francisco. PyTorch + TypeScript +
  cloud-heavy.
  *To us:* *partner candidate* via the DroneDeploy partner network
  (also relevant for our CV / mapping work).

- **Iris Automation** — detect-and-avoid for BVLOS drone operations,
  which is a prerequisite for any real multi-drone outdoor fleet.
  Reno + San Francisco.
  *To us:* reference point; partner candidate if we move into
  regulated BVLOS work.

- **FlytBase / Pegasus** — drone fleet management SaaS layers.
  Smaller teams, mostly remote.
  *To us:* *partner candidates* if a customer needs an off-the-
  shelf fleet-management UI we can integrate against.

- **Gather AI** — multi-drone indoor warehouse inventory. Pittsburgh,
  CMU-spinout. Smaller team.
  *To us:* reference point; *potential customer* for niche overflow
  work given small team size.

- **Anduril Ghost program** — autonomous multi-rotor UAS (Ghost-4,
  Ghost-X) increasingly deployed as coordinated multi-aircraft
  packages within the Lattice OS. Costa Mesa CA. C++ + Rust +
  PyTorch. Senior IC $350-500k+.
  *To us:* talent risk; not a realistic customer (classified +
  in-house). Reference point for heterogeneous multi-platform
  coordination via Lattice.

- **Shield AI V-BAT swarm** — Hivemind-driven multi-V-BAT operations,
  publicly demonstrated 2023-2024 in DoD exercises. San Diego.
  C++ + PyTorch + custom middleware. Senior IC $300-450k.
  *To us:* talent risk; reference point for tactical drone-swarm
  autonomy. Median TC reportedly ~$228k across all levels per
  public salary reports.

- **Saronic** — multi-USV (unmanned surface vessel) maritime
  patrols. Austin TX. Series-B+ 2024 at $1B+.
  *To us:* reference point for maritime fleet coordination — a
  potential niche vertical for us if we ever get a port / harbor
  customer.

- **HavocAI, Vannevar Labs, Mach Industries** — younger dual-use
  names with multi-platform ambitions. Small teams, fast hiring.
  *To us:* reference points.

---

## Multi-arm and multi-robot coordination (non-mobile)

Fleets where the robots are stationary or local but coordinate as
a group — multi-arm cells, multi-humanoid pilots, hospital service
fleets.

- **Boston Dynamics (Hyundai)** — Spot fleets deployed at scale at
  Hyundai facilities and other industrial customers; some sites run
  dozens of Spots on patrol / inspection schedules. Boston. C++
  first, internal state-estimation and fleet-orchestration tooling.
  Senior IC $230-380k.
  *To us:* reference point; *potential customer* for niche Spot
  fleet-integration consulting (their direct services bandwidth is
  limited).

- **Figure** — multi-humanoid pilots at BMW Spartanburg (announced
  2024, scaling 2025) and reported logistics-customer pilots.
  Sunnyvale. PyTorch + C++ + NVIDIA Isaac. Senior IC reportedly
  $350-600k+ on equity-heavy packages.
  *To us:* talent risk; reference point for multi-humanoid
  deployment patterns (which are still early — hedge here, much
  of this is announced rather than steady-state).

- **Diligent Robotics (Moxi)** — multi-Moxi service-robot fleets in
  hospitals (Texas Health, Mayo Clinic). Austin TX. Tens of
  engineers. ROS 2-based.
  *To us:* reference point for healthcare service fleets;
  *potential customer* for custom hospital-IT integration work
  (every hospital's IT stack is different).

- **Cobot** (2022, ex-Amazon Robotics VP Brad Porter) — collaborative
  mobile manipulator. Boston, low-tens. Multi-robot ambitions are
  there but pilots are still small.
  *To us:* reference point.

- **Apptronik (Apollo)** — multi-humanoid pilots with Mercedes
  (2023+) and reported expansion 2024-2025. Austin TX. More eng-
  than-research, more shipping-focused.
  *To us:* *potential customer* for industrial integration work if
  multi-humanoid pilots scale to actual fleet deployments. Hedge:
  fleet sizes here are likely single-digit through 2026.

---

## AV traffic and fleet coordination

Autonomous-vehicle operators are running real production fleets,
which means fleet-routing, dispatch, charging, and tele-ops
coordination at scale. Different problem shape than warehouse AMR
(open-world, regulatory, public safety) but related at the
scheduling and dispatch layer.

- **Waymo** — production robotaxi fleet in Phoenix, SF, LA, Austin,
  expanding 2025. Fleet routing, ride-matching, depot operations,
  remote assistance dispatch. SF / Mountain View / Phoenix / PGH.
  C++ + Python on TPUs; internal scheduling stacks. Senior fleet-
  routing / dispatch IC $300-450k.
  *To us:* talent risk for senior fleet-ops ICs; reference point
  for AV fleet architecture. Not a realistic customer.

- **Zoox (Amazon)** — robotaxi, Foster City CA. Pre-commercial as of
  late 2025 but fleet-ops teams are staffing up for Vegas / SF
  rollout. C++ + PyTorch; Amazon L5/L6 bands.
  *To us:* reference point.

- **Cruise (GM)** — re-staffing through 2025 after the 2023
  suspension. Fleet operations restructured.
  *To us:* reference point; watch hiring signal late 2025 / 2026
  for market direction. Hedge — direction is still uncertain.

- **Aurora Innovation** — autonomous trucking fleet (Pittsburgh +
  Dallas + Bay Area). Hub-to-hub commercial launch underway 2024-
  2025 on Dallas-Houston. Fleet dispatch, yard ops, terminal
  integration are real ongoing work. Senior IC $250-400k.
  *To us:* reference point; potential customer for niche terminal-
  integration consulting (their direct partners are mostly large
  3PLs).

- **Nuro** — autonomous goods delivery; pivoted toward licensing
  their autonomy stack in 2024. Fleet logistics around small EVs.
  Mountain View. Senior IC $250-400k.
  *To us:* reference point.

- **Outrider** — autonomous yard trucks (yard-tractor fleet
  coordination at distribution yards). Brighton CO + Bay Area.
  Scaled 2022+.
  *To us:* reference point for yard-ops fleet coordination, which
  is closer to warehouse AMR in problem shape than to over-the-road
  trucking.

---

## Open-source multi-robot stacks

What our team builds on. Knowing these in depth is most of what
makes a fleet-management agency credible.

- **ROS 2 + Nav2 (with Multi-Robot Tutorials)** — the default
  starting point. Multi-robot namespacing, shared map servers,
  costmap layers. Maintained by Open Robotics / Intrinsic +
  community. C++ + Python. Apache 2.0.
  *To us:* foundational. Most of our deliverables sit on top of
  Nav2; multi-robot Nav2 tutorials are a credible interview-prep
  reference for new hires.

- **Eclipse Zenoh** (ZettaScale) — federated pub/sub middleware
  that is increasingly the right answer for multi-robot
  communication (especially across networks / sites / cloud). DDS
  has well-known issues at fleet scale; Zenoh handles
  discovery-over-WAN, bandwidth shaping, and lossy links more
  gracefully. Now an official ROS 2 RMW option (rmw_zenoh).
  *To us:* increasingly central. Any fleet engagement past 10
  robots or spanning sites is a Zenoh conversation. *Partner
  candidate*: ZettaScale runs a commercial-support program for
  Zenoh deployments — worth a conversation if we land enterprise
  fleet work.

- **OpenRMF (Open Robotics Robotic Middleware Framework)** — fleet
  manager for heterogeneous robot fleets (mixed vendors, mixed
  form factors). Originated at Open Robotics, sponsored by
  Intrinsic / Alphabet, used in Singapore healthcare and CSIRO
  pilots. Apache 2.0. C++ + Python.
  *To us:* this is the single most strategic open-source project
  for our shop. OpenRMF integration work is exactly the niche
  where warehouse integrators are weak (they prefer their own
  closed stacks) and where customers with mixed fleets have real
  pain. *Partner candidate* — OpenRMF has a community contributor
  path that doubles as credibility for sales.

- **Foxglove** — multi-robot visualization and fleet observability.
  TypeScript frontend, MCAP storage. Free tier + commercial.
  *To us:* default observability layer for our deliverables;
  *partner candidate* (they have an integrator-friendly
  ecosystem).

- **Formant, InOrbit, Freedom Robotics** — fleet observability +
  ops SaaS. Small but rapidly growing (all founded 2018-2022).
  *To us:* *partner candidates*; sometimes *competitors* when a
  customer would rather buy SaaS than custom dashboards.

---

## Competing fleet-management services shops

The integrators and consultancies we'll run into in fleet RFPs.
Honest framing: the established warehouse integrators are the
dominant competitor for any meaningful contract. We win on
multi-vendor / mixed-fleet work where their proprietary stacks are
the wrong answer, and on observability / ops work where their bias
is toward project-based delivery rather than recurring ops support.

- **Open Robotics Consulting / Intrinsic services** — the closest
  thing to a canonical OpenRMF integrator. Small team relative to
  warehouse integrators; high credibility.
  *Where we beat them:* responsiveness, vertical specialization,
  willingness to run ops as a retainer rather than a project. Often
  better positioned as a partner than a competitor.

- **Dematic (KION Group)** — global warehouse-automation integrator.
  Thousands of staff. Owns end-to-end design + integration + post-
  install support for large DCs.
  *Where we beat them:* nowhere on greenfield mega-projects. Where
  we play: brownfield retrofits, multi-vendor sites, customers
  unhappy with Dematic's response times on small change requests.

- **KION Group (parent of Dematic and STILL)** — even larger than
  Dematic alone. Materials handling + intralogistics globally.
  *Where we beat them:* same logic as Dematic.

- **Honeywell Intelligrated** — warehouse automation integrator.
  Mason OH + global. Similar shape to Dematic.
  *Where we beat them:* smaller multi-vendor sites; bespoke
  observability and shift-handoff tooling.

- **SSI Schäfer** — German intralogistics integrator. Strong in EU.
  *Where we beat them:* US-side work where SSI is less staffed;
  any retrofit / multi-vendor angle.

- **Vanderlande (Toyota Industries)** — airport baggage and
  warehouse automation. Strong in baggage handling, parcel, e-comm.
  *Where we beat them:* niche warehouse work; multi-vendor.

- **Swisslog (KUKA)** — warehouse + healthcare automation
  integrator. Similar shape to SSI / Dematic but smaller US
  footprint.
  *Where we beat them:* US healthcare-fleet work (Diligent /
  hospital integrations) where Swisslog is less embedded.

- **LogiNext, FleetX, Bringg** — fleet-software companies more in
  the last-mile delivery / logistics SaaS space than robotics
  per se, but they show up in fleet conversations adjacent to
  warehouse outbound.
  *Where we beat them:* anything involving actual robot
  coordination rather than vehicle dispatch.

- **Smaller regional fleet shops** — too many to name (Movement
  Robotics, ATS Automation, etc.). Most aren't directly
  competitive because their lead pipelines are local.

Be honest with prospects: if they have a greenfield 2000-bot site
to design, Dematic / Honeywell / KION will win. Our wedge is the
*mixed-vendor, retrofit, operations-heavy* customer that the big
integrators undervalue.

---

## Partnership and reseller programs worth joining

Concrete programs where applying as an agency unlocks credits,
sales co-marketing, or a customer pipeline.

- **NVIDIA Inception** — free DGX cloud credits, NVIDIA Connect
  intros to enterprise customers, GTC speaking opportunities. For
  fleet work specifically, Isaac Mission Dispatch (fleet
  orchestration on Isaac) and Isaac Perceptor (fleet-wide
  perception) are increasingly relevant. Open to AI / robotics
  shops under ~$50M revenue. Apply at nvidia.com/en-us/startups.
- **Open Robotics support / partner program** — paid support tier
  for ROS 2 / Nav2 / Gazebo / OpenRMF customers. Listing as a
  recognized integrator is realistic for a small shop that
  contributes upstream.
- **OpenRMF community contributor status** — informal but
  meaningful for sales. Contributing fixes / docs / adapters to
  OpenRMF gives us name recognition with the small set of
  customers actively evaluating mixed-fleet management.
- **AWS RoboMaker** — cloud-based fleet simulation and deployment
  tooling. AWS Activate gives $25k-$200k of cloud credits useful
  for fleet-sim work on customer engagements. Note: RoboMaker
  itself has had product-direction uncertainty — verify current
  status before committing customer work to it.
- **ROS Industrial Consortium** — membership-based industrial ROS
  ecosystem. Sponsored by SwRI in the US, Fraunhofer IPA in EU.
  Membership unlocks pre-publication access to industrial ROS
  packages and intros to industrial members (which are
  prospective customers).
- **AutoStore Authorized Partner / Integrator** — for the
  AutoStore cube-AMR ecosystem; relevant if we land any AutoStore-
  adjacent work. Real revenue share, real referral pipeline.
- **KION Group partner network** (Dematic / STILL) — large-
  integrator partner programs exist but are slow to join. Worth a
  conversation only if we have an entry point.
- **Dematic Partner Network** — same caveat.
- **Honeywell / Intelligrated partners** — same caveat.
- **Foxglove Integrator** — small but real; Foxglove routes
  enterprise inquiries to integrators.
- **Formant / InOrbit partner programs** — small partner ecosystems
  where being listed gives lead flow on fleet-observability work.
- **ZettaScale (Zenoh) commercial support partner** — informal but
  emerging; worth a conversation if we have Zenoh-heavy customer
  work.

Most of these are free to apply to. The realistic high-value ones
for a fleet-management services shop are: NVIDIA Inception, Open
Robotics / OpenRMF, ROS Industrial Consortium, and Foxglove /
Formant / InOrbit for observability work.

---

## Comp bands (for setting our own salaries)

Approximate TC bands for senior IC (3-7 years), 2025 Bay Area /
NYC / Boston. Sources: levels.fyi, 2025 Robotics Salary Guide,
Glassdoor self-reports, public funding announcements. Startup TC
is noisy because it includes illiquid common shares.

- **Amazon Robotics (fleet ICs):** $230-380k (L5-L6 bands)
- **Symbotic:** $200-330k
- **Warehouse AMR startups (Locus, GreyOrange, Hai, AutoStore US,
  Exotec US):** $230-350k
- **AV fleet routing / dispatch (Waymo, Zoox, Aurora):** $300-450k
- **Defense fleet / swarm (Anduril, Shield AI, Saronic):** $300-500k+
  (heavy equity)
- **Humanoid fleet pilots (Figure, Apptronik):** $300-600k+ (equity
  is the lottery ticket; hedge — most "fleets" here are sub-10
  robots through 2026)
- **Boston Dynamics, Diligent, Cobot:** $230-380k
- **Fleet observability SaaS (Formant, InOrbit, Foxglove,
  Freedom Robotics):** $200-330k with full-remote optionality
- **Warehouse integrators (Dematic, KION, Honeywell, SSI,
  Vanderlande):** $180-260k US, lower in EU; less equity, more
  base + benefits stability

Remote / EU usually 20-40% lower; London / Munich / Zurich close
the gap on the high end.

**For our hires:** band our base salaries at the fleet-observability-
SaaS range or above. Below that and our offers read as low against
the market our team is comparing against. Defense / humanoid
equity-heavy packages are not direct comp competitors for our
headcount; their candidates are taking lottery-ticket risk we
can't match.

---

## Hiring market signal

From the 2025 Robotics Salary Guide (907 jobs analyzed Nov-Dec
2025) and public job-listing scrapes:

- Robotics Software Engineer median: **$189k**.
- "Fleet Engineer" and "Multi-Robot Coordination Engineer" are
  newly named trending titles in 2025 hiring reports.
- Warehouse-automation hiring is steady (not explosive) — the
  install base is large and growing, but new-site cadence is
  governed by retailer capex cycles.
- Drone-fleet hiring picked up sharply after FAA Part 108 BVLOS
  rulemaking accelerated in 2024-2025 — hedge here, regulation
  is the actual gating factor.
- AV fleet-ops hiring is concentrated at Waymo and Aurora as both
  expand commercial footprints.

Translation: a steady, growing specialty with a clear customer
base. Less explosive than VLA or humanoids, much deeper recurring-
revenue potential. Good market for our shop's positioning.

---

## Remote / hybrid posture by employer type

Useful for understanding which talent pools are accessible to us
(remote-friendly = larger candidate pool for our remote hires).

- **Warehouse AMR operators (Amazon Robotics, Symbotic, Locus,
  GreyOrange):** mostly on-site or hybrid 3-4 days, because work
  often touches physical robots and customer sites.
- **AV fleet ops (Waymo, Zoox, Aurora, Cruise):** hybrid 3-5 days;
  routing / dispatch / ML can sometimes flex.
- **Defense swarm (Anduril, Shield AI, Saronic):** mostly on-site;
  some non-classified hybrid.
- **Humanoid fleet pilots (Figure, Apptronik, Diligent, Cobot,
  Boston Dynamics):** strictly on-site.
- **Drone fleet (Skydio, Verity, Iris, Gather):** hybrid on-site.
- **Fleet observability SaaS (Formant, InOrbit, Foxglove, Freedom
  Robotics, FlytBase):** fully remote, globally distributed. Our
  biggest direct competitors for distributed-team talent.
- **Warehouse integrators (Dematic, KION, Honeywell, SSI,
  Vanderlande):** on-site at customer DCs for delivery, hybrid
  for HQ engineering.

---

## Title decoder

The same role carries half a dozen different names across companies.
Use this when reading job ads (competitor signaling) or when
writing our own postings.

- **Fleet Engineer** — umbrella title (Locus, GreyOrange, Symbotic,
  Brain Corp, some Amazon Robotics teams). Owns the fleet manager
  end-to-end: dispatch, traffic, charging, observability.
- **Multi-Robot Coordination Engineer** — research-leaning variant
  (Intrinsic / Open Robotics, Anduril Lattice, Shield AI Hivemind).
  Algorithms-heavy: MAPF, auction-based task allocation, conflict
  resolution.
- **Warehouse Automation Engineer** — generalist warehouse-side
  title at integrators (Dematic, Honeywell, Vanderlande). More
  systems integration than pure fleet algorithms; WMS / WES interop,
  PLC interfaces.
- **Robotics Operations Engineer** — ops-side role (Locus, Brain
  Corp, Diligent, Verity). On-call for production fleets, customer-
  site bring-up, incident response. Closer to SRE than to
  researcher.
- **Solutions Architect (warehouse AMR vendors)** — pre-sales /
  customer-facing technical lead (Locus, Geek+, AutoStore partners,
  Exotec partners). Sites design, throughput modeling, customer
  expectation-setting.
- **Site Reliability Engineer (Robotics)** — newer title showing up
  at Locus, Symbotic, Amazon Robotics. Production-fleet uptime,
  alerting, runbooks. Closest analog to web SRE adapted for
  physical fleets.

---

## What this means for our positioning

Three short takeaways for the team:

1. **Fleet management is one of the highest-leverage services we
   sell.** Every customer with 5+ robots has ongoing operational
   pain — traffic deadlocks, mixed-vendor coordination, shift
   handoffs, observability gaps — that doesn't end with a deploy.
   That makes fleet ops a candidate for *recurring retainer*
   revenue, not just one-off integration projects. Lead with that
   framing in pitches.
2. **Warehouse integrators (Dematic, Honeywell, KION, SSI,
   Vanderlande) are the dominant competitor for any greenfield or
   large RFP.** Don't pretend otherwise. Our wedge is the *mixed-
   vendor, brownfield, ops-heavy* customer where the integrators'
   proprietary stacks are the wrong answer and their service
   bandwidth is too slow.
3. **OpenRMF + Zenoh + Foxglove + Nav2 is our most defensible
   technical bet.** It's the only mixed-fleet stack with real
   community momentum, and most large integrators won't go near
   it because it competes with their proprietary fleet managers.
   Contribute upstream where we can — it doubles as marketing.
4. **NVIDIA Inception, Open Robotics partner status, and
   OpenRMF contributor status are the three partnerships worth
   prioritizing early.** They each give credibility and lead flow
   disproportionate to the effort to join.
