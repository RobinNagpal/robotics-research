# Four Projects You Can Build and Sell

Each project below is sized to ship in 2-4 weeks of solo work, has a
concrete buyer, and reuses skills a web developer already has
(FastAPI/Express, Docker, GitHub Actions, Postgres, React). The
robotics-specific parts are clearly flagged.

A note on pricing: these are realistic ranges for **2025 in North
America / Western Europe**. Big robotics primes pay the high end;
seed-stage startups pay the low end. Always quote a fixed-fee
"discovery phase" first ($2-5k) to de-risk both sides.

---

## 1. VLA fine-tuning service for niche tasks (~3 weeks)

**What you're selling.** A customer (a warehouse, lab, restaurant
chain) has one repetitive task they want a robot to do. They give you
50-200 video demos plus joint logs (recorded via teleop). You give
them back a fine-tuned policy that runs that task on their existing
hardware.

**Why it works.** Most robotics integrators don't have ML staff. They
have automation engineers who can wire up a robot but cannot train a
neural network. You sit in that gap.

**Concrete examples of target tasks:**
- warehouse pick-pack of irregular SKUs;
- lab pipetting / sample prep;
- retail shelf-facing / restock;
- restaurant prep (assembly, packaging).

**Stack:**
- **LeRobot** dataset format for the input data.
- **OpenVLA-7B** or **pi0-base** as the foundation model.
- **LoRA + 8-bit quantization** so fine-tuning fits on one A100 ($1-2
  per hour rented).
- Held-out eval set; sim deployment in **RoboCasa** or **Robosuite**
  for pre-flight checks.
- **Docker image** as the deliverable: customer runs `docker run` on
  their robot's on-board PC.

**Pricing:** $15-50k per task setup + $1-3k/month for retraining as
the customer's data grows.

**What you need first:** one happy reference customer. Find them by
hanging out in the LeRobot Discord and offering a free first project.

---

## 2. Synthetic demonstration generator (~3 weeks)

**What you're selling.** A SaaS that takes a single human teleop demo
and generates 1,000+ variations by changing object positions, lighting,
backgrounds, distractors, and camera angles. Used to train more robust
policies without re-collecting data.

**Why it works.** Data collection is the single biggest cost in robot
learning right now. Every robotics startup is burning cash on humans
in motion-capture rigs. Anything that 10x's data is valuable.

**Stack:**
- **Isaac Sim Replicator** or **MuJoCo MJX** for the physics + domain
  randomization.
- A "kinematic replay" layer that takes the original action sequence
  and replays it in the new scene (with small interpolation fixes).
- **Stable Diffusion + IP-Adapter** for image-space augmentation
  (re-skinning the texture of objects, swapping backgrounds).
- React + FastAPI front-end where users upload a demo and queue a
  generation job. S3 for storage.

**Pricing:** SaaS credit pack at $0.05-$0.20 per generated episode,
or $2-10k flat per dataset. Realistic ARR target after 6 months:
$5-15k/month.

**Hardest part:** validating that policies trained on your synthetic
data actually transfer. Run a SimplerEnv comparison and put the
numbers on your landing page.

---

## 3. VLA evaluation harness (~2-3 weeks)

**What you're selling.** Customers upload a policy checkpoint; you
return a benchmark report — success rates across **LIBERO**,
**RoboCasa**, **Meta-World**, plus a generalization score and a
failure-mode taxonomy (which kinds of objects/scenes/instructions it
struggles with). Like Sentry for robot policies.

**Why it works.** Most robotics teams have models but no rigorous
eval. They ship by demo. When something regresses they don't notice
until a customer complains. Robot CI is genuinely missing.

**Stack:**
- Dockerized **eval workers on GPU**, parallel rollouts.
- Standard benchmarks (LIBERO + RoboCasa + Meta-World) wrapped as
  reproducible jobs.
- **Failure clustering**: embed each failed rollout's last frame with
  **CLIP** or **DINOv2** and cluster — automatically groups failures
  by what went wrong.
- PDF report generator (WeasyPrint or Puppeteer + HTML template) —
  ship a nice deliverable, not a dashboard URL.
- **GitHub Actions integration** so a PR can trigger a nightly run.

**Pricing:** $500-$2k per one-off run; $1-5k/month subscription for a
nightly regression suite. Pure-software, recurring revenue, no
hardware coordination needed — this is the easiest of the four to
operate.

---

## 4. Natural-language -> robot task DSL (~4 weeks)

**What you're selling.** A web tool where a non-technical operator
types something like:

> "Pick up red blocks and place them in the bin on the left. Ignore
> green blocks."

The tool outputs a **structured task spec** + a few-shot prompt that a
downstream VLA consumes. Think Zapier for "what should the robot do
today?"

**Why it works.** End customers don't want to retrain a VLA every
time they change the SKU layout. They want a config-file abstraction.
You provide it.

**Stack:**
- **Claude / GPT-4** with a JSON-schema-enforced output (the task
  DSL: object descriptions, regions, constraints).
- Prompt examples derived from RoboCasa task library.
- Optional: sim playback loop — generate the task in MuJoCo and
  show the user a 5-second preview before committing.
- React front-end. Auth0 for SSO. Stripe for billing.

**Pricing:**
- $20-100k licensing per OEM (robot manufacturer integrates it).
- $99-499/month SaaS for end-customer SMBs.

**Why this fits a web dev specifically.** Three out of the four
layers (LLM API integration, JSON schemas, React, billing) are
exactly what you already build. The novel pieces are the task DSL
design and the VLA integration — both learnable in a couple of weeks.

---

## How to pick which one to start with

- **Cheapest to start, fastest to revenue:** #3 (eval harness). No
  hardware, no customer data dependency, pure software.
- **Most defensible long-term:** #1 (fine-tuning service). Each
  customer makes you better at this; their data is your moat.
- **Highest ceiling:** #4 (natural-language DSL). Could become a
  product company if you find the right OEM partner.
- **Hardest to validate:** #2 (synthetic data). Worth it only if you
  enjoy the simulation side and can run a credible sim-to-real study.
