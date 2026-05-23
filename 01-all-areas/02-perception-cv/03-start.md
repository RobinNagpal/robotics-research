# How to Get Started

A concrete 8-week plan. The goal isn't to read everything — it's to
ship a working perception demo end-to-end by the end. Treat it like
learning a new framework: build a toy first, then go back and read
the docs that suddenly make sense.

Mental model coming in from web dev: perception is a pipeline of
transforms, just like a middleware chain in Express. Pixels in, a
mask or a pose or a point cloud out. The hard part is not any single
node — it is that every node has its own coordinate frame, its own
units, and its own failure modes, and stitching them together feels
like wiring five GraphQL services with mismatched schemas. Expect the
first three weeks to feel like that. By week six it starts to click.

If you only remember three things from this doc: (1) calibrate
everything, twice; (2) visualize every intermediate output — `rerun`
and `rviz2` are your `console.log`; (3) ship a tiny artifact at the
end of every week so you have something to point at when someone
asks "what have you been doing?"

For background reading before you start: `00-basics.md` for the
field map, `01-examples.md` for working demos to crib from,
`02-learn.md` for the deeper textbooks and courses,
`05-projects.md` for portfolio inspiration, and `06-courses.md` for
the structured-curriculum option.

## Prerequisites (1 week, can overlap with Week 1)

- Comfortable Python. If you have only ever written TypeScript,
  spend a weekend on the language: list comprehensions, `with`
  blocks, virtualenvs, `pip` vs `conda`. Python's tooling story is
  roughly where Node's was around 2015 — many competing package
  managers, none of which fully win. `uv` (from Astral, same folks
  as ruff) is the closest analogue to `pnpm`: fast, deterministic,
  what you should reach for first.
- Comfortable with NumPy and basic PyTorch (Karpathy's "neural
  networks zero-to-hero" if not). Numpy arrays are the Lodash of
  scientific Python — you will use the same dozen functions
  (`reshape`, `transpose`, `stack`, `where`, broadcasting rules) on
  every line.
- A laptop with a webcam.
- Optional but very useful: a smartphone (any iPhone 12+ or Pixel
  works — for scan capture). An iPhone with LiDAR (Pro models) is
  even better — it gives you a real depth sensor in your pocket,
  the way an M1 MacBook gave web devs a real local dev server.
- A GPU. Three options:
  - **Rent**: Lambda Labs, RunPod, Modal, Vast.ai. ~$0.40-$2/hr for
    an A100/H100. Easiest start. Think of it like Vercel for ML:
    you push a script, a GPU spins up, you pay for what you used.
  - **Colab Pro** ($10/mo) — fine for tutorials, light fine-tuning.
    Notebook UX is a step down from VS Code, but the zero-setup
    cost is hard to beat for week 1.
  - **Local 16-24GB GPU** (RTX 4070+ / 3090 / 4090) — best if you
    already own one. Nerfstudio + gsplat are very GPU-VRAM hungry.
    Running CUDA on your own box is the moral equivalent of running
    Postgres locally vs using Supabase: more setup pain, but every
    iteration is free and instant.
- Two screens if you can. You will routinely have a terminal, a
  3D viewer (rviz2 or rerun), and a Jupyter notebook open at the
  same time — the same multi-pane life as running `vite`, Storybook
  and a browser inspector side by side.

## Week 1: Classical foundations — the camera math

Goal: stop being afraid of camera matrices.

A camera matrix is just a 3x3 array of numbers that maps a 3D point
in the world to a pixel coordinate. Calibrating a camera is like
running migrations on your dev DB — boring, you'll do it dozens of
times, and skipping it once will cost you a day chasing a bug that
turns out to be a 5-pixel offset.

- Skim **Stanford CS231A** lecture notes (free PDFs). Read the first
  4 lectures: camera model, calibration, single-view metrology,
  two-view geometry. Treat it like reading the spec for a new HTTP
  protocol — you do not need to memorize, you need to know what
  exists so you can grep for it later.
- **Calibrate your laptop webcam** with OpenCV's
  `cv2.calibrateCamera()` and a printed checkerboard. Get an
  intrinsic matrix `K` and reproject a 3D point onto the image.
  When the reprojection lands where you expect, you "get it." The
  minimal flow looks roughly like this:

  ```python
  import cv2, numpy as np
  objp = np.zeros((6*9, 3), np.float32)
  objp[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)
  obj_points, img_points = [], []  # filled by looping over images
  # for each frame: cv2.findChessboardCorners + append to lists
  ret, K, dist, rvecs, tvecs = cv2.calibrateCamera(
      obj_points, img_points, gray.shape[::-1], None, None)
  ```

- Re-implement: pinhole projection, RANSAC, PnP. Don't write your
  own RANSAC for production — but writing one once teaches you why
  it works. RANSAC is "try a random subset, fit, count inliers,
  repeat" — the same shape as the retry-with-jitter logic you would
  put around a flaky external API.

**Common ways this week goes wrong**

- Your checkerboard calibration gets nonsense `K` values (focal
  length of 50 pixels, or 50,000). Fix: check you printed the
  checkerboard at the right physical size — most printers default
  to "fit to page" and silently scale your PDF. Measure a square
  with a ruler and pass the real edge length in meters.
- `cv2.findChessboardCorners` returns `False` on most frames. Fix:
  bad lighting or the board is too small in the frame. Move
  closer, add a lamp, and make sure the whole board is visible
  with some margin.
- Reprojection error is 20+ pixels. Fix: you mixed up rows and
  columns of the checkerboard, or you used a non-planar surface
  (curling paper). Tape it to a clipboard.

**End-of-week deliverable you can post**: a single image of your
desk with a 3D cube reprojected on top of the checkerboard, plus
the printed `K` and reprojection error in the caption. Tweet-sized
proof you understand projective geometry.

## Week 2: Modern detection and segmentation

Goal: load a vision foundation model and run it.

Using a vision foundation model is the moral equivalent of calling
the OpenAI API from a Next.js route handler — somebody else trained
the giant thing, you are wiring up the I/O. The whole week is about
getting fluent at "load the weights, push a tensor in, get a tensor
out, draw the result."

- Read the **CS231n** notes on CNNs and on Transformers (the deep
  CV companion to CS231A). You do not need to derive backprop; you
  need to recognize the shapes of the building blocks when you read
  a model card.
- Run **SAM 2** on your own photos via Hugging Face. Click a point
  on a mug, get a mask. Wire it into a small Python script. The
  Hugging Face one-liner is roughly:

  ```python
  from transformers import pipeline
  seg = pipeline("mask-generation", model="facebook/sam2-hiera-large")
  masks = seg("mug.jpg")  # exact model id may differ — check the hub
  ```

  (Confirm the exact model ID on the Hugging Face hub; SAM 2 is
  sometimes served via `sam2` package directly rather than the
  pipeline API.)
- Run **DINOv2** to extract per-image embeddings; cluster the
  embeddings of 100 photos with `sklearn.cluster.KMeans` and see if
  semantically similar images end up in the same cluster. This is
  the visual analogue of running OpenAI text embeddings over your
  blog posts and seeing related-posts clustering fall out for free.
- Train a tiny detector on a custom dataset with **YOLO v11**
  (Ultralytics). Collect 50 photos of one object, label with
  Roboflow or CVAT, fine-tune in 10 minutes on a free GPU.
  Fine-tuning YOLO on 50 custom photos is like deploying a
  Cloudflare Worker that handles your specific routing — small,
  narrow, ships fast, and feels disproportionately satisfying.

**Common ways this week goes wrong**

- SAM 2 install fails with a `torch` version mismatch. Fix: install
  `torch` first, matched to your CUDA version, then install SAM 2.
  Do not let pip resolve them together. This is the Python ecosystem
  equivalent of a peer-dependency hell — pin manually.
- YOLO trains but mAP is 0.05. Fix: your labels are in the wrong
  format (YOLO expects normalized xywh in a per-image `.txt`).
  Re-export from Roboflow with the explicit "YOLOv8 PyTorch" preset.
- DINOv2 embeddings cluster everything into one giant blob. Fix:
  you forgot to L2-normalize before KMeans, or you picked too few
  clusters (start with k=10 for 100 images).

**End-of-week deliverable you can post**: a 10-second screen
recording of you clicking points on a photo and SAM 2 masks
appearing in real time, or a confusion-matrix-style grid of your
custom YOLO detector's results on 8 held-out test images.

## Week 3: Monocular depth and 3D from pixels

Goal: build a "phone -> 3D" toy.

This is the week the tooling actually starts feeling magical. You
put in a folder of phone photos and you get back a navigable 3D
scene. The closest web-dev analogue is the first time you ran a
SSG and watched it spit out a whole site from a folder of markdown.

- Run **Depth-Anything v2** on a single photo. Plot the depth map.
  Note the colors are relative depth, not metric — a foundation
  model cannot tell whether your chair is 1 meter or 2 meters away
  without a calibrated reference. Metric depth needs `Metric3D`,
  `UniDepth`, or a real depth camera.
- Take 30-50 photos of your desk from different angles. Run
  **COLMAP** (or **glomap** — modern, faster) to recover camera
  poses and a sparse 3D point cloud. Photo capture tip: walk in a
  half-circle around the object, vary height, do not just pivot in
  place. COLMAP needs parallax the same way stereo vision does.
- Feed the same photos into **Nerfstudio** and train a small NeRF
  (5-10 minutes on a 4070 / A100). Render a fly-through video. The
  end-to-end command sequence is roughly:

  ```bash
  ns-process-data images --data ./photos --output-dir ./processed
  ns-train splatfacto --data ./processed
  # then: ns-viewer --load-config outputs/.../config.yml
  ```

- Train a **3D Gaussian Splat** of the same scene with
  `nerfstudio`'s `splatfacto` or **gsplat** directly. Compare
  quality and rendering speed — splats win. A splat is essentially
  the WebGL particle-system version of a NeRF: same input, far
  faster render, easier to ship to a browser viewer.

**Common ways this week goes wrong**

- Nerfstudio crashes with CUDA OOM. Fix: drop the batch size,
  downsample images to 1080p before training, or rent an A100 for
  an hour. Splatfacto in particular wants 16+ GB VRAM for a
  reasonable scene.
- COLMAP finishes but registers only 8 of your 50 images. Fix: your
  photos are too similar (you stood in one spot) or too different
  (lighting changed between morning and afternoon). Re-shoot in
  one continuous pass.
- The splat looks great from training views and like garbage from
  novel angles. Fix: you did not cover the scene from enough
  viewpoints. Splats and NeRFs interpolate, they do not extrapolate.

**End-of-week deliverable you can post**: a 5-second fly-through
video of your desk splat, embedded as an MP4 in a tweet or as an
interactive viewer link (Polycam, SuperSplat, or a self-hosted
gsplat viewer).

## Week 4: 6-DoF pose for a real object

Goal: localize a known object in 6D from a webcam image.

6-DoF means six degrees of freedom: three for translation (x, y, z)
and three for rotation (roll, pitch, yaw). What FoundationPose
actually outputs per frame is a **4x4 homogeneous transform matrix**
— the top-left 3x3 is a rotation, the top-right 3x1 is a translation
in meters, and the bottom row is `[0, 0, 0, 1]` so you can compose
poses by matrix multiplication. If you have ever done CSS `transform:
matrix3d(...)` you have already seen the data structure; this is the
same idea applied to a physical object.

- Pick an object you have on your desk that has a CAD model
  available online (LEGO, a 3D-printed thing, an off-the-shelf
  mug). Otherwise scan it with **Polycam** on your phone and export
  to `.obj` or `.glb`.
- Run **FoundationPose** on a video of you moving it around. You
  should get a 6-DoF pose per frame.
- Visualize the pose stream in **Open3D** (draw the CAD mesh with
  the transform applied each frame) or, much nicer, in
  **rerun.io** — log the mesh once, log a `rr.Transform3D` per
  frame, scrub the timeline like you would scrub a video editor.
  rerun is to robotics what the React DevTools timeline is to a
  Next.js app: once you have it, you cannot work without it.
- This is the exact thing a bin-picking robot does. You've now
  implemented the core of an industrial picker.

**Common ways this week goes wrong**

- FoundationPose returns a pose but the rendered mesh is rotated
  90 degrees from the real object. Fix: your CAD model is in a
  different coordinate convention (Y-up vs Z-up, meters vs
  millimeters). Bake a transform into the mesh or apply one before
  rendering.
- Pose jitters wildly between frames. Fix: lighting is too dim or
  the object is partly occluded. Add a desk lamp and keep the whole
  object in view; pose estimators degrade gracefully on paper and
  ungracefully in practice.
- You cannot get a depth stream because your laptop only has an RGB
  webcam. Fix: use FoundationPose's RGB-only mode if available, or
  borrow a friend's RealSense for a weekend.

**End-of-week deliverable you can post**: a side-by-side video —
left pane is your webcam feed, right pane is the CAD model snapping
to the real object's pose in rerun. Caption: "the core of every
bin-picker, in 200 lines of Python."

## Week 5: SLAM — the moving-camera problem

Goal: make a map from a video.

SLAM (Simultaneous Localization and Mapping) is the problem of
building a map while figuring out where you are in it. The web-dev
analogue is a single-page app that has to render the route tree
while also discovering the routes from a streaming API — both at
once, neither correct without the other. It is harder than it
sounds, which is why people are still publishing SLAM papers
thirty years in.

- Walk through your apartment with your phone, recording 1080p
  video at 30 fps. Or use a EuRoC dataset (free, has IMU + cameras).
  Slow walking, no fast pans, plenty of texture in view. Hallways
  with blank white walls are the SLAM equivalent of a CORS error:
  you will hit them and you will hate them.
- Run **ORB-SLAM3** in monocular or RGB-D mode on the recording.
  Visualize the camera trajectory and the sparse map.
- Read the **DROID-SLAM** paper; run their pretrained model on the
  same video. Compare against ORB-SLAM3.

A "good" trajectory, plotted top-down, looks like a smooth loop
that closes back on itself when you return to the start — drift on
the order of centimeters over a 50-meter walk. A "drifting"
trajectory looks like a flat spiral: the loop never closes, the
end point is meters away from the start, and any sharp turn makes
the path snap to a wrong angle. The standard tool for plotting and
comparing trajectories is `evo` — `pip install evo --upgrade` and
then `evo_traj tum trajectory.txt --plot` gives you trajectory
plots, and `evo_ape` / `evo_rpe` compute absolute and relative
pose errors against ground truth. Treat APE under 1% of trajectory
length as a healthy result for monocular SLAM on EuRoC-class data.

**Common ways this week goes wrong**

- ORB-SLAM3 builds for 45 minutes and fails at the linker. Fix: the
  Pangolin / OpenCV / Eigen version dance is real. Use the
  community Docker image — `docker pull jahaniam/orbslam3` (or the
  current maintained equivalent) — and skip the build.
- Monocular SLAM gives you a map with no metric scale (everything
  is in "units"). This is correct, not a bug — monocular cannot
  recover scale without an IMU or known object. Switch to RGB-D
  mode or use stereo.
- Trajectory looks fine in the viewer but `evo_ape` reports huge
  error. Fix: your trajectory and ground truth are in different
  coordinate frames or different time offsets. Use `evo_traj
  --align` and `--correct_scale`.

**End-of-week deliverable you can post**: a top-down trajectory
plot of your apartment walk with the loop closure visible, plus a
quick `evo_ape` number against the ground truth (if you used EuRoC)
or against a second pass through the same space.

## Week 6: ROS2 + a real perception node

Goal: ship perception inside an actual robotics framework.

ROS2 is the message bus, build system, and tooling standard for
robotics. A ROS2 topic subscription is roughly subscribing to an
EventEmitter or a Redis pub/sub channel — you declare a topic name
and a message type, you get a callback every time someone publishes.
A ROS2 service is an RPC call. A ROS2 action is a long-running RPC
with progress updates, the same shape as a Server-Sent Events
endpoint.

- Install **ROS2 Humble** (Ubuntu 22.04) or **Jazzy** (Ubuntu 24.04
  — Jazzy is the current LTS as of mid-2025). If your distro fights
  you, use the official Docker image; it is genuinely easier than
  the apt install for a first taste.
- Build a small **rclpy** node that subscribes to a
  `/camera/image_raw` topic, runs SAM 2 segmentation, and publishes
  a mask topic. Visualize in `rviz2`. A minimal subscriber looks
  like:

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

  Run it with `ros2 run your_pkg frame_size_printer` after building
  with `colcon build`. The `cv_bridge` package converts the `Image`
  message into an OpenCV ndarray when you are ready to actually do
  perception on the frame.
- If you have a depth camera (RealSense / iPhone via ROS bridge),
  pipe its depth in too and publish a colored point cloud. The
  `realsense2_camera` ROS2 package gives you `/camera/depth/...`
  topics out of the box; subscribe to both color and depth with a
  `message_filters.ApproximateTimeSynchronizer` so frames line up.

**Common ways this week goes wrong**

- `colcon build` succeeds but `ros2 run` says "package not found."
  Fix: you forgot to `source install/setup.bash` in the new shell.
  Add it to your `.bashrc` once you commit to a workspace.
- Two nodes cannot see each other's topics. Fix: `ROS_DOMAIN_ID`
  is different in the two terminals, or you are on different
  networks. Set the same domain ID in both shells.
- Setting up CUDA on Ubuntu in time to run SAM 2 inside a ROS2 node
  feels like getting Postgres talking to your Node app on a fresh
  laptop, but the error messages are more demoralizing. Fix: run
  the perception model in a separate Docker container with CUDA
  baked in, expose it as a tiny gRPC or HTTP service, and have the
  rclpy node call it. Decoupling the GPU runtime from the ROS
  runtime saves a week of pain.

**End-of-week deliverable you can post**: a GitHub gist of your
rclpy node plus a 15-second screen recording of rviz2 showing the
camera feed on the left and a live segmentation mask overlay on the
right.

## Week 7-8: Build one substantial portfolio project

Pick something you'd put on your resume. Two weeks is short — scope
ruthlessly, ship one narrow thing well, and treat the README and
the demo video as first-class deliverables. A perception project
with no demo video does not exist in the job market.

Some ideas, expanded:

- **Phone-to-Gaussian-splat web app.** User uploads a phone video,
  service returns a `.splat` file plus an interactive viewer URL.
  Wrap Nerfstudio in a FastAPI job queue (Celery + Redis is fine).
  Target customer: realtors, e-commerce sellers, indie game devs
  who want to scan props. Pricing model: $5-$20 per scan or
  $50/month for a small bundle — comparable to Polycam Pro and
  Luma. The demo video should show a phone walking around a real
  object, a "processing..." spinner, then a browser viewer with
  orbit controls and the scan loading in under 10 seconds. On
  GitHub: the FastAPI service, a Dockerfile, a `docker compose`
  one-liner to bring it up locally, and a `examples/` folder with
  one finished `.splat` so reviewers do not have to run a GPU job
  to see what the output looks like.

- **6-DoF pose REST endpoint.** Customer uploads a CAD model, you
  return a Docker container exposing a `/pose` endpoint that takes
  an RGB-D frame and returns a 4x4 transform plus a confidence
  score. Wrap FoundationPose. Target customer: small-shop robotics
  integrators doing pick-and-place who do not want to license
  Halcon or MVTec. Pricing: $500-$2k per container per integration,
  or a $200/month SaaS tier with an API key. The demo video should
  show a 10-second `curl` upload, the response JSON, and a
  rerun.io playback of the pose snapping onto the object frame by
  frame. On GitHub: the wrapper code, a `pose-eval/` folder with
  BOP-style metrics on a few public objects, and a `make demo`
  target that brings up the whole stack on one machine.

- **Anomaly detection demo.** Take 50 "good" and 50 "bad" photos of
  any product (PCBs, fruit, fabric, 3D prints, coffee beans). Train
  a PatchCore / anomalib model. Ship a Streamlit dashboard where
  you upload an image and get a heatmap of defective regions plus
  a pass/fail verdict. Target customer: small manufacturers who
  cannot justify a Cognex license but want some QA automation.
  Pricing: $1-2k for a custom-trained model + dashboard, or a
  $99/month hosted version with a per-image API. The demo video
  should show the dashboard in action on three "bad" examples,
  with the heatmap correctly highlighting the defect. On GitHub:
  the training notebook, the Streamlit app, and a small dataset
  (or links to a public one like MVTec AD) so the project is
  reproducible.

- **SLAM benchmark dashboard.** Drop in a ROS bag, run ORB-SLAM3 +
  VINS-Fusion + a learned method (DROID-SLAM or NICER-SLAM), output
  a side-by-side video and a trajectory-error PDF generated by
  `evo`. Target customer: research engineers and grad students who
  need to compare baselines for a paper and do not want to wire
  three SLAM systems by hand. Pricing: open-source it for free,
  use it as an obvious hiring signal. The demo video should show
  three trajectories overlaid on the EuRoC ground truth with the
  APE/RPE numbers in a corner. On GitHub: Dockerfiles for each
  SLAM system, a single `python bench.py --bag my.bag` entrypoint,
  and a sample report PDF committed to the repo.

**End-of-week deliverable you can post (Week 8)**: a 60-second
demo video plus a polished README, both linked from a single tweet
or LinkedIn post. The README should have a hero GIF in the first
screen, a one-line "what this is", a one-line "who this is for",
the `docker compose up` command, and only then the technical
detail. Treat it like a product launch, not a homework submission.

**Common ways Week 7-8 goes wrong**

- You scope a "platform" and finish nothing. Fix: pick the
  smallest possible vertical slice and ship that. A working
  Streamlit dashboard with one model beats a half-built
  microservices platform every time.
- You skip the demo video because "the code is on GitHub." Fix:
  90% of viewers will watch the video and never clone the repo.
  Spend an afternoon on a clean recording with captions.
- You forget to write a README for a non-roboticist reader. Fix:
  show it to a web-dev friend; if they cannot tell what the
  project does in 30 seconds, rewrite the top of the README.

## Tooling setup

The one-time dev-environment recipe — the `npx create-next-app`
equivalent for robotics perception. Set this up once, reuse it for
every project from now on.

- **OS**: Ubuntu 22.04 LTS (matches ROS2 Humble) or Ubuntu 24.04
  LTS (matches ROS2 Jazzy). Dual-boot or a dedicated machine, not
  a VM — GPU passthrough on a VM is a multi-day yak shave.
  macOS works for Weeks 1-3 if you stick to CPU or MPS, but ROS2
  and CUDA-heavy tools are second-class there. Windows + WSL2
  works for some things and breaks for others; avoid as a primary
  setup.
- **NVIDIA driver + CUDA**: install the proprietary NVIDIA driver
  via `ubuntu-drivers autoinstall`, reboot, verify with
  `nvidia-smi`. Install CUDA via the runtime that ships with your
  PyTorch wheel — you almost never need a system-wide CUDA toolkit
  for pure-Python work. If you do need `nvcc` (for building
  custom CUDA kernels in gsplat etc.), install the matching
  toolkit from NVIDIA's apt repo, not the Ubuntu archive.
- **Python envs**: `uv` is the new default — fast, deterministic,
  ships its own Python. `conda` (or `mamba`) is still the right
  pick when a package only has conda-forge builds (a lot of older
  geometry / 3D code). Pin a Python version per project (3.10 or
  3.11 are the safest in 2025/2026; 3.12+ still breaks some
  binary wheels).
- **ROS2**: two paths. (a) Apt install on a matching Ubuntu — fast,
  integrates with your shell, but couples your perception code to
  your OS. (b) The official `osrf/ros:jazzy-desktop` Docker image
  — more boilerplate, fully reproducible. For learning use apt;
  for production or shared dev use Docker.
- **VS Code**: install the extensions `ROS` (Microsoft), `Pylance`,
  `Ruff` (replaces black + isort + flake8 in one tool), `Even
  Better TOML`, `Docker`, `Dev Containers`, and `Jupyter`. The
  Cursor or Zed equivalents work fine too; the extension list is
  what matters.
- **Visualization**: install `rerun-sdk` (`pip install rerun-sdk`),
  Open3D (`pip install open3d`), and Foxglove Studio (the web-app
  version of rviz2, very useful when you cannot ssh-forward a GUI).
- **Project template**: keep a personal `cookiecutter-perception`
  or `uv init` template with a `pyproject.toml`, a `Dockerfile`,
  a `Makefile` with `make fmt`, `make lint`, `make test`, and a
  `data/` and `outputs/` gitignored. The web-dev habit of
  scaffolding once and reusing pays off here too.

## Stretch goals

Things to try after Week 8, in roughly increasing ambition:

- **Contribute a small fix to an OSS perception project.** Pick
  Nerfstudio, gsplat, ORB-SLAM3, anomalib, or a Hugging Face
  vision pipeline. Find an issue labeled `good first issue`, send
  a PR. A merged PR to a 5k-star perception repo is worth more on
  a resume than a from-scratch toy.
- **Reproduce a recent CVPR paper from scratch.** Pick something
  with code already released (do not pick a no-code paper for your
  first attempt). Re-run their training, match a number from their
  table within 10%, write up what went wrong. This is the
  perception equivalent of cloning a popular library to understand
  how it works.
- **Deploy a perception model to an edge device.** A Raspberry Pi
  5 with a Hailo-8L hat, a Jetson Orin Nano (8GB), or a Coral USB
  accelerator. Take your Week 2 YOLO model, convert it to ONNX,
  then to TensorRT or Hailo's runtime, and benchmark FPS at
  different input resolutions. Write up the latency-vs-accuracy
  curve. This is one of the most common interview questions for
  embedded perception roles.
- **Stand up a multi-camera rig.** Two cheap webcams plus a
  calibration board, computed extrinsics, then a stereo depth
  pipeline. Bridges the gap between "I ran a model" and "I
  understand sensor systems."

## What to NOT do in the first 8 weeks

These are real traps that eat months and produce nothing shippable.

- **Do not write your own SLAM from scratch.** ORB-SLAM3 is
  ~30k lines of C++ that took a decade. You will reinvent a worse
  version in three months. Use it, do not rewrite it.
- **Do not try to train a foundation model from scratch.** SAM,
  DINOv2 and Depth-Anything cost six- to seven-figure compute
  budgets. Fine-tune, do not pretrain.
- **Do not buy a Velodyne or Ouster LiDAR yet.** $5k+ for
  hardware you will not have the software stack to exploit in two
  months. iPhone LiDAR or a RealSense covers Weeks 1-8.
- **Do not try to set up a full self-driving stack.** Autoware /
  Apollo are 10+ GB of dependencies and need real cars or
  high-fidelity sim to be interesting. Pick one perception slice
  (lane detection, object detection on KITTI) instead.
- **Do not chase every new arXiv paper.** Twitter will surface
  three "state of the art" perception models a week. Pick one
  per topic, finish the week's project, move on. Paper-of-the-week
  syndrome is the new framework-of-the-week.
- **Do not refactor your code before it works.** The first version
  of your pose pipeline will be a 200-line script. Get it working
  end-to-end before you split it into modules. Same rule as
  prototyping a React feature.

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

Prices reflect Q4 2025 / early 2026 street prices in USD; check
before you buy, supply and tariffs move these around.

- **Intel RealSense D435 / D455** (~$300-400) — the workhorse RGB-D
  stereo camera. Good for: getting started with depth, ROS2
  tutorials, indoor SLAM. Note Intel announced wind-down then
  partial reversal of the RealSense line; check current supply.
- **Orbbec Femto Bolt** (~$300) — ToF depth camera, Microsoft
  Azure Kinect successor. Good for: indoor mapping, higher-quality
  depth than stereo at close range.
- **iPhone with LiDAR** (Pro models 12+, you may already own one,
  used iPhone 12 Pro around $250-350) — combined with apps like
  Polycam, Scaniverse, or Record3D. Good for: object scans, room
  scans, the fastest "real depth camera" available with zero setup.
- **OAK-D series** (Luxonis, ~$200-400) — stereo depth plus
  on-device Myriad-X neural inference. Good for: hobby robots,
  battery-powered demos, anywhere you do not want to ship a host
  PC alongside the camera.
- **Livox Mid-360 / Mid-70** ($1.5-3k) — entry-tier solid-state
  LiDAR. Good for: outdoor SLAM at scale, drone / AMR
  experimentation. Overkill for Weeks 1-8; pick this up only after
  you have a clear project that needs it.
- **NVIDIA Jetson Orin Nano Super 8GB dev kit** (~$249) — Arm SoC
  with a small CUDA GPU. Good for: deploying a perception model at
  the edge, on-robot inference, the cheapest way to learn
  Jetson-stack tooling. (Confirm current pricing — NVIDIA cut the
  Orin Nano Super price in late 2024.)
- **Raspberry Pi 5 (8GB)** (~$80) — general-purpose SBC, no GPU.
  Good for: pairing with a Hailo-8L AI hat (~$70) or Coral USB
  accelerator (~$60) for cheap edge inference; not for training
  anything.
- **Used RTX 3090 24GB** (~$700-900) — second-hand desktop GPU.
  Good for: local Nerfstudio / gsplat training, fine-tuning, and
  the single best dollar-per-VRAM option for hobby perception work.
- **Generic 8" checkerboard print on foamcore** (~$10) — laminate
  a 7x10 or 9x12 checkerboard, glue to a flat backer. Good for:
  calibrating literally every camera you will ever own. Cheapest
  high-leverage purchase on this list.

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
