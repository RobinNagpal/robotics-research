# Examples of Work

This is a tour of "what perception code looks like in the wild." If
you're new, skim it — the goal is to know the names so the rest of the
material has hooks to land on.

## Deployed products (real-world perception running today)

These are the equivalent of "production at scale" in web terms — large
teams, billions of inference calls, real customers.

- **Waymo, Zoox, Cruise** — multi-camera + LiDAR + radar perception
  stacks for full self-driving. Waymo's been driverless in Phoenix,
  SF, LA, Austin, and Atlanta as of 2025. Big perception teams,
  research-grade work, $200k+ base.
- **Tesla FSD** — famously camera-only ("vision-only"); ships an
  "occupancy network" that builds a voxel-grid of free vs. occupied
  space directly from 8 cameras. Different bet than the rest of the
  industry.
- **Mobileye EyeQ** — ADAS perception SoCs shipped in 150M+ vehicles
  cumulatively (as of 2024). The quiet giant of automotive vision.
- **Skydio drones** — fully autonomous obstacle-avoidance flight from
  6 cameras + on-board NN inference on a Jetson. Their tech demos are
  the canonical "wow, that's perception working" moment.
- **Boston Dynamics Spot / Atlas** — depth-camera-driven obstacle maps
  and semantic terrain classification. Spot is the most-deployed
  legged robot in industry today.
- **Apple Vision Pro, iPhone LiDAR + ARKit** — real-time scene mesh,
  plane detection, hand tracking, eye tracking. The most polished
  consumer perception stack on the planet.
- **Pickle Robot, Symbotic, Covariant** (Covariant acquired by Amazon
  Aug 2024) — warehouse perception: bin segmentation, 6-DoF pose for
  irregular SKUs.
- **Verkada, Ambient.ai, Veo** — security-camera anomaly detection +
  person/event recognition. The "computer vision as a SaaS" wedge.

## Landmark research papers (read these eventually, in this order)

The papers that built the modern stack. Treat each as a 1-3 day
investment.

- **NeRF** (Mildenhall et al., ECCV 2020) — neural radiance fields.
  Started the neural-3D wave. The "AlexNet moment" for 3D vision.
- **3D Gaussian Splatting** (Kerbl et al., SIGGRAPH 2023, Inria) —
  real-time photoreal 3D rendering from photos. Killed NeRF as the
  default and is now the mainstream choice for robotics digital
  twins. ~100x faster to render.
- **Segment Anything (SAM 1)** (Meta, April 2023) and **SAM 2** (Meta,
  July 2024) — promptable, universal segmentation. Trained on 1B+
  masks; works zero-shot on essentially any object. SAM 2 added video
  tracking.
- **DINOv2** (Meta, April 2023) — self-supervised vision features
  that work zero-shot for classification, retrieval, depth. The
  closest thing CV has to a "CLIP for pure pixels."
- **Depth-Anything v1 / v2** (Yang et al., CVPR 2024 / arXiv 2024) —
  monocular metric depth at production quality. Single image -> dense
  depth map.
- **FoundationPose** (NVIDIA, CVPR 2024 best paper) — 6-DoF object
  pose from a single CAD model, no per-object training required.
  Production-ready for bin picking.
- **MegaPose** (Labbe et al., 2022) — earlier instance of the
  "render-and-compare" 6-DoF pose family.
- **DROID-SLAM** (Teed & Deng, NeurIPS 2021) — learned SLAM end to
  end. First to convincingly beat ORB-SLAM3 on benchmarks.
- **VGGT** (Wang et al., 2025) — feed-forward 3D scene reconstruction
  from a few images. No optimization, just a transformer. Latest
  state of the art.
- **CoTracker, TAPIR** (Meta, DeepMind, 2023-2024) — dense long-term
  point tracking through video. The "dense optical flow" of the 2020s.

## Open-source stack (the equivalent of "npm packages you'll actually use")

- **OpenCV** — the jQuery of computer vision. 25 years old, ships
  everywhere, do not avoid it. Python and C++.
- **Open3D** — point clouds, meshes, RGB-D processing. The Intel-led
  3D companion to OpenCV.
- **PyTorch3D** — Facebook's differentiable 3D library. The way to do
  3D inside a neural network.
- **Nerfstudio** — turnkey NeRF / Gaussian Splatting training. Drop
  in photos, get a scene.
- **gsplat** — the fast CUDA backbone for Gaussian Splatting. The
  "PyTorch kernel" of the splatting world.
- **COLMAP** — the classical "structure from motion" pipeline. Given
  photos, recovers camera poses + a sparse 3D point cloud. The first
  step in most NeRF / GS pipelines. **glomap** is the modern faster
  alternative (2024+).
- **ORB-SLAM3, OpenVSLAM, VINS-Fusion** — the dominant open-source
  classical SLAM systems. C++; you'll see all three in robotics
  internships.
- **MMDetection, MMSegmentation, Detectron2** — model zoos for
  detection and segmentation training.
- **Ultralytics YOLO (v8 / v11)** — the fast-iteration, fine-tune-on-
  your-own-data detector. Not the most cited, but the most used in
  industry.
- **FoundationPose, MegaPose, GigaPose** — pretrained 6-DoF pose
  inference, drop-in ready.
- **hloc** (HierarchicalLocalization) — modern visual localization
  pipeline (SuperPoint + SuperGlue / LightGlue).
- **Hugging Face Transformers + `transformers.AutoImageProcessor`** —
  vision foundation models (SAM, DINOv2, Depth-Anything) are all
  one-line loads now. Use them.

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
