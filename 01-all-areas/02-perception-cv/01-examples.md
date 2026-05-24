# Examples of Work

A tour of perception code in the wild. Skim it — the goal is to know
the names so the rest of the material has hooks to land on.

Cross-references: `00-basics.md` for vocabulary, `02-learn.md` for the
learning path, `03-start.md` for setup, `04-market.md` for the
company list, `05-projects.md` for portfolio ideas, `06-courses.md`
for structured learning.

## Deployed products (real-world perception running today)

Large teams, billions of inference calls, real customers.

- **Waymo, Zoox, Cruise** — multi-camera + LiDAR + radar stacks for
  full self-driving. Waymo is driverless in Phoenix, SF, LA, Austin,
  and Atlanta as of 2025. The signature challenge is sensor fusion at
  scale: asynchronous streams from a dozen sensors into one consistent
  world model, ~10 Hz, with collision as the failure mode. Waymo
  reportedly drives billions of simulated miles per week in Carcraft /
  Simulation City because real miles cannot cover the long tail.
- **Tesla FSD** — camera-only ("vision-only"), shipping an "occupancy
  network" that builds a voxel grid of free vs. occupied space from
  8 cameras. Tesla removed radar and ultrasonics in successive years
  to commit to the thesis. The engineering moat is the auto-labeling
  pipeline: the fleet uploads clips, an offline "monster network"
  re-derives ground truth with future-frame hindsight, and that
  becomes training data for the smaller on-car model.
- **Mobileye EyeQ** — ADAS perception SoCs shipped in 150M+ vehicles
  cumulatively (as of 2024). Hard real-time constraints on a
  fixed-function chip; closer to embedded systems than to a notebook.
  Mobileye also invests in REM (Road Experience Management), a
  crowdsourced HD-map layer built from production cars.
- **Skydio drones** — fully autonomous obstacle-avoidance from
  6 cameras + on-board NN inference on a Jetson. The hard problem is
  closing the perception-action loop fast enough to dodge a branch at
  speed. They fuse classical visual-inertial odometry (VIO) with
  learned obstacle nets because pure classical fails on textureless
  surfaces and pure learning is too unpredictable.
- **Boston Dynamics Spot / Atlas** — depth-camera-driven obstacle maps
  and semantic terrain classification. Spot is the most-deployed
  legged robot in industry. The perception question for legs is "is
  this surface load-bearing?" — terrain classification with
  consequences. Published work covers stair detection and uneven-
  terrain locomotion using structured-light depth plus proprioception.
- **Apple Vision Pro, iPhone LiDAR + ARKit** — real-time scene mesh,
  plane detection, hand and eye tracking. The most polished consumer
  perception stack on the planet. The constraint is power budget: it
  must run for hours on a battery without thermal throttling. Stack
  is hardware-software co-designed (Neural Engine, R1, ARKit, Metal
  Performance Shaders, Core ML).
- **Pickle Robot, Symbotic, Covariant** (Covariant acquired by Amazon
  Aug 2024) — warehouse perception: bin segmentation and 6-DoF pose
  for irregular SKUs. The challenge is the long tail: hundreds of
  thousands of shiny, transparent, deformable, or crumpled items.
  Covariant's bet was the "Covariant Brain" — one foundation model
  across all customer deployments.
- **Verkada, Ambient.ai, Veo** — security-camera anomaly detection
  and event recognition. Multi-tenant scale forces a cascade: cheap
  motion detector triggers a mid-tier classifier triggers an
  expensive event recognizer on a fraction of frames. Ingestion side
  is RTSP streams, GStreamer, GPU-side H.264 decoding before a single
  pixel hits a model.

## Landmark research papers (read these eventually, in this order)

The papers that built the modern stack. Treat each as a 1-3 day
investment.

- **NeRF** (Mildenhall et al., ECCV 2020) — neural radiance fields.
  Train a tiny MLP to memorize color and density at each 3D point,
  then render new views by raymarching. Started the neural-3D wave.
  Repo: `bmild/nerf`; practical follow-up: `nerfstudio-project/nerfstudio`.
- **3D Gaussian Splatting** (Kerbl et al., SIGGRAPH 2023, Inria) —
  represent a scene as millions of fuzzy 3D ovals with color and
  opacity and rasterize them directly. ~100x faster than NeRF, 60+
  FPS, now the default for robotics digital twins. Repos:
  `graphdeco-inria/gaussian-splatting`, `nerfstudio-project/gsplat`.
- **Segment Anything (SAM 1)** (Meta, April 2023) and **SAM 2** (Meta,
  July 2024) — promptable universal segmentation, trained on 1B+
  masks, zero-shot on essentially any object. SAM 2 added video
  tracking. Annotation pipelines that took human-weeks now take an
  afternoon. HuggingFace: `facebook/sam2-hiera-large`; repo:
  `facebookresearch/segment-anything-2`.
- **DINOv2** (Meta, April 2023) — self-supervised vision features
  that work zero-shot for classification, retrieval, and depth. A
  ViT trained on unlabeled images well enough that frozen features
  match supervised models on most downstream tasks. HuggingFace:
  `facebook/dinov2-base`; repo: `facebookresearch/dinov2`.
- **Depth-Anything v1 / v2** (Yang et al., CVPR 2024 / arXiv 2024) —
  monocular metric depth at production quality from a huge student-
  teacher pipeline on unlabeled images. Made one-camera depth viable
  for background blur, AR placement, and rough obstacle avoidance.
  HuggingFace: `depth-anything/Depth-Anything-V2-Large`; repo:
  `DepthAnything/Depth-Anything-V2`.
- **FoundationPose** (NVIDIA, CVPR 2024 best paper) — 6-DoF pose
  from a CAD mesh + RGB-D crop, no per-object training. Production-
  ready for bin picking. Repo: `NVlabs/FoundationPose`.
- **MegaPose** (Labbe et al., 2022) — earlier render-and-compare
  6-DoF pose family that set the template FoundationPose refined.
  Repo: `megapose6d/megapose6d`.
- **DROID-SLAM** (Teed & Deng, NeurIPS 2021) — a recurrent network
  that does the bundle-adjustment step itself, first to convincingly
  beat ORB-SLAM3 on benchmarks. Repo: `princeton-vl/DROID-SLAM`.
- **VGGT** (Wang et al., 2025) — feed-forward 3D reconstruction from
  a few images: a transformer outputs camera poses, depth, and a
  point cloud in one forward pass, no per-scene optimization. Raises
  the question of whether classical SfM (COLMAP) has a future for
  small scenes. Repo: `facebookresearch/vggt`.
- **CoTracker, TAPIR** (Meta, DeepMind, 2023-2024) — dense long-term
  point tracking through video, including through occlusion. Replaces
  keyframe tricks and Kalman filters for many video tasks. Repos:
  `facebookresearch/co-tracker`, `google-deepmind/tapnet`.

## Open-source stack

The libraries you will actually install.

- **OpenCV** — the jQuery of computer vision. 25 years old, ships
  everywhere, do not avoid it. Python and C++, quirky API, inconsistent
  BGR-vs-RGB, unbeatable for basic operations.
- **Open3D** — point clouds, meshes, RGB-D processing. The Intel-led
  3D companion to OpenCV.
- **PyTorch3D** — Facebook's differentiable 3D library. Renderers and
  3D ops you can backprop through.
- **Nerfstudio** — turnkey NeRF / Gaussian Splatting training. Drop
  in photos, get a scene.
- **gsplat** — the fast CUDA backbone for Gaussian Splatting.
- **COLMAP** — classical structure-from-motion: photos in, camera
  poses + sparse point cloud out. First step in most NeRF / GS
  pipelines. **glomap** (2024+) is the faster modern alternative.
- **ORB-SLAM3, OpenVSLAM, VINS-Fusion** — dominant open-source
  classical SLAM systems. C++; you will see all three in robotics
  internships.
- **MMDetection, MMSegmentation, Detectron2** — model zoos for
  detection and segmentation training. Detectron2 (Meta) is cleaner
  code; the MM* family (OpenMMLab) has more recent models.
- **Ultralytics YOLO (v8 / v11)** — the fast-iteration fine-tune-on-
  your-own-data detector. Not the most cited, but the most used.
- **FoundationPose, MegaPose, GigaPose** — pretrained 6-DoF pose
  inference, drop-in ready.
- **hloc** (HierarchicalLocalization) — modern visual localization
  pipeline (SuperPoint + SuperGlue / LightGlue).
- **Hugging Face Transformers** — one-line loading of vision
  foundation models (SAM, DINOv2, Depth-Anything) via
  `AutoImageProcessor`. Use it.
- **Kornia** — classical CV (warps, filters, color conversions,
  geometry) as differentiable PyTorch ops you can drop into a
  training loop.
- **timm** (pytorch-image-models, Ross Wightman, now under Hugging
  Face) — huge zoo of image-classification backbones with consistent
  APIs and pretrained weights.
- **Albumentations** — fast image augmentation pipelines: crops,
  flips, color jitter, weather effects.
- **MONAI** — medical-imaging DL framework: 3D volumes, DICOM I/O,
  organ-segmentation models. Crosses into industrial CT and 3D
  image-stack tasks.
- **supervision** (Roboflow) — utility belt for chaining detectors,
  trackers, annotators, and writing video outputs.
- **Lightning AI / PyTorch Lightning** — training-loop boilerplate
  abstraction. Hides the for-loop, optimizer step, and distributed
  plumbing.
- **DeepStream** (NVIDIA) — production video-analytics framework on
  GStreamer with TensorRT-accelerated inference nodes. The thing for
  32 RTSP cameras through a detector on one Jetson.
- **GStreamer** — the underlying media-pipeline layer DeepStream
  and many camera drivers sit on. Source/filter/sink graphs,
  hardware-accelerated codecs.
- **Hydra** (Facebook Research) — YAML config composition,
  hyperparameter sweeps, CLI overrides for ML experiments. Pairs
  naturally with Lightning.
- **PyTorch checkpoint** — a `.pt` or `.ckpt` file with model
  weights. You `torch.load()` it and feed it tensors.

## Datasets that show up in every paper

- **KITTI** (2012) — outdoor driving; ageing but still benchmarked.
- **nuScenes** (2019) — large multi-modal AV dataset.
- **ScanNet, ScanNet++** — indoor RGB-D, the default for indoor 3D.
- **TUM RGB-D, EuRoC** — handheld / drone SLAM benchmarks.
- **Replica, Hypersim** — photoreal synthetic indoor for sim2real.
- **BOP** (Benchmark for 6D Object Pose) — standard for 6-DoF pose
  evaluation.
- **MS COCO, Objects365, LVIS** — detection / segmentation classics.
- **Open Images V7** — 9M images with multi-label annotations.
- **Argoverse 2** — multi-city AV dataset with HD-map context;
  common motion-forecasting benchmark too.
- **Waymo Open Dataset** — LiDAR + camera with 3D bounding boxes;
  one of the largest public AV datasets, with periodic challenges.
- **Lyft Level 5 / Woven by Toyota** — Lyft's AV dataset, later
  stewarded by Woven. Standard in trajectory-forecasting benchmarks.
- **Mapillary** — crowdsourced street-level imagery for large-scale
  visual place recognition and semantic segmentation.
- **BDD100K** (Berkeley) — 100k driving videos across weather and
  time-of-day; the "off the sunny California test set" benchmark.
- **ADE20K** (MIT) — scene parsing with hundreds of fine semantic
  classes; the indoor / general-scene complement to COCO.
- **NYU Depth V2 (NYUv2)** — small classic indoor RGB-D dataset;
  default sanity check for monocular depth.

## Production perception stacks decomposed

A hypothetical autonomous mobile robot (AMR) — a warehouse cart that
drives between shelves and grabs totes — broken down by package.

1. **Camera driver** — `usb_cam`, `realsense2_camera`, or a vendor
   ROS 2 driver. Publishes raw frames on a ROS 2 topic.
2. **image_transport** — handles compressed transport (JPEG, Theora,
   H.264) between nodes so you do not push raw 1080p over loopback.
3. **camera_info / rectification** — `image_proc` undistorts the raw
   frame using calibration intrinsics.
4. **Segmentation** — SAM 2 (via a ROS 2 wrapper or a HuggingFace
   node) produces per-object masks for the totes. Production swaps
   in a fine-tuned smaller model.
5. **6-DoF pose** — FoundationPose takes the masked region, the
   tote CAD mesh, and depth, and publishes a
   `geometry_msgs/PoseStamped` on `/totes/pose`.
6. **TF tree** — the pose is broadcast as a `tf2` transform so other
   nodes can ask "where is `tote_42` in the `map` frame?" with built-
   in time interpolation.
7. **Costmap / occupancy** — a Nav2 plugin consumes the LiDAR scan
   plus detected obstacles and rasterizes a 2D costmap.
8. **Planner + controller** — Nav2's planner (Smac, NavFn) and
   controller (DWB, MPPI) consume the costmap and goal pose and
   publish `/cmd_vel`.
9. **Recording + replay** — `ros2 bag record` captures topics every
   run; bug fires, replay against a new perception node, diff outputs.

Knowing this stack end-to-end is what separates "I can fine-tune a
detector" from "I can ship a robot."

## Staying current

- **CVPR / ICCV / ECCV proceedings** — `openaccess.thecvf.com`,
  free, skim the awards list each year.
- **arXiv cs.CV** — firehose; filter via `arxiv-sanity-lite` or
  `huggingface.co/papers`.
- **Two Minute Papers** (YouTube, Károly Zsolnai-Fehér).
- **Yannic Kilcher** (YouTube) — deeper paper walkthroughs.
- **The Robot Report** (`therobotreport.com`).
- **IEEE Spectrum Robotics**.
- **Robohub** (`robohub.org`).
- **ROS Discourse** (`discourse.ros.org`).
- **X / Twitter** — `@AIatMeta`, `@NVIDIAAIDev`, `@_akhaliq`,
  `@karpathy`, `@jonbarron`. See `04-market.md` for more handles.
- **Hugging Face Spaces and Models tabs**.
- **Papers With Code** (`paperswithcode.com`) — benchmark leaderboards.
- **GitHub trending in Python**.

## How to skim a CV paper in 20 minutes

1. Read the abstract: problem, method, numbers.
2. Look at Figure 1 — usually the architecture diagram or hero result.
3. Look at the qualitative results grid (Figures 5 / 6, usually).
4. Read the last paragraph of the intro for the contributions bullet list.
5. Check the GitHub repo: exists, `pip install`-able, recently committed.
6. Search Hugging Face for a checkpoint; if present you can run inference in five minutes.
