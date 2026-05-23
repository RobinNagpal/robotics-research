# Important Things to Learn

If you're coming from web dev, the gap is **math** (linear algebra and
multi-view geometry) and **a small amount of robotics vocabulary**. The
good news: the python tooling (PyTorch, Hugging Face, Docker) is exactly
what you've been using for LLM work — perception just adds geometry on
top.

Mental reframe before you start: in web dev your "ground truth" is what
the server returned and your hardest bugs are usually concurrency or
state-management bugs. In perception your ground truth is *the physical
world* — which is noisy, badly lit, and lies to you. Your hardest bugs
are coordinate-frame bugs, timestamp bugs, and calibration bugs. The
code is often simpler than a React app; the *epistemics* are harder.
Whenever you're stuck, the first three questions to ask are: "what
frame is this number in?", "what timestamp is this number from?", and
"is my calibration still valid?" See `00-basics.md` for the vocabulary
that goes with these questions.

## Layer 0: Python and PyTorch

Same baseline as any ML field. Spend a week if you haven't:

- Python type hints, dataclasses, NumPy, pathlib. NumPy in particular
  is the closest analog to "Lodash for numerical data" — broadcasting
  rules play the role of implicit type coercion, and you must learn
  them or your shapes will silently misalign.
- PyTorch tensors and autograd. The mental model: a tensor is a
  multi-dimensional array, and `requires_grad=True` is like reactive
  state — PyTorch tracks every operation so it can auto-compute
  gradients later. A PyTorch tensor with `requires_grad=True` is
  basically a MobX observable: the framework instruments every read
  and write so it can recompute (gradients, in this case) when you
  call `.backward()`. Karpathy's "neural networks zero-to-hero"
  series is the best free intro that exists.
- **OpenCV** in Python. Loading images, drawing boxes, basic
  thresholding. You'll use this every day. Caveat from a web-dev
  brain: OpenCV stores colors as **BGR**, not RGB — the equivalent
  of an API that returns `{b, g, r}` instead of `{r, g, b}`. Forget
  this once and you will spend an hour debugging why your "blue"
  detector finds red things.
- Device discipline. `tensor.to("cuda")` and `tensor.to("cpu")` are
  the perception equivalent of `await` — every cross-device move is
  a sync point. Mixing devices in one expression throws; treat it
  like mixing `Promise<T>` with `T`.

**Mini-project to cement this layer.** In one evening, write a 40-line
PyTorch script that loads a single JPEG with OpenCV, converts BGR to
RGB, normalizes it to a `[1, 3, H, W]` tensor, runs it through a
pretrained ResNet-18 from `torchvision`, and prints the top-5 ImageNet
labels. The whole thing is shorter than a typical React component and
gets you fluent with the tensor / device / dtype shuffle that every
perception script begins with.

## Layer 1: Math foundations (the part that scares web devs unnecessarily)

You do not need a PhD; you need the following 6 concepts to "click."
Think of them as the six "primitive types" of 3D — once they're in
muscle memory, the rest of perception is composition.

- **Matrices as transforms.** A 3x3 matrix rotates / scales a 3D
  point. A 4x4 matrix can also translate it. This is the only way 3D
  computation is done.
  - *30-second equation walkthrough.* Picture a point `p = [x, y, z]`
    as a 3-element column. Multiply by a 3x3 matrix `R` and you get
    `R @ p`, a new 3-element column rotated in space. Want to also
    *move* it? Append a 1 to make `[x, y, z, 1]` and use a 4x4 matrix
    whose top-right column is the translation `t`. The trailing 1 is
    a tiny hack that lets one matrix multiply handle both rotation
    and translation. That's it.
- **SE(3) and SO(3).** Names for "the group of all 3D rigid-body
  transforms" and "the group of all rotations." Don't memorize the
  group theory — just know that an SE(3) is a 4x4 matrix and an SO(3)
  is a 3x3 matrix that preserves lengths. Think of SE(3) as the
  typed wrapper around `(position, orientation)` — like a TypeScript
  branded type that prevents you from accidentally adding a
  world-frame pose to a camera-frame pose. The whole point of
  carrying the type around is to surface frame mismatches at compose
  time instead of three layers downstream.
  - *30-second equation walkthrough.* SO(3) means "any rotation, no
    scaling, no shearing" — equivalently a 3x3 matrix `R` with
    `R.T @ R == I` and `det(R) == +1`. SE(3) glues an SO(3) to a
    translation: `T = [[R, t], [0, 0, 0, 1]]`. Composing two SE(3)s
    is matrix multiplication. Inverse is `[[R.T, -R.T @ t], [0,0,0,1]]`,
    not the generic 4x4 inverse — exploit the structure.
- **Quaternions.** A 4-number compact way to store a rotation that
  avoids the "gimbal lock" bug. Standard in robotics; libraries like
  Sophus or `scipy.spatial.transform.Rotation` handle the math. A
  quaternion is a compact serialization format for rotation, the way
  a JWT is a compact serialization for an auth token — humans cannot
  read it directly, but it survives composition and interpolation
  cleanly and you trust the library to encode/decode it.
  - *30-second equation walkthrough.* A unit quaternion is
    `q = (w, x, y, z)` with `w^2 + x^2 + y^2 + z^2 == 1`. The `w` is
    "how much rotation" (cosine of half the angle) and `(x, y, z)` is
    "around which axis" (sine of half the angle times the axis).
    Composing two rotations is quaternion multiplication, four
    multiplies and some signs — way cheaper than 27 multiplies for
    two 3x3 matmuls. Different libraries disagree on whether the
    order is `(w, x, y, z)` or `(x, y, z, w)`; check the docs every
    single time.
- **Pinhole camera model.** Pixels = `K * [R | t] * world_point`,
  where `K` is the intrinsic matrix and `[R | t]` is the extrinsic
  pose. Understand this one equation and 80% of multi-view geometry
  is unlocked.
  - *30-second equation walkthrough.* Take a world point `X`. The
    extrinsic `[R | t]` rotates and translates it into the camera's
    coordinate frame, giving `X_cam`. Divide by `Z_cam` to project
    onto a unit-depth plane (this is the "perspective divide"; far
    things shrink). Multiply by the 3x3 intrinsic `K` (which encodes
    focal length and the principal point in pixels) and you get pixel
    `(u, v)`. The whole pipeline is one matmul followed by a divide.
- **Epipolar geometry, triangulation, PnP.** How to recover 3D
  structure given 2D pixels in two or more views. PnP =
  "Perspective-n-Point": given known 3D points and their pixel
  observations, solve for camera pose. Used everywhere.
  - *30-second equation walkthrough for PnP.* You have N known 3D
    points `X_i` and their pixel observations `u_i` in one image.
    For an unknown pose `(R, t)`, the predicted pixel is
    `pi(K @ (R @ X_i + t))`. PnP minimizes `sum_i || u_i - predicted ||^2`
    over `(R, t)`. Four points (one of them off-plane) is the minimum
    for a unique solution; in practice you give it 50+ and RANSAC the
    outliers. Solvers: `cv2.solvePnP`, EPnP, SQPnP.
- **Bundle adjustment.** Jointly optimize all camera poses + 3D
  points to minimize reprojection error. The math engine inside
  every SLAM system; you'll call it as a library (Ceres, g2o,
  GTSAM, pypose), not implement it.
  - *30-second equation walkthrough.* Same loss as PnP, but the
    `X_i` are *also* unknowns and you have *many* cameras. So you
    minimize `sum_{cam c, point i visible in c} || u_{c,i} - pi(K @ (R_c @ X_i + t_c)) ||^2`
    over every pose and every point at once. The Jacobian is sparse
    (each residual touches only one camera and one point), so
    specialized solvers like Ceres exploit that sparsity. That
    sparsity is the entire reason BA scales to thousands of frames.

If you only do one course: **Stanford CS231A** (computer vision: from
3D reconstruction to recognition). Lecture videos free on YouTube. See
`06-courses.md` for the longer list and which weeks to skip.

**Mini-project to cement this layer.** In one evening, draw a virtual
1m cube at the origin and a virtual camera 3m back looking at it.
Hand-build `K`, `R`, and `t` in NumPy, project the 8 corners to pixels,
and use matplotlib to draw the wireframe. Then translate the cube by
0.5m and re-project. If the cube moves the right way on the image,
you have internalized the pinhole model — which is more than half of
new perception engineers can claim on day one.

## Layer 2: Classical computer vision (still the bread and butter)

Classical CV is not "the old way" — it is the substrate everything
else runs on. Even your fanciest transformer pipeline still uses
classical geometry to triangulate, to RANSAC, and to calibrate. Treat
this layer as the equivalent of HTTP / TCP for a web dev: you do not
hand-write packets, but if you do not know how they work, you will
not be able to debug the day they misbehave.

- **Feature detection / matching:** SIFT (the OG, 1999), ORB (fast
  binary descriptor), SuperPoint (learned, 2018), LightGlue (learned
  matcher, 2023). LightGlue is the current default for SLAM-grade
  matching.

  | Detector / matcher | Year | Speed | Accuracy | License | Notes |
  |---|---|---|---|---|---|
  | SIFT | 1999 | slow | high | free since 2020 (patent expired) | rotation- and scale-invariant; gold-standard baseline |
  | ORB | 2011 | very fast | medium | BSD (OpenCV) | binary descriptor; default in ORB-SLAM family |
  | SuperPoint | 2018 | fast on GPU | high | research / non-commercial in original release | learned keypoints; widely re-implemented |
  | LightGlue | 2023 | fast on GPU | very high | Apache-2.0 | matcher, not a detector; pair with SuperPoint / DISK |

  Pick by constraint: pure CPU and embedded? ORB. GPU available and
  you want best matches? SuperPoint + LightGlue. Need a permissive
  license guaranteed? double-check the model card — research code
  often ships under a non-commercial license and the weights are the
  thing that matters.
- **Stereo and structured light.** How depth cameras work. Two
  cameras side-by-side, triangulate disparities. Structured light is
  a projector + camera (the original Kinect). A depth camera is the
  hardware equivalent of `Promise.all([leftEye, rightEye])` resolved
  by a tiny FPGA — you receive an already-aligned depth image, but
  every quirk of that fusion (occlusions, IR interference, baseline
  limits) leaks into your data.

  | Depth sensor | Typical range | Accuracy | Lighting tolerance | Notes |
  |---|---|---|---|---|
  | Passive stereo | 0.3 - 10 m | medium | needs texture, fails on blank walls | RealSense D4xx; cheapest |
  | Active stereo (IR projector) | 0.3 - 5 m | medium-high indoor | bad in direct sunlight (IR washout) | RealSense D435i, Orbbec |
  | Structured light | 0.5 - 3 m | high indoor | fails outdoor | original Kinect, iPhone TrueDepth |
  | Time of Flight (ToF) | 0.3 - 5 m (short), longer for industrial | high | multi-path artifacts on shiny / corners | Azure Kinect, PMD |
  | LiDAR | 1 - 200 m | very high in range | works in dark, struggles in heavy rain / fog | Velodyne, Ouster, Livox, Hesai |

- **Optical flow.** Per-pixel motion between two frames. Lucas-Kanade
  (classical), RAFT (learned). Mental model: flow is `git diff` for
  pixels — every pixel reports a 2D displacement to its match in the
  next frame. Sparse flow (Lucas-Kanade) only reports it at corners;
  dense flow (RAFT) reports it everywhere.
- **Camera calibration.** Zhang's method (checkerboard) for a single
  camera; Kalibr for IMU + multi-camera rigs. You will calibrate
  cameras. Many times. Calibration is to perception what env-var
  configuration is to a web app: invisible when right, catastrophic
  when wrong, and almost always the actual cause when nothing else
  explains the bug.

**Mini-project to cement this layer.** Calibrate your laptop webcam
with OpenCV in 30 minutes. Print a 9x6 checkerboard, capture 20 frames
holding it at different angles, run `cv2.calibrateCamera`, and save
`K` and the distortion coefficients to a JSON file. Then take a single
new photo, pick a pixel on a known object (say, a corner of a sheet of
paper at a known distance), back-project to a 3D ray, and reproject a
point on that ray. If it lands where you expect, you have just done
your first end-to-end multi-view geometry pipeline. Keep the JSON; you
will use it in the SLAM mini-project later.

## Layer 3: Modern deep computer vision

- **CNNs** — convolutional networks (ResNet, EfficientNet). Still
  ship in production; understand them as a 1-day refresher. A CNN is
  effectively a stack of learned image filters; the analogy is a CSS
  filter chain where the kernel weights were chosen by gradient
  descent on a dataset rather than by a designer's eye.
- **Vision Transformers (ViT, Swin, DINO).** The replacement.
  Architecturally identical to text transformers; the only twist is
  splitting an image into 16x16 patches and treating each patch as a
  "token." If you have ever tokenized text into BPE subwords, a ViT
  is the same idea applied to images — except the "tokenizer" is just
  a grid chop, no learned vocabulary.
- **Detection.** DETR family (transformer-based), YOLO v8 / v11
  (CNN-based, fast). YOLO ships in everything; DETR variants win
  papers.
- **Segmentation.** SAM 2 for promptable, Mask2Former for trained.
- **Monocular depth.** Depth-Anything v2, Marigold (diffusion-based),
  ZoeDepth. Production quality from a single image — would have been
  unthinkable in 2020.
- **Vision foundation models.** DINOv2 (self-supervised features),
  CLIP / SigLIP (vision-language), Florence-2 (Microsoft, multi-task).
  Load from Hugging Face like a tokenizer.

**When to NOT reach for a foundation model.** It is tempting to drop
SAM 2 or Depth-Anything into every pipeline because the demos are
magic. In production this often loses to a 200-line YOLOv8 fine-tune,
and here is the honest cost ledger. A foundation model is a 300M-1B
parameter beast — on a Jetson Orin you may get 2-5 Hz at fp16 and burn
20+ watts. A YOLOv8n fine-tuned on your 5 object classes runs at
60+ Hz, fits in 50 MB, and costs you a tenth of the GPU memory budget
you need for everything else (planner, tracker, downstream policy).
Production latency budgets are usually under 33 ms end-to-end; that
leaves perhaps 10 ms for the detector. If your class set is fixed,
your camera is fixed, and you can label 2k images, the small purpose-
built model wins on latency, memory, cost per inference, and
predictability. Reach for the foundation model when (a) the class set
is open-ended, (b) you have no labels yet and need zero-shot, or
(c) prompt-driven flexibility is worth the watts. See
`01-examples.md` for the kinds of pipelines where each tier shows up.

**Mini-project to cement this layer.** In one evening, take a video
from your phone, run YOLOv8 on every frame with the Ultralytics
package, and draw boxes. Then swap in SAM 2 with point prompts on
one frame and let it propagate masks across the video. Compare the
two outputs side by side and note the runtime — you will viscerally
feel the tradeoff described above.

## Layer 4: 3D and neural rendering (the part that's eating perception)

- **Representations.** Point clouds, meshes, voxels, signed distance
  fields (SDFs), NeRFs, Gaussian splats. Each has trade-offs;
  Gaussian splats are the current default for photoreal renders.
  Think of these as competing data formats: a point cloud is JSON
  (universal, verbose, no built-in topology), a mesh is a normalized
  SQL schema (relations between vertices), an SDF is a procedural
  function (compute on demand), and a Gaussian splat scene is a
  binary blob format optimized for one renderer.
- **NeRF.** A small MLP that maps `(x, y, z, viewing direction) ->
  (RGB, density)`. You query it like a function. Slow.
- **3D Gaussian Splatting.** Scene = millions of fuzzy 3D blobs.
  Real-time rendering. Use Nerfstudio + gsplat.
- **Differentiable rendering.** `nvdiffrast`, gsplat, PyTorch3D. The
  ability to backprop through the renderer means you can fit
  geometry / texture / pose from pixels using gradient descent.

  *Plain-English explainer.* Imagine if React's `render` function
  were invertible — you could hand it the screenshot you want and it
  would compute the props that produce it. That is differentiable
  rendering. A normal renderer takes a scene (geometry + materials
  + camera) and produces pixels. A differentiable renderer also
  reports, for every pixel, how the pixel would change if you
  nudged any input parameter. That gradient lets you do the inverse
  problem: "given this photo, what scene must have produced it?"
  Optimize parameters with Adam, the way you train a network, and
  the geometry / texture / camera pose falls out. It is the entire
  reason NeRF and Gaussian splatting work at all.
- **6-DoF pose estimation.** FoundationPose, MegaPose, GigaPose —
  the model-based modern approach (give it a CAD model, no per-object
  training). For learned, see FFB6D, PoseCNN. "6-DoF" means three
  numbers for position and three for orientation — the full SE(3)
  pose of an object relative to the camera. The output of a
  pose-estimation node is what a grasp planner consumes upstream of
  any manipulation policy.

**Mini-project to cement this layer.** In one evening, capture 60
photos of an object on your desk from all sides with your phone, drop
them into Nerfstudio, train a `splatfacto` model on a single GPU for
20 minutes, and orbit the result in the web viewer. You will end the
evening with a free-look 3D reconstruction of an object you own — and
a visceral sense of why this approach has eaten so much of perception
research.

## Layer 5: SLAM and visual localization (the moving-camera problem)

- **Visual odometry vs. visual-inertial vs. SLAM.** VO = "where did
  the camera move?", VIO = same plus IMU fusion, SLAM = same plus a
  map you can come back to. Pick the strictness based on application.
  Web-dev analogy: VO is a stateless API endpoint, VIO is the same
  endpoint with an idempotency token (IMU integration smooths the
  jitter), and SLAM adds a persistent database (the map) plus a
  query that asks "have I been here before?" (loop closure).
- **Filter-based** (EKF, MSCKF) vs. **optimization-based** (ORB-SLAM3,
  VINS-Fusion). Modern systems are optimization-based.
- **Learned SLAM.** DROID-SLAM (NeurIPS 2021), DPVO. Higher
  accuracy, more compute.
- **Visual relocalization.** Given a new image, find where you are
  on an existing map. hloc + SuperPoint + LightGlue is the modern
  pipeline.

| System | Language | Sensors | License | Learned vs classical | Typical use case |
|---|---|---|---|---|---|
| ORB-SLAM3 | C++ | mono / stereo / RGB-D / VI | GPLv3 | classical | research baseline; well-documented; reference for "what good SLAM looks like" |
| VINS-Fusion | C++ | mono / stereo + IMU | GPLv3 | classical | drones; tight VIO pipeline from HKUST |
| OpenVSLAM / Stella-VSLAM | C++ | mono / stereo / RGB-D | 2-clause BSD (Stella fork) | classical | when license matters; ORB-SLAM-style features without GPL |
| DROID-SLAM | Python (CUDA ops) | mono / stereo / RGB-D | research code, check repo | learned (recurrent flow) | offline reconstruction; GPU required |
| NeRF-SLAM / Glorie-SLAM | Python | mono / RGB-D | research code | learned + classical hybrid | research; dense reconstruction with neural map |
| Spectacular AI | closed-source SDK | various, vendor-specific | commercial | hybrid | shipping product where you do not want to maintain SLAM yourself |

Hedging: the SLAM landscape moves fast and licenses change; double-
check the repo before committing to a stack, especially for any
commercial use.

**Mini-project to cement this layer.** In one evening, download the
EuRoC MAV dataset (a standard drone visual-inertial benchmark), run
ORB-SLAM3 in its stereo-inertial mode on one sequence, and compare
the estimated trajectory to the ground truth with `evo_traj`. You
will get an Absolute Trajectory Error number in meters — your first
quantitative SLAM result. The first time the trajectory plot overlays
the ground truth almost perfectly is a small dopamine hit you do not
forget.

## Layer 6: Tooling and infra

- **Languages:** Python for research and prototyping; **C++** for
  real-time stacks and ROS nodes. You will end up writing some C++
  if you go deep — most production SLAM is C++.
- **PyTorch 2.x** — the framework. `torch.compile` and TensorRT for
  deployment.
- **OpenCV, Open3D, PyTorch3D, Nerfstudio, gsplat** — the daily
  libraries.
- **COLMAP / glomap, hloc** — structure-from-motion pipelines.
- **ROS2** — the operating system robots run. Topics, services,
  tf2, image_transport, rclpy/rclcpp. Learn enough to publish and
  subscribe to a `/camera/image_raw` topic. A ROS2 topic is a typed
  pub/sub stream — think Redis Streams or NATS subjects, but with
  code generation for message types so the consumer and the producer
  agree on the schema at build time, not at parse time.
- **Triton Inference Server, ONNX, TensorRT** — deployment.
  Robotics inference often runs at 30+ Hz on edge hardware (Jetson),
  so deployment matters.
- **Docker + CUDA** — same gotchas as ML in general. CUDA versions
  are how robotics teams lose afternoons. Docker for CUDA is like
  Docker for Node, but with one extra dependency (the host driver)
  that ruins your day if it does not match: the container ships the
  CUDA *toolkit*, but it talks to the *driver* on the host, and the
  version compatibility matrix is brutal.

**The deployment lifecycle: PyTorch -> ONNX -> TensorRT -> Triton -> ROS2 node.**

1. **PyTorch checkpoint.** Your training output: a `.pt` or
   `.safetensors` file with weights, plus the Python class that
   defines the architecture. Great for research, way too heavy and
   too dynamic for a real-time loop on a Jetson.
2. **ONNX export.** `torch.onnx.export` traces the model and writes
   a framework-agnostic computation graph. ONNX is the equivalent
   of compiling your TypeScript to plain ES2015 — you lose the nice
   developer ergonomics but anything can now run it.
3. **TensorRT engine.** NVIDIA's optimizer consumes the ONNX file,
   fuses kernels, picks fp16/int8 precision, and emits a `.engine`
   binary specialized to one specific GPU. TensorRT is Webpack with
   tree-shaking and Babel: same source model, much smaller and
   faster after the optimizer hits it — and, like a production
   bundle, not portable across machines.
4. **Triton Inference Server (optional).** A serving layer that
   loads many engines, batches requests across clients, and exposes
   gRPC / HTTP. Use it when multiple ROS nodes (or multiple robots)
   share one GPU. Skip it when one ROS node owns one GPU; load the
   engine in-process instead.
5. **ROS2 node.** A C++ or Python process that subscribes to
   `/camera/image_raw`, runs the engine, and publishes results on a
   typed topic like `/perception/detections`. This is where you
   finally meet timestamps, frame IDs, and QoS profiles. Latency
   measured from `image.header.stamp` to `detections.header.stamp`
   is the number your team will actually grade you on.

Cross-reference `03-start.md` for the concrete starter project that
walks through steps 1-5 end to end.

**Mini-project to cement this layer.** In one evening, take a
pretrained YOLOv8n from Ultralytics, export to ONNX, convert to a
TensorRT engine with `trtexec`, and benchmark inference latency on
your machine before and after. If you do not have an NVIDIA GPU,
substitute ONNX Runtime with the CPU execution provider — the
lifecycle steps are identical, only the final runtime differs.

## Layer 7: Robotics integration

- **Sensors:** RGB cameras (USB / GigE), depth cameras (Intel
  RealSense, Orbbec, Microsoft Azure Kinect), LiDAR (Velodyne,
  Hesai, Livox, Ouster), IMUs, event cameras.
- **Time synchronization.** Cameras run at different rates than
  IMUs. Hardware sync, PTP, or software interpolation. A surprising
  amount of perception bugs are sync bugs.
- **Calibration.** Camera-to-camera, camera-to-IMU, camera-to-LiDAR.
  Use Kalibr. Recalibrate when hardware moves.
- **Coordinate frames.** Every robot has a tree: world -> base ->
  arm -> end-effector -> camera. ROS's `tf2` tracks this. Get this
  wrong and your math will be off by a rotation. The `tf2` tree is
  the perception equivalent of React context: an ambient,
  hierarchical lookup of "given a name, give me the current value."
  Except here the value is an SE(3) and it updates at 100 Hz.

**Sensor-fusion gotcha catalog.** Five specific bugs that bite new
perception engineers, written so you recognize the symptom:

1. **Timestamp drift between sensors.** Your IMU is on a USB bus and
   your camera is on another, each stamps frames in its own clock,
   and the OS adds a variable few-millisecond delay. Symptom: VIO
   trajectory looks correct when stationary but smears during fast
   motion. Fix: hardware-trigger the camera off the IMU, or run PTP
   if both speak it, or estimate the offset online (Kalibr can do
   this).
2. **Rolling shutter vs. global shutter.** A rolling-shutter camera
   reads pixels row by row over ~10 ms; if the robot moves during
   that window, straight lines bend. Symptom: SLAM works fine on
   tripod data and falls apart on the actual robot. Fix: use a
   global-shutter sensor for SLAM, or use a SLAM front-end that
   models rolling shutter explicitly.
3. **IMU bias drift.** Accelerometer and gyro biases are not
   constant — they wander with temperature and over hours of
   operation. Symptom: pose estimate slowly tilts even when the
   robot is still. Fix: estimate biases as states in your filter,
   warm up the IMU before calibrating, never trust factory-shipped
   biases for more than a session.
4. **Extrinsic calibration rot from screws loosening.** You
   calibrated the camera-to-LiDAR transform on Tuesday; on Friday
   a tech replaced a mounting bracket and now the transform is
   off by a degree. Symptom: LiDAR points project a few pixels off
   in the image; downstream depth fusion produces ghost objects.
   Fix: monthly calibration audit, recompute after any hardware
   touch, store calibration files versioned in git with hardware
   serial numbers.
5. **LiDAR-camera lighting mismatch in tunnels and glare.** The
   LiDAR sees the tunnel walls fine; the camera is overexposed at
   the entrance and underexposed inside, so visual features vanish
   while LiDAR sails on. Symptom: the fused estimator suddenly
   weights LiDAR 100% and drifts in long featureless tunnels
   where LiDAR also degenerates (a long pipe has no geometric
   anchor along its axis). Fix: model sensor health explicitly,
   degrade gracefully, do not assume one modality is always
   trustworthy.

**Mini-project to cement this layer.** In one evening, write a tiny
ROS2 Python node that subscribes to `/camera/image_raw` and
`/imu/data`, prints the time delta between the latest sample of each,
and publishes a histogram of that delta over the last 10 seconds. You
will be shocked how non-zero and non-constant that number is on a
laptop without hardware sync — which is exactly the lesson.

## Must-read papers (in this order)

1. **ORB-SLAM3** (Campos et al., 2021) — modern classical SLAM.
   After this paper, "classical SLAM that handles monocular, stereo,
   RGB-D, and visual-inertial in one codebase with loop closure and
   multi-map merging" became a solved-on-paper problem and the
   reference baseline every learned SLAM paper has to beat. Repo
   pattern: `UZ-SLAMLab/ORB_SLAM3`, dense C++ with Pangolin viewer
   and a Vocabulary file you must download separately.
2. **NeRF** (Mildenhall et al., 2020). After this paper, "novel view
   synthesis" stopped meaning blurry interpolation and started
   meaning photoreal renders from any angle. Spawned a thousand
   follow-ups (Instant-NGP, Mip-NeRF, Nerfacto). Repo pattern: small
   PyTorch script for the original, then everything migrated to
   `nerfstudio-project/nerfstudio`.
3. **3D Gaussian Splatting** (Kerbl et al., 2023). After this paper,
   NeRF lost its real-time crown — rendering went from seconds per
   frame to 100+ FPS on a single GPU. Most new neural-rendering work
   since 2024 is splat-based. Repo pattern: original CUDA in
   `graphdeco-inria/gaussian-splatting`, friendlier reimplementations
   in `nerfstudio-project/gsplat`.
4. **Segment Anything (SAM 1)** (Meta, 2023). After this paper,
   "zero-shot segmentation of anything from a point click" became a
   one-line API and labeling pipelines were rebuilt around it
   overnight. Repo pattern: `facebookresearch/segment-anything`,
   with a checkpoint download and a 20-line demo. SAM 2 (2024) adds
   video.
5. **DINOv2** (Meta, 2023). After this paper, "self-supervised
   features that match or beat supervised pretraining" stopped being
   a research curiosity and started shipping in production
   pipelines as a frozen backbone. Repo pattern:
   `facebookresearch/dinov2`, or load from `transformers`.
6. **FoundationPose** (NVIDIA, 2024). After this paper, "6-DoF pose
   estimation of a novel object from a CAD model, no per-object
   training" became practical. Replaced a lot of bespoke per-object
   training pipelines in manipulation. Repo pattern:
   `NVlabs/FoundationPose`, heavy CUDA dependencies, expects a mesh.
7. **Depth-Anything v2** (2024). After this paper, monocular metric
   depth from a single image became a drop-in component you could
   trust for non-safety-critical use. Repo pattern:
   `DepthAnything/Depth-Anything-V2`, Hugging Face hosted, ~30 ms
   on a modern GPU.
8. **DROID-SLAM** (Teed & Deng, 2021). After this paper, learned
   SLAM became competitive with classical on accuracy; the trade is
   a hefty GPU at inference. Repo pattern:
   `princeton-vl/DROID-SLAM`, Python + custom CUDA ops.
9. **VGGT** (2025). After this paper, "feed a handful of unposed
   images, get geometry + poses + depth in one forward pass" became
   the new bar for transformer-based 3D. Hedging: details still
   shaking out, expect the repo and surrounding ecosystem to evolve.

Write a 1-page summary of each in your own words. Single
highest-leverage habit in this field. Pair this with `01-examples.md`
to see which of these papers ended up in shipping systems.

## How perception engineers think differently from web engineers

Worth naming explicitly because the shifts are easy to underestimate
until they bite you:

- **Preference for explicit coordinate frames over implicit globals.**
  In a web app, `Date.now()` and the user's locale are ambient.
  Perception engineers reflexively suffix every variable name with a
  frame: `p_world`, `p_cam`, `T_world_cam`. Implicit frames are the
  perception equivalent of mixing up Unix and ISO 8601 timestamps —
  it compiles, it runs, it lies.
- **Failure-mode analysis as first-class.** A web engineer ships and
  watches Sentry. A perception engineer enumerates failure modes
  *before* shipping: "what does this do at night?", "what does this
  do in rain?", "what does this do if the lens fogs?", "what does
  this do at 5 Hz instead of 30?" The list goes into the design doc;
  the planner downstream needs to know which failures degrade
  silently and which raise an alarm.
- **Sensor latency as a constraint, not a property.** A 200 ms p99
  on an API call is fine; 200 ms latency on a perception pipeline
  means the robot has driven half a meter past the obstacle. Latency
  is a hard budget you allocate at design time, not something you
  optimize at the end.
- **Reproducibility via seeded RNG and frozen calibration files.**
  A web bug is reproducible if you have the request payload. A
  perception bug is reproducible only if you have the bag file, the
  calibration JSON at that moment, the model checkpoint, and the
  random seed. Versioning all four together is non-negotiable;
  bagfile + git-sha + checkpoint-sha + calibration-sha is the
  minimum receipt to reopen a bug.
- **Distrust of single-frame inference.** A web engineer trusts a
  single API response. A perception engineer trusts no single frame
  — every detection is filtered, tracked, or aggregated across time
  before it influences a decision. One bad frame is normal; one bad
  trajectory is a bug.
- **Comfort with approximation over exactness.** In web dev,
  "wrong" usually means "wrong." In perception, every number is a
  point estimate with a covariance, and "wrong" is a probabilistic
  statement. Engineers who internalize this stop trying to make the
  estimator perfect and start budgeting how much error each layer
  can tolerate.

## Communities and people to follow

- Conferences: **CVPR**, **ICCV**, **ECCV** (vision); **CoRL**,
  **ICRA**, **IROS** (robotics-perception).
- Twitter/X: @TomasJakab, @ShuranSong, @DieterFox, @AndrewDavison,
  @AjdDavison, @jonbarron (NeRF), @yenchenlin (NeRF).
- Hugging Face Spaces — try SAM 2, Depth-Anything, DINOv2 demos.
- r/computervision for general lurking.
