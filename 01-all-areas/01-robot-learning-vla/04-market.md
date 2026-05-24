# The VLA and Robot-Learning Market

> Market intel for our team. The companies below are the landscape
> we operate in as a robotics services shop considering or doing VLA
> (Vision-Language-Action) work. Some are potential customers, some
> are partners we can integrate with, some are competitors, some are
> talent sources for our hires, and some are reference points for
> stack and case studies. Comp bands are included so we set our own
> salaries fairly against the market.

## What this file is for

When we pitch a VLA engagement, we sometimes need to position
against the big names ("we do bespoke imitation-learning fine-tunes,
smaller and faster than Skild's generalist pitch"). When we hire, we
benchmark against NVIDIA GEAR / DeepMind Robotics / Physical
Intelligence comp so our offers don't read as low. When we read CoRL
or RSS papers, half come from teams listed here. This is our shared
map of the landscape.

See also: `01-examples.md` (deployed VLAs and reference papers),
`05-projects.md` (what we sell), `06-courses.md` (where our team
learns from), `00-basics.md` (concrete agency project patterns).

## How to read each entry

For each company below: what they do, the tech stack they're known
to use, the TC band our team competes with, the location, and
**what they mean to us** - one of:

- *Potential customer* - their internal teams sometimes hire
  agencies for overflow data work, sim-to-real engineering,
  fine-tunes on customer-specific tasks, or deployment glue.
- *Partner candidate* - they run a formal partner / reseller /
  inception / model-host program we could join.
- *Competitor* - they sell into the same RFPs we do.
- *Talent source / talent risk* - we hire from them; our team
  might leave to them.
- *Reference point* - published work, stack, or case studies we
  study but don't directly compete with.

---

## Big tech and established research labs

Bigger teams, more process, slower cadence. Mostly *reference
points* for stack and published baselines, and *talent risks* for
senior ICs.

- **Google DeepMind Robotics** - the team behind RT-1 / RT-2 / RT-X
  and Gemini Robotics. London, Mountain View. JAX-heavy, publishes
  often. Senior IC reportedly $300-500k.
  *To us:* reference point for the entire RT-X data format and for
  Gemini Robotics' VLM-planner pattern; talent risk for senior ICs.

- **NVIDIA GEAR / Isaac team** - Jim Fan's group, behind GR00T,
  Isaac Lab, Cosmos. Multiple 20-80-engineer teams. PyTorch + CUDA
  + Isaac Sim. Median TC reportedly ~$270k; senior staff $400k+.
  *To us:* **partner candidate** via NVIDIA Inception (free DGX
  cloud credits, GR00T early-access tier, NVIDIA Connect customer
  intros); reference point for Isaac Sim and GR00T integration;
  occasionally a customer for outsourced Isaac Lab / Replicator
  data pipelines.

- **Tesla Optimus** - humanoid policies, vision-only sensing,
  secretive. PyTorch + custom C++; Dojo training. Base lower than
  DeepMind, equity-heavy.
  *To us:* reference point for vision-only humanoid policy stacks;
  not a partner, not a customer.

- **Meta AI / FAIR Robotics** - Habitat simulator, Embodied AI
  research. Less product, more papers. PyTorch.
  *To us:* major reference point - Habitat 3.0, Ego4D, and several
  imitation-learning baselines live here; our team uses their
  open-source work directly.

- **Apple** - robotics rumored, hiring quiet. Top-of-market comp,
  $300-500k+.
  *To us:* reference point only; black box.

- **Amazon Robotics / Lab126** - manipulation, Astro home robot,
  warehouse stack. Mid-Atlantic + Bay Area + Boston. Amazon L5/L6
  bands.
  *To us:* **potential customer** for niche warehouse-manipulation
  consulting; reference point for at-scale industrial deployments.

- **Toyota Research Institute (TRI)** - pioneered Diffusion Policy.
  Cambridge MA + Los Altos. PyTorch + JAX, open publication
  culture. $250-400k.
  *To us:* reference point; some of their open code (Diffusion
  Policy, LfD baselines) is genuinely useful in client work.

- **Boston Dynamics (Hyundai)** - Atlas humanoid + Spot. Boston.
  C++ first, tight controls coupling, learning team growing.
  Senior IC $230-380k.
  *To us:* reference point for state estimation and legged
  locomotion learning; brand carries credibility when team
  members come from here.

- **OpenAI Robotics** - relaunched team (after the 2021 wind-down).
  Reportedly partnering with humanoid OEMs rather than building
  hardware. PyTorch.
  *To us:* reference point; watch for hiring signal as a market
  bellwether.

---

## VLA-native and frontier robot-learning startups (2020-2025)

This is where the explosive growth (and compensation variance)
lives. Many of these did not exist 3 years ago.

- **Physical Intelligence (Pi)** (founded 2024) - pi0, pi0-FAST,
  pi0.5, OpenPI. Raised $400M Nov 2024 at $2.4B. Open-weights for
  some models, generalist focus. PyTorch + JAX. Under 100 total,
  high talent density.
  *To us:* **major reference point** - their OpenPI weights and
  inference code are the closest thing to a "Linux of VLA" right
  now. Our team uses them directly in client fine-tunes. Talent
  risk for senior ML ICs.

- **Skild AI** (2023, ex-CMU) - "Skild Brain," robot-agnostic
  generalist policy. $300M Series A July 2024 at ~$1.5B. PyTorch.
  Pittsburgh + Bay Area.
  *To us:* reference point; their generalist pitch is the one we
  most often have to position against in client conversations
  ("smaller, customer-specific fine-tune vs. one giant policy").

- **Figure AI** (2022) - Figure 02 humanoid + Helix VLA.
  Cumulative >$1.5B raised; reported $39.5B valuation talks Feb
  2025. PyTorch + C++ + NVIDIA Isaac. Sunnyvale.
  *To us:* talent risk for our humanoid-curious senior ICs;
  reference point for Isaac-Sim-based VLA pipelines.

- **1X Technologies** (rebranded from Halodi 2022) - NEO consumer
  humanoid + world-model-based policies. Norway + SF. PyTorch + C++.
  *To us:* reference point for world-model approaches to humanoid
  policy.

- **Apptronik** (Apollo humanoid, Mercedes pilots 2023+) - Austin
  TX. More engineering-than-research, more shipping-focused.
  *To us:* potential customer for industrial integration work if
  they expand partnerships beyond Mercedes.

- **Sanctuary AI** (Phoenix robot, scaled 2023+) - "Carbon"
  cognitive architecture; Canadian.
  *To us:* reference point.

- **Generalist** (2024) - ex-Tesla / OpenAI founders, foundation
  models for humanoids. Pre-product, hiring aggressively.
  *To us:* talent risk; reference point.

- **Reflex Robotics** (2023) - mobile humanoid for warehouses.
  *To us:* potential customer for warehouse-integration consulting;
  reference point.

- **Mentee Robotics** (Israel, 2022) - Menteebot humanoid.
  *To us:* reference point.

- **Persona AI** (2024) - software-first humanoid stack.
  *To us:* reference point; the software-first pitch is closest to
  our own positioning.

- **K-Scale Labs** (2024) - open-source humanoid for developers.
  "Arduino for humanoids."
  *To us:* **partner candidate** for any open-source-humanoid
  client work; reference point.

- **Field AI** (2023) - outdoor / off-road foundation policies for
  inspection, construction. Mission Viejo / Pasadena.
  *To us:* reference point for off-road / unstructured-environment
  policies, which is a potential niche vertical for us.

- **Daedalus** (2024) - manufacturing-focused robot brain.
  *To us:* reference point; potential coopetitor in manufacturing.

- **Cobot** (2022, ex-Amazon Robotics VP Brad Porter) - collaborative
  mobile manipulator built on learned policies. Boston.
  *To us:* reference point for the manipulation-perception
  interface.

- **Wayve** (UK, 2017, Series-C 2024 at $1B+) - end-to-end driving
  foundation models. London + Mountain View. PyTorch + JAX.
  *To us:* reference point for end-to-end policy training at
  scale; talent risk in London.

- **Hugging Face (LeRobot)** - not a robotics startup per se, but
  ships the most-used open-source VLA framework. Paris + remote.
  PyTorch.
  *To us:* **major partner candidate** via Hugging Face Enterprise
  Hub and LeRobot integration partnerships; reference point;
  occasionally a routing source for downstream fine-tune work.

---

## Competing VLA / robotics-learning services shops

The honest answer is that the dedicated VLA / imitation-learning
services market is *thin* compared to the perception consulting
market. Most companies doing VLA-style work are product companies,
not agencies. The names below are the ones we have reasonable
confidence about; we'd hedge on any others.

- **Weights & Biases Professional Services** - not VLA-specific,
  but the closest large-ML-consulting brand teams turn to for
  training-pipeline help. Compete with us only on the training-
  infra slice, not on robot integration.
  *Where we beat them:* full-stack delivery (data + training +
  sim-to-real + deployment), not just training infrastructure.

- **Anyscale Professional Services** - Ray-focused; sometimes
  consulted by teams doing large-scale RL or distributed
  imitation-learning training. Not robotics-specific.
  *Where we beat them:* domain knowledge of teleop data, sim-to-
  real, and onboard inference.

- **Generalist ML consultancies with growing robotics practices**
  (MobiDev, InData Labs, N-iX, Innowise, others) - these are the
  same shops named in our perception-cv employers file; some are
  beginning to take on imitation-learning RFPs. Most are still
  more comfortable on perception than on policy.
  *Where we beat them:* depth on VLA-specific stacks (LeRobot,
  OpenPI, RT-X format, LIBERO benchmark), not generalist ML.

- **Boutique humanoid-software shops emerging 2024-2025** - too
  small and too new to name with confidence. Watch K-Scale Labs'
  partner directory and the LeRobot community channels as these
  surface.

Hedge: the agency market for VLA-specific delivery is early enough
that the named field is small. If a client asks "who else does
this?" the honest answer is usually "the product companies above
do it in-house; outside of them, the agency field is forming, and
we're one of the few shops positioning as VLA-native."

---

## Partnership and reseller programs worth joining

Concrete programs where applying as an agency unlocks credits,
sales co-marketing, or a customer pipeline. We've only listed
programs we're confident actually exist; for anything labeled
"reportedly" we'd verify before relying on it.

- **NVIDIA Inception** - free DGX cloud credits, NVIDIA Connect
  intros to enterprise customers, GTC speaking opportunities,
  reportedly an early-access tier for GR00T tooling. Open to AI /
  robotics shops under ~$50M revenue. Apply at
  nvidia.com/en-us/startups. This is the single highest-value
  program for a VLA-focused shop.
- **Hugging Face Enterprise Hub** - partner-tier discounts for our
  customers; LeRobot integration co-marketing; the LeRobot
  community ecosystem is the closest thing to a referral pipeline
  for VLA fine-tunes. Worth tracking whether HF formalizes a
  separate LeRobot integration partner tier; right now it operates
  more informally through the community channels.
- **AWS Activate / Google Cloud for Startups / Microsoft for
  Startups** - $25k-$200k of cloud credits available; useful for
  GPU-heavy training during initial customer engagements before
  the customer foots the cloud bill.
- **Modal startup program** - GPU credits for serverless inference
  and training; reportedly generous for early-stage shops. Useful
  if our VLA inference servers run on Modal for clients.
- **Lambda Labs startup program** - GPU credits and discounted
  reserved capacity; one of the better-priced H100 / H200 options
  for VLA fine-tunes.
- **RunPod startup program** - similar pattern, lower price point;
  good for smaller engagements.
- **Physical Intelligence's OpenPI ecosystem** - OpenPI weights and
  inference code are openly released; we're unsure whether Pi
  operates a formal partner program around it. Worth asking
  directly. For now, contributing visibly to OpenPI is the closest
  thing to "partner status" with that ecosystem.
- **DeepMind / Google Research collaborations** - rare and
  invitation-based; not a program one applies to. Worth noting as
  a possibility if a client engagement produces publishable
  results.

Most of the above are free to apply to. The realistic high-value
ones for a VLA shop are: NVIDIA Inception, Hugging Face Enterprise
Hub, and at least one GPU-credit program (Modal, Lambda, or RunPod)
to keep training costs predictable.

---

## Comp bands (inputs to setting our own salaries)

Approximate TC bands for senior IC (3-7 years), 2025 Bay Area / NYC.
Sources: levels.fyi, 2025 Robotics Salary Guide, public funding
announcements. Startup TC is noisy because it includes illiquid
common shares.

- **NVIDIA, Google DeepMind, Apple, Tesla:** $300-500k+
- **Physical Intelligence, Skild, Figure, 1X, Wayve, Generalist:**
  $350-600k+ (equity is the lottery ticket)
- **TRI, Meta FAIR, OpenAI Robotics:** $250-400k
- **Boston Dynamics, Apptronik, Cobot, Sanctuary:** $230-380k
- **Smaller humanoid / specialist startups (Reflex, Mentee,
  Persona, Field AI, Daedalus, K-Scale):** $200-350k
- **Hugging Face, Weights & Biases:** $200-330k with full-remote
  optionality
- **EU and remote roles:** typically 20-40% lower than Bay Area;
  London / Munich close the gap on the high end.

**For our hires:** band our base salaries at or above the
Hugging Face / Weights & Biases range. Below that and our offers
read as low against the market our team is comparing against.
Equity-heavy frontier VLA startups (Pi, Figure, Skild) are not
direct comp competitors for our headcount; their candidates take
lottery-ticket risk we can't match, so we compete on cash,
project variety, and remote optionality.

---

## Hiring market signal

From the 2025 Robotics Salary Guide:

- ML Engineer is the **second-highest-paying IC track** in robotics
  (after embedded real-time + Linux).
- "RL" and "diffusion" each command a **+33% salary premium** when
  listed as a required skill.
- ML appears in **~31% of all robotics job postings** - the
  single most-requested skill family in the field.

Translation: VLA / robot-learning is the highest-paying robotics
specialty by a meaningful margin, and demand is visible enough that
the bar is rising fast. Good market for our shop's positioning, but
we should expect to keep investing in team capability (see
`06-courses.md`) just to stay credible against frontier-startup
candidates.

---

## Remote / hybrid posture by employer type

Useful for understanding which talent pools are accessible to us
(remote-friendly competitors = larger candidate pool for our
remote hires, but also more competition for distributed talent).

- **Big tech research (DeepMind, FAIR, NVIDIA Research, OpenAI
  Robotics):** remote-friendly for research and ML infra; less for
  product or hardware-adjacent roles.
- **Humanoid startups (Figure, 1X, Apptronik, Cobot, Sanctuary,
  Reflex, Generalist):** strictly on-site. Their candidate pool
  doesn't overlap much with ours for remote roles.
- **Pi, Skild, Wayve:** mostly on-site at Bay Area / London hubs.
- **TRI, BD:** hybrid 3-5 days on-site at Cambridge / Boston.
- **Hugging Face (LeRobot), Weights & Biases:** fully remote,
  globally distributed. Our biggest direct competitors for
  distributed-team talent.
- **Tesla Optimus:** strictly on-site Bay Area / Texas.
- **Open-source / community-led (K-Scale, LeRobot maintainers):**
  remote and project-based.

---

## Title decoder (how to read competitor job ads)

The same role carries five different names across companies. Use
this when reading competitor job ads (market signaling) or when
writing our own postings.

- **Research Scientist** - PhD or equivalent, publishes papers
  (DeepMind, FAIR, NVIDIA Research, TRI, Pi). The frontier-paper
  track.
- **Research Engineer** - strong eng + decent ML chops (Pi, Skild,
  Figure, 1X, OpenAI Robotics, Wayve). Glues datasets, runs
  training, optimizes inference. **The role our team's career
  trajectory most resembles**, so the most relevant comp band
  for us.
- **ML Engineer, Robotics / VLA** - training, infra, scaling
  (Wayve, Tesla, Pi, Skild, FAIR). PyTorch / JAX, distributed
  training.
- **Robotics Software Engineer (Learning)** - generalist with ROS
  / C++ comfort (Figure, 1X, Apptronik, BD, Cobot). More systems
  integration than pure ML.
- **Foundation Model Engineer** - frontier-startup variant of ML
  Engineer (Pi, Skild, Generalist). Often code for the pretraining
  stack.
- **Data Engineer, Teleop / Robotics** - dataloaders, eval
  harnesses, teleop-data pipelines (every company above). Our
  team's existing web-eng skills already overlap a lot here.
- **Simulation Engineer** - Isaac Sim / MuJoCo / Habitat (NVIDIA,
  Pi, Figure, FAIR). Sim-to-real adjacent.

---

## What this means for our positioning

Four short takeaways for the team:

1. **Big tech and frontier humanoid startups are reference points,
   not competitors.** They serve different price points (internal
   headcount, custom silicon, generalist policy ambitions) than we
   sell. Mention them only when a customer asks "who else does
   this?"
2. **The VLA agency field is thin.** Unlike the perception-CV
   market, there are very few dedicated VLA services shops. This
   is an opportunity (early mover, well-positioned for inbound
   demand) and a risk (no big anchor partners to absorb spillover
   work; the customer education burden is on us).
3. **Open-source ecosystems are where the leverage is.** LeRobot
   (Hugging Face), OpenPI (Physical Intelligence), Isaac Lab /
   GR00T (NVIDIA), Habitat (FAIR). Visible contributions to these
   are worth more to our positioning than a marketing budget.
4. **Talent risk is concentrated in humanoid startups.** If we
   grow into VLA-native senior hires, expect Figure / 1X /
   Generalist / Pi to be the most realistic departure paths. Plan
   compensation, remote flexibility, and project variety to be
   competitive on the axes equity-heavy startups can't match.
