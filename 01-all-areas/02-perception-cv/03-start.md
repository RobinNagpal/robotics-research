# How to Get Started

A concrete 8-week plan. Ship a working perception demo end-to-end by
the end. Build a toy first, then read the docs that suddenly make
sense.

Three things to remember: (1) calibrate everything, twice; (2)
visualize every intermediate output — `rerun` and `rviz2` are your
`console.log`; (3) ship a tiny artifact at the end of every week.

Background reading: `00-basics.md` (field map), `01-examples.md`
(working demos), `02-learn.md` (textbooks and courses),
`05-projects/` (portfolio inspiration), `06-courses.md`
(structured-curriculum option).

## Prerequisites (1 week, can overlap with Week 1)

- Comfortable Python. If you only know TypeScript, spend a weekend
  on list comprehensions, `with` blocks, virtualenvs, `pip` vs
  `conda`. Reach for `uv` first — fast, deterministic, the closest
  Python has to `pnpm`.
- Comfortable with NumPy and basic PyTorch (Karpathy's
  "neural networks zero-to-hero" if not).
- A laptop with a webcam.
- Optional: a smartphone (iPhone 12+ or Pixel) for scan capture.
  iPhone Pro models add LiDAR — a real depth sensor in your pocket.
- A GPU. Pick one:
  - **Rent**: Lambda Labs, RunPod, Modal, Vast.ai. ~$0.40-$2/hr for
    an A100/H100. Easiest start.
  - **Colab Pro** ($10/mo) — fine for tutorials and light
    fine-tuning.
  - **Local 16-24GB GPU** (RTX 4070+ / 3090 / 4090) — best if you
    own one. Nerfstudio and gsplat are VRAM-hungry.
- Two monitors if you can. Terminal, 3D viewer, and Jupyter open
  side by side is the default workflow.

## Week 1 — Classical foundations: the camera math

Goal: stop being afraid of camera matrices.

A camera matrix is a 3x3 array mapping a 3D point to a pixel. You
will calibrate cameras dozens of times; skipping it once costs you
a day chasing a 5-pixel offset.

- Skim **Stanford CS231A** lecture notes, lectures 1-4: camera
  model, calibration, single-view metrology, two-view geometry.
- **Calibrate your laptop webcam** with OpenCV's
  `cv2.calibrateCamera()` and a printed checkerboard. Get an
  intrinsic matrix `K` and reproject a 3D point onto the image.

  ```python
  import cv2, numpy as np
  objp = np.zeros((6*9, 3), np.float32)
  objp[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)
  obj_points, img_points = [], []  # filled by looping over images
  # for each frame: cv2.findChessboardCorners + append to lists
  ret, K, dist, rvecs, tvecs = cv2.calibrateCamera(
      obj_points, img_points, gray.shape[::-1], None, None)
  ```

- Re-implement pinhole projection, RANSAC, and PnP once. Not for
  production — for the intuition.

**Common ways this week goes wrong**

- Nonsense `K` values (focal length 50 or 50,000 pixels). Your
  printer scaled the PDF; measure a square with a ruler and pass
  the real edge length in meters.
- `cv2.findChessboardCorners` returns `False` on most frames. Bad
  lighting or the board is too small; move closer and add a lamp.
- Reprojection error 20+ pixels. You mixed up rows/columns, or used
  a curling page. Tape it to a clipboard.

**Deliverable**: one image of your desk with a 3D cube reprojected
onto the checkerboard, with `K` and reprojection error in the
caption.

## Week 2 — Modern detection and segmentation

Goal: load a vision foundation model and run it.

- Read the **CS231n** notes on CNNs and Transformers. Recognize the
  building blocks; do not derive backprop.
- Run a **SAM 2** segmentation model on your own photos via Hugging
  Face. Click a point on a mug, get a mask.

  ```python
  from transformers import pipeline
  seg = pipeline("mask-generation", model="facebook/sam2-hiera-large")
  masks = seg("mug.jpg")  # confirm exact model id on the HF hub
  ```

- Run **DINOv2** to extract per-image embeddings. Cluster 100
  photos with `sklearn.cluster.KMeans` and check that semantically
  similar images land in the same cluster.
- Fine-tune a tiny **YOLO** detector (Ultralytics) on 50 photos of
  one object. Label with Roboflow or CVAT. ~10 minutes on a free
  GPU.

**Common ways this week goes wrong**

- SAM 2 install fails on a `torch` version mismatch. Install
  `torch` first, matched to your CUDA version; then install SAM 2.
  Do not let pip resolve both at once.
- YOLO mAP comes back at 0.05. Labels are in the wrong format
  (YOLO wants normalized xywh in a per-image `.txt`). Re-export
  with the explicit "YOLOv8 PyTorch" preset in Roboflow.
- DINOv2 embeddings collapse into one blob. You forgot to
  L2-normalize before KMeans, or picked too few clusters (start
  k=10 for 100 images).

**Deliverable**: a 10-second screen recording of SAM 2 masks
appearing as you click, or a grid of your YOLO detector's outputs
on 8 held-out images.

## Week 3 — Monocular depth and 3D from pixels

Goal: build a "phone to 3D" toy.

- Run **Depth-Anything v2** on a single photo. Plot the depth map.
  Colors are relative depth, not metric — for metric depth use
  `Metric3D`, `UniDepth`, or a real depth camera.
- Take 30-50 photos of your desk from different angles. Run
  **COLMAP** (or **glomap**, modern and faster) to recover camera
  poses and a sparse point cloud. Walk in a half-circle, vary
  height; do not pivot in place. COLMAP needs parallax.
- Train a small NeRF or 3D Gaussian Splat with **Nerfstudio**
  (5-10 min on a 4070/A100). Splats render far faster than NeRFs at
  similar quality — prefer `splatfacto`.

  ```bash
  ns-process-data images --data ./photos --output-dir ./processed
  ns-train splatfacto --data ./processed
  # then: ns-viewer --load-config outputs/.../config.yml
  ```

**Common ways this week goes wrong**

- Nerfstudio crashes with CUDA OOM. Drop batch size, downsample to
  1080p, or rent an A100. Splatfacto wants 16+ GB VRAM.
- COLMAP registers only 8 of 50 images. Photos too similar (you
  stood still) or too different (lighting changed). Re-shoot in one
  continuous pass.
- Splat looks great from training views, garbage from novel
  angles. You did not cover enough viewpoints — splats interpolate,
  they do not extrapolate.

**Deliverable**: a 5-second fly-through video of your desk splat,
or an interactive viewer link (Polycam, SuperSplat, self-hosted
gsplat).

## Week 4 — 6-DoF pose for a real object

Goal: localize a known object in 6D from a webcam image.

6-DoF: three translation (x, y, z), three rotation (roll, pitch,
yaw). FoundationPose outputs a 4x4 homogeneous transform per frame
(top-left 3x3 rotation, top-right 3x1 translation in meters, bottom
row `[0, 0, 0, 1]`).

- Pick a desk object with a CAD model online (LEGO, 3D print, a
  mug). Or scan it with **Polycam** and export `.obj` / `.glb`.
- Run **FoundationPose** on a video of you moving the object.
- Visualize the pose stream in **rerun.io**: log the mesh once, log
  a `rr.Transform3D` per frame, scrub the timeline.
- This is the core of an industrial bin-picker.

**Common ways this week goes wrong**

- Rendered mesh is 90 degrees off from the real object. Your CAD
  uses a different convention (Y-up vs Z-up, mm vs m). Bake a
  transform into the mesh.
- Pose jitters wildly. Dim lighting or partial occlusion. Add a
  lamp and keep the whole object in view.
- No depth stream because your laptop is RGB-only. Use
  FoundationPose's RGB-only mode, or borrow a RealSense.

**Deliverable**: a side-by-side video — webcam feed on the left,
CAD mesh snapping to the object's pose in rerun on the right.

## Week 5 — SLAM: the moving-camera problem

Goal: make a map from a video.

SLAM (Simultaneous Localization and Mapping): build a map while
figuring out where you are in it. Hard enough that people still
publish on it thirty years in.

- Record 1080p / 30 fps video walking through your apartment, or
  use a EuRoC dataset (free, includes IMU + cameras). Walk slowly,
  no fast pans, avoid blank white walls.
- Run **ORB-SLAM3** in monocular or RGB-D mode. Visualize the
  trajectory and sparse map.
- Read the **DROID-SLAM** paper; run their pretrained model on the
  same video. Compare against ORB-SLAM3.
- Plot and compare trajectories with `evo`:

  ```bash
  pip install evo --upgrade
  evo_traj tum trajectory.txt --plot
  evo_ape tum gt.txt est.txt --align --correct_scale
  ```

  A "good" monocular trajectory closes the loop with APE under
  about 1% of trajectory length on EuRoC-class data. A drifting
  one spirals open.

**Common ways this week goes wrong**

- ORB-SLAM3 fails at the linker after 45 minutes. The
  Pangolin/OpenCV/Eigen version dance is real — use the community
  Docker image (`jahaniam/orbslam3` or current equivalent).
- Monocular SLAM gives a map in arbitrary units. Correct, not a
  bug — monocular cannot recover scale without an IMU or known
  object. Use RGB-D or stereo.
- Trajectory looks fine but `evo_ape` reports huge error. Frames
  or time offsets differ; use `--align` and `--correct_scale`.

**Deliverable**: a top-down trajectory plot with loop closure
visible, plus an `evo_ape` number against ground truth or a second
pass.

## Week 6 — ROS2 and a real perception node

Goal: ship perception inside a real robotics framework.

ROS2 is the message bus, build system, and tooling standard for
robotics. A topic subscription is roughly a Redis pub/sub channel:
declare a topic and a message type, get a callback on every publish.

- Install **ROS2 Jazzy** (Ubuntu 24.04, current LTS) or **Humble**
  (22.04). Use the official Docker image if your distro fights you.
- Build an **rclpy** node that subscribes to `/camera/image_raw`,
  runs SAM 2 segmentation, and publishes a mask topic. Visualize
  in `rviz2`.

  ```python
  import rclpy
  from rclpy.node import Node
  from sensor_msgs.msg import Image

  class FrameSizePrinter(Node):
      def __init__(self):
          super().__init__('frame_size_printer')
          self.sub = self.create_subscription(
              Image, '/camera/image_raw', self.cb, 10)

      def cb(self, msg: Image):
          self.get_logger().info(
              f'frame {msg.width}x{msg.height} encoding={msg.encoding}')

  def main():
      rclpy.init()
      rclpy.spin(FrameSizePrinter())
      rclpy.shutdown()

  if __name__ == '__main__':
      main()
  ```

  Build with `colcon build`, run with `ros2 run your_pkg
  frame_size_printer`. Use `cv_bridge` to convert `Image` to an
  OpenCV ndarray when you do real perception on the frame.
- If you have a depth camera (RealSense / iPhone via ROS bridge),
  publish a colored point cloud. The `realsense2_camera` package
  exposes `/camera/depth/...`; sync color and depth with a
  `message_filters.ApproximateTimeSynchronizer`.

**Common ways this week goes wrong**

- `colcon build` succeeds but `ros2 run` says "package not found."
  You forgot to `source install/setup.bash` in the new shell.
- Two nodes cannot see each other's topics. `ROS_DOMAIN_ID`
  differs across shells, or you are on different networks.
- Wedging CUDA + SAM 2 inside a ROS2 node turns into a multi-day
  yak shave. Run the model in a separate Docker container with
  CUDA baked in, expose it as a tiny gRPC or HTTP service, and
  have the rclpy node call it.

**Deliverable**: a GitHub gist of your rclpy node plus a 15-second
rviz2 recording showing the camera feed and a live segmentation
mask overlay.

## Weeks 7-8 — Ship one substantial internal reference build

Pick something the team can show as a credibility anchor in client
pitches. Scope ruthlessly. A perception project with no demo video
does not exist as far as a prospective client is concerned.

Ideas:

- **Phone-to-Gaussian-splat web app.** User uploads a phone video,
  service returns a `.splat` plus an interactive viewer URL. Wrap
  Nerfstudio in a FastAPI job queue (Celery + Redis). Target:
  realtors, e-commerce sellers, indie game devs. Pricing: $5-$20
  per scan or ~$50/month. Demo: phone walking around an object, a
  spinner, then a browser viewer in under 10 seconds. Ship a
  Dockerfile, `docker compose` one-liner, and an `examples/` folder
  with a finished `.splat`.

- **6-DoF pose REST endpoint.** Customer uploads a CAD model; you
  return a Docker container with a `/pose` endpoint that takes an
  RGB-D frame and returns a 4x4 transform plus confidence. Wrap
  FoundationPose. Target: small-shop integrators avoiding
  Halcon/MVTec. Pricing: $500-$2k per integration, or $200/month
  SaaS. Demo: 10-second `curl` upload, response JSON, rerun.io
  playback of pose snapping to the object. Include a `pose-eval/`
  folder with BOP-style metrics and a `make demo` target.

- **Anomaly detection demo.** 50 "good" and 50 "bad" photos of any
  product (PCBs, fruit, fabric, 3D prints). Train PatchCore via
  anomalib. Ship a Streamlit dashboard with heatmaps and pass/fail.
  Target: small manufacturers who cannot justify Cognex. Pricing:
  $1-2k custom, or $99/month hosted with a per-image API. Include
  the training notebook, the app, and a small or public dataset
  (MVTec AD).

- **SLAM benchmark dashboard.** Drop in a ROS bag, run ORB-SLAM3 +
  VINS-Fusion + a learned method (DROID-SLAM or NICER-SLAM), get a
  side-by-side video and an `evo`-generated trajectory-error PDF.
  Target: research engineers comparing baselines. Open-source it
  as a credibility signal for the team. Demo: three trajectories
  overlaid on EuRoC ground truth with APE/RPE numbers in a corner.
  Ship Dockerfiles per SLAM system and a `python bench.py --bag
  my.bag` entrypoint.

**Week 8 deliverable**: a 60-second demo video plus a polished
README, linked from one tweet or LinkedIn post. README needs a hero
GIF, a one-line "what this is", a one-line "who this is for", the
`docker compose up` command, then the technical detail.

**Common ways Weeks 7-8 go wrong**

- You scope a "platform" and finish nothing. Pick the smallest
  vertical slice and ship that.
- You skip the demo video. 90% of viewers never clone the repo;
  spend an afternoon on a clean recording with captions.
- README assumes a roboticist reader. Show it to a web-dev friend;
  if they cannot tell what it does in 30 seconds, rewrite the top.

## Tooling setup

- **OS**: Ubuntu 24.04 LTS (Jazzy) or 22.04 LTS (Humble). Dual-boot
  or dedicated machine, not a VM — GPU passthrough is a yak shave.
  macOS works for Weeks 1-3 on CPU/MPS. Avoid Windows + WSL2 as
  primary.
- **NVIDIA driver**: `ubuntu-drivers autoinstall`, reboot, verify
  with `nvidia-smi`. Get CUDA from your PyTorch wheel; only install
  the system toolkit (`nvcc`) if you build custom kernels (gsplat).
- **Python envs**: `uv` by default. Fall back to `conda` / `mamba`
  for packages with conda-forge-only builds (older 3D code). Pin
  3.10 or 3.11 per project; 3.12+ still breaks some binary wheels.
- **ROS2**: apt install on matching Ubuntu for learning; official
  `osrf/ros:jazzy-desktop` Docker image for production or shared
  dev.
- **VS Code extensions**: `ROS` (Microsoft), `Pylance`, `Ruff`,
  `Even Better TOML`, `Docker`, `Dev Containers`, `Jupyter`. Cursor
  and Zed work fine with the same list.
- **Visualization**: `pip install rerun-sdk open3d`; install
  Foxglove Studio for web-based rviz2 when GUI forwarding is
  painful.
- **Project template**: keep a personal `cookiecutter-perception`
  or `uv init` template with `pyproject.toml`, `Dockerfile`,
  `Makefile` (`make fmt`, `lint`, `test`), and gitignored `data/`
  and `outputs/`.

## Stretch goals

- Contribute a small fix (`good first issue`) to Nerfstudio,
  gsplat, ORB-SLAM3, anomalib, or a Hugging Face vision pipeline.
- Reproduce a recent CVPR paper from scratch (pick one with code
  released); match a table number within 10% and write up what
  went wrong.
- Deploy a perception model to an edge device (Raspberry Pi 5 +
  Hailo-8L, Jetson Orin Nano 8GB, Coral USB): convert YOLO to ONNX,
  then TensorRT or Hailo runtime, benchmark FPS vs accuracy.
- Stand up a multi-camera rig: two cheap webcams, calibration board,
  computed extrinsics, then stereo depth.

## What NOT to do in the first 8 weeks

- Do not write your own SLAM from scratch — ORB-SLAM3 is ~30k lines
  of C++ that took a decade.
- Do not train a foundation model from scratch — SAM, DINOv2, and
  Depth-Anything cost six- to seven-figure compute budgets.
- Do not buy a Velodyne or Ouster LiDAR yet — $5k+ for hardware
  you cannot exploit yet; iPhone LiDAR or a RealSense covers
  Weeks 1-8.
- Do not set up a full self-driving stack — Autoware/Apollo are
  10+ GB of dependencies and need real cars or high-fidelity sim.
- Do not chase every arXiv paper — pick one per topic, finish the
  week's project, move on.
- Do not refactor before it works — get the 200-line script
  end-to-end before splitting into modules.

## Datasets you should know by name

- **KITTI** — outdoor driving (since 2012, still benchmarked).
- **nuScenes** — large multi-modal AV.
- **ScanNet, ScanNet++** — indoor RGB-D, default for indoor 3D.
- **TUM RGB-D, EuRoC** — handheld / drone SLAM.
- **Replica, Hypersim, Habitat-Matterport** — photoreal indoor sim.
- **BOP** — 6-DoF pose evaluation.
- **MS COCO, Objects365, LVIS** — detection / segmentation classics.
- **DROID** (Stanford) — large robot manipulation dataset with
  cameras + actions (useful for VLA crossover).

## Benchmarks (so you can compare to papers)

- **KITTI Odometry, EuRoC, TUM RGB-D** — SLAM accuracy.
- **BOP Challenge** — 6-DoF pose.
- **NYU Depth v2, ETH3D** — monocular depth.
- **Cityscapes, ADE20K** — semantic segmentation.

## Cheap hardware (optional but motivating)

Prices are late-2025 / early-2026 USD street; verify before buying.

- **Intel RealSense D435 / D455** (~$300-400) — workhorse RGB-D
  stereo. Good for: depth basics, ROS2 tutorials, indoor SLAM.
- **Orbbec Femto Bolt** (~$300) — ToF depth, Azure Kinect
  successor. Good for: indoor mapping, close-range depth quality.
- **iPhone with LiDAR** (Pro 12+, used ~$250-350) — pair with
  Polycam, Scaniverse, or Record3D. Good for: object and room
  scans with zero setup.
- **OAK-D series** (Luxonis, ~$200-400) — stereo depth + on-device
  neural inference. Good for: hobby robots and battery-powered
  demos.
- **Livox Mid-360 / Mid-70** ($1.5-3k) — entry-tier solid-state
  LiDAR. Good for: outdoor SLAM, drones, AMRs. Overkill until you
  have a specific need.
- **NVIDIA Jetson Orin Nano Super 8GB dev kit** (~$249) — small
  CUDA GPU on Arm. Good for: on-robot inference and Jetson tooling.
- **Raspberry Pi 5 (8GB)** (~$80) — general SBC, no GPU. Good for:
  pairing with Hailo-8L AI hat (~$70) or Coral USB (~$60) for
  cheap edge inference.
- **Used RTX 3090 24GB** (~$700-900) — best dollar-per-VRAM for
  local Nerfstudio / gsplat training and fine-tuning.
- **Generic 8" checkerboard on foamcore** (~$10) — laminate a
  7x10 or 9x12 board, glue to a flat backer. Good for: calibrating
  every camera you will ever own.

## Communities and conferences

- **CVPR, ICCV, ECCV** — the three vision conferences. CVPR in
  June; ECCV biennial in October (even years); ICCV biennial in
  October (odd years). All free livestream + paper PDFs.
- **CoRL, ICRA, IROS** — robotics venues with strong perception
  tracks.
- **Hugging Face** Spaces and model hub — try foundation models
  hands-on.
- **r/computervision, r/robotics, r/ROS** — for lurking.
- **Roboflow Universe** — open detection datasets.
- X/Twitter: @TomasJakab, @AjdDavison, @jonbarron, @yenchenlin,
  @DieterFox, @ShuranSong.
