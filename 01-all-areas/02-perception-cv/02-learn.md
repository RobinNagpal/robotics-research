# Important Things to Learn

Coming from web dev, the gap is **math** (linear algebra and multi-view
geometry) and **a small amount of robotics vocabulary**. The Python
tooling (PyTorch, Hugging Face, Docker) is the same as for LLM work;
perception adds geometry on top.

The deeper reframe: in web dev your ground truth is what the server
returned. In perception your ground truth is the physical world, which
is noisy, badly lit, and lies to you. The hardest bugs are
coordinate-frame, timestamp, and calibration bugs. The code is often
simpler than a React app; the epistemics are harder. When stuck, ask:
what frame is this number in? what timestamp? is my calibration still
valid? See `00-basics.md` for the vocabulary.

## Layer 0: Python and PyTorch

One week if you're rusty:

- Python type hints, dataclasses, NumPy, pathlib. Learn NumPy
  broadcasting rules or your shapes will silently misalign.
- PyTorch tensors and autograd. Karpathy's "neural networks
  zero-to-hero" series is the best free intro.
- **OpenCV** in Python. Loading images, drawing boxes, basic
  thresholding. OpenCV stores colors as **BGR**, not RGB; forget this
  once and you'll spend an hour debugging a "blue" detector that
  finds red things.
- Device discipline. Every `.to("cuda")` / `.to("cpu")` is a sync
  point. Mixing devices in one expression throws.

**Mini-project.** Write a 40-line script that loads a JPEG with
OpenCV, converts BGR to RGB, normalizes to `[1, 3, H, W]`, runs a
pretrained ResNet-18 from `torchvision`, and prints top-5 ImageNet
labels. Gets you fluent with the tensor / device / dtype shuffle that
every perception script begins with.

## Layer 1: Math foundations

Six concepts to internalize. Once they're muscle memory, the rest is
composition.

- **Matrices as transforms.** A 3x3 matrix rotates / scales a 3D
  point. A 4x4 matrix also translates it. This is how all 3D
  computation is done.
  - *Equation walkthrough.* For point `p = [x, y, z]`, `R @ p` gives
    a rotated column. To also translate, append a 1 to make
    `[x, y, z, 1]` and use a 4x4 whose top-right column is `t`. The
    trailing 1 lets one matmul handle rotation and translation.
- **SE(3) and SO(3).** SO(3) is the group of rotations (3x3 matrices
  with `R.T @ R == I` and `det(R) == +1`). SE(3) is rigid-body
  transforms: a 4x4 gluing an SO(3) to a translation,
  `T = [[R, t], [0, 0, 0, 1]]`. Composition is matmul. Inverse is
  `[[R.T, -R.T @ t], [0, 0, 0, 1]]` — exploit the structure, don't
  call generic 4x4 inverse.
- **Quaternions.** A 4-number rotation that avoids gimbal lock.
  *Quaternions are like JWTs: compact serialization that humans
  can't read directly but that survives composition cleanly through
  a trusted library.* Use Sophus or
  `scipy.spatial.transform.Rotation`.
  - *Equation walkthrough.* Unit quaternion `q = (w, x, y, z)` with
    `w^2 + x^2 + y^2 + z^2 == 1`. `w` is cosine of half-angle,
    `(x, y, z)` is sine of half-angle times the axis. Composition
    is quaternion multiplication: four multiplies vs. 27 for two
    3x3 matmuls. Libraries disagree on `(w, x, y, z)` vs.
    `(x, y, z, w)` order; check the docs every time.
- **Pinhole camera model.** `pixel = K * [R | t] * world_point`.
  `K` is the intrinsic matrix (focal length, principal point in
  pixels); `[R | t]` is the extrinsic pose. Understand this and 80%
  of multi-view geometry unlocks.
  - *Equation walkthrough.* Take world point `X`. `[R | t]` brings
    it to camera frame `X_cam`. Divide by `Z_cam` for the
    perspective divide (far things shrink). Multiply by `K`, get
    pixel `(u, v)`. One matmul, one divide.
- **Epipolar geometry, triangulation, PnP.** How to recover 3D from
  2D pixels across views. PnP ("Perspective-n-Point") solves camera
  pose from known 3D points and their observed pixels.
  - *Equation walkthrough.* For N known 3D points `X_i` with pixel
    observations `u_i`, predicted pixel is
    `pi(K @ (R @ X_i + t))`. PnP minimizes
    `sum_i || u_i - predicted ||^2` over `(R, t)`. Four points (one
    off-plane) is the minimum; in practice feed 50+ and RANSAC the
    outliers. Solvers: `cv2.solvePnP`, EPnP, SQPnP.
- **Bundle adjustment.** Jointly optimize all camera poses and 3D
  points to minimize reprojection error. The engine inside every
  SLAM system; you call it as a library (Ceres, g2o, GTSAM, pypose),
  you don't implement it.
  - *Equation walkthrough.* Same loss as PnP, but `X_i` are also
    unknowns and there are many cameras:
    `sum_{c, i visible in c} || u_{c,i} - pi(K @ (R_c @ X_i + t_c)) ||^2`.
    The Jacobian is sparse (each residual touches one camera and
    one point); specialized solvers exploit that sparsity. That's
    the entire reason BA scales to thousands of frames.

One course: **Stanford CS231A**. See `06-courses.md` for the longer
list.

**Mini-project.** Draw a virtual 1m cube at the origin and a virtual
camera 3m back. Hand-build `K`, `R`, `t` in NumPy, project the 8
corners to pixels, draw the wireframe in matplotlib. Translate the
cube 0.5m and re-project. If it moves correctly, you've internalized
the pinhole model.

## Layer 2: Classical computer vision

Classical CV is the substrate everything runs on. Your fanciest
transformer pipeline still uses classical geometry to triangulate,
RANSAC, and calibrate.

- **Feature detection / matching.** SIFT (1999), ORB (fast binary),
  SuperPoint (learned, 2018), LightGlue (learned matcher, 2023).
  LightGlue is the current default for SLAM-grade matching.

  | Detector / matcher | Year | Speed | Accuracy | License | Notes |
  |---|---|---|---|---|---|
  | SIFT | 1999 | slow | high | free since 2020 | rotation- and scale-invariant; gold-standard baseline |
  | ORB | 2011 | very fast | medium | BSD (OpenCV) | binary descriptor; default in ORB-SLAM family |
  | SuperPoint | 2018 | fast on GPU | high | research / non-commercial in original | learned keypoints; widely re-implemented |
  | LightGlue | 2023 | fast on GPU | very high | Apache-2.0 | matcher, not detector; pair with SuperPoint / DISK |

  Pure CPU / embedded: ORB. GPU and best matches: SuperPoint +
  LightGlue. Need a permissive license: double-check the model card.
- **Stereo and structured light.** How depth cameras work. Two
  cameras triangulate disparities; structured light adds an IR
  projector.

  | Depth sensor | Range | Accuracy | Lighting | Examples |
  |---|---|---|---|---|
  | Passive stereo | 0.3 - 10 m | medium | needs texture, fails on blank walls | RealSense D4xx |
  | Active stereo | 0.3 - 5 m | medium-high indoor | bad in direct sunlight | RealSense D435i, Orbbec |
  | Structured light | 0.5 - 3 m | high indoor | fails outdoor | original Kinect, iPhone TrueDepth |
  | Time of Flight | 0.3 - 5 m | high | multi-path on shiny / corners | Azure Kinect, PMD |
  | LiDAR | 1 - 200 m | very high | dark fine, rain / fog struggle | Velodyne, Ouster, Livox, Hesai |

- **Optical flow.** Per-pixel motion between frames. Lucas-Kanade
  (classical, sparse), RAFT (learned, dense).
- **Camera calibration.** Zhang's method (checkerboard) for single
  camera; Kalibr for IMU + multi-camera rigs. You will calibrate
  cameras many times. Bad calibration is the actual cause of more
  bugs than any other single thing.

**Mini-project.** Calibrate your laptop webcam with OpenCV. Print a
9x6 checkerboard, capture 20 frames at varied angles, run
`cv2.calibrateCamera`, save `K` and distortion to JSON. Take a new
photo, pick a pixel on a known object, back-project to a 3D ray, and
reproject. Keep the JSON for the SLAM mini-project later.

## Layer 3: Modern deep computer vision

- **CNNs** (ResNet, EfficientNet). Still ship in production; one-day
  refresher.
- **Vision Transformers** (ViT, Swin, DINO). Architecturally
  identical to text transformers; split the image into 16x16 patches
  and treat each as a token.
- **Detection.** DETR family (transformer), YOLO v8 / v11 (CNN,
  fast). YOLO ships in everything; DETR variants win papers.
- **Segmentation.** SAM 2 for promptable, Mask2Former for trained.
- **Monocular depth.** Depth-Anything v2, Marigold (diffusion-based),
  ZoeDepth. Production quality from a single image.
- **Vision foundation models.** DINOv2 (self-supervised features),
  CLIP / SigLIP (vision-language), Florence-2 (multi-task). Load from
  Hugging Face.

**When not to use a foundation model.** A 300M-1B parameter model on
a Jetson Orin gets 2-5 Hz at fp16 and burns 20+ watts. A YOLOv8n
fine-tuned on your 5 classes runs at 60+ Hz, fits in 50 MB, and frees
GPU memory for the planner, tracker, and downstream policy.
Production latency budgets are typically under 33 ms end-to-end,
leaving ~10 ms for the detector. If your class set is fixed, your
camera is fixed, and you can label 2k images, the small purpose-built
model wins on latency, memory, cost, and predictability. Reach for
the foundation model when the class set is open-ended, you have no
labels, or prompt-driven flexibility is worth the watts. See
`01-examples.md` for which tier shows up where.

**Mini-project.** Run YOLOv8 on a phone video with Ultralytics, draw
boxes. Then swap in SAM 2 with point prompts on one frame and
propagate masks across the video. Compare runtime side by side.

## Layer 4: 3D and neural rendering

- **Representations.** Point clouds, meshes, voxels, signed distance
  fields (SDFs), NeRFs, Gaussian splats. Gaussian splats are the
  current default for photoreal renders.
- **NeRF.** A small MLP mapping `(x, y, z, view_dir) -> (RGB,
  density)`. Query like a function. Slow.
- **3D Gaussian Splatting.** Scene = millions of fuzzy 3D blobs.
  Real-time rendering. Use Nerfstudio + gsplat.
- **Differentiable rendering.** `nvdiffrast`, gsplat, PyTorch3D.
  Normal renderers take a scene and produce pixels. Differentiable
  renderers also report, for every pixel, how it would change if you
  nudged any input parameter. That gradient lets you solve the
  inverse problem: given this photo, what scene produced it? Optimize
  with Adam, and geometry / texture / camera pose fall out. This is
  why NeRF and Gaussian splatting work at all.
- **6-DoF pose estimation.** FoundationPose, MegaPose, GigaPose
  (model-based modern; give it a CAD model, no per-object training).
  Learned: FFB6D, PoseCNN. "6-DoF" = three numbers for position, three
  for orientation — the full SE(3) pose of an object relative to the
  camera. Output feeds the grasp planner.

**Mini-project.** Capture 60 phone photos of an object from all
sides, drop them into Nerfstudio, train a `splatfacto` model for 20
minutes on a single GPU, orbit the result in the web viewer.

## Layer 5: SLAM and visual localization

- **Visual odometry vs. visual-inertial vs. SLAM.** VO answers
  "where did the camera move?", VIO fuses an IMU for jitter
  reduction, SLAM adds a persistent map and loop closure ("have I
  been here before?").
- **Filter-based** (EKF, MSCKF) vs. **optimization-based** (ORB-SLAM3,
  VINS-Fusion). Modern systems are optimization-based.
- **Learned SLAM.** DROID-SLAM (NeurIPS 2021), DPVO. Higher accuracy,
  more compute.
- **Visual relocalization.** Given a new image, find where you are on
  an existing map. hloc + SuperPoint + LightGlue is the modern
  pipeline.

| System | Language | Sensors | License | Type | Use case |
|---|---|---|---|---|---|
| ORB-SLAM3 | C++ | mono / stereo / RGB-D / VI | GPLv3 | classical | research baseline; reference for "good SLAM" |
| VINS-Fusion | C++ | mono / stereo + IMU | GPLv3 | classical | drones; tight VIO from HKUST |
| OpenVSLAM / Stella-VSLAM | C++ | mono / stereo / RGB-D | 2-clause BSD (Stella) | classical | when license matters; ORB-SLAM-style without GPL |
| DROID-SLAM | Python + CUDA | mono / stereo / RGB-D | research | learned (recurrent flow) | offline reconstruction; GPU required |
| NeRF-SLAM / Glorie-SLAM | Python | mono / RGB-D | research | hybrid | dense reconstruction with neural map |
| Spectacular AI | closed SDK | vendor-specific | commercial | hybrid | shipping product without maintaining SLAM |

The SLAM landscape moves fast and licenses change; check the repo
before committing, especially for commercial use.

**Mini-project.** Download EuRoC MAV (a standard drone VI benchmark),
run ORB-SLAM3 in stereo-inertial on one sequence, compare the
trajectory to ground truth with `evo_traj`. You'll get an Absolute
Trajectory Error in meters — your first quantitative SLAM result.

## Layer 6: Tooling and infra

- **Languages.** Python for research; **C++** for real-time stacks
  and ROS nodes. Most production SLAM is C++.
- **PyTorch.** `torch.compile` and TensorRT for deployment.
- **OpenCV, Open3D, PyTorch3D, Nerfstudio, gsplat** — daily
  libraries.
- **COLMAP / glomap, hloc** — structure-from-motion.
- **ROS2.** Topics, services, tf2, image_transport, rclpy/rclcpp.
  Learn enough to publish and subscribe to `/camera/image_raw`. Topics
  are typed pub/sub with build-time schema agreement.
- **Triton Inference Server, ONNX, TensorRT** — deployment. Robotics
  inference often runs at 30+ Hz on edge hardware (Jetson).
- **Docker + CUDA.** The container ships the CUDA toolkit but talks
  to the driver on the host; the version compatibility matrix is
  brutal and how robotics teams lose afternoons.

**Deployment lifecycle: PyTorch -> ONNX -> TensorRT -> Triton -> ROS2.**

1. **PyTorch checkpoint.** `.pt` or `.safetensors` plus the Python
   class. Great for research, too heavy and dynamic for a real-time
   loop on a Jetson.
2. **ONNX export.** `torch.onnx.export` traces the model into a
   framework-agnostic graph.
3. **TensorRT engine.** NVIDIA's optimizer fuses kernels, picks
   fp16/int8 precision, emits a `.engine` binary specialized to one
   GPU. Not portable across machines.
4. **Triton (optional).** Serving layer that batches across clients
   and exposes gRPC / HTTP. Use it when multiple nodes share one GPU;
   skip and load in-process when one node owns one GPU.
5. **ROS2 node.** Subscribes to `/camera/image_raw`, runs the engine,
   publishes on `/perception/detections`. Latency from
   `image.header.stamp` to `detections.header.stamp` is what your
   team grades you on.

Cross-reference `03-start.md` for the concrete starter that walks
steps 1-5 end to end.

**Mini-project.** Take pretrained YOLOv8n, export to ONNX, convert
to a TensorRT engine with `trtexec`, benchmark before and after. No
NVIDIA GPU? Substitute ONNX Runtime with the CPU provider.

## Layer 7: Robotics integration

- **Sensors.** RGB cameras (USB / GigE), depth cameras (RealSense,
  Orbbec, Azure Kinect), LiDAR (Velodyne, Hesai, Livox, Ouster),
  IMUs, event cameras.
- **Time synchronization.** Cameras and IMUs run at different rates.
  Hardware sync, PTP, or software interpolation. A surprising share
  of perception bugs are sync bugs.
- **Calibration.** Camera-to-camera, camera-to-IMU, camera-to-LiDAR.
  Use Kalibr. Recalibrate when hardware moves.
- **Coordinate frames.** Every robot has a tree: world -> base ->
  arm -> end-effector -> camera. ROS's `tf2` tracks it. Get it wrong
  and your math is off by a rotation.

**Sensor-fusion gotcha catalog.**

1. **Timestamp drift between sensors.** IMU and camera on different
   USB buses, each with its own clock and OS jitter. Symptom: VIO
   correct stationary, smears under fast motion. Fix: hardware-trigger
   the camera off the IMU, run PTP, or estimate the offset online
   (Kalibr).
2. **Rolling vs. global shutter.** Rolling shutter reads rows over
   ~10 ms; motion during that window bends straight lines. Symptom:
   SLAM fine on tripod, falls apart on the robot. Fix: global-shutter
   sensor, or a front-end that models rolling shutter.
3. **IMU bias drift.** Accelerometer and gyro biases wander with
   temperature and time. Symptom: pose tilts even when still. Fix:
   estimate biases as filter states; never trust factory biases past
   a session.
4. **Extrinsic calibration rot.** A tech replaces a bracket and the
   camera-to-LiDAR transform is off by a degree. Symptom: LiDAR
   points project a few pixels off; depth fusion produces ghosts.
   Fix: monthly audits, recompute after any hardware touch, version
   calibration in git with hardware serials.
5. **LiDAR-camera lighting mismatch.** At a tunnel entrance the
   camera blows out while LiDAR sails on; deep in a featureless
   tunnel LiDAR degenerates along the axis. Symptom: fused estimator
   weights one modality 100% and drifts. Fix: model sensor health
   explicitly, degrade gracefully.

**Mini-project.** Write a ROS2 Python node that subscribes to
`/camera/image_raw` and `/imu/data`, prints the time delta between
the latest sample of each, and publishes a histogram over the last 10
seconds. You'll be shocked how non-zero and non-constant that number
is without hardware sync.

## Must-read papers (in this order)

1. **ORB-SLAM3** (Campos et al., 2021). Modern classical SLAM:
   monocular, stereo, RGB-D, and visual-inertial in one codebase with
   loop closure and multi-map merging. Reference baseline every
   learned SLAM paper has to beat. Repo: `UZ-SLAMLab/ORB_SLAM3`, C++
   with Pangolin viewer and a separate Vocabulary file.
2. **NeRF** (Mildenhall et al., 2020). Novel view synthesis went from
   blurry interpolation to photoreal renders. Spawned Instant-NGP,
   Mip-NeRF, Nerfacto. Everything migrated to
   `nerfstudio-project/nerfstudio`.
3. **3D Gaussian Splatting** (Kerbl et al., 2023). NeRF lost its
   real-time crown: seconds per frame to 100+ FPS on one GPU. Most
   new neural-rendering work since 2024 is splat-based. Repo:
   `graphdeco-inria/gaussian-splatting`; friendlier reimplementation
   `nerfstudio-project/gsplat`.
4. **Segment Anything (SAM 1)** (Meta, 2023). Zero-shot segmentation
   from a point click became a one-line API; labeling pipelines were
   rebuilt overnight. Repo: `facebookresearch/segment-anything`. SAM
   2 (2024) adds video.
5. **DINOv2** (Meta, 2023). Self-supervised features that match or
   beat supervised pretraining; shipped in production as a frozen
   backbone. Repo: `facebookresearch/dinov2`, or load from
   `transformers`.
6. **FoundationPose** (NVIDIA, 2024). 6-DoF pose of a novel object
   from a CAD model, no per-object training. Replaced bespoke
   per-object pipelines in manipulation. Repo:
   `NVlabs/FoundationPose`, heavy CUDA, expects a mesh.
7. **Depth-Anything v2** (2024). Monocular metric depth became a
   drop-in component for non-safety-critical use. Repo:
   `DepthAnything/Depth-Anything-V2`, ~30 ms on a modern GPU.
8. **DROID-SLAM** (Teed & Deng, 2021). Learned SLAM became
   competitive with classical on accuracy; trade is a hefty GPU at
   inference. Repo: `princeton-vl/DROID-SLAM`, Python + custom CUDA.
9. **VGGT** (2025). Feed unposed images, get geometry + poses + depth
   in one forward pass. Details still shaking out; expect the
   ecosystem to evolve.

Write a 1-page summary of each in your own words — highest-leverage
habit in this field. Pair with `01-examples.md` for which papers
ended up in shipping systems.

## How perception engineers think differently

- **Explicit coordinate frames.** Suffix every variable with its
  frame: `p_world`, `p_cam`, `T_world_cam`. Implicit frames compile,
  run, and lie.
- **Failure-mode analysis up front.** Enumerate "what does this do at
  night / in rain / if the lens fogs / at 5 Hz?" before shipping. The
  list goes into the design doc so the planner downstream knows which
  failures degrade silently.
- **Latency as a hard budget.** 200 ms on an API call is fine; 200 ms
  in a perception pipeline means the robot drove half a meter past
  the obstacle. Allocate latency at design time.
- **Versioned reproducibility.** A bug is reopenable only with bag
  file + git sha + checkpoint sha + calibration sha together.
- **Distrust single frames.** Every detection is filtered, tracked,
  or aggregated before it influences a decision. One bad frame is
  normal; one bad trajectory is a bug.
- **Probabilistic correctness.** Every number is a point estimate
  with a covariance. Stop trying to make the estimator perfect;
  budget how much error each layer tolerates.

## Communities and people to follow

- Conferences: **CVPR**, **ICCV**, **ECCV** (vision); **CoRL**,
  **ICRA**, **IROS** (robotics-perception).
- Twitter/X: @TomasJakab, @ShuranSong, @DieterFox, @AndrewDavison,
  @AjdDavison, @jonbarron (NeRF), @yenchenlin (NeRF).
- Hugging Face Spaces — try SAM 2, Depth-Anything, DINOv2 demos.
- r/computervision for general lurking.
