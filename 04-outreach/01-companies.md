# Outreach Target List: Robotics Companies for Simulation & Synthetic-Data Services

A prospect list of **pure-play robotics companies** that could buy
services for **simulation-environment creation** (digital twins, Gazebo /
Isaac Sim / MuJoCo scenes, domain randomization pipelines) or
**synthetic-data generation** (rendered training imagery, simulated
sensor data, procedural scenario libraries).

**Inclusion criteria** (every company below was checked against all
three):

- Raised **more than $5M** in a funding round announced between
  **June 2024 and June 2026** (the last two years).
- Valuation **below $5 billion** (companies at or above $5B — e.g.
  Figure AI, Anduril, Shield AI, Apptronik — were excluded).
- **Pure robotics**: the robot, or the robot's autonomy/intelligence
  stack, is the product. No 3PLs, retailers, or medtech firms that
  merely use robots.

**Caveats:** valuations, raise amounts, and headcounts are approximate
(`~`), drawn from press coverage and LinkedIn at research time
(June 2026), and **drift quickly — re-verify before quoting in an
outreach email**. Where a valuation was never disclosed, total funding
raised is given instead. **103 companies** are grouped by sector; the
numbering runs continuously across sections.

---

## 1. Humanoids & general-purpose robot intelligence

These companies live or die by sim-to-real training and large-scale
synthetic data — the strongest fit for both service lines.

1. **Agility Robotics** — Corvallis, USA
   - **What they do:** Builds Digit, a bipedal humanoid robot for
     warehouse and logistics work (tote moving, pick-and-place),
     deployed with customers like GXO.
   - **Website:** https://www.agilityrobotics.com
   - **Valuation:** ~$2.1B post-money reported (as of 2025 round)
   - **Last raise:** ~$400M Series C (announced March–April 2025) —
     [Agility Robotics reportedly raising $400M for humanoid warehouse robots](https://www.geekwire.com/2025/agility-robotics-reportedly-raising-400m-for-humanoid-warehouse-robots/)
   - **Employees:** ~400
   - **Why sim / synthetic data:** Digit's locomotion and manipulation
     policies are trained heavily in simulation (sim-to-real RL);
     scaling to new warehouse layouts and SKUs demands large libraries
     of randomized warehouse environments and synthetic perception
     data.

2. **NEURA Robotics** — Metzingen, Germany
   - **What they do:** Develops "cognitive" collaborative robots
     (MAiRA, MAV) and the 4NE-1 humanoid for manufacturing, logistics,
     and household use, plus the Neuraverse robot-skills platform.
   - **Website:** https://neura-robotics.com
   - **Valuation:** ~€4B (~$4.3B) reported around the March 2026 raise
     — re-check before quoting
   - **Last raise:** ~€1B (~$1.2B) growth round led by Tether
     (March 2026); previously ~€120M Series B (January 2025) —
     [Humanoid robot maker Neura Robotics reportedly raising $1.2B in funding](https://siliconangle.com/2026/03/04/humanoid-robot-maker-neura-robotics-reportedly-raising-1-2b-funding/)
   - **Employees:** ~500 (doubling headcount through 2025)
   - **Why sim / synthetic data:** NEURA ships a multi-robot ecosystem
     (cobots plus a humanoid) into many industries at once and needs
     simulated work cells and synthetic vision/touch data to train and
     certify each new "skill" without per-customer data collection.

3. **Dyna Robotics** — Redwood City, USA
   - **What they do:** Trains robotic foundation models (DYNA-1) that
     make affordable stationary arms commercially viable for
     repetitive tasks like napkin folding and dishwashing in real
     businesses.
   - **Website:** https://www.dyna.co
   - **Valuation:** ~$600M+ post-money (as of September 2025)
   - **Last raise:** ~$120M Series A (September 2025) —
     [Dyna Robotics closes $120M funding round to scale robotics foundation model](https://www.therobotreport.com/dyna-robotics-closes-120m-funding-round-to-scale-robotics-foundation-model/)
   - **Employees:** ~60
   - **Why sim / synthetic data:** A foundation-model shop whose
     bottleneck is task and environment diversity — simulated
     kitchens/laundromats and synthetic deformable-object data
     (towels, napkins, dishes) directly augment their costly
     real-world teleoperation data.

4. **FieldAI** — Mission Viejo, USA
   - **What they do:** Builds "Field Foundation Models" — risk-aware
     embodied-AI brains that let third-party quadrupeds, wheeled
     robots, and humanoids navigate unstructured construction, energy,
     and industrial sites.
   - **Website:** https://www.fieldai.com
   - **Valuation:** ~$2B (as of August 2025)
   - **Last raise:** ~$405M across two back-to-back rounds (August
     2025; Bezos Expeditions, NVentures, Temasek, Khosla) —
     [Nvidia, Bill Gates-backed robotics startup Field AI hits $2 billion valuation](https://www.cnbc.com/2025/08/20/gates-nvidia-fieldai-robotics.html)
   - **Employees:** ~150
   - **Why sim / synthetic data:** Models that must generalize across
     robot embodiments and hazardous sites need procedurally generated
     environments and synthetic sensor data across terrain, weather,
     and embodiment variations — real testing there is slow and
     dangerous.

5. **Mind Robotics** — Palo Alto, USA
   - **What they do:** Rivian spin-out building foundation models plus
     purpose-built robots to automate dexterous factory tasks, seeded
     with production data from Rivian's EV manufacturing lines.
   - **Website:** https://www.mindrobotics.com
   - **Valuation:** ~$2B (March 2026 Series A; a later round reportedly
     ~$3.4B — re-check)
   - **Last raise:** ~$500M Series A (March 2026, Accel and a16z
     co-led) —
     [Rivian spin-out Mind Robotics raises $500M for industrial AI-powered robots](https://techcrunch.com/2026/03/11/rivian-mind-robotics-series-a-500m-fund-raise-industrial-ai-powered-robots/)
   - **Employees:** ~150 (scaling rapidly)
   - **Why sim / synthetic data:** Factory data from one plant doesn't
     cover the variation needed for general industrial manipulation;
     digital twins of assembly stations and synthetic part/fixture
     data let them validate policies before touching a live production
     line.

6. **The Bot Company** — San Francisco, USA
   - **What they do:** Kyle Vogt's (ex-Cruise) startup building a
     wheeled home robot with an arm and grippers that tidies and
     organizes household items via natural-language commands.
   - **Website:** https://bot.co
   - **Valuation:** ~$2B (March 2025); a ~$250M round at ~$4B+ was
     reported in late 2025 — re-check
   - **Last raise:** ~$150M Series B (March 2025, Greenoaks-led) —
     [Former Cruise CEO Kyle Vogt's new robotics startup reportedly raises another $150M](https://techcrunch.com/2025/03/23/former-cruise-ceo-kyle-vogts-new-robotics-startup-reportedly-raises-another-150m/)
   - **Employees:** ~60
   - **Why sim / synthetic data:** Pre-product, they can't gather fleet
     data from customer homes yet; procedurally generated household
     environments (clutter, toys, furniture variation) and synthetic
     grasp data are the fastest path to training mobile-manipulation
     policies.

7. **Sunday Robotics** — San Francisco Bay Area, USA
   - **What they do:** Building Memo, a home robot that does chores
     (dishes, laundry, tidying), trained on millions of real-world
     household demonstrations collected with a "Skill Capture Glove."
   - **Website:** https://www.sunday.ai
   - **Valuation:** ~$1.15B reported around an early-2026 Series B
     (~$165M) — re-check before quoting
   - **Last raise:** ~$35M seed announced November 2025 (Benchmark and
     Conviction), with the larger Series B reported early 2026 —
     [Sunday wants to put a robot in every home, beginning with the launch of Memo](https://siliconangle.com/2025/11/20/sunday-wants-put-robot-every-home-beginning-launch-memo/)
   - **Employees:** ~50
   - **Why sim / synthetic data:** Their glove-collected human data
     covers only a few hundred homes; simulated home environments and
     synthetic object/scene variation would multiply skill coverage
     and let them regression-test policies before beta units enter
     real households.

8. **Genesis AI** — Palo Alto, USA & Paris, France
   - **What they do:** Full-stack physical-AI lab building a universal
     robotics foundation model (GENE) plus dexterous robot hardware,
     leveraging the open-source Genesis physics engine for ultra-fast
     data generation.
   - **Website:** https://www.genesis.ai
   - **Valuation:** undisclosed; raised ~$105M total
   - **Last raise:** ~$105M seed (July 2025, Eclipse and Khosla
     co-led) —
     [Genesis AI launches with $105M seed funding to build AI models for robots](https://techcrunch.com/2025/07/01/genesis-ai-launches-with-105m-seed-funding-from-eclipse-khosla-to-build-ai-models-for-robots/)
   - **Employees:** ~60
   - **Why sim / synthetic data:** Their training strategy is
     synthetic-data-first on their own engine, but engines need
     content — they are a natural buyer of environment/asset creation,
     scene authoring, and domain-specific simulation scenario work at
     scale.

9. **Flexion** — Zurich, Switzerland
   - **What they do:** Hardware-agnostic "brain" for humanoid robots: a
     reinforcement-learning and sim-to-real software stack that gives
     off-the-shelf humanoids autonomous manipulation and locomotion
     skills.
   - **Website:** https://flexion.ai
   - **Valuation:** undisclosed; raised ~$60M total
   - **Last raise:** ~$50M Series A (November 2025, DST Global
     Partners, NVentures) —
     [Flexion to use Series A to build sim-to-real, AI systems powering humanoids](https://www.therobotreport.com/flexion-raises-50m-build-ai-systems-power-humanoids/)
   - **Employees:** ~30
   - **Why sim / synthetic data:** Their entire product is trained
     sim-to-real across multiple humanoid morphologies — they
     explicitly need fleets of simulated environments, randomized task
     scenarios, and synthetic perception data to make one brain work
     on many bodies.

10. **mimic robotics** — Zurich, Switzerland
    - **What they do:** ETH Zurich spin-off building dexterous humanoid
      robotic hands driven by foundation models trained on human
      demonstrations, retrofittable to existing arms for manufacturing
      and logistics.
    - **Website:** https://www.mimicrobotics.com
    - **Valuation:** undisclosed; raised ~$20M+ total
    - **Last raise:** ~$16M seed (November 2025, Elaia and
      Speedinvest) —
      [Mimic raises $16M to build AI models for human-like robotic hands](https://siliconangle.com/2025/11/04/mimic-raises-16m-build-ai-models-human-like-robotic-hands/)
    - **Employees:** ~25
    - **Why sim / synthetic data:** Dexterous-hand policies need
      enormous contact-rich interaction data that human demos alone
      can't cover; simulated hand-object interaction with accurate
      contact physics and synthetic object libraries would scale their
      skill training cheaply.

11. **Tacta Systems** — Palo Alto, USA
    - **What they do:** Building "dextrous intelligence" — a robot
      nervous system combining tactile hardware, software, and AI so
      robots can manipulate with human-like touch in logistics,
      manufacturing, and healthcare.
    - **Website:** https://www.tactasystems.com
    - **Valuation:** undisclosed; raised ~$75M total
    - **Last raise:** ~$64M Series A (June/July 2025, America's
      Frontier Fund and SBVA) —
      [Tacta Systems raises $75M to give robots a 'smart nervous system'](https://www.therobotreport.com/tacta-systems-raises-75m-give-robots-smart-nervous-system/)
    - **Employees:** ~50
    - **Why sim / synthetic data:** Tactile-driven manipulation needs
      paired touch-vision training data that's scarce in the real
      world; simulated contact/force environments and synthetic
      tactile-sensor data would let them pre-train policies before
      fine-tuning on physical sensors.

12. **Persona AI** — Houston, USA
    - **What they do:** Building rugged industrial humanoids for
      shipbuilding and heavy manufacturing (welding-class tasks), with
      a deployment agreement with HD Hyundai shipyards.
    - **Website:** https://persona.ai
    - **Valuation:** undisclosed; raised ~$27M total
    - **Last raise:** ~$27M pre-seed (May 2025, Unity Growth and Tides
      Ventures co-led) —
      [Persona AI raises $27M to develop humanoid robots for shipyards](https://www.therobotreport.com/persona-ai-raises-27m-develops-purpose-built-humanoid-robots-shipyards/)
    - **Employees:** ~40
    - **Why sim / synthetic data:** Shipyards are among the hardest
      places to collect training data (welding arcs, confined spaces,
      safety rules); digital-twin shipyard environments and synthetic
      weld-seam/part data are essentially the only way to train and
      validate their humanoid on schedule.

13. **Fourier (Fourier Intelligence)** — Shanghai, China
    - **What they do:** Makes GR-series general-purpose humanoid robots
      (GR-2, GR-3) plus rehabilitation robotics, targeting research,
      care, and human-robot-interaction deployments.
    - **Website:** https://www.fftai.com
    - **Valuation:** undisclosed; latest round ~$109M (total several
      hundred million — re-check)
    - **Last raise:** ~$109M (¥800M) Series E (January 2025,
      Prosperity7-backed) —
      [Chinese robotics firm Fourier books nearly $109m in Series E round](https://www.dealstreetasia.com/stories/chinese-robotics-firm-fourier-books-nearly-109m-in-prosperity7-backed-series-e-round-425571)
    - **Employees:** ~500+
    - **Why sim / synthetic data:** Fourier sells humanoid platforms to
      research and care customers who each need new skills; simulated
      locomotion/manipulation curricula and synthetic interaction data
      shorten the path from hardware shipment to useful deployed
      behaviors.

14. **Galbot** — Beijing, China
    - **What they do:** Embodied-AI company whose wheeled dual-arm
      Galbot G1 robots run unmanned retail stores in 30+ Chinese
      cities and do manufacturing/logistics tasks, powered by in-house
      VLA foundation models trained largely on synthetic data.
    - **Website:** https://www.galbot.com
    - **Valuation:** ~$3B (as of December 2025)
    - **Last raise:** ~$300M+ growth round (December 2025; a further
      ~$362M reported by March 2026) —
      [Humanoid robot maker Galbot raises $300 million and reaches $3 billion valuation](https://roboticsandautomationnews.com/2025/12/20/humanoid-robot-maker-galbot-raises-300-million-and-reaches-3-billion-valuation/)
    - **Employees:** ~500
    - **Why sim / synthetic data:** Galbot's grasping models are
      famously trained on billions of simulated grasps ("sim-first"
      strategy); expanding from retail into factories needs ever more
      diverse simulated environments and synthetic SKU/scene data to
      keep that flywheel spinning.

15. **Wandercraft** — Paris, France
    - **What they do:** Makes self-balancing walking exoskeletons
      (Atalante X for rehab, Eve for personal mobility) and Calvin-40,
      an industrial humanoid developed with Renault.
    - **Website:** https://www.wandercraft.eu
    - **Valuation:** undisclosed; total raised well over $150M
    - **Last raise:** ~$75M Series D (June 2025, Renault Group and
      Bpifrance) —
      [Wandercraft raises $75M to scale exoskeletons, humanoids](https://www.therobotreport.com/wandercraft-raises-75m-to-scale-exoskeletons-humanoids/)
    - **Employees:** ~150–300 (estimates vary)
    - **Why sim / synthetic data:** Bipedal balance controllers for
      exoskeletons and the Calvin humanoid cannot be safely iterated
      on patients or factory floors; physics-accurate gait simulation
      and synthetic terrain/factory environments are core to
      validating locomotion policies.

---

## 2. Warehouse, logistics & manufacturing automation

Perception-heavy picking, unloading, and fleet autonomy — every new
customer site or SKU is a synthetic-data problem.

16. **Dexterity** — Redwood City, USA
    - **What they do:** AI-powered industrial robot arms ("physical
      AI") that do human-like warehouse tasks — parcel sorting, truck
      loading, palletizing — for customers like FedEx and UPS.
    - **Website:** https://www.dexterity.ai
    - **Valuation:** ~$1.65B (as of March 2025)
    - **Last raise:** ~$95M venture round (March 2025, Lightspeed and
      Sumitomo) —
      [Yet another AI robotics firm lands major funding, as Dexterity closes latest round](https://techcrunch.com/2025/03/11/yet-another-ai-robotics-firm-lands-major-funding-as-dexterity-closes-latest-round/)
    - **Employees:** ~300
    - **Why sim / synthetic data:** Their task-specific models for
      mixed-SKU truck loading must handle endless parcel shapes,
      weights, and stacking configurations — simulated trailers and
      synthetic parcel data are far cheaper than collecting failure
      cases on live dock doors.

17. **Nimble Robotics** — San Francisco, USA
    - **What they do:** General-purpose warehouse fulfillment robots
      and fully autonomous 3PL warehouses (picking, packing, storage,
      sorting), scaling with strategic partner FedEx.
    - **Website:** https://www.nimble.ai
    - **Valuation:** ~$1B (as of October 2024)
    - **Last raise:** ~$106M Series C (October 2024, FedEx-led) —
      [Nimble Closes $106 Million Series C Funding Round](https://www.businesswire.com/news/home/20241023998446/en/Nimble-Closes-$106-Million-Series-C-Funding-Round-Scales-Fully-Autonomous-Fulfillment-with-FedEx)
    - **Employees:** ~150–200
    - **Why sim / synthetic data:** Their pick-and-pack robots must
      grasp millions of distinct SKUs; synthetic item renders and
      simulated grasp/pose data are the standard way to expand SKU
      coverage and test full-warehouse orchestration without halting
      live fulfillment.

18. **Mytra** — San Francisco, USA
    - **What they do:** Founded by an ex-Tesla Optimus lead; builds a
      3D matrix storage-and-retrieval system where robots move pallets
      and cases through a modular grid, run by an AI orchestration
      layer.
    - **Website:** https://mytra.ai
    - **Valuation:** undisclosed; raised ~$200M total
    - **Last raise:** ~$120M Series C (January 2026) —
      [Mytra raises $120 million Series C to scale supply chain robotics](https://fortune.com/2026/01/15/mytra-raises-120-million-series-c-scale-supply-chain-robotics/)
    - **Employees:** ~100
    - **Why sim / synthetic data:** Fleet-level orchestration of
      hundreds of cell-robots in a dense 3D grid needs discrete-event
      and physics simulation of customer-specific grid configurations
      for design validation, throughput guarantees, and
      control-software testing before steel goes up.

19. **Sereact** — Stuttgart, Germany
    - **What they do:** AI software (PickGPT / Cortex) that lets
      standard robot arms do zero-shot picking, packing, and order
      consolidation in warehouses; 200+ systems deployed in Europe.
    - **Website:** https://sereact.ai
    - **Valuation:** undisclosed; raised ~$140M+ total
    - **Last raise:** ~$110M Series B (April 2026) —
      [Sereact Raises $110M in Series B Funding to Expand Warehouse Robotics Platform](https://theaiinsider.tech/2026/04/27/sereact-raises-110m-in-series-b-funding-to-expand-warehouse-robotics-platform/)
    - **Employees:** ~80
    - **Why sim / synthetic data:** Their whole pitch is picking items
      the robot has never seen — synthetic training data for novel
      SKUs, packaging, and bin clutter, plus simulated cells for
      pre-deployment validation, map directly onto their
      model-improvement loop as they scale into the US.

20. **Bright Machines** — San Francisco, USA
    - **What they do:** Software-defined "microfactories" — modular
      robotic assembly cells plus computer-vision software that
      automate electronics assembly, including AI-server manufacturing
      for hyperscalers.
    - **Website:** https://www.brightmachines.com
    - **Valuation:** undisclosed; raised ~$305M total
    - **Last raise:** ~$106M Series C equity + $20M debt, incl. NVIDIA
      and Microsoft (June 2024) —
      [AI-focused manufacturing startup raises $106 million, from Nvidia and others](https://finance.yahoo.com/news/ai-focused-manufacturing-startup-raises-130425825.html)
    - **Employees:** ~400–500
    - **Why sim / synthetic data:** Each microfactory line is
      reconfigured per product; digital-twin simulation of assembly
      cells and synthetic vision data for new components (connectors,
      PCBs, fasteners) shortens line bring-up — a core economic lever
      of their model.

21. **RobCo** — Munich, Germany
    - **What they do:** Modular, snap-together industrial robot kits
      with a physical-AI software stack, sold as robotics-as-a-service
      for SME machine tending, palletizing, dispensing, and welding.
    - **Website:** https://www.robco.de
    - **Valuation:** undisclosed; raised ~$200M+ total
    - **Last raise:** ~$100M Series C (January 2026) —
      [RobCo raises Series C funding to scale industrial automation](https://www.therobotreport.com/robco-raises-100m-scale-industrial-automation/)
    - **Employees:** ~200
    - **Why sim / synthetic data:** RobCo configures thousands of
      bespoke SME cells from modular parts — automated simulation of
      each proposed cell (reach, cycle time, collisions) and synthetic
      data for part-detection models is what lets a small team deploy
      at fleet scale.

22. **Standard Bots** — Glen Cove, USA
    - **What they do:** Designs and US-manufactures affordable
      AI-native cobot arms (RO1, RO3-Max) and industrial humanoids
      that learn tasks from physical demonstration; customers include
      Amazon, NASA, and Lockheed Martin.
    - **Website:** https://standardbots.com
    - **Valuation:** ~$1B (as of June 2026)
    - **Last raise:** ~$200M Series C (June 2026, RoboStrategy and
      General Catalyst co-led); previously ~$63M Series B (July
      2024) —
      [Standard Bots raises $200M to expand U.S. manufacturing footprint](https://www.therobotreport.com/standard-bots-raises-200m-expand-u-s-manufacturing-footprint/)
    - **Employees:** ~150
    - **Why sim / synthetic data:** Learning-from-demonstration arms
      need huge volumes of additional rollouts to make each
      demonstrated task robust — simulated work cells and synthetic
      variations of demonstrated trajectories multiply every human
      demo into thousands of training episodes.

23. **Pickle Robot** — Cambridge, USA
    - **What they do:** Robot arms that autonomously unload
      floor-loaded trucks and shipping containers at warehouse docks,
      working alongside human staff.
    - **Website:** https://www.picklerobot.com
    - **Valuation:** undisclosed; raised ~$75M+ total
    - **Last raise:** ~$50M Series B (November 2024, with Teradyne
      Robotics Ventures and Toyota Ventures) —
      [Pickle Robot gets orders for over 30 unloading systems plus $50M in funding](https://www.therobotreport.com/pickle-robot-gets-orders-over-30-unloading-systems-plus-50m-funding/)
    - **Employees:** ~100
    - **Why sim / synthetic data:** Every trailer is a different
      jumbled wall of boxes; simulated container interiors with
      randomized box sizes, weights, and collapse dynamics — plus
      synthetic depth/vision data — are the cheapest way to cover the
      long tail of unload scenarios.

24. **Dexory** — London, UK
    - **What they do:** Tall autonomous mobile robots that scan
      warehouse racking to deliver real-time inventory visibility and
      digital-twin analytics (DexoryView) for customers like GXO,
      Maersk, and DB Schenker.
    - **Website:** https://www.dexory.com
    - **Valuation:** undisclosed; raised ~$120M total
    - **Last raise:** ~$80M Series B (October 2024) —
      [Dexory secures $80M series B funding to support global expansion](https://www.robotics247.com/article/dexory_secures_80m_series_b_funding_to_support_global_expansion)
    - **Employees:** ~180
    - **Why sim / synthetic data:** Their product literally builds
      warehouse digital twins, and their scan-recognition models must
      read every barcode, label, and pallet type across new
      facilities — synthetic rack/label imagery and simulated
      navigation environments fit both the AI and autonomy sides.

25. **Nomagic** — Warsaw, Poland
    - **What they do:** AI-driven robotic pick-and-place arms for
      e-commerce and apparel fulfillment (picking, packing, sorting),
      expanding from Europe into North America.
    - **Website:** https://nomagic.ai
    - **Valuation:** undisclosed; raised ~$80M total
    - **Last raise:** ~$44M round, EBRD-led with Khosla Ventures
      (February 2025) —
      [Nomagic picks up $44M for its AI-powered robotic arms](https://techcrunch.com/2025/02/26/nomagic-picks-up-44m-for-its-ai-powered-robotic-arms/)
    - **Employees:** ~110–120
    - **Why sim / synthetic data:** Nomagic's edge is a learned
      "library" of how to grasp and handle objects; synthetic object
      datasets (deformable polybags, apparel, odd packaging) and
      simulated pick cells would expand that library far faster than
      waiting for production picks.

26. **Vecna Robotics** — Waltham, USA
    - **What they do:** Autonomous forklifts and pallet-mover AMRs plus
      orchestration software for warehousing, manufacturing, and
      automotive logistics.
    - **Website:** https://www.vecnarobotics.com
    - **Valuation:** undisclosed; raised ~$179M total
    - **Last raise:** ~$14.5M insider round (November 2024), after a
      ~$100M Series C in June 2024 —
      [Vecna Robotics raises $14.5M and taps former Motional CEO to lead startup](https://techcrunch.com/2024/11/13/vecna-robotics-raises-14-5m-and-taps-former-motional-ceo-to-lead-startup/)
    - **Employees:** ~200
    - **Why sim / synthetic data:** Autonomous forklifts must handle
      rare, safety-critical edge cases (people, dropped pallets, dock
      edges) that can't be tested live — simulated facilities and
      synthetic LiDAR/camera data for validation and regression
      testing are standard needs.

27. **Third Wave Automation** — Union City, USA
    - **What they do:** Autonomous high-reach forklifts (TWA Reach)
      with a "shared autonomy" platform that blends full autonomy with
      remote human assist.
    - **Website:** https://thirdwave.ai
    - **Valuation:** undisclosed; raised ~$97M total
    - **Last raise:** ~$27M Series C led by Toyota's Woven Capital
      (October 2024) —
      [Third Wave Automation picks up Series C funding for robotic forklifts](https://www.therobotreport.com/third-wave-automation-picks-series-c-funding-automated-forklifts/)
    - **Employees:** ~100
    - **Why sim / synthetic data:** High-reach pallet handling at
      height is risky to train and test on real racking; simulated
      warehouses with varied rack geometries, pallet conditions, and
      lighting — and synthetic pallet-pocket detection data — directly
      de-risk their autonomy stack.

28. **Slip Robotics** — Atlanta, USA
    - **What they do:** SlipBots — robots that ride inside trailers and
      auto-load/unload palletized freight in about five minutes;
      customers include John Deere, GE Appliances, and Nissan.
    - **Website:** https://www.sliprobotics.com
    - **Valuation:** undisclosed; raised ~$45M total
    - **Last raise:** ~$28M Series B led by DCVC (December 2024) —
      [Slip Robotics snags $28M for its bots that can load a truck in five minutes](https://techcrunch.com/2024/12/17/slip-robotics-snags-28m-for-its-bots-that-can-load-a-truck-in-five-minutes/)
    - **Employees:** ~70
    - **Why sim / synthetic data:** SlipBots navigate cluttered docks
      and trailer interiors with no infrastructure changes; simulating
      dock/trailer variability (ramps, gaps, freight configurations)
      and generating synthetic sensor data is far cheaper than staging
      real trucks for every edge case.

29. **Gather AI** — Pittsburgh, USA
    - **What they do:** Autonomous drones and fixed cameras with AI
      that scan warehouse inventory, predict stockouts, and flag
      misplaced pallets; customers include GEODIS and NFI.
    - **Website:** https://www.gather.ai
    - **Valuation:** undisclosed; raised ~$74M total
    - **Last raise:** ~$40M Series B led by Smith Point Capital
      (February 2026) —
      [Gather AI, maker of 'curious' warehouse drones, lands $40M](https://techcrunch.com/2026/02/09/gather-ai-maker-of-curious-warehouse-drones-lands-40m-led-by-keith-blocks-firm/)
    - **Employees:** ~70
    - **Why sim / synthetic data:** Their drones fly GPS-denied aisles
      and their vision models must read barcodes/labels across endless
      rack, lighting, and packaging variations — synthetic rendered
      rack imagery and simulated flight environments accelerate both
      autonomy testing and recognition-model training.

30. **Brightpick** — Bratislava, Slovakia
    - **What they do:** Autopicker mobile robots that drive warehouse
      aisles and pick e-commerce orders with an onboard arm, enabling
      "lights-out" fulfillment; 300+ robots deployed in the US and
      Europe.
    - **Website:** https://brightpick.ai
    - **Valuation:** undisclosed; raised ~$47M total
    - **Last raise:** ~$12M equity + debt round (November 2024) —
      [Brightpick brings in $12M to deploy more mobile picking robots in the U.S.](https://www.therobotreport.com/brightpick-brings-in-12m-to-deploy-more-mobile-robots-in-the-u-s/)
    - **Employees:** ~200
    - **Why sim / synthetic data:** Autopicker combines fleet
      navigation with AI grasping of arbitrary retail SKUs in totes —
      synthetic 3D item data for grasp training plus full-warehouse
      simulation for fleet throughput and in-motion picking validation
      are both squarely on their roadmap.

31. **Contoro Robotics** — Austin, USA
    - **What they do:** AI-powered robots that unload floor-loaded
      trailers and containers, with a human-in-the-loop teleoperation
      fallback and pay-per-container pricing; backed by Doosan,
      Coupang, and Amazon.
    - **Website:** https://www.contoro.com
    - **Valuation:** undisclosed; raised ~$22M total
    - **Last raise:** ~$12M Series A (March 2025) —
      [Contoro Robotics raises $12M to scale AI-powered trailer unloading](https://www.freightwaves.com/news/contoro-robotics-raises-12m-to-scale-ai-powered-trailer-unloading)
    - **Employees:** ~40
    - **Why sim / synthetic data:** Contoro trains customer-specific AI
      models to hit 99% unload success — synthetic container scenes
      covering each customer's box mix, shifted loads, and damaged
      packaging would shrink the per-customer model ramp.

32. **Anyware Robotics** — Fremont, USA
    - **What they do:** Pixmo, a mobile robot combining an AMR base,
      cobot arm, and 3D vision that unloads containers and trucks;
      first disclosed customer is Western Post US.
    - **Website:** https://anyware-robotics.com
    - **Valuation:** undisclosed; raised ~$17M total
    - **Last raise:** ~$12M seed led by GFT Ventures (March 2025) —
      [Anyware Robotics picks up $12M seed funding to automate container unloading](https://www.therobotreport.com/anyware-robotics-picks-up-12m-seed-funding-to-automate-container-unloading/)
    - **Employees:** ~30
    - **Why sim / synthetic data:** A small team shipping a
      perception-heavy unloading robot can't afford large real-world
      data ops — simulated trailer interiors and synthetic 3D
      box-detection datasets are the fastest path to robust picking
      across new freight types, and a natural fit for outside help.

---

## 3. Agriculture, construction & energy (field robotics)

Unstructured outdoor environments: perception models here must cope
with crop variation, weather, dust, and lighting — classic synthetic-
data territory, and field testing is slow and seasonal.

33. **Carbon Robotics** — Seattle, USA
    - **What they do:** Builds the LaserWeeder, a tractor-pulled robot
      that uses computer vision and 30 CO2 lasers to identify and kill
      weeds plant-by-plant without herbicides.
    - **Website:** https://carbonrobotics.com
    - **Valuation:** undisclosed; raised ~$177M total
    - **Last raise:** ~$70M Series D (October 2024), plus a ~$20M
      extension in June 2025 —
      [Carbon Robotics brings in $70M to scale LaserWeeder](https://www.therobotreport.com/carbon-robotics-brings-in-70m-to-scale-laserweeder/)
    - **Employees:** ~200
    - **Why sim / synthetic data:** Their models must distinguish crops
      from weeds at millimeter accuracy across 100+ crop types, growth
      stages, soils, and lighting conditions — synthetic crop/weed
      imagery is far cheaper than collecting labeled field data for
      every new crop and region they expand into.

34. **Ecorobotix** — Yverdon-les-Bains, Switzerland
    - **What they do:** Makes the ARA ultra-high-precision sprayer that
      scans fields and applies herbicide/fertilizer plant-by-plant,
      cutting chemical use by ~70–95%.
    - **Website:** https://ecorobotix.com
    - **Valuation:** undisclosed; raised ~$150M+ total
    - **Last raise:** ~$105M Series D (October 2025) —
      [Ecorobotix doubles down on AI software for precision spraying after $150m raise](https://agfundernews.com/ecorobotix-doubles-down-on-ai-software-for-precision-spraying-after-150m-raise)
    - **Employees:** ~250
    - **Why sim / synthetic data:** Plant-by-plant AI needs per-species
      detection models for every new crop/weed pair and geography;
      synthetic data covering plant variation, occlusion, and lighting
      would shorten the months-long data-collection cycle for each new
      crop algorithm they sell.

35. **Bonsai Robotics** — San Jose, USA
    - **What they do:** Sells vision-based "physical AI" autonomy kits
      that make OEM orchard equipment (e.g., nut harvesters) drive
      itself in GPS-denied, dusty orchards.
    - **Website:** https://www.bonsairobotics.ai
    - **Valuation:** undisclosed; raised ~$25M total
    - **Last raise:** ~$15M Series A (January 2025) —
      [Bonsai Robotics raises Series A funding for vision-based agricultural autonomy](https://www.therobotreport.com/bonsai-robotics-raises-series-a-funding-vision-based-agricultural-autonomy/)
    - **Employees:** ~35
    - **Why sim / synthetic data:** Camera-only autonomy must handle
      dust clouds, darkness, debris, and canopy occlusion where GPS
      fails — conditions that are dangerous and slow to capture on
      real harvesters; simulated orchards with weather/dust variation
      would de-risk testing and expand their training set.

36. **Agtonomy** — South San Francisco, USA
    - **What they do:** Software-defined autonomy platform that OEM
      partners (Kubota, Bobcat) embed to turn tractors and
      land-maintenance vehicles into supervised autonomous fleets for
      vineyards and orchards.
    - **Website:** https://www.agtonomy.com
    - **Valuation:** undisclosed; raised ~$64M total
    - **Last raise:** ~$18M Series B (October 2025) —
      [Agtonomy bags $18m to bring more AI to agricultural equipment](https://agfundernews.com/agtonomy-bags-18m-to-bring-more-ai-to-the-next-frontier-of-automation-agricultural-equipment)
    - **Employees:** ~60
    - **Why sim / synthetic data:** A software autonomy company
      integrating with multiple OEM vehicle platforms needs
      vehicle-in-the-loop simulation to validate each integration,
      plus perception data across vineyard/orchard row geometries,
      seasons, and the new verticals it is expanding into.

37. **Bedrock Robotics** — San Francisco, USA
    - **What they do:** Founded by ex-Waymo engineers; retrofits
      excavators and other heavy construction machinery with sensors
      and AI for fully operator-less earthmoving.
    - **Website:** https://www.bedrockrobotics.com
    - **Valuation:** ~$1.75B (as of February 2026)
    - **Last raise:** ~$270M Series B (February 2026) —
      [Bedrock Robotics raises $270M in red-hot AI sector](https://www.constructiondive.com/news/bedrock-robotics-raise-ai-automation-funding/811982/)
    - **Employees:** ~130
    - **Why sim / synthetic data:** Operator-less excavation on live
      jobsites demands Waymo-style simulation rigor — digital twins of
      dig sites with varied terrain, soil interaction, dust, and
      worker/equipment encounters to rack up validation miles that
      would be unsafe and slow to accumulate on real sites.

38. **Charge Robotics** — San Francisco Bay Area, USA
    - **What they do:** MIT spinout whose portable robotic "field
      factories" automatically assemble solar tracker sections and
      place them on utility-scale solar sites.
    - **Website:** https://chargerobotics.com
    - **Valuation:** undisclosed; raised ~$30M total
    - **Last raise:** ~$22M Series B (March 2025) —
      [MIT-based startup launches solar construction robotics system](https://pv-magazine-usa.com/2025/03/17/mit-based-startup-launches-solar-construction-robotics-system/)
    - **Employees:** ~40
    - **Why sim / synthetic data:** Each solar site has different
      racking hardware, ground undulation, and sun/glare conditions;
      simulating assembly sequences and generating synthetic imagery
      of tracker components in outdoor lighting would let them
      validate new hardware SKUs and site layouts before mobilizing.

39. **Infravision** — Austin, USA
    - **What they do:** Heavy-lift drone and intelligent
      ground-equipment system (TX System) that strings and
      reconductors high-voltage power lines without helicopters or
      extensive ground crews.
    - **Website:** https://www.infravisioninc.com
    - **Valuation:** undisclosed; raised ~$115M total
    - **Last raise:** ~$91M Series B (November 2025) —
      [Aerial Robotics Startup Infravision Raises $91M Series B](https://news.crunchbase.com/venture/aerial-robotics-startup-infravision-seriesb/)
    - **Employees:** ~120
    - **Why sim / synthetic data:** Drone stringing near energized
      lines happens in wind, variable terrain, and complex tower
      geometries; flight-dynamics simulation plus synthetic data for
      detecting conductors, towers, and obstacles under varied weather
      would support automation without risking grid assets.

40. **Xpanner** — Los Angeles area, USA
    - **What they do:** Retrofits customers' existing construction
      equipment with its X1 Kit hardware/software for autonomous
      operation, sold as an "Automation-as-a-Service" subscription.
    - **Website:** https://xpanner.com
    - **Valuation:** undisclosed; raised ~$38M total
    - **Last raise:** ~$18M Series B bridge (May 2026) —
      [Xpanner Lands $18M To Offer 'Automation As A Service' To Construction Sites](https://news.crunchbase.com/real-estate-property-tech/xpanner-automation-as-a-service-for-construction-sites-startup-funding-physical-ai-robotics/)
    - **Employees:** ~60
    - **Why sim / synthetic data:** Retrofitting many makes/models of
      equipment means re-validating perception and control per machine
      on varied jobsite terrain; per-model simulation and synthetic
      jobsite perception data (grades, spoil piles, workers, dust)
      would scale their integration pipeline faster than field testing.

41. **All3** — London, UK
    - **What they do:** Combines an AI architecture platform, robotic
      off-site factories, and "Mantis," an autonomous legged robot
      that assembles building structures on active construction sites.
    - **Website:** https://all3.com
    - **Valuation:** undisclosed; raised ~$25M+ total
    - **Last raise:** ~$25M seed (April 2026) —
      [All3 raises $25m to automate construction with legged robots](https://thenextweb.com/news/all3-25m-seed-construction-robots-ai-housing)
    - **Employees:** ~50
    - **Why sim / synthetic data:** A legged robot assembling
      components on partially built structures faces constantly
      changing geometry, clutter, and outdoor lighting; simulated
      construction-site environments are essential for training
      locomotion/manipulation policies before first commercial
      deployments.

42. **AgriPass Robotics** — Israel
    - **What they do:** Develops autonomous robotic weeding systems
      that mechanically remove weeds to help farmers cut herbicide use
      and improve yields.
    - **Website:** https://www.agripass-robotics.com
    - **Valuation:** undisclosed; raised ~$7.5M+ total
    - **Last raise:** ~$7.5M seed (March 2026) —
      [Robotic weeding start-up AgriPass raises $7.5m seed round](https://www.agtechnavigator.com/Article/2026/03/05/weed-management-how-this-startup-is-helping-farmers-improve-yields/)
    - **Employees:** ~15
    - **Why sim / synthetic data:** An early-stage weeding company must
      build crop-vs-weed detection for each target crop with a small
      team; synthetic plant imagery spanning species, growth stages,
      and field lighting is the cheapest way to bootstrap perception
      before they have large real-world datasets.

43. **Tevel Aerobotics Technologies** — Gedera, Israel
    - **What they do:** Tethered flying autonomous robots that pick
      tree fruit — locating, grading ripeness, and harvesting apples
      and stone fruit around the clock.
    - **Website:** https://www.tevel-tech.com
    - **Valuation:** undisclosed; raised ~$50M total
    - **Last raise:** ~$18M Series C (March 2026) —
      [Tevel raises $18m for autonomous fruit harvesting robots](https://www.fruitnet.com/eurofruit/tevel-secures-funding-for-flying-robot-harvesters/271009.article)
    - **Employees:** ~100
    - **Why sim / synthetic data:** Detecting and grading fruit within
      dense, wind-moved canopies under harsh sun/shadow contrast is a
      textbook synthetic-data problem — rendered orchards with fruit
      occlusion, ripeness variation, and lighting sweeps would expand
      coverage to new fruit varieties far faster than waiting for each
      harvest season.

44. **FarmDroid** — Vejen, Denmark
    - **What they do:** Solar-powered field robot (FD20) that both
      seeds and mechanically weeds row crops like sugar beets and
      onions, using GPS positioning of each seed.
    - **Website:** https://farmdroid.com
    - **Valuation:** undisclosed; raised ~€10.5M (~$11M) in this round
    - **Last raise:** ~€10.5M growth round (October 2024) —
      [Danish agtech FarmDroid secures €10.5 million for its autonomous, solar-powered agricultural robot](https://www.eu-startups.com/2024/10/danish-agtech-farmdroid-secures-e10-5-million-for-its-autonomous-solar-powered-agricultural-robot/)
    - **Employees:** ~75
    - **Why sim / synthetic data:** Expansion into conventional farming
      requires adding camera-based weed recognition beyond GPS
      seed-mapping; synthetic crop/weed datasets across new crops and
      European field conditions would accelerate that vision
      capability with limited in-house AI resources.

45. **Naïo Technologies** — Toulouse, France
    - **What they do:** Manufactures autonomous weeding robots (Oz,
      Ted, Orio) for vegetable farms and vineyards, with hundreds of
      units deployed worldwide.
    - **Website:** https://www.naio-technologies.com
    - **Valuation:** undisclosed; raised ~$55M total
    - **Last raise:** ~€6.4M (~$7M) relaunch financing
      (November 2025) —
      [How Naïo Technologies plots its comeback](https://www.agtechnavigator.com/Article/2025/11/11/how-naio-technologies-plots-its-comeback/)
    - **Employees:** ~50
    - **Why sim / synthetic data:** Post-restructuring with a leaner
      team, Naïo needs cost-efficient ways to improve camera-based row
      following and weed detection across many vegetable crops;
      simulation and synthetic data substitute for the large
      field-trial programs it can no longer afford.

46. **TRIC Robotics** — San Luis Obispo, USA
    - **What they do:** Operates tractor-sized autonomous robots that
      treat strawberry fields overnight with UV-C light and vacuums to
      kill pests and pathogens without chemicals, sold as a service.
    - **Website:** https://www.tricrobotics.com
    - **Valuation:** undisclosed; raised ~$10M total
    - **Last raise:** ~$5.5M seed (July 2025) —
      [How TRIC Robotics is reducing pesticide use on strawberries using UV light](https://techcrunch.com/2025/07/23/how-tric-robotics-is-reducing-pesticide-use-on-strawberries-using-uv-light/)
    - **Employees:** ~25
    - **Why sim / synthetic data:** Its robots navigate strawberry beds
      autonomously at night and plan to expand to new crops; simulated
      fields and synthetic low-light imagery of beds, rows, and
      obstacles would validate navigation and coverage logic for each
      new crop without burning scarce robot-hours.

47. **AirForestry** — Uppsala, Sweden
    - **What they do:** Develops heavy-lift electric drones that thin
      forests from the air — autonomously selecting, gripping,
      cutting, and extracting whole trees without ground machinery
      damaging the soil.
    - **Website:** https://airforestry.com
    - **Valuation:** undisclosed; raised ~$15.5M total
    - **Last raise:** ~€10.3M (~$11M) seed (October 2024) —
      [AirForestry bags €10.3M for drone-based tree harvesting tech](https://siliconcanals.com/swedens-airforestry-bags-e10-3m/)
    - **Employees:** ~35
    - **Why sim / synthetic data:** Autonomous tree selection and
      aerial harvesting require perceiving individual stems, branches,
      and canopy gaps in dense forest under wind and variable light —
      real test flights are slow and high-risk, so simulated forests
      and synthetic LiDAR/camera data are the practical path.

---

## 4. Medical, surgical & lab automation

Real procedure data is scarce, regulated, and privacy-bound — synthetic
imagery and procedure simulation are often the only way to train and
validate before clinical use.

48. **CMR Surgical** — Cambridge, UK
    - **What they do:** Maker of Versius, a modular soft-tissue
      surgical robot and the second-most-adopted soft-tissue system
      worldwide.
    - **Website:** https://cmrsurgical.com
    - **Valuation:** ~$3–4B (2021 round valued it ~$3B; a ~$4B sale
      process was reported — re-check)
    - **Last raise:** ~$200M+ equity and debt round (April 2025) —
      [CMR Surgical raises $200M to expand Versius robot access across the U.S.](https://www.therobotreport.com/cmr-surgical-raises-over-200m-expand-versius-robot-access/)
    - **Employees:** ~800
    - **Why sim / synthetic data:** Scaling Versius to thousands of new
      surgeons and US hospitals means heavy investment in surgeon
      training simulators and synthetic data to train
      instrument-tracking and scene-understanding models across varied
      anatomies.

49. **Distalmotion** — Lausanne, Switzerland
    - **What they do:** Maker of Dexter, a soft-tissue surgical robot
      aimed at hospitals and ambulatory surgical centers, cleared in
      the US for hernia, gallbladder, and hysterectomy procedures.
    - **Website:** https://www.distalmotion.com
    - **Valuation:** undisclosed (as of November 2025)
    - **Last raise:** ~$150M Series G (November 2025) —
      [Distalmotion raises $150M to accelerate U.S. adoption of DEXTER surgical robot](https://www.therobotreport.com/distalmotion-raises-150m-accelerate-u-s-dexter-surgical-robot-adoption/)
    - **Employees:** ~250
    - **Why sim / synthetic data:** A US commercial ramp across many
      surgeons and procedure types depends on scalable training
      simulators and synthetic surgical imagery to train and de-risk
      instrument tracking and scene understanding.

50. **ForSight Robotics** — Yokneam, Israel
    - **What they do:** Building the ORYOM robotic platform for
      cataract and other eye surgery, using computer vision and
      micromechanics to automate delicate ophthalmic procedures.
    - **Website:** https://forsightrobotics.com
    - **Valuation:** undisclosed; raised ~$195M total
    - **Last raise:** ~$125M Series B (June 2025) —
      [ForSight Robotics raises $125M to trial cataract eye surgery platform](https://www.fiercebiotech.com/medtech/forsight-robotics-raises-125m-trial-cataract-eye-surgery-platform)
    - **Employees:** ~100
    - **Why sim / synthetic data:** Sub-millimeter eye surgery needs
      vast labeled imagery of the anterior eye and procedure
      simulation; real surgical video is scarce and privacy-bound, so
      synthetic ophthalmic scenes and a procedure twin directly feed
      their AI vision and motion algorithms.

51. **Capstan Medical** — Santa Cruz, USA
    - **What they do:** Developing structural-heart implants
      (mitral/aortic valves) delivered by a catheter-based robotic
      system for minimally invasive valve replacement.
    - **Website:** https://capstanmedical.com
    - **Valuation:** undisclosed; raised ~$150M+ total
    - **Last raise:** ~$110M Series C (January 2025) —
      [Capstan Medical raises $110M for heart valve with robotic system](https://www.medtechdive.com/news/Capstan-Medical-funding-round-heart-valve-robot/735404/)
    - **Employees:** ~80
    - **Why sim / synthetic data:** Robotic transcatheter valve
      delivery inside a beating heart is extremely hard to test on
      real patients; simulated cardiac anatomy and synthetic
      fluoroscopic/ultrasound imagery let them train navigation and
      validate the robot before first-in-human procedures.

52. **Surgerii Robotics** — Beijing, China
    - **What they do:** Makes the SHURUI single-port endoscopic
      surgical robot for urologic, gynecologic, general, and thoracic
      procedures.
    - **Website:** https://en.surgerii.com
    - **Valuation:** undisclosed (as of December 2025)
    - **Last raise:** ~$100M Series D (December 2025) —
      [Surgerii Robotics raises $100M to fund global expansion](https://www.medtechdive.com/news/Surgerii-Robotics-raises-100M-fund-global-expansion/809056/)
    - **Employees:** ~200+
    - **Why sim / synthetic data:** Single-port systems cram multiple
      instruments through one channel, creating tight motion-planning
      and collision-avoidance challenges that are ideal to rehearse in
      simulation and to train perception models on synthetic
      endoscopic imagery.

53. **Ronovo Surgical** — Shanghai, China
    - **What they do:** Makes Carina, a modular laparoscopic surgical
      robot configurable across general surgery, gynecology, urology,
      and thoracic procedures.
    - **Website:** https://ronovosurgical.com
    - **Valuation:** undisclosed; raised ~$100M+ across 2025 rounds
    - **Last raise:** ~$67M Series D (September 2025) —
      [Ronovo Surgical raises $67M for modular laparoscopic robot with J&J backing](https://www.fiercebiotech.com/medtech/ronovo-surgical-raises-67m-modular-laparoscopic-robot-jj-backing)
    - **Employees:** ~150
    - **Why sim / synthetic data:** A modular system reconfigured per
      specialty multiplies the motion-planning and collision scenarios
      to validate, and training surgical-vision models across four
      specialties benefits from synthetic endoscopic imagery plus a
      procedure twin.

54. **XCath** — Houston, USA
    - **What they do:** Develops a neuro-endovascular surgical robot
      that steers catheters and guidewires through blood vessels to
      treat strokes and aneurysms remotely.
    - **Website:** https://www.xcath.com
    - **Valuation:** undisclosed; raised ~$92M total
    - **Last raise:** ~$30M Series C (March 2026) —
      [XCath Secures $30 Million Series C to Improve Global Outcomes in Neurovascular Care](https://www.businesswire.com/news/home/20260312760700/en/XCath-Secures-$30-Million-Series-C-to-Improve-Global-Outcomes-in-Neurovascular-Care)
    - **Employees:** ~50
    - **Why sim / synthetic data:** Endovascular navigation through
      patient-specific vasculature is hard to train on real human
      data; synthetic vessel anatomies and simulated catheter-tissue
      interaction would let them build perception/control models and
      validate steering before clinical use.

55. **Robeauté** — Paris, France
    - **What they do:** Developing a rice-grain-sized self-propelled
      neurosurgical microrobot that travels through the brain to take
      biopsies and deliver therapy.
    - **Website:** https://www.robeaute.com
    - **Valuation:** undisclosed; raised ~$28M in this round
    - **Last raise:** ~$28M Series A (January 2025) —
      [Robeauté raises $28M for neurosurgical microrobots](https://tech.eu/2025/01/14/robeaute-raises-28m-for-neurosurgical-microrobots-a-new-era-in-neurology/)
    - **Employees:** ~40
    - **Why sim / synthetic data:** Path-planning a microrobot through
      brain tissue is impossible to iterate on in real patients;
      physics-based brain simulation and synthetic neuro-imaging are
      essential to develop and validate navigation before human
      trials.

56. **Petal Surgical** — Bay Area, USA
    - **What they do:** Emerged from stealth developing an
      "incisionless" surgical system combining acoustic liquefaction,
      AI, and robotics to operate without cutting.
    - **Website:** https://www.petalsurgical.com
    - **Valuation:** undisclosed; raised ~$20M total
    - **Last raise:** ~$10M Series A (2025) —
      [Incisionless surgical robotic tech startup Petal Surgical emerges from stealth with $10M Series A](https://www.massdevice.com/petal-surgical-raises-10m-series-a/)
    - **Employees:** ~20
    - **Why sim / synthetic data:** An early-stage startup pioneering a
      novel modality has essentially no real-world procedure data —
      simulation environments and synthetic imagery are the only
      practical way to develop perception and control before clinical
      access.

57. **Vitestro** — Amsterdam, Netherlands
    - **What they do:** Makes Aletta, an autonomous robotic
      blood-drawing (phlebotomy) device that uses imaging and AI to
      find a vein and insert the needle.
    - **Website:** https://vitestro.com
    - **Valuation:** undisclosed; raised ~$120M+ total
    - **Last raise:** ~$70M Series B (March 2026) —
      [Vitestro raises $70M to ready blood collection robot for US launch](https://www.medtechdive.com/news/vitestro-raises-70m-to-ready-blood-collection-robot-for-us-launch/814396/)
    - **Employees:** ~70
    - **Why sim / synthetic data:** Autonomous needle insertion needs
      huge volumes of vein-imaging data across diverse skin tones,
      ages, and anatomies — exactly the kind of rare, regulated
      imagery best supplemented with synthetic vein/arm datasets and
      simulated insertion scenarios.

58. **Mendaera** — San Mateo, USA
    - **What they do:** Makes Focalist, a handheld robotic system that
      clips onto an ultrasound probe to guide precise needle placement
      across many specialties.
    - **Website:** https://www.mendaera.com
    - **Valuation:** undisclosed; raised ~$90M+ total
    - **Last raise:** ~$73M Series B (September 2024) —
      [Mendaera Closes $73M Series B Financing to Scale Robotics and AI](https://www.businesswire.com/news/home/20240926902349/en/Mendaera-Closes-$73M-Series-B-Financing-to-Scale-Robotics-and-AI-Across-Mainstream-Medical-Procedures)
    - **Employees:** ~60
    - **Why sim / synthetic data:** Their AI must interpret live
      ultrasound to guide a needle to a target; synthetic ultrasound
      imagery and simulated needle-tissue dynamics are valuable
      because real labeled ultrasound is noisy, scarce, and
      operator-dependent.

59. **Cellares** — South San Francisco, USA
    - **What they do:** Builds the Cell Shuttle, a fully automated
      robotic factory-in-a-box that manufactures cell therapies,
      replacing manual GMP lab work.
    - **Website:** https://www.cellares.com
    - **Valuation:** undisclosed; raised ~$612M total
    - **Last raise:** ~$257M Series D (January 2026) —
      [Cellares Raises $257 Million Series D Led by BlackRock and Eclipse](https://www.businesswire.com/news/home/20260128817422/en/Cellares-Raises-$257-Million-Series-D-Led-by-BlackRock-and-Eclipse-to-Industrialize-Global-Cell-Therapy-Manufacturing)
    - **Employees:** ~350
    - **Why sim / synthetic data:** Orchestrating many robotic arms and
      fluidics in a closed cell-therapy factory benefits from
      simulating the whole automated workflow and generating synthetic
      vision data for labware handling, liquid handling, and error
      recovery.

60. **Automata** — London, UK
    - **What they do:** Builds robotic-arm-based lab automation ("the
      operating system for AI-ready labs") that runs life-science
      workflows for pharma and biotech.
    - **Website:** https://www.automata.tech
    - **Valuation:** undisclosed (as of January 2026)
    - **Last raise:** ~$45M Series C (January 2026) —
      [Automata Raises $45M Series C to Build the Operating System for AI-Ready Labs](https://www.businesswire.com/news/home/20260129548625/en/Automata-Raises-$45M-Series-C-to-Build-the-Operating-System-for-AI-Ready-Labs)
    - **Employees:** ~150
    - **Why sim / synthetic data:** Coordinating robotic arms across
      varied labware and bench layouts is well suited to digital-twin
      simulation, and synthetic vision data helps train reliable
      labware/plate detection and pick-and-place across countless lab
      configurations.

---

## 5. Drones, maritime, inspection & defense

Rare, dangerous, or contested scenarios (GPS-denied flight, swarms,
storms, defects) that can't be tested at scale in the real world.

61. **Skydio** — San Mateo, USA
    - **What they do:** America's largest drone manufacturer, building
      autonomous quadcopters and drone-in-a-box docks for public
      safety, defense, and infrastructure inspection, relying on
      onboard vision-based autonomy rather than GPS.
    - **Website:** https://www.skydio.com
    - **Valuation:** ~$4.4B (as of April 2026 Series F)
    - **Last raise:** ~$110M Series F (April 2026) —
      [Skydio Raises $110M Series F, Signals Strong Revenue and U.S. Manufacturing Push](https://dronelife.com/2026/04/28/skydio-series-f-110m-funding-us-manufacturing/)
    - **Employees:** ~700–800
    - **Why sim / synthetic data:** Their core differentiator is visual
      (GPS-denied) navigation and obstacle avoidance, which demands
      massive volumes of diverse visual training data and
      high-fidelity simulated flight environments for rare scenarios
      (night, smoke, cluttered indoor spaces).

62. **BRINC Drones** — Seattle, USA
    - **What they do:** Builds 911-response and public-safety drones
      (Lemur, Responder) plus drone-in-a-box stations, deployed as
      first responders by police and emergency agencies.
    - **Website:** https://brincdrones.com
    - **Valuation:** undisclosed; raised ~$157M total
    - **Last raise:** ~$75M Series C (April 2025) —
      [A 25-year-old police drone founder just raised $75M led by Index](https://techcrunch.com/2025/04/08/a-25-year-old-police-drone-founder-just-raised-75m-led-by-index/)
    - **Employees:** ~150–200
    - **Why sim / synthetic data:** BRINC drones fly indoors through
      broken windows and dark buildings in emergencies — exactly the
      rare, dangerous scenarios (smoke-filled rooms, GPS-denied
      interiors) that can't be flown repeatedly in the real world and
      need simulated environments and synthetic perception data.

63. **Quantum Systems** — Gilching (Munich), Germany
    - **What they do:** Makes electric VTOL fixed-wing reconnaissance
      drones (Vector, Trinity) used by NATO militaries and Ukraine for
      intelligence, surveillance, and reconnaissance.
    - **Website:** https://quantum-systems.com
    - **Valuation:** ~€3B (~$3.3B) (as of November 2025)
    - **Last raise:** ~€180M Series C extension (November 2025) —
      [Quantum Systems passes €3 billion valuation with €180 million injection](https://www.eu-startups.com/2025/11/quantum-systems-passes-e3-billion-valuation-with-e180-million-injection-backing-its-nato-deployed-platforms/)
    - **Employees:** ~1,000
    - **Why sim / synthetic data:** Their ISR drones must operate in
      GPS-jammed, contested airspace and auto-detect vehicles/targets
      from the air; synthetic aerial imagery (varied terrain,
      camouflage, weather) and simulated GPS-denied flight testing
      directly accelerate their perception and navigation stack.

64. **Tekever** — Lisbon, Portugal
    - **What they do:** Builds medium-endurance autonomous surveillance
      drones (AR3, AR5) for maritime patrol and defense ISR, heavily
      used over Ukraine and by European coast guards.
    - **Website:** https://www.tekever.com
    - **Valuation:** ~£1B (~$1.25B) (as of May 2025)
    - **Last raise:** ~€70M growth round (May 2025) —
      [Portugal's dual-use drone startup Tekever raises €70M and joins the unicorn club](https://www.vestbee.com/insights/articles/tekever-secures-funding)
    - **Employees:** ~700
    - **Why sim / synthetic data:** Maritime ISR perception (small
      vessels, debris, people in water across sea states and sensor
      types) suffers from scarce real training data; synthetic ocean
      scenes and simulated long-endurance missions in jammed
      environments map directly to their product promises.

65. **Saildrone** — Alameda, USA
    - **What they do:** Builds wind- and solar-powered uncrewed surface
      vessels that patrol oceans for months, providing maritime domain
      awareness for navies and ocean data for science.
    - **Website:** https://www.saildrone.com
    - **Valuation:** ~$575M post-money (2024 Series C-1; later rounds
      undisclosed)
    - **Last raise:** ~$60M financing (May 2025), plus a $50M Lockheed
      Martin strategic investment (October 2025) —
      [Saildrone Bags $60M Investment for AI-Powered Maritime Security in Europe](https://thedefensepost.com/2025/05/21/saildrone-maritime-security-europe/)
    - **Employees:** ~250
    - **Why sim / synthetic data:** Their value is autonomous detection
      of dark vessels and threats at sea; rare events (smugglers,
      sabotage near subsea cables, extreme sea states) are nearly
      impossible to collect at scale, making synthetic radar/EO
      maritime data and simulated littoral environments a natural fit.

66. **HavocAI** — Rhode Island, USA
    - **What they do:** Builds small and medium autonomous surface
      vessels (drone boats) and the autonomy stack to run them in
      swarms for the US Navy and allies.
    - **Website:** https://www.havocai.com
    - **Valuation:** undisclosed; raised ~$100M total since January
      2024
    - **Last raise:** ~$85M venture round (October 2025) —
      [HavocAI obtains $85M to scale autonomous marine systems](https://www.therobotreport.com/havocai-obtains-85m-to-scale-autonomous-marine-systems/)
    - **Employees:** ~100–150
    - **Why sim / synthetic data:** Multi-vessel swarm coordination and
      collision avoidance in contested, GPS-denied waters can only be
      validated at scale in simulation; they also need synthetic
      maritime sensor data for target recognition across sea states
      they can't physically test.

67. **Blue Water Autonomy** — Boston, USA
    - **What they do:** Designs full-sized (100–150 ft) unmanned
      autonomous ships for the US Navy, built to cross oceans and stay
      at sea for months without crew.
    - **Website:** https://www.bluewaterautonomy.com
    - **Valuation:** undisclosed; raised ~$64M total
    - **Last raise:** ~$50M Series A (August 2025) —
      [Blue Water Autonomy nets $50M to build autonomous ships](https://www.therobotreport.com/blue-water-autonomy-nets-50m-to-build-autonomous-ships/)
    - **Employees:** ~50–70
    - **Why sim / synthetic data:** They get exactly one expensive
      first ship — virtually all autonomy validation (COLREGs
      compliance, storms, degraded-sensor and GPS-denied navigation
      over thousands of miles) must happen in simulated ocean
      environments before steel hits water.

68. **Gecko Robotics** — Pittsburgh, USA
    - **What they do:** Wall-climbing, flying, and swimming inspection
      robots that gather ultrasonic and visual data on critical
      infrastructure (power plants, ships, refineries), fed into their
      Cantilever AI platform.
    - **Website:** https://www.geckorobotics.com
    - **Valuation:** ~$1.25B (as of June 2025)
    - **Last raise:** ~$125M Series D (June 2025) —
      [Gecko Robotics raises $125 million surpassing billion-dollar valuation](https://www.cnbc.com/2025/06/12/gecko-robotics-raises-125-million-surpassing-billion-dollar-valuation.html)
    - **Employees:** ~350–900 (estimates vary widely)
    - **Why sim / synthetic data:** Their robots crawl boiler walls and
      ship hulls where every asset geometry is different; simulated
      digital twins of tanks/vessels and synthetic defect data
      (corrosion, cracks across materials) would speed both robot
      navigation testing and defect-detection model training.

69. **ANYbotics** — Zurich, Switzerland
    - **What they do:** Makes ANYmal, a four-legged autonomous
      inspection robot that patrols refineries, chemical plants,
      mines, and power stations, including an Ex-certified version for
      explosive atmospheres.
    - **Website:** https://www.anybotics.com
    - **Valuation:** undisclosed; raised ~$150M+ total
    - **Last raise:** ~$60M Series B extension (announced across
      December 2024–mid-2025), plus ~$20M with Climate Investment
      (September 2025) —
      [Swiss robotics developer ANYbotics raises over €127 million for its four-legged workforce](https://www.eu-startups.com/2025/09/swiss-robotics-developer-anybotics-raises-over-e127-million-for-its-four-legged-workforce/)
    - **Employees:** ~300–350
    - **Why sim / synthetic data:** Legged locomotion policies are
      trained almost entirely in simulation, and their inspection AI
      must recognize gauges, leaks, and anomalies across thousands of
      distinct plant layouts — synthetic plant environments and
      rare-anomaly data are core to scaling deployments.

70. **Voliro** — Zurich, Switzerland
    - **What they do:** Builds tilt-rotor contact drones that
      physically touch infrastructure (flare stacks, tanks, wind
      turbines) to perform non-destructive ultrasonic testing without
      scaffolding or rope access.
    - **Website:** https://voliro.com
    - **Valuation:** undisclosed; Series A totals ~$23M
    - **Last raise:** ~$23M Series A extension (June 2025) —
      [Voliro Raises $23M to Expand Aerial Robotics for Infrastructure Inspection](https://dronelife.com/2025/06/18/voliro-funding-23m-to-expand-aerial-robotics-for-infrastructure-inspection/)
    - **Employees:** ~70
    - **Why sim / synthetic data:** Their roadmap is explicitly toward
      full autonomy for contact-based inspection — flying a tilting
      drone into physical contact with curved steel in wind is a
      control and perception problem that demands high-fidelity
      aerodynamic/contact simulation and synthetic imagery of varied
      industrial assets.

71. **Aerones** — Riga, Latvia
    - **What they do:** Robotic systems that climb wind turbines to
      inspect, clean, and repair blades, roughly halving maintenance
      time versus human rope-access crews; AI processes the inspection
      data.
    - **Website:** https://aerones.com
    - **Valuation:** undisclosed; raised ~$120M+ total
    - **Last raise:** ~$62M growth round (June 2025) —
      [AI-driven robotic wind turbine maintenance firm Aerones raises $62M](https://siliconangle.com/2025/06/03/ai-driven-robotic-wind-turbine-maintenance-firm-aerones-raises-62m/)
    - **Employees:** ~300–400
    - **Why sim / synthetic data:** Blade-defect detection models
      (erosion, lightning damage, cracks) need far more labeled defect
      imagery than real inspections produce; synthetic blade-damage
      data plus simulated turbine environments for motion planning in
      wind would directly support their predictive-maintenance push.

72. **Square Robot** — Boston, USA
    - **What they do:** Submersible robots that inspect the floors of
      in-service fuel and chemical storage tanks while the tanks stay
      full and operational, eliminating confined-space human entry.
    - **Website:** https://squarerobot.com
    - **Valuation:** undisclosed; ~$13M Series B plus a December 2025
      extension with Marathon Petroleum
    - **Last raise:** ~$13M Series B (November 2024), extended
      December 2025 —
      [Square Robot raises new Series B funding and agrees collaboration with Marathon Petroleum](https://roboticsandautomationnews.com/2025/12/17/square-robot-raises-new-series-b-funding-and-agrees-collaboration-with-marathon-petroleum/)
    - **Employees:** ~50
    - **Why sim / synthetic data:** Their robots navigate
      zero-visibility, GPS-denied environments inside liquid-filled
      tanks using sonar — simulated tank environments and synthetic
      sonar data for floor-corrosion classification are far cheaper
      than gathering data inside live diesel tanks.

73. **Forterra** — Clarksburg, USA
    - **What they do:** Develops AutoDrive, a retrofit autonomous
      driving system that turns existing military and industrial
      ground vehicles (tactical trucks, terminal tractors) into
      uncrewed vehicles.
    - **Website:** https://www.forterra.com
    - **Valuation:** undisclosed; ~$75M Series B was 2.5x
      oversubscribed
    - **Last raise:** ~$75M Series B (September 2024) —
      [Forterra: Self-Driving Technology Company Raises $75 Million (Series B)](https://pulse2.com/forterra-self-driving-technology-company-raises-75-million-series-b/)
    - **Employees:** ~300–350
    - **Why sim / synthetic data:** Off-road military autonomy has no
      lane lines and few real-world miles to learn from — synthetic
      off-road terrain data, rare battlefield obstacle scenarios, and
      GPS-denied navigation testing in simulation are precisely what
      an autonomy retrofit company needs to certify across many
      vehicle types.

74. **Overland AI** — Seattle, USA
    - **What they do:** Builds off-road ground autonomy software (born
      from DARPA's RACER program) and the ULTRA UGV for US Army
      missions like contested logistics.
    - **Website:** https://www.overland.ai
    - **Valuation:** ~$850M post-money (as of February 2026)
    - **Last raise:** ~$100M Series B incl. ~$20M venture debt
      (February 2026) —
      [Overland AI raises $100M to scale autonomy with the U.S. armed forces](https://www.therobotreport.com/overland-ai-raises-100m-scale-autonomy-u-s-armed-forces/)
    - **Employees:** ~150
    - **Why sim / synthetic data:** Their entire product is GPS-denied,
      off-road navigation in unstructured terrain; scaling beyond
      DARPA testbeds requires simulated terrains (mud, dust,
      vegetation, night) and synthetic sensor data for terrain
      classification far beyond what physical testing miles supply.

75. **ARX Robotics** — Oberding (Munich), Germany
    - **What they do:** Builds the Gereon modular unmanned ground
      vehicles (logistics, casualty evacuation, recon) and Mithra OS
      autonomy software for European armed forces and Ukraine.
    - **Website:** https://www.arx-robotics.com
    - **Valuation:** undisclosed; raised ~€42M total Series A
    - **Last raise:** ~€31M Series A (April 2025) plus ~€11M extension
      (July 2025) —
      [German DefenseTech ARX Robotics reinforces Europe's battlefield edge with €42 million for tactical UGVs](https://www.eu-startups.com/2025/07/german-defensetech-arx-robotics-reinforces-europes-battlefield-edge-with-e42-million-for-tactical-ugvs/)
    - **Employees:** ~200
    - **Why sim / synthetic data:** Their UGVs must traverse
      battlefield terrain autonomously under GPS jamming, and Mithra
      OS aims to retrofit 50,000+ NATO vehicles — validating autonomy
      across that many platforms and terrain types is only feasible
      with simulation and synthetic off-road perception data.

76. **Scout AI** — Sunnyvale, USA
    - **What they do:** Builds Fury, a vision-language-action
      foundation model that gives defense robots (ground vehicles and
      drones) embodied autonomy in comms- and GPS-denied environments,
      plus its own robot testbeds.
    - **Website:** https://scoutco.ai
    - **Valuation:** undisclosed; raised ~$115M total
    - **Last raise:** ~$100M Series A (April 2026) —
      [Scout AI raises $100M to train its models for war](https://techcrunch.com/2026/04/29/coby-adcocks-scout-ai-raises-100-million-to-train-models-for-war-we-visited-its-bootcamp/)
    - **Employees:** ~70
    - **Why sim / synthetic data:** A VLA foundation model for defense
      robotics is bottlenecked on embodied training data — synthetic
      multi-domain scenario generation and simulation environments for
      rare combat-adjacent situations are arguably their single
      largest input cost.

77. **Fortem Technologies** — Pleasant Grove, USA
    - **What they do:** Counter-UAS company whose autonomous
      DroneHunter interceptor drone captures hostile drones with net
      guns, paired with TrueView radar and SkyDome command software.
    - **Website:** https://fortemtech.com
    - **Valuation:** undisclosed; raised well over $100M total
    - **Last raise:** ~$25M Series B initial tranche from Lockheed
      Martin (April 2026) —
      [Lockheed Martin Invests $25 Million in Fortem Technologies to Scale Counter-UAS Capability](https://insideunmannedsystems.com/lockheed-martin-invests-25-million-in-fortem-technologies-to-scale-counter-uas-capability/)
    - **Employees:** ~150
    - **Why sim / synthetic data:** Drone-on-drone interception of
      maneuvering targets (including swarms) cannot be safely or
      affordably tested at scale in real airspace — simulated
      engagement scenarios and synthetic radar/EO signatures of
      diverse drone types are central to training their autonomy.

78. **Asylon Robotics** — Norristown, USA
    - **What they do:** Robotic security-as-a-service combining
      autonomous patrol drones with battery-swap ground stations and
      DroneDog (a security-modified Boston Dynamics Spot), run through
      its Guardian command software.
    - **Website:** https://www.asylonrobotics.com
    - **Valuation:** undisclosed; raised ~$45M total
    - **Last raise:** ~$26M Series B (July 2025) —
      [Robot guard dogs help Asylon raise a $26M Series B](https://techcrunch.com/2025/07/22/robot-guard-dogs-help-asylon-raise-a-26m-series-b/)
    - **Employees:** ~100–120
    - **Why sim / synthetic data:** Perimeter-security perception
      (intruders, anomalies, gas leaks at night across varied sites)
      depends on rare-event detection where real positives are
      scarce — synthetic intruder/anomaly scenarios and per-site
      simulated environments would shorten every new deployment.

---

## 6. Service, delivery, consumer & recycling

Robots operating among people and infinite object variety — sidewalks,
kitchens, stores, and waste streams.

79. **Coco Robotics** — Los Angeles, USA
    - **What they do:** Operates a fleet of ~1,300 cooler-sized
      sidewalk delivery robots for restaurant and merchant deliveries
      via Uber Eats and DoorDash, with a data partnership feeding
      urban driving data to OpenAI.
    - **Website:** https://cocodelivery.com
    - **Valuation:** undisclosed; raised ~$110M+ total
    - **Last raise:** ~$80M strategic round (June 2025) —
      [Sam Altman-backed Coco Robotics raises $80M](https://techcrunch.com/2025/06/11/sam-altman-backed-coco-robotics-raises-80m/)
    - **Employees:** ~200–300
    - **Why sim / synthetic data:** Scaling from 1,300 to a planned
      10,000 robots means their sidewalk-navigation stack must handle
      pedestrians, dogs, curb cuts, and clutter in new cities before
      deployment — simulated pedestrian environments and synthetic
      edge-case data are far cheaper than collecting failures live.

80. **Starship Technologies** — San Francisco, USA (R&D in Tallinn)
    - **What they do:** The largest autonomous sidewalk delivery fleet
      in the world (~2,700 robots, 9M+ deliveries), operating Level 4
      autonomy on campuses and city sidewalks in seven countries.
    - **Website:** https://www.starship.xyz
    - **Valuation:** undisclosed; raised ~$280M+ total
    - **Last raise:** ~$50M Series C (October 2025) —
      [Starship Technologies obtains Series C for autonomous deliveries across the U.S.](https://www.therobotreport.com/starship-technologies-obtains-series-c-funding-for-autonomous-deliveries/)
    - **Employees:** ~300
    - **Why sim / synthetic data:** Plans to grow to 12,000+ robots in
      dense US cities — synthetic pedestrian, crosswalk, and
      weather-variation data plus city-scale sim environments would
      let them validate Level 4 sidewalk autonomy in new urban
      geographies before robots ship.

81. **Avride** — Austin, USA
    - **What they do:** Builds autonomous sidewalk delivery robots
      (live on Uber Eats in several US cities) and robotaxis sharing
      one autonomy stack; spun out of Yandex's self-driving group
      under Nebius.
    - **Website:** https://avride.ai
    - **Valuation:** undisclosed; strategic commitments of up to ~$375M
      from Uber and Nebius
    - **Last raise:** up to ~$375M strategic investment
      (October 2025) —
      [Uber, Nebius Commit Up to $375M to Avride for Robotaxis and Delivery Bots](https://theaiinsider.tech/2025/10/23/uber-nebius-commit-up-to-375m-to-avride-for-robotaxis-and-delivery-bots/)
    - **Employees:** ~400
    - **Why sim / synthetic data:** Running one perception stack across
      robotaxis and sidewalk bots in multiple new markets demands
      massive scenario coverage — synthetic pedestrian/traffic data
      and digital-twin city environments directly de-risk their
      expansion.

82. **Chef Robotics** — San Francisco, USA
    - **What they do:** AI-enabled robot arms that do high-mix food
      assembly (portioning, depositing ingredients) for food
      manufacturers under a robotics-as-a-service model; 100M+
      servings produced via its ChefOS physical-AI stack.
    - **Website:** https://www.chefrobotics.ai
    - **Valuation:** undisclosed; raised ~$65.6M total
    - **Last raise:** ~$43.1M Series A — $20.6M equity + $22.5M
      equipment financing (March 2025, Avataar-led) —
      [Chef Robotics raises $43m Series A to scale AI-enabled robotics in meal assembly](https://agfundernews.com/breaking-chef-robotics-raises-43m-series-a-to-scale-ai-enabled-robotics-in-meal-assembly)
    - **Employees:** ~60–70
    - **Why sim / synthetic data:** Manipulating deformable, visually
      variable food (rice, sauces, diced vegetables) is a data
      problem — synthetic food-item imagery and simulated
      scooping/portioning physics would let them onboard new
      ingredients and recipes without weeks of in-plant data
      collection.

83. **Botrista** — San Francisco, USA
    - **What they do:** Makes DrinkBot, a robotic beverage station that
      mixes craft drinks (boba, cold brew, smoothies) to order in ~20
      seconds for restaurant chains across 37+ US states.
    - **Website:** https://botrista.com
    - **Valuation:** undisclosed; raised ~$120M total
    - **Last raise:** ~$65M Series C led by Jollibee Foods
      (July 2024) —
      [Automated beverage system Botrista lands investment from Jollibee Foods](https://www.restaurantbusinessonline.com/technology/automated-beverage-system-botrista-lands-investment-jollibee-foods)
    - **Employees:** ~150
    - **Why sim / synthetic data:** Expanding into food-side automation
      and quality monitoring requires vision systems that recognize
      cups, fill levels, garnishes, and ingredient states across
      franchise environments — synthetic beverage/dispensing imagery
      beats collecting labeled data in thousands of restaurants.

84. **Posha** — San Francisco, USA
    - **What they do:** Sells a ~$1,750 countertop cooking robot that
      uses computer vision to autonomously cook full meals from a
      recipe library in consumer kitchens.
    - **Website:** https://posha.com
    - **Valuation:** undisclosed; raised ~$10M+ total
    - **Last raise:** ~$8M Series A led by Accel (May 2025) —
      [Meet Posha, a countertop robot that cooks your meals for you](https://techcrunch.com/2025/05/06/meet-posha-a-countertop-robot-that-cooks-your-meals-for-you/)
    - **Employees:** ~60
    - **Why sim / synthetic data:** Their vision system must judge
      doneness, ingredient identity, and quantity across wildly
      variable home ingredients and lighting — synthetic food-state
      image data (browning, boiling, sauce thickness) is the cheapest
      way to expand the recipe library.

85. **Glacier** — San Francisco, USA
    - **What they do:** Builds low-cost AI vision-guided robot arms
      that sort recyclables on recycling-facility conveyor lines,
      recognizing 30+ material categories; deployed in six+ US metros.
    - **Website:** https://endwaste.io
    - **Valuation:** undisclosed; raised ~$29M total
    - **Last raise:** ~$16M Series A with Amazon's Climate Pledge Fund
      (April 2025) —
      [Amazon-backed Glacier gets $16M to expand its robot recycling fleet](https://techcrunch.com/2025/04/28/amazon-backed-glacier-gets-16m-to-expand-its-robot-recycling-fleet/)
    - **Employees:** ~50
    - **Why sim / synthetic data:** Waste-stream object detection is a
      textbook synthetic-data problem — crushed, dirty, occluded
      packaging in infinite variation per facility — and synthetic
      conveyor-belt scenes would let Glacier add new material
      categories and deployments without months of manual labeling.

86. **AMP Robotics (AMP Sortation)** — Louisville, Colorado, USA
    - **What they do:** AI-powered robotic and optical sorting systems
      for recycling facilities (~400 robots deployed), now also
      building and operating full robot-run waste-sorting facilities.
    - **Website:** https://ampsortation.com
    - **Valuation:** undisclosed; raised ~$270M+ equity to date
    - **Last raise:** ~$91M Series D led by Congruent Ventures
      (December 2024) —
      [Amp Robotics raises $91M to build more robot-filled waste-sorting facilities](https://techcrunch.com/2024/12/05/amp-robotics-raises-91m-to-build-more-robot-filled-waste-sorting-facilities/)
    - **Employees:** ~300
    - **Why sim / synthetic data:** Whole facilities run on their
      perception of mixed municipal waste, where regional packaging
      and contamination differ per site — synthetic waste-stream data
      and simulated sortation lines would speed commissioning of each
      new facility and improve recall on rare materials.

87. **Simbe Robotics** — South San Francisco, USA
    - **What they do:** Makes Tally, an autonomous shelf-scanning robot
      that roams retail stores auditing inventory, pricing, and
      planogram compliance for grocers like Albertsons and Wakefern.
    - **Website:** https://www.simberobotics.com
    - **Valuation:** undisclosed; raised ~$100M+ total
    - **Last raise:** ~$50M Series C led by Goldman Sachs Growth Equity
      (October 2024) —
      [Goldman Sachs-backed Simbe Robotics raises $50M in Series C funding](https://fortune.com/2024/10/24/goldman-sachs-simbe-series-c-robot-business/)
    - **Employees:** ~180
    - **Why sim / synthetic data:** Tally must detect hundreds of
      thousands of SKUs, price tags, and out-of-stock gaps across
      every retail banner's unique shelving — synthetic store
      environments and rendered shelf/product imagery would slash
      per-retailer onboarding and improve detection of new packaging.

88. **Lucid Bots** — Charlotte, USA
    - **What they do:** Builds exterior-cleaning robots — the Sherpa
      window/facade-washing drone and the Lavo autonomous
      pressure-washing robot — sold to cleaning contractors, with
      ~1,000 units deployed.
    - **Website:** https://lucidbots.com
    - **Valuation:** undisclosed; raised ~$34M total
    - **Last raise:** ~$20M Series B (March 2026) —
      [Lucid Bots raises $20M to keep up with demand for its window-washing drones](https://techcrunch.com/2026/03/25/lucid-bots-raises-20m-to-keep-up-with-demand-for-its-window-washing-drones/)
    - **Employees:** ~70
    - **Why sim / synthetic data:** Drones and ground robots cleaning
      building facades must perceive glass, reflections, dirt levels,
      and obstacles — notoriously hard surfaces for vision — so
      synthetic facade/surface datasets and simulated building
      environments would accelerate the autonomy they're adding.

89. **Hullbot** — Sydney, Australia
    - **What they do:** Designs autonomous underwater robots that clean
      and inspect ship hulls to remove biofouling, cutting vessel fuel
      use 10–26%; 1,000+ paid cleans delivered.
    - **Website:** https://www.hullbot.com
    - **Valuation:** undisclosed; raised ~A$20M+ total
    - **Last raise:** ~A$16M (~US$10M) Series A (November 2025) —
      [Shipping climate tech startup Hullbot steams ahead with $16 million Series A](https://www.startupdaily.net/topic/funding/shipping-climate-tech-startup-hullbot-steams-ahead-with-16-million-series-a/)
    - **Employees:** ~40
    - **Why sim / synthetic data:** Underwater perception (turbidity,
      low light, biofouling textures on curved hulls) makes real data
      collection slow and expensive — simulated underwater
      environments and synthetic biofouling imagery would train
      navigation and inspection models for larger vessel classes.

90. **Beatbot** — Shenzhen, China
    - **What they do:** Makes premium AI-powered robotic pool cleaners
      (AquaSense line) that autonomously vacuum floors, walls, and
      waterlines and skim surfaces; sold globally direct-to-consumer.
    - **Website:** https://beatbot.com
    - **Valuation:** undisclosed; latest round ~RMB 1B (~$140M)
    - **Last raise:** ~$140M growth round led by Meituan's DragonBall
      Capital (September 2025) —
      [Beatbot secures funding from Meituan and co to take premium pool cleaning robots global](https://kr-asia.com/beatbot-secures-funding-from-meituan-and-co-to-take-premium-pool-cleaning-robots-global)
    - **Employees:** ~1,000
    - **Why sim / synthetic data:** Their cleaners rely on underwater
      vision and mapping across endlessly varied pool shapes,
      finishes, lighting, and debris — synthetic pool environments and
      debris datasets are far more practical than physically testing
      in thousands of pools.

---

## 7. More verified prospects (mixed sectors)

A final sweep across sectors to round out the list.

91. **Monarch Tractor** — Livermore, USA
    - **What they do:** Builds the MK-V, a fully electric,
      driver-optional autonomous tractor for vineyards, orchards, and
      dairies, plus the WingspanAI farm management platform.
    - **Website:** https://www.monarchtractor.com
    - **Valuation:** ~$500M+ (as of July 2024 Series C; the company
      hit financial turbulence and layoffs in 2025 — re-check)
    - **Last raise:** ~$133M Series C (July 2024) —
      [Monarch Tractor CEO says $133M raise will help it escape 'quite a challenging time'](https://techcrunch.com/2024/07/22/monarch-tractor-ceo-says-133m-raise-will-help-it-escape-quite-a-challenging-time/)
    - **Employees:** ~200–300 (reduced after 2025 layoffs)
    - **Why sim / synthetic data:** Driver-optional tractors must
      validate vision-based autonomy across endless crop-row,
      lighting, dust, and weather edge cases that are slow and costly
      to capture on real farms; simulated vineyards and synthetic
      agricultural imagery directly feed their perception stack.

92. **Burro (Augean Robotics)** — Philadelphia, USA
    - **What they do:** Makes autonomous "people-scale to pallet-scale"
      outdoor mobile robots that tow, haul, mow, and patrol in
      nurseries, vineyards, and orchards.
    - **Website:** https://burro.ai
    - **Valuation:** undisclosed; raised ~$54M total
    - **Last raise:** ~$24M Series B (January 2025) —
      [With a fresh $24m, Burro grows from 'people to pallet scale'](https://agfundernews.com/with-a-fresh-24m-burro-grows-from-people-to-pallet-scale-with-autonomous-harvest-assist-robots)
    - **Employees:** ~50
    - **Why sim / synthetic data:** Their robots navigate unstructured
      outdoor rows using vision; synthetic crop-row, foliage, and
      terrain data plus simulated farms would let them regression-test
      navigation across crops and seasons without burning fleet time
      in the field.

93. **Cartken** — Oakland, USA
    - **What they do:** Builds camera-based autonomous delivery robots,
      now pivoting from sidewalk food delivery to indoor/outdoor
      industrial material transport in factories and labs.
    - **Website:** https://www.cartken.com
    - **Valuation:** undisclosed; raised ~$22.5M total
    - **Last raise:** ~$10M round, bringing aggregate to ~$22.5M
      (July 2024) —
      [From burritos to biotech: How robotics startup Cartken found its AV niche](https://techcrunch.com/2024/07/03/from-burritos-to-biotech-how-robotics-startup-cartken-found-its-av-niche/)
    - **Employees:** ~50
    - **Why sim / synthetic data:** A camera-only (no lidar) autonomy
      stack moving between sidewalks, campuses, and factory floors
      needs huge labeled visual variety; simulated facilities and
      synthetic pedestrian/forklift interaction scenarios are a
      natural fit for safe policy testing.

94. **Ati Motors** — Bengaluru, India
    - **What they do:** Manufactures Sherpa autonomous mobile robots
      (tugs, pallet and bin movers) for factories, using a
      self-driving-car-style autonomy stack; deployed at 40+
      manufacturers including Hyundai and Forvia.
    - **Website:** https://www.atimotors.com
    - **Valuation:** undisclosed; raised ~$37M total
    - **Last raise:** ~$20M Series B (January 2025) —
      [Ati Motors Raises $20M Series B for Global Expansion](https://www.prnewswire.com/news-releases/ati-motors-raises-20m-series-b-for-global-expansion-of-its-ai-powered-robotics-workforce-302357446.html)
    - **Employees:** ~150
    - **Why sim / synthetic data:** Every new factory deployment means
      a new floor layout, traffic pattern, and sensor environment;
      digital twins of customer plants and synthetic lidar/camera data
      would shorten site commissioning and de-risk global expansion.

95. **Matic** — Mountain View, USA
    - **What they do:** Consumer home robot that vacuums and mops fully
      autonomously using five-plus RGB/IR cameras and on-device neural
      networks instead of lidar.
    - **Website:** https://maticrobots.com
    - **Valuation:** ~$650M (as of July 2025)
    - **Last raise:** ~$77.3M "Series A Prime" (July 2025) —
      [Matic funding, news & analysis](https://sacra.com/c/matic/)
    - **Employees:** ~50
    - **Why sim / synthetic data:** Camera-only indoor SLAM and
      dirt/object recognition must generalize across millions of
      unique homes; synthetic home interiors with varied flooring,
      lighting, clutter, and pets are the cheapest way to expand
      training coverage.

96. **Outrider** — Golden, USA
    - **What they do:** Automates distribution-yard operations with
      autonomous electric yard trucks that hitch trailers, move them
      between docks, and connect trailer brake lines — sold as a
      service to Fortune 500 logistics operators.
    - **Website:** https://www.outrider.ai
    - **Valuation:** undisclosed; raised ~$250M+ total
    - **Last raise:** ~$62M Series D (October/November 2024) —
      [Outrider Raises $62M to Expand Autonomous Yard Truck Services](https://www.supplychain247.com/article/outrider-raises-62-million-autonomous-yard-truck-services)
    - **Employees:** ~200
    - **Why sim / synthetic data:** Yard autonomy needs validated
      behavior around trailers, jockeying trucks, and human workers;
      digital-twin yards and synthetic trailer/coupler perception data
      let them prove safety cases and test rare events.

97. **Corvus Robotics** — Boston, USA
    - **What they do:** Fully autonomous, infrastructure-free indoor
      drones (Corvus One) that fly warehouse aisles scanning barcodes
      for inventory counts, including in lights-out facilities.
    - **Website:** https://www.corvus-robotics.com
    - **Valuation:** undisclosed; raised ~$23M total
    - **Last raise:** ~$18M Series A (October 2024) —
      [Corvus Robotics soars to new heights with Series A round for drone inventory](https://www.therobotreport.com/corvus-robotics-series-a-round-drone-inventory/)
    - **Employees:** ~30
    - **Why sim / synthetic data:** GPS-denied flight via an "AI world
      model" must handle every rack type, label, and lighting
      condition; simulated warehouses and synthetic barcode/rack
      imagery (including low-light) would scale their perception
      training far faster than customer site visits.

98. **Four Growers** — Pittsburgh, USA
    - **What they do:** Builds the GR-100, an AI-powered greenhouse
      robot that detects ripeness and harvests tomatoes (and now
      cucumbers) with ~98% pick accuracy.
    - **Website:** https://fourgrowers.com
    - **Valuation:** undisclosed; raised ~$15M+ total
    - **Last raise:** ~$9M Series A (November 2024) —
      [YC-backed Four Growers builds robots to help solve greenhouse labor shortages](https://techcrunch.com/2024/11/20/yc-backed-four-growers-builds-robots-to-help-solve-greenhouse-labor-shortages/)
    - **Employees:** ~25
    - **Why sim / synthetic data:** Harvesting under heavy occlusion
      demands training data spanning fruit ripeness, leaf cover, and
      trellis variation per crop; procedurally generated synthetic
      plants are the standard way to expand to new crops without
      months of greenhouse data collection.

99. **Neros** — El Segundo, USA
    - **What they do:** US manufacturer of low-cost FPV reconnaissance
      and strike drones (Archer line) and ground control systems for
      defense customers, with a China-free supply chain.
    - **Website:** https://neros.tech
    - **Valuation:** undisclosed; raised ~$120M+ total
    - **Last raise:** ~$75M Series B (November 2025) —
      [Drone maker Neros closes Series B round to expand industrial capacity](https://www.therobotreport.com/drone-maker-neros-raises-75m-expand-industrial-capacity/)
    - **Employees:** ~150
    - **Why sim / synthetic data:** FPV drones operating under
      electronic warfare and GPS denial need simulated flight
      environments for autonomy testing, synthetic target imagery for
      visual guidance, and sim-based operator training at scale.

100. **Deep Robotics** — Hangzhou, China
     - **What they do:** Maker of industrial quadruped robots (X- and
       Lynx-series "robot dogs") for power-station inspection,
       tunnels, and emergency response, now expanding into the DR02
       all-weather humanoid.
     - **Website:** https://www.deeprobotics.cn/en
     - **Valuation:** undisclosed; reportedly well under $5B
       (preparing a STAR Market IPO)
     - **Last raise:** ~$68–70M Series C (December 2025) —
       [Deep Robotics Secures $68M in Series C to Fuel Humanoid and 'Embodied AI' Push](https://www.humanoidsdaily.com/news/deep-robotics-secures-68m-in-series-c-to-fuel-humanoid-and-embodied-ai-push)
     - **Employees:** ~400
     - **Why sim / synthetic data:** Legged locomotion over stairs,
       rubble, and substation terrain is trained almost entirely via
       reinforcement learning in simulation; custom terrain
       environments and domain-randomized synthetic data are core
       inputs to their embodied-AI roadmap.

101. **LimX Dynamics** — Shenzhen, China
     - **What they do:** Develops modular and general-purpose humanoid
       robots and bipedal platforms (Oli, TRON series) aimed at
       logistics and industrial tasks, backed by JD.com.
     - **Website:** https://www.limxdynamics.com
     - **Valuation:** undisclosed; raised ~$296M total
     - **Last raise:** ~$200M Series B (February 2026) —
       [Chinese embodied AI startup LimX Dynamics raises $200m in Series B round](https://www.dealstreetasia.com/stories/limx-dynamics-series-b-round-471255)
     - **Employees:** ~300
     - **Why sim / synthetic data:** Humanoid whole-body control and
       manipulation skills are trained sim-first (RL plus sim-to-real
       transfer); purpose-built simulation environments and synthetic
       manipulation datasets are exactly the scaling bottleneck a
       $200M deployment push creates.

102. **Booster Robotics** — Beijing, China
     - **What they do:** Builds low-cost, durable humanoid robots (T1,
       K1) sold as development platforms for researchers and
       developers; its robots powered the 2025 RoboCup AdultSize
       champion team.
     - **Website:** https://www.booster.tech
     - **Valuation:** undisclosed; ~$14M Series A+ (RMB ~100M) plus
       earlier rounds
     - **Last raise:** ~$14M Series A+ (July 2025), following a
       Series A in June 2025 —
       [China's Booster Robotics Lands New Funding as it Hits a Winning Streak](https://www.caixinglobal.com/2025-07-25/chinas-booster-robotics-lands-new-funding-as-it-hits-a-winning-streak-102344904.html)
     - **Employees:** ~150
     - **Why sim / synthetic data:** As a developer-platform humanoid
       company, both Booster and its customer base need ready-made
       simulation environments, accurate robot models, and synthetic
       training data — a consultant can plug into their SDK/ecosystem
       play directly.

103. **EngineAI** — Shenzhen, China
     - **What they do:** Develops agile, low-cost humanoid and bipedal
       robots (PM01, T800) known for highly dynamic RL-trained gaits,
       with a new factory targeting one humanoid every 15 minutes.
     - **Website:** https://www.engineai.com.cn
     - **Valuation:** ~$1.4B (over RMB 10B, as of late 2025)
     - **Last raise:** ~$139M across Pre-A++ and Series A1 rounds
       (July 2025; further A1+/A2 rounds closed December 2025) —
       [EngineAI raises nearly $140M to develop legged, humanoid robots](https://www.therobotreport.com/engineai-raises-nearly-140m-developing-legged-humanoid-robots/)
     - **Employees:** ~200
     - **Why sim / synthetic data:** Their signature dynamic locomotion
       is produced by large-scale reinforcement learning in
       simulation; scaling from gait demos to useful manipulation
       requires exactly the custom sim environments and synthetic
       skill data a consultant would provide.

---

## Companies checked and excluded

For transparency on the screen: **Figure AI, Skild AI, Anduril,
Shield AI, Apptronik, 1X Technologies, Unitree** were excluded on
valuation (at/above ~$5B or unverifiable below it); **RIVR/Swiss-Mile**
(Amazon), **Fernride** (Quantum Systems), **Mentee Robotics**
(Mobileye), and **Fox Robotics** (Symbotic) were excluded as acquired;
**Collaborative Robotics** (April 2024) and **Hai Robotics** (2021)
last raised outside the two-year window; **Waymo and robotaxi firms**
were excluded as not pure-play robotics in the sense used here.
