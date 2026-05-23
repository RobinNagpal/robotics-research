# Important Things to Learn

## Physics simulation foundations

- Rigid-body dynamics, contact mechanics, constraint solvers.
- Time-stepping: explicit, semi-implicit, implicit; substepping.
- Soft body, cloth, fluids (when needed).
- Differentiable physics: MJX, Warp, Brax, Genesis, Drake autodiff.

## Rendering and assets

- USD (Universal Scene Description) — the lingua franca of modern
  sims.
- PBR materials, ray tracing basics, NVIDIA RTX rendering.
- Procedural generation: Houdini-style, USD composition arcs.
- 3D Gaussian Splatting, NeRF, neural reconstruction for twin assets.
- Polycam / Luma / Matterport workflows for scanning real environments.

## Sim2Real

- Domain randomization (textures, lighting, physics, sensor noise).
- System identification, real-to-sim asset capture.
- RMA (Rapid Motor Adaptation), DR + privileged information.
- Cosmos / world models for video-level data augmentation.

## Synthetic data

- Replicator (Isaac Sim's domain-randomization framework).
- BlenderProc, NVISII for procedural data.
- Annotation generation: 2D/3D boxes, segmentation, depth, normals,
  optical flow.

## Tools and platforms

- **Isaac Sim + Isaac Lab** for high-fidelity GPU-parallel training.
- **MuJoCo / MJX** for fast research iteration.
- **Genesis** for unified fast sim (2024+).
- **Gazebo Garden** for ROS2-native sim.
- **Drake** for model-based.
- **CARLA / DRIVE Sim** for AV.

## Standards and ecosystems

- USD, OpenUSD, Pixar USD docs.
- ROS2 + gz_ros2_control, isaac_ros.
- glTF, OBJ, FBX import/export.
- AnyMAL OpenUSD assets, NVIDIA SimReady asset standard.

## Must-read papers

"Domain Randomization" (Tobin et al.), "Sim-to-real via RMA" (Kumar et
al.), "Isaac Lab" (Mittal et al., 2023), "RoboCasa", "MimicGen",
"DextrAH", Tobias Lasser's lectures on differentiable rendering.
