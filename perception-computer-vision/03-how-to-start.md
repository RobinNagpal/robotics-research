# How to Get Started

A 6-8 week ramp from zero to a demoable portfolio.

## Week 1-2: Classical foundations

- Work through Stanford **CS231A** (computer vision: from 3D
  reconstruction to recognition) lecture notes — best multi-view geometry
  intro.
- Re-implement: pinhole projection, 8-point algorithm, PnP, RANSAC.
- Calibrate your laptop webcam with OpenCV; reproject a known checkerboard.

## Week 3-4: Modern deep CV

- Stanford **CS231n** (deep learning for vision) for the NN side.
- Run SAM 2, DINOv2, Depth-Anything v2 on your own photos via Hugging
  Face. Wire them into a small Python service.
- Train a tiny detector on a custom dataset with YOLO v11 (Ultralytics).

## Week 5-6: 3D and neural rendering

- Capture 30-50 phone photos of a desk, run COLMAP, then feed into
  Nerfstudio and gsplat. Render novel views.
- Read the 3D Gaussian Splatting paper end to end.
- Try FoundationPose on a single 3D-printed or LEGO object you own.

## Week 7-8: One real robotics integration

Pick one:

- ORB-SLAM3 on a phone or USB-camera trajectory; visualize the map.
- Build a small ROS2 node that runs SAM 2 segmentation on a camera topic.
- A Gaussian-splat-from-phone-walkthrough pipeline that exports a mesh
  loadable in Isaac Sim.

## Datasets to know inside-out

KITTI, nuScenes, ScanNet, TUM RGB-D, Replica, BOP, EuRoC.

## Communities and conferences

CVPR, ICCV, ECCV (vision); CoRL, ICRA, IROS (robotics-perception);
roboticists on X/Twitter; r/computervision; Hugging Face spaces for
vision foundation models.
