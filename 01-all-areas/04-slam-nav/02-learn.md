# Important Things to Learn

## Math foundations

- Lie groups: SO(3), SE(3) — every SLAM paper assumes this.
- Probabilistic state estimation: Kalman / EKF / UKF, particle filter,
  Rao-Blackwellized PF.
- Nonlinear least squares: Gauss-Newton, Levenberg-Marquardt.
- Factor graphs and incremental smoothing (iSAM2, GTSAM).
- Information theory basics for active SLAM and exploration.

## SLAM building blocks

- Feature-based vs direct vs learned front-ends.
- Loop closure (DBoW2, NetVLAD, place recognition).
- Bundle adjustment, pose-graph optimization.
- IMU pre-integration (Forster et al.).
- Sensor fusion: camera + IMU + LiDAR + GPS + wheel odometry.
- Map representations: sparse landmarks, occupancy grids, signed-distance
  fields, semantic maps, NeRF / Gaussian splat maps.

## Planning

- Search: A*, D*-Lite, Theta*, ARA*.
- Sampling: RRT, RRT*, RRT-Connect, BIT*, PRM.
- Trajectory optimization: CHOMP, TrajOpt, GPMP, MPC.
- Lattice / hybrid-A* (used heavily in AVs).
- Behavior planning: state machines, POMDPs, MCTS, learned policies.

## Local control / obstacle avoidance

- DWA, TEB, VFH for differential drive.
- MPC for cars and drones.
- Control barrier functions for safety.

## Tools

GTSAM, Ceres, g2o, OMPL, Nav2, MoveIt 2, ROS2, Foxglove, evo (eval).

## Must-read papers

ORB-SLAM3, VINS-Mono, FAST-LIO2, DROID-SLAM, Cartographer, Hybrid A*
(Dolgov), iSAM2, ViNT / NoMaD.
