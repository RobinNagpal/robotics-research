# Six Projects You Can Build and Sell

Each scoped to 2-4 weeks of solo work, with a concrete buyer, and
reusing skills a web developer already has (FastAPI / Express, Docker,
GitHub Actions, Postgres, React). Perception-specific parts are
flagged.

Pricing ranges below are realistic for **2025-2026 in North America /
Western Europe**. Robotics primes and AV teams pay the high end;
seed-stage startups and manufacturing SMBs pay the low end. Cross-
cutting advice on discovery scoping, pricing, agency tooling,
contracts, and the 12-month growth path lives in the meta sections at
the end — per-project entries assume you have read those.

Cross-references: `00-basics.md` for vocabulary, `01-examples.md` for
code snippets, `02-learn.md` for the 12-week curriculum, `03-start.md`
for the zero-to-first-commit ramp, `04-employers.md` for who is
buying, `06-courses.md` for deeper ML study.

---

## 1. Phone-scan to robot-ready 3D environment (~4 weeks)

**What you're selling.** A web service: the customer walks a room
with their phone for 5 minutes, uploads the video, and 20 minutes
later receives a Gaussian splat + collision mesh + per-object
semantic segmentation, packaged as USD or URDF that loads directly
into Isaac Sim or Gazebo. One URL, one upload field, one
notification, one download.

**Why it works.** Every robotics startup needs digital twins of
customer sites for sim2real training, sales demos, and validation.
Hiring a 3D artist or flying an engineer on-site costs $5-20k each
time. Polycam and Matterport target real-estate and AEC; nobody
targets robotics-grade capture with URDF joints, semantic labels,
and a physics-friendly collision proxy. You are not competing with
Polycam — you are competing with a roboticist hand-authoring a
kitchen in Blender on a Saturday.

**Stack:**
- iPhone capture with Polycam, Scaniverse, or a custom ARKit app.
- COLMAP or glomap for structure-from-motion.
- Nerfstudio + gsplat for splat training.
- SAM 2 for semantic masks fused across views.
- Open3D for collision-proxy mesh extraction.
- USD / URDF export via `usd-core` and NVIDIA's `pxr`.
- React + FastAPI front-end, S3-backed job queue, Stripe billing.

**Pricing:** $1-5k per scene or $500/mo subscription. Matterport
pro sits in the few-hundred range per scan, Polycam pro at ~$20/mo
— buyers will accept a 5-10x premium once they realize neither
ships a URDF.

**Sales angle.** "I turn a 5-minute phone walkthrough of your
customer's warehouse into an Isaac-Sim-ready USD file so your sales
engineer stops spending Fridays in Blender."

**Hardest part.** Capture-failure debugging — bad lighting, motion
blur, reflective surfaces, sparse texture. You will need a
re-capture instruction template and a human QA pass on every
delivery for the first 20 scenes.

---

## 2. 6-DoF pose-estimation API for industrial parts (~3 weeks)

**What you're selling.** The customer uploads a CAD model. Your
service generates synthetic training data, fine-tunes
**FoundationPose** or **MegaPose**, and returns a Dockerized REST
endpoint that takes an RGB-D image and returns a 6-DoF pose. The
integrator drops the STEP file into a web form; 30-60 minutes later
they get a `docker pull` command and a diagnostic if accuracy fell
short ("symmetric on Z axis, plateaued at 14mm, add a fiducial or
secondary view").

**Why it works.** Bin-picking integrators (Pickle, Kindred, hundreds
of system integrators worldwide) are constantly asked to add new
SKUs. The right answer used to be a multi-week PhD project per SKU
— FoundationPose changed that, and most integrators haven't
internalized it. Integrators currently pad $15-50k of "perception
engineering" into each cell quote to cover unknown future SKUs. If
you collapse that to a predictable $2-10k per SKU with a turnaround
SLA, you become a line item in their proposal, not a competitor.

**Stack:**
- FoundationPose (NVIDIA, Apache 2.0) as the base model.
- BlenderProc or Isaac Sim Replicator for synthetic data.
- NVIDIA Triton Inference Server, or FastAPI + ONNX Runtime.
- Docker image as the deliverable.
- Optional React dashboard for CAD upload, accuracy monitoring,
  re-training.

**Pricing:** $2-10k setup per part, plus $0.01-0.10 per inference
or a $500-2k/mo flat plan. The metered tier mostly exists as
psychological anchoring — most customers pick the flat fee — but
quoting both signals "real API product" rather than one-off
contracting and raises the whole proposal's ceiling.

**Sales angle.** "I add new SKUs to your bin-picker in 48 hours for
a flat fee, so your perception lead stops being a ticket-closer."

**Hardest part.** Shiny and textureless metal parts (the perennial
bane of vision-based pose). Have a mitigation ready: structured-
light sensor, tactile retry, or secondary-view fusion. The
secondary villain is synthetic-to-real domain gap — budget a week
of every engagement for on-site data collection and a re-tune on
100-500 real images, and frame it to the customer as a feature
("the system gets smarter the more it sees your line").

---

## 3. Visual-inspection-as-a-service (~2-3 weeks)

**What you're selling.** A web UI where a small-to-mid manufacturer
uploads 50-100 "good" and 50-100 "bad" product images. Your service
trains an anomaly detector (PatchCore, EfficientAD, or DINOv2 + kNN)
and returns a Docker container with a REST endpoint. The customer
drops it onto their line PC.

**Why it works.** QC departments at PCB shops, food packers, fabric
mills, and parts suppliers pay well and have **zero ML staff**.
Their existing choices are a $50k+ Cognex/Keyence system or doing
nothing. You undercut Cognex and beat "doing nothing" by miles.
The quality manager's whole performance metric is escape rate, and
they have clean ROI math: defects caught cost $X to scrap, defects
shipped cost $10X-100X. A demo on their own images that catches 90%
of known defects is selling them their bonus.

**Stack:**
- `anomalib` (OpenVINO, MIT) for the model zoo.
- DINOv2 + nearest-neighbor on embeddings as a strong baseline that
  often beats supervised approaches at this data scale.
- ONNX or TensorRT export for deployment speed.
- Docker image, FastAPI endpoint, React upload UI, Stripe billing.

**Pricing:** $5-25k per defect class deployed, plus $200-1000/mo
support and re-training. Pure software, recurring revenue, no
on-site work.

**Sales angle.** "I bolt a Cognex-equivalent defect detector onto
your line for one tenth the price, and you can run it before your
next shift change."

**Hardest part.** Explaining evaluation in plain English. You will
spend more time saying "we catch 94 of every 100 defects and
false-alarm 3 times per 1000 good parts" than you spend on the
model. Build one slide that maps precision/recall onto dollars and
reuse it in every pitch.

---

## 4. Real-time SLAM benchmark and tuning service (~3 weeks)

**What you're selling.** Customer uploads a ROS bag or any video +
IMU. Your service runs **ORB-SLAM3**, **VINS-Fusion**, and
**DROID-SLAM** with several parameter sets, evaluates each against
ground truth (if available) or self-consistency loop closures (if
not), and returns a tuning report with ranked recommendations.
Deliver both formats: a PDF for the VP of Engineering and a Git
repo with a `Makefile` for the perception engineer. Selling both is
the difference between a $2k report and a $5k report.

**Why it works.** Drone, AMR, and AR startups have engineers who
can tune one SLAM stack but rarely have bandwidth to comparison-
shop across the four big options. The one-off report is the lead
magnet; the real product is a GitHub Action that runs the same
sweep nightly against firmware builds and comments on PRs.

**Stack:**
- `evo` for trajectory comparison.
- Pinned Docker images for ORB-SLAM3, VINS-Fusion, OpenVSLAM,
  DROID-SLAM.
- Parameter sweep harness (Ray Tune or a YAML matrix).
- WeasyPrint or Puppeteer for the PDF report.
- GitHub Actions integration for nightly runs.

**Pricing:** $2-5k per benchmark report, $500-2k/mo for CI.

**Sales angle.** "I will tell you in two weeks whether your SLAM
stack is the bottleneck on your demo, and which open-source
alternative would beat it, with numbers."

**Hardest part.** Ground truth. Most customers have no motion-
capture or RTK-GPS rig, so you cannot definitively say "A is more
accurate than B." Lean on relative metrics (loop-closure error,
scale drift, ATE against a fused reference) and have a one-page
explainer ready — you will email it constantly.

---

## 5. AR scene-understanding Unity plugin (~3-4 weeks)

**What you're selling.** A `.unitypackage` file that exposes a real-
time mesh + semantic segmentation feed from any RGB or RGB-D camera
the Unity app can access. Under the hood it wraps SAM 2 and
Depth-Anything v2, both running locally via ONNX Runtime, with a
thin C# API exposing `SceneMesh` and `SemanticLabels` per frame.
The developer drags a prefab into a scene, hits play, and sees
colored bounding volumes around chairs and walls. No Python, no
model downloads, no CUDA setup. Unreal port as a stretch.

**Why it works.** Small game studios, training-sim shops, and
location-based-VR operators want "Meta Quest passthrough but
smarter" without staffing a perception team. Native ARKit/ARCore
scene understanding has plateaued, Vision Pro is locked to one
device, and cross-platform Unity developers have nothing. The
Asset Store has trained game studios to spend $50-500 on tools and
$5-50k on custom integrations — you sit one tier above the default.

**Stack:**
- Unity 2022 LTS or 6 as the target; Unreal 5.x as a stretch.
- ONNX Runtime with DirectML/CUDA on Windows, CoreML on Mac/iOS,
  NNAPI on Android.
- SAM 2 (int8-quantized ONNX) for segmentation, Depth-Anything v2
  small for depth.
- C# wrapper marshalling textures into ONNX tensors and back into
  `Mesh` / `Texture2D`.
- Sample scene that segments a webcam feed — your demo and README
  in one.
- Per-seat license keys checked against a small FastAPI endpoint.

**Pricing:** $5-30k per integration, plus $1-5k/mo for support,
model updates, and Unity LTS compatibility patches. Some studios
prefer a perpetual license at $10-20k — offer both.

**Sales angle.** "I drop a real-time mesh-and-semantics layer into
your Unity project this month, so your demo at GDC actually
understands the room instead of just seeing it."

**Hardest part.** Real-time performance budget. Studios will not
accept 100ms per frame when their entire frame budget is 16ms.
Most of the engagement is quantization, distillation, frame-
skipping, and "only re-segment when the camera moves enough"
tricks. The SAM 2 wrapper is easy; fitting it into a game loop is
not.

---

## 6. Camera-calibration concierge service (~ongoing, no project end)

**What you're selling.** The most boring possible product, which is
why nobody else sells it: a recurring camera-calibration service
for robotics startups. Customer joins a 30-minute Zoom (or ships
the rig); you walk their tech through a ChArUco capture; you mail
back a YAML file (intrinsics, distortion, hand-eye, stereo
extrinsics), a 3-page validation report, and a 90-day calendar
reminder. When the reminder fires, you do it again, on a
subscription. You are not selling capability; you are selling
discipline-as-a-service.

**Why it works.** Every perception lead at a 5-50 person robotics
startup has calibration on their backlog. It never ships because it
is never the most important thing. Meanwhile the stereo baseline
has drifted, the hand-eye is off by half a degree, and grasp
success is mysteriously down 8% from last quarter. Same logic as a
payroll provider: the math is not hard, but the calendar discipline
and the audit trail are worth the monthly fee.

**Stack:**
- OpenCV for intrinsics and stereo, Kalibr for IMU-camera, standard
  hand-eye (Tsai, Park, Daniilidis) with a clean Python wrapper.
- A printable ChArUco/AprilTag board mailed to customers with a
  QR-coded serial number per rig.
- S3 + presigned URLs for async video upload.
- WeasyPrint or ReportLab report generator (same template every
  time, only numbers change).
- Airtable + cron for CRM and reminders; HubSpot or Attio at 20+
  rigs.

**Pricing:** $1-2k one-time per rig, $200/mo retainer per rig
(quarterly re-calibration, Slack channel, written incident report
if validation fails). Volume discounts at 10+ rigs per customer.

**Sales angle.** "Your stereo calibration drifted 3 weeks ago and
you have not noticed; I will catch it next time, and the time after
that, for $200 a month."

**Hardest part.** No hard technical part, which is also the trap.
The hard part is operations: shipping boards, tracking serials,
scheduling across time zones, chasing customers who skip a quarter,
keeping a tidy audit trail. Treat this like running an accounting
firm.

---

## How to scope a discovery phase

Before any of the six projects, sell a discovery phase first. Short,
fixed-fee, explicitly de-risking both sides before anyone commits
to a full build.

**Template:**

- **Duration:** 1-2 weeks, never longer.
- **Price:** $2-5k flat, paid up front (50/50 on signing/delivery
  if their procurement insists).
- **Deliverable 1:** A 5-10 page written assessment — what they
  actually need, what the literature says is possible, realistic
  accuracy/latency/cost numbers. Structured, opinionated,
  decision-ready.
- **Deliverable 2:** A working proof-of-concept notebook that runs
  end-to-end on a sample of their data. Not production code; a
  demonstration that the hard parts are not show-stoppers.
- **Deliverable 3:** A fixed-fee quote for the full build with
  three scope options (minimum viable, recommended, all the
  bells). Each has a price, timeline, and explicit out-of-scope
  list.

About a third of customers will see the assessment and decline to
proceed, which is the best possible outcome — they keep the value,
you keep the cash and the case study, neither side sinks 8 weeks
into a doomed engagement. The discovery phase also shifts how
customers price you mentally: a fixed-fee build off a 30-minute
call is a freelancer; insisting on discovery first is a
consultancy.

---

## Pricing principles

1. **Charge per outcome, not per hour.** Transferring risk to you
   is what customers pay for. Per-hour caps your upside at "fast
   typist with a PhD."
2. **Always sell discovery before quoting a build.** Especially
   when the customer is impatient — those are the ones with
   unrealistic expectations that blow up fixed-fee margins.
3. **Line-item recurring revenue separately from setup.** Setup is
   the wedding, subscription is the marriage. Customers accept
   recurring fees when named clearly ("re-training subscription,"
   "calibration retainer," "uptime SLA"); they resent fees buried
   in setup.
4. **Anchor against Cognex, Keyence, Matterport, Polycam.** Hedge
   ("comparable industrial vision starts in the $40-80k range")
   rather than quoting unpublished competitor numbers.
5. **Raise prices 25% every 3 paying customers.** Confidence lags
   reality; this rule corrects it. Four iterations nearly triples
   pricing, and customers paying the higher rate are still getting
   a bargain versus in-house.

---

## Tooling stack for the agency

- **Analytics:** Posthog or Plausible.
- **Project management:** Linear.
- **Async demos:** Loom. Weekly check-ins should be a Loom plus
  written summary unless the customer asks for live time.
- **Client wikis:** Notion or Obsidian Publish, one workspace per
  customer with architecture, calibration files, checkpoints,
  changelog.
- **Billing:** Stripe + Stripe Tax (the underrated one — handles
  VAT, GST, US sales-tax automatically).
- **Legal entity:** US LLC, or Stripe-Atlas-equivalent locally
  (Tide, Mercury, Wise Business). One entity, one bank account,
  one bookkeeping system from day one.
- **Insurance:** professional liability / E&O. Vouch.us in the US,
  Hiscox in EU/UK. Budget $50-200/mo. Larger customers require
  proof of coverage before signing.
- **Optional:** Pylon or Plain for shared customer Slack channels;
  Cal.com for booking; 1Password for contractor credentials;
  Sentry for the FastAPI services; Tailscale for accessing
  customer hardware (with written permission).

---

## Sample contract clauses to insist on

Not legal advice — get a lawyer for $500-1500 to write your
template. The clauses below are the perception-specific ones a
generic services contract does not cover.

- **Generic code IP stays with you.** Base Docker image, FastAPI
  scaffolding, React UI, evaluation harness — yours, reusable.
  Customer gets a non-exclusive license.
- **Per-customer fine-tuned weights belong to the customer.** Pose
  models on their CAD, anomaly detectors on their defects,
  calibration files for their rig — theirs, transferable,
  deletable on request.
- **Customer data stays customer data; you keep anonymized
  aggregate metrics.** Average inference latency, frequency of
  failure modes — yours. Underlying images and CAD — theirs.
- **30-day cancellation notice; 14-day data return on
  termination.**
- **Force-majeure for upstream model breakage.** If Hugging Face
  pulls a model, NVIDIA changes the FoundationPose license, or
  Meta restricts SAM 2, you are not in breach. Commit to a
  best-effort replacement within 60 days.
- **Liability capped at fees paid in the last 12 months.** Standard
  SaaS clause; without it a single bin-picking failure that
  damages a robot arm ends your agency.

---

## The 12-month agency growth path

- **Months 1-2: free pilots.** Pick one project (visual inspection
  or calibration concierge are lowest-friction). Build the pipeline
  on public data. Run 2-3 free pilots for whoever says yes. Goal:
  two outcome metrics you can quote and one written testimonial.
- **Months 3-6: first paid project.** Convert a pilot or sell a
  fresh discovery. Target: one $5-15k engagement that finishes on
  time, on budget, referenceable. End of month 6: $5-15k revenue,
  one case study, a backlog of warm referrals.
- **Months 6-9: second project plus recurring layer.** Sell a
  second paid project in a different vertical. Convert your first
  customer onto a subscription. Target: first $1-3k MRR alongside
  project revenue. Formalize the discovery template, proposal
  template, and master services agreement.
- **Months 9-12: first contractor or co-founder.** With 2-3 active
  customers and inbound referrals, hire a part-time contractor
  (perception specialist if model quality is the bottleneck,
  generalist if shipping is). Or find a co-founder if you want a
  real company rather than a lifestyle agency. End of month 12:
  $5-15k MRR, 2-4 active customers, one teammate, a defensible
  vertical.

Honest framing: a year of this tells you whether the model works.
If month 12 has one customer and no MRR, change tactics or fold
the agency and take the perception-engineer job that is now on the
table because you have a portfolio. Both beat staying a generic
web dev for another year.

---

## How to pick which one to start with

- **Cheapest to start, fastest to revenue:** #3 (inspection), #6
  (calibration concierge). Pure software, huge pools, short
  cycles.
- **Most defensible long-term:** #2 (pose API). Each customer's
  fine-tuned model and accuracy benchmarks are your moat.
- **Highest ceiling:** #1 (phone-scan to digital twin), #5 (Unity
  plugin). Acquirers: NVIDIA/Matterport/Polycam for #1; Unity/
  Niantic/headset OEMs for #5.
- **Easiest premium:** #4 (SLAM tuning). One report pays for a
  month; harder pipeline to keep busy.
- **Most boring, most reliable:** #6. No moat, no glamour, no
  acquisition story — just steady $200/mo per rig from customers
  who would rather not think about it.

A reasonable default mix once you have momentum: one of {#3, #6}
as the recurring base, one of {#1, #5} as the high-ceiling play,
one of {#2, #4} as the premium consulting arm. Three projects,
three customer segments, one agency.
