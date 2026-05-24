# Perception & Computer Vision — The Basics

> Written for a web developer who has never touched a robot. Read
> this before the other files in this folder.

## What is this field, in detail?

A robot is blind until perception code turns its raw sensor data —
camera pixels, LiDAR returns, depth maps, IMU readings — into
**structured knowledge of the world**. Specifically: "there is a red
mug at world coordinates (1.23, -0.45, 0.78), oriented 30 degrees
off-axis, sitting on a table 80 cm in front of me, and the detected
human face is looking away."

If LLMs are about understanding language, perception is about
understanding the physical scene in front of a robot, accurately
enough that downstream code (motion planner, grasp selector, safety
monitor) can act on it without crashing into things or breaking the
part it just picked up.

Think of perception as the parse + hydrate layer of the robot's
app: sensors emit a firehose of bytes; perception is the
`JSON.parse` + schema validator + reducer producing a typed 3D
world-state that every downstream consumer reads. Garbage in,
garbage everywhere downstream.

Flashy demos (a humanoid pouring coffee, a Waymo doing a California
stop) work because the perception stack made the scene legible.
Most robotics startups that fail do so because perception was 80%
reliable when it needed to be 99.5%.

### How perception differs from "computer vision"

Computer vision spans Instagram filters, medical imaging, and
satellite analysis. **Robotics perception** is CV with extra
constraints:

- **Real-time.** Most perception runs at 10-60 Hz. A 200 ms delay
  can crash a quadcopter or topple a bipedal robot. The frame
  budget (16.6 ms at 60 Hz, 33 ms at 30 Hz, 11 ms at 90 Hz) is a
  contract, not a target.
- **Geometry-aware.** Output is a 3D pose / mesh / trajectory, not
  just a label. "It's a chair" isn't enough; you need where the
  seat is, where the legs are, which way the back faces.
- **Multi-sensor.** Production robots fuse RGB + depth + IMU + LiDAR
  + sometimes radar. Time-syncing and cross-calibrating these
  sensors is most of the engineering work. A 5 ms misalignment can
  move a pedestrian by 30 cm at highway speed.
- **Edge-deployed.** Inference runs on a Jetson, an embedded RTX, or
  custom silicon — not on an A100 in a data center. Model size and
  TensorRT optimization matter.
- **Safety-critical.** A misclassification on a Tesla isn't bad UX,
  it's a crash. Perception engineers do failure-mode analysis the
  way frontend devs handle bug tickets, except the "P0" can be a
  recall.

### Coordinate frames: the part nobody warned you about

A *coordinate frame* is just an origin point plus three axes (X, Y, Z).
The same physical point in space gets different numerical coordinates
depending on which frame you describe it in. "The mug is at
(1.2, 0.3, 0.8)" is meaningless unless you also say "in the robot's
base frame" or "in the camera frame" or "in the world frame."

Every sensor, joint, and object has its own frame. The camera thinks
"+Z forward, +X right, +Y down" (OpenCV's convention); ROS thinks
"+X forward, +Y left, +Z up"; the arm base has its own; the world
has yet another. A *transform* is the 4×4 matrix that converts a
point from one frame to another.

The `tf2` library tracks every frame on the robot in a tree
(`world` → `base_link` → `arm_link_1` → ... → `camera_color_optical_frame`)
and lets you ask "give me the transform from `base_link` to
`camera_color_optical_frame` as of timestamp T." It does the matrix
multiplications down the tree for you.

You will spend an embarrassing amount of your first year converting
between frames. Two common bug-classes: forgetting to wait for a
transform to become available at startup (your first query returns
garbage); and silently mixing two different conventions (a 90°
rotation between OpenCV and ROS frames produces sideways detections
that look almost right but are completely wrong).

### The four canonical perception sub-problems

Almost every robotics perception task is one of these four, or a
combination of them. Here is each one in plain English, with what
goes in and what comes out.

---

#### 1. Detection and segmentation — "what is in the picture, and which pixels are it"

**Plain-English definition.** Look at a 2D image and find every
object of interest in it. *Detection* draws a rectangle (a "bounding
box") around each object and labels it. *Segmentation* goes further
and tells you exactly which pixels belong to which object.

Two flavors of segmentation worth distinguishing:

- **Semantic segmentation** labels every pixel by class ("road",
  "pedestrian", "sky"). It does not separate one pedestrian from
  another — they are all just "pedestrian pixels."
- **Instance segmentation** separates two of the same thing. This
  is *pedestrian #1*, that is *pedestrian #2*, each with its own
  mask. This is what a robot usually needs (you grasp one specific
  cup, not "the cup pixels in general").

**Why a robot needs it.** Before a robot can pick up a cup it has
to know which pixels in the camera image are "cup" and which are
"table" or "background." Without that, the grasp planner has no
surface to aim for.

**Inputs and outputs.**

- *Input:* one RGB image, shape `H × W × 3` (height × width × 3
  color channels).
- *Output:* a list of detections. Each detection has a class label
  ("cup"), a confidence score from 0 to 1, a bounding box (4
  numbers: x, y, width, height in pixels), and optionally a mask
  (an `H × W` boolean array where `True` means "this pixel is part
  of this object").

**Concrete example.** A warehouse robot looks at a shelf. The
detector returns something like
`[{label: "box", conf: 0.98, bbox: [120, 80, 200, 150], mask: <H×W bool array>}, ...]`
— one entry per item on the shelf. The mask tells the grasp planner
exactly which pixels are "this box" vs. "the shelf behind it."

**Models worth knowing.** YOLO v8 / v11 (fast, fine-tune on your own
data), DETR (transformer-based detection), Mask2Former (segmentation),
SAM 2 (Meta's universal "click a point, get a mask" model).

**Try it locally.**

```bash
pip install ultralytics
```
```python
from ultralytics import YOLO
model = YOLO("yolov8n.pt")        # downloads ~6 MB the first time
results = model("my_photo.jpg")
results[0].show()                 # opens the image with boxes drawn
```

For SAM 2 via Hugging Face, load `facebook/sam2-hiera-large` with
`transformers.Sam2Model.from_pretrained(...)`.

---

#### 2. 6-DoF pose estimation — "where in 3D is this object, and which way is it facing"

**Plain-English definition.** Given an image of a known object (a
power drill, a specific bracket, a SKU), figure out exactly where it
sits in 3D space *and* how it is rotated.

**What "6-DoF" means.** Six Degrees of Freedom — three numbers for
position (x, y, z, in meters) and three for orientation (roll,
pitch, yaw — the rotation around each axis). Together they fully
describe "where the object is and how it is oriented" in 3D.

**Why a robot needs it.** To grasp something, the gripper has to
approach from the right angle. "The cup is somewhere in front of me"
is not enough; you need "the cup's handle is 25 cm forward, 5 cm to
the left, at table height, tilted 30° to the right." The inverse-
kinematics solver that drives the arm wants exactly one target pose
to plan toward.

**Inputs and outputs.**

- *Input:* an RGB or RGB-D image, plus (usually) a CAD mesh of the
  object you are looking for.
- *Output:* a single 4×4 transform matrix, written `T_camera_object`.
  This matrix mathematically describes "to convert any point that
  is expressed in the object's coordinate frame into the camera's
  coordinate frame, multiply it by this matrix." The matrix packs
  rotation (its top-left 3×3 block) and translation (its rightmost
  3×1 column) into one tidy object.

**Concrete example.** A robot arm needs to pick up a power drill.
The camera sees the drill at frame K. FoundationPose returns
`T_camera_drill`. The grasp planner already knows, in the drill's
own local frame, that the handle is at point `(-0.05, 0, 0.10)`.
Multiplying that point by `T_camera_drill` turns it into a 3D
location in the camera's frame. The arm controller then drives the
gripper there.

**Models worth knowing.** FoundationPose (NVIDIA, 2024 — the current
default; works on novel objects given only a CAD model), MegaPose
(2022), GigaPose, FFB6D (older, learned per-object).

**Try it locally.** FoundationPose has no `pip install` shortcut —
it's research code. Clone and follow the conda environment:

```bash
git clone https://github.com/NVlabs/FoundationPose
```

---

#### 3. Depth and 3D reconstruction — "how far is everything, and what does the room look like in 3D"

This is really two related-but-distinct problems. Both produce 3D
information from images, but at different time scales.

##### 3a. Depth estimation (real-time, per-frame)

**Plain-English definition.** Take a single image and predict the
distance from the camera to whatever surface is visible at each
pixel.

**Inputs and outputs.**

- *Input:* one RGB image, shape `H × W × 3`.
- *Output:* one depth map, shape `H × W`, where each value is the
  distance in meters. A pixel value of `5.2` means "the surface
  visible at this pixel is 5.2 m from the camera."

**Why a robot needs it.** Depth tells the robot what is reachable,
what is an obstacle, and how to plan a collision-free path. Many
depth-camera sensors (Intel RealSense, Orbbec, iPhone LiDAR) give
this directly. When you only have a regular RGB camera, a neural
net like Depth-Anything v2 predicts it.

**Try it locally.**

```python
from transformers import pipeline
depth = pipeline(
    task="depth-estimation",
    model="depth-anything/Depth-Anything-V2-Small-hf",
)
out = depth("my_photo.jpg")
out["depth"].save("depth.png")     # grayscale: brighter = closer
```

##### 3b. 3D reconstruction (offline, from many images)

**Plain-English definition.** Given a bunch of overlapping photos of
the same scene from different angles, figure out (a) where each
photo was taken from, and (b) build a 3D model of the scene (point
cloud, mesh, NeRF, or Gaussian splat).

**Inputs and outputs.**

- *Input:* N overlapping RGB images, typically 20-200.
- *Output:* N camera poses (one 4×4 transform per photo, saying
  where the camera was when it took that photo) plus a 3D model of
  the scene. The model is usually a point cloud — a list of
  millions of 3D points with colors — or a Gaussian splat.

**Why a robot needs it.** This is how you build a digital twin of a
customer's warehouse for simulation training, how a drone team
turns a vineyard flyover into a 3D crop-yield model, or how an AR
app reconstructs your living room.

**Concrete example.** A drone flies over a vineyard taking 200
overlapping photos. COLMAP estimates each camera pose and
reconstructs a dense point cloud, which is then used to count
grape clusters and predict yield.

**Tools worth knowing.** COLMAP and glomap (classical structure-
from-motion, the workhorse tools), Nerfstudio (NeRF training),
gsplat / Nerfstudio's `splatfacto` (Gaussian Splatting — the
current default for photoreal output), VGGT (2025, feed-forward
transformer that skips the optimization step).

---

#### 4. SLAM — "where am I, and what does the world look like, both at the same time"

**Plain-English definition.** While a robot is moving, two questions
need to be answered together: "where am I right now?" and "what
does the world around me look like?" *SLAM* (Simultaneous
Localization and Mapping) solves both at the same time, from a
stream of camera (and usually IMU) data.

**Why it is hard.** A robot indoors has no GPS. The only data is the
moving camera. The catch is circular: knowing where you are needs a
map, and building a map needs to know where you are. SLAM breaks
this chicken-and-egg by keeping both estimates and continually
refining them together with an optimization called *bundle
adjustment*.

**Why a robot needs it.** A Roomba maps your apartment. A delivery
robot localizes on an existing map. A drone needs to know if it has
drifted from its planned path. Vision Pro keeps your virtual
monitors fixed in space while you walk around.

**Inputs and outputs.**

- *Input:* a continuous stream of camera images, usually plus IMU
  data (200 Hz accelerometer + gyroscope readings).
- *Output (updated every frame):* (a) the robot's current pose as a
  4×4 transform from world frame to robot frame, and (b) a map —
  usually a sparse 3D point cloud of "landmarks" the SLAM system
  has recognized and can re-find later.

**Related but lighter problems.**

- *Visual Odometry (VO):* the "where am I" part only. No reusable
  map.
- *Visual-Inertial Odometry (VIO):* VO plus IMU fusion. The
  workhorse for fast-moving robots like drones.
- *Full SLAM:* VO + a map you can come back to and *re-localize*
  against later.

**Concrete example.** A Roomba-like robot enters a new apartment.
Visual-inertial SLAM builds an occupancy map as it drives while
estimating its own pose to a few centimeters, so it can return to
the dock when the battery is low.

**Tools worth knowing.** ORB-SLAM3 (the canonical C++ classical
implementation), VINS-Fusion (visual-inertial), DROID-SLAM (modern
learned), Spectacular AI (commercial, easy SDK).

**Try it locally.** SLAM is mostly C++. Clone and build with CMake
against OpenCV + Pangolin + Eigen:

```bash
git clone https://github.com/UZ-SLAMLab/ORB_SLAM3
```

Python-friendly option:

```bash
git clone https://github.com/princeton-vl/DROID-SLAM
```

---

Most real pipelines combine 2-3 of these. A warehouse arm uses
**detection + 6-DoF pose**. A drone uses **SLAM + depth**. An AV
uses **all four**.

### Why this is one of the most reliable robotics specialties

- **Broadest customer base.** Every robot, drone, AV, AR headset,
  inspection rig, and security camera needs perception. You can
  sell into warehouses, hospitals, farms, defense, automotive, and
  AR with overlapping skills.
- **Foundation models changed everything.** SAM 2 (Meta, 2024),
  DINOv2 (Meta, 2023), Depth-Anything v2 (2024), FoundationPose
  (NVIDIA, 2024) turned problems that required PhD-level expertise
  in 2020 into "load the model from Hugging Face and call it."
- **Strong pay bands.** Robotics Software Engineer median is $189k
  (2025 Robotics Salary Guide); perception specialists at AV / AR
  shops clear $300k+ TC.

### What the day-to-day work looks like

- **Sensor calibration.** Intrinsics and extrinsics. Camera-to-camera,
  camera-to-IMU, camera-to-LiDAR. Lots of Kalibr, lots of
  checkerboards. Get a unit wrong (mm vs m) or flip an axis and
  every downstream consumer is silently wrong forever.
- **Pipeline building.** Wiring detection -> tracking -> 3D
  triangulation -> SLAM -> map publication, in ROS2 or proprietary
  middleware. A ROS2 topic is a typed pub/sub channel — like a
  Kafka topic, but with `.msg` files and QoS knobs.
- **Model integration.** Taking a research model (SAM 2,
  FoundationPose, ORB-SLAM3) and making it run at 30+ Hz on a Jetson
  with TensorRT.
- **Failure-mode triage.** A black object on a black background, a
  depth camera dying in sunlight, SLAM diverging in a featureless
  hallway.
- **Data pipelines.** Collecting, labeling, augmenting, validating.

About 60% Python, 40% C++ (most production SLAM and high-rate
perception is C++).

---

## Three real-world projects a 5-10 dev shop ships for clients

These are the shape of CV / perception work that a small-to-mid
services agency actually sells and delivers. Each one starts with
**Public references** naming real shops and clients that have
published work in this category, so you can look up the
case-studies yourself. The detailed project below is the typical
pattern those references describe, scaled to a 5-10 dev shop's
engagement size.

---

### Use case 1 — Production-line visual quality inspection

**Public references.** This is the most-documented category of CV
agency work. Real shops with public case studies on this pattern:

- **Landing AI** (Andrew Ng's company) — case studies with Foxconn
  (phone-assembly defect inspection), Bombardier (aluminum panel
  inspection), and AstraZeneca (drug-vial inspection). Published at
  landing.ai/case-studies. ~100 people total, but the per-engagement
  delivery team is 5-10.
- **Plainsight** (formerly Sixgill) — case studies with Tyson Foods
  (poultry-quality grading) and energy operators (substation
  inspection). plainsight.ai.
- **Cogniac** — case studies with U.S. Steel and others.
- **MobiDev** — a published wineyard yield estimation case study
  (mobidev.biz) is one of the clearest "small-team services-shop"
  walkthroughs publicly available.
- **Datature**, **Encord**, **Roboflow**'s customer showcase list
  many similar industrial deployments.

A 5-10 dev shop ships this exact pattern for smaller customers
(50-500 employee manufacturers) that the above companies are too
expensive to take on.

**The client and the problem.** A mid-size manufacturer — say, a
200-employee precision-fastener factory, a 50-employee chocolate
plant, a small PCB assembler — currently has 4-6 humans rejecting
bad parts visually at the end of a line. They want to: catch 5-10×
more defects than humans miss, free up the humans for higher-value
work, and have an auditable record of every part inspected (for ISO
9001 compliance).

**What you actually deliver to the customer (the artifact).**

- **4-8 industrial cameras** mounted around the inspection station,
  on a custom aluminum rig you design. Typical hardware: **Basler
  ace-2** or **Allied Vision Mako** cameras using **GigE Vision**
  (an industrial standard for streaming camera data over Ethernet
  instead of USB; works at longer cable runs and has hardware
  trigger sync).
- **An edge inference computer** sitting next to the line. Either an
  **NVIDIA Jetson AGX Orin** (an embedded computer-on-module with
  GPU for AI inference at the edge, ~$2-3k each) or a fanless
  industrial PC with an RTX-class GPU.
- **A trained model**. Two common choices: **anomalib's PatchCore**
  (open-source anomaly-detection library by Intel; the killer
  feature is that it needs only 100-200 "good" sample images and no
  defect labels), or a fine-tuned **Ultralytics YOLO v11** detector
  if the defect classes can be enumerated and labeled.
- **A FastAPI inference service** on the edge box, with the model
  exported through **ONNX** (a portable cross-framework model
  format) and compiled to **TensorRT** (NVIDIA's GPU-specific model
  compiler, produces a `.engine` file that runs ~5-10× faster than
  raw PyTorch on the same hardware).
- **PLC integration**. A **PLC** (Programmable Logic Controller) is
  the rugged industrial computer that drives factory equipment.
  Your service talks to it via **OPC-UA** (the modern industrial
  pub/sub-and-RPC protocol; the `python-opcua` library is the
  canonical client) and fires a reject solenoid within 50 ms of a
  flagged frame.
- **A React + FastAPI dashboard** for the QC supervisor: live
  camera feed, history of flagged parts, ability to mark misses for
  retraining, weekly PDF reports for compliance audits.
- **Monitoring**: **Prometheus + Grafana** (open-source metrics
  collection and dashboarding) for uptime, false-positive rate, and
  model-drift alerts.

**Team for a 12-16 week engagement (5 people).**

- 1 CV/ML engineer — model training, anomalib/YOLO tuning,
  evaluation against held-out defect sets.
- 1 edge deployment engineer — ONNX export, TensorRT compilation,
  Jetson setup, latency profiling.
- 1 industrial integration engineer — cameras, lighting, PLC,
  factory networking. Often a contractor with an electrical
  background.
- 1 full-stack web developer — React dashboard, FastAPI backend,
  user auth, PDF generation.
- 1 project manager / customer-success person — site visits, QC
  team training, post-launch support.

**Pricing and timeline.** $80-180k for the initial 12-16 week build,
plus $2-5k/month support retainer, plus per-additional-camera-station
expansion fees. Some shops bundle it as a $5-15k/month subscription
instead of a one-time build.

**The hardest part.** Specular surfaces (shiny metal, chrome,
polished aluminum, plastic foil). Reflections from overhead factory
lights mimic defects; subtle real defects hide in glare. Most
agencies retain a lighting-design specialist (often a $20-50k
contracted optical engineer) who designs the LED arrays, polarizers,
and diffusers. Budget 2-3 weeks of lighting iteration on any
chrome-or-aluminum project before model training even starts.

---

### Use case 2 — Phone-scan-to-digital-twin for AEC, real estate, or insurance

**Public references.** Shops and platforms that publicly document
this category of work:

- **Matterport** runs a large partner network of small CV agencies
  that build custom workflows on top of Matterport scans. Verticals:
  insurance claims, real estate listings, commercial property.
- **NavVis** (German) has a similar partner ecosystem for AEC
  (Architecture, Engineering, Construction) digital twins.
- **Polycam** Pro is used by many small AEC / interior-design agencies
  as their capture layer; the agency adds workflow software on top.
- **Buildots** (Israeli) does this for construction progress
  monitoring — they're 100+ people now, but their published workflow
  is the canonical small-shop pattern.
- **HoloBuilder**, **OpenSpace**, **Reconstruct** — published case
  studies in construction-progress documentation.
- **Visual Layer**, **Imerso**, **Pointivo** — smaller specialists
  with public customer cases.

**The client and the problem.** Pick one:

- *An insurance adjuster firm* needs to document 100-200 damaged
  houses per week after a hurricane. Current cost: $300/house
  through Matterport's pro photographer network, 2 hours per house.
- *A regional real-estate brokerage* wants searchable 3D listings
  with automatic floor-plan extraction. Current option: pay
  Matterport per scan, no measurement extraction.
- *A construction general contractor* wants weekly progress
  documentation: "show me every wall built last week, and how it
  compares to the BIM model." Current method: a project manager
  walks the site with a clipboard and an iPhone.

In all three cases, the customer wants the cost per scan down to
$30-80 and the turnaround down to minutes, with structured data
(measurements, segmented rooms, BIM comparison) the existing tools
don't provide.

**What you actually deliver.**

- **A custom iPhone app** built in Swift using **ARKit** (Apple's
  augmented-reality framework that exposes camera frames, ARKit
  anchors, and on-device LiDAR depth) plus **AVFoundation** (the
  iOS camera/video API). The app captures synchronized RGB +
  depth + IMU + ARKit poses, batches them, and uploads to your
  cloud. (Alternative: skip building an app, use **Polycam Pro**
  or **Scaniverse**'s SDK as the capture layer and build only the
  cloud pipeline.)
- **A cloud processing pipeline** on AWS or GCP:
  - **COLMAP** or **glomap** for *Structure-from-Motion* — given
    the captured photos, recover the precise camera pose for each
    photo and a sparse 3D point cloud of the scene. (glomap is the
    newer, faster open-source rewrite of COLMAP.)
  - **Nerfstudio** with the **`splatfacto`** trainer (or **gsplat**
    directly) to fit a **3D Gaussian Splat** of the scene —
    photoreal, real-time renderable. (Gaussian Splatting is the
    current default for "photoreal 3D from photos"; replaced NeRF
    in 2023.)
  - **Open3D** (a 3D processing library by Intel) for mesh
    extraction (turning the point cloud into a watertight surface)
    and floor / wall detection.
  - **SAM 2** (Meta's universal segmentation model) to segment
    each room, wall, window, and door across the photos. The masks
    get back-projected into 3D to label the splat.
  - **Plane fitting via RANSAC** (a classical outlier-tolerant
    fitting algorithm — picks the best plane from a noisy point
    set) for floor-area and wall-length measurements.
- **A web viewer** in React. Renders the Gaussian splat via
  **`@playcanvas/supersplat`** or **`gsplat.js`** (WebGL libraries
  for splat rendering in the browser). Customer measures walls, drops
  pins, exports floor plans.
- **An export pipeline**: floor plans as PDF or DXF (the standard
  CAD format), measurements as CSV, the full splat as a `.ply` or
  `.splat` file for download.
- **CRM / BIM integrations** depending on vertical: Salesforce for
  insurance, Autodesk Construction Cloud or Procore for AEC,
  Zillow / MLS for real estate.

**Team for a 16-20 week engagement (6 people).**

- 1 iOS / Swift developer (ARKit capture app).
- 1 backend Python engineer (cloud pipeline, COLMAP / Nerfstudio
  orchestration, S3 storage, job queue with Celery or RQ).
- 1 CV/ML engineer (SAM 2 prompting, measurement-extraction
  algorithms, evaluation).
- 1 frontend developer (React + Three.js + supersplat viewer).
- 1 full-stack developer (auth, billing, exports, CRM integrations).
- 1 project manager.

**Pricing and timeline.** $120-250k for the initial 16-20 week build.
Recurring: $20-100/scan SaaS pricing, or $1-5k/month per "seat" for
unlimited scans, or per-vertical enterprise contracts at
$50-200k/year. The economics improve dramatically once you have a
reference customer in a vertical — the second insurance company is
80% the same product.

**The hardest part.** Capture quality. Untrained users hold the phone
wrong (too fast, too few overlapping frames, jumps cuts). The first
6 weeks of any engagement is usually spent on a guided capture UX:
real-time feedback in the app ("slow down", "you missed this
corner"), validation thresholds before upload, and a fallback path
("our pipeline rejected this scan, here's why; please re-capture
these specific rooms").

---

### Use case 3 — Drone-based aerial inspection for agriculture, solar, or utilities

**Public references.** This category has dozens of public reference
shops:

- **DroneDeploy** runs a partner network of small CV agencies that
  build vertical-specific apps on top of DroneDeploy's capture
  platform. Verticals: crop scouting, solar inspection, roof
  inspection, mining stockpile measurement.
- **Pix4D** (Swiss) — similar platform-plus-partners model.
  Photogrammetry SDK + cloud processing.
- **Sentera** — agriculture-focused, ~80 people, published case
  studies with farm cooperatives.
- **Skycatch** — construction earthwork measurement, public
  case studies with mining and infrastructure customers.
- **PrecisionHawk**, **DroneSense**, **Aerodyne** (Malaysia) —
  larger but documented end-to-end deployments.
- **TerraSentia / EarthSense Inc** — ag-robotics with documented
  in-row scouting work.
- **Iris Automation** — drone safety, published deployment data.

A 5-10 dev shop usually plays in one vertical (just solar, or just
almonds, or just oil-pipelines) and builds a turnkey workflow for
operators in that vertical.

**The client and the problem.** Pick one:

- *A 200-acre solar farm operator* wants thermal-anomaly inspection.
  Damaged panels run hotter than healthy ones. A drone with a
  thermal camera can spot 500+ defects per flight. Currently they
  hire a $5k/day drone pilot quarterly; they want monthly.
- *An almond orchard manager* wants per-tree health scoring across
  4000 acres. Stressed trees (water, disease, frost damage) have
  distinct multispectral signatures. Currently nobody scores at
  per-tree resolution; decisions are made per-block.
- *A transmission utility* wants powerline inspection: rust on
  insulators, vegetation encroachment in the right-of-way, broken
  wires. Currently helicopter inspections at $10-30k per mile.

**What you actually deliver.**

- **A drone fleet protocol**. Customer flies their own drones (you
  don't pilot). You give them a flight plan: a `.kmz` mission file
  for **DJI Pilot 2** (DJI's flight-planning app) or a Litchi
  mission. Typical drones: **DJI Mavic 3 Enterprise** with the
  Mavic 3T thermal payload, or **Skydio X2D**, or **Autel EVO Max
  4T**.
- **A cloud processing pipeline**:
  - **Photogrammetry**: **OpenDroneMap** (open-source) or **Pix4D
    API** (commercial) stitches the 500-2000 captured photos into
    an *orthomosaic* (one huge top-down image of the whole field,
    georeferenced) plus a *DSM* (Digital Surface Model — a depth
    map of the terrain) plus a *DTM* (Digital Terrain Model — DSM
    minus vegetation).
  - **GDAL** (Geospatial Data Abstraction Library — the standard
    open-source toolkit for geospatial raster and vector data) for
    handling orthomosaics, reprojections, and tiling.
  - **CV models**: **Ultralytics YOLO** or **RT-DETR** fine-tuned
    on aerial imagery (often starting from **Roboflow Universe**
    datasets) for trees, panels, towers, or pipeline-defect
    detection.
  - **Thermal-anomaly detection**: usually a temperature-threshold
    pipeline written in Python + GDAL, sometimes augmented with
    **anomalib** for unsupervised hot-spot detection.
  - **Multispectral indices** for ag: **NDVI** (Normalized
    Difference Vegetation Index — a 2-channel formula from red and
    near-infrared bands; the canonical "is this plant healthy"
    score) plus newer indices (NDRE, GNDVI) for stress detection.
- **A web app** with an interactive map. **React + Mapbox GL JS**
  or **Leaflet** for the map; **PostGIS** (the geospatial extension
  for PostgreSQL) as the backend store for detected anomalies,
  flight history, and customer-asset metadata. Anomalies show as
  pins, click-through to the original photo, with PDF export for
  compliance.
- **Compute**: AWS **EC2 g5.xlarge** or **g6.xlarge** for GPU
  photogrammetry stitching (~$1-1.50/hr), batched per flight.

**Team for a 10-14 week engagement (4-5 people).**

- 1 CV/ML engineer (YOLO fine-tuning on aerial datasets, anomaly
  detection).
- 1 geospatial / photogrammetry engineer (OpenDroneMap or Pix4D
  pipeline, GDAL, ortho/DSM generation). Often the rarest hire.
- 1 backend developer (job queue, PostGIS, S3, AWS automation).
- 1 frontend developer (Mapbox / Leaflet UI, anomaly review UX,
  PDF reports).
- 1 PM / customer-success.

**Pricing and timeline.** $60-150k for the initial 10-14 week build,
plus $2-5k per flight processed, plus $1-3k/month per active customer
SaaS. Successful shops graduate to a $50-150k/year enterprise
contract per major customer once they prove the workflow on a few
sites.

**The hardest part.** Calibrating the model to a specific customer's
asset type. A YOLO trained on Roboflow's "solar panels" dataset will
detect 70% of one customer's panels and miss 30% because the brand
is different. Plan for 1-2 weeks of per-customer fine-tuning on
their first 200-500 hand-labeled photos. Tools that smooth this:
**Roboflow** for the labeling + auto-augmentation pipeline,
**Encord** or **Datature** for higher-end labeling workflows,
**fiftyone** (Voxel51's open-source dataset visualization tool) for
finding the failure cases.

---

## What ties the three projects together

All three share five layers:

1. **A capture layer** — industrial cameras, an iPhone with ARKit,
   or a drone with photogrammetry. The interface to the physical
   world.
2. **A calibration / preprocessing layer** — geometry corrections,
   coordinate alignment, format conversion.
3. **A model layer** — usually 1-3 open-source models (YOLO,
   anomalib, SAM 2, Depth-Anything, Nerfstudio) fine-tuned on
   100-2000 customer-specific samples.
4. **A delivery layer** — a web dashboard, a PDF report, an API,
   or a CAD export. The customer rarely wants the raw model output;
   they want it in the format their existing workflow consumes.
5. **A long-tail support layer** — model retraining when accuracy
   drifts, customer-specific edge cases, integrations with the
   customer's CRM / ERP / BIM tools.

The pattern: open-source CV models are now strong enough that the
*model* is rarely the moat. The moat is the *capture protocol +
delivery integration + per-customer fine-tuning loop*. That's a
classic services-shop opportunity.

---

## How a perception frame flows through the system

Each box is a "node" in the ROS2 sense (a process subscribing to
topics and publishing to others). Times are typical budgets for a
30 Hz indoor manipulator, not Waymo-class hardware.

```
   [Sensor: RGB-D camera @ 30 Hz]
              |
              | (raw bayer + depth frame, ~2-5 ms over USB3 / GMSL)
              v
   [Driver node: ros2_realsense or similar]
              |
              | publishes /camera/image_raw, /camera/depth/image_raw
              | (~1-3 ms: format conversion, timestamping)
              v
   [Preprocess node: rectify + crop + resize]
              |
              | (~2-4 ms: undistort using calibrated intrinsics,
              |  resize to model input shape)
              v
   [Neural net inference node: YOLO / SAM2 / pose estimator]
              |
              | (~8-25 ms on a Jetson Orin with TensorRT INT8;
              |  usually the biggest single chunk)
              v
   [Postprocess node: NMS + 2D -> 3D lift using depth]
              |
              | (~2-5 ms: non-max suppression, deproject pixels
              |  into camera-frame XYZ using depth + intrinsics)
              v
   [Tracker / fusion node: associate detections across frames]
              |
              | (~1-3 ms: Hungarian assignment, Kalman update)
              v
   [tf2 transform: camera frame -> world / base_link frame]
              |
              | (<1 ms: matrix multiply by current camera pose)
              v
   [Published topic: /perception/world_objects @ 30 Hz]
              |
              v
   [Downstream: motion planner, grasp picker, safety monitor]
```

Total wall-clock budget at 30 Hz: ~33 ms per frame. The inference
node usually eats half of that. Anything above 33 ms means you're
dropping frames and downstream consumers are reading stale state.

---

## Tools, libraries, and terms used in this file

Quick definitions for everything named above. Use it as a lookup,
not a read-through.

### Models and model families

- **YOLO (Ultralytics, v8 / v11)** — the most-used open-source
  object detector. CNN-based. Fast (real-time on a Jetson). Easy to
  fine-tune on 50-500 labeled images. `pip install ultralytics`.
- **DETR / RT-DETR** — transformer-based object detectors.
  Higher-accuracy alternative to YOLO, comparable speed in RT-DETR.
- **Mask R-CNN** — older but still-shipped detector that also
  produces segmentation masks per detection.
- **Mask2Former** — modern transformer-based segmentation. Higher
  accuracy than Mask R-CNN; slower.
- **SAM / SAM 2** (Meta, 2023 / 2024) — *Segment Anything*. A
  universal segmentation model: click a point or draw a box on an
  image, get back a clean mask of the object. Trained on 1B+ masks.
  Hugging Face model id `facebook/sam2-hiera-large`.
- **DINOv2** (Meta, 2023) — a self-supervised vision model that
  produces general-purpose image features. The "CLIP for pure
  pixels." Useful for clustering, retrieval, and as a backbone for
  other tasks.
- **Depth-Anything v2** (2024) — predicts depth (meters per pixel)
  from a single RGB image. Hugging Face model id
  `depth-anything/Depth-Anything-V2-Small-hf` (and larger variants).
- **FoundationPose** (NVIDIA, 2024) — current default for 6-DoF
  pose estimation from RGB-D + a CAD model. Works on novel objects.
- **MegaPose, GigaPose, FFB6D** — older or alternative 6-DoF pose
  estimators.
- **anomalib** (Intel / OpenVINO) — open-source library bundling
  modern anomaly-detection methods (PatchCore, EfficientAD, PaDiM).
  Trains on "good" samples only, no defect labels needed.
- **PatchCore, EfficientAD, PaDiM** — specific anomaly-detection
  methods inside anomalib.
- **PointPillars, CenterPoint, VoxelNet** — 3D object detectors
  that work on LiDAR point clouds. Used by every AV team.
- **MultiPath++, Wayformer, MVF** — Waymo's published trajectory-
  prediction and multi-view-fusion models.
- **ORB-SLAM3** — the canonical open-source classical SLAM system.
  C++. Camera + IMU + stereo support.
- **VINS-Fusion** — visual-inertial SLAM (camera + IMU). The default
  for fast-moving platforms like drones.
- **DROID-SLAM** — modern learned (neural-network-based) SLAM. More
  accurate than ORB-SLAM3 on benchmarks; more compute-hungry.
- **Spectacular AI** — commercial visual-inertial SLAM with an easy
  SDK; popular when you want SLAM without building from source.

### Libraries (CV and 3D)

- **OpenCV** — the foundational computer-vision library. 25 years
  old, ubiquitous. Python and C++. Handles image I/O, classical
  feature detection, calibration, drawing.
- **Open3D** (Intel) — point clouds, meshes, RGB-D, ICP
  registration. The 3D companion to OpenCV.
- **PyTorch3D** (Meta) — differentiable 3D operations inside
  neural networks. For research-grade 3D ML work.
- **Kornia** — differentiable OpenCV-style operations in PyTorch.
- **Nerfstudio** — turnkey training framework for NeRF and Gaussian
  Splatting. CLI commands like `ns-process-data` and `ns-train`.
- **gsplat** — the fast CUDA backbone for Gaussian Splatting.
- **`splatfacto`** — the Gaussian-Splatting trainer inside
  Nerfstudio. The most common entry point.
- **COLMAP** — the classical structure-from-motion pipeline. Given
  photos, recovers each camera's pose and a sparse 3D point cloud.
  The first step in most NeRF / Gaussian Splat pipelines.
- **glomap** — modern faster open-source rewrite of COLMAP (2024+).
- **VGGT** (2025) — feed-forward transformer that reconstructs a
  3D scene from a few images, skipping COLMAP's optimization step.
- **Polycam, Scaniverse, Niantic Scaniverse** — consumer iOS apps
  that capture and reconstruct 3D scenes; some expose an SDK that
  agencies build on.
- **`@playcanvas/supersplat`, `gsplat.js`** — WebGL libraries for
  rendering Gaussian splats in the browser.
- **fiftyone** (Voxel51) — open-source tool for exploring,
  comparing, and debugging vision datasets.
- **Roboflow** — labeling-plus-training-plus-deployment platform.
  Roboflow Universe is a large public dataset repository.
- **Encord, Datature** — higher-end commercial labeling platforms.

### Deployment and inference

- **PyTorch** — the deep-learning framework. The de-facto standard;
  TensorFlow has been losing ground for years.
- **TensorFlow** — Google's deep-learning framework. Still in use at
  Waymo / Google and parts of TF-Hub, less common in new projects.
- **ONNX** (Open Neural Network Exchange) — a portable cross-
  framework model format. PyTorch → ONNX → TensorRT / OpenVINO /
  Core ML is a common deployment path.
- **TensorRT** (NVIDIA) — compiler that turns ONNX models into
  faster, smaller `.engine` files optimized for a specific NVIDIA
  GPU. 5-10× speedup over raw PyTorch typical.
- **Triton Inference Server** (NVIDIA) — model-serving HTTP/gRPC
  server. Like nginx for ML models.
- **OpenVINO** (Intel) — TensorRT's equivalent for Intel CPUs and
  iGPUs.
- **INT8 quantization** — converting model weights from 32-bit
  floats to 8-bit integers. ~4× memory reduction, 2-4× speedup,
  usually 0-2% accuracy loss. Standard for edge deployment.

### Hardware

- **Intel RealSense D435 / D455** — the workhorse RGB-D camera.
  Active-stereo depth, 1280×720 at 30 FPS, $300-400.
- **Orbbec Femto Bolt** — newer time-of-flight depth camera, $300.
  Successor to the Microsoft Azure Kinect.
- **Basler ace-2, Allied Vision Mako** — industrial machine-vision
  cameras. GigE Vision protocol, hardware triggering, much more
  rugged than consumer cameras.
- **GigE Vision** — industrial standard for streaming high-
  resolution camera data over Gigabit Ethernet (vs. USB). Allows
  long cable runs and hardware-synced multi-camera rigs.
- **DJI Mavic 3 Enterprise / Mavic 3T** — current standard
  professional drone. Mavic 3T adds a thermal imager.
- **Skydio X2D** — Skydio's professional drone, strong autonomy.
- **NVIDIA Jetson AGX Orin / Orin Nano** — embedded computer
  modules with GPU, the standard edge target for robotics. ~$2-3k
  (AGX) / ~$500 (Nano).

### Industrial protocols and tooling

- **PLC** (Programmable Logic Controller) — the rugged industrial
  computer that drives factory equipment.
- **OPC-UA** — modern industrial pub/sub-and-RPC protocol for
  talking to PLCs. Python: `python-opcua`.
- **Modbus TCP** — older industrial protocol; still ubiquitous.
- **GDAL** (Geospatial Data Abstraction Library) — the standard
  open-source toolkit for geospatial raster and vector data.
- **PostGIS** — geospatial extension for PostgreSQL.
- **NDVI** (Normalized Difference Vegetation Index) — a 2-channel
  formula `(NIR - Red) / (NIR + Red)` from multispectral imagery;
  the canonical "is this plant healthy" score. NDRE and GNDVI are
  newer variants.
- **DSM / DTM** — Digital Surface Model / Digital Terrain Model.
  Per-pixel elevation; DSM includes vegetation, DTM excludes it.
- **Orthomosaic** — a single huge top-down image stitched from
  hundreds of drone photos, with all distortion corrected so
  measurements are accurate.
- **Pix4D** — commercial photogrammetry SaaS. The expensive option.
- **OpenDroneMap (ODM)** — open-source photogrammetry. Slower but
  free.

### Capture frameworks and SDKs

- **ARKit** (Apple) — iOS augmented-reality framework. Exposes
  camera frames, IMU, LiDAR depth (on Pro iPhones), plane
  detection, and ARKit anchors (persistent 3D coordinate
  references).
- **AVFoundation** (Apple) — the underlying iOS camera/video API
  used by ARKit and any custom capture app.
- **RealityKit, Metal, SwiftUI** — Apple's higher-level 3D rendering
  framework, low-level GPU API, and UI framework respectively.
- **visionOS** — the OS on Apple Vision Pro. Derived from iOS /
  macOS XNU.

### Robotics middleware

- **ROS2** (Robot Operating System 2) — the de-facto open-source
  middleware for robotics. Provides typed pub/sub topics, services,
  parameters, the `tf2` transform tree, lifecycle management.
- **ROS2 distros** — major versioned releases. Current LTS:
  **Humble** (Ubuntu 22.04, until 2027), **Jazzy** (Ubuntu 24.04,
  until 2029). **Iron** was a non-LTS interim.
- **rclpy, rclcpp** — Python and C++ client libraries for ROS2.
- **rosbag** — recorded log file of all topic data from a ROS
  session. The CI fixture format for perception teams.
- **`tf2`** — the ROS2 library that tracks coordinate-frame
  transforms across the robot.
- **QoS / SensorDataQoS** — ROS2's Quality-of-Service profiles for
  topics. `SensorDataQoS` is the "best-effort, latest-N" profile
  appropriate for high-rate sensor streams; using the wrong profile
  causes silent frame drops.

### Calibration and math

- **Kalibr** — the standard open-source toolkit for multi-camera
  and camera-IMU calibration. Requires waving a checkerboard.
- **`cv2.calibrateCamera`** — OpenCV's single-camera intrinsics
  routine; the first calibration you'll ever run.
- **PnP** (Perspective-n-Point) — the math problem: given known 3D
  points and their pixel observations, solve for camera pose.
- **RANSAC** — RANdom SAmple Consensus. A robust fitting algorithm
  that tolerates many outliers; used everywhere in classical CV
  (line fitting, fundamental matrix estimation, plane fitting).
- **Bundle adjustment** — the big joint optimization inside every
  SLAM system: refine all camera poses and 3D points so projection
  error is minimized. Libraries: Ceres, g2o, GTSAM.
- **EKF / UKF** — Extended / Unscented Kalman Filter. Classical
  state estimators that fuse noisy sensor streams.
- **Kalman update** — one step of an EKF/UKF: take a new
  measurement, update the state estimate and its uncertainty.
- **Hungarian algorithm** — the standard solver for the
  "assignment problem" (which detection in frame T matches which
  in frame T+1?). Used in multi-object tracking.

### AV-specific extras

- **HD map** — high-definition lane-level map used by AVs to
  localize and plan.
- **Occupancy network** — a model that consumes camera (+/- LiDAR)
  and emits a 3D voxel grid of free vs. occupied space. Tesla's
  big bet.
- **Bazel** — Google's build system; Waymo and other Google-derived
  AV teams use it.

---

## What's next to read

- `01-examples.md` — the broader landscape of who's building what.
- `02-learn.md` — the layered curriculum to build the skills above.
- `03-start.md` — a concrete 8-week ramp-up.
- `06-courses.md` — courses (basics + project-driven) to take.
