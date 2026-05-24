# The Motion-Planning Market

> Market intel for our team. Motion planning is rarely sold as a
> standalone service — it almost always rides inside a manipulation,
> AV, or AMR engagement. The companies and groups below are the
> ecosystem we tap when a client needs motion-planning depth: a
> trajectory optimizer for a welding cell, a collision-aware MPC for
> a mobile manipulator, a behavior planner for an off-road vehicle.
> Some are potential customers, some are partners we can integrate
> with, some are competitors, some are talent sources, and some are
> reference points for stack and case studies. Comp bands are
> included so we set our own salaries fairly against the market.

## What this file is for

When we pitch a manipulation or navigation engagement that has a
meaningful planning component, we sometimes need to position against
the few names a sophisticated buyer will mention ("yes, like what
PickNik does on top of MoveIt, but for your specific welding cell").
When we hire a planning-literate engineer, we benchmark against
NVIDIA cuMotion / Waymo / TRI comp so our offers don't read as low.
When we read ICRA / IROS / RSS papers, a sizable fraction of the
planning track comes from teams listed here. This is our shared map
of a thinner-than-perception landscape.

See also: `01-examples.md` (deployed planners and papers),
`05-projects.md` (what we sell), `06-courses.md` (where our team
learns from), `00-basics.md` (concrete agency project patterns where
planning shows up).

## How to read each entry

For each group below: what they do, the planning stack they're
known to use, the TC band our team competes with, the location, and
**what they mean to us** — one of:

- *Potential customer* — their internal teams sometimes hire
  agencies for overflow or specialized work.
- *Partner candidate* — they run a formal partner / inception /
  agency program we could join.
- *Competitor* — they sell into the same RFPs we do.
- *Talent source / talent risk* — we hire from them; our team might
  leave to them.
- *Reference point* — published work, stack, or case studies we
  study but don't directly compete with.

---

## Reference research groups

Motion planning is unusually academic — much of the working stack
in industry traces back to a handful of labs. These are mostly
*reference points* and *talent sources*, not direct competitors.

- **Toyota Research Institute (TRI)** — Cambridge MA + Los Altos.
  Home of **Drake** (Russ Tedrake) and a steady output on
  trajectory optimization, contact-implicit MPC, and dexterous
  manipulation planning. Apache-2.0 open code. PyTorch + C++ +
  Drake. $230-330k.
  *To us:* reference point and **talent source** — Drake committers
  are gold; the publication culture means we can read their stack
  directly and adapt it for client work.

- **Stanford / IPRL (Interactive Perception and Robot Learning Lab,
  Jeannette Bohg) and ASL (Marco Pavone)** — manipulation and
  trajectory optimization, including the academic side of Pavone's
  group that overlaps with NVIDIA Research.
  *To us:* reference point for sampling-based and optimization-based
  planners; talent source for new grads.

- **CMU Robotics Institute** — historically the deepest planning
  bench (Maxim Likhachev's SBPL, Siddhartha Srinivasa's lab before
  he moved to UW, CHOMP origins). Pittsburgh.
  *To us:* reference point and talent source; many of the senior
  planners at Waymo / NVIDIA / Path Robotics are CMU alumni.

- **MIT CSAIL** — Tedrake's group historically lived here before
  TRI; LIS (Leslie Kaelbling, Tomas Lozano-Perez) on
  task-and-motion planning (TAMP). Cambridge MA.
  *To us:* reference point for TAMP, which is the realistic
  framing for most manipulation jobs we get asked about.

- **UC Berkeley (Pieter Abbeel's group, plus AUTOLAB on the
  grasping side)** — historically heavy on learning-based planning
  and policy, less on classical optimization. Berkeley CA.
  *To us:* reference point for learned planners; talent source for
  RL-flavored planning engineers.

- **University of Washington Personal Robotics Lab (Sidd Srinivasa,
  post-CMU move)** — manipulation planning, AIKIDO planning
  framework. Seattle.
  *To us:* reference point.

- **ETH Zurich (RSL — Marco Hutter; ASL — Roland Siegwart) and TU
  Munich** — European deep bench on legged-robot and AMR planning;
  many ANYbotics / Wayve hires originate here.
  *To us:* reference point; talent source if we ever hire EU-side.

---

## Big-company motion-planning teams

Bigger teams, more process, slower cadence. Mostly *reference
points* for stack and *talent risks* for senior planning ICs. None
of them realistically outsource core planning to an agency.

- **Waymo (Alphabet)** — trajectory optimization and behavior
  planning at scale; a sizable internal planner team distinct from
  perception. C++ + custom optimization stack. Median TC ~$232k;
  senior planning IC $300-450k. SF / Mountain View / Pittsburgh.
  *To us:* reference point; talent risk for senior planning ICs.

- **Cruise (GM)** — re-staffing through 2025. Behavior planner +
  trajectory optimizer team was historically strong.
  *To us:* reference point; watch hiring signal for market
  direction on AV planning roles.

- **Zoox (Amazon)** — full AV stack including a substantial
  planning team. Foster City CA. Amazon L5/L6 bands.
  *To us:* reference point.

- **NVIDIA (cuMotion, Isaac Manipulator, Isaac Sim, DRIVE
  planning)** — **cuMotion** is GPU-accelerated trajectory
  optimization shipped in Isaac; the team is small but well-known.
  Stack: C++ + CUDA + PyTorch. Median TC ~$270k; senior staff
  $400k+.
  *To us:* **partner candidate** via NVIDIA Inception (cuMotion
  access, DGX cloud credits, GTC speaking); reference point for
  GPU-accelerated planning; occasional customer for Isaac Manipulator
  integration on client robots.

- **Boston Dynamics (Hyundai)** — planning is tightly coupled to
  controls on Spot and Atlas. Mostly internal frameworks. Boston.
  Senior IC $230-380k.
  *To us:* reference point for legged-robot motion planning;
  brand credibility on resumes.

- **Apple (ARKit pathing, Vision Pro spatial)** — pathing for AR
  experiences is a niche planning surface. Stack: Metal +
  proprietary. Senior IC $300-500k.
  *To us:* reference point only; not a planning services market.

- **Amazon Robotics (fleet routing, Symbotic-adjacent)** — fleet-
  level path planning and multi-agent coordination at warehouse
  scale. Java + C++. Some published work on conflict-based search
  for warehouse AMRs.
  *To us:* **potential customer** for niche warehouse planning
  consulting (rare but not zero); reference point for multi-agent
  planning at scale.

---

## Specialist motion-planning startups and commercial players

This list is genuinely short. We hedge — motion planning as a
standalone product is a thinner market than perception or
simulation, and most "planning startups" sell something larger
(a full manipulation cell, an off-road platform) with planning
underneath.

- **Realtime Robotics** — Boston. **RapidPlan** is hardware-
  accelerated motion planning on a custom processor; sells into
  industrial cells as both an SDK and an integration. The clearest
  example of motion-planning-as-a-product in the market. Senior IC
  $230-380k (estimate; non-public).
  *To us:* **partner candidate** if a planning-SDK partnership
  exists (worth checking — we have not confirmed); reference point;
  potential competitor if a client is comparing "buy RapidPlan
  versus have us build a custom planner."

- **Path Robotics** — Columbus OH. Autonomous robotic welding;
  planning is core (weld-path generation from CAD, collision
  avoidance, process constraints). Mid-sized team.
  *To us:* reference point for welding-path planning; potential
  customer is unlikely (they have a strong in-house planner team).

- **Bedrock Robotics** — SF. Autonomous earth-moving; off-road
  planning under uncertain terrain. Series-A scale.
  *To us:* reference point for off-road / construction planning,
  which has different cost functions than on-road AV.

- **Cobot** (2022, ex-Amazon Robotics VP Brad Porter) — Boston.
  Collaborative mobile manipulator; planning sits at the
  manipulation-navigation interface.
  *To us:* reference point.

- **NVIDIA cuMotion** — listed here as well as above because the
  GPU-planning team operates more like a product unit than a
  research org. Treat as both.
  *To us:* partner candidate, reference point.

- **Field AI** (2023) — Mission Viejo / Pasadena. Off-road
  foundation policy that *subsumes* classical planning into a
  learned end-to-end model. Worth flagging because if their thesis
  holds, the boundary between "planner" and "policy" disappears in
  outdoor domains.
  *To us:* reference point; a directional bet to watch — if learned
  policies eat classical planners in off-road, our positioning has
  to shift toward the cost-function and constraint-design layer.

We deliberately keep this list short. We have not validated a
broader set of "motion-planning startups," and we'd rather hedge
than pad with names we can't back up.

---

## Open-source planning frameworks (knowing these IS market knowledge)

Unlike perception, where most of the value lives in trained
weights, planning value lives in *frameworks* — and almost all the
serious frameworks are open source. Fluency in these is itself a
sellable skill.

- **Drake** (TRI, Apache 2.0) — C++ first, Python bindings.
  Multibody dynamics + trajectory optimization + MPC + system-level
  modeling. The serious choice for contact-rich manipulation
  planning.
  *To us:* the deepest open-source planning stack; engineers with
  Drake commits are rare and command premium comp.

- **OMPL** (Open Motion Planning Library, Rice University,
  BSD) — the standard library of sampling-based planners (RRT,
  RRT-Connect, PRM, BIT*, etc.). Integrated into MoveIt by default.
  *To us:* baseline literacy; any planning hire should know OMPL.

- **MoveIt 2** (PickNik + Open Robotics, BSD) — the de-facto ROS 2
  manipulation planner. Wraps OMPL, integrates with planning-scene
  collision checking, MoveIt Servo for real-time control.
  *To us:* the most common planning stack we'll see on client
  arms; MoveIt fluency is table stakes for manipulation work.

- **Nav2** (Open Robotics, Apache 2.0) — the de-facto ROS 2 mobile
  navigation planner. Plugin-based global + local planner
  architecture; behavior trees on top.
  *To us:* table stakes for any AMR engagement.

- **CHOMP / TrajOpt / STOMP** — academic trajectory-optimization
  algorithms; reference implementations exist in MoveIt and in
  research codebases. Not actively maintained as products.
  *To us:* useful conceptual vocabulary; we'll occasionally
  reimplement TrajOpt-style costs for a specific client.

- **Pinocchio** (INRIA, BSD) — rigid-body dynamics + analytical IK
  + derivatives. Used as the dynamics backend for many MPC
  implementations.
  *To us:* essential under-the-hood library for any optimization-
  based planner we build.

- **ACADO / CasADi** — symbolic optimization frameworks for MPC.
  CasADi is more actively maintained.
  *To us:* the realistic toolchain when a client wants a custom
  MPC rather than a packaged planner.

- **cuRobo / cuMotion** (NVIDIA, source-available) — GPU-
  accelerated motion generation. Increasingly the "fast path" for
  manipulator planning.
  *To us:* worth fluency; aligns with NVIDIA Inception partnership.

---

## Competing services shops for planning-heavy work

Honest read: this list is thin. Motion planning rarely supports a
pure-play services shop on its own.

- **PickNik Robotics** — Boulder CO. **The** motion-planning
  services name in the ROS world: MoveIt maintainers plus paid
  engineering services on top. The clearest direct competitor for
  any manipulation-planning engagement that lives in ROS 2. ~50
  people. $150-250k IC band (estimate).
  *Where we beat them:* we don't, usually — they're stronger on
  pure MoveIt depth. We'd win on vertical specialization or on
  engagements that span perception + planning + sim where their
  pure-planning focus is a constraint.

- **Open Robotics services arm (Intrinsic, now Alphabet)** —
  historically the OSRF / Open Robotics consulting line was the
  fallback for ROS-deep work; ownership has changed and it's less
  clear how active the services side is today. Hedging.
  *Where we beat them:* responsiveness for small / mid engagements.

- **Realtime Robotics services** — they do paid integration of
  RapidPlan into client cells. More a product-led services motion
  than a generalist consultancy.
  *Where we beat them:* engagements that need a custom planner
  rather than the RapidPlan product.

- **Tangram Vision** — Denver. Primarily a perception / sensor-
  calibration shop, but adjacent enough to come up in robotics
  RFPs. Not a direct planning competitor.
  *Where we beat them:* anywhere planning is the core requirement.

- **The larger ML / robotics consultancies (MobiDev, N-iX, InData
  Labs, etc.)** rarely show up in serious planning RFPs because
  the work demands ROS / Drake / MPC fluency they don't staff
  deeply.

We have not identified a broader set of planning-only services
shops with confidence. The realistic competitive set for a
planning-heavy engagement is PickNik first, then in-house.

---

## Partnership programs worth joining

Concrete programs where applying as an agency unlocks credits,
sales co-marketing, or a customer pipeline relevant to planning
work.

- **NVIDIA Inception** — free DGX cloud credits, cuMotion / Isaac
  Manipulator access, NVIDIA Connect intros, GTC speaking. Open to
  AI / robotics shops under ~$50M revenue. Apply at
  nvidia.com/en-us/startups. **High value** for planning work
  because cuMotion access matters.
- **Open Robotics / Open Source Robotics Alliance partner or
  support tier** — formal affiliation with the ROS 2 ecosystem;
  may include co-marketing on case studies. Worth checking current
  program structure.
- **ROS Industrial Consortium** — paid membership; member
  directory, working groups, customer intros for industrial-ROS
  work. Realistic value for manipulator integration engagements.
- **PickNik partner ecosystem** — if PickNik runs a formal partner
  program for MoveIt integrators, it would be a natural fit. We
  have not confirmed this exists; worth checking.
- **Realtime Robotics SDK partner** — if such a program exists
  (unconfirmed), it would unlock RapidPlan resale or integration.
- **University research collaborations (Berkeley, CMU, MIT, UW,
  ETH)** — joint papers and intern pipelines. Less a "program" and
  more a relationship play, but the talent pipeline value is real.
  A single co-authored ICRA paper with a known lab is worth more
  than most paid memberships for credibility on planning RFPs.

The realistic high-value programs for a planning-adjacent shop
are: NVIDIA Inception, ROS Industrial Consortium, and at least one
university research relationship.

---

## Comp bands (for setting our own salaries)

Approximate TC bands for senior IC (3-7 years), 2025 Bay Area / NYC.
Sources: levels.fyi, 2025 Robotics Salary Guide, Glassdoor self-
reports. Planning-specific data is thinner than perception, so
these are partly inferred from adjacent roles.

- **NVIDIA (cuMotion / Isaac):** $270k median, senior staff $400k+
- **Waymo motion-planning ICs:** $300-450k (Waymo median $232k
  across levels)
- **Zoox, Cruise:** comparable to Waymo bands
- **Toyota Research Institute:** $230-330k
- **Specialist startups (Realtime Robotics, Path Robotics,
  Bedrock, Cobot):** $230-380k
- **Boston Dynamics:** $230-380k
- **PickNik:** $150-250k (services-shop band, closer to ours)
- **EU labs (ETH spinouts, ANYbotics):** EUR 120-200k, lower than
  US

Remote / EU usually 20-40% lower. Equity-heavy frontier startups
(Field AI, etc.) pay base lower than the headline; the equity is
the lottery ticket.

**For our hires:** band our planning-engineer base salaries at or
above the PickNik range. Below that and our offers will lose to the
realistic alternative our candidates are weighing. We are unlikely
to win against Waymo / NVIDIA on raw cash; we win on project
variety and ownership.

---

## Hiring market signal

Motion planning is a *smaller niche* than perception or RL inside
the broader robotics labor market. "Motion Planning Engineer" is a
named title at Waymo, Zoox, Cruise, NVIDIA, and a handful of
specialists — and almost nowhere else under that exact name.

From the 2025 Robotics Salary Guide:

- Robotics Software Engineer median: **$189k**.
- "Motion Planning Engineer" does not appear as a top trending
  title in 2025 hiring reports the way "Computer Vision Engineer"
  does — it is real but narrower.
- Most planning work hires under broader titles (Robotics Software
  Engineer, Autonomy Engineer, Manipulation Engineer).

Translation: a smaller, deeper talent pool than perception. Good
news for retention once we have a strong planning IC; bad news for
fast hiring at scale. We should expect 3-6 month hiring cycles for
a senior planning hire, not 6 weeks.

---

## Remote / hybrid posture by employer type

- **AV labs (Waymo, Cruise, Zoox):** hybrid 3-5 days on-site.
- **NVIDIA cuMotion / Isaac:** hybrid; some remote for senior ICs.
- **TRI, MIT / Stanford / CMU labs:** on-site (lab is a physical
  thing).
- **Boston Dynamics, Apptronik, Figure (where planning lives in
  the controls stack):** strictly on-site.
- **Specialist planning startups (Realtime Robotics, Path
  Robotics, Bedrock):** on-site in non-major-tech cities.
- **PickNik:** historically remote-friendly; one of the more
  distributed planning-services shops.
- **Open Robotics:** distributed by default.

The remote-friendly slice of the planning market is small. PickNik
and the open-source frameworks ecosystem (Open Robotics, the
academic-adjacent contributor pool) are where we can realistically
hire planners remotely.

---

## Title decoder

The same role carries several names. Use this when reading job ads
or writing our own postings.

- **Motion Planning Engineer** — the on-the-tin title (Waymo,
  Zoox, NVIDIA, Realtime Robotics). Often AV or manipulator
  specific.
- **Trajectory Optimization Engineer** — narrower, more
  optimization-flavored (Waymo, TRI, NVIDIA). MPC, direct
  collocation, contact-implicit methods.
- **Path Planning Engineer** — frequently AMR / mobile-robot
  flavor; less common in manipulation. Nav2-adjacent stacks.
- **Behavior Planning Engineer** — AV-specific (Waymo, Cruise,
  Zoox). Higher level than trajectory: lane changes, yielding,
  multi-agent reasoning.
- **Manipulation Planning Engineer** — manipulator-specific; often
  spans MoveIt / Drake / cuMotion fluency (PickNik, Path Robotics,
  NVIDIA Isaac Manipulator).
- **Robotics Software Engineer (Planning)** — generalist umbrella
  with planning slant (Boston Dynamics, Apptronik, smaller
  startups). Expect ROS / C++ depth alongside planning.
- **Autonomy Engineer (Planning)** — defense / drone variant where
  planning is one slice of an autonomy stack.

---

## What this means for our positioning

Three takeaways for the team:

1. **We rarely sell motion planning standalone.** Frame planning
   as part of a larger manipulation, AMR, or AV engagement. A
   client buying "motion planning" usually means "make my robot
   do the task" — they want the planner *and* the perception
   wiring, the cost-function tuning, the integration test rig.
2. **The moat is in domain-specific cost functions and
   constraints, not the solver.** Drake, OMPL, MoveIt 2, Nav2,
   cuMotion are all free or near-free and well documented. The
   defensible work is the welding-process constraints, the
   warehouse-aisle cost shaping, the loading-dock approach
   geometry — the parts that need a human who has watched the
   robot fail twenty times in this specific cell.
3. **Direct competition is thin but real where it exists.**
   PickNik is the one name to take seriously on manipulation-
   planning engagements that live in ROS 2. Outside ROS, the
   competitive set is mostly in-house teams or the cuMotion /
   Realtime Robotics product motion. Position accordingly: be
   explicit about the vertical and the integration scope, not
   the planner name.
4. **Watch the learned-policy boundary.** Field AI, Skild,
   Physical Intelligence, and similar are pushing toward learned
   end-to-end policies that swallow what was previously a
   planner. In off-road and dexterous-manipulation domains this
   could compress the addressable market for classical planning
   services over the next 2-3 years. We should keep at least one
   engagement per year on the learned-policy side to stay current.
