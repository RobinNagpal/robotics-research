# Important Things to Learn

## Math foundations

- Linear algebra: SVD, eigendecomposition, least squares.
- Rigid-body transforms: SE(3), SO(3), quaternions, Lie groups (enough to
  use Sophus / pypose).
- Multi-view geometry: pinhole camera model, intrinsics/extrinsics,
  epipolar constraint, triangulation, PnP, bundle adjustment.
- Bayesian filtering: Kalman, EKF, particle filter (still everywhere in
  perception).
- Probability for vision: GMMs, RANSAC, robust estimation.

## Classical CV

- Feature detection/matching: SIFT, ORB, SuperPoint, LightGlue.
- Stereo and structured light.
- Optical flow.
- Camera calibration (Zhang's method, Kalibr).

## Modern deep CV

- CNNs and Vision Transformers (ViT, Swin, DINO).
- Detection: DETR family, YOLO v8/v11.
- Segmentation: SAM 2, Mask2Former.
- Depth: Depth-Anything, Marigold, ZoeDepth.
- Self-supervised features: DINOv2, MAE, CLIP.

## 3D and neural rendering

- Point clouds, meshes, voxels, SDFs, NeRF, Gaussian splatting.
- Differentiable rendering (nvdiffrast, gsplat).
- 6-DoF pose: FoundationPose, MegaPose, GigaPose.

## Tooling

- **Languages:** Python (everything), C++ (real-time stacks, ROS nodes).
- **Libraries:** PyTorch, OpenCV, Open3D, PyTorch3D, Nerfstudio, gsplat,
  COLMAP, hloc.
- **Robotics integration:** ROS2, tf2, image_transport, rclpy/rclcpp.
- **Datasets/benchmarks:** KITTI, nuScenes, ScanNet, Replica, TUM RGB-D,
  Hypersim, BOP (pose).

## Must-read papers

ORB-SLAM3, NeRF, 3D Gaussian Splatting, Segment Anything, DINOv2,
FoundationPose, Depth-Anything v2, DROID-SLAM, VGGT.
