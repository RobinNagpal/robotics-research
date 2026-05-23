# How to Get Started

A concrete 8-week plan. The goal isn't to read everything — it's to
ship a working perception demo end-to-end by the end. Treat it like
learning a new framework: build a toy first, then go back and read
the docs that suddenly make sense.

## Prerequisites (1 week, can overlap with Week 1)

- Comfortable Python.
- Comfortable with NumPy and basic PyTorch (Karpathy's "neural
  networks zero-to-hero" if not).
- A laptop with a webcam.
- Optional but very useful: a smartphone (any iPhone 12+ or Pixel
  works — for scan capture). An iPhone with LiDAR (Pro models) is
  even better.
- A GPU. Three options:
  - **Rent**: Lambda Labs, RunPod, Modal, Vast.ai. ~$0.40-$2/hr for
    an A100/H100. Easiest start.
  - **Colab Pro** ($10/mo) — fine for tutorials, light fine-tuning.
  - **Local 16-24GB GPU** (RTX 4070+ / 3090 / 4090) — best if you
    already own one. Nerfstudio + gsplat are very GPU-VRAM hungry.

## Week 1: Classical foundations — the camera math

Goal: stop being afraid of camera matrices.

- Skim **Stanford CS231A** lecture notes (free PDFs). Read the first
  4 lectures: camera model, calibration, single-view metrology,
  two-view geometry.
- **Calibrate your laptop webcam** with OpenCV's
  `cv2.calibrateCamera()` and a printed checkerboard. Get an
  intrinsic matrix `K` and reproject a 3D point onto the image.
  When the reprojection lands where you expect, you "get it."
- Re-implement: pinhole projection, RANSAC, PnP. Don't write your
  own RANSAC for production — but writing one once teaches you why
  it works.

## Week 2: Modern detection and segmentation

Goal: load a vision foundation model and run it.

- Read the **CS231n** notes on CNNs and on Transformers (the deep
  CV companion to CS231A).
- Run **SAM 2** on your own photos via Hugging Face. Click a point
  on a mug, get a mask. Wire it into a small Python script.
- Run **DINOv2** to extract per-image embeddings; cluster the
  embeddings of 100 photos with `sklearn.cluster.KMeans` and see if
  semantically similar images end up in the same cluster.
- Train a tiny detector on a custom dataset with **YOLO v11**
  (Ultralytics). Collect 50 photos of one object, label with
  Roboflow or CVAT, fine-tune in 10 minutes on a free GPU.

## Week 3: Monocular depth and 3D from pixels

Goal: build a "phone -> 3D" toy.

- Run **Depth-Anything v2** on a single photo. Plot the depth map.
- Take 30-50 photos of your desk from different angles. Run
  **COLMAP** (or **glomap** — modern, faster) to recover camera
  poses and a sparse 3D point cloud.
- Feed the same photos into **Nerfstudio** and train a small NeRF
  (5-10 minutes on a 4070 / A100). Render a fly-through video.
- Train a **3D Gaussian Splat** of the same scene with
  `nerfstudio`'s `splatfacto` or **gsplat** directly. Compare
  quality and rendering speed — splats win.

## Week 4: 6-DoF pose for a real object

Goal: localize a known object in 6D from a webcam image.

- Pick an object you have on your desk that has a CAD model
  available online (LEGO, a 3D-printed thing, an off-the-shelf
  mug). Otherwise scan it with **Polycam** on your phone.
- Run **FoundationPose** on a video of you moving it around. You
  should get a 6-DoF pose per frame.
- This is the exact thing a bin-picking robot does. You've now
  implemented the core of an industrial picker.

## Week 5: SLAM — the moving-camera problem

Goal: make a map from a video.

- Walk through your apartment with your phone, recording 1080p
  video at 30 fps. Or use a EuRoC dataset (free, has IMU + cameras).
- Run **ORB-SLAM3** in monocular or RGB-D mode on the recording.
  Visualize the camera trajectory and the sparse map.
- Read the **DROID-SLAM** paper; run their pretrained model on the
  same video. Compare against ORB-SLAM3.

## Week 6: ROS2 + a real perception node

Goal: ship perception inside an actual robotics framework.

- Install **ROS2 Humble** (Ubuntu 22.04) or **Iron** (22.04/24.04).
- Build a small **rclpy** node that subscribes to a `/camera/
  image_raw` topic, runs SAM 2 segmentation, and publishes a mask
  topic. Visualize in `rviz2`.
- If you have a depth camera (RealSense / iPhone via ROS bridge),
  pipe its depth in too and publish a colored point cloud.

## Week 7-8: Build one substantial portfolio project

Pick something you'd put on your resume. Some ideas:

- **Phone-to-Gaussian-splat web app.** User uploads a phone video;
  service returns a `.splat` file + a viewer. Wrap Nerfstudio in a
  FastAPI job queue.
- **6-DoF pose REST endpoint.** Customer uploads a CAD model; you
  return a Docker container exposing a `/pose` endpoint that takes
  RGB-D and returns 6-DoF. Wrap FoundationPose.
- **Anomaly detection demo.** Take 50 "good" and 50 "bad" photos of
  any product (PCBs, fruit, fabric). Train a PatchCore / anomalib
  model. Ship a Streamlit dashboard.
- **SLAM benchmark dashboard.** Drop in a ROS bag, run ORB-SLAM3
  + VINS-Fusion + a learned method, output a side-by-side video and
  trajectory error PDF.

## Datasets you should know by name

- **KITTI** — outdoor driving (since 2012, still benchmarked).
- **nuScenes** — large multi-modal AV.
- **ScanNet, ScanNet++** — indoor RGB-D, default for indoor 3D.
- **TUM RGB-D, EuRoC** — handheld / drone SLAM.
- **Replica, Hypersim, Habitat-Matterport** — photoreal indoor sim.
- **BOP** — 6-DoF pose evaluation.
- **MS COCO, Objects365, LVIS** — detection / segmentation classics.
- **DROID** (Stanford) — large robot manipulation dataset with
  cameras + actions (useful for VLA crossover work).

## Benchmarks (so you can compare to papers)

- **KITTI Odometry, EuRoC, TUM RGB-D** — SLAM accuracy.
- **BOP Challenge** — 6-DoF pose.
- **NYU Depth v2, ETH3D** — monocular depth.
- **Cityscapes, ADE20K** — semantic segmentation.

## Cheap hardware (optional but motivating)

Prices reflect Q4 2025 / early 2026:

- **Intel RealSense D435 / D455** (~$300-400) — the workhorse RGB-D
  camera, supported everywhere.
- **Orbbec Femto Bolt** (~$300) — newer ToF depth, Microsoft-Azure-
  Kinect successor.
- **iPhone with LiDAR** (Pro models 12+, you may already own one)
  — combined with apps like Polycam, Scaniverse, or Record3D, this
  is the fastest "real depth camera" available.
- **OAK-D series** (Luxonis, ~$200-400) — depth + on-device neural
  inference, popular for hobby robots.
- **Livox Mid-360 / Mid-70** ($1.5-3k) — entry-tier LiDAR if you
  want to play with point clouds at scale.

## Communities and conferences

- **CVPR, ICCV, ECCV** — the three vision conferences. CVPR is in
  June, ECCV biennial in October (even years), ICCV biennial in
  October (odd years). All free livestream + paper PDFs.
- **CoRL, ICRA, IROS** — robotics venues with strong perception
  tracks.
- **Hugging Face** Spaces and model hub — try foundation models
  hands-on.
- **r/computervision, r/robotics, r/ROS** — for lurking.
- **Roboflow Universe** — open detection datasets.
- X/Twitter: @TomasJakab, @AjdDavison, @jonbarron, @yenchenlin,
  @DieterFox, @ShuranSong.
