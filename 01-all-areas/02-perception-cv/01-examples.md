# Examples of Work

This is a tour of "what perception code looks like in the wild." If
you're new, skim it — the goal is to know the names so the rest of the
material has hooks to land on.

Coming from web dev, think of this page like the "awesome-list" you'd
read when picking up a new JS framework. You won't remember every
entry, but next time someone says "we ran a quick SAM 2 mask on the
frame and fed it into FoundationPose," you'll have hooks for each
noun. Cross-references: see `00-basics.md` for vocabulary, `02-learn.md`
for the learning path, `03-start.md` for setup, `04-employers.md` for
the company list, `05-projects.md` for portfolio ideas, and
`06-courses.md` for structured learning.

## Deployed products (real-world perception running today)

These are the equivalent of "production at scale" in web terms — large
teams, billions of inference calls, real customers.

- **Waymo, Zoox, Cruise** — multi-camera + LiDAR + radar perception
  stacks for full self-driving. Waymo's been driverless in Phoenix,
  SF, LA, Austin, and Atlanta as of 2025. Big perception teams,
  research-grade work, $200k+ base. The signature perception
  challenge is sensor fusion at scale: stitching together asynchronous
  streams from a dozen sensors into a single consistent world model,
  ~10 times per second, with the consequence-of-failure of an actual
  collision. Public engineering decisions include a heavy investment
  in a custom simulator (Carcraft / Simulation City) — they reportedly
  drive billions of simulated miles per week, because real-world miles
  are too expensive to be the bottleneck for the long tail. A junior
  perception engineer at Waymo will spend a startling fraction of
  their first year writing ground-truth labelers, triage tools, and
  regression tests over labeled segments from the on-road fleet —
  think "Jest snapshot tests, but each snapshot is a LiDAR sweep with
  ground-truth bounding boxes."
- **Tesla FSD** — famously camera-only ("vision-only"); ships an
  "occupancy network" that builds a voxel-grid of free vs. occupied
  space directly from 8 cameras. Different bet than the rest of the
  industry. Tesla's bet on pure vision is famously controversial —
  they argue cost + scaling (cameras are cheap, the fleet provides
  near-infinite labeled data); the industry counter-argues redundancy
  (a LiDAR sees in fog, dust, and direct sun, where cameras blow out).
  Reportedly they ripped out radar and even ultrasonics in successive
  years to commit to the vision-only thesis. The auto-labeling pipeline
  is the famous engineering moat: the fleet uploads clips, an offline
  "monster network" re-derives ground truth with hindsight (future
  frames), and that becomes training data for the smaller online model
  that ships to cars. A junior here lives in a data-pipeline mindset —
  the work is closer to building a giant ETL system than to writing
  novel models.
- **Mobileye EyeQ** — ADAS perception SoCs shipped in 150M+ vehicles
  cumulatively (as of 2024). The quiet giant of automotive vision.
  Their challenge is shipping useful perception under hard real-time
  constraints on a fixed-function chip — closer to embedded systems
  than to a Python notebook. Public stance: they take the opposite
  bet of Tesla and invest in REM (Road Experience Management), a
  crowdsourced HD-map layer built from production cars. A junior at
  Mobileye is likely to do a lot of model-quantization work, INT8
  calibration, and kernel-level perf tuning to fit a network in tens
  of milliseconds on a chip you cannot upgrade after fab.
- **Skydio drones** — fully autonomous obstacle-avoidance flight from
  6 cameras + on-board NN inference on a Jetson. Their tech demos are
  the canonical "wow, that's perception working" moment. The hard
  problem is closing the perception-action loop fast enough that a
  drone can dodge a tree branch at speed — latency is everything.
  Reportedly they fuse classical visual-inertial odometry (VIO) with
  learned obstacle nets because pure classical fails on textureless
  surfaces and pure learning is too unpredictable. A junior at Skydio
  spends most of their time on log-replay regression tests: every
  near-miss in the field becomes a saved bag file that the perception
  stack must continue to pass after every PR.
- **Boston Dynamics Spot / Atlas** — depth-camera-driven obstacle maps
  and semantic terrain classification. Spot is the most-deployed
  legged robot in industry today. The perception challenge is unique
  to legs: not just "is the floor flat?" but "is this surface
  load-bearing, and will my foot stick?" — terrain classification with
  consequences. They've published on stair detection and "uneven
  terrain locomotion" using a mix of structured-light depth (the head
  cameras) and proprioception. Juniors often work in the simulator
  pipeline (Webots / their internal sim) before changes go anywhere
  near a real $75k robot.
- **Apple Vision Pro, iPhone LiDAR + ARKit** — real-time scene mesh,
  plane detection, hand tracking, eye tracking. The most polished
  consumer perception stack on the planet. The challenge is power
  budget: it has to run forever on a battery and never thermally
  throttle while a user watches a movie. Apple's public stance is
  hardware-software co-design — the Neural Engine, the R1 chip, and
  ARKit are explicitly designed together. Juniors on the perception
  side typically work in Metal Performance Shaders and Core ML, which
  is a different world from the standard PyTorch + CUDA pipeline.
- **Pickle Robot, Symbotic, Covariant** (Covariant acquired by Amazon
  Aug 2024) — warehouse perception: bin segmentation, 6-DoF pose for
  irregular SKUs. The perception challenge here is "the long tail of
  stuff": a warehouse SKU catalog has hundreds of thousands of items,
  many shiny, transparent, deformable, or in crumpled packaging — all
  failure modes for standard models. Covariant's bet was the
  "Covariant Brain" — a single foundation model trained across all
  customer deployments, so a new SKU at one warehouse improves
  performance everywhere. A junior here spends a lot of time on
  failure-case triage: a grasp failed, why? Was it perception, motion
  planning, or the gripper? You learn to read a lot of overlaid debug
  images.
- **Verkada, Ambient.ai, Veo** — security-camera anomaly detection +
  person/event recognition. The "computer vision as a SaaS" wedge.
  The perception challenge is multi-tenant scale: thousands of
  cameras per customer, hundreds of customers, but the actual model
  inference must be cheap enough that the unit economics work. The
  trick is usually a cascade — a cheap motion detector triggers a
  mid-tier classifier which triggers an expensive event recognizer
  only on a fraction of frames. Juniors at Verkada-style companies
  often start on the ingestion side: RTSP streams, GStreamer pipelines,
  H.264 decoding on the GPU before a single pixel hits a model.

## Landmark research papers (read these eventually, in this order)

The papers that built the modern stack. Treat each as a 1-3 day
investment.

- **NeRF** (Mildenhall et al., ECCV 2020) — neural radiance fields.
  Started the neural-3D wave. The "AlexNet moment" for 3D vision. In
  your own words: train a tiny MLP to memorize "what color and density
  is at this 3D point, viewed from this angle?" — then render new views
  by raymarching. What changed: 3D reconstruction stopped being a
  geometry problem and became a learning problem; an entire subfield
  (neural fields) sprang up overnight. Repo: `bmild/nerf` on GitHub,
  and the cleaner `nerfstudio-project/nerfstudio` for the practical
  follow-up.
- **3D Gaussian Splatting** (Kerbl et al., SIGGRAPH 2023, Inria) —
  real-time photoreal 3D rendering from photos. Killed NeRF as the
  default and is now the mainstream choice for robotics digital
  twins. ~100x faster to render. In your own words: instead of a
  neural network, represent the scene as millions of fuzzy 3D ovals
  ("Gaussians") with color and opacity, and rasterize them directly.
  What changed: the rendering loop went from seconds-per-frame to
  60+ FPS, which unlocked actual interactive use in robotics sims
  and AR/VR. Repos: `graphdeco-inria/gaussian-splatting` (the
  original), `nerfstudio-project/gsplat` (the fast CUDA backbone).
- **Segment Anything (SAM 1)** (Meta, April 2023) and **SAM 2** (Meta,
  July 2024) — promptable, universal segmentation. Trained on 1B+
  masks; works zero-shot on essentially any object. SAM 2 added video
  tracking. In your own words: click a pixel, get a clean mask of
  whatever object that pixel is on, without training on your data.
  What changed: image segmentation effectively became a solved API
  call — annotation pipelines that took human-weeks now take an
  afternoon. HuggingFace pattern: `facebook/sam2-hiera-large` and
  similar; repo: `facebookresearch/segment-anything-2`.
- **DINOv2** (Meta, April 2023) — self-supervised vision features
  that work zero-shot for classification, retrieval, depth. The
  closest thing CV has to a "CLIP for pure pixels." In your own
  words: a vision transformer trained on unlabeled images so well
  that its features alone (no fine-tuning) match supervised models
  on most downstream tasks. What changed: people stopped training
  task-specific backbones from scratch and started using DINO
  features as a frozen feature extractor — much like everyone in
  NLP stopped training their own BERT and started using pretrained
  embeddings. HuggingFace pattern: `facebook/dinov2-base` and the
  larger variants; repo: `facebookresearch/dinov2`.
- **Depth-Anything v1 / v2** (Yang et al., CVPR 2024 / arXiv 2024) —
  monocular metric depth at production quality. Single image -> dense
  depth map. In your own words: an enormous student-teacher pipeline
  on unlabeled images that finally made "one camera, real depth" work
  on out-of-distribution scenes. What changed: a lot of cheap RGB-D
  applications (background blur, AR object placement, rough obstacle
  avoidance) became viable without a depth sensor. HuggingFace
  pattern: `depth-anything/Depth-Anything-V2-Large`; repo:
  `DepthAnything/Depth-Anything-V2`.
- **FoundationPose** (NVIDIA, CVPR 2024 best paper) — 6-DoF object
  pose from a single CAD model, no per-object training required.
  Production-ready for bin picking. In your own words: hand it a
  CAD mesh and an RGB-D crop, get back the 4x4 transform that places
  the mesh on the object. What changed: the warehouse-robotics
  community's pose-estimation problem went from "train a custom
  network per SKU" to "render the CAD, run the model." Repo:
  `NVlabs/FoundationPose`.
- **MegaPose** (Labbe et al., 2022) — earlier instance of the
  "render-and-compare" 6-DoF pose family. In your own words: render
  hypotheses of the object in many poses, compare to the real image,
  pick the best. What changed: established the template for the
  CAD-driven pose-estimation work that FoundationPose later refined.
  Repo: `megapose6d/megapose6d`.
- **DROID-SLAM** (Teed & Deng, NeurIPS 2021) — learned SLAM end to
  end. First to convincingly beat ORB-SLAM3 on benchmarks. In your
  own words: a recurrent network that does the bundle-adjustment
  step itself, instead of leaving it to a hand-written optimizer.
  What changed: the SLAM community had to take learning-based methods
  seriously, not just as a feature-extraction front-end. Repo:
  `princeton-vl/DROID-SLAM`.
- **VGGT** (Wang et al., 2025) — feed-forward 3D scene reconstruction
  from a few images. No optimization, just a transformer. Latest
  state of the art. In your own words: stuff a handful of images
  into a transformer and it spits out camera poses, depth, and a
  point cloud in one forward pass — no per-scene optimization at
  all. What changed: it raises the question of whether classical
  structure-from-motion (COLMAP and friends) has a future for small
  scenes. Repo pattern: `facebookresearch/vggt`.
- **CoTracker, TAPIR** (Meta, DeepMind, 2023-2024) — dense long-term
  point tracking through video. The "dense optical flow" of the 2020s.
  In your own words: pick any point in the first frame, get its
  trajectory through hundreds of subsequent frames, even through
  occlusion. What changed: a lot of video-analysis problems that
  used to need keyframe tricks and Kalman filters are now a single
  model call. Repos: `facebookresearch/co-tracker`,
  `google-deepmind/tapnet`.

## Open-source stack (the equivalent of "npm packages you'll actually use")

- **OpenCV** — the jQuery of computer vision. 25 years old, ships
  everywhere, you'll grumble about it but you'll ship with it daily.
  Python and C++. Quirky API, inconsistent BGR-vs-RGB conventions,
  unbeatable for the basic operations.
- **Open3D** — point clouds, meshes, RGB-D processing. The Intel-led
  3D companion to OpenCV. Think of it as "OpenCV for 3D arrays."
- **PyTorch3D** — Facebook's differentiable 3D library. The way to do
  3D inside a neural network. Analogy: like having a 3D renderer
  whose output you can take a gradient through, the way you can
  backprop through a tensor op.
- **Nerfstudio** — turnkey NeRF / Gaussian Splatting training. Drop
  in photos, get a scene. Analogy: `create-react-app` for neural 3D
  — opinionated defaults, sensible CLI, you can override later.
- **gsplat** — the fast CUDA backbone for Gaussian Splatting. The
  "PyTorch kernel" of the splatting world.
- **COLMAP** — the classical "structure from motion" pipeline. Given
  photos, recovers camera poses + a sparse 3D point cloud. The first
  step in most NeRF / GS pipelines. **glomap** is the modern faster
  alternative (2024+). Analogy: COLMAP is a build system for 3D —
  it reconstructs everything from scratch from the source (photos);
  glomap is the "esbuild" to COLMAP's "webpack" — same outputs,
  much faster pipeline.
- **ORB-SLAM3, OpenVSLAM, VINS-Fusion** — the dominant open-source
  classical SLAM systems. C++; you'll see all three in robotics
  internships.
- **MMDetection, MMSegmentation, Detectron2** — model zoos for
  detection and segmentation training. Detectron2 (Meta) tends to
  be cleaner code; the MM* family (OpenMMLab) tends to have more
  recent models. Analogy: the difference between using `lodash` and
  using a kitchen-sink utility belt — both work, pick the one with
  the recipe you need.
- **Ultralytics YOLO (v8 / v11)** — the fast-iteration, fine-tune-on-
  your-own-data detector. Not the most cited, but the most used in
  industry. Analogy: the Tailwind of object detection — purists
  scoff at it, every hackathon ships with it.
- **FoundationPose, MegaPose, GigaPose** — pretrained 6-DoF pose
  inference, drop-in ready.
- **hloc** (HierarchicalLocalization) — modern visual localization
  pipeline (SuperPoint + SuperGlue / LightGlue).
- **Hugging Face Transformers + `transformers.AutoImageProcessor`** —
  vision foundation models (SAM, DINOv2, Depth-Anything) are all
  one-line loads now. Use them. Analogy: Hugging Face for vision
  foundation models is npm for JS packages — `pip install
  transformers`, one line to load any pretrained model by name,
  versioned, with a README.
- **Kornia** — differentiable CV in PyTorch. Classical operations
  (warps, filters, color conversions, geometry) implemented as
  tensor ops you can backprop through. Analogy: "OpenCV that
  speaks tensor" — drop it into your training loop and use a
  homography as a layer.
- **timm** (pytorch-image-models, by Ross Wightman, now under
  Hugging Face) — an enormous zoo of image classification backbones
  with consistent APIs. Analogy: the DefinitelyTyped of vision
  models — if a backbone exists, timm has the weights and a
  one-line constructor.
- **Albumentations** — fast image augmentation library. Pipelines
  of crops, flips, color jitter, weather effects, etc. Analogy: a
  Webpack loader chain for images — declare the transforms once,
  apply them consistently across train / val.
- **MONAI** — medical-imaging deep learning framework (3D volumes,
  DICOM I/O, organ-segmentation models). Cross-pollinates into
  industrial CT inspection and any 3D-image-stack task. Analogy: a
  vertical-specific framework like Next.js is for React — opinionated
  about its niche but the patterns are reusable.
- **supervision** (Roboflow) — utility belt for chaining detectors,
  trackers, annotators, and writing video outputs. The "glue" library
  for demo notebooks. Analogy: lodash for vision pipelines.
- **Lightning AI / PyTorch Lightning** — training-loop boilerplate
  abstraction. Hides the for-loop, the optimizer step, the
  distributed-training plumbing. Analogy: an Express.js for ML
  training — you still write the model, but the framework owns the
  request/response lifecycle.
- **DeepStream** (NVIDIA) — production video-analytics pipeline
  framework built on GStreamer, with TensorRT-accelerated inference
  nodes. The thing you reach for when you need to run 32 RTSP
  cameras through a detector on a single Jetson. Analogy: a managed
  Kubernetes for video frames.
- **GStreamer** — the underlying media-pipeline layer that DeepStream
  (and many camera drivers) sit on top of. Source/filter/sink graphs,
  hardware-accelerated codecs. Analogy: the Node.js `stream` module,
  but for video, with decades of plugins.
- **Hydra** (Facebook Research) — config management for ML
  experiments. Compose YAML configs, sweep hyperparameters, override
  from the CLI. Analogy: dotenv + a templating engine, designed for
  experiments. Pairs naturally with Lightning.
- **PyTorch checkpoint** — a `.pt` or `.ckpt` file with the model
  weights. Analogy: a compiled binary you load at boot — it's not
  source code, you don't read it, you just `torch.load()` it and
  feed it tensors.

## Datasets that show up in every paper

- **KITTI** (2012) — outdoor driving; ageing but still benchmarked.
- **nuScenes** (2019) — large multi-modal AV dataset.
- **ScanNet, ScanNet++** — indoor RGB-D, the default for indoor 3D.
- **TUM RGB-D, EuRoC** — handheld / drone SLAM benchmarks.
- **Replica, Hypersim** — photoreal synthetic indoor for sim2real.
- **BOP** (Benchmark for 6D Object Pose) — the standard for 6-DoF
  pose evaluation.
- **MS COCO, Objects365, LVIS** — detection / segmentation classics.
- **Open Images V7** — 9M images with multi-label annotations.
- **Argoverse 2** (Argo AI / now part of academic stewardship) —
  multi-city autonomous-driving dataset with rich HD-map context.
  Common benchmark for motion forecasting as well as perception.
- **Waymo Open Dataset** — Waymo's public release of LiDAR + camera
  data with 3D bounding boxes; one of the largest publicly available
  AV datasets. Comes with periodic challenge competitions.
- **Lyft Level 5 / Woven by Toyota** — the Lyft self-driving dataset
  later stewarded by Woven. Frequently cited in motion-prediction
  papers; you'll see it in trajectory-forecasting benchmarks.
- **Mapillary** — crowdsourced street-level imagery, useful for
  large-scale visual place recognition and semantic segmentation.
- **BDD100K** (Berkeley) — 100k driving videos with diverse weather
  and time-of-day; standard for "does my detector generalize off the
  sunny California test set?"
- **ADE20K** (MIT) — scene-parsing dataset with hundreds of fine
  semantic classes; the indoor / general-scene complement to COCO.
- **NYU Depth V2 (NYUv2)** — small but classic indoor RGB-D dataset;
  still the default sanity check for monocular depth estimators.

## Production perception stacks decomposed

Let's walk through a hypothetical autonomous mobile robot (AMR) — say
a warehouse cart that drives between shelves and grabs totes. This is
the kind of robot a junior is most likely to encounter at a small
robotics company, and naming the package at each stage demystifies the
stack.

1. **Camera driver** — `usb_cam`, `realsense2_camera`, or a vendor
   ROS 2 driver. Pulls raw frames off the sensor, publishes them on
   a ROS 2 topic. Analogy: a ROS 2 topic is like a Redis pub/sub
   channel — anyone subscribed gets the new message; the publisher
   doesn't care who's listening.
2. **image_transport** — ROS 2 wrapper that handles compressed
   transport (JPEG, Theora, H.264) between nodes so you don't push
   raw 1080p frames over loopback. Analogy: gzip middleware for an
   Express route.
3. **camera_info / rectification** — `image_proc` undistorts the
   raw frame using calibration intrinsics. Analogy: a "preflight
   normalize" step before anything downstream touches the image.
4. **Segmentation** — SAM 2 (via a custom ROS 2 wrapper, or a
   homegrown Python node using the HuggingFace checkpoint) produces
   per-object masks for the totes in view. In a tighter prod pipe
   you'd swap in a fine-tuned smaller model — SAM 2 is the
   prototyping step.
5. **6-DoF pose** — FoundationPose takes the masked region + the
   tote's CAD mesh + the depth image and returns the 4x4 transform.
   Output is published as a `geometry_msgs/PoseStamped` on a topic
   like `/totes/pose`.
6. **TF tree** — the pose is broadcast as a `tf2` transform so other
   nodes can ask "where is `tote_42` in the `map` frame?" without
   knowing how the perception node figured it out. Analogy: a tf
   transform tree is like a shared global state store (Redux), but
   with built-in time interpolation.
7. **Costmap / occupancy** — a Nav2 plugin consumes the LiDAR scan
   plus the detected obstacles and rasterizes a 2D costmap. Nav2
   itself is the standard ROS 2 navigation stack — analogous to
   React Router for "where do I go next?" decisions.
8. **Planner + controller** — Nav2's planner (Smac, NavFn) and
   controller (DWB, MPPI) consume the costmap and the goal pose and
   publish `/cmd_vel`. Outside the perception team's lane, but you'll
   debug interactions across this boundary all the time.
9. **Recording + replay** — every run, `ros2 bag record` captures
   the topics. When a bug fires, you replay the bag against a new
   version of the perception node and diff the outputs. Analogy: a
   bag file is a HAR file for the entire robot — every input and
   intermediate state, saved for post-mortem.

Knowing this stack end-to-end is what separates a "I can fine-tune a
detector" applicant from a "I can ship a robot" hire.

## Reading the trade press / staying current

The field moves fast. You don't have to read everything; you do have
to know where to look when something gets hyped.

- **CVPR / ICCV / ECCV open-access proceedings**
  (`openaccess.thecvf.com`) — the three big computer-vision
  conferences. Every accepted paper is free. Skim the awards list
  each year; it's a curated highlight reel.
- **arXiv cs.CV** — the firehose. Use `arxiv-sanity-lite` or
  Hugging Face's daily-papers feed (`huggingface.co/papers`) to
  filter to what others are upvoting.
- **Two Minute Papers** (YouTube, Károly Zsolnai-Fehér) — short,
  enthusiastic visual recaps of new graphics + vision papers. Great
  for keeping a passive awareness while doing chores.
- **Yannic Kilcher** (YouTube) — deeper paper walkthroughs with
  skeptical commentary; the "code review" of new ML papers.
- **The Robot Report** (`therobotreport.com`) — industry news, who
  raised, who hired, who launched what. Useful for job-market
  awareness.
- **IEEE Spectrum Robotics** — longer-form journalism on robotics
  and adjacent perception work; reliable, not hype-y.
- **Robohub** (`robohub.org`) — academic-flavored robotics
  newsletter; lots of crossposts from university labs.
- **ROS Discourse** (`discourse.ros.org`) — the actual mailing-list
  / forum where ROS 2, Nav2, and related package maintainers
  discuss. Lurk for a few weeks to absorb the vocabulary.
- **X / Twitter** — follow handles like `@AIatMeta`,
  `@NVIDIAAIDev`, `@_akhaliq` (paper aggregator), and individual
  researchers (e.g., `@karpathy` for the AV-meets-deep-learning
  takes, `@jonbarron` for neural rendering). See `04-employers.md`
  for a more complete handle list.
- **Hugging Face Spaces and Models tabs** — track which vision
  models are trending. The "GitHub trending" of foundation models.
- **Papers With Code** (`paperswithcode.com`) — leaderboards by
  benchmark. When someone says "state of the art on COCO", you can
  verify in a click.
- **GitHub trending in Python** — coarse but useful; a perception
  paper without a popular repo within a month usually fades.

## How to actually skim a CV paper in 20 minutes

Treat this as the rubber-ducking of perception research. You're not
trying to understand every equation on first pass — you're trying to
decide "is this worth a deeper read, and can I use it?" The six-step
recipe:

1. **Read the abstract.** What problem, what method, what numbers.
   If you can't summarize it in one sentence after reading, that's
   fine — keep going, the figures often clarify what the prose
   buries.
2. **Look at Figure 1.** Almost every CV paper puts its money figure
   first — an architecture diagram or a hero result. If Figure 1
   makes the contribution obvious, you've already absorbed 50% of
   what matters.
3. **Look at Figures 5 / 6 (or the qualitative results).** Toward
   the back of the paper, there's usually a grid of
   inputs-and-outputs. If the qualitative results look great, the
   numbers usually follow. If the qualitative results look weird or
   cherry-picked, be suspicious.
4. **Read the last paragraph of the intro.** This is where authors
   are forced to enumerate their contributions as bullets. It is
   the TL;DR you should have gotten from the abstract but didn't.
5. **Check the GitHub repo.** Is there one? Is it
   `pip install`-able? When was the last commit? Are there open
   issues that say "this doesn't reproduce"? A great repo turns a
   3-day project into a 3-hour project; a bad / absent repo turns a
   3-hour project into a 3-week project.
6. **Search Hugging Face for the model.** If the authors uploaded a
   checkpoint, you can run inference in five minutes from a Colab
   notebook. If they didn't, factor that into your reading priority
   — "interesting but I won't use it this quarter" is a valid file
   to put it in.

Optional step 0: search for the paper on Two Minute Papers / Yannic
Kilcher / a Twitter thread before reading. Sometimes 90 seconds of
someone else's summary is the right primer.

After enough reps, this loop takes 10 minutes for a familiar topic
and 30 for an unfamiliar one. That's the actual professional reading
speed — nobody reads every CVPR paper end-to-end, and you shouldn't
feel bad about not doing so either.
