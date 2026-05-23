# Four Projects You Can Build and Sell

## 1. SLAM tuning + benchmark report-as-a-service (~3 weeks)

Customer ships you a ROS bag from their robot. You run ORB-SLAM3,
VINS-Fusion, FAST-LIO2 (whichever fits their sensors) across a parameter
sweep, evaluate with evo, and deliver a PDF report with the best
configuration and tuned config files.

- **Buyers:** AMR, drone, and field-robotics startups with small teams.
- **Pricing:** $2-5k per report; $1k/mo retainer.

## 2. Indoor relocalization service from a phone scan (~4 weeks)

Customer scans their warehouse / office with an iPhone once. You build a
visual place-recognition index (NetVLAD or DINOv2) + a sparse 3D map. A
client SDK lets any cheap RGB camera localize against that map in
real time.

- **Stack:** hloc (hierarchical localization), COLMAP, NetVLAD,
  C++/Python SDK, REST or on-device ONNX.
- **Buyers:** AR companies, low-cost AMRs that can't afford LiDAR,
  inventory drones.
- **Pricing:** $5k setup + $200/mo per site.

## 3. GPS-denied drone navigation kit (~4 weeks)

Self-contained package: Jetson Orin Nano + RealSense + ArduPilot/PX4
integration + a tuned VINS-Fusion + obstacle-avoidance config + Nav2
glue. Sold as a bring-up service to drone teams that don't have a
perception engineer.

- **Buyers:** defense primes, inspection-drone companies, indoor-mapping
  startups.
- **Pricing:** $10-25k bring-up + hardware markup + retainer.

## 4. Map-versioning + change-detection SaaS (~3-4 weeks)

Web service that ingests sequential ROS bags / point clouds of the same
facility over time and produces a "diff" — what moved, what's new, what's
gone. Critical for warehouses and construction sites where the
environment changes weekly.

- **Stack:** ICP-based registration, voxelization + change masks,
  optional semantic labels with SAM 2, dashboard in React + deck.gl.
- **Buyers:** warehouse operators, construction-tech, facility managers.
- **Pricing:** $1-3k/mo per site, multi-site discounts.
