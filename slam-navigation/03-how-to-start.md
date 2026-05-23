# How to Get Started

## Week 1-2: Probabilistic robotics

- Read Thrun, Burgard, Fox **"Probabilistic Robotics"** chapters 1-9.
- Implement an EKF in 1D, then in 2D for a differential drive robot.
- Cyrill Stachniss's YouTube lectures (Bonn) are the best free SLAM
  course online.

## Week 3-4: Hands-on classical SLAM

- Run ORB-SLAM3 on the EuRoC and TUM RGB-D datasets. Compare ATE/RPE
  with evo.
- Run VINS-Fusion or OpenVINS on the same data.
- Capture your own visual-inertial dataset with an iPhone (NeRFCapture
  app or RTAB-Map) and run SLAM on it.

## Week 5: LiDAR SLAM

- Run FAST-LIO2 / GLIM on a public Velodyne or Ouster dataset
  (Newer College, KITTI, MulRan).
- Visualize the map in CloudCompare or Foxglove.

## Week 6: Learned SLAM

- Run DROID-SLAM on a custom video.
- Try SplaTAM or Gaussian-SLAM to get a feel for neural-3D SLAM.

## Week 7-8: Planning + integration

- Stand up a small differential-drive robot in Gazebo + ROS2.
- Get Nav2 working: SLAM Toolbox -> costmaps -> planner -> controller.
- Implement Hybrid-A* from scratch for a car-like robot.

## Datasets

EuRoC, TUM RGB-D, KITTI, KITTI-360, nuScenes, Newer College, MulRan,
Hilti SLAM Challenge.

## Communities

ICRA, IROS, RSS conferences; OpenSLAM, ROS Discourse, Cyrill Stachniss's
"SLAM Lectures" YouTube channel.
