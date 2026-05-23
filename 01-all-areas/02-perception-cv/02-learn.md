# Important Things to Learn

If you're coming from web dev, the gap is **math** (linear algebra and
multi-view geometry) and **a small amount of robotics vocabulary**. The
good news: the python tooling (PyTorch, Hugging Face, Docker) is exactly
what you've been using for LLM work — perception just adds geometry on
top.

## Layer 0: Python and PyTorch

Same baseline as any ML field. Spend a week if you haven't:

- Python type hints, dataclasses, NumPy, pathlib.
- PyTorch tensors and autograd. The mental model: a tensor is a
  multi-dimensional array, and `requires_grad=True` is like reactive
  state — PyTorch tracks every operation so it can auto-compute
  gradients later. Karpathy's "neural networks zero-to-hero" series
  is the best free intro that exists.
- **OpenCV** in Python. Loading images, drawing boxes, basic
  thresholding. You'll use this every day.

## Layer 1: Math foundations (the part that scares web devs unnecessarily)

You do not need a PhD; you need the following 6 concepts to "click."

- **Matrices as transforms.** A 3x3 matrix rotates / scales a 3D
  point. A 4x4 matrix can also translate it. This is the only way 3D
  computation is done.
- **SE(3) and SO(3).** Names for "the group of all 3D rigid-body
  transforms" and "the group of all rotations." Don't memorize the
  group theory — just know that an SE(3) is a 4x4 matrix and an SO(3)
  is a 3x3 matrix that preserves lengths.
- **Quaternions.** A 4-number compact way to store a rotation that
  avoids the "gimbal lock" bug. Standard in robotics; libraries like
  Sophus or `scipy.spatial.transform.Rotation` handle the math.
- **Pinhole camera model.** Pixels = `K * [R | t] * world_point`,
  where `K` is the intrinsic matrix and `[R | t]` is the extrinsic
  pose. Understand this one equation and 80% of multi-view geometry
  is unlocked.
- **Epipolar geometry, triangulation, PnP.** How to recover 3D
  structure given 2D pixels in two or more views. PnP =
  "Perspective-n-Point": given known 3D points and their pixel
  observations, solve for camera pose. Used everywhere.
- **Bundle adjustment.** Jointly optimize all camera poses + 3D
  points to minimize reprojection error. The math engine inside
  every SLAM system; you'll call it as a library (Ceres, g2o,
  GTSAM, pypose), not implement it.

If you only do one course: **Stanford CS231A** (computer vision: from
3D reconstruction to recognition). Lecture videos free on YouTube.

## Layer 2: Classical computer vision (still the bread and butter)

- **Feature detection / matching:** SIFT (the OG, 1999), ORB (fast
  binary descriptor), SuperPoint (learned, 2018), LightGlue (learned
  matcher, 2023). LightGlue is the current default for SLAM-grade
  matching.
- **Stereo and structured light.** How depth cameras work. Two
  cameras side-by-side, triangulate disparities. Structured light is
  a projector + camera (the original Kinect).
- **Optical flow.** Per-pixel motion between two frames. Lucas-Kanade
  (classical), RAFT (learned).
- **Camera calibration.** Zhang's method (checkerboard) for a single
  camera; Kalibr for IMU + multi-camera rigs. You will calibrate
  cameras. Many times.

## Layer 3: Modern deep computer vision

- **CNNs** — convolutional networks (ResNet, EfficientNet). Still
  ship in production; understand them as a 1-day refresher.
- **Vision Transformers (ViT, Swin, DINO).** The replacement.
  Architecturally identical to text transformers; the only twist is
  splitting an image into 16x16 patches and treating each patch as a
  "token."
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

## Layer 4: 3D and neural rendering (the part that's eating perception)

- **Representations.** Point clouds, meshes, voxels, signed distance
  fields (SDFs), NeRFs, Gaussian splats. Each has trade-offs;
  Gaussian splats are the current default for photoreal renders.
- **NeRF.** A small MLP that maps `(x, y, z, viewing direction) ->
  (RGB, density)`. You query it like a function. Slow.
- **3D Gaussian Splatting.** Scene = millions of fuzzy 3D blobs.
  Real-time rendering. Use Nerfstudio + gsplat.
- **Differentiable rendering.** `nvdiffrast`, gsplat, PyTorch3D. The
  ability to backprop through the renderer means you can fit
  geometry / texture / pose from pixels using gradient descent.
- **6-DoF pose estimation.** FoundationPose, MegaPose, GigaPose —
  the model-based modern approach (give it a CAD model, no per-object
  training). For learned, see FFB6D, PoseCNN.

## Layer 5: SLAM and visual localization (the moving-camera problem)

- **Visual odometry vs. visual-inertial vs. SLAM.** VO = "where did
  the camera move?", VIO = same plus IMU fusion, SLAM = same plus a
  map you can come back to. Pick the strictness based on application.
- **Filter-based** (EKF, MSCKF) vs. **optimization-based** (ORB-SLAM3,
  VINS-Fusion). Modern systems are optimization-based.
- **Learned SLAM.** DROID-SLAM (NeurIPS 2021), DPVO. Higher
  accuracy, more compute.
- **Visual relocalization.** Given a new image, find where you are
  on an existing map. hloc + SuperPoint + LightGlue is the modern
  pipeline.

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
  subscribe to a `/camera/image_raw` topic.
- **Triton Inference Server, ONNX, TensorRT** — deployment.
  Robotics inference often runs at 30+ Hz on edge hardware (Jetson),
  so deployment matters.
- **Docker + CUDA** — same gotchas as ML in general. CUDA versions
  are how robotics teams lose afternoons.

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
  wrong and your math will be off by a rotation.

## Must-read papers (in this order)

1. **ORB-SLAM3** (Campos et al., 2021) — modern classical SLAM.
2. **NeRF** (Mildenhall et al., 2020).
3. **3D Gaussian Splatting** (Kerbl et al., 2023).
4. **Segment Anything (SAM 1)** (Meta, 2023).
5. **DINOv2** (Meta, 2023).
6. **FoundationPose** (NVIDIA, 2024).
7. **Depth-Anything v2** (2024).
8. **DROID-SLAM** (Teed & Deng, 2021).
9. **VGGT** (2025).

Write a 1-page summary of each in your own words. Single
highest-leverage habit in this field.

## Communities and people to follow

- Conferences: **CVPR**, **ICCV**, **ECCV** (vision); **CoRL**,
  **ICRA**, **IROS** (robotics-perception).
- Twitter/X: @TomasJakab, @ShuranSong, @DieterFox, @AndrewDavison,
  @AjdDavison, @jonbarron (NeRF), @yenchenlin (NeRF).
- Hugging Face Spaces — try SAM 2, Depth-Anything, DINOv2 demos.
- r/computervision for general lurking.
