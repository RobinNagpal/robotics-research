# Major and New Employers

Who pays perception engineers, and what to know about each. Salary
numbers are from levels.fyi, the 2025 Robotics Salary Guide, public
funding rounds, and self-reported Glassdoor data. Treat them as
bands, not guarantees.

If you are coming from web (Node / React / TypeScript) and just
finished a six-month perception ramp, the analogy that will save you
the most heartache is this one: the robotics labor market right now
is structurally similar to the JavaScript ecosystem in 2014-2015.
There is a small set of FAANG-tier blue-chip employers, a layer of
extremely hot Series-B/C scaleups that look a bit like 2014-era
Stripe / Airbnb / Uber, a long tail of vertical SaaS plays that look
like the early Vercel / Netlify era, and a defense slice that has no
real web analog except maybe Palantir. The strategy below maps each
to a concrete application path.

See also: `00-basics.md` for the vocabulary you'll need to pass a
recruiter screen; `01-examples.md` for the kinds of demos that get
you in the door; `02-learn.md` for the curriculum; `03-start.md` for
the first 30/60/90 plan; `05-projects.md` for portfolio ideas; and
`06-courses.md` for paid / structured options.

## Big tech and established AV / AR labs

Bigger teams, more process, slightly less upside, very strong
mentorship. Think of this tier as the AWS / Google Cloud / Azure of
robotics employers: stable, well-paid, well-respected on your CV,
but also slow-moving and political. If you came from a series-B web
startup where you pushed to prod ten times a day, the cadence at
Waymo or Apple will feel glacial.

- **Waymo (Alphabet)** — AV perception. The technical bar is high
  and the data is unmatched: the perception team owns the camera
  + lidar + radar fusion stack end-to-end, scene segmentation,
  tracking, prediction-adjacent perception, and the offline auto-
  labeling pipeline that feeds training. Team size is reportedly in
  the low-hundreds across perception alone. Stack is heavy C++ with
  PyTorch for model dev, TensorFlow for some legacy training, and
  a custom internal framework on TPUs. Interviews reportedly run
  five rounds: two coding (LeetCode medium with a vision twist, e.g.
  IoU between two boxes), one ML/CV depth (anchor-free detection,
  NMS variants), one system design (design an offline auto-labeling
  pipeline), one behavioral. Reported median TC **~$232k**, senior
  IC $300k-$450k+. SF / Mountain View / Pittsburgh / Phoenix.
  Realistic target for a junior web dev with 6 months of ramp: L3
  "Software Engineer II" with a perception focus, via the referral
  path. Cold-applying as a career-switcher is very hard here.
- **NVIDIA** — Isaac, GR00T, Cosmos, FoundationPose, foundation
  perception. Think of NVIDIA's perception teams as Vercel's
  platform team — adjacent to the hot framework, and the equity
  tailwind compensation has been silly for years. Multiple smaller
  teams (Isaac SDK, Isaac Sim, GR00T humanoid, DRIVE for AV,
  Research) rather than one big org; each is reportedly 20-80
  engineers. Stack is C++ + PyTorch + CUDA, plus their own TensorRT
  inference runtime. Interview is reportedly more academic than
  Google's: expect a CUDA / parallelism question, a CV depth round,
  and behavioral. Median TC **~$270k**, senior staff $400k+. The
  NVIDIA equity tailwind has been enormous; a senior IC who joined
  in 2020 has reportedly seen total comp double or triple via stock
  appreciation alone. Realistic target for the career-switcher: a
  "Solutions Engineer, Robotics" or "Developer Relations, Isaac"
  role rather than core perception research; these convert into
  perception SWE within 18-24 months and are far more open to
  non-traditional backgrounds.
- **Tesla Autopilot / Optimus** — camera-only perception + humanoid
  perception. Famously secretive and high-pressure; the working
  culture has been compared to early Uber engineering or to a Series
  B startup at FAANG scale. Stack is heavy PyTorch + custom C++
  inference, with Dojo training infrastructure. Interview reportedly
  emphasizes raw coding speed (two LeetCode-style problems back to
  back) plus a deep CV round. Comp competitive but heavy on equity;
  base often lower than Waymo. Realistic for a junior switcher: tough
  unless you can demo a strong from-scratch perception project on
  a Tesla-relevant problem (e.g. monocular depth, BEV segmentation).
- **Mobileye** — vision-centric ADAS. Jerusalem + US offices.
  Perception team is large and mature; they own one of the longest-
  running production camera stacks in the industry. Stack is heavy
  C++ on custom EyeQ silicon, with PyTorch for training. Interview
  reportedly leans classical CV (epipolar geometry, calibration,
  feature matching) more than deep learning. Lower comp than US
  giants but stable; senior IC $230-380k in the US, much less in
  Israel. Career-switcher angle: their US offices in Detroit and
  San Jose are reportedly more open to non-traditional CVs than HQ.
- **Apple** — Vision Pro, ARKit, hiring rumored to be quiet but
  steady. The perception org spans Vision Pro tracking, ARKit / VPS,
  camera ISP perception (Portrait mode, Cinematic), and AV (Project
  Titan's residue is reportedly absorbed into Vision Products Group).
  Stack publicly known to include Metal + CoreML + a lot of custom
  C++. Interview is reportedly the most opaque of the FAANGs: five
  to seven rounds, very team-dependent, no canonical pattern.
  Top-of-market comp; senior IC TC $300-500k. Realistic target for
  a junior switcher: very hard cold, but Apple does hire from ARKit-
  adjacent communities, so a published ARKit / RealityKit demo helps.
- **Meta Reality Labs** — Aria glasses, SAM, DINOv2 teams. Strong
  research culture; FAIR Perception is the most-published industry
  team after Google. Two distinct sub-orgs: FAIR (research, mostly
  PhDs, publishes openly) and Reality Labs Product (ships glasses /
  Quest, more eng-heavy). PyTorch obviously dominates here — it's
  literally their framework. Interview at RL Product reportedly
  more standard FAANG with a CV twist; FAIR interview is more like
  a faculty job talk. Realistic switcher target: RL Product "ML
  Engineer, Perception" — not FAIR.
- **Boston Dynamics (Hyundai)** — Spot, Atlas perception. Boston.
  Robotics-prime brand. Perception team is smaller than the AV labs
  (reportedly tens, not hundreds), tightly coupled to controls.
  Stack is C++ first, Python second, with internal frameworks for
  state estimation. Interviews reportedly heavy on classical
  estimation: Kalman filters, factor graphs, ICP. Comp is solid but
  not top-of-market ($230-380k senior). The brand on your CV is
  worth a real premium when you next interview elsewhere — similar
  to having Stripe or Airbnb on a web-dev resume.
- **Zoox (Amazon)** — full AV stack. Foster City CA. Healthy
  pipeline, slow rollout. Perception team is large; they own the
  multi-sensor stack on their bidirectional vehicle. Acquisition by
  Amazon has reportedly made comp more competitive (matches Amazon
  L5/L6 bands) but slowed shipping. Stack is C++ + PyTorch.
- **Cruise (GM)** — worth a mention even after the 2023 setback;
  they reportedly retained a perception bench and have been
  re-staffing through 2025. Comp competitive, morale historically
  bruised; watch for signal in late 2025 / 2026.
- **Toyota Research Institute (TRI)** — research-grade work,
  Cambridge MA + Los Altos. Smaller team, more open publication
  culture, PyTorch + JAX. Comp on the lower end of this tier ($230-
  330k) but the research environment is excellent.
- **Symbotic, Amazon Robotics** — warehouse perception at scale.
  Less glamorous than AV but the deployment volume is enormous;
  Amazon Robotics ships more perception code to physical systems
  per day than almost anyone. Stack heavy on Java + C++, with
  ROS-adjacent internal frameworks. Realistic switcher target:
  excellent. They hire generalists and train them.
- **Skydio** — straddles this tier and defense; see below.

## Defense / dual-use companies (massive growth 2022-2025)

This sub-segment has exploded post-2022 with US/EU defense budgets.
Comp here often beats commercial robotics. The web-dev analogy:
Anduril for defense perception is roughly Palantir for data
analytics — high-paying, mission-driven, and you'll need to make
peace with the use cases before you take the offer. Citizenship and
clearance requirements are real; most US defense roles require US
citizenship (not green-card), and a non-trivial subset require
SECRET or above clearance, which the employer sponsors but which
takes 6-12 months to land.

- **Anduril** (perception ramped 2021+) — autonomy stack for
  defense; large CV team for ISR (intelligence, surveillance,
  recon) and counter-UAS. Perception team is reportedly one of the
  largest in defense, in the low-hundreds across Lattice, Ghost,
  Roadrunner, and the maritime products. Stack is publicly known to
  be C++ + Rust + PyTorch, with a heavy in-house data and labeling
  platform. Interview reportedly emphasizes systems thinking over
  pure algorithms: expect a "design the perception stack for a
  counter-drone turret given these constraints" round. Senior IC
  $350-500k+; equity is real but illiquid. US citizenship required
  for almost all roles. Realistic switcher target: their "Mission
  Software Engineer" role is closer to product eng and is the most
  open door for a web background.
- **Shield AI** (Hivemind, scaled 2022+) — autonomous flight,
  V-BAT drone + Hivemind autonomy stack. Smaller than Anduril;
  perception team is reportedly tens of engineers. Stack: C++ +
  PyTorch + ROS-adjacent custom middleware. Interview reportedly
  more classical (state estimation, SLAM, controls-adjacent) than
  Anduril's. Median **~$228k**, senior IC $300-450k. San Diego is
  the center of gravity; some roles in DC.
- **Saronic** (2022) — autonomous surface vessels. Series-B+ 2024,
  reportedly raised at a $1B+ valuation in early 2025. Very small
  perception team (single-digit to low-tens), Austin TX. Maritime
  perception is its own subspecialty — radar, AIS fusion, horizon
  detection, wave-aware tracking — and there's almost no one with
  five years of experience in it, so a motivated switcher can ramp
  faster than at an AV company. Realistic target: excellent for the
  right candidate, but you must be willing to relocate to Austin.
- **Helsing** (Germany, 2021) — defense AI; large UK/EU presence
  (Munich + London + Paris). The European Anduril analog. They
  reportedly hire more openly in the EU and have a more research-y
  culture. Comp lower than US peers in absolute terms but very
  competitive for Europe (senior IC EUR 150-250k + equity).
- **Skydio** — consumer / defense / public-safety drones. Founded
  2014, scaled past 2022 after pivoting away from consumer. Strong
  visual-inertial SLAM team in Redwood City CA. Stack: heavy C++
  + PyTorch, with one of the most polished on-device perception
  stacks in the industry. Interviews reportedly classical CV / SLAM
  heavy. Senior IC $250-400k.
- **Saildrone, Vannevar Labs, HavocAI, Mach Industries** — younger
  dual-use names worth tracking. Mach (2023) reportedly raised a
  large Series B in 2025; they hire perception for autonomous
  missiles / drones. Small teams, fast hiring, citizenship required.
- **Palmer Luckey-adjacent and ex-SpaceX founder networks** — many
  2024-2025 defense startups recruit heavily from this network on
  LinkedIn and X. If you can credibly demo one perception project
  applied to a defense-relevant problem (e.g. small-object detection
  on drone video), you will get DMs.

## Perception-heavy startups founded or scaled 2020-2025

This is where the explosive growth (and compensation) is. Most of
these did not exist 4 years ago. The mental model: Figure or
Apptronik are roughly pre-IPO Stripe in 2014 — high-variance,
high-equity, big-name customers nominally lining up, prove-it-or-
die culture. Physical Intelligence and Skild are closer to OpenAI
circa 2021 — research-prestige hires, capped-profit-style equity
narratives, very high bar. Roboflow / Polycam / Veo are Vercel /
Cloudflare equivalents — DX-first, fast hiring, smaller team,
perception-as-developer-product.

- **Wayve** (UK, founded 2017, Series-C 2024 at **$1B+**) —
  end-to-end driving foundation models. Large CV team in London +
  Mountain View, reportedly 100+ across perception and learning.
  Stack is heavily PyTorch + JAX with a large internal training
  platform. Interview reportedly research-y: a paper-discussion
  round in addition to coding and ML depth. London team is more
  open to non-PhD hires than the SF research outpost. Realistic
  switcher target: their "Engineer, Data & Perception" type roles
  are eng-heavy and a credible door for a strong web background.
- **Physical Intelligence (Pi)** (founded 2024) — VLA models with
  heavy perception inputs. $400M Nov 2024 at $2.4B valuation.
  Reportedly tiny team (under 100 total in 2025), enormous talent
  density (ex-Google Brain, ex-DeepMind, ex-Tesla). PyTorch + JAX.
  Interview is reportedly the most research-heavy on this list,
  with multi-round paper discussions. Realistic switcher target:
  honest answer is "low unless you have a publication or a very
  strong VLA demo," but the ML engineering / infra roles are more
  open than the research roles.
- **Skild AI** (2023, ex-CMU) — robot-agnostic generalist policy.
  Perception-heavy backbone. $300M Series A July 2024 at ~$1.5B.
  Reportedly similar profile to Pi: small, research-dense, PyTorch.
  Pittsburgh + Bay Area. Realistic switcher target: difficult
  through the front door; easier via the CMU robotics network.
- **Figure AI** (2022) — humanoid with strong vision stack (Helix
  VLA). Cumulative >$1.5B raised; Feb 2025 valuation talks at
  $39.5B. Perception team reportedly grew from single-digits in
  2023 to 30-50+ by mid-2025. Stack: PyTorch + heavy C++, NVIDIA
  Isaac in the loop. Famously demanding, on-site five days at
  Sunnyvale. Interview reportedly leans toward a "ship something
  in 48 hours" take-home plus standard coding. Realistic switcher
  target: their "Robotics Software Engineer" funnel is more open to
  non-traditional CVs than the ML side, and they hire aggressively
  in 2025.
- **1X Technologies** (rebranded from Halodi 2022) — NEO consumer
  humanoid + world-model perception. Norway + SF. Stack PyTorch +
  C++; team smaller than Figure. They've reportedly been open to
  hiring strong generalists and training them in robotics.
- **Apptronik** (Apollo humanoid, commercial push 2023+) — Mercedes
  pilots; one of the more credible commercial humanoids. Austin TX.
  Reportedly more eng-than-research culture than Figure, lower
  comp variance but more shipping-focused. Realistic switcher
  target: very good — they hire generalists.
- **Cobot** (2022, founded by Brad Porter, ex-Amazon Robotics VP) —
  collaborative mobile manipulator; perception-heavy stack. Boston.
  Small team (low-tens), reportedly very strong on the
  manipulation-perception interface.
- **Bedrock Robotics** (2023) — autonomous earth-moving equipment.
  Construction / dirt is a perception-rich, GPS-friendly domain;
  the data is messy in interesting ways. Reportedly small team,
  San Francisco.
- **Pickle Robot** (2018, scaled 2023+) — truck-unloading
  perception. Strong customer pipeline with shippers. Cambridge MA.
  Perception is the core technical bet (boxes in a truck are a
  surprisingly hard perception problem because of occlusion and
  variable shapes). Realistic switcher target: very good. Email the
  CTO directly.
- **Field AI** (2023) — outdoor / off-road foundation policies for
  inspection, construction. Mission Viejo / Pasadena. Reportedly
  small but well-funded; off-road perception (no lane lines, no
  HD map) is a distinct skillset.
- **Chef Robotics** (2019, scaled past 2023) — food assembly
  perception. Commercial deployments in food factories. SF. The
  food perception problem (deformable, occluded, glossy, wet) is
  weirdly close to medical / pathology imaging in difficulty.
- **Rivr** (2023, Switzerland, ex-ETH) — last-mile delivery robots.
  European Swiss-quality engineering culture; comp lower than US
  but cost of living also lower in some Swiss cities (not Zurich).
- **Polycam, Luma AI, Spline, Scaniverse (Niantic)** — consumer
  3D-from-photos. Smaller perception teams but pure software, fast
  hiring. This sub-tier is the closest thing in robotics to the
  Vercel / Linear / Raycast cluster — DX-obsessed, designer-heavy,
  remote-friendly. Luma and Polycam have reportedly hired from
  non-traditional backgrounds. Stack: PyTorch + heavy iOS / web
  frontend, which is gold for a former web dev.
- **Niantic** — recently spun out their geospatial / VPS (visual
  positioning system) team; they have one of the world's largest
  AR map datasets. The spinout is reportedly hiring perception
  engineers as of 2025.
- **Veo Robotics, Roboflow, Voxel51, Encord, Scale AI** —
  perception infrastructure plays. Roboflow in particular is the
  most web-dev-friendly perception company on the list: TypeScript
  frontend, Python backend, perception as a developer product, fast
  hiring, fully remote. Realistic switcher target: excellent —
  your existing web skills are a feature, not a bug.
- **Standard Bots, Dexterity, Covariant (now mostly absorbed into
  Amazon)** — warehouse / industrial manipulation perception.
  Smaller teams, more shipping pressure.
- **Path Robotics, Bright Machines, Machina Labs** — industrial
  perception for welding, electronics assembly, sheet-metal
  forming. Less hyped, very real customers, comp solid.

## How they hire (so you can target effectively)

Most teams above hire perception engineers in three buckets. **The
realistic target for a junior web dev with ~6 months of ramp is
"perception software engineer" — bucket 2.**

- **Research scientist / research perception** — PhD or equivalent,
  publishes at CVPR/ICCV/ECCV. Hardest to break in cold. Web-dev
  analog: this is the "ML research engineer at OpenAI" tier — the
  job listings exist, but realistically you need a PhD or 2+ first-
  author top-venue papers.
- **Perception software engineer** — strong eng + working ML chops.
  You'll integrate models, write inference services, optimize C++
  hot paths, and own the camera pipeline end-to-end. This is the
  bread-and-butter perception role. Web-dev analog: full-stack
  engineer at a Series B — generalist, pragmatic, ships.
- **Sensor / calibration engineer** — overlaps with EE; lots of
  hands-on calibration, time-sync, multi-sensor fusion. C++ heavy.
  Underrated path for a switcher: less competition, very real
  shortage, and once you've calibrated a multi-camera-lidar rig in
  anger you have a moat.

## How to actually apply to each tier

Different employer tiers respond to different application channels.
Treating Anduril like Waymo (or vice versa) will waste months.

- **Big tech (Waymo, NVIDIA, Apple, Meta Reality Labs, Zoox)** —
  use the referral path, always. Cold applications to these
  companies disappear into ATSes that were tuned for traditional CS
  pipelines, and a career-switcher CV does not look like the median
  candidate the filter expects. Concrete tactic: open LinkedIn,
  filter by company + title ("perception" / "computer vision"), find
  five people at your level (L3/L4), and send each a three-sentence
  intro: who you are, what specific project of theirs caught your
  eye, and that you are exploring a switch and would value 15 min
  of their time. Conversion to referral is reportedly 5-15% on a
  well-crafted note. Followup if no reply at 10 days, then move on.
- **Defense (Anduril, Shield AI, Saronic, Helsing, Skydio)** —
  apply directly through the company site. These recruiters move
  fast (often a screen within a week) because they are head-count
  constrained and well-funded. Citizenship requirements matter and
  are non-negotiable; check the job posting carefully. Concrete
  tactic: apply Tuesday or Wednesday morning Pacific time, when
  recruiter inbox volume is reportedly lowest. Mention your
  willingness to relocate up front — defense is on-site heavy.
- **Hot frontier startups (Figure, 1X, Skild, Pi, Wayve)** —
  recruiters DM on LinkedIn and X. Make your X profile show a real
  perception project — a short video of a working SLAM trajectory,
  a published mini-paper on arXiv, a Roboflow-hosted detection
  model. Founders and recruiters at these companies reportedly
  scroll the perception-Twitter timeline as part of their sourcing
  workflow; a 30-second working demo loop is worth more than a
  polished resume PDF. If you have something they want, they will
  find you.
- **Smaller perception startups (Pickle, Chef, Rivr, Bedrock,
  Cobot, Field AI)** — email the CTO or VP Eng directly with a
  two-line "I made this thing, want to talk?" pitch and a link to
  a 60-second demo video. These companies are too small to run a
  proper recruiting pipeline; the founder is often the recruiter.
  Conversion on a relevant, well-targeted cold email is reportedly
  much higher than at any larger company — call it 20-40% reply
  rate if the demo is genuinely good.
- **Perception SaaS / infra (Roboflow, Voxel51, Polycam, Luma)** —
  apply directly but lead with web-stack relevance. Mention
  TypeScript, React, Next.js, your frontend work. These companies
  need engineers who can ship a polished developer product, not
  another ResNet trainer. Your background is uniquely valuable here.
- **Research labs (FAIR, TRI, NVIDIA Research, DeepMind Robotics)** —
  cold applications rarely work; the path is to coauthor a workshop
  paper with someone already inside, or to land a research-engineer
  role (non-PhD track) at the same lab and convert. Very long
  timeline; not a realistic six-month plan.

## Interview prep — what perception interviews actually ask

The patterns below show up repeatedly across reported interview
loops at the companies above. They are listed roughly in order of
how often they appear in a perception-engineer screen.

- **"Explain how a Kalman filter works in your own words."** Almost
  every perception interview at every level asks some version of
  this. Study by reading the first three chapters of Probabilistic
  Robotics (Thrun et al.) and implementing a 1D constant-velocity
  filter from scratch in numpy. Be able to draw the predict /
  update equations and explain what the covariance matrix is doing
  intuitively. Bonus: be able to explain why EKF and UKF exist and
  when each is preferred.
- **"Write code to implement RANSAC for line fitting."** This is
  the classical-CV equivalent of FizzBuzz; it tests whether you
  internalized the inlier / outlier loop. Study by implementing it
  for line, then plane, then homography on a real image. Be ready
  to discuss how you pick the inlier threshold and the number of
  iterations.
- **"Derive the pinhole projection equation."** Tests basic 3D
  geometry literacy. Study by working through Hartley & Zisserman
  chapter 6, or the equivalent in Szeliski. You should be able to
  go from world point through extrinsics, intrinsics, distortion,
  to pixel, on a whiteboard, without notes.
- **"Given a noisy IMU stream, how would you fuse it with camera
  poses?"** Tests whether you understand visual-inertial odometry
  (VIO) at a system level. Study by reading the VINS-Mono paper and
  ideally getting it running on the EuRoC dataset. Be ready to
  discuss bias estimation, gravity alignment, and the time-sync
  problem.
- **"Debug a SLAM trajectory that's drifting."** Open-ended systems
  question. Study by actually breaking a known-good SLAM pipeline
  (ORB-SLAM3, e.g.) in different ways — bad calibration, missing
  loop closure, sensor desync — and noting the failure signature
  of each. Expect to discuss differentials: loop closure off,
  scale drift, IMU bias estimation, calibration error.
- **"Describe a recent vision paper you read."** Tests genuine
  curiosity. Pick two or three recent papers (DINOv2, SAM 2,
  FoundationPose, Co-Tracker, NeRF-on-the-go, anything from the
  last CVPR) and be able to explain the problem, the contribution,
  and one limitation. Avoid claiming you read papers you only
  skimmed; senior interviewers will probe and you will get burned.
- **"Implement non-maximum suppression."** Coding-round classic.
  Practice it cold; you should be able to write it in 15 minutes
  with the IoU helper included. Bonus points for the vectorized
  numpy version and for knowing about Soft-NMS and DIoU-NMS.

## Red flags when evaluating a perception job

You will (hopefully) end up with multiple offers. The salary band
is easy to compare. The harder thing to compare is whether the
perception org is set up to succeed. Watch for these.

- **No engineer-on-site at the customer.** Perception always
  degrades when only the dev environment is tested. If the company
  ships robots to customers but has no field-eng rotation, you will
  spend your nights debugging issues from screenshots and one-line
  Slack messages. Ask in the interview: "When a customer reports
  a perception bug, what's the loop?"
- **No time-sync infrastructure.** A tell that they treat sensors
  as independent. Ask: "How are your sensors time-synced?" If the
  answer is "we use system clocks and it's mostly fine," run. If
  the answer mentions PTP, hardware triggers, or a dedicated sync
  board, you're in good hands.
- **The only person who can debug the camera pipeline is leaving.**
  Single-point-of-failure orgs are everywhere in perception because
  the senior person tends to have built the whole stack. Ask: "If
  the perception lead got hit by a bus, who could debug a
  calibration drift in production?" The answer reveals a lot.
- **The data-collection process requires a PhD.** If the company's
  labeling and curation pipeline is "ask Maria, she has the
  spreadsheet," your day-two will be eating glass. Healthy
  perception orgs have a data platform team or at least a clear
  labeling tool (Roboflow, Voxel51, Encord, Scale, in-house).
- **No evaluation harness for the model.** "We ship when it looks
  good in the demo" is a code smell as serious as no CI for a web
  app. Ask: "What's your perception eval set? How often does it
  run? What metrics gate a release?"
- **Equity is mentioned but the cap table is hidden.** At small
  companies it's reasonable to ask for the percentage of fully-
  diluted equity, the current preference stack, and the most
  recent 409A. Refusal is a flag.
- **The role title and the actual work don't match.** "ML Engineer,
  Perception" that turns out to be 80% data labeling supervision
  is a common bait-and-switch. Ask for a concrete description of
  what the last person in this role shipped in the past six months.

## Where perception engineers earn the most

Approximate TC bands for senior IC (3-7 years exp), 2025 Bay Area /
NYC. Sources: levels.fyi (NVIDIA, Waymo, Apple, Meta, Tesla bands),
the 2025 Robotics Salary Guide (medians and the $189k overall
median), Glassdoor self-reports (Shield AI, Anduril, Boston Dynamics,
Mobileye), public funding announcements for relative startup tier,
and Blind / Hacker News compensation threads (cross-validation).
Hedge: startup TC numbers are particularly noisy because they
include illiquid common shares valued at the last preferred-round
price.

- NVIDIA: $300-450k
- Waymo: $300-450k (median $232k for all levels)
- Apple, Meta Reality Labs: $300-500k
- Tesla: $300-500k+
- Anduril, Shield AI: $300-500k (heavy equity)
- Physical Intelligence, Wayve, Skild, Figure, 1X: $350-600k+ (the
  equity is the lottery ticket)
- Boston Dynamics, TRI, Mobileye: $230-380k
- Smaller startups (Pickle, Chef, Bedrock, Rivr): $200-350k
- Perception SaaS (Roboflow, Voxel51, Polycam, Luma): $200-330k,
  but with full-remote optionality that the on-site companies
  cannot match

Numbers assume Bay Area / NYC / Seattle. Remote / EU is usually
20-40% lower; London Wayve / Helsing close the gap a bit.

**Equity vs. cash trade-off — read this before you optimize for
the biggest number.** At a $40B-valuation humanoid startup (Figure
at the rumored Feb 2025 valuation, e.g.), a 0.05% RSU grant feels
small on paper but is a meaningful lottery ticket if you believe a
2x to 5x outcome is plausible — that's $20M to $50M paper value, of
which maybe 20-40% becomes liquid in any near-term scenario. At a
Series-B perception SaaS, the same 0.05% is worth less in expected
value (call it $100k-$500k), but vests faster, is more likely to
become liquid via secondaries or a strategic acquihire, and does
not depend on a particular 5-year science bet paying off. A useful
heuristic: discount frontier-startup equity by 70-90% when
comparing offers, discount Series-B/C startup equity by 40-60%, and
treat public-company RSUs at face value (they vest into actual
liquid stock). Cash is cash. If you have personal runway
constraints — student loans, family obligations, no savings — bias
toward base salary at a large company; if you have 12+ months of
runway and high risk tolerance, the frontier startups have
meaningfully better expected value over a five-year horizon.

## Remote / hybrid posture by employer type

A surprisingly important filter, since perception is one of the
less remote-friendly robotics subfields (the robot is in the lab).

- **AV labs (Waymo, Cruise, Zoox)** — strictly hybrid, on-site
  3-5 days for vehicle work. Some offline / data / training roles
  are more flexible. Do not assume remote is on the table.
- **Foundation-model perception (Meta FAIR, NVIDIA Research, Google
  DeepMind robotics)** — quite remote-friendly for research and
  for ML infra; less so for product perception.
- **Humanoid startups (Figure, 1X, Apptronik, Cobot)** — strictly
  on-site, the robot is in the lab and you cannot debug a
  manipulation perception bug over Slack. Plan to relocate.
- **Defense (Anduril, Shield AI, Saronic, Helsing)** — mostly
  on-site, partly because of classified work and partly because of
  hardware. Some non-classified roles allow hybrid.
- **AR / glasses (Apple Vision Products, Meta Reality Labs)** —
  on-site for hardware-integrated work, hybrid for app-layer
  perception.
- **Perception SaaS (Polycam, Luma, Roboflow, Voxel51, Veo,
  Encord)** — fully remote-friendly, often globally distributed.
  If remote is a hard requirement, this is your tier.
- **Industrial / vertical robotics (Pickle, Chef, Bedrock, Path,
  Symbotic)** — on-site, often in a non-major-tech city (Cambridge
  MA, Pittsburgh, Austin, Ohio). Compensation adjusts.

## Title decoder ring

Hiring titles in perception are inconsistent across companies,
and the same job can carry five different names. Below is a rough
mapping; treat it as a translation table when reading job boards.

- **Perception Engineer** — most common umbrella title. Covers
  classical CV, deep learning, sensor fusion, and the integration
  glue between them. Used by Waymo, Zoox, Cruise, Skydio, Pickle,
  Cobot. Day-to-day: own one slice of the pipeline (e.g. tracking,
  or lidar segmentation), ship code that runs on the robot.
- **Computer Vision Engineer** — slightly more ML / image-focused,
  less sensor-fusion-y. Used heavily by Apple, Meta Reality Labs,
  Snap, Polycam, Luma, Roboflow, Voxel51. Day-to-day: train and
  deploy CV models, often with a product / API surface.
- **Robotics Software Engineer (Perception)** — generalist robotics
  eng who happens to work on the perception stack; expects ROS /
  C++ comfort plus model integration. Used by Figure, 1X,
  Apptronik, Boston Dynamics, Saronic. Day-to-day: more systems-
  integration than pure ML.
- **ML Engineer, Perception** — emphasis on training, infra, and
  scaling, less on the on-robot deployment side. Used by Wayve,
  Tesla, Physical Intelligence, Skild, Meta FAIR. Day-to-day:
  PyTorch / JAX, data loaders, distributed training, evaluation.
- **Sensor Fusion Engineer** — explicitly multi-modal. Used by
  Mobileye, Shield AI, Anduril (some Lattice roles), Bosch, ZF.
  Day-to-day: Kalman / particle / factor-graph filters, time-sync,
  calibration, very C++ heavy.
- **SLAM Engineer** — narrow specialty around simultaneous
  localization and mapping. Used by Skydio, Niantic, Magic Leap,
  Apple ARKit, some AV teams. Day-to-day: pose estimation, loop
  closure, map management, visual-inertial odometry.
- **3D Vision Engineer** — emphasis on geometric reconstruction,
  NeRF / Gaussian splatting, multi-view stereo. Used by Polycam,
  Luma, Spline, Scaniverse, Niantic. Day-to-day: PyTorch + a lot
  of geometry; closer to a graphics-adjacent role.
- **Spatial Computing Engineer** — Apple / Meta marketing-flavored
  variant of 3D vision, mostly used in AR roles.
- **Autonomy Engineer (Perception)** — defense / drone variant;
  used by Anduril, Shield AI, Saronic. Often a generalist title
  with a perception slant.

A practical tip when applying: search job boards under all of
these titles, not just "perception engineer." Many of the best-fit
roles for a web-dev switcher are titled "Computer Vision Engineer"
or "ML Engineer, Perception" rather than the perception umbrella
term, and a keyword-only search will miss them.

## Hiring market signal

From the 2025 Robotics Salary Guide (907 jobs analyzed Nov-Dec 2025):

- Robotics Software Engineer median: **$189k**.
- ML in perception roles commands a similar +30% premium to RL/
  diffusion in VLA roles.
- "Computer Vision Engineer" is a named trending title in 2025
  hiring reports.
- Global CV market: **$19.82B in 2024**, growing at **~19.8% CAGR
  through 2030** (Grand View Research, MarketsandMarkets).

Translation: this is the most broadly-applicable robotics specialty.
Less explosive than VLA right now, but with a much wider customer
base and dozens of viable employers in every major US/EU city.

For where to go next: `05-projects.md` lists portfolio projects
that map cleanly to the interview patterns above (a from-scratch
RANSAC notebook, a working VINS-Mono run, a small object-detection
pipeline on a Roboflow dataset). `03-start.md` gives the first 30-
60-90 day plan that gets you to the point of credibly applying to
the tier-2 startups on this list.
