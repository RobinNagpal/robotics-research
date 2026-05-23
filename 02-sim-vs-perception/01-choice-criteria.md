# Digital Twins / Simulation vs. Perception & Computer Vision

> A criteria-by-criteria comparison for someone choosing between
> these two fields as the basis for a **3-10 person robotics
> services shop**. Read this if you've already decided VLA isn't
> the right fit for an agency (it isn't — see the rationale at the
> bottom) and you're picking between the two remaining top-3
> options.

This file goes deep on five criteria that actually move the
needle for an agency business: customer pipeline, hireability,
engagement economics, defensibility, and long-term trajectory.

---

## Criterion 1 — Customer pipeline & buyer maturity

**Question: How easy is it to land your first 10 paying clients?**

### Perception & Computer Vision

- **Buyer recognizes the problem.** "We need to detect defects on
  our PCB line" or "we need to count people coming through the
  store" is a request a procurement officer can write and a CFO
  can approve. The buyer has heard of Cognex, OpenAI Vision, AWS
  Rekognition — they have mental anchors for what CV does and
  what it costs. You don't have to explain the category.
- **Buyer pool is enormous and named.** Industrial inspection
  market alone is **~$30B in 2025 (~7% CAGR)**. Add agriculture,
  drones, AR, AV, defense, retail analytics, healthcare imaging,
  and you're looking at hundreds of thousands of addressable
  organizations globally, of which tens of thousands have ML
  budget today.
- **Channel partners exist.** System integrators (JR Automation,
  ATS, Olympus Controls, hundreds of regional shops) already sell
  vision systems and routinely subcontract the ML piece. You can
  build a pipeline through these partnerships in 6 months.
- **Cold outreach works.** LinkedIn + trade shows + Industry Week
  press list = a credible client pipeline by month 3.

### Simulation & Digital Twins

- **Buyer often can't articulate what they want.** "We need
  better synthetic data" is a research-engineer concern, not a
  procurement officer one. The buyer is usually an engineering
  manager at a humanoid / AMR / AV startup, and they're already
  trying to build the capability internally.
- **Buyer pool is small but well-funded.** Maybe 200 humanoid /
  AMR / AV companies globally have the budget + interest to buy
  sim work. Add Tier-1 automotive ($15-50B vendors) and a few
  hundred industrial-twin programs at large manufacturers, and
  you're at ~1-2k addressable buyers — vs. 100k+ for perception.
- **Buying signal is weak.** Sim spend is mostly internal headcount
  at those companies. You're selling against "we'll just hire one
  more engineer," which is a harder pitch than "you don't have
  any CV engineers."
- **Sales cycles are long.** Enterprise twins (Siemens / BMW
  scale) are 6-12 month sales cycles. Even mid-market sim
  engagements take 2-4 months from first call to PO.

**Verdict: Perception wins clearly.** A perception shop will land
clients in months. A sim shop will land them in quarters.

---

## Criterion 2 — Talent market & hireability (scaling from 3 → 10)

**Question: Can you actually hire 7 more engineers in 18 months
without burning out the founders on recruiting?**

### Perception & Computer Vision

- **Talent pool is hundreds of thousands globally.** Every CS
  graduate who took a CV elective, every self-taught engineer
  who finished CS231n or PyImageSearch, every ML engineer with
  vision experience. CVPR alone has 10k+ attendees.
- **Salary bands are reasonable for an agency.** Strong mid-level
  CV engineers go for **$120-180k base in the US**, less in EU /
  India / LatAm. You can profitably bill at $150-200/hr while
  paying $130k.
- **Onboarding is fast.** A new hire with general ML + Python
  background can ship a working anomaly-detection model in week
  2 if your templates are good.
- **Geographic flexibility.** Strong CV talent exists in every
  major tech hub + many non-traditional ones (Poland, Argentina,
  India, Vietnam, Egypt). Remote-first is realistic.

### Simulation & Digital Twins

- **Talent pool is in the low tens of thousands.** Isaac
  Sim / Isaac Lab / Omniverse experience is rare. USD experience
  is rarer. Sim+RL together is rarer still.
- **Salary bands are inflated by NVIDIA and humanoid startups.**
  Engineers who know Isaac Lab + RL command **$200-350k** at
  US startups; NVIDIA itself pays $270k median. You'll pay close
  to top-of-market or you won't hire.
- **Onboarding takes months.** Isaac Lab's abstractions, USD
  composition arcs, sim2real recipes — all take real time to
  internalize. A new hire takes 2-3 months to be productive on
  customer work even with strong RL background.
- **Geographic concentration is severe.** Most of the talent is
  in 6-8 metros (Bay Area, Seattle, Pittsburgh, Boston, Zurich,
  Munich, London, Tel Aviv). Remote is harder because adjacent
  experts to learn from are scarce.

**Verdict: Perception wins clearly.** You can hire 7 perception
engineers in 18 months at agency margins. Doing the same for sim
either compresses your margins or stretches your hiring runway
to 30+ months.

---

## Criterion 3 — Engagement economics & recurring revenue

**Question: Per active client per year, how much revenue can you
realistically book — and how much is recurring vs. one-shot?**

### Perception & Computer Vision

- **One-shot engagements: $15-80k typical.** Visual inspection
  model: $15-40k. 6-DoF pose API setup: $20-60k. SLAM tuning
  report: $5-25k. On-prem inference container: $10-30k. These
  are sized for SMB manufacturers and mid-market integrators.
- **Recurring revenue is natural.** Models drift, lighting
  changes, SKUs evolve, new defect classes appear. "Quarterly
  retraining + monitoring" = $1-3k/month per customer.
  Eventually 50% of revenue is recurring, which is what makes
  the agency valuation-attractive (2-4x ARR vs. 0.5-1x for
  pure services).
- **Customer LTV is high.** A satisfied SMB manufacturer expands
  to more defect classes, more product lines, more sites. $30k
  initial engagement turns into $80-200k cumulative over 3 years.
- **Repeatable templates.** By engagement #5 of "visual QC for an
  SMB factory," you're reusing 60% of the code (data pipeline,
  anomaly detector, deployment container, monitoring dashboard).
  Margins climb from 30% to 55%+.

### Simulation & Digital Twins

- **One-shot engagements: $30-120k typical.** Custom Isaac Lab
  env: $15-60k. Procedural scene generator: $20-80k. Synthetic
  data pipeline: $5-50k. Full digital twin of a customer site:
  $50-200k+. Bigger checks but rarer.
- **Recurring revenue is harder.** Once you deliver an env or a
  synthetic dataset, the customer often doesn't need ongoing
  work — they take it in-house. Maintenance retainers exist
  ($5-25k/year licenses) but they're a smaller slice.
- **Customer LTV is bimodal.** Either the customer becomes a
  long-term partner ($200-500k/year) or they pay once and leave.
  Few in the middle.
- **Less repeatable per customer.** Every Isaac Lab env is at
  least 40% bespoke (different robot, different task, different
  reward shape). Code reuse exists but at a lower rate than CV
  templates.

**Verdict: Close, but perception edges out for an agency.** Sim
has a higher *peak* per engagement, but perception has a more
predictable mid-range and a much stronger recurring-revenue
profile. For agency valuation, recurring matters more than peak.

---

## Criterion 4 — Competitive landscape & defensibility

**Question: How crowded is the market, and what's your moat?**

### Perception & Computer Vision

- **More competition.** Existing CV agencies (some big — Innowise,
  Intellias, plus hundreds of smaller shops), product companies
  (Roboflow, Encord, Scale AI), and the cloud incumbents (AWS
  Rekognition, Google Vision API).
- **But the competitive gap is real.** Most generic CV agencies
  don't know ROS, don't know edge deployment, don't know
  industrial sensor calibration. The robotics-grade CV
  positioning — "we deliver vision that runs on a Jetson at 30
  Hz inside a real robot" — separates you from the web-CV
  crowd.
- **Defensibility via vertical specialization.** Pick a vertical
  (industrial QC for PCB assembly, or 6-DoF for warehouse
  picking, or perception for delivery drones) and build a deep
  reputation in it. Within 18 months you can be the named
  expert in that vertical.
- **Defensibility via templates and data assets.** Your library
  of pre-trained anomaly models, your evaluation suites, and
  your fine-tuning pipelines compound. Hard to replicate without
  the customer base.

### Simulation & Digital Twins

- **Less direct competition.** Very few agencies do robotics-
  grade sim. The competitors that exist (small specialty shops
  + NVIDIA's Professional Services group + Applied Intuition for
  AV specifically) are limited.
- **NVIDIA's partner ecosystem creates a clear lane.** Becoming
  a recognized NVIDIA Isaac / Omniverse partner is achievable
  with a few good case studies and gives you co-marketing,
  joint sales, and a halo effect that's hard for competitors to
  match.
- **Defensibility via NVIDIA relationship.** If you're in NVIDIA's
  Solution Provider directory and they refer customers to you,
  that's an extremely durable moat that money alone can't
  replicate.
- **Risk: NVIDIA changes its mind or builds it themselves.** Your
  entire moat depends on a single platform vendor's continued
  goodwill. NVIDIA could (a) build first-party services that
  compete with you, (b) shift to a different stack, or (c)
  prioritize different partners. This is a real concentration
  risk that doesn't exist in perception (where Apple, Meta,
  AWS, and Google all matter, so no single vendor can ice you
  out).

**Verdict: Sim wins on raw competition (less crowded), but
perception wins on long-term defensibility (no platform-vendor
concentration risk).** The two cancel out roughly; this criterion
is closer than the first three.

---

## Criterion 5 — 5-10 year market trajectory & exit options

**Question: If you build this for 5-10 years, what does the
ceiling look like? Acquisition? IPO? Lifestyle business?**

### Perception & Computer Vision

- **Market size.** Global CV market: **$19.82B (2024) → ~$58B
  (2030) at 19.8% CAGR**. Industrial vision specifically growing
  ~7-9% CAGR. AV perception spend is multi-billions per year
  across primes.
- **Exit paths are abundant.** Cognex, Keyence, Zebra, Teledyne,
  Trimble, Hexagon — any of these mid-cap industrial-vision
  companies will buy a quality CV services shop with $5-20M
  ARR for 1.5-3x revenue (services multiple) or 4-8x ARR
  (if you've productized). Roll-ups are also common.
- **Productization is realistic.** Many of the best CV services
  shops have spun out a SaaS product (Roboflow's lineage, for
  example). You can run services to fund product development
  and pivot to product if a clear opportunity emerges.
- **Ceiling.** A perception agency can realistically scale to
  $10-30M ARR with 30-80 people, then either sell or stay
  lifestyle.

### Simulation & Digital Twins

- **Market size.** Physical-AI sim + digital-twin market: **$3.8B
  (2025) → $34.6B (2034) at 28.5% CAGR — the highest of any
  robotics segment**. Specifically, the Isaac / Omniverse
  ecosystem is in hyper-growth.
- **Exit paths exist but are concentrated.** Likely acquirers:
  NVIDIA itself (most likely), Autodesk, Siemens, Dassault,
  Applied Intuition. Plus the humanoid winners (Figure / 1X / PI)
  could acquire a sim shop they've grown to depend on. Smaller
  acquirer pool than perception, but the strategics will pay
  more (NVIDIA in particular).
- **Productization is realistic.** A sim agency naturally
  develops reusable components (env templates, synthetic-data
  generators, sim2real adapters) that can productize.
- **Ceiling.** A sim agency can realistically scale to $5-20M ARR
  with 20-50 people in 5 years if it rides the NVIDIA wave
  successfully. Higher per-engagement revenue compensates for
  the narrower customer base.

**Verdict: Sim has higher *growth rate* of underlying market;
perception has more *exit optionality and acquirer diversity*.**
For a founder optimizing for maximum 10-year upside *if you ride
the right wave*, sim wins. For a founder optimizing for
robust-to-bad-luck outcomes, perception wins.

---

## Composite scorecard

| Criterion | Perception | Sim | Winner |
|---|---|---|---|
| 1. Customer pipeline & buyer maturity | A | C+ | **Perception** |
| 2. Talent market & hireability | A | C | **Perception** |
| 3. Engagement economics & recurring revenue | A- | B | **Perception** |
| 4. Competitive landscape & defensibility | B+ | B+ | Tie |
| 5. 5-10 year market trajectory & exit options | A- | A- | Tie |

**Overall: Perception is the safer, faster-to-revenue, easier-to-
scale choice for a services shop. Sim is the higher-ceiling-but-
narrower bet for a founder willing to accept a slower start in
exchange for less competition and the NVIDIA tailwind.**

---

## Recommendation for a 3-10 dev agency

**Lead with Perception. Layer in Sim as a premium specialty.**

A pragmatic 24-month roadmap:

- **Months 0-6:** Stand up a perception practice. Visual QC, 6-DoF
  pose API, custom detection models. Target SMB manufacturers
  and regional system integrators. Goal: 4 paying clients,
  $200-300k revenue.
- **Months 6-12:** Hire 2-3 more perception engineers. Add a
  vertical specialization (pick one: industrial QC, warehouse
  picking, drone inspection). Goal: 8-10 active clients,
  $700k-1.2M revenue, 40% recurring.
- **Months 12-18:** Hire your first sim engineer. Pitch sim
  work to your existing perception customers ("we built your
  defect detector; now let us build the synthetic data
  pipeline that keeps it from drifting"). Goal: 2 sim
  engagements, $100-200k incremental.
- **Months 18-24:** Become an NVIDIA Isaac partner. Spin up a
  small sim team (2-3 engineers). Start pitching humanoid /
  AMR startups directly. Goal: 3-5 sim engagements + ongoing
  perception practice, $2-3M total revenue.

This sequencing keeps cash flow healthy (perception pays the
bills from month 3) while letting you build the sim
capability into a higher-margin premium offering by year 2.

---

## Why not VLA for an agency?

VLA loses on all five criteria above:

- **Pipeline (1):** buyers can't articulate requirements.
- **Hireability (2):** $400k+ engineer cost vs. $150-200/hr
  billing rate doesn't math.
- **Economics (3):** every engagement is one-of-one; no
  templates yet.
- **Competition (4):** dominated by in-house teams at top labs
  with $200M+ in research budgets.
- **Trajectory (5):** likely an enormous product opportunity,
  but not a services one — the value capture is in the model
  weights, not the integration work.

Revisit VLA in 2-3 years when the buying side matures, OR
build a VLA-adjacent product company instead of an agency.
