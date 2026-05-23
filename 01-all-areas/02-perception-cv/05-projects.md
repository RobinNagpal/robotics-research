# Six Projects You Can Build and Sell

Each scoped to 2-4 weeks of solo work, with a concrete buyer, and
reusing skills a web developer already has (FastAPI / Express, Docker,
GitHub Actions, Postgres, React). The perception-specific parts are
clearly flagged.

A note on pricing: ranges below are realistic for **2025-2026 in North
America / Western Europe**. Big robotics primes and AV teams pay the
high end; seed-stage robotics startups and manufacturing SMBs pay the
low end. Always quote a fixed-fee "discovery phase" first ($2-5k) to
de-risk both sides before quoting a full build.

A note on framing: every project below is, structurally, a SaaS or
agency engagement that you have probably already shipped — only the
upstream model has changed. A FastAPI inference endpoint serving
SAM 2 is roughly a Next.js API route serving GPT-4: same plumbing,
different upstream. Stripe billing for a perception-as-a-service
product is Stripe billing for a SaaS product, because it **is** a
SaaS product — the model just happens to be a CV model instead of an
LLM. A Docker image with FoundationPose inside is a Vercel deploy of
a Next.js app: it is the artifact your customer runs, and your job
is to make sure it boots clean on their machine. If you reframe the
work this way, the only genuinely new skill is "talk to a perception
engineer without panicking," which the rest of this folder
(`02-learn.md`, `04-employers.md`) is designed to fix.

Cross-references in this folder: `00-basics.md` for the vocabulary,
`01-examples.md` for working code snippets you will copy-paste,
`02-learn.md` for the 12-week curriculum, `03-start.md` for the
zero-to-first-commit ramp, `04-employers.md` for who is buying, and
`06-courses.md` for the deeper-study path if you decide to skill up
on the ML side beyond what an agency needs.

---

## 1. Phone-scan -> robot-ready 3D environment (~4 weeks)

**What you're selling.** A web service: the customer walks around a
room with their phone (5 minutes), uploads the video, and receives
back a Gaussian splat + collision mesh + per-object semantic
segmentation, all packaged as a USD (Universal Scene Description) or
URDF file that loads directly into Isaac Sim or Gazebo.

The customer experience is closer to Loom than to a 3D-scanning
tool. They press record, walk a loop, hit upload, and 20 minutes
later get an email with a link to a viewer plus a download bundle.
The whole product surface from the buyer's side is roughly the
complexity of a Calendly: one URL, one upload field, one
notification, one download. The hard parts — pose estimation,
splat training, semantic fusion, collision-mesh decimation — happen
inside the box.

**Why it works.** Every robotics startup needs digital twins of
customer sites (for sim2real training, for sales demos, for
sim-based validation). Hiring a 3D artist or sending an engineer
on-site costs $5-20k each time. You sell a $1-5k self-serve
alternative.

The deeper "why" is that simulation has quietly become the default
training surface for manipulation and navigation policies, and every
sim needs an environment. Polycam and Matterport target real-estate
and AEC; nobody is targeting "robotics-grade" capture where you
need URDF joints, semantic labels on every object, and a collision
proxy that does not blow up the physics solver. That gap is your
wedge. You are not competing with Polycam; you are competing with a
roboticist on a Saturday afternoon trying to hand-author a kitchen
in Blender.

**Stack:**
- **iPhone capture** with Polycam, Scaniverse, or a custom
  ARKit/AVFoundation app.
- **COLMAP** or **glomap** for structure-from-motion (camera poses
  + sparse point cloud).
- **Nerfstudio + gsplat** for Gaussian splat training.
- **SAM 2** to project semantic masks across views, fused into the
  3D scene.
- **Open3D** to mesh-extract a collision proxy.
- **USD / URDF export** with the `usd-core` Python library and
  `pxr` from NVIDIA's USD SDK.
- React + FastAPI front-end with an S3-backed job queue (Celery /
  RQ). Stripe for billing.

**Pricing:** $1-5k per scene; or $500/mo subscription for unlimited
small scenes. Realistic ARR target after 6 months: $5-15k MRR.

For anchoring, Matterport's pro tier sits in the few-hundred-dollars
per scan range for real-estate use; Polycam's pro subscription is
roughly $20/mo. Your buyers will compare you to those prices and
then accept a 5-10x premium once they realize neither of those
products spits out a URDF or labeled collision mesh. Lean into that
gap when you quote — you are selling the format, not the capture.

**What you need first:** one happy reference customer. Hang out in
the Isaac Sim and LeRobot Discords, offer a free first scan in
exchange for a public testimonial.

**Sales angle in one sentence.** "I turn a 5-minute phone walkthrough
of your customer's warehouse into an Isaac-Sim-ready USD file so
your sales engineer stops spending Fridays in Blender."

**First-customer playbook.** The fastest path to a paid pilot is a
seed-stage mobile-manipulation or AMR startup that has a demo
coming up. They have site visits they cannot scale, an investor
deck that needs a sim screenshot, and a founder who will say yes on
a Zoom call. Find them via the LeRobot Discord, the Isaac Sim
forum, YC's company directory filtered by "robotics," and Series-A
announcements on TechCrunch from the last 18 months. Pitch a $5-10k
fixed-fee, 6-week engagement: three scenes of their choosing, a
working pipeline they can re-run on their own captures, and a
30-minute handoff call. Make the contract one page.

**What this scales to.** At $10k MRR you are running 5-20 paid
scenes per month, probably mostly one-off per-scene billing with
two retainer customers. At $50k MRR you have a self-serve tier
(Stripe Checkout, no human in the loop), a higher-touch enterprise
tier ($2-5k per scene with a human QA pass), and one hired
contractor handling the long tail of capture-failure debugging. As
a $1-5M ARR boutique you are the default vendor every Series-A
robotics company gets pointed to when their VP of Engineering says
"we need a digital twin pipeline by Q3," and your acquisition
candidates are Matterport, Polycam, NVIDIA Omniverse, or a sim
vendor like Foretellix.

---

## 2. 6-DoF pose-estimation API for industrial parts (~3 weeks)

**What you're selling.** A customer uploads a CAD model of a part
they need to pick (a fitting, a bracket, an SKU). Your service
returns a fine-tuned **FoundationPose** / **MegaPose** checkpoint +
a Dockerized REST endpoint that takes an RGB-D image and returns a
6-DoF pose for that part.

Think of the UX as Vercel for pose models. The integrator drops a
STEP file into a web form the way a frontend dev pushes to a Git
branch; a build kicks off (synthetic-data generation, fine-tune,
eval, package); 30-60 minutes later they get a green checkmark and
a `docker pull` command. Failures come back with a readable diagnostic
("part is too symmetric on the Z axis, accuracy plateaued at 14mm,
suggest adding a fiducial or a secondary view") instead of a stack
trace.

**Why it works.** Bin-picking integrators (Pickle, Kindred,
hundreds of system integrators worldwide) are constantly being
asked to add new SKUs. The "right" answer used to be a
multi-week PhD project per SKU. FoundationPose changed that.
Most integrators haven't internalized it yet — you sit in that
gap.

The economic logic is even better than it sounds. An integrator
quoting a new bin-picking cell to an end customer typically pads
$15-50k of "perception engineering" into the project just to cover
the unknown of adding new SKUs over the contract's lifetime. If
you can collapse that cost line to a predictable $2-10k per SKU
with a turnaround SLA, you become a line item in their proposal,
not a competitor — and that is the relationship you want.

**Stack:**
- **FoundationPose** (NVIDIA, Apache 2.0) as the base model.
- A small **synthetic data pipeline** in BlenderProc or Isaac Sim
  Replicator to generate training images of the part in varied
  lighting / backgrounds / occlusions.
- **NVIDIA Triton Inference Server** or a simple FastAPI + ONNX
  Runtime endpoint for serving.
- **Docker image** as the deliverable.
- Optional React dashboard for the customer to upload CAD,
  monitor accuracy, and re-train.

**Pricing:** $2-10k setup per part + $0.01-0.10 per inference (or
a $500-2k/mo all-you-can-eat plan).

The metered tier is more for psychological anchoring than for
revenue — most customers will pick the flat monthly because their
finance team prefers predictable line items. But quoting per-call
pricing alongside the flat fee signals "this is a real API
product," not a one-off contracting gig, which raises the price
ceiling on every other deliverable in the contract.

**Hardest part:** getting accuracy good enough on shiny / textureless
metal parts (the bane of vision-based pose estimation). Have a
mitigation ready: combine with a structured-light sensor or
fall-back tactile retry strategy.

The second-hardest part is synthetic-to-real domain gap. Your
BlenderProc renders will look beautiful and your model will hit
2mm accuracy in sim, then collapse on the customer's actual factory
floor because their lighting is fluorescent and yellow, the
conveyor is vibrating, and the parts arrive partially occluded by
swarf. Budget a week of every engagement for "real-data calibration"
where you collect 100-500 real images from the customer's line and
fine-tune again. Frame this to the customer as a feature, not a
cost: "the system gets smarter the more it sees your line."

**Sales angle in one sentence.** "I add new SKUs to your bin-picker
in 48 hours for a flat fee, so your perception lead can stop being
a ticket-closer and go back to building your roadmap."

**First-customer playbook.** Target Tier-2 system integrators, not
end customers and not the big names. Find them by searching
LinkedIn for "robotics integrator" + a region, or by scraping the
Universal Robots / FANUC / KUKA certified-partner directories.
These shops have 5-30 engineers, a backlog of bin-picking quotes
they cannot staff, and a sales cycle measured in weeks rather than
quarters. Offer a free first SKU in exchange for a case study and
a logo on your site. Convert to a paid retainer when they bring
you SKU number two.

**What this scales to.** At $10k MRR you have 5-10 integrator
customers each paying $500-2k/mo, plus 1-2 setup fees per month.
At $50k MRR you have a self-serve portal (CAD-in, Docker-out), a
small library of pre-trained models for common part families
(fasteners, brackets, electronics), and a partnerships channel with
one or two robot OEMs who recommend you. As a $1-5M ARR boutique
you are essentially the "Twilio for industrial pose estimation,"
your moat is the proprietary dataset of CAD-to-trained-model pairs
you have accumulated, and your acquirers are Cognex, Zebra
Technologies, or a Tier-1 industrial-vision player.

---

## 3. Visual-inspection-as-a-service (~2-3 weeks)

**What you're selling.** A web UI where a small-to-mid manufacturer
uploads 50-100 "good" and 50-100 "bad" product images. Your service
trains an anomaly-detection model (PatchCore / EfficientAD / DINOv2
+ kNN) and ships back a Docker container with a REST endpoint that
classifies new images. The customer drops it onto their line PC.

Onboarding a manufacturer to your inspection service is roughly
like onboarding a small business to Shopify — except the
integration takes 2 hours instead of one click, because someone has
to physically aim a camera at the conveyor and run a calibration
pass. That 2-hour gap is the only piece of friction left, and
half your job at the agency stage is figuring out how to either
collapse it (a pre-mounted camera kit you ship) or productize it
(a one-page install guide their existing PLC integrator can follow).

**Why it works.** Visual QC departments at small-to-mid
manufacturers (PCB shops, food packers, fabric mills, parts
suppliers) pay well and have **zero ML staff**. Their existing
options are buying a $50k+ Cognex / Keyence system or doing nothing.
You undercut Cognex on price and beat "doing nothing" by miles.

The other thing they have is a quality manager whose entire job
performance is measured in escape rate (defects shipped to
customers). That person has clear ROI math: every defect caught
costs them $X to scrap, every defect shipped costs them $10X to
$100X in returns, recalls, and lost contracts. When you can show a
demo on their own images that catches 90% of their known defect
classes, you are not selling them software, you are selling them
their bonus. Pricing follows from that.

**Stack:**
- **anomalib** (OpenVINO toolkit, MIT licensed) for the model zoo.
- Or **DINOv2 + nearest-neighbor on embeddings** as a baseline that
  often beats supervised approaches with limited data.
- **ONNX / TensorRT** export for deployment speed.
- Docker image with FastAPI inference endpoint.
- React upload UI; Stripe billing.

**Pricing:** $5-25k per defect class deployed, plus $200-1000/mo
support / re-training subscription. Pure software, recurring
revenue, no on-site work needed.

**Why this fits a web dev specifically.** Three of four layers
(upload UI, billing, Docker delivery) are exactly what you already
build. The ML piece is a 200-line `anomalib` config plus some
evaluation code. The "training" step is roughly equivalent to
configuring a Vercel build: pick a base model, point it at the
data folder, hit go, watch the logs. The novelty is entirely in
the eval — you have to learn to read a precision-recall curve and
explain it to a non-technical buyer in plain English ("we catch
94 of every 100 defects, and false-alarm 3 times per 1000 good
parts").

**Sales angle in one sentence.** "I bolt a Cognex-equivalent
defect detector onto your line for one tenth the price and no
PhD, and you can be running it before your next shift change."

**First-customer playbook.** Skip the giant brands. Target a single
contract manufacturer with 50-500 employees, ideally one already on
Industry-4.0 mailing lists (signals they care). Cold-email the
quality manager (not the CEO, not IT) with a 60-second Loom video
showing a defect detector running on stock images of their product
category. Offer a $5k pilot on one defect class with a money-back
guarantee if you do not beat 80% recall on their own held-out test
set. The hit rate on those cold emails will be 1-3%, so write 100
of them. Trade shows like IMTS, Pack Expo, and Automate are also
fertile ground — one good conversation at a booth often beats a
month of cold outreach.

**What this scales to.** At $10k MRR you have 5-15 manufacturers
each on a $500-2k/mo plan, with a steady drip of $5-25k setup fees
as they add defect classes. At $50k MRR you have a self-serve
trainer (upload images, get a Docker tag back, no human in the
loop), a partnership with one or two industrial PC vendors who
preload your container, and a "channel" of automation integrators
who resell you. As a $1-5M ARR boutique you have crossed into
"baby Cognex" territory: a recurring SaaS with a strong industry
niche (say, food packaging, or PCBs), and your most likely
acquirers are Cognex, Keyence (unlikely, they build everything),
or a private-equity rollup of industrial-software companies.

---

## 4. Real-time SLAM benchmark + tuning service (~3 weeks)

**What you're selling.** Customer uploads a ROS bag (or any
video + IMU). Your service runs **ORB-SLAM3**, **VINS-Fusion**, and
**DROID-SLAM** with several parameter sets, evaluates each against
their ground-truth trajectory (if available) or against
self-consistency loop closures (if not), and returns a tuning
report with parameter recommendations and an accuracy comparison.

The deliverable is a PDF and a Git repo — the PDF for the VP of
Engineering to forward to the CEO, the Git repo for the actual
perception engineer to reproduce, modify, and re-run. The PDF has
charts, a short narrative, and a numbered list of recommendations
(ranked by expected impact). The Git repo has a `Makefile` that
re-runs the whole sweep, the Docker Compose file, and the eval
notebooks. Selling both formats is the difference between a
$2k report and a $5k report.

**Why it works.** Drone, AMR, and AR startups have engineers who
know perception well enough to tune one SLAM stack, but rarely
have the bandwidth to comparison-shop across the four big options.
You provide that "Sentry for SLAM" service — like a CI step that
catches drift / scale errors before customers do.

Your CI angle is the long-term lock-in. A one-off benchmark
report is interesting; a nightly GitHub Action that runs against
their latest firmware build and posts a comment on the PR is
indispensable. Pitch the benchmark as the lead magnet and the CI
add-on as the actual product — same pattern as Sentry, Datadog,
or Vercel's preview deploys, which are also "infrastructure
products you forget you are paying for."

**Stack:**
- **evo** (Python eval tool) for trajectory comparison.
- Dockerized **ORB-SLAM3**, **VINS-Fusion**, **OpenVSLAM**, and
  **DROID-SLAM** images, all pinned.
- Parameter sweep harness (Ray Tune or even just a YAML matrix).
- **WeasyPrint** or **Puppeteer** for the PDF report.
- **GitHub Actions integration** so a PR can trigger a nightly run.

**Pricing:** $2-5k per benchmark report; $500-2k/mo for nightly CI
add-on. Pure software, no hardware coordination needed.

**Hardest part:** ground truth. Most customers do not have a motion-
capture system or RTK-GPS rig, which means you cannot definitively
say "stack A is more accurate than stack B." You will instead lean
on relative metrics (loop-closure error, scale drift, ATE against
a fused reference trajectory), and you will spend serious time
educating customers on why a perfect number is not available. Have
a one-page explainer ready; you will email it constantly.

**Sales angle in one sentence.** "I will tell you in two weeks
whether your SLAM stack is the bottleneck on your demo, and which
one of the four open-source alternatives would beat it, with
numbers."

**First-customer playbook.** The cleanest buyers are drone startups
preparing for a Series A and AR/VR studios shipping a headset demo
at a trade show — both have a hard date by which "the map has to
stop drifting" and both have a single perception lead who would
love a second pair of eyes. Find them via Drone Industry Insights,
the AWE conference attendee list, and the ROS Discourse forum.
Pitch a $5-10k, 4-week engagement: a benchmark report, a tuned
config file for their chosen stack, and a setup of the CI harness
in their existing GitHub repo. The CI harness is the bait for the
recurring subscription.

**What this scales to.** At $10k MRR you have a portfolio of 5-10
recurring CI customers plus a steady drip of one-off benchmarks.
At $50k MRR you have productized the benchmark harness into a
self-serve SaaS where customers connect their S3 bucket of ROS
bags and pick a stack from a dropdown; you also publish a public
leaderboard that becomes a marketing flywheel (think Hugging Face
leaderboards, but for SLAM). As a $1-5M ARR boutique you are the
default observability platform for spatial AI startups, with
acquirers including a robotics simulation vendor (Foretellix,
Applied Intuition) or a sensor company (Ouster, Luminar) who
wants a software services arm.

---

## 5. AR scene-understanding Unity plugin (~3-4 weeks)

**What you're selling.** A Unity package (single `.unitypackage`
file, drag-and-drop install) that exposes a real-time mesh +
semantic-segmentation feed from any RGB or RGB-D camera the Unity
app has access to. Under the hood it wraps SAM 2 for segmentation
and Depth-Anything v2 for monocular depth, both running locally via
ONNX Runtime, with a thin C# API that gives the game developer a
`SceneMesh` and `SemanticLabels` stream per frame. Optional Unreal
port for the second engagement.

The buyer experience is "I import your package, drag the prefab
into my scene, hit play, and I see colored bounding-volume meshes
around every chair and wall in my room." No Python, no model
downloads, no CUDA setup — that part you have already pre-baked.
Think of it as the difference between npm-installing a
fully-tree-shaken React component versus configuring webpack from
scratch: same underlying capability, totally different
developer experience.

**Why it works.** Small game studios, training-sim shops, and
location-based-VR operators want "Meta Quest passthrough but
smarter" without staffing a perception team. Native ARKit /
ARCore scene understanding has plateaued; Apple's Vision Pro APIs
are improving but locked to one device; cross-platform Unity
developers have basically nothing. You fill that gap by selling a
package that runs on any laptop or headset with a camera and a
mid-tier GPU.

The unit economics favor this project more than people expect.
Game studios already buy Unity assets routinely — the Asset Store
has trained them to spend $50-500 on a tool and $5-50k on a custom
integration. You are just pricing one tier above the Asset Store
default, which is where genuinely engineering-heavy assets
(networking middleware, AI behavior trees) already live.

**Stack:**
- **Unity 2022 LTS or 6** as the integration target; Unreal 5.x as
  a stretch goal.
- **ONNX Runtime** with the DirectML or CUDA execution provider
  for Windows; CoreML for Mac/iOS; NNAPI for Android.
- **SAM 2** (quantized to int8, exported to ONNX) for
  segmentation; **Depth-Anything v2** small variant for depth.
- A thin **C# wrapper** that marshals texture data into ONNX
  tensors and back into a `Mesh` / `Texture2D` Unity can render.
- A small **sample scene** that shows real-time segmentation of a
  webcam feed — your demo and your README in one.
- Licensing managed via a per-seat key check against a tiny
  FastAPI endpoint you host (essentially the same flow as JetBrains
  or Sketch licensing — boring, well-trodden).

**Pricing:** $5-30k per integration depending on engine, target
platform, and custom model swaps; plus $1-5k/mo for support, model
updates, and version-compatibility patches as Unity itself ships
new LTS releases. Some studios will prefer a perpetual license
($10-20k flat); offer both and let them choose.

**Hardest part:** real-time performance budget. Game studios will
not accept a 100ms-per-frame inference cost when they have a 16ms
budget for the entire frame. You will spend most of the engagement
on quantization, distillation, frame-skipping heuristics, and
"only re-segment when the camera moves enough" tricks. Plan for
this — it is not the SAM 2 wrapper that is hard, it is the
"fit inside a game loop" optimization.

**Sales angle in one sentence.** "I drop a real-time
mesh-and-semantics layer into your Unity project this month, so
your demo at GDC actually understands the room instead of just
seeing it."

**First-customer playbook.** Two distinct buyer personas. Persona
one: a small VR training-sim studio (fire-safety, medical,
industrial-safety training) that is bidding on a government or
enterprise contract that requires "scene understanding." They have
a contract deadline and a budget. Find them via SBIR award
announcements and the I/ITSEC conference. Persona two: a
location-based VR operator (think the Sandbox VR or Dreamscape
franchises) building a new attraction. Find them via the
Location-Based Entertainment Association and the IAAPA expo. Both
will pay $10-25k for a 6-week integration if you can show a working
demo on the first call.

**What this scales to.** At $10k MRR you have 3-5 studios on
support retainers plus 1-2 paid integrations per quarter. At
$50k MRR you have a Unity Asset Store SKU at a "lead-magnet" price
($199), a "Pro" license tier at $5k/year self-serve, and an
"Enterprise" tier that includes custom model fine-tuning. As a
$1-5M ARR boutique you are the default spatial-AI middleware for
non-Meta XR, your acquirers are Unity itself, Niantic (8th Wall),
or a headset OEM (Pico, HTC) that wants better passthrough
without an in-house perception team.

---

## 6. Camera-calibration concierge service (~ongoing, no project end)

**What you're selling.** The most boring possible product, which is
why nobody else is selling it: a recurring camera-calibration
service for robotics startups. Customer ships you their robot's
camera rig (or, more often, joins a 30-minute Zoom call where you
walk their tech through the capture procedure with a checkerboard
or ChArUco board). You mail back a YAML calibration file
(intrinsics, distortion, hand-eye, stereo extrinsics as
applicable), a 3-page validation report with reprojection-error
charts and known-failure-mode notes, and a calendar reminder to
re-calibrate every 90 days. When the reminder fires, you do it
again, automatically, on a subscription.

Calibration is the dental cleaning of robotics: everyone knows
they should do it, almost nobody does it on schedule, and the
consequences (silent accuracy drift, weird policy failures, debug
sessions that end with "oh, the camera moved 2mm") are exactly
the kind of thing a perception lead would happily pay $200/mo to
outsource. You are not selling capability; you are selling
discipline-as-a-service.

**Why it works.** Every perception lead at a 5-50 person robotics
startup has a calibration task on their backlog. It is never the
most important thing, so it never ships. Meanwhile their stereo
baseline has drifted, their hand-eye is off by half a degree, and
their grasp-success rate is mysteriously down 8% from last
quarter. You are the boring outsourced fix.

Roughly the same logic as a payroll provider: you could do it
in-house, the math is not hard, but the calendar discipline and
the audit trail are worth the monthly fee.

**Stack:**
- **OpenCV** for intrinsics and stereo calibration; **Kalibr** for
  IMU-camera; standard **hand-eye** routines (Tsai, Park, Daniilidis)
  with a clean Python wrapper.
- A printable **ChArUco / AprilTag** board you mail to customers,
  with a QR-coded serial number so you know which calibration
  belongs to which rig.
- A **video-upload workflow** (S3 + presigned URLs) for customers
  who cannot do live Zoom calibration; you process asynchronously.
- A **report generator** in WeasyPrint or ReportLab; the report
  template is the same every time, only the numbers change.
- A **CRM / reminder system** — Airtable + a cron job is enough
  to start; HubSpot or Attio when you have 20+ rigs under
  management.

**Pricing:** $1-2k per rig for an initial calibration (one-time);
$200/mo per rig retainer that includes a quarterly re-calibration
session, a Slack channel for ad-hoc questions, and a written
incident report if their calibration ever fails validation. Volume
discounts at 10+ rigs under one customer.

**Hardest part:** there is no hard technical part, which is also
the trap. The hard part is operations: shipping boards, tracking
serials, scheduling Zoom calls across time zones, chasing
customers who skip a quarter, keeping a tidy audit trail. Treat
this like running an accounting firm, not an engineering firm.

**Sales angle in one sentence.** "Your stereo calibration drifted
3 weeks ago and you have not noticed; I will catch it next time,
and the time after that, for $200 a month."

**First-customer playbook.** Post a free "calibration audit" offer
in the LeRobot, Isaac Sim, and ROS Discourse forums. Run the
audit live on Zoom: 30 minutes, you compute their reprojection
error, you tell them whether it is acceptable, you send a short
PDF. Convert any rig with measurable issues into a $1k initial
re-calibration plus the $200/mo retainer. Hit rate on these
audits is high (most rigs are out of spec) and the conversation
itself is the sale.

**What this scales to.** At $10k MRR you have ~50 rigs under
management across 10-20 customers. At $50k MRR you have ~250 rigs,
a part-time contractor running the Zoom calibrations, and a
self-serve portal where customers can upload calibration videos
and get reports without your involvement. As a $1-5M ARR boutique
you are essentially an outsourced metrology department for the
robotics industry, with ISO certification, automotive-grade audit
trails, and a software product (the rig-tracking and drift-alert
system) that becomes the actual durable asset. Acquirers: a
robotics consultancy doing roll-up, an industrial metrology
company (Hexagon, FARO), or a robotics insurance startup that
wants underwriting data.

---

## How to scope a discovery phase

Before any of the six projects, sell a **discovery phase** first.
This is the perception-agency equivalent of a design sprint or a
"technical spike" in a Scrum team — short, fixed-fee, and
explicitly de-risking both sides before anyone commits to a full
build.

**The template.**

- **Duration:** 1-2 weeks, never longer.
- **Price:** $2-5k, flat, paid up front (50% on signing, 50% on
  delivery is fine if their procurement insists).
- **Three deliverables, every time, no exceptions:**
  1. A **written assessment** (5-10 pages) of what the customer
     actually needs, what the literature says is possible, and
     what the realistic accuracy / latency / cost numbers look
     like. Roughly the format of a Stripe Atlas pre-incorporation
     memo: structured, opinionated, decision-ready.
  2. A **working proof-of-concept notebook** that runs end-to-end
     on a small sample of the customer's data. It does not need
     to be production code; it needs to demonstrate that the
     hard parts are not show-stoppers. Treat this like a Vercel
     preview deploy of the eventual product.
  3. A **fixed-fee quote** for the full build, with two or three
     scope options ("minimum viable," "recommended," and
     "all the bells"). Each option has a price, a timeline, and
     a list of explicitly-out-of-scope items.

The discovery phase is also your filter. About a third of
customers will see the assessment and decide not to proceed,
which is the best possible outcome for both of you — they keep
the $2-5k of value, you keep the cash and the case study, and
neither of you sinks 8 weeks into a doomed engagement.

A second purpose of the discovery phase is that it makes you
look like a professional. A web developer who quotes a fixed
build with no discovery is a freelancer; one who insists on a
discovery first is a consultancy. The price band the customer
mentally puts you in shifts accordingly.

---

## Pricing principles

Five rules of thumb that apply to all six projects above.

1. **Charge per outcome, not per hour, where possible.** "I will
   add a new SKU to your bin-picker for $5k" beats "I bill at
   $200/hr" every time, because it transfers risk from the
   customer to you, and customers pay handsomely to offload risk.
   Per-hour pricing also caps your upside at "fast typist with a
   PhD."
2. **Bundle a discovery phase before quoting a build.** Never
   quote a 6-week project off a 30-minute call. Always insert
   the 1-2 week discovery first. This is true even when the
   customer is impatient — especially when the customer is
   impatient, since impatient customers are exactly the ones
   most likely to have unrealistic expectations that will blow
   up your fixed-fee margin.
3. **Always price recurring (support, re-training,
   re-calibration) separately from setup.** Setup is the wedding;
   the subscription is the marriage. Customers will accept a
   recurring fee if it is line-itemed and named clearly
   ("model re-training subscription," "calibration retainer,"
   "uptime SLA"). They will resent it if you bury it inside the
   setup fee and hope they do not notice.
4. **Reference Cognex, Keyence, Matterport, and Polycam for
   price anchoring.** Customers in your space have a vague sense
   that "industrial vision is expensive" (Cognex) and that
   "consumer 3D scanning is cheap" (Polycam). Your pricing
   should land between these anchors, and you should mention
   the anchors explicitly in your proposal so the customer's
   pricing intuition is calibrated before they read your
   number. Hedge — these vendors do not publish list prices, so
   say "comparable industrial vision systems start in the
   $40-80k range" rather than quoting a specific competitor
   number you cannot back up.
5. **Raise prices 25% after every 3 paying customers.** You
   will systematically underprice early because your confidence
   is low. The fastest correction is a rule: every third
   signed customer, raise the published price band by 25%.
   After four iterations you have nearly tripled your pricing,
   and the customers paying the higher rate will still be
   getting a bargain compared to building in-house.

---

## Tooling stack for the agency

Treat the agency itself as a small SaaS company. The tools below
are the same ones a web-dev agency would use, with one or two
additions specific to perception work.

- **Product analytics:** Posthog (open source, generous free
  tier) or Plausible (simpler, hosted). You want to know which
  customers are actually hitting your API, how often, and where
  they drop off in the onboarding flow.
- **Project management:** Linear. Cheap, fast, opinionated,
  designed for small product teams. Asana and Jira are overkill
  at agency scale.
- **Async demos to customers:** Loom. Three-minute videos beat
  one-hour meetings for status updates and feature walkthroughs.
  Every weekly client check-in should be a Loom plus a written
  summary unless the customer specifically asks for live time.
- **Client wikis:** Notion or Obsidian-published (via Obsidian
  Publish or Quartz). One workspace per customer, with their
  architecture, calibration files, model checkpoints, and a
  changelog. Customers love this and competitors rarely do it.
- **Billing:** Stripe + Stripe Tax. Stripe Tax is the underrated
  one — it handles VAT, GST, and US sales-tax automatically once
  you cross thresholds, which you absolutely will if you sell
  internationally.
- **Legal entity:** an LLC in the US, or a Stripe-Atlas-equivalent
  in your country (Tide, Mercury, Wise Business depending on
  geography). One legal entity per agency, one bank account, one
  bookkeeping system from day one. Mixing personal and business
  finances is the most expensive mistake first-time founders
  make.
- **Insurance:** professional liability (also called Errors &
  Omissions). Vouch.us in the US covers tech startups well;
  Hiscox is a defensible default in the EU and UK. Budget
  $50-200/mo. Larger customers will literally require proof of
  coverage before signing — having the certificate ready is the
  difference between closing in 2 weeks and closing in 2 months.
- **Optional but useful:** Pylon or Plain for shared Slack-style
  support channels with each customer; Cal.com for booking;
  1Password for credential sharing with contractors; Sentry for
  the FastAPI services you ship; Tailscale for accessing
  customer hardware behind their firewalls (with their
  permission, in writing).

The pattern: every tool on this list is one a competent web-dev
agency would already use. You are not learning a new tool stack;
you are learning a new domain to point the existing stack at.

---

## Sample contract clauses to insist on

Not legal advice — get a real lawyer for $500-1500 to write your
template. But the clauses below are the ones perception-specific
work tends to need that a generic web-dev contract does not
cover.

- **IP ownership of generic code stays with you.** The Docker
  base image, the FastAPI scaffolding, the React upload UI, the
  evaluation harness — all yours, reusable across customers. The
  customer gets a non-exclusive license to use them as part of
  the deliverable. Without this clause every project starts
  from zero.
- **Per-customer fine-tuned weights belong to the customer.**
  The pose model trained on their CAD files, the anomaly
  detector trained on their defect images, the calibration files
  for their specific rig — those are theirs, transferable,
  deletable on request. This makes the conversation easy and
  signals you are not trying to lock them in.
- **Data they upload is theirs, but you can use anonymized
  aggregate metrics.** "Average inference latency across all
  customers" and "frequency of common failure modes" are yours;
  the underlying images and CAD files are not. This lets you
  publish leaderboards, write blog posts, and improve your
  default pipelines without ever touching customer data
  directly.
- **30-day notice on subscription cancellation.** Standard, but
  worth naming explicitly. Customers can cancel any time; you
  bill for the next 30 days; you hand back their data within
  14 days of termination.
- **Force-majeure clause for upstream model breakage.** If
  Hugging Face pulls a model, NVIDIA changes the FoundationPose
  license, Meta restricts SAM 2, or a vendor's API goes dark,
  you are not in breach. You commit to a "best-effort
  replacement within 60 days" and the customer commits to
  accept a reasonable substitute. This is a real risk that
  generic SaaS contracts do not contemplate.
- **Limitation of liability capped at fees paid in the last 12
  months.** Standard SaaS clause. Without it a single
  bin-picking failure that damages a robot arm could end your
  agency.

---

## The 12-month agency growth path

A realistic, not heroic, calendar for going from "web dev with
spare evenings" to "small perception agency with paying
customers and a clear path to hiring."

- **Months 1-2: free pilots.** Pick one of the six projects
  (visual inspection or calibration concierge are the lowest-
  friction starts). Build the end-to-end pipeline on public
  data. Run two or three free pilots for whoever will say yes —
  a friend's robotics startup, a small manufacturer you
  cold-emailed, anyone. The goal is not revenue; it is two
  outcomes you can show ("we caught 92% of defects on their
  test set," "we reduced their reprojection error from 1.4px
  to 0.3px") and one written testimonial.
- **Months 3-6: first paid project.** Convert one of the free
  pilots, or sell a fresh discovery phase to a new prospect.
  Your goal is one paid $5-15k engagement that finishes on
  time, on budget, and with a referenceable customer. By the
  end of month 6 you should have $5-15k in revenue, one case
  study, and a small backlog of warm leads from referrals.
- **Months 6-9: second project plus the recurring layer.** Sell
  a second paid project — ideally to a different vertical so
  you are not over-fitting to one buyer profile. Simultaneously,
  convert your first customer onto a recurring subscription
  (support, re-training, or calibration retainer). The goal
  is your first $1-3k of MRR alongside the project revenue.
  This is also when you formalize the discovery-phase template,
  the proposal template, and the master services agreement.
- **Months 9-12: first contractor or co-founder.** By now you
  are juggling two or three active customers and getting
  inbound from referrals. Hire your first part-time contractor
  — either a perception specialist (if the bottleneck is model
  quality) or a generalist engineer (if the bottleneck is
  shipping integrations). Or find a co-founder if you would
  rather build a real company than a lifestyle agency. By the
  end of month 12 you should be at $5-15k MRR, two to four
  active customers, one contractor or co-founder on the team,
  and a defensible niche (one vertical you know better than
  anyone else who is small enough to take the call).

The honest framing: a year of this is enough to know whether
you have a real business. If at month 12 you have one paying
customer and no MRR, the model is not working and you should
either change tactics (different project, different vertical,
different price point) or fold the agency and take the
perception-engineer job that is now on the table because you
have a portfolio. Either outcome is fine — both beat the
counterfactual of staying a generic web dev for another year.

---

## How to pick which one to start with

- **Cheapest to start, fastest to revenue:** #3 (visual inspection)
  and #6 (calibration concierge). Both are pure software with
  enormous customer pools and short sales cycles.
- **Most defensible long-term:** #2 (6-DoF pose API). Each customer's
  fine-tuned model and accuracy benchmarks are your moat.
- **Highest ceiling:** #1 (phone-scan to digital twin) and #5 (Unity
  plugin). If digital twins of customer sites become a default
  robotics workflow, #1 is acquired by NVIDIA / Matterport /
  Polycam. If spatial computing becomes ubiquitous, #5 is acquired
  by Unity / Niantic / a headset OEM.
- **Easiest to charge premium for:** #4 (SLAM tuning). One report
  pays for a month of your time; harder pipeline to keep busy.
- **Most boring and therefore most reliable:** #6 (calibration
  concierge). No moat, no glamour, no acquisition story — just
  steady $200/mo per rig from customers who would rather not
  think about it. The most underrated project on the list.

A reasonable default mix once you have momentum: one of {#3, #6}
as the recurring-revenue base, one of {#1, #5} as the
high-ceiling play, and one of {#2, #4} as the premium consulting
arm. Three projects, three customer segments, one agency.
