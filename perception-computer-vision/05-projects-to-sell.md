# Four Projects You Can Build and Sell

Each scoped to <= 1 month of focused work.

## 1. Phone-scan -> robot-ready 3D environment (~4 weeks)

User walks around a room with their phone; your service returns a
Gaussian splat + collision mesh + semantic segmentation suitable for
loading into Isaac Sim or Gazebo.

- **Stack:** iPhone capture app -> COLMAP/glomap -> gsplat -> Open3D mesh
  + SAM 2 semantic mask projection -> USD/URDF export.
- **Buyers:** robotics startups that need digital twins of customer sites
  but don't have an in-house 3D team.
- **Pricing:** $1-5k per scene; or $500/mo subscription for unlimited
  small scenes.

## 2. 6-DoF pose-estimation API for industrial parts (~3 weeks)

Customer uploads a CAD model; your service returns a fine-tuned
FoundationPose / MegaPose checkpoint and a REST endpoint that returns
6-DoF pose from an RGB-D image.

- **Stack:** FoundationPose + a small synthetic data pipeline in
  BlenderProc / Isaac Sim Replicator -> Triton inference server.
- **Buyers:** bin-picking integrators, contract manufacturers, machine
  vision shops.
- **Pricing:** $2-10k setup + $0.01-0.10 per inference.

## 3. Visual-inspection-as-a-service (~2-3 weeks)

Web UI where a customer uploads 50 "good" and 50 "bad" product images;
you train an anomaly-detection model (PatchCore, EfficientAD, or DINOv2
+ kNN) and deliver a deployable container.

- **Stack:** anomalib or custom DINOv2-based detector -> ONNX/TensorRT
  export -> Docker image with REST endpoint.
- **Buyers:** QC departments at small-to-mid manufacturers — they pay
  well and have low ML maturity.
- **Pricing:** $5-25k per defect class, recurring support fees.

## 4. Real-time SLAM benchmark + tuning service (~3 weeks)

Tool that ingests a customer's ROS bag, runs ORB-SLAM3 / VINS-Fusion /
OpenVSLAM with several parameter sets, and produces a tuning report with
parameter recommendations and accuracy comparisons.

- **Stack:** evo (evaluation tool), Docker images of major SLAM systems,
  parameter sweep harness, PDF report generator.
- **Buyers:** drone and AMR teams whose engineers don't have time to
  benchmark SLAM variants themselves.
- **Pricing:** $2-5k per benchmark report, or a monthly CI add-on.
